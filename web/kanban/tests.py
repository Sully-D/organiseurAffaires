import ast
import json
import re
from datetime import date
from html import unescape
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.template.loader import render_to_string

from .models import KanbanColumn
from .views import _attach_card_filter_json, board


BOARD_TEMPLATE = Path(__file__).resolve().parent / "templates" / "kanban" / "board.html"
BASE_TEMPLATE = Path(__file__).resolve().parent / "templates" / "kanban" / "base.html"
CARD_SNIPPET_TEMPLATE = Path(__file__).resolve().parent / "templates" / "kanban" / "card_snippet.html"
STYLE_CSS = Path(__file__).resolve().parent / "static" / "kanban" / "css" / "style.css"
VIEWS_PY = Path(__file__).resolve().parent / "views.py"


class RelatedList:
    def __init__(self, items):
        self.items = items

    def all(self):
        return self.items

    def count(self):
        return len(self.items)


class BoardFilterCatalogQueryTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def get_board_context(self):
        def render_stub(request, template_name, context):
            response = HttpResponse("")
            response.context_data = context
            return response

        request = self.request_factory.get("/")
        with (
            patch("kanban.views.render", side_effect=render_stub),
            patch.object(KanbanColumn.objects, "exclude") as exclude,
        ):
            exclude.return_value.order_by.return_value = []
            return board(request).context_data

    def assert_catalog_queryset(self, queryset, table_name):
        query = queryset.query
        sql = str(query)

        self.assertTrue(query.distinct)
        self.assertEqual(query.order_by, ("description",))
        self.assertEqual(query.values_select, ("description",))
        self.assertIn(f'"{table_name}"."description" IS NOT NULL', sql)
        self.assertIn(f'NOT ("{table_name}"."description" = ', sql)
        self.assertNotIn(f'"{table_name}"."done"', sql)

    def test_traitement_filter_catalog_includes_done_and_pending_non_empty_descriptions(self):
        context = self.get_board_context()

        self.assert_catalog_queryset(context["filter_traitements"], "traitements")

    def test_tache_filter_catalog_includes_done_and_pending_non_empty_descriptions(self):
        context = self.get_board_context()

        self.assert_catalog_queryset(context["filter_taches"], "taches")


class CardFilterJsonTests(SimpleTestCase):
    def build_activity(self):
        special = "Contrôle d'appel \"A\" <urgent> & final"
        scelle = SimpleNamespace(
            traitements=RelatedList([
                SimpleNamespace(description=special, done=True),
                SimpleNamespace(description="Controle restant", done=False),
                SimpleNamespace(description="", done=False),
            ]),
            taches=RelatedList([
                SimpleNamespace(description="Tâche faite", done=True),
                SimpleNamespace(description="Tache restante", done=False),
                SimpleNamespace(description="", done=True),
            ]),
        )
        return SimpleNamespace(
            id=1,
            name="Activite test",
            date=date(2026, 4, 25),
            description="Description",
            urgency_class="",
            pending_traitements=1,
            pending_taches=1,
            has_cta=False,
            has_reparations=False,
            tags=RelatedList([]),
            scelles=RelatedList([scelle]),
            column=SimpleNamespace(name="En cours"),
        )

    def test_card_filter_json_includes_done_pending_special_chars_and_omits_empty_descriptions(self):
        activity = self.build_activity()

        _attach_card_filter_json(activity)

        traitements = json.loads(activity.traitements_filter_json)
        taches = json.loads(activity.taches_filter_json)

        self.assertEqual(
            traitements,
            [
                {"description": "Contrôle d'appel \"A\" <urgent> & final", "done": True},
                {"description": "Controle restant", "done": False},
            ],
        )
        self.assertEqual(
            taches,
            [
                {"description": "Tâche faite", "done": True},
                {"description": "Tache restante", "done": False},
            ],
        )
        self.assertIs(type(traitements[0]["done"]), bool)
        self.assertNotIn('""', activity.traitements_filter_json)

    def test_card_snippet_renders_json_attributes_with_legacy_attributes(self):
        activity = _attach_card_filter_json(self.build_activity())

        html = render_to_string("kanban/card_snippet.html", {"activity": activity})

        self.assertIn("data-traitements=", html)
        self.assertIn("data-taches=", html)
        self.assertIn("data-pending-traitements=", html)
        self.assertIn("data-pending-taches=", html)
        self.assertIn("data-pending-traitement-names=", html)
        self.assertIn("data-pending-tache-names=", html)

        traitements_attr = re.search(r'data-traitements="([^"]*)"', html).group(1)
        taches_attr = re.search(r'data-taches="([^"]*)"', html).group(1)

        traitements = json.loads(unescape(traitements_attr))
        taches = json.loads(unescape(taches_attr))

        self.assertEqual(traitements[0]["description"], "Contrôle d'appel \"A\" <urgent> & final")
        self.assertIs(type(traitements[0]["done"]), bool)
        self.assertEqual(taches[0]["description"], "Tâche faite")


class BoardBusinessFilterScriptTests(SimpleTestCase):
    def get_board_template(self):
        return BOARD_TEMPLATE.read_text(encoding="utf-8")

    def get_base_template(self):
        return BASE_TEMPLATE.read_text(encoding="utf-8")

    def get_style_css(self):
        return STYLE_CSS.read_text(encoding="utf-8")

    def get_card_snippet_template(self):
        return CARD_SNIPPET_TEMPLATE.read_text(encoding="utf-8")

    def get_views_source(self):
        return VIEWS_PY.read_text(encoding="utf-8")

    def get_function_body(self, function_name):
        template = self.get_board_template()
        signature_start = template.find(f"function {function_name}(")
        self.assertNotEqual(signature_start, -1, f"{function_name} not found")

        body_start = template.find("{", signature_start)
        self.assertNotEqual(body_start, -1, f"{function_name} body not found")

        depth = 0
        for index in range(body_start, len(template)):
            if template[index] == "{":
                depth += 1
            elif template[index] == "}":
                depth -= 1
                if depth == 0:
                    return template[body_start + 1:index]

        self.fail(f"{function_name} body not closed")

    def test_board_template_exposes_business_filter_functions(self):
        template = self.get_board_template()

        for function_name in [
            "parseCardFilterData",
            "matchesItemFilter",
            "getGlobalFilterState",
            "matchesSearchText",
            "matchesLegacyGlobalFilter",
            "matchesBusinessFilters",
            "isCardVisible",
            "updateVisibleCounts",
            "updateNoFilterResults",
            "applyBoardFilters",
            "reapplyBoardFiltersAfterMutation",
            "syncBusinessFilterControlState",
            "updateBusinessFilterStateFromControls",
            "resetBusinessFilters",
        ]:
            self.assertIn(f"function {function_name}", template)
            self.assertIn(f"window.{function_name} = {function_name};", template)

    def test_matches_item_filter_uses_exact_labels_and_boolean_done_states(self):
        body = self.get_function_body("matchesItemFilter")

        self.assertIn("item.description !== selectedLabel", body)
        self.assertIn("item.done === true", body)
        self.assertIn("item.done === false", body)
        self.assertIn("(!doneChecked && !pendingChecked) || (doneChecked && pendingChecked)", body)
        self.assertNotIn(".includes(", body)
        self.assertNotIn("innerText", body)
        self.assertNotIn("toLowerCase", body)

    def test_apply_board_filters_centralizes_search_global_filter_and_business_filters(self):
        body = self.get_function_body("applyBoardFilters")

        self.assertIn("const globalState = getGlobalFilterState();", body)
        self.assertIn("matchesSearchText(card, globalState.query)", body)
        self.assertIn("matchesLegacyGlobalFilter(card, globalState.filterValue)", body)
        self.assertIn("matchesBusinessFilters(card, filterState)", body)
        self.assertIn("card.hidden = !visible;", body)
        self.assertIn("const totalVisible = updateVisibleCounts();", body)
        self.assertIn("updateNoFilterResults(totalVisible);", body)
        self.assertNotIn("hasActiveBusinessFilters", body)
        self.assertNotIn("style.display", body)

    def test_legacy_global_specific_filters_use_structured_exact_matching(self):
        body = self.get_function_body("matchesLegacyGlobalFilter")

        self.assertIn("data-pending-traitements", body)
        self.assertIn("data-pending-taches", body)
        self.assertIn("parseCardFilterData(card).traitements", body)
        self.assertIn("parseCardFilterData(card).taches", body)
        self.assertIn("matchesItemFilter", body)
        self.assertIn("target, false, false", body)
        self.assertNotIn("data-pending-traitement-names", body)
        self.assertNotIn("data-pending-tache-names", body)
        self.assertNotIn(".includes(", body)

    def test_base_global_search_delegates_to_board_filter_engine(self):
        template = self.get_base_template()
        script = template[template.find("<script>"):]

        self.assertIn("window.applyBoardFilters()", script)
        self.assertIn("searchInput.addEventListener('input', filterCards)", script)
        self.assertIn("filterSelect.addEventListener('change', filterCards)", script)
        self.assertNotIn("card.style.display", script)
        self.assertNotIn("data-pending-traitement-names", script)
        self.assertNotIn("data-pending-tache-names", script)

    def test_business_filter_bar_markup_uses_catalogs_and_stable_hooks(self):
        template = self.get_board_template()
        board_position = template.find('<div class="board-container">')

        self.assertIn('id="business-filter-bar"', template)
        self.assertLess(template.find('id="business-filter-bar"'), board_position)
        self.assertIn('id="business-filter-traitement"', template)
        self.assertIn('id="business-filter-tache"', template)
        self.assertIn("{% for t in filter_traitements %}", template)
        self.assertIn("{% for t in filter_taches %}", template)
        self.assertIn('<option value="">Traitement</option>', template)
        self.assertIn('<option value="">Tache</option>', template)

        for checkbox_id in [
            "business-filter-traitement-done",
            "business-filter-traitement-pending",
            "business-filter-tache-done",
            "business-filter-tache-pending",
        ]:
            self.assertIn(f'type="checkbox" id="{checkbox_id}" disabled', template)
            self.assertIn(f'<label for="{checkbox_id}">', template)

        self.assertIn('id="business-filter-reset"', template)

    def test_business_filter_controls_update_state_and_apply_filters(self):
        template = self.get_board_template()
        update_body = self.get_function_body("updateBusinessFilterStateFromControls")
        sync_body = self.get_function_body("syncBusinessFilterControlState")

        self.assertIn("window.businessFilterState = {", update_body)
        self.assertIn("traitementLabel: controls.traitementSelect.value", update_body)
        self.assertIn("traitementDone: controls.traitementDoneCheckbox.checked", update_body)
        self.assertIn("traitementPending: controls.traitementPendingCheckbox.checked", update_body)
        self.assertIn("tacheLabel: controls.tacheSelect.value", update_body)
        self.assertIn("tacheDone: controls.tacheDoneCheckbox.checked", update_body)
        self.assertIn("tachePending: controls.tachePendingCheckbox.checked", update_body)
        self.assertIn("window.applyBoardFilters();", update_body)
        self.assertIn("addEventListener('change', updateBusinessFilterStateFromControls)", template)
        self.assertIn("initializeBusinessFilterControls();", template)

        self.assertIn("controls.traitementDoneCheckbox.disabled = !hasTraitement;", sync_body)
        self.assertIn("controls.traitementPendingCheckbox.disabled = !hasTraitement;", sync_body)
        self.assertIn("controls.tacheDoneCheckbox.disabled = !hasTache;", sync_body)
        self.assertIn("controls.tachePendingCheckbox.disabled = !hasTache;", sync_body)
        self.assertIn("controls.traitementDoneCheckbox.checked = false;", sync_body)
        self.assertIn("controls.tachePendingCheckbox.checked = false;", sync_body)

    def test_business_filter_reset_only_clears_business_controls(self):
        body = self.get_function_body("resetBusinessFilters")

        self.assertIn("controls.traitementSelect.value = '';", body)
        self.assertIn("controls.tacheSelect.value = '';", body)
        self.assertIn("controls.traitementDoneCheckbox.checked = false;", body)
        self.assertIn("controls.traitementPendingCheckbox.checked = false;", body)
        self.assertIn("controls.tacheDoneCheckbox.checked = false;", body)
        self.assertIn("controls.tachePendingCheckbox.checked = false;", body)
        self.assertIn("updateBusinessFilterStateFromControls();", body)
        self.assertNotIn("global-search", body)
        self.assertNotIn("global-filter", body)

    def test_no_filter_results_message_is_available_and_hidden_by_default(self):
        template = self.get_board_template()
        board_position = template.find('<div class="board-container">')
        message_position = template.find('id="noFilterResults"')

        self.assertNotEqual(message_position, -1)
        self.assertLess(message_position, board_position)
        self.assertIn('id="noFilterResults"', template)
        self.assertIn('aria-live="polite"', template)
        self.assertIn('id="noFilterResults" aria-live="polite" hidden', template)
        self.assertIn("Aucune carte ne correspond aux filtres", template)

    def test_visible_count_helpers_use_hidden_cards_and_keep_columns_visible(self):
        template = self.get_board_template()
        is_visible_body = self.get_function_body("isCardVisible")
        counts_body = self.get_function_body("updateVisibleCounts")
        no_results_body = self.get_function_body("updateNoFilterResults")

        self.assertIn("return !card.hidden;", is_visible_body)
        self.assertIn("document.querySelectorAll('.kanban-column')", counts_body)
        self.assertIn("column.querySelectorAll('.activity-card')", counts_body)
        self.assertIn(".filter(isCardVisible).length", counts_body)
        self.assertIn("column.querySelector('.count')", counts_body)
        self.assertIn("countEl.innerText = visibleCount;", counts_body)
        self.assertIn("totalVisible += visibleCount;", counts_body)
        self.assertIn("return totalVisible;", counts_body)

        self.assertIn("document.getElementById('noFilterResults')", no_results_body)
        self.assertIn("noResults.hidden = totalVisible > 0;", no_results_body)
        self.assertNotIn(".kanban-column", no_results_body)
        self.assertNotIn("style.display", template)

    def test_business_filter_css_preserves_kanban_scroll_and_styles_controls(self):
        css = self.get_style_css()

        for selector in [
            ".business-filter-bar",
            ".business-filter-group",
            ".business-filter-select",
            "#business-filter-reset",
            "#noFilterResults",
        ]:
            self.assertIn(selector, css)

        self.assertIn("flex-wrap: wrap;", css)
        self.assertIn("background: rgba(30, 41, 59, 0.78);", css)
        self.assertIn("border: var(--glass-border);", css)
        self.assertIn("min-height: 38px;", css)
        self.assertIn("text-overflow: ellipsis;", css)
        self.assertIn("white-space: nowrap;", css)
        self.assertIn("outline: 2px solid var(--accent);", css)
        self.assertIn("accent-color: var(--accent);", css)
        self.assertIn("opacity: 0.45;", css)

        main_block = re.search(r"\.main-content\s*\{(?P<body>[^}]*)\}", css, re.S).group("body")
        self.assertIn("display: flex;", main_block)
        self.assertIn("flex-direction: column;", main_block)
        self.assertIn("min-height: 0;", main_block)

        board_block = re.search(r"\.board-container\s*\{(?P<body>[^}]*)\}", css, re.S).group("body")
        self.assertIn("flex: 1 1 auto;", board_block)
        self.assertIn("min-height: 0;", board_block)
        self.assertIn("overflow-x: auto;", board_block)
        self.assertIn("overflow-y: hidden;", board_block)

        column_block = re.search(r"\.kanban-column\s*\{(?P<body>[^}]*)\}", css, re.S).group("body")
        self.assertIn("flex: 0 0 300px;", column_block)

    def test_business_filter_css_has_responsive_layout_without_hiding_columns(self):
        css = self.get_style_css()

        self.assertIn("@media (max-width: 760px)", css)
        self.assertIn("flex-direction: column;", css)
        self.assertIn("align-items: stretch;", css)
        self.assertIn("max-width: none;", css)
        self.assertIn("#noFilterResults[hidden]", css)
        self.assertNotRegex(css, r"\.kanban-column(?:\[[^\]]+\])?\s*\{[^}]*display\s*:\s*none")
        self.assertNotIn(".activity-card[hidden]", css)

    def test_reapply_filters_helper_delegates_to_apply_board_filters(self):
        body = self.get_function_body("reapplyBoardFiltersAfterMutation")

        self.assertIn("if (window.applyBoardFilters)", body)
        self.assertIn("window.applyBoardFilters();", body)
        self.assertIn("applyBoardFilters();", body)

    def test_mutation_callbacks_reapply_filters_after_dom_changes(self):
        expectations = [
            ("sortColumn", "cards.forEach(card => columnBody.appendChild(card));"),
            ("createActivity", "column.appendChild(newCard);"),
            ("deleteActivity", "card.remove();"),
            ("cleanupDuplicates", "card.remove();"),
            ("refreshActivityColumns", "body.replaceChild(newCard, existingCard);"),
            ("refreshActivityColumns", "body.appendChild(newCard);"),
            ("refreshActivityColumns", "existingCard.remove();"),
            ("toggleDone", "targetBody.appendChild(card);"),
        ]

        for function_name, mutation in expectations:
            with self.subTest(function_name=function_name, mutation=mutation):
                body = self.get_function_body(function_name)
                mutation_index = body.find(mutation)
                helper_index = body.find("reapplyBoardFiltersAfterMutation()", mutation_index)
                self.assertNotEqual(mutation_index, -1, f"{mutation} not found in {function_name}")
                self.assertNotEqual(helper_index, -1, f"helper not called after {mutation} in {function_name}")

    def test_mutation_callbacks_use_central_filter_for_counts(self):
        for function_name in ["createActivity", "deleteActivity", "cleanupDuplicates", "refreshActivityColumns"]:
            with self.subTest(function_name=function_name):
                body = self.get_function_body(function_name)
                self.assertIn("reapplyBoardFiltersAfterMutation();", body)
                self.assertNotIn("innerText = parseInt", body)
                self.assertNotIn("innerText = Math.max", body)

    def test_sort_column_preserves_existing_sort_contracts_and_reapplies_filters(self):
        template = self.get_board_template()
        body = self.get_function_body("sortColumn")

        for criteria in ["date", "name", "pending-traitements", "pending-taches"]:
            self.assertIn(f"'{criteria}'", template)

        self.assertIn("const isNumeric = criteria === 'pending-traitements' || criteria === 'pending-taches';", body)
        self.assertIn("a.getAttribute(`data-${criteria}`)", body)
        self.assertIn("b.getAttribute(`data-${criteria}`)", body)
        self.assertIn("parseFloat(valA) || 0", body)
        self.assertIn("parseFloat(valB) || 0", body)
        self.assertIn("valA = (valA || '').toLowerCase();", body)
        self.assertIn("valB = (valB || '').toLowerCase();", body)

        append_index = body.find("cards.forEach(card => columnBody.appendChild(card));")
        reapply_index = body.find("reapplyBoardFiltersAfterMutation();", append_index)
        self.assertNotEqual(append_index, -1)
        self.assertNotEqual(reapply_index, -1)

    def test_modal_delegation_and_create_activity_click_remain_intact(self):
        template = self.get_board_template()
        create_body = self.get_function_body("createActivity")

        self.assertIn("document.querySelector('.board-container').addEventListener('click', function (e)", template)
        self.assertIn("const card = e.target.closest('.activity-card');", template)
        self.assertIn("if (!card) return;", template)
        self.assertIn("if (e.target.closest('.delete-activity-btn')) return;", template)
        self.assertIn("openModal();", template)
        self.assertIn("fetch(`/activity/${activityId}/`)", template)

        append_index = create_body.find("column.appendChild(newCard);")
        reapply_index = create_body.find("reapplyBoardFiltersAfterMutation();", append_index)
        click_index = create_body.find("newCard.click();", reapply_index)
        self.assertNotEqual(append_index, -1)
        self.assertNotEqual(reapply_index, -1)
        self.assertNotEqual(click_index, -1)

    def test_sortable_drag_and_drop_permissions_and_refresh_contracts_remain_intact(self):
        template = self.get_board_template()

        self.assertIn("Sortable.create(board, {", template)
        self.assertIn("disabled: {% if not user.is_superuser %}true{% else %}false{% endif %}", template)
        self.assertIn("fetch('{% url \"kanban:update_column_order\" %}'", template)
        self.assertIn("body: JSON.stringify({ order: order })", template)

        self.assertIn("Sortable.create(col, {", template)
        self.assertIn("group: 'shared'", template)
        self.assertIn("fetch('{% url \"kanban:move_activity\" %}'", template)
        self.assertIn("activity_id: activityId", template)
        self.assertIn("column_id: newColumnId", template)
        self.assertIn("cleanupDuplicates(activityId, itemEl);", template)
        self.assertIn("refreshActivityColumns(activityId);", template)

        card_snippet = self.get_card_snippet_template()
        self.assertIn('class="done-checkbox"', card_snippet)
        self.assertIn("{% if not user.is_superuser %}disabled{% endif %}", card_snippet)

    def test_neutral_filter_state_preserves_unfiltered_board_visibility(self):
        item_body = self.get_function_body("matchesItemFilter")
        global_body = self.get_function_body("matchesLegacyGlobalFilter")
        business_state_body = self.get_function_body("getBusinessFilterState")
        search_body = self.get_function_body("matchesSearchText")

        self.assertIn("if (!selectedLabel) return true;", item_body)
        self.assertIn("if (selectedFilter === 'all') return true;", global_body)
        self.assertIn("traitementLabel: ''", business_state_body)
        self.assertIn("tacheLabel: ''", business_state_body)
        self.assertIn("traitementDone: false", business_state_body)
        self.assertIn("traitementPending: false", business_state_body)
        self.assertIn("tacheDone: false", business_state_body)
        self.assertIn("tachePending: false", business_state_body)
        self.assertIn("if (!query) return true;", search_body)

    def test_virtual_column_queries_and_endpoint_contracts_remain_in_place(self):
        views_source = self.get_views_source()

        for column_name in ["Traitements", "Tâches", "CTA", "Réparations", "En attente", "En cours"]:
            self.assertIn(f'col.name == "{column_name}"', views_source)

        self.assertIn("def update_column_order(request):", views_source)
        self.assertIn("def move_activity(request):", views_source)
        self.assertIn("def create_activity(request):", views_source)
        self.assertIn("def delete_activity(request, activity_id):", views_source)
        self.assertIn("def get_activity_columns(request, activity_id):", views_source)

    def test_minimal_filter_tests_do_not_depend_on_production_database(self):
        tests_source = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(tests_source)
        django_test_imports = [
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "django.test"
            for alias in node.names
        ]
        class_base_names = [
            base.id
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
            for base in node.bases
            if isinstance(base, ast.Name)
        ]

        self.assertIn("SimpleTestCase", tests_source)
        self.assertIn("SimpleNamespace", tests_source)
        self.assertIn("RelatedList", tests_source)
        self.assertNotIn("TestCase", django_test_imports)
        self.assertNotIn("TestCase", class_base_names)
        self.assertNotRegex(tests_source, r"\.objects\.create\s*\(")
        self.assertNotIn("organiseur" + ".db", tests_source)

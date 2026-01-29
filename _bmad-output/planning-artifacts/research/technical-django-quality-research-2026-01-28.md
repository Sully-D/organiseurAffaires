---
stepsCompleted: [1, 2, 3]
inputDocuments: []
workflowType: 'research'
lastStep: 1
research_type: 'technical'
research_topic: 'Django Code Quality - Testing, Performance & Optimization'
research_goals: 'Assurer que le code Django est correct, fiable et robuste. Focus sur testing/couverture et performance/optimisation pour créer un plan d''amélioration.'
user_name: 'Sullivan'
date: '2026-01-28'
web_research_enabled: true
source_verification: true
---

# Research Report: Technical Research

**Date:** 2026-01-28
**Author:** Sullivan
**Research Type:** Technical Research
**Topic:** Django Code Quality - Testing, Performance & Optimization

---

## Technical Research Scope Confirmation

**Research Topic:** Django Code Quality - Testing, Performance & Optimization
**Research Goals:** Assurer que le code Django est correct, fiable et robuste. Focus sur testing/couverture et performance/optimisation pour créer un plan d'amélioration.

**Technical Research Scope:**

- Architecture Analysis - design patterns, frameworks, system architecture
- Implementation Approaches - development methodologies, coding patterns
- Technology Stack - languages, frameworks, tools, platforms
- Integration Patterns - APIs, protocols, interoperability
- Performance Considerations - scalability, optimization, patterns

**Research Methodology:**

- Current web data with rigorous source verification
- Multi-source validation for critical technical claims
- Confidence level framework for uncertain information
- Comprehensive technical coverage with architecture-specific insights

**Scope Confirmed:** 2026-01-28

---

## Technology Stack Analysis

### Testing Frameworks and Code Coverage

**Popular Testing Frameworks for Django (2024/2025):**

_pytest continues to be the leading framework for Django code quality testing, used with coverage.py (via pytest-cov) for measuring test coverage._ [High Confidence]

**Pytest for Django Testing:**
- `pytest` is highly recommended for its simple, readable syntax and extensive plugin ecosystem
- `pytest-django` plugin integrates seamlessly with Django for unit, functional, and API tests
- Compatible with Python 3.8+ and considered more user-friendly than unittest
- Key benefits: compact test management, easy plugin addition (pytest-html for reports), strong community support

**Code Coverage with Pytest-cov:**
- `coverage.py` is the standard tool for measuring code coverage in Python
- `pytest-cov` integrates coverage.py with pytest for Django projects
- Best practices 2024/2025:
  - Focus on meaningful coverage (critical business logic, edge cases)
  - High coverage % doesn't automatically mean high-quality tests
  - Integrate coverage reports into CI/CD pipelines
  - Regular monitoring of coverage trends

**Other Notable Testing Tools:**
- Django's built-in TestCase (`django.test.TestCase` for DB tests, `SimpleTestCase` without DB)
- REST Framework's `APITestCase` for API testing
- `factory_boy` for test data generation
- Selenium, Cypress.io, or Playwright for E2E testing

_Source: [FreeCodeCamp](https://www.freecodecamp.org), [OnGraph](https://www.ongraph.com), [GeeksforGeeks](https://www.geeksforgeeks.org)_

### Performance Optimization and Profiling Tools

**Django-Specific Profiling Tools:**

_Django Silk_ is the leading profiling tool specifically designed for Django applications in 2024. [High Confidence]
- Tracks requests, SQL queries, and rendering times
- Interactive UI to examine call graphs and identify optimization areas
- Can be configured for production use with data sampling
- Particularly useful for Django API performance analysis

**Advanced Profiling Tools:**
- **line_profiler**: Granular insights into Django model methods/properties performance
  - Details: time per method, total execution time, time per hit, number of hits
  - Ideal for optimizing heavy logic or database operations

- **Pyinstrument**: Visualizes call stacks and pinpoints bottlenecks in Python code
- **Scalene**: Memory and CPU profiling for Python, focused on large datasets
- **Python built-in profilers**: cProfile, profile modules

**Django Debug Toolbar:** [High Confidence]
- Remains highly recommended for development environments (2024)
- Real-time statistics and performance information in browser
- Panels for: SQL queries + execution times, cache performance, template rendering, code execution insights
- **WARNING**: For development only - not recommended for production due to unencrypted post data storage

_Source: [Medium Performance](https://medium.com), [TestDriven.io](https://testdriven.io), [PlainEnglish.io](https://plainenglish.io), [Django Project](https://djangoproject.com)_

### Code Quality and Static Analysis Tools

**Python Code Quality Tools Comparison (2024):**

**Ruff** - The Modern Choice [High Confidence]
- Extremely fast linter and formatter written in Rust
- Can replace Flake8, Pylint, isort, and approaching Black compatibility
- Designed for large codebases and CI/CD pipelines
- Formatter aims for 100% Black compatibility
- **2024 Trend**: Ruff + Mypy is the leading choice for modern Python development

**Pylint** - Comprehensive Static Analyzer
- Thorough code analyzer: errors, coding standards, code smells, refast factoring
- Extensive documentation and wide array of checks
- **Drawback**: Can be slower, more false positives requiring configuration
- Recent updates: Pylint 3.2.6 (July 2024), Pylint 3.0.4 (February 2024)

**Mypy** - Essential Type Checker [High Confidence]
- Static type checker for Python type annotations
- Critical for complex applications, catches type-related bugs early
- Gradual typing support - add type hints incrementally
- Most popular type checker, integrates with VS Code and PyCharm
- Recent versions: 1.14 (Dec 2024), 1.13 (Oct 2024), 1.12 (Oct 2024), 1.11 (July 2024)
- Added Python 3.12 syntax support and initial Python 3.13 support

**Black** - Opinionated Formatter
- Enforces consistent style with minimal configuration
- Uncompromising standard to end formatting bikeshedding
- Highly popular for ensuring code consistency
- Often used alongside linters and type checkers

**Recommended 2024 Stack for Django:**
```
Black (formatting) + Ruff (fast linting + import sorting) + Mypy (type checking)
```

This combination leverages each tool's strengths for high-quality, maintainable Python/Django code.

_Source: [Jit.io](https://jit.io), [HackMD](https://hackmd.io), [Frank-Mich](https://frank-mich.com), [Medium](https://medium.com), [Real Python](https://realpython.com)_

### Testing Best Practices and Strategies

**Multi-Layered Testing Approach (2024):**

**Unit Testing Best Practices:**
- Use `django.test.TestCase` for DB tests, `SimpleTestCase` for non-DB tests
- Employ `factory_boy` for test data generation (preferred over fixtures)
- Use `unittest.mock` to simulate external dependencies
- Organize tests into modules by functionality
- Descriptive test names indicating scenarios
- Speed optimization:
  - SQLite in-memory database for faster runs
  - Disable unnecessary logging/middleware
  - Consider disabling migrations for tests
  - Run tests in parallel
  - Use `InMemory Storage` to avoid disk access

**Integration Testing:**
- Test entire user workflows and database transactions
- Use `rest_framework.test.APITestCase` for Django REST APIs
- Validate HTTP status codes and database states
- Test authentication flows regularly
- Use Django's Test Client (`django.test.Client`) for HTTP request simulation
- Separate live external service tests from mocked tests

**End-to-End (E2E) Testing:**
- Simulate real user interactions across entire application
- Design tests mimicking actual user workflows
- Tools: Selenium, Cypress.io, Playwright, Django's `LiveServerTestCase`
- Use Page Object Model for maintainability
- Optimize with headless browser modes and parallel execution

**General Testing Recommendations 2024:**
- Follow testing pyramid: many fast unit tests, fewer integration tests, minimal E2E tests
- Integrate test suite into CI/CD pipelines
- Use `coverage.py` to measure and track coverage
- Focus on testing custom code and business logic (not Django/Python itself)
- Ensure test independence - no reliance on previous test state

_Source: [Medium Testing](https://medium.com), [Mozilla](https://mozilla.org), [Django Project](https://djangoproject.com), [PlainEnglish.io](https://plainenglish.io), [Honey Badger](https://honeybadger.io)_

### CI/CD Integration and Automation

**GitHub Actions for Django CI/CD (2024):**

_GitHub Actions has become the standard CI/CD platform for Django applications in 2024._ [High Confidence]

**Key Components:**
- **Workflow Definition**: YAML files in `.github/workflows/` directory
- **Trigger Events**: `push`, `pull_request`, custom events
- **Typical CI Pipeline Steps**:
  1. Style checkers (Black, Ruff)
  2. Static analysis (Mypy)
  3. Unit test runners (pytest)
  4. Code quality checks
  5. Security vulnerability scanning
  6. Database migrations
  7. Deployment to staging/production

**Pre-commit Hooks:**
- Client-side Git hooks that check code BEFORE commit
- Catches issues early in development cycle
- Common hooks: Black, Flake8/Ruff, isort
- **Best Practice 2024**: Pre-commit for fast local checks, comprehensive pytest in CI pipeline
- Avoid running full test suites in pre-commit (slows local development)
- GitHub Actions can enforce pre-commit checks even if local hooks bypassed

**CI/CD Best Practices 2024:**
- **Workflow Optimization**: Job dependencies, aggressive dependency caching, run quick checks before expensive ones
- **Security**: Pin GitHub Actions to specific versions (@v4 or commit SHA), define explicit `GITHUB_TOKEN` permissions
- **Branch Protection**: Require PR reviews and passing CI before merge
- **Environment Protection**: Set up reviewers and wait timers for production
- **Containerization**: Docker for consistency across dev/test/prod
- **Parallel Execution**: Run tests across multiple Python/database versions

_Source: [Medium GitH ub Actions](https://medium.com), [Dev.to](https://dev.to), [Digital Ocean](https://digitalocean.com), [Real Python](https://realpython.com), [GitHub](https://github.com)_

### Database Query Optimization

**Core Optimization Techniques:**

**select_related() and prefetch_related():** [High Confidence]
Both methods solve the \"N+1 query problem\" where accessing related objects in loops causes excessive queries.

- **`select_related()`**:
  - For `ForeignKey` and `OneToOneField` relationships
  - Performs SQL JOIN in single query
  - Fetches all data in one query, eliminating subsequent queries
  - Efficient for single-valued relationships

- **`prefetch_related()`**:
  - For `ManyToManyField` and reverse `ForeignKey` relationships
  - Performs separate lookup, then joins in Python memory
  - Uses `IN` clause for related objects
  - Avoids row duplication from JOINs
  - Effective for large numbers of related objects

**Database Indexing:** [High Confidence]
Critical for speeding up data retrieval, especially with large datasets.

**Django Indexing:**
- **Automatic**: Primary keys and foreign keys auto-indexed
- **Custom**: Use `Meta.indexes` or `db_index=True` on fields
- **Index Types**: Primary, Unique, Composite, Functional, Partial

**When to Index:**
- Frequently queried fields (WHERE, JOIN, ORDER BY clauses)
- Foreign keys and primary keys
- Composite indexes for multi-column queries

**Indexing Best Practices 2024:**
- Profile queries first to identify bottlenecks
- Avoid over-indexing (slows writes, consumes storage)
- Monitor and rebuild indexes regularly
- Test with `QuerySet.explain()` to ensure indexes are used
- Align indexes with actual query patterns

**Other Critical Optimizations:**
- **`only()` and `defer()`**: Load only necessary fields, reduce memory/network load
- **`annotate()` and `aggregate()`**: Push calculations to database (sums, counts, averages)
- **Caching**: Django's caching framework for frequently accessed, rarely changing data
- **Bulk Operations**: `bulk_create()`, `bulk_update()`, `bulk_delete()` for batch operations
- **Query Limits**: Always limit results on large tables, use pagination
- **`exists()` vs `count()`**: Use `exists()` for checking row existence (more efficient)
- **Profiling**: Use Django Debug Toolbar or `connection.queries` for continuous analysis

_Source: [Medium DB Optimization](https://medium.com), [Django Project](https://djangoproject.com), [TestDriven.io](https://testdriven.io), [YouTube Django](https://youtube.com), [HackerNoon](https://hackernoon.com)_

### Technology Adoption Trends 2024/2025

**Emerging Patterns:**
- **Ruff Adoption**: Replacing traditional linting toolchains (Flake8, Pylint, isort)
- **Type Checking Mainstream**: Mypy usage increasing for robust applications
- **CI/CD Automation**: GitHub Actions dominance for Django projects
- **Testing Framework Consolidation**: pytest-django as de facto standard
- **Performance Focus**: Increased use of profiling tools (Silk, line_profiler)
- **BDD and Property-Based Testing**: Growing adoption of Behave, Hypothesis

**Developer Preferences 2024:**
- Preference for fast, Rust-based tools (Ruff)
- All-in-one solutions over multiple tools
- Strong type safety with gradual adoption path
- Automation-first approaches (pre-commit, GitHub Actions)
- Performance monitoring integrated from development

---

## Integration Patterns Analysis

### Development Workflow Integration with Pre-commit Hooks

**Modern Django Workflow avec Pre-commit (2024):**

_Pre-commit hooks sont devenus la pratique standard pour automatiser les vérifications de code AVANT le commit._ [High Confidence]

**Setup Pre-commit:**
```bash
pip install pre-commit
pre-commit install  # Installe les Git hooks
```

**Configuration (.pre-commit-config.yaml):**
Exemple de configuration recommandée 2024 pour Django:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]
        
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.11
```

**Best Practices Pre-commit 2024:**
- **Fast checks only**: Linting, formatting uniquement (Ruff, Black, Mypy)
- **Avoid heavy tests**: Ne pas exécuter pytest dans pre-commit (ralentit le développement)
- **Auto-fix when possible**: `ruff --fix` auto-corrige les problèmes
- **Skip option**: Développeurs peuvent skip avec `--no-verify` si nécessaire
- **CI enforcement**: GitHub Actions doit réexécuter tous les checks même si pre-commit bypass

**Integration Benefits:**
- Catches issues immediately before commit
- Enforces consistent code style automatically
- Reduces CI pipeline failures
- Provides instant feedback to developers

_Source: [Medium Pre-commit](https://medium.com), [Pre-commit.com](https://pre-commit.com), [Dev.to](https://dev.to)_

### Continuous Quality Monitoring Integration

**SonarQube for Django (2024):** [High Confidence]

_SonarQube reste la plateforme robuste pour inspection continue de qualité et sécurité du code Django en 2024._

**Setup SonarQube Integration:**
1. **Server Setup**: Docker-based SonarQube server
   ```bash
   docker run -d -p 9000:9000 sonarqube:latest
   ```

2. **Project Configuration** (`sonar-project.properties`):
   ```properties
   sonar.projectKey=organiseur-affaires-django
   sonar.projectName=Organiseur Affaires Web
   sonar.sources=web/
   sonar.exclusions=**/migrations/**,**/static/**,**/venv/**
   sonar.python.version=3.11
   sonar.tests=web/kanban/tests/
   sonar.python.coverage.reportPaths=coverage.xml
   ```

3. **CI/CD Integration** (GitHub Actions example):
   ```yaml
   - name: SonarQube Scan
     uses: sonarsource/sonarqube-scan-action@master
     env:
       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
       SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
   ```

**SonarQube Benefits:**
- Comprehensive dashboard: coverage, complexity, maintainability
- Identifies bugs, vulnerabilities, code smells
- Automated code reviews on every commit
- Python 3.9+ support, updated SonarScanner 2024
- Quality gates: block merges if quality thresholds not met

**Code Climate for Django:**

Alternative platform for automated code review:
- Integrates with GitHub PRs for automatic review
- Configuration via `.codeclimate.yml`
- Part of CI/CD pipeline (GitHub Actions)
- Enforces code quality standards
- Identifies bottlenecks and improvements

_Source: [DZone](https://dzone.com), [CTO.ai](https://cto.ai), [Code Climate](https://codeclimate.com), [Buddy.works](https://buddy.works)_

### Centralized Configuration with pyproject.toml

**pyproject.toml as Single Source of Truth (2024):** [High Confidence]

_pyproject.toml est devenu le fichier de configuration central pour projets Python, consolidant settings pour pytest, coverage, ruff, mypy, etc._

**Complete pyproject.toml Example for Django Quality:**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "organiseur-affaires"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "django>=4.2",
    "djangorestframework>=3.14",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.7",
    "pytest-cov>=4.1",
    "ruff>=0.9.0",
    "mypy>=1.14",
    "black>=24.10",
    "django-stubs>=5.0",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "organiseur_web.settings"
python_files = ["test_*.py", "*_test.py"]
testpaths = ["web/kanban/tests"]
addopts = [
    "--cov=web/kanban",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--strict-markers",
]

[tool.coverage.run]
source = ["web/kanban"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false

[tool.ruff]
target-version = "py311"
line-length = 88
exclude = ["migrations", "venv", ".git"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "DJ",  # flake8-django
]

[tool.mypy]
python_version = "3.11"
plugins = ["mypy_django_plugin.main"]
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true

[tool.django-stubs]
django_settings_module = "organiseur_web.settings"

[tool.black]
line-length = 88
target-version = ["py311"]
exclude = '''
/(
    \.git
  | \.venv
  | migrations
)/
'''
```

**pyproject.toml Best Practices 2024:**
- **Single configuration file**: Replaces setup.py, setup.cfg, multiple .rc files
- **Editable install**: `pip install -e .` for development
- **src layout**: Organize project with `src/` folder for better imports
- **Tool-specific sections**: `[tool.pytest]`, `[tool.ruff]`, etc.
- **Version pinning**: Pin Python version and dependencies
- **Django-specific plugins**: django-stubs for mypy, flake8-django for ruff

_Source: [Python.org](https://python.org), [Lincoln Loop](https://lincolnloop.com), [Astral.sh](https://astral.sh), [GitHub Ruff](https://github.com)_

### Complete CI/CD Pipeline Pattern

**Recommended GitHub Actions Workflow 2024:**

```yaml
name: Django Quality Pipeline

on: [push, pull_request]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
    
    # Fast checks first
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Ruff Linting
      run: ruff check .
      
    - name: Ruff Format Check
      run: ruff format --check .
    
    - name: Mypy Type Checking
      run: mypy web/
    
    # Then tests
    - name: Run Tests with Coverage
      run: |
        pytest --cov --cov-report=xml
    
    - name: Upload Coverage to Codecov
      uses: codecov/codecov-action@v4
      
    # Optional: SonarQube
    - name: SonarQube Scan
      if: github.event_name == 'push'
      uses: sonarsource/sonarqube-scan-action@master
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**Pipeline Benefits:**
- **Fast feedback**: Linting avant tests (fail fast)
- **Parallel execution**: Jobs can run concurrently
- **Caching**: Dependencies cached for speed
- **Branch protection**: Require all checks pass before merge
- **Coverage tracking**: Automatic coverage reports
- **Quality gates**: SonarQube blocks poor quality code

### Tool Integration Ecosystem

**Complete Django Quality Stack 2024:**

```
┌─────────────────────────────────────────────────┐
│          Developer Workflow                      │
├─────────────────────────────────────────────────┤
│  Local Dev → Pre-commit → Push → CI/CD          │
│     ↓            ↓          ↓        ↓           │
│  IDE Tools   Ruff/Black   GitHub   Quality Gate │
│  (PyCharm)   Mypy         Actions   (SonarQube) │
└─────────────────────────────────────────────────┘

Configuration:
- pyproject.toml (single source)
- .pre-commit-config.yaml (Git hooks)
- .github/workflows/*.yml (CI/CD)
- sonar-project.properties (Quality monitoring)
```

**Integration Layers:**
1. **IDE Layer**: PyCharm/VSCode with Ruff, Mypy plugins
3. **CI/CD Layer**: GitHub Actions comprehensive validation
4. **Monitoring Layer**: SonarQube continuous quality tracking

---

## Synthèse Finale et Recommendations

### Key Research Findings

**1. Stack Recommandé 2024 pour Django Quality:**

```
Testing:        pytest-django + coverage.py + factory_boy
Code Quality:   Ruff + Black + Mypy (trio gagnant 2024)
Performance:    Django Silk + Debug Toolbar + line_profiler
CI/CD:          GitHub Actions + pre-commit hooks
Monitoring:     SonarQube (optionnel: Code Climate)
Configuration:  pyproject.toml (single source of truth)
```

**2. Tendances Majeures 2024/2025:**
- **Ruff dominance**: Remplace Flake8/Pylint/isort, ultra-rapide (Rust)
- **Type checking mainstream**: Mypy essentiel pour robustesse
- **Automation-first**: Pre-commit + GitHub Actions standard
- **Consolidated configuration**: pyproject.toml unifie tout

**3. Testing Best Practices:**
- Testing pyramid: beaucoup de unit tests, moins d'integration, minimal E2E
- pytest-django pour structure tests
- factory_boy pour données de test (vs fixtures)
- Coverage.py intégré dans CI/CD
- Tests rapides: SQLite in-memory, parallel execution

**4. Performance Critical Points:**
- **N+1 queries**: select_related() / prefetch_related() obligatoires
- **Indexing**: Index sur champs fréquemment requêtés
- **Profiling**: Django Silk pour production-like analysis
- **Caching**: Django cache framework pour queries répétitives
- **Bulk operations**: bulk_create/update/delete pour performance

**5. Integration Ecosystem:**
- Pre-commit hooks: fast local checks (linting, formatting)
- CI/CD: comprehensive validation (linting + typing + tests)
- Quality gates: SonarQube bloque merges de mauvaise qualité
- Configuration centralisée: pyproject.toml

---

### Action Plan pour organiseurAffaires

**Phase 1: Foundation Setup (Priorité HAUTE)**

**1.1 Configuration Centralisée**
```bash
# Créer pyproject.toml à la racine du projet
touch pyproject.toml
```

**Contenu pyproject.toml** (adapté au projet):
```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "organiseur-affaires"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "django>=4.2",
    "djangorestframework>=3.14",
    # Ajouter autres dépendances existantes
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.7",
    "pytest-cov>=4.1",
    "ruff>=0.9.0",
    "mypy>=1.14",
    "black>=24.10",
    "django-stubs>=5.0",
    "factory-boy>=3.3",
    "django-silk>=5.1",  # Pour profiling
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "organiseur_web.settings"
python_files = ["test_*.py", "*_test.py"]
testpaths = ["web/kanban/tests"]
addopts = [
    "--cov=web/kanban",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--strict-markers",
]

[tool.coverage.run]
source = ["web/kanban"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/venv/*",
]

[tool.ruff]
target-version = "py311"
line-length = 88
exclude = ["migrations", "venv", ".git"]

[tool.ruff.lint]
select = [
    "E", "W",  # pycodestyle
    "F",       # pyflakes
    "I",       # isort
    "B",       # flake8-bugbear
    "C4",      # flake8-comprehensions
    "DJ",      # flake8-django
]

[tool.mypy]
python_version = "3.11"
plugins = ["mypy_django_plugin.main"]
strict = false  # Commencer strict=false, augmenter progressivement
warn_return_any = true
warn_unused_configs = true

[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true

[tool.django-stubs]
django_settings_module = "organiseur_web.settings"

[tool.black]
line-length = 88
target-version = ["py311"]
exclude = '''
/(
    \.git
  | \.venv
  | migrations
)/
'''
```

**1.2 Installer les outils de qualité**
```bash
cd /path/to/organiseurAffaires
pip install -e ".[dev]"  # Installe toutes les dev dependencies
```

**1.3 Pre-commit hooks**
```bash
# Installer pre-commit
pip install pre-commit

# Créer .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]
        args: [--config-file=pyproject.toml]
EOF

# Installer les hooks
pre-commit install
```

---

**Phase 2: Testing Infrastructure (Priorité HAUTE)**

**2.1 Structure tests existants**
```
web/kanban/tests/
├── __init__.py
├── conftest.py          # Fixtures pytest communes
├── factories.py         # factory_boy factories
├── test_models.py      # Tests modèles
├── test_views.py       # Tests vues
├── test_api.py         # Tests API REST
└── test_integration.py # Tests d'intégration
```

**2.2 Créer factories.py**
```python
# web/kanban/tests/factories.py
import factory
from factory.django import DjangoModelFactory
from kanban.models import Task, Board  # Adapter aux modèles réels

class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board
    
    name = factory.Sequence(lambda n: f"Board {n}")

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task
    
    title = factory.Sequence(lambda n: f"Task {n}")
    board = factory.SubFactory(BoardFactory)
```

**2.3 Exemple test avec pytest-django**
```python
# web/kanban/tests/test_models.py
import pytest
from .factories import TaskFactory, BoardFactory

@pytest.mark.django_db
class TestTaskModel:
    def test_task_creation(self):
        task = TaskFactory(title="Test Task")
        assert task.title == "Test Task"
        assert task.board is not None
    
    def test_task_str_representation(self):
        task = TaskFactory(title="My Task")
        assert str(task) == "My Task"
```

**2.4 Exécuter tests et coverage**
```bash
# Lancer tous les tests avec coverage
pytest

# Voir coverage détaillé
pytest --cov --cov-report=html
# Ouvrir htmlcov/index.html dans browser

# Voir missing lines
pytest --cov --cov-report=term-missing
```

---

**Phase 3: Code Quality Checks (Priorité MOYENNE)**

**3.1 Linting avec Ruff**
```bash
# Check code quality
ruff check web/

# Auto-fix issues
ruff check --fix web/

# Format code
ruff format web/
```

**3.2 Type checking avec Mypy**
```bash
# Vérifier types
mypy web/

# Commencer progressivement: un module à la fois
mypy web/kanban/models.py
```

**3.3 Formatting avec Black** (optionnel si Ruff format suffit)
```bash
black web/
```

---

**Phase 4: Performance Optimization (Priorité MOYENNE)**

**4.1 Installer Django Debug Toolbar (dev)**
```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

**4.2 Installer Django Silk (profiling)**
```python
# settings.py
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

# urls.py
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

# Migrer
python manage.py migrate
```

**4.3 Optimiser queries critiques**
Identifier et corriger N+1 queries:
```python
# AVANT (N+1 problem):
tasks = Task.objects.all()
for task in tasks:
    print(task.board.name)  # Query pour chaque task!

# APRÈS (optimisé):
tasks = Task.objects.select_related('board').all()
for task in tasks:
    print(task.board.name)  # Pas de query supplémentaire
```

**4.4 Ajouter indexes**
```python
# models.py
class Task(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Index
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['board', 'status']),  # Composite index
        ]
```

---

**Phase 5: CI/CD Pipeline (Priorité MOYENNE-BASSE)**

**5.1 Créer GitHub Actions workflow**
```bash
mkdir -p .github/workflows
```

**5.2 Configuration .github/workflows/quality.yml**
```yaml
name: Django Quality Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Ruff Linting
      run: ruff check .
      
    - name: Ruff Format Check
      run: ruff format --check .
    
    - name: Mypy Type Checking
      run: mypy web/
      continue-on-error: true  # Ne pas bloquer au début
    
    - name: Run Tests with Coverage
      run: |
        pytest --cov --cov-report=xml
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v4
      if: github.event_name == 'push'
```

---

**Phase 6: Continuous Monitoring (Optionnel)**

**6.1 SonarQube (optionnel, pour projets + grands)**
```bash
# Docker SonarQube
docker run -d -p 9000:9000 sonarqube:latest
```

**6.2 sonar-project.properties**
```properties
sonar.projectKey=organiseur-affaires
sonar.projectName=Organiseur Affaires
sonar.sources=web/
sonar.exclusions=**/migrations/**,**/static/**,**/venv/**
sonar.python.version=3.11
sonar.tests=web/kanban/tests/
sonar.python.coverage.reportPaths=coverage.xml
```

---

### Priorisation Recommendations

**🔴 CRITIQUE (Faire immédiatement):**
1. ✅ Setup pyproject.toml avec configuration centralisée
2. ✅ Installer pre-commit hooks (Ruff + Mypy)
3. ✅ Configurer pytest-django avec structure tests de base
4. ✅ Créer factories pour génération données test

**🟡 IMPORTANT (Semaine 1-2):**
5. ✅ Écrire tests unitaires pour modèles critiques
6. ✅ Setup coverage tracking (75%+ target)
7. ✅ Installer Django Debug Toolbar
8. ✅ Identifier et corriger N+1 queries principales

**🟢 BÉNÉFIQUE (Semaine 3-4):**
9. ✅ Setup GitHub Actions CI/CD
10. ✅ Ajouter Django Silk pour profiling
11. ✅ Ajouter type hints progressivement (mypy strict mode)
12. ✅ Optimiser indexes database

**🔵 OPTIONNEL (Long terme):**
13. ⭕ SonarQube pour monitoring continu
14. ⭕ Integration tests complets
15. ⭕ E2E tests (Selenium/Playwright)

---

### Success Metrics

**Objectifs à 1 mois:**
- ✅ Pre-commit hooks actifs
- ✅ pytest-django configuré
- ✅ Coverage ≥ 60% sur code métier
- ✅ Ruff linting: 0 erreurs
- ✅ N+1 queries critiques résolus

**Objectifs à 3 mois:**
- ✅ Coverage ≥ 75%
- ✅ CI/CD pipeline fonctionnel
- ✅ Mypy type checking sur 50% du code
- ✅ Performance baseline établie (Silk)
- ✅ Indexes optimisés

**Long terme (6+ mois):**
- ✅ Coverage ≥ 85%
- ✅ Mypy strict mode partout
- ✅ Monitoring continu (SonarQube)
- ✅ Zero technical debt backlog
- ✅ Documentation complète

---

### Quick Start Commands

```bash
# 1. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. Installer dépendances dev
pip install -e ".[dev]"

# 3. Setup pre-commit
pre-commit install

# 4. Vérifier qualité code
ruff check web/
ruff format web/

# 5. Lancer tests
pytest --cov

# 6. Vérifier types
mypy web/

# 7. Développement: pre-commit vérifie automatiquement à chaque commit
git add .
git commit -m "Setup quality tools"  # Pre-commit hooks s'exécutent
```

---

## Research Completion

**Date de fin:** 2026-01-28  
**Portée complétée:**
- ✅ Technology Stack Analysis
- ✅ Integration Patterns Analysis  
- ✅ Performance Considerations (intégrés)
- ✅ Synthèse et Action Plan

**Prochaines étapes recommandées:**
1. Commencer Phase 1: Setup pyproject.toml + pre-commit
2. Phase 2: Tests infrastructure (pytest-django + factories)
3. Itération progressive sur coverage et quality

**Document prêt pour:**
- Plan d'amélioration détaillé
- Implémentation immédiate
- Suivi métrique de progression

---

---
title: 'Corriger le défilement vertical de la page Synthèse'
slug: 'fix-scrolling-synthese'
created: '2026-01-29T20:54:17+01:00'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Django 4.x', 'Vanilla CSS', 'HTML5']
files_to_modify: ['web/kanban/templates/kanban/synthese.html']
code_patterns: ['Fixed-header layout', 'Individual page scrolling', 'BEM-ish CSS naming']
test_patterns: ['Manual cross-browser confirmation']
---

# Tech-Spec: Corriger le défilement vertical de la page Synthèse

**Created:** 2026-01-29T20:54:17+01:00

## Overview

### Problem Statement

La page de synthèse (`/synthese/`) ne permet pas de faire défiler le contenu verticalement lorsque le nombre d'activités est important. Cela est dû à la structure CSS globale qui définit `overflow: hidden` sur le conteneur principal (`.main-content`), attendant que chaque page gère son propre défilement.

**Vérification :** Le conteneur actuel à la ligne 4 de `synthese.html` est `<div class="container-fluid" style="padding: 2rem;">` et se ferme à la ligne 131.

### Solution

Envelopper le contenu de la page dans un conteneur défilable. Utiliser la classe `.board-container` (déjà définie en CSS) avec des surcharges inline pour transformer le layout flex horizontal en un bloc défilable verticalement, tout en conservant la gestion de la hauteur.

**Justification des styles inline :** Les styles inline sont utilisés ici pour éviter de polluer le fichier CSS global avec une classe utilisée une seule fois. Cela maintient la modification localisée et facile à identifier.

### Scope

**In Scope:**
- Modification de `web/kanban/templates/kanban/synthese.html` lignes 4 et 131.
- Tests de compatibilité sur Chrome 90+, Firefox 88+, Safari 14+, Edge 90+.
- Validation de l'accessibilité (navigation clavier, lecteurs d'écran).

**Out of Scope:**
- Modifications des fichiers CSS statiques.
- Changements fonctionnels autres que le défilement.
- Optimisation des performances (aucun problème de performance identifié).

## Context for Development

### Codebase Patterns

L'application utilise une mise en page fixe où le header est permanent et le contenu défile à l'intérieur de `.main-content`. La structure attendue pour permettre le défilement est un conteneur avec `height: 100%` et `overflow-y: auto`.

### Files to Reference

| File | Purpose |
| ---- | ------- |
| [web/kanban/templates/kanban/synthese.html](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/templates/kanban/synthese.html) | Template à modifier |
| [web/kanban/templates/kanban/archives.html](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/templates/kanban/archives.html) | Exemple de page fonctionnelle avec scroll vertical |
| [web/kanban/static/kanban/css/style.css](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/static/kanban/css/style.css) | Définitions CSS globales |

### Technical Decisions

**Utilisation de `.board-container` avec `display: block` :**
La classe `.board-container` (définie dans `style.css` lignes 101-107) fournit `height: 100%`, ce qui est nécessaire pour que le défilement fonctionne dans `.main-content`. En forçant `display: block` via style inline, on évite le comportement `display: flex` par défaut (utilisé pour le Kanban horizontal) tout en conservant la gestion de la hauteur. La classe a `padding-bottom: 1rem` par défaut, qui sera écrasé par notre `padding: 2rem` inline.

**Navigateurs cibles :**
- Chrome/Edge 90+ (Windows, macOS, Linux)
- Firefox 88+ (Windows, macOS, Linux)
- Safari 14+ (macOS, iOS)

**Accessibilité :**
- Navigation clavier : Le défilement doit fonctionner avec les touches fléchées, Page Up/Down, Home/End.
- Lecteurs d'écran : Le contenu défilant doit rester annoncé correctement (pas de `aria-hidden` problématique).
- Contraste : Pas d'impact car on ne change que le défilement.

## Implementation Plan

### Tasks

- [ ] Task 1: Remplacer le conteneur de base dans `synthese.html`
  - **File:** `web/kanban/templates/kanban/synthese.html`
  - **Lignes:** 4 et 131
  - **Action:** Remplacer la ligne 4 et conserver la fermeture à la ligne 131.
  - **Code avant (ligne 4) :**
    ```html
    <div class="container-fluid" style="padding: 2rem;">
    ```
  - **Code après (ligne 4) :**
    ```html
    <div class="board-container" style="display: block; overflow-y: auto; padding: 2rem;">
    ```
  - **Notes:** 
    - `.board-container` fournit déjà `height: 100%` via CSS.
    - `display: block` écrase le `display: flex` par défaut.
    - `overflow-y: auto` active le scroll vertical.
    - `padding: 2rem` maintient l'espacement actuel.

### Acceptance Criteria

- [ ] **AC 1 - Défilement vertical fonctionnel :** Given une fenêtre de navigateur de 800px de hauteur avec 20+ activités affichées, when j'accède à `/synthese/`, then une barre de défilement verticale apparaît et je peux voir toutes les activités en défilant jusqu'en bas.

- [ ] **AC 2 - Header fixe :** Given la page défilée à mi-hauteur, when je regarde le haut de l'écran, then le header de navigation avec le logo et le menu reste visible et fixe.

- [ ] **AC 3 - Défilement smooth :** Given la page avec scroll activé, when je fais défiler avec la molette de la souris ou le trackpad, then le défilement est fluide sans saccades ni glitches visuels.

- [ ] **AC 4 - Scrollbar visible :** Given la page avec contenu débordant, when j'observe la partie droite de la fenêtre, then la scrollbar est visible et utilisable (sur Windows/Linux, peut être cachée sur macOS selon les préférences système).

- [ ] **AC 5 - Navigation clavier :** Given la page en focus, when j'utilise les touches fléchées haut/bas, Page Up/Down, Home/End, then le défilement fonctionne correctement.

- [ ] **AC 6 - Responsive mobile :** Given un viewport de 375px de largeur (iPhone), when j'accède à `/synthese/`, then le défilement vertical fonctionne sans overflow horizontal.

- [ ] **AC 7 - Pas de régression :** Given les autres pages (board, archives), when je navigue entre elles, then leur défilement respectif fonctionne toujours correctement.

## Additional Context

### Dependencies

- Aucune dépendance externe.

### Testing Strategy

**Tests de compatibilité navigateur :**

1. **Chrome 90+ (Windows/macOS/Linux) :**
   - Redimensionner la fenêtre à 1920x1080, puis 1366x768, puis 800x600.
   - Vérifier le défilement vertical avec molette, scrollbar, et touches fléchées.
   - Ouvrir DevTools et tester en mode responsive (iPhone SE, iPad).

2. **Firefox 88+ (Windows/macOS/Linux) :**
   - Mêmes tests que Chrome.
   - Vérifier que la scrollbar personnalisée (si présente dans CSS) s'affiche correctement.

3. **Safari 14+ (macOS/iOS) :**
   - Tester sur macOS avec trackpad (geste de défilement).
   - Tester sur iPhone/iPad en mode portrait et paysage.

4. **Edge 90+ (Windows) :**
   - Mêmes tests que Chrome.

**Test d'accessibilité :**

- Naviguer avec Tab jusqu'à la zone de contenu, puis utiliser les touches fléchées pour défiler.
- Tester avec NVDA (Windows) ou VoiceOver (macOS) pour vérifier que le contenu est correctement annoncé.

**Test de régression :**

- Vérifier que `/` (board) et `/archives/` conservent leur défilement respectif.

**Baseline de performance (optionnel) :**

- Mesurer le temps de First Contentful Paint (FCP) avant et après modification avec Lighthouse (cible : différence < 100ms).

### Notes

**Plan de rollback :**

Si le changement provoque des problèmes après déploiement :
1. Revenir à la version précédente via Git : `git revert <commit-hash>`
2. Ou restaurer manuellement la ligne 4 : `<div class="container-fluid" style="padding: 2rem;">`
3. Redéployer immédiatement

**Risques identifiés et mitigation :**

- **Risque F8 (padding conflict) :** Vérifié que `.board-container` a `padding-bottom: 1rem` qui sera écrasé par `padding: 2rem` inline (spécificité supérieure). Aucun conflit attendu.

- **Risque F7 (responsive) :** `.board-container` n'a pas de media queries dans `style.css` lignes 101-107. Le comportement sera identique sur mobile/tablette.

- **Risque F11 (structure HTML) :** Vérification manuelle effectuée - le `div.container-fluid` existe bien à la ligne 4 de la version actuelle.

**Améliorations futures (hors scope) :**

- Créer une classe CSS dédiée `.synthese-container` si d'autres pages nécessitent le même pattern.
- Ajouter des tests automatiques Playwright pour valider le défilement.

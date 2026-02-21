# PLAN-mobile-responsive.md

## Context
- **User Request**: Audit codebase for responsive units (em/rem instead of px), center sections vertically/horizontally, fix mobile scrolling, and implement a floating bottom bar for mobile navigation using `ui-ux-pro-max` and `visual-coding-kimi` principles.
- **Mode**: PLANNING

---

## 🏗️ Architecture & Changes

### 1. UX Audit & Responsive Units (px -> rem/em)
- **Target**: `src/styles/_tokens.scss`, `src/styles/components/_card.scss`, `src/styles/components/_button.scss`, `src/styles/layout/_grid.scss`.
- **Action**: Convert all hardcoded pixel values (except 1px borders) to `rem`. 
  - `xs: 0.25rem`, `sm: 0.5rem`, `md: 1rem`, `lg: 1.5rem`, `xl: 2rem`, `2xl: 3rem`, `3xl: 4rem`.
  - Border radius: `12px` -> `0.75rem`, `8px` -> `0.5rem`.
  - Media queries: `1024px` -> `64em`, `768px` -> `48em`.

### 2. Centering Sections
- **Target**: `src/styles/layout/_grid.scss` (`.pf-section-content`)
- **Action**: Add `align-items: center` and adjusting flex layout so content is perfectly centered horizontally and vertically, as requested.

### 3. Mobile Scroll Fix
- **Target**: `src/styles/layout/_grid.scss` and `src/app/page.tsx`
- **Root Cause**: The mobile override (`@media (max-width: 1024px)`) sets `height: auto` on `.pf-layout` and `.pf-scroll-container`, but `.pf-page` or `html/body` might not be allowing native page scroll.
- **Action**: Ensure `html, body { overflow-x: hidden; height: auto; }` works correctly for mobile, and the `scroll-snap` is properly disabled or re-configured for mobile touch interactions.

### 4. Floating Bottom Navigation (Mobile)
- **Target**: `src/components/Sidebar.tsx` (or new `MobileNav.tsx`) and SCSS.
- **Design Guidelines (`ui-ux-pro-max`)**:
  - Glassmorphism: `background: rgba(var(--color-surface-rgb), 0.8)`, `backdrop-filter: blur(12px)`.
  - Spacing: Floating above bottom edge (`bottom: 1.5rem`), rounded pill shape (`border-radius: 9999px`).
  - Interaction: High contrast active state, icon + text or icon-only for space.
- **Implementation**: Hide sidebar nav on mobile `(< 1024px)`, render a fixed bottom bar with `Magnet` and React Lucide icons mapped to `SECTIONS`.

---

## 📋 Task Breakdown

- [ ] **Task 1: CSS Refactoring & Audit**
  - Update `_tokens.scss` to use `rem`.
  - Replace `px` in `_button.scss`, `_card.scss`, `_react-bits.scss`.
- [ ] **Task 2: Layout Centering & Mobile Scroll**
  - Update `_grid.scss` `.pf-section-content` for horizontal/vertical centering.
  - Fix mobile overflow issues allowing native touch scrolling.
- [ ] **Task 3: Mobile Floating Nav**
  - Create `MobileNav.tsx` generic component.
  - Implement glassmorphism bottom bar UI.
  - Integrate in `page.tsx` (conditionally visible via CSS/JS).

---

## ✅ Verification Checklist
- Content is centered on both desktop & mobile.
- No `px` values used for padding/margin/layout sizing in SCSS components.
- Mobile scroll works natively and smoothly.
- Floating bottom bar appears on mobile screens (<1024px) and navigates correctly.

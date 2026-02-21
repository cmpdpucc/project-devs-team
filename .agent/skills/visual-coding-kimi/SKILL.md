---
name: visual-coding-kimi
description: Master guide for transforming visual sketches into Pixel-Perfect React/Tailwind code using Kimi 2.5.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Visual Coding with Kimi 2.5

> **Objective:** Transform low-fidelity sketches or high-fidelity screenshots into production-ready React + Tailwind CSS code with extreme precision.

---

## 1. Core Directives

### 🧠 Thinking Mode (Phase 1)
Before writing a single line of code, Kimi must **verbally analyze** the image.

| Step | Action | Focus |
|------|--------|-------|
| **1. Layout** | Identify grid/flex structures | Rows, Columns, Gaps, Alignment |
| **2. Components** | Break down into atoms/molecules | Buttons, Cards, Inputs, Navbars |
| **3. Design System** | Extract visual tokens | Colors, Typography, Spacing (p-4, m-2), Shadows |
| **4. Interactivity** | Anticipate user states | Hover, Focus, Active, Disabled |

### 🎯 Pixel Perfect (Phase 2)
The output must match the visual reference as closely as possible.

| Aspect | Rule |
|--------|------|
| **Spacing** | Use Tailwind's scale (`p-4` = 1rem). Guess relative proportions if exact px is unknown. |
| **Typography** | Match font weights (`font-bold`, `font-medium`) and sizes (`text-xl`, `text-sm`) accurately. |
| **Colors** | Approximate Tailwind colors (`bg-blue-500`) or use arbitrary values (`bg-[#1a2b3c]`) if strictly necessary. |
| **Radius** | Observe corner rounding (`rounded-lg`, `rounded-full`). |

---

## 2. Kimi 2.5 Prompt Templates

Use these prompts to instruct the vision model.

### Template A: The "Architect" (Complex Layouts)
> Use this for full page layouts or complex dashboards.

```text
ACT AS: Frontend Architect & UI Designer.
TASK: Convert this image into a React (Next.js/Vite) component using Tailwind CSS.

### 🧠 THINKING MODE
1. Analyze the layout structure (Flex vs Grid).
2. Identify repeating components (create map/loops).
3. List all necessary Tailwind utility classes for the container.

### 🎯 PIXEL PERFECT CODE
- Use `lucide-react` for icons.
- Use `clsx` or `tailwind-merge` if conditional logic is needed.
- Ensure responsive design (mobile-first).
- OUTPUT: Single file React component.
```

### Template B: The "Component" (Specific UI Elements)
> Use this for isolated components like Cards, Modals, or Headers.

```text
ACT AS: Senior React Developer.
TASK: Recreate this specific component with pixel-perfect precision.

### 🧠 THINKING MODE
- Detect shadow depth (`shadow-md`, `shadow-xl`).
- Analyze border usage (`border`, `divide-y`).
- Check for gradients or background patterns.

### 🎯 PIXEL PERFECT CODE
- Hardcode text from the image for fidelity.
- Use semantic HTML (`<article>`, `<section>`, `<button>`).
- Implement hover states seen or implied.
```

---

## 3. React & Tailwind Standards

### Code Structure

| Feature | Standard |
|---------|----------|
| **Framework** | React 18+ (Functional Components) |
| **Styling** | Tailwind CSS (Utility-first) |
| **Icons** | `lucide-react` (Default) |
| **Images** | Use placeholders (`https://placehold.co/600x400`) if assets missing |

### Anti-Patterns to Avoid

| ❌ Don't | ✅ Do |
|----------|-------|
| **Fixed Widths** | Use `w-full`, `max-w-md`, `flex-1` |
| **Magic Numbers** | Use Tailwind spacing scale (`gap-4`) |
| **Div Soup** | Use Semantic tags (`<main>`, `<header>`) |
| **Inline Styles** | Use Tailwind classes or `style={{ variable }}` only for dynamic values |

---

## 4. Execution Workflow for Agent

1. **Receive Image**: User uploads sketch/screenshot.
2. **Select Template**: Choose Template A or B based on scope.
3. **Run Kimi**: Send prompt + image.
4. **Refine**: If output drifts from design, reply with: *"Review the padding on the card header, it looks too tight compared to the image. Fix using 'Thinking Mode'."*
5. **Implement**: Save the code to `.tsx` file using `write` tool.

> **Pro Tip:** If the design is abstract, ask Kimi to "Improvise a modern UI based on this wireframe" to fill in the gaps with high-quality defaults.

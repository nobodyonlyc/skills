# Prototype Quality Rubric — "what a good screen looks like"

A prototype is only done when each screen passes this rubric, not merely when
every screen on the coverage checklist exists. Completeness ≠ quality. Self-check
every screen against these before any preview; a design critic ([workflow-prototype
Phase 3](../../workflow-prototype/references/phase-3-preview-feedback.md)) scores
against the same list.

Score each screen on the eight dimensions below. A screen "passes" only when none
are **Fail**; treat any Fail as a fix before preview.

## 1. Visual hierarchy
- One clear primary action per screen (a single dominant button); secondary/tertiary actions are visually demoted.
- Type, weight, and color guide the eye top-down: page title → section headers → body → captions. Nothing competes.
- **Fail:** everything is the same size/weight; two buttons fight to be "the" primary.

## 2. Spacing & rhythm
- Consistent spacing scale (4/8pt grid) — margins and padding are multiples of the spacing tokens, not arbitrary px.
- Generous whitespace; content is grouped by proximity, not crammed edge-to-edge.
- Aligned to a grid; no ragged left edges or off-by-a-few-px drift between sibling elements.
- **Fail:** cramped, inconsistent gutters, elements touching container edges.

## 3. Color & contrast
- Uses the design-system tokens only — no ad-hoc hex values per screen.
- Body text meets **WCAG AA** (≥ 4.5:1; ≥ 3:1 for large text). Muted text is still legible.
- Color carries meaning consistently (semantic success/warning/danger), never decoration alone.
- **Fail:** low-contrast grey-on-grey; raw colors invented per screen.

## 4. Typography
- A real type scale (not two arbitrary sizes); line-height ~1.4–1.6 for body; line length ~45–75 chars.
- Numerals/labels/headings use deliberate weights; no all-bold or all-regular screens.
- **Fail:** default browser type, walls of same-size text, unreadable line length.

## 5. Component polish & states
- Buttons, inputs, cards share consistent radius, border, shadow, and padding (from tokens).
- Every interactive element shows **hover / focus / active / disabled**; focus rings are visible (keyboard a11y).
- Inputs show label, placeholder, and at least one **validation/error** state.
- **Fail:** flat un-styled controls, no hover/focus, invisible focus ring.

## 6. Realistic content (no lorem, no placeholders)
- Real-feeling copy, names, dates, numbers ("Welcome back, Jane Doe", "₫1,240,000", "3 days ago") — never "Title goes here" or `[Image]`.
- Real placeholder imagery/avatars (e.g. `https://placehold.co/...`, icon set) and plausible data volumes (not one row).
- **Fail:** Lorem Ipsum, `[Image here]`, single demo row.

## 7. Edge / data states
- Each data view mocks **empty**, **loading** (skeleton/spinner), and **error** in addition to the populated state — at least visually.
- Long-content overflow is handled (truncation/wrapping), not breaking the layout.
- **Fail:** only the happy populated state exists.

## 8. Responsive polish
- Renders cleanly at all three breakpoints (mobile ≤639 / tablet 640–1023 / desktop ≥1024); mobile-first.
- Nav collapses sensibly on mobile; touch targets ≥ 44px; no horizontal scroll; nothing clipped.
- **Fail:** desktop layout squashed onto mobile, overflow, tap targets too small.

## Quick gate (use before every preview)
> Primary action obvious? · spacing on the 8pt grid? · text AA-contrast & readable length? ·
> every control has hover+focus? · realistic copy/images? · empty/loading/error shown? ·
> clean at mobile/tablet/desktop? · all colors/space/type from the design-system tokens?

If any answer is "no", fix it before showing the user.

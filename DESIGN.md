# CatchLog — Design System

## 1. Visual Theme & Atmosphere

CatchLog is a fishing community platform where anglers share their catches, discover new spots, and connect with fellow fishers. The design draws inspiration from the outdoors — the teal-green of river water, the warm orange of a sunrise over a lake, and the clear blue of an open sky. It feels like opening a well-worn field journal: warm, trustworthy, and alive with stories.

The interface balances **nature-inspired warmth** with **modern clarity**. Generous photography of catches and landscapes anchors the emotional experience, while clean card-based layouts and a structured grid keep things scannable. The overall mood is: _welcoming community lodge meets modern social app_.

**Key Characteristics:**

- Teal-green primary palette evoking water and nature, with warm orange accents for energy
- Clean, modern sans-serif typography (Inter + DM Sans) — legible in any context
- Rounded, friendly UI elements — soft corners, gentle shadows, approachable feel
- Card-based social feed layout inspired by Instagram and Fishbrain
- Map-centric discovery page with rich location markers
- Photography-forward: large catch images and scenic fishing spots take center stage
- Subtle depth through layered shadows — never harsh, always natural
- Organic micro-animations: gentle fades, smooth slides, natural easing curves

## 2. Color Palette & Roles

### Primary

- **Teal** (`#0F766E`): The core brand color — used for primary buttons, active navigation, map pins, key icons, and brand accents. Evokes river water and lush vegetation.
- **Teal Dark** (`#0D6560`): Hover/pressed state for primary buttons.
- **Teal Light** (`#E0F5F2`): Subtle teal tint for active nav backgrounds, selected states, and highlights.

### Secondary / Accent

- **Sunset Orange** (`#F97316`): High-energy accent for CTAs, featured trips, notification badges, and promotional elements. Evokes warmth, sunrise over water.
- **Orange Dark** (`#EA6C10`): Hover state for orange CTAs.
- **Orange Light** (`#FFF3E8`): Subtle warm tint for featured card backgrounds.

### Tertiary

- **Sky Blue** (`#0EA5E9`): Links, informational accents, sky/water imagery accents, and secondary interactive elements.
- **Sky Blue Dark** (`#0B8DC7`): Hover state for blue links.

### Surfaces & Backgrounds

- **White** (`#FFFFFF`): Page background, card surfaces, modals.
- **Off-White** (`#F8FAFB`): Subtle alternate background for sections (e.g., alternating feed sections, settings panels).
- **Light Gray** (`#F1F5F9`): Input field backgrounds, disabled surfaces.

### Text & Content

- **Text Primary** (`#1E293B`): Headlines, primary body text — dark slate for excellent readability.
- **Text Secondary** (`#64748B`): Descriptions, metadata, timestamps, secondary labels.
- **Text Muted** (`#94A3B8`): Placeholders, disabled text, tertiary information.
- **Text Inverse** (`#FFFFFF`): Text on dark/colored backgrounds.

### Borders & Separation

- **Border Default** (`#E2E8F0`): Card borders, input borders, dividers.
- **Border Strong** (`#CBD5E1`): Focused input borders, emphasized dividers.

### Semantic / Feedback

- **Success** (`#059669`): Successful actions, catch logged confirmations, online indicators.
- **Warning** (`#D97706`): Caution states, weather alerts on map.
- **Error** (`#EF4444`): Form validation errors, delete confirmations, destructive actions.
- **Info** (`#0EA5E9`): Informational banners, tips, help text (same as Sky Blue).

### Shadows & Depth

- **Shadow XS** (`rgba(15, 118, 110, 0.04)`): Barely-there tint lift for flat cards.
- **Shadow SM** (`0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06)`): Default card elevation.
- **Shadow MD** (`0 4px 12px rgba(0, 0, 0, 0.10)`): Hovered cards, dropdown menus.
- **Shadow LG** (`0 8px 24px rgba(0, 0, 0, 0.12)`): Modals, floating action buttons.
- **Shadow Orange Glow** (`0 4px 14px rgba(249, 115, 22, 0.25)`): Featured/promoted card glow effect.

### Gradient System

- **Hero Overlay**: `linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.6) 100%)` — dark overlay on hero images for text readability.
- **Teal Gradient**: `linear-gradient(135deg, #0F766E 0%, #0EA5E9 100%)` — used sparingly for premium banners or empty-state illustrations.
- **Sunrise Gradient**: `linear-gradient(135deg, #F97316 0%, #FBBF24 100%)` — for featured badges and promotional tags.

## 3. Typography Rules

### Font Family

- **Headline / Display**: `'DM Sans'`, with fallbacks: `'Inter', system-ui, -apple-system, sans-serif`
- **Body / UI**: `'Inter'`, with fallbacks: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

_Both fonts are available from Google Fonts and are free to use. Load via:_

```html
<link
  href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700&family=Inter:wght@400;500;600&display=swap"
  rel="stylesheet"
/>
```

### Hierarchy

| Role            | Font    | Size             | Weight | Line Height | Letter Spacing | Notes                            |
| --------------- | ------- | ---------------- | ------ | ----------- | -------------- | -------------------------------- |
| Display / Hero  | DM Sans | 40px (2.5rem)    | 700    | 1.2         | -0.02em        | Hero headlines, splash text      |
| Page Title      | DM Sans | 30px (1.875rem)  | 700    | 1.27        | -0.01em        | Page-level headings (h1)         |
| Section Heading | DM Sans | 24px (1.5rem)    | 700    | 1.33        | -0.01em        | Section anchors (h2)             |
| Card Title      | DM Sans | 18px (1.125rem)  | 700    | 1.33        | 0              | Card headings, post titles       |
| Sub-heading     | DM Sans | 16px (1rem)      | 500    | 1.5         | 0              | Sub-section headers (h4)         |
| Nav / UI Large  | Inter   | 15px (0.9375rem) | 600    | 1.33        | 0              | Navigation links, tab labels     |
| Body            | Inter   | 15px (0.9375rem) | 400    | 1.6         | 0              | Standard body text, descriptions |
| Body Small      | Inter   | 14px (0.875rem)  | 400    | 1.5         | 0              | Secondary info, metadata         |
| Button Label    | Inter   | 14px (0.875rem)  | 600    | 1           | 0.01em         | Button text, action labels       |
| Caption         | Inter   | 13px (0.8125rem) | 500    | 1.38        | 0              | Timestamps, tags, helper text    |
| Micro           | Inter   | 12px (0.75rem)   | 400    | 1.33        | 0.01em         | Fine print, badges, counters     |

### Principles

- **DM Sans for headings only**: Rounded geometric character gives headlines warmth and personality without sacrificing clarity.
- **Inter for everything else**: Supreme readability at all sizes, neutral enough to let content shine.
- **Comfortable line-heights**: Body text at 1.5-1.6 for easy reading of fishing stories and descriptions.
- **Negative letter-spacing on headlines**: Tightens large text for visual impact.
- **Weight contrast creates hierarchy**: Headlines bold (700), body regular (400), UI elements semi-bold (600).

## 4. Component Stylings

### Buttons

**Primary (Teal CTA)**

- Background: Teal (`#0F766E`)
- Text: White (`#FFFFFF`)
- Padding: 10px 20px
- Radius: 8px
- Font: Inter 14px weight 600
- Hover: background darkens to `#0D6560`, shadow SM appears
- Active: background `#0B5650`, translateY(1px)
- Focus: 2px outline `#0F766E` with 2px offset
- Transition: all 0.2s ease

**Secondary (Outlined)**

- Background: White (`#FFFFFF`)
- Text: Teal (`#0F766E`)
- Border: 1.5px solid `#0F766E`
- Padding: 10px 20px
- Radius: 8px
- Hover: background shifts to Teal Light (`#E0F5F2`)
- Active: background `#CCE8E5`

**Accent (Orange CTA)**

- Background: Sunset Orange (`#F97316`)
- Text: White (`#FFFFFF`)
- Padding: 10px 20px
- Radius: 8px
- Hover: background `#EA6C10`, Shadow Orange Glow
- Used for: featured actions, "Start Fishing Trip", promotional CTAs

**Ghost / Tertiary**

- Background: transparent
- Text: Text Secondary (`#64748B`)
- Padding: 8px 16px
- Radius: 8px
- Hover: background `#F1F5F9`
- Used for: cancel actions, less prominent options

**Icon Button**

- Background: White or transparent
- Size: 40px × 40px
- Radius: 50% (circle)
- Icon color: Text Secondary (`#64748B`)
- Hover: background `#F1F5F9`, icon color darkens to `#1E293B`
- Used for: like, comment, share, bookmark, map controls

### Cards & Containers

- Background: White (`#FFFFFF`)
- Border: 1px solid `#E2E8F0`
- Radius: 12px
- Shadow: Shadow SM by default; Shadow MD on hover
- Transition: `box-shadow 0.2s ease, transform 0.15s ease`
- Hover: subtle lift with `transform: translateY(-2px)` + Shadow MD
- Internal padding: 16px (compact) or 20px (comfortable)
- Image-led cards use full-bleed imagery at top with 12px radius on top corners only

**Featured Card Variant:**

- Border: 1px solid `rgba(249, 115, 22, 0.3)`
- Shadow: Shadow Orange Glow
- Small "Featured" badge with Sunrise Gradient background

### Inputs & Forms

- Background: Light Gray (`#F1F5F9`)
- Text: Text Primary (`#1E293B`)
- Placeholder: Text Muted (`#94A3B8`)
- Border: 1.5px solid transparent (default) → `#CBD5E1` (hover) → `#0F766E` (focus)
- Radius: 8px
- Padding: 12px 14px
- Font: Inter 15px weight 400
- Focus: border color `#0F766E`, background White, shadow `0 0 0 3px rgba(15, 118, 110, 0.1)`
- Label: Inter 14px weight 500, Text Primary, margin-bottom 6px
- Error state: border `#EF4444`, helper text in Error red below field

### Navigation

- Sticky top navigation with white background and bottom border `#E2E8F0`
- Logo: 🎣 emoji in a 34px teal circle + "CatchLog" in DM Sans 20px weight 700
- Nav links: Inter 15px weight 500, color `#64748B`
- Active nav link: color `#0F766E`, background `#E0F5F2`, weight 600, radius 999px
- Hover: background `#F1F5F9`, radius 999px
- Link padding: 8px 14px
- Login button: Teal background, white text, radius 999px, padding 8px 16px
- Mobile: hamburger menu toggle, vertical slide-down nav panel
- Max inner width: 960px, centered

### Tags & Chips

- Background: `#F1F5F9`
- Text: `#64748B`
- Padding: 6px 14px
- Radius: 999px (pill)
- Font: Inter 13px weight 500
- Active: background `#0F766E`, text White
- Hover: background `#E2E8F0`
- Used for: fish species filters, post categories, location tags

**Species Tag Variant:**

- Background: `#E0F5F2`
- Text: `#0F766E`
- Small fish icon prefix (optional)
- Used specifically for fish species labels on posts

### Image Treatment

- Catch photos displayed prominently — hero-sized in post detail, grid in feed
- All contained images: 8px radius (in cards) or 12px radius (standalone)
- Image grid in feed: 2-column with 4px gap, 6px radius on each image
- Aspect ratio: 4:3 for landscape catches, 1:1 for grid thumbnails
- Empty state: teal-tinted illustration placeholder
- Avatar images: 40px circle (feed), 80px circle (profile), border `2px solid #E2E8F0`
- Map pin images: 32px circle with `2px solid #FFFFFF` and Shadow SM

### Distinctive Components

**Post Card (Feed)**

- Card with 12px radius, border, Shadow SM
- Header: avatar (40px circle) + username (Inter 14px/600) + timestamp (Inter 13px/400 muted) + location pin icon + location text
- Body: post text in Inter 15px/400
- Image area: full-bleed images, 2-column grid if multiple
- Species tag: pill tag below images
- Footer: like, comment, share, bookmark icon buttons with counts
- Separator: 1px `#E2E8F0` between body and footer

**Map Pin / Marker**

- Circular teal pin with white fish icon center
- Active/selected: larger pin with orange ring and Shadow MD
- Cluster: teal circle with white count text, size scales with count

**Catch Detail Modal / Page**

- Large hero image at top (full width, 16:9 or 4:3)
- Semi-transparent gradient overlay at bottom of image for title text
- Details grid below: species, weight, bait, method — in 2-column layout
- Location shown with inline mini-map
- Comments section below

**Empty States**

- Centered layout with teal-tinted illustration
- DM Sans 20px/700 heading: "No catches yet!"
- Inter 15px/400 body in Text Secondary
- Teal primary CTA: "Log Your First Catch"

## 5. Layout Principles

### Spacing System

- Base unit: 4px
- Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80px
- Component internal padding: 16px (compact), 20px (standard), 24px (spacious)
- Section vertical spacing: 48-64px between major sections
- Card gap in feed: 16px
- Form field gap: 20px

### Grid & Container

- Max container width: 960px, centered with `margin: 0 auto`
- Feed: single-column, max-width 600px, centered
- Map page: full-viewport map with floating sidebar/cards
- Profile: single-column header + tabbed content (My Posts / Saved / Stats)
- Settings: single-column form, max-width 640px
- Side padding: 20px (mobile), 24px (tablet+)

### Whitespace Philosophy

- **Breathable but purposeful**: more generous than Uber's density — fishing stories need room to breathe. But not wastefully airy.
- **Content hierarchy through spacing**: more space before section headings, tighter spacing within related groups.
- **Cards define content blocks**: shadow + border + radius create clear boundaries without relying on heavy dividers.

### Border Radius Scale

- Small (6px): Image grid thumbnails, small chips
- Standard (8px): Buttons, input fields, inline tags
- Comfortable (12px): Cards, containers, modals, larger images
- Large (16px): Hero sections, promotional banners
- Full Pill (999px): Nav chips, tags, filter pills, avatar images
- Circle (50%): Icon buttons, avatar containers, map pins

## 6. Depth & Elevation

| Level              | Treatment                            | Use                                 |
| ------------------ | ------------------------------------ | ----------------------------------- |
| Flat (Level 0)     | No shadow, border only (`#E2E8F0`)   | Default cards, static containers    |
| Subtle (Level 1)   | Shadow SM                            | Feed cards, form containers         |
| Raised (Level 2)   | Shadow MD                            | Hovered cards, dropdowns, popovers  |
| Floating (Level 3) | Shadow LG                            | Modals, floating map controls, FABs |
| Featured           | Shadow Orange Glow                   | Featured/promoted content           |
| Focus Ring         | `0 0 0 3px rgba(15, 118, 110, 0.15)` | Keyboard focus indicators           |

**Shadow Philosophy**: Shadows are soft and natural — they mimic the gentle diffusion of outdoor light. No harsh edges, no dramatic drops. The teal-tinted focus ring subtly reinforces brand identity even at the interaction level.

## 7. Do's and Don'ts

### Do

- Use Teal (`#0F766E`) as the dominant brand color — it anchors the outdoor identity
- Use Sunset Orange (`#F97316`) sparingly as an energizing accent for key CTAs and featured content
- Keep cards rounded (12px) and shadows soft — the interface should feel friendly and approachable
- Use generous, comfortable spacing — fishing stories and photos need breathing room
- Show catch photography prominently — images are the hero content
- Use species tags (teal pills) to make content filterable and scannable
- Maintain clear visual hierarchy: DM Sans bold headings → Inter regular body
- Use semantic colors consistently: green=success, orange=warning, red=error
- Design map elements to be tap-friendly with clear active/selected states
- Add hover transitions (0.2s ease) to all interactive elements for a polished feel

### Don't

- Don't use Teal and Orange together in equal amounts — Teal is 70%, Orange is 10%
- Don't use pure black (`#000000`) for text — use slate `#1E293B` for a softer feel
- Don't apply heavy or colored drop shadows — keep everything soft and natural
- Don't use more than two font families — stick to DM Sans + Inter
- Don't make cards completely flat (no border, no shadow) — they need subtle definition
- Don't use sharp corners (0px radius) on interactive elements — this app should feel rounded and friendly
- Don't overuse the Sunrise Gradient — reserve it for badges and small featured tags
- Don't make images too small — catches are the star of the content
- Don't forget hover and focus states — every interactive element needs feedback
- Don't use generic placeholder images — show realistic fishing content or themed empty states

## 8. Responsive Behavior

### Breakpoints

| Name    | Width   | Key Changes                                                        |
| ------- | ------- | ------------------------------------------------------------------ |
| Mobile  | < 640px | Single column, hamburger nav, stacked forms, full-width cards      |
| Tablet  | 640px   | Two-column grids begin, expanded card layouts, side-by-side inputs |
| Desktop | 960px   | Full desktop layout, horizontal nav, max-width container activates |

### Touch Targets

- All buttons: minimum 44px height
- Icon buttons: 40px × 40px minimum
- Nav links with padding: comfortable thumb tapping at 44px+ hit area
- Tags/chips: minimum 32px height with generous padding
- Card surfaces serve as full-area touch targets on mobile

### Collapsing Strategy

- **Navigation**: Horizontal links collapse to hamburger menu with slide-down panel
- **Feed cards**: maintain single-column, full-width on all sizes
- **Image grids**: 2-column on all sizes, images scale proportionally
- **Profile**: stats row stacks if needed, tabs remain horizontal with scroll
- **Map**: full viewport on all sizes, floating controls reposition
- **Forms**: inputs stack vertically on mobile, side-by-side on tablet+
- **Typography**: Display 40px → 30px on mobile; Page Title 30px → 24px

### Image Behavior

- Catch photos maintain aspect ratio, may crop slightly on smaller screens
- Avatar sizes remain consistent across breakpoints
- Map pins scale with zoom level, not screen size
- Image grid thumbnails: fixed 2-column layout, height scales with width

## 9. Implementation Quick Reference

### CSS Custom Properties

```css
:root {
  /* Brand Colors */
  --color-primary: #0f766e;
  --color-primary-dark: #0d6560;
  --color-primary-light: #e0f5f2;
  --color-secondary: #f97316;
  --color-secondary-dark: #ea6c10;
  --color-secondary-light: #fff3e8;
  --color-tertiary: #0ea5e9;

  /* Surfaces */
  --color-bg: #ffffff;
  --color-bg-alt: #f8fafb;
  --color-surface: #ffffff;
  --color-surface-muted: #f1f5f9;

  /* Text */
  --color-text: #1e293b;
  --color-text-secondary: #64748b;
  --color-text-muted: #94a3b8;
  --color-text-inverse: #ffffff;

  /* Borders */
  --color-border: #e2e8f0;
  --color-border-strong: #cbd5e1;

  /* Semantic */
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #ef4444;
  --color-info: #0ea5e9;

  /* Typography */
  --font-display: "DM Sans", "Inter", system-ui, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, sans-serif;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radii */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 999px;
  --radius-circle: 50%;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --shadow-glow: 0 4px 14px rgba(249, 115, 22, 0.25);
  --shadow-focus: 0 0 0 3px rgba(15, 118, 110, 0.15);

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.2s ease;
  --transition-slow: 0.3s ease;
}
```

### Example Component Patterns

- **Primary Button**: `background: var(--color-primary); color: var(--color-text-inverse); border-radius: var(--radius-md); padding: 10px 20px; font: 600 14px var(--font-body);`
- **Feed Card**: `background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);`
- **Species Tag**: `background: var(--color-primary-light); color: var(--color-primary); border-radius: var(--radius-pill); padding: 6px 14px; font: 500 13px var(--font-body);`
- **Nav Link Active**: `background: var(--color-primary-light); color: var(--color-primary); font-weight: 600; border-radius: var(--radius-pill);`
- **Input Focus**: `border-color: var(--color-primary); background: var(--color-bg); box-shadow: var(--shadow-focus);`

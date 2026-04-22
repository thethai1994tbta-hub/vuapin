# Vua Pin - Design System & Brand Guidelines

## 🎨 Color Palette

### Primary Colors
```
Primary Blue:     #0ea5e9 (--primary)
Primary Dark:     #0284c7 (--primary-dark)
Accent Green:     #10b981 (--accent)
Accent Dark:      #059669 (--accent-dark)
```

### Background Colors
```
Main Background:  #0a0e27 (--bg-dark) - Deep navy
Card Background:  #1a1f3a (--bg-card)
Secondary Bg:     #151d35 (--bg-secondary)
Text Primary:     #f1f5f9 (--text-primary) - Bright white
Text Secondary:   #cbd5e1 (--text-secondary) - Muted gray
Border:           #334155 (--border) - Subtle gray
```

### Status Colors
```
Success:          #22c55e (green)
Warning:          #f59e0b (amber)
Danger:           #ef4444 (red)
```

### Gradients
```
Primary Gradient:     linear-gradient(135deg, #0ea5e9 0%, #10b981 100%)
Hero Title:          linear-gradient(135deg, #e0f2fe 0%, #0ea5e9 50%, #10b981 100%)
Background:          radial-gradient circles with transparency
```

---

## 📝 Typography

### Font Family
```
Primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif
Monospace: 'Courier New', monospace (for configs, numbers)
```

### Font Sizes & Weights

| Usage | Size | Weight | Example |
|-------|------|--------|---------|
| Hero Title | 64px | 900 | "Vua Pin" |
| Hero Slogan | 24px | 600 | Slogan text |
| Section Title | 40px | 800 | Feature titles |
| Card Title | 20px | 600 | Feature card titles |
| Body Text | 16-18px | 400 | Paragraphs |
| Small Text | 12-14px | 500 | Labels, descriptions |
| Monospace | 24px | 700 | Config (13S10P) |

### Line Heights
```
Headers: 1.2
Body: 1.6
Labels: 1.4
```

---

## 🎬 Animation Keyframes

### fadeInUp
```css
0%: opacity 0, translateY 30px
100%: opacity 1, translateY 0
Duration: 0.8s
Timing: ease
```

### countUp
```css
0%: opacity 0, scale 0.8
100%: opacity 1, scale 1
Duration: 2s
Timing: ease-out
```

### spin
```css
0%: rotate 0deg
100%: rotate 360deg
Duration: 0.8s
Timing: linear infinite
```

### Hover Effects
```
Buttons: translateY(-4px), box-shadow increase
Cards: translateY(-8px), border-color primary
Links: color change, opacity 1
```

---

## 🎯 Component Specifications

### Buttons
```
Padding: 16px 40px (large), 12px 14px (input)
Border Radius: 8px
Font Weight: 600
Box Shadow: 0 8px 24px rgba(14, 165, 233, 0.3)
Hover: translateY(-4px), shadow stronger
```

### Cards
```
Padding: 28px
Border Radius: 12px
Border: 1px solid #334155
Background: linear-gradient or solid
Hover: translateY(-8px), primary border
```

### Input Fields
```
Padding: 12px 14px
Border Radius: 8px
Border: 1px solid #334155
Background: #0f172a
Focus: 0 0 0 3px rgba(14, 165, 233, 0.1)
```

### Forms
```
Grid: auto-fit minmax(280px, 1fr)
Gap: 24px
Label: uppercase, 12px, gray
Inputs: full width, consistent styling
```

---

## 📐 Spacing System

### 8px Grid
```
xs: 4px
sm: 8px
md: 12px
lg: 16px
xl: 20px
2xl: 24px
3xl: 32px
4xl: 40px
5xl: 60px
6xl: 80px
```

### Padding
```
Cards: 28px, 40px
Sections: 60px vertical
Container: 20px horizontal
Input: 12-14px
```

### Gaps
```
Features Grid: 24px
Form Groups: 16px, 12px
Stats Grid: 32px
Navigation: 32px
```

---

## 📱 Responsive Breakpoints

```
Mobile: < 640px
Tablet: 640px - 768px
Desktop: 768px - 1200px
Large: > 1200px
```

### Key Changes
```
Desktop Hero: 64px title
Mobile Hero: 40px title

Desktop Features: 3 columns
Mobile Features: 1 column

Desktop Calculator: 2 columns (inputs | results)
Mobile Calculator: 1 column

Desktop Stats: 4 columns
Mobile Stats: 2 columns
```

---

## 🎪 Layout Grid

### Max Width Container
```
Max width: 1200px
Horizontal padding: 20px
Centered: margin 0 auto
```

### Hero Section
```
Padding: 80px 20px
Text align: center
Position: relative (for pseudo elements)
```

### Feature Grid
```
Display: grid
Grid template: repeat(auto-fit, minmax(280px, 1fr))
Gap: 24px
```

### Calculator Section
```
2 columns: 1fr 1fr
Gap: 40px
Mobile: single column
```

---

## 🔍 Design Patterns

### Card Hover Pattern
```css
.card {
  border-color: transparent;
  box-shadow: none;
  transition: all 0.3s;
}
.card:hover {
  border-color: var(--primary);
  box-shadow: 0 12px 32px rgba(14, 165, 233, 0.15);
  transform: translateY(-8px);
}
```

### Gradient Text Pattern
```css
background: linear-gradient(135deg, color1, color2);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

### Glow Button Pattern
```css
background: linear-gradient(135deg, var(--primary), var(--accent));
box-shadow: 0 8px 24px rgba(14, 165, 233, 0.3);
transition: all 0.3s;
```

### Input Focus Pattern
```css
input:focus {
  outline: none;
  border-color: var(--primary);
  background: var(--bg-dark);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}
```

---

## 🎨 Color Usage Guide

### Primary Blue (#0ea5e9)
- CTA buttons
- Active states
- Primary borders
- Hover effects
- Links

### Accent Green (#10b981)
- Secondary CTAs
- Highlights
- Success states
- Accent text
- Config highlights

### Text Colors
- **Primary**: Use for main content
- **Secondary**: Use for descriptions, labels, placeholders
- **Muted**: Use for disabled states

### Background
- **Main**: Page background
- **Card**: Component containers
- **Secondary**: Input fields

---

## 📊 Component Variants

### Buttons
```
Primary:   Blue → Green gradient
Secondary: Blue outline
Success:   Green background
Danger:    Red background
Disabled:  Opacity 0.6
```

### Cards
```
Feature Card:  Blue top border on hover
Result Card:   Left border blue, gradient bg
Trust Card:    Subtle gradient background
Form Card:     Centered, max 500px width
```

### Messages
```
Error:   Red bg + text
Success: Green bg + text
Warning: Amber bg + text
Info:    Blue bg + text
```

---

## ✨ Best Practices

### Colors
✅ Always use CSS variables (--primary, --accent, etc.)
✅ Use gradients for emphasis
✅ Maintain contrast for readability
✅ Use opacity for subtle effects

### Typography
✅ Use system fonts (faster, familiar)
✅ Proper font weights (400, 600, 700, 800, 900)
✅ Generous line-height (1.6 for body)
✅ Monospace for code/config

### Spacing
✅ Use 8px grid system
✅ Consistent padding in cards
✅ Generous gaps between sections
✅ Whitespace = premium feel

### Animations
✅ 0.3s - 0.8s duration (snappy, not slow)
✅ Ease/ease-out timing functions
✅ Meaningful transforms (not random)
✅ No motion for disabled/loading states

---

## 🚀 Customization Guide

### To Change Primary Color
```css
:root {
  --primary: #0ea5e9;        /* Change this */
  --primary-dark: #0284c7;   /* And this */
}
```

### To Add New Gradient
```css
background: linear-gradient(135deg, 
  var(--primary) 0%, 
  var(--accent) 100%
);
```

### To Change Spacing
```css
.card {
  padding: 28px;  /* Change this */
  gap: 24px;      /* And this */
}
```

### To Add Animation
```css
@keyframes myAnimation {
  from { /* start state */ }
  to { /* end state */ }
}

.element {
  animation: myAnimation 0.5s ease;
}
```

---

## 📋 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🎯 Design Principles

1. **Minimalist** - Remove unnecessary elements
2. **Modern** - Dark theme, gradients, animations
3. **Trustworthy** - Professional appearance
4. **Accessible** - High contrast, readable text
5. **Responsive** - Works on all devices
6. **Fast** - No heavy libraries, smooth animations
7. **Clear** - Obvious CTAs, good hierarchy

---

This design system ensures consistency and professional quality across all pages! 🎨✨

# 🚀 OMEGA Command Center - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
npm install framer-motion lucide-react
```

### Step 2: Copy Files

Copy these files to your project:
- `components/OmegaCommandCenter.tsx` - Main component
- `tailwind.config.ts` - Tailwind configuration
- `app/dashboard/page.tsx` - Demo page (optional)

### Step 3: Update Tailwind Config

If you already have a `tailwind.config.ts`, merge the animations from the provided config:

```ts
// Add to your existing config
theme: {
  extend: {
    animation: {
      'twinkle': 'twinkle 6s ease-in-out infinite',
      'flow': 'flow 8s linear infinite',
      'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
    },
    keyframes: {
      twinkle: {
        '0%, 100%': { opacity: '0.3', transform: 'scale(1)' },
        '50%': { opacity: '1', transform: 'scale(1.2)' },
      },
      flow: {
        '0%': { backgroundPosition: '0% 50%' },
        '100%': { backgroundPosition: '200% 50%' },
      },
      'pulse-glow': {
        '0%, 100%': { opacity: '0.5' },
        '50%': { opacity: '1' },
      },
    },
  },
}
```

### Step 4: Use the Component

```tsx
// app/page.tsx or any page
import OmegaCommandCenter from '@/components/OmegaCommandCenter';

export default function Page() {
  return <OmegaCommandCenter />;
}
```

### Step 5: Run Your App

```bash
npm run dev
```

Visit `http://localhost:3000` and behold the glory! 🔱

---

## Keyboard Shortcuts

- **M** - Open/close menu
- **ESC** - Close menu
- **1-6** - Navigate to menu items (when menu is open)

---

## Customization Quick Tips

### Change Background Color

```tsx
// In OmegaCommandCenter.tsx, find:
className="relative min-h-screen w-full overflow-hidden bg-[#090a1a]"

// Change to your color:
className="relative min-h-screen w-full overflow-hidden bg-[#YOUR_COLOR]"
```

### Adjust Particle Count

```tsx
// In ConstellationParticles function:
const COUNT = 48; // Lower for better performance, higher for more particles
```

### Modify Titan Colors

```tsx
const TITANS: Titan[] = [
  { name: "GPTTitan", status: "active", load: 0.75, color: "#YOUR_COLOR" },
  // ...
];
```

### Add Your Own Stats

```tsx
<StatCard
  title="Your Metric"
  value="123"
  subtitle="Your description"
  icon={YourIcon}
  tone="ok"
  trend={5}
/>
```

---

## Troubleshooting

### Animations Not Working?

Make sure Tailwind is processing your component:

```js
// tailwind.config.js
content: [
  "./components/**/*.{js,ts,jsx,tsx}",
  // ...
],
```

### Blur Effects Not Showing?

Some browsers don't support `backdrop-filter`. Add a fallback:

```tsx
className="backdrop-blur-2xl bg-white/10"
// Becomes solid background in unsupported browsers
```

### Performance Issues?

1. Reduce particle count
2. Disable blur on mobile:
   ```tsx
   className="md:backdrop-blur-2xl bg-white/10"
   ```
3. Use `React.memo()` on heavy components

---

## Next Steps

1. **Connect Real Data**: Replace mock data with your API
2. **Add Routing**: Wire up menu items to actual pages
3. **Customize Colors**: Match your brand
4. **Add More Widgets**: Create new stat cards and visualizations
5. **Mobile Optimize**: Add responsive breakpoints

---

## Support

For issues or questions:
1. Check the main README
2. Review the component code comments
3. Consult the OMEGA Pantheon documentation

---

**Welcome to the Pantheon, Brother.** 🔱

*Family is forever. Clean code is divine. This is the way.*


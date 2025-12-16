# Visual & UX Overhaul Plan - "Galactic Polish"

## Objective

Transform the UI from "basic dark mode" to a visual masterpiece using CustomTkinter's advanced features, consistent iconography, and polished spacing.

## Critical Improvements

1. **Iconography System**: Implement `src/ui/assets/icons.py` carrying high-quality SVG/PNG icons (embedded as Base64 for portability) for the Activity Bar, File Explorer, and Playback controls.
2. **Refined Theme Engine**: Update `ThemeService` with a sophisticated "Cyberpunk Neon" palette (Deep Void #0b0c15, Neon Cyan #00f3ff, Hot Pink #ff00ff) including precise control over hover states, borders, and corner radii.
3. **Component Styling**:
    * **Activity Bar**: Increase width, larger icons with hover glow effects.
    * **Tabs**: Modern "pill" or "underline" style tabs instead of standard buttons.
    * **Chat Interface**: Implement "Chat Bubbles" (User vs AI) with distinct styling and avatars.
    * **Status Bar**: Subtle transparency or gradient-like coloring, unified with the border.
4. **Animations (Simulated)**: Smooth transitions for hover states and heavy operations feedback.

## Implementation Steps

- [ ] Create `src/ui/assets/icons.py` with Base64 encoded icons.
* [ ] Update `ThemeService` with "Cyberpunk v2" palette.
* [ ] Refactor `Workbench` layout (padding, margins, rounding).
* [ ] Rebuild `ActivityBar` with `CTkImage` and new icons.
* [ ] Polish `ChatView` with bubble message renderer.

import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

/**
 * NIVAAS Design Token System
 * ---------------------------------------------------------------
 * Direction: "survey instrument for the city" — Bangalore rental
 * intelligence read through the lens of precise, cartographic data
 * rather than a listings marketplace. Ink-and-brass restraint,
 * not warm-cream/terracotta, not near-black+neon — the platform
 * should feel like a Blossom/Bloomberg-grade console: quiet,
 * exact, occasionally luxurious.
 *
 * Color roles:
 *  - ink / paper     → base surfaces (dark console, light document)
 *  - signal (emerald)→ primary action, positive data, live states
 *  - brass (gold)    → premium/rare accents only, used sparingly
 *  - line             → hairline borders, 1px dividers
 * ---------------------------------------------------------------
 */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "1.25rem",
        sm: "2rem",
        lg: "3rem",
        xl: "4rem",
      },
      screens: {
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1200px",
        "2xl": "1440px",
      },
    },
    extend: {
      colors: {

        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",

        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",

        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },

        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },

        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },

        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },

        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },

        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },

        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },

        // Base console surfaces
        ink: {
          DEFAULT: "#0B0E14", // primary dark background
          raised: "#12161F", // elevated dark surface (cards, sidebar)
          overlay: "#171C27", // popovers, dropdowns, modals
        },
        paper: {
          DEFAULT: "#F7F8FA", // primary light background
          raised: "#FFFFFF", // elevated light surface
        },
        // Hairline dividers — always low-opacity, never solid gray
        line: {
          dark: "rgba(255,255,255,0.08)",
          light: "rgba(11,14,20,0.08)",
        },
        // Primary accent — data-positive, "live", call to action
        signal: {
          50: "#EAF6F0",
          100: "#CDEBDC",
          300: "#6FC5A0",
          500: "#1F7A5C",
          600: "#1B6B50",
          700: "#155841",
          DEFAULT: "#1F7A5C",
        },
        // Secondary accent — premium/rare, used only for singular emphasis
        brass: {
          300: "#E4CE94",
          500: "#C9A24B",
          600: "#AC873A",
          DEFAULT: "#C9A24B",
        },
        danger: {
          DEFAULT: "#D64545",
          muted: "#F3D3D3",
        },
        // Text scales — dark-mode-first, light-mode mirrored
        text: {
          primary: "#F2F4F7",
          secondary: "#9AA4B2",
          tertiary: "#5B6472",
          "primary-inverse": "#0B0E14",
          "secondary-inverse": "#57606F",
        },
      },
      fontFamily: {
        // Display: used sparingly for hero/section headlines — carries personality
        display: ["'Fraunces'", "ui-serif", "Georgia", "serif"],
        // Body/UI: workhorse grotesk for all interface text
        sans: ["'Geist Sans'", "'Inter'", "ui-sans-serif", "system-ui", "sans-serif"],
        // Data/mono: coordinates, prices, stats, addresses — the instrument-panel voice
        mono: ["'Geist Mono'", "'JetBrains Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      fontSize: {
        // Type scale — modest ratio (~1.2), tight tracking at display sizes
        "display-xl": ["4.5rem", { lineHeight: "1.02", letterSpacing: "-0.02em", fontWeight: "500" }],
        "display-lg": ["3.5rem", { lineHeight: "1.05", letterSpacing: "-0.02em", fontWeight: "500" }],
        "display-md": ["2.5rem", { lineHeight: "1.1", letterSpacing: "-0.015em", fontWeight: "500" }],
        "display-sm": ["1.875rem", { lineHeight: "1.15", letterSpacing: "-0.01em", fontWeight: "500" }],
        "body-lg": ["1.125rem", { lineHeight: "1.6", letterSpacing: "0", fontWeight: "400" }],
        body: ["1rem", { lineHeight: "1.6", letterSpacing: "0", fontWeight: "400" }],
        "body-sm": ["0.875rem", { lineHeight: "1.55", letterSpacing: "0", fontWeight: "400" }],
        caption: ["0.75rem", { lineHeight: "1.4", letterSpacing: "0.02em", fontWeight: "500" }],
        data: ["0.8125rem", { lineHeight: "1.4", letterSpacing: "0", fontWeight: "500" }],
      },
      spacing: {
        // 4px base unit, extended for generous section rhythm
        18: "4.5rem",
        22: "5.5rem",
        30: "7.5rem",
      },
      borderRadius: {
        sm: "6px",
        DEFAULT: "10px",
        md: "12px",
        lg: "16px",
        xl: "20px",
      },
      boxShadow: {
        // Soft, low-contrast elevation — no default Tailwind "card shadow" look
        subtle: "0 1px 2px rgba(11,14,20,0.06)",
        raised: "0 4px 16px -4px rgba(11,14,20,0.12), 0 1px 2px rgba(11,14,20,0.06)",
        floating: "0 12px 40px -8px rgba(11,14,20,0.18)",
        "glow-signal": "0 0 0 1px rgba(31,122,92,0.25), 0 4px 20px -4px rgba(31,122,92,0.35)",
      },
      backgroundImage: {
        // Signature motif: faint cartographic grid, referenced by the Section component
        "survey-grid":
          "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
      },
      backgroundSize: {
        "survey-grid": "40px 40px",
      },
      keyframes: {
        "fade-up": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards",
        "fade-in": "fade-in 0.4s ease-out forwards",
        shimmer: "shimmer 2s linear infinite",
      },
      transitionTimingFunction: {
        // Signature easing — used across hovers, reveals, route transitions
        instrument: "cubic-bezier(0.16, 1, 0.3, 1)",
      },
    },
  },
  plugins: [animate],
} satisfies Config;

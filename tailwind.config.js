/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,html}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ═══════════════════════════════════════════════════════════════
        // DEEP VIOLET GLASSMORPHISM (IceWarp Style)
        // ═══════════════════════════════════════════════════════════════
        
        // Primary violet palette
        'ice-violet': {
          DEFAULT: '#4c1d95',
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        
        // Glassmorphism backgrounds - DARKER for better contrast
        'ice-glass': {
          DEFAULT: 'rgba(0, 0, 0, 0.25)',
          light: 'rgba(0, 0, 0, 0.15)',
          medium: 'rgba(0, 0, 0, 0.35)',
          card: 'rgba(0, 0, 0, 0.3)',
          dark: 'rgba(15, 10, 35, 0.9)',
          darker: 'rgba(15, 10, 35, 0.95)',
          darkest: 'rgba(15, 10, 35, 0.98)',
          input: 'rgba(0, 0, 0, 0.4)',          // bg-black/40 for inputs
          'input-light': 'rgba(0, 0, 0, 0.3)',
        },
        
        // Text colors - WCAG AA Compliant (NO grays!)
        'ice-text': {
          DEFAULT: '#FFFFFF',
          primary: '#FFFFFF',       // Pure white - primary
          secondary: '#E9D5FF',     // Pale lavender - secondary (NOT gray!)
          muted: '#E9D5FF',         // Pale lavender - use instead of gray
          accent: '#E9D5FF',        // Pale lavender
          placeholder: 'rgba(255, 255, 255, 0.4)',  // White at 40% opacity
        },
        
        // Accent colors
        'ice-mint': {
          DEFAULT: '#10b981',
          light: 'rgba(16, 185, 129, 0.15)',
          medium: 'rgba(16, 185, 129, 0.3)',
          bright: '#34d399',
          dark: '#059669',
        },
        'ice-pink': {
          DEFAULT: '#ec4899',
          light: 'rgba(236, 72, 153, 0.15)',
          medium: 'rgba(236, 72, 153, 0.3)',
          bright: '#f472b6',
          dark: '#db2777',
        },
        'ice-blue': {
          DEFAULT: '#3b82f6',
          light: 'rgba(59, 130, 246, 0.15)',
          medium: 'rgba(59, 130, 246, 0.3)',
          bright: '#60a5fa',
          dark: '#2563eb',
        },
        'ice-red': {
          DEFAULT: '#ef4444',
          light: 'rgba(239, 68, 68, 0.15)',
          medium: 'rgba(239, 68, 68, 0.3)',
          bright: '#f87171',
          dark: '#dc2626',
        },
        
        // Border colors
        'ice-border': {
          DEFAULT: 'rgba(255, 255, 255, 0.1)',
          light: 'rgba(255, 255, 255, 0.05)',
          medium: 'rgba(255, 255, 255, 0.15)',
          strong: 'rgba(255, 255, 255, 0.2)',
        },
      },
      
      // Glassmorphism backdrop blur
      backdropBlur: {
        'ice': '12px',
        'ice-light': '8px',
        'ice-heavy': '20px',
      },
      
      // Custom gradients
      backgroundImage: {
        'ice-gradient': 'linear-gradient(135deg, #2e1065 0%, #4c1d95 100%)',
        'ice-gradient-light': 'linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%)',
        'ice-mint-gradient': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        'ice-pink-gradient': 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
      },
      
      // Box shadows for glass effect
      boxShadow: {
        'ice': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'ice-glow': '0 0 20px rgba(91, 33, 182, 0.4)',
        'ice-mint-glow': '0 8px 20px rgba(16, 185, 129, 0.3)',
        'ice-pink-glow': '0 8px 20px rgba(236, 72, 153, 0.3)',
      },
      
      // Border radius
      borderRadius: {
        'ice': '16px',
        'ice-sm': '12px',
        'ice-lg': '20px',
      },
      
      // Font family
      fontFamily: {
        'ice': ['Inter', 'system-ui', 'sans-serif'],
        'ice-mono': ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}

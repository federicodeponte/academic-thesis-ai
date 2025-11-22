// ABOUTME: Centralized design tokens for consistent color usage across OpenDraft
// ABOUTME: Maps semantic names to brand colors to prevent random shade picking

/**
 * OpenDraft Design Tokens
 *
 * Provides a consistent color system based on the brand purple/cyan palette.
 * Use these tokens instead of hardcoding Tailwind classes to ensure visual consistency.
 *
 * Brand Colors:
 * - Primary: Purple (#8B5CF6 - brand-purple-500)
 * - Accent: Cyan (#06B6D4 - brand-cyan-500)
 *
 * Usage:
 * ```tsx
 * import { DESIGN_TOKENS } from '@/lib/design-tokens';
 * <button className={DESIGN_TOKENS.button.primary.bg + ' ' + DESIGN_TOKENS.button.primary.text}>
 * ```
 */

export const DESIGN_TOKENS = {
  // Primary actions (buttons, CTAs, badges)
  button: {
    primary: {
      bg: 'bg-brand-purple-600',
      bgHover: 'hover:bg-brand-purple-700',
      text: 'text-white',
      border: 'border-brand-purple-600',
    },
    secondary: {
      bg: 'bg-brand-cyan-500',
      bgHover: 'hover:bg-brand-cyan-600',
      text: 'text-white',
      border: 'border-brand-cyan-500',
    },
    outline: {
      bg: 'bg-transparent',
      bgHover: 'hover:bg-brand-purple-50 dark:hover:bg-brand-purple-950',
      text: 'text-brand-purple-600 dark:text-brand-purple-400',
      border: 'border-brand-purple-200 dark:border-brand-purple-800',
      borderHover: 'hover:border-brand-purple-400 dark:hover:border-brand-purple-600',
    },
  },

  // Borders (consistent border widths and colors)
  border: {
    default: 'border-border',  // CSS variable
    subtle: 'border-brand-purple-100 dark:border-brand-purple-900',
    emphasis: 'border-brand-purple-200 dark:border-brand-purple-800',
    strong: 'border-brand-purple-300 dark:border-brand-purple-700',
  },

  // Backgrounds
  bg: {
    brand: {
      subtle: 'bg-brand-purple-50 dark:bg-brand-purple-950',
      light: 'bg-brand-purple-100 dark:bg-brand-purple-900',
      medium: 'bg-brand-purple-500',
      strong: 'bg-brand-purple-600',
    },
    accent: {
      subtle: 'bg-brand-cyan-50 dark:bg-brand-cyan-950',
      light: 'bg-brand-cyan-100 dark:bg-brand-cyan-900',
    },
  },

  // Text colors
  text: {
    brand: {
      light: 'text-brand-purple-400',
      default: 'text-brand-purple-600 dark:text-brand-purple-400',
      strong: 'text-brand-purple-700 dark:text-brand-purple-300',
    },
    accent: 'text-brand-cyan-500 dark:text-brand-cyan-400',
  },

  // Gradients (use with bg-gradient-to-*)
  gradient: {
    hero: 'from-brand-purple-500 to-brand-cyan-500',
    button: 'from-brand-purple-500 to-brand-purple-600',
    buttonHover: 'from-brand-purple-600 to-brand-purple-700',
    card: 'from-brand-purple-50 to-white dark:from-brand-purple-950 dark:to-slate-900',
    logo: 'from-brand-purple-500 to-brand-purple-600',
  },

  // Shadows (brand-aware)
  shadow: {
    brand: 'shadow-brand-purple-500/20',
    brandHover: 'hover:shadow-brand-purple-500/30',
    brandStrong: 'shadow-2xl shadow-brand-purple-500/20',
  },

  // Status colors (semantic - keep separate from brand)
  status: {
    success: {
      bg: 'bg-green-50 dark:bg-green-950',
      border: 'border-green-300 dark:border-green-700',
      text: 'text-green-700 dark:text-green-300',
      icon: 'text-green-600 dark:text-green-400',
    },
    error: {
      bg: 'bg-red-50 dark:bg-red-950',
      border: 'border-red-300 dark:border-red-700',
      text: 'text-red-700 dark:text-red-300',
      icon: 'text-red-600 dark:text-red-400',
    },
    warning: {
      bg: 'bg-yellow-50 dark:bg-yellow-950',
      border: 'border-yellow-300 dark:border-yellow-700',
      text: 'text-yellow-700 dark:text-yellow-300',
      icon: 'text-yellow-600 dark:text-yellow-400',
    },
    info: {
      bg: 'bg-brand-cyan-50 dark:bg-brand-cyan-950',
      border: 'border-brand-cyan-300 dark:border-brand-cyan-700',
      text: 'text-brand-cyan-700 dark:text-brand-cyan-300',
      icon: 'text-brand-cyan-600 dark:text-brand-cyan-400',
    },
  },

  // Badge colors
  badge: {
    brand: 'bg-brand-purple-50 dark:bg-brand-purple-950 text-brand-purple-700 dark:text-brand-purple-300 border-brand-purple-300 dark:border-brand-purple-700',
    accent: 'bg-brand-cyan-50 dark:bg-brand-cyan-950 text-brand-cyan-700 dark:text-brand-cyan-300 border-brand-cyan-300 dark:border-brand-cyan-700',
    success: 'bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 border-green-300 dark:border-green-700',
  },
} as const;

/**
 * Helper function to combine multiple token classes
 * @param tokens Array of token class strings
 * @returns Combined className string
 */
export const combineTokens = (...tokens: string[]) => tokens.join(' ');

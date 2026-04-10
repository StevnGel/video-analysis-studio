export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'app-bg': '#0a0e17',
        'app-bg-secondary': '#111827',
        'app-card': '#1f2937',
        'app-primary': '#3b82f6',
        'app-success': '#10b981',
        'app-warning': '#f59e0b',
        'app-error': '#ef4444',
        'app-text': '#f9fafb',
        'app-text-secondary': '#9ca3af',
      },
    },
  },
  plugins: [],
}
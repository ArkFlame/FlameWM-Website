import { defineConfig } from 'astro/config';

// For the existing custom domain, BASE_PATH is '/'. For a GitHub project URL,
// use SITE_URL=https://ArkFlame.github.io and BASE_PATH=/FlameWM-Website/.
export default defineConfig({
  output: 'static',
  site: process.env.SITE_URL || 'https://wm.arkflame.com',
  base: process.env.BASE_PATH || '/',
  trailingSlash: 'always',
  build: { format: 'directory' },
});

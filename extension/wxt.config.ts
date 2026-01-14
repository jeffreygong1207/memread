import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    permissions: ['storage', 'tabs'],
    host_permissions: [
      '*://chatgpt.com/*',
      '*://claude.ai/*',
      'http://localhost:8000/*'
    ],
    name: 'MemRead: Universal Memory',
    description: 'Syncs your chat history to a local memory bank.',
  },
});

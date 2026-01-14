import { fetchContext } from '../utils/api';

export default defineContentScript({
  matches: ['*://chatgpt.com/*', '*://claude.ai/*'],
  main() {
    console.log('MemRead content script loaded');

    // --- Ingestion Logic ---
    let lastMessageCount = 0;
    const observer = new MutationObserver(() => {
      const messages = document.querySelectorAll('[data-message-author-role]');
      if (messages.length > lastMessageCount) {
        // ... (existing ingestion logic) ...
        lastMessageCount = messages.length;
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // --- Injection Logic ---
    async function injectContext() {
      // Simple heuristic: If URL is "new chat" or no messages exist
      const isNewChat = window.location.pathname === '/' || window.location.pathname.includes('/new');
      
      if (isNewChat) {
        console.log('New chat detected, fetching context...');
        const data = await fetchContext('current project context'); // Simple query for now
        
        if (data.context && data.context.length > 0) {
          const contextText = `\n\n[System Note: ${data.context.join(' ')}]`;
          
          // Retry finding the textarea
          const interval = setInterval(() => {
            const textarea = document.querySelector('textarea');
            if (textarea) {
              clearInterval(interval);
              textarea.value = (textarea.value || '') + contextText;
              // Trigger input event to resize/activate button
              textarea.dispatchEvent(new Event('input', { bubbles: true }));
              console.log('Context injected!');
            }
          }, 500);
          
          // Stop retrying after 10 seconds
          setTimeout(() => clearInterval(interval), 10000);
        }
      }
    }

    // Run injection on load and URL change
    injectContext();
    
    // Watch for URL changes (SPA navigation)
    let lastUrl = location.href;
    new MutationObserver(() => {
      const url = location.href;
      if (url !== lastUrl) {
        lastUrl = url;
        injectContext();
      }
    }).observe(document, { subtree: true, childList: true });
  },
});

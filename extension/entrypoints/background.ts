import { ingestChat } from '../utils/api';

export default defineBackground(() => {
  console.log('MemRead background script running!');

  browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'INGEST_CHAT') {
      console.log('Ingesting chat:', message.payload);
      ingestChat(message.payload)
        .then((res) => sendResponse({ status: 'success', data: res }))
        .catch((err) => sendResponse({ status: 'error', error: err.message }));
      return true; // Keep channel open for async response
    }
  });
});

// Load the existing floating icon script
const script = document.createElement('script');
script.src = browser.runtime.getURL('assets/floatingIcon.ts-CJpmuZwW.js');
script.onload = function() {
  this.remove();
};

// Inject browser API compatibility for the floating icon script
const compatibilityScript = document.createElement('script');
compatibilityScript.textContent = `
  // Replace chrome.* with browser.* for Firefox compatibility
  if (typeof browser !== 'undefined' && typeof chrome === 'undefined') {
    window.chrome = browser;
  }
  
  // Ensure messaging works properly
  if (typeof browser !== 'undefined') {
    // Override chrome.runtime.sendMessage to use browser.runtime.sendMessage
    const originalChrome = window.chrome || {};
    window.chrome = {
      ...originalChrome,
      runtime: {
        ...originalChrome.runtime,
        sendMessage: function() {
          return browser.runtime.sendMessage.apply(browser.runtime, arguments);
        },
        onMessage: {
          addListener: function(listener) {
            return browser.runtime.onMessage.addListener(listener);
          }
        }
      },
      storage: {
        local: {
          get: function() {
            return browser.storage.local.get.apply(browser.storage.local, arguments);
          },
          set: function() {
            return browser.storage.local.set.apply(browser.storage.local, arguments);
          }
        }
      }
    };
  }
`;

// Inject compatibility first, then the floating icon script
(document.head || document.documentElement).appendChild(compatibilityScript);
(document.head || document.documentElement).appendChild(script);

// Forward messages to the background script
window.addEventListener('message', (event) => {
  if (event.source !== window || !event.data.type) return;
  
  if (event.data.type === 'RCP_MESSAGE') {
    browser.runtime.sendMessage(event.data.payload).then(response => {
      window.postMessage({
        type: 'RCP_RESPONSE',
        response: response
      }, '*');
    });
  }
});
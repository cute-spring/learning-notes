chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "translate",
    title: "Translate Selected Text",
    contexts: ["selection"]
  });
  chrome.contextMenus.create({
    id: "explain",
    title: "Explain Selected Text",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  const action = info.menuItemId;
  const selectedText = info.selectionText;
  if (!selectedText) return;

  // Ensure we're on a page where we can inject content scripts.
  if (!tab || !tab.id || !tab.url || (!tab.url.startsWith("http://") && !tab.url.startsWith("https://"))) {
    console.error("Content script cannot be injected on this page.");
    return;
  }

  // Function to send a message to the content script.
  const sendMessageToContentScript = () => {
    chrome.tabs.sendMessage(tab.id, { action: action, type: "loading" }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error sending loading message:", chrome.runtime.lastError.message);
      }
    });
  };

  // First try to send the message.
  chrome.tabs.sendMessage(tab.id, { action: action, type: "loading" }, (response) => {
    if (chrome.runtime.lastError) {
      // If content script is not present, try to inject it.
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
      }, () => {
        if (chrome.runtime.lastError) {
          console.error("Error injecting content script:", chrome.runtime.lastError.message);
        } else {
          // Now that the content script is injected, send the message.
          sendMessageToContentScript();
        }
      });
    }
  });

  // Determine the correct FastAPI endpoint.
  const endpoint = action === "translate" ?
    "http://localhost:8000/translate" :
    "http://localhost:8000/explain";

  // Call the FastAPI service.
  fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: selectedText })
  })
    .then(response => response.json())
    .then(data => {
      chrome.tabs.sendMessage(tab.id, {
        action: action,
        type: "result",
        result: data.result
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error sending result message:", chrome.runtime.lastError.message);
        }
      });
    })
    .catch(error => {
      console.error("Fetch error:", error);
      chrome.tabs.sendMessage(tab.id, {
        action: action,
        type: "error",
        error: error.toString()
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error sending error message:", chrome.runtime.lastError.message);
        }
      });
    });
});
// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "loading") {
    createOrUpdatePopup("Loading...");
  } else if (message.type === "result") {
    createOrUpdatePopup(message.result);
  } else if (message.type === "error") {
    createOrUpdatePopup("Error: " + message.error);
  }
});

// Create or update the floating popup
function createOrUpdatePopup(content) {
  let popup = document.getElementById("ollama-popup");
  if (!popup) {
    popup = document.createElement("div");
    popup.id = "ollama-popup";
    // Optimized inline styling
    popup.style.position = "fixed"; // or "absolute"
    popup.style.top = "50%"; // or "20px"
    popup.style.left = "50%";
    popup.style.transform = "translate(-50%, -50%)"; // to center the popup
    popup.style.backgroundColor = "#fff";
    popup.style.border = "1px solid #ccc";
    popup.style.padding = "20px";
    popup.style.zIndex = "9999";
    popup.style.maxWidth = "700px"; // Increased width
    popup.style.maxHeight = "500px"; // Added max height
    popup.style.overflowY = "auto"; // Added vertical overflow
    popup.style.boxShadow = "0 4px 16px rgba(0,0,0,0.3)";
    popup.style.borderRadius = "8px"; // Increased border radius for a softer look
    popup.style.fontFamily = "Arial, sans-serif";
    popup.style.fontSize = "14px"; // Increased font size for better readability
    popup.style.lineHeight = "1.5"; // Added line height for better spacing

    // Create a close button
    const closeBtn = document.createElement("span");
    closeBtn.innerText = "✖";
    closeBtn.style.float = "right";
    closeBtn.style.cursor = "pointer";
    closeBtn.style.marginLeft = "10px"; // Added margin to separate it from content
    closeBtn.onclick = () => {
      popup.remove();
    };
    popup.appendChild(closeBtn);

    // Content container
    const contentDiv = document.createElement("div");
    contentDiv.id = "ollama-popup-content";
    contentDiv.style.clear = "both";
    contentDiv.style.paddingTop = "10px"; // Increased padding top for better spacing
    popup.appendChild(contentDiv);

    // Add a fade-in effect
    popup.style.opacity = "0";
    popup.style.transition = "opacity 0.5s";
    setTimeout(() => {
      popup.style.opacity = "1";
    }, 10);

    document.body.appendChild(popup);
  }
  // Update the content
  const contentDiv = document.getElementById("ollama-popup-content");
  contentDiv.innerText = content;
}

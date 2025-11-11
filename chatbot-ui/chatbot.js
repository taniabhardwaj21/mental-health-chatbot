const API_URL ="http://127.0.0.1:8000/";
const session_id = "user_"+Math.floor(Math.random()*10000);
const video = document.getElementById("video");
const emotion="neutral";
class MindfulChatbot {
  constructor() {
    this.messagesContainer = document.getElementById("messagesContainer");
    this.messageForm = document.getElementById("messageForm");
    this.messageInput = document.getElementById("messageInput");
    this.typingTemplate = document.getElementById("typingIndicator");
    this.init();
  }

  init() {
    this.messageForm.addEventListener("submit", (e) =>
      this.handleSendMessage(e)
    );
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.messageForm.dispatchEvent(new Event("submit"));
      }
    });
  }

  async handleSendMessage(e) {
    e.preventDefault();
    const message = "the users current state of emotion is"+ emotion + this.messageInput.value.trim();

    if (!message) return;

    // Add user message to UI
    this.addMessage(message, "user");
    this.messageInput.value = "";
    this.messageInput.focus();

    // Show typing indicator
    this.showTypingIndicator();

    // Send to backend
    try {
      const response = await this.sendToBackend(message);
      this.removeTypingIndicator();
      this.addMessage(response, "bot");
    } catch (error) {
      console.error("Error:", error);
      this.removeTypingIndicator();
      this.addMessage("I had trouble connecting. Please try again.", "bot");
    }
  }

  addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    if (sender === "bot") {
      messageDiv.innerHTML = `
                <div class="message-avatar">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="50" cy="50" r="45" fill="url(#gradientMsg)" opacity="0.9"/>
                        <defs>
                            <linearGradient id="gradientMsg" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#a78bfa;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#60a5fa;stop-opacity:1" />
                            </linearGradient>
                        </defs>
                        <circle cx="35" cy="40" r="4" fill="#fff"/>
                        <circle cx="65" cy="40" r="4" fill="#fff"/>
                        <path d="M 40 60 Q 50 68 60 60" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="message-content">
                    <p>${this.escapeHtml(text)}</p>
                </div>
            `;
    } else {
      messageDiv.innerHTML = `
                <div class="message-avatar"></div>
                <div class="message-content">
                    <p>${this.escapeHtml(text)}</p>
                </div>
            `;
    }

    this.messagesContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }

  showTypingIndicator() {
    const typingDiv = this.typingTemplate.content.cloneNode(true);
    this.messagesContainer.appendChild(typingDiv);
    this.scrollToBottom();
  }

  removeTypingIndicator() {
    const typing = this.messagesContainer.querySelector(".typing-message");
    if (typing) typing.remove();
  }

  async sendToBackend(message) {
    // Replace this with your actual backend URL and endpoint
    // Example: const response = await fetch('http://localhost:5000/api/chat', {...})

    try {
      const response = await fetch(API_URL+"chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ session_id , query:message }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      return data.response || "I understood that. Tell me more.";
    } catch (error) {
      // Fallback for development
      console.warn("Backend connection failed. Using fallback responses.");
      return this.getFallbackResponse(message);
    }
  }

  getFallbackResponse(userMessage) {
    const responses = [
      "That sounds important. How does that make you feel?",
      "I hear you. Can you tell me more about that?",
      "That's something many people experience. What matters most to you right now?",
      "Thank you for sharing that. What would help you feel better?",
      "I'm listening. What else is on your mind?",
      "That's a valid feeling. How can I support you?",
      "I appreciate you opening up. What do you think you need right now?",
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new MindfulChatbot();
});

//start webcam

navigator.mediaDevices.getUserMedia({video:true})
.then(stream => { video.srcObject=stream;})
.catch(err => console.error("camera error :",err));

//capture frame every 30s
setInterval(async ()=>{
    const canvas =document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video,0,0);
    const imgData =canvas.toDataURL('image/jpeg');

    const response = await fetch(API_URL+"emotion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body:JSON.stringify({frame: imgData})
    });
    if (!response.ok) throw new Error("emotion recognition did not work");

    const data = await response.json();
    emotion=data.emotion;
},10000);

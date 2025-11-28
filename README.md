## 🧠 AI Mental Health Chatbot

### *An Emotion-Aware Conversational Companion using Gemini LLM + DeepFace + FastAPI*

---

### 🌟 **Overview**

This project is an **AI-powered Mental Health Chatbot** that blends conversational intelligence with real-time **emotion analysis**.
It uses **Google’s Gemini 2.5 LLM** to generate context-aware, empathetic responses and **DeepFace** to interpret users’ facial emotions from webcam images — combining text and emotion signals for a more human-like interaction.

---

### 🎯 **Objectives**

* To build a chatbot that can engage users empathetically in mental health conversations.
* To integrate **emotion detection** for enhanced context and personalization.
* To maintain conversational memory using **LangChain’s conversation buffer**.
* To enable smooth backend–frontend communication using **FastAPI** and **JavaScript**.

---

### ⚙️ **System Architecture**

#### 🧩 Components

1. **Frontend (HTML, CSS, JS)**

   * Captures user input and periodically sends webcam frames for emotion detection.
   * Displays AI-generated responses in a chat-like UI.

2. **Backend (FastAPI)**

   * Handles chat (`/chat`) and emotion (`/emotion`) endpoints.
   * Integrates Gemini API for text generation.
   * Uses DeepFace for facial emotion detection.
   * Logs conversations and emotional state for session tracking.

3. **AI Models**

   * **Gemini 2.5 Flash** — conversational language model (via `langchain_google_genai`).
   * **DeepFace** — image-based emotion analysis using facial expressions.

---

### 🧠 **System Workflow**

1. **User sends a message** through the frontend chat interface.
2. **FastAPI backend** receives the message via `/chat`.
3. If a webcam frame is sent, the `/emotion` endpoint analyzes it with **DeepFace**.
4. The current **emotion state** + text query are passed to **Gemini LLM**.
5. The chatbot generates a **context-aware, emotionally aligned response**.
6. The conversation (including detected emotion) is logged for session continuity.

---

### 🛠️ **Tech Stack**

| Category                   | Tools / Libraries                                          |
| -------------------------- | ---------------------------------------------------------- |
| **Language**               | Python, JavaScript                                         |
| **Backend Framework**      | FastAPI                                                    |
| **AI / NLP**               | LangChain, Gemini 2.5 Flash (via `langchain-google-genai`) |
| **Emotion Detection**      | DeepFace, OpenCV                                           |
| **Frontend**               | HTML, CSS, Vanilla JS                                      |
| **Data Handling**          | NumPy, Base64                                              |
| **Environment Management** | Conda / Python-dotenv                                      |
| **Server**                 | Uvicorn                                                    |

---

### 📦 **Installation Guide**

#### 🧰 Step 1: Clone the Repository

```bash
git clone https://github.com/diwansanyam/mental-health-chatbot.git
cd mental-health-chatbot
```

#### 🧪 Step 2: Create Virtual Environment

```bash
conda create -n mental_health_cb python=3.10
conda activate mental_health_cb
```

#### 🧩 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### 🔐 Step 4: Add Environment Variables

Create a `.env` file in your project root:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

#### 🚀 Step 5: Run the FastAPI Server

```bash
uvicorn main:app --reload
```

Server will start on 👉 `http://127.0.0.1:8000`

#### 💬 Step 6: Run the Frontend

Simply open `frontend/index.html` in your browser.
If CORS issues arise, serve it locally:

```bash
python -m http.server 5500
```

Then open 👉 `http://127.0.0.1:5500/frontend/index.html`

---

### 📸 **Emotion Detection Integration**

* The frontend captures a webcam image every 60 seconds.
* The image is converted to **Base64** and sent to `/emotion`.
* DeepFace predicts the dominant emotion (`happy`, `sad`, `angry`, etc.).
* The backend passes both **text query** and **emotion label** to Gemini for emotionally aligned responses.

---

### 📈 **Expected Outcomes**

* Real-time **emotional intelligence** in chatbot conversations.
* Seamless integration of **multimodal AI** (text + image).
* Improved **user engagement and empathy** in mental health support systems.

---

### 🚧 **Future Scope**

* Integrate **voice recognition & tone analysis** for richer context.
* Deploy as a **progressive web app (PWA)** with user authentication.
* Add a **data analytics dashboard** to monitor emotional trends.
* Integrate a **mental health resource recommender system** using vector databases.

---

### 💡 **Conclusion**

This project showcases how **AI can be used responsibly and empathetically** in mental health domains.
By combining **Gemini LLM’s conversational intelligence** with **DeepFace emotion recognition**, we bridge the gap between machine understanding and human empathy.

---

### 👩‍💻 **Author**

**Tania Bhardwaj**
🧩 Built with 💙 using Python, FastAPI, LangChain, and DeepFace
📫 taniabhardwaj6086@gmail.com



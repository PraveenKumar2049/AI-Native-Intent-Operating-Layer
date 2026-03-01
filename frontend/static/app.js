/* ==================== STATE ==================== */

let sessions = [];
let activeSession = null;
let chatStarted = false;
let currentStreamController = null;


/* ==================== SESSION MANAGEMENT ==================== */

function createSession() {
    const id = Date.now();

    sessions.push({
        id: id,
        title: "New Chat",
        messages: []
    });

    activeSession = id;
    chatStarted = false;

    setDockCentered();
    renderSidebar();
    renderChat();
}


/* ==================== SIDEBAR ==================== */

function toggleSidebar() {
    document.querySelector(".layout").classList.toggle("collapsed");
}

function renderSidebar() {
    const history = document.getElementById("chatHistory");
    history.innerHTML = "";

    sessions.forEach(session => {
        const div = document.createElement("div");
        div.className = "history-item" +
            (session.id === activeSession ? " active" : "");

        div.innerText = session.title;

        div.onclick = () => {
            activeSession = session.id;
            renderSidebar();
            renderChat();

            const sessionData = sessions.find(s => s.id === activeSession);
            sessionData.messages.length === 0
                ? setDockCentered()
                : setDockBottom();
        };

        history.appendChild(div);
    });
}


/* ==================== CHAT RENDERING ==================== */

function renderChat() {
    const container = document.getElementById("chatContainer");
    container.innerHTML = "";

    const session = sessions.find(s => s.id === activeSession);
    if (!session || session.messages.length === 0) {
        container.innerHTML = `
            <div id="welcomeBlock" class="welcome-block">
                <h1>ZeroTouch</h1>
                <p>Intelligent Operating Layer</p>
            </div>
        `;
        return;
    }

    session.messages.forEach(msg => {
        container.appendChild(createMessageElement(msg));
    });

    scrollToBottom();
}

function createMessageElement(msg) {
    const div = document.createElement("div");
    div.className = "message " + msg.role;

    if (msg.typing) {
        div.innerHTML = `
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        `;
    } else {
        // ✅ Only AI messages render Markdown
        if (msg.role === "ai") {
            div.innerHTML = marked.parse(msg.text || "");
        } else {
            div.textContent = msg.text;
        }
    }

    return div;
}

function scrollToBottom() {
    const container = document.getElementById("chatContainer");
    container.scrollTop = container.scrollHeight;
}


/* ==================== STREAMING MESSAGE FLOW ==================== */

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();
    if (!text || !activeSession) return;

    const session = sessions.find(s => s.id === activeSession);

    if (session.messages.length === 0) {
        session.title = generateTitle(text);
        renderSidebar();
    }

    session.messages.push({ role: "user", text });
    input.value = "";

    if (!chatStarted) startChatMode();
    renderChat();

    const aiMessage = { role: "ai", text: "", typing: true };
    session.messages.push(aiMessage);
    renderChat();

    if (currentStreamController) {
        currentStreamController.abort();
    }

    currentStreamController = new AbortController();

    try {
        const response = await fetch("/chat-stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
            signal: currentStreamController.signal
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let buffer = "";
        let firstToken = false;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            let boundary;
            while ((boundary = buffer.indexOf("\n\n")) !== -1) {
                const chunk = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + 2);

                if (!chunk.startsWith("data: ")) continue;

                const payload = chunk.replace("data: ", "").trim();

                if (payload === "[DONE]") {
                    aiMessage.typing = false;
                    renderChat();
                    scrollToBottom();
                    return;
                }

                let parsed;
                try {
                    parsed = JSON.parse(payload);
                } catch {
                    continue;
                }

                if (parsed.error) {
                    aiMessage.typing = false;
                    aiMessage.text = "Error: " + parsed.error;
                    renderChat();
                    return;
                }

                if (!firstToken) {
                    aiMessage.typing = false;
                    aiMessage.text = "";
                    firstToken = true;
                }

                aiMessage.text += parsed.token || "";
                updateLastMessage(aiMessage);
                scrollToBottom();
            }
        }

        aiMessage.typing = false;
        renderChat();

    } catch (err) {
        if (err.name !== "AbortError") {
            console.error("Streaming error:", err);
            aiMessage.typing = false;
            aiMessage.text = "Connection error.";
            renderChat();
        }
    }
}


/* ==================== UPDATE LAST MESSAGE ==================== */

function updateLastMessage(messageObj) {
    const container = document.getElementById("chatContainer");
    const lastMessage = container.lastElementChild;
    if (!lastMessage) return;

    lastMessage.className = "message ai";
    lastMessage.innerHTML = marked.parse(messageObj.text || "");
}


/* ==================== STOP STREAM ==================== */

function stopStreaming() {
    if (currentStreamController) {
        currentStreamController.abort();
    }
}


/* ==================== TITLE GENERATION ==================== */

function generateTitle(text) {
    const trimmed = text.substring(0, 20);
    return trimmed.length < text.length ? trimmed + "..." : trimmed;
}


/* ==================== DOCK CONTROL ==================== */

function startChatMode() {
    chatStarted = true;
    setDockBottom();

    const welcome = document.getElementById("welcomeBlock");
    if (welcome) welcome.style.opacity = "0";
}

function setDockCentered() {
    const wrapper = document.getElementById("dockWrapper");
    wrapper.classList.remove("bottom");
    wrapper.classList.add("centered");
}

function setDockBottom() {
    const wrapper = document.getElementById("dockWrapper");
    wrapper.classList.remove("centered");
    wrapper.classList.add("bottom");
}


/* ==================== INPUT EVENTS ==================== */

function handleKey(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
}

function handleUpload() {
    console.log("Upload clicked (backend ready)");
}


/* ==================== VOICE HANDLER ==================== */

async function handleMic() {
    if (!activeSession) return;

    const session = sessions.find(s => s.id === activeSession);

    if (!chatStarted) startChatMode();

    try {
        const listeningMsg = { role: "ai", text: "🎙 Listening...", typing: true };
        session.messages.push(listeningMsg);
        renderChat();
        scrollToBottom();

        const response = await fetch("/voice-chat", {
            method: "POST"
        });

        const data = await response.json();

        session.messages.pop();

        if (data.error) {
            session.messages.push({
                role: "ai",
                text: "Error: " + data.error
            });
            renderChat();
            return;
        }

        if (session.messages.length === 0) {
            session.title = generateTitle(data.user_text);
            renderSidebar();
        }

        session.messages.push({
            role: "user",
            text: data.user_text
        });

        session.messages.push({
            role: "ai",
            text: data.response
        });

        renderChat();
        scrollToBottom();

    } catch (err) {
        console.error("Voice error:", err);

        session.messages.push({
            role: "ai",
            text: "Voice connection error."
        });

        renderChat();
    }
}


/* ==================== INIT ==================== */

document.addEventListener("DOMContentLoaded", () => {
    createSession();
    setDockCentered();
});
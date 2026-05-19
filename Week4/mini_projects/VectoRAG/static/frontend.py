css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --accent: #7c6aff;
    --accent2: #ff6a9a;
    --green: #4affb4;
    --text: #e8e8f0;
    --muted: #6b6b80;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

.block-container { padding-top: 2rem !important; max-width: 1100px; }

h1, h2, h3 { font-family: 'Syne', sans-serif; }

/* Header */
.vecto-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2rem;
}
.vecto-logo {
    font-size: 2.6rem;
    line-height: 1;
}
.vecto-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.vecto-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Status pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: var(--surface2);
    margin-bottom: 1.5rem;
}
.status-pill.ready {
    border-color: var(--green);
    color: var(--green);
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }

/* Chat area */
.chat-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    min-height: 360px;
    max-height: 480px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 14px;
}
.msg-user .bubble {
    background: var(--accent);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 16px;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 14px;
    gap: 10px;
}
.ai-avatar {
    font-size: 1.3rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.msg-ai .bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 4px 18px 18px 18px;
    padding: 10px 16px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.6;
    font-family: 'Space Mono', monospace;
}
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    text-align: center;
    gap: 8px;
}
.empty-icon { font-size: 2.5rem; opacity: 0.4; }

/* Sidebar sections */
.sidebar-section {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.sidebar-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
}

/* Streamlit overrides */
[data-testid="stFileUploader"] { color: var(--text); }
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    width: 100%;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.danger-btn > button {
    background: #3a1a24 !important;
    border: 1px solid var(--accent2) !important;
    color: var(--accent2) !important;
}

/* Metrics */
.metric-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.2rem;
}
.metric-card {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
}
.metric-val {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent);
}
.metric-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
</style>
"""


sidebar = """
    <div style="margin-bottom:1.5rem">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
                    background:linear-gradient(135deg,#7c6aff,#ff6a9a);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            ⬡ VectoRAG
        </div>
        <div style="font-family:'Space Mono',monospace;font-size:0.6rem;
                    color:#6b6b80;letter-spacing:0.14em;text-transform:uppercase;">
            In-memory vector search
        </div>
    </div>
    """

jina_css = """
    <div style="margin-top:auto;padding-top:2rem;font-family:'Space Mono',monospace;
                font-size:0.6rem;color:#3a3a50;text-align:center;">
        GROQ · JINA AI · QDRANT<br>in-memory · session-scoped
    </div>
    """


main = """
<div class="vecto-header">
    <div class="vecto-logo">⬡</div>
    <div>
        <div class="vecto-title">VectoRAG</div>
        <div class="vecto-sub">Retrieval-Augmented Generation · Jina + Groq + Qdrant</div>
    </div>
</div>
"""

chat_css = """
    <div class="empty-state">
        <div class="empty-icon">⬡</div>
        <div>Upload & vectorize documents,<br>then ask anything about them.</div>
    </div>"""


sidebar_txt = '<div class="sidebar-label">Upload documents</div>'
div_style = "<div style='height:12px'></div>"
database_side = '<div class="sidebar-label" style="margin-top:0.5rem">Database</div>'
danger_button = '<div class="danger-btn">'
div = "</div>"
status_pill_ready = '<div class="status-pill ready"><span class="dot"></span>Vector DB ready</div>'
status_pill_unready = '<div class="status-pill"><span class="dot"></span>No documents indexed</div>'
chat_container = '<div class="chat-container">'


def state_user(state, content):
    if state:
        return f'<div class="msg-user"><div class="bubble">{content}</div></div>'
    else:
        return f'<div class="msg-ai"><div class="ai-avatar">⬡</div><div class="bubble">{content}</div></div>'

def session_state(metric_val, session_messages):
    return f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-val">{metric_val}</div>
                <div class="metric-lbl">Chunks</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{session_messages}</div>
                <div class="metric-lbl">Turns</div>
            </div>
        </div>
        """

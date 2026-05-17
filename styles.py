import streamlit as st


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #07090d;
    --bg-2: #0d1118;
    --panel: rgba(15, 20, 29, 0.92);
    --panel-2: rgba(24, 29, 38, 0.82);
    --line: rgba(255, 109, 64, 0.22);
    --line-strong: rgba(255, 109, 64, 0.54);
    --oxide: #ff5b38;
    --oxide-dark: #8f2d22;
    --copper: #d98b45;
    --cyan: #63d8ff;
    --green: #73e0a9;
    --text: #f2f4f8;
    --text-soft: #c8d0dc;
    --muted: #7e8897;
    --dim: #4b5563;
    --shadow: 0 18px 56px rgba(0, 0, 0, 0.42);
    --glow-red: 0 0 30px rgba(255, 91, 56, 0.18);
    --font-display: 'Rajdhani', sans-serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'Space Mono', monospace;
}

html,
body,
.stApp {
    background:
        radial-gradient(circle at 18% 8%, rgba(255, 91, 56, 0.16), transparent 34%),
        radial-gradient(circle at 82% 22%, rgba(99, 216, 255, 0.08), transparent 28%),
        linear-gradient(180deg, #07090d 0%, #0c1119 52%, #08090d 100%) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        linear-gradient(rgba(255, 109, 64, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99, 216, 255, 0.035) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: linear-gradient(180deg, rgba(0,0,0,0.65), transparent 82%);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background: linear-gradient(115deg, transparent 0 58%, rgba(255, 91, 56, 0.05) 58.2%, transparent 72%);
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    max-width: 1200px !important;
    padding: 1.5rem 2.1rem 7rem !important;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(10, 13, 19, 0.98), rgba(18, 23, 31, 0.98)) !important;
    border-right: 1px solid rgba(255, 109, 64, 0.24) !important;
    box-shadow: 16px 0 54px rgba(0, 0, 0, 0.36);
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    inset: 0 0 auto 0;
    height: 3px;
    background: linear-gradient(90deg, var(--oxide), var(--cyan), transparent);
}

[data-testid="stSidebarHeader"] {
    height: 54px !important;
    align-items: center !important;
}

[data-testid="stSidebarCollapseButton"] {
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button,
button[data-testid="stExpandSidebarButton"],
button[data-testid="stBaseButton-headerNoPadding"] {
    opacity: 1 !important;
    visibility: visible !important;
    width: 34px !important;
    height: 34px !important;
    border: 1px solid rgba(255, 109, 64, 0.42) !important;
    border-radius: 4px !important;
    background: rgba(255, 91, 56, 0.12) !important;
    color: var(--text) !important;
    box-shadow: 0 0 18px rgba(255, 91, 56, 0.18) !important;
}

[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarCollapsedControl"] button:hover,
button[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stBaseButton-headerNoPadding"]:hover {
    border-color: var(--line-strong) !important;
    background: rgba(255, 91, 56, 0.22) !important;
}

[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapsedControl"] span,
button[data-testid="stExpandSidebarButton"] span,
button[data-testid="stBaseButton-headerNoPadding"] span {
    color: var(--text) !important;
    opacity: 1 !important;
}

.sidebar-brand {
    padding: 18px 0 20px;
    border-bottom: 1px solid rgba(255, 109, 64, 0.18);
    margin-bottom: 18px;
    text-align: left;
}

.sidebar-brand-name {
    font-family: var(--font-display);
    font-size: 1.75rem;
    line-height: 1;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.12em;
}

.sidebar-brand-name::before {
    content: 'COMMAND // ';
    display: block;
    margin-bottom: 6px;
    color: var(--oxide);
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
}

.sidebar-brand-sub {
    margin-top: 7px;
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 0.62rem;
    line-height: 1.6;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.ares-header {
    display: grid;
    grid-template-columns: 72px minmax(0, 1fr);
    align-items: center;
    gap: 18px;
    margin: 8px 0 22px;
    padding: 18px 0 8px;
}

.ares-logo {
    width: 68px;
    height: 68px;
    display: grid;
    place-items: center;
    color: var(--text);
    background:
        linear-gradient(135deg, rgba(255, 91, 56, 0.2), rgba(99, 216, 255, 0.06)),
        #10151d;
    border: 1px solid var(--line-strong);
    border-radius: 6px;
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    box-shadow: var(--glow-red), inset 0 0 22px rgba(255, 91, 56, 0.08);
    clip-path: polygon(10% 0, 100% 0, 100% 76%, 86% 100%, 0 100%, 0 16%);
}

.ares-title {
    font-family: var(--font-display) !important;
    font-size: clamp(2.4rem, 5vw, 4.6rem) !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    color: var(--text) !important;
    line-height: 0.86 !important;
    margin: 0 !important;
    text-transform: uppercase;
}

.ares-title::after {
    content: '';
    display: block;
    width: min(420px, 70vw);
    height: 3px;
    margin-top: 14px;
    background: linear-gradient(90deg, var(--oxide), var(--copper), var(--cyan), transparent);
    box-shadow: var(--glow-red);
}

.ares-subtitle {
    margin-top: 10px !important;
    color: var(--text-soft) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}

.stat-card,
.ares-response,
div[data-testid="stStatusWidget"],
.stAlert {
    background:
        linear-gradient(145deg, rgba(255, 91, 56, 0.075), transparent 38%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.045), rgba(255, 255, 255, 0.018)),
        var(--panel) !important;
    border: 1px solid var(--line) !important;
    border-radius: 6px !important;
    box-shadow: var(--shadow) !important;
}

.stat-card {
    position: relative;
    overflow: hidden;
    padding: 16px 18px;
}

.stat-card::before {
    content: '';
    position: absolute;
    inset: 0 auto 0 0;
    width: 3px;
    background: linear-gradient(180deg, var(--oxide), var(--cyan));
}

.stat-label {
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}

.stat-value {
    margin-top: 6px;
    color: var(--text);
    font-family: var(--font-display);
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.stat-sub {
    margin-top: 2px;
    color: var(--muted);
    font-size: 0.76rem;
}

.mode-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 40px;
    gap: 8px;
    padding: 8px 14px;
    border: 1px solid var(--line-strong);
    border-radius: 6px;
    background: rgba(255, 91, 56, 0.1);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    white-space: nowrap;
}

.mode-dot {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    background: var(--oxide);
    box-shadow: 0 0 16px rgba(255, 91, 56, 0.65);
}

.mode-doc {
    background: rgba(115, 224, 169, 0.1);
    border-color: rgba(115, 224, 169, 0.42);
}

.mode-doc .mode-dot {
    background: var(--green);
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.ares-response {
    margin: 8px 0 12px;
    padding: 22px 24px;
    color: var(--text-soft);
    line-height: 1.72;
    font-size: 0.96rem;
    border-left: 4px solid var(--oxide) !important;
}

.ares-response strong {
    color: var(--cyan) !important;
    font-family: var(--font-display);
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.step-trail {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 7px;
    margin: 10px 0 12px;
}

.step-pill {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border: 1px solid rgba(99, 216, 255, 0.22);
    border-radius: 4px;
    background: rgba(99, 216, 255, 0.07);
    color: var(--text-soft);
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.step-arrow {
    color: var(--oxide);
    font-family: var(--font-mono);
    font-size: 0.72rem;
}

.step-1 { border-color: rgba(255, 91, 56, 0.44); }
.step-2 { border-color: rgba(99, 216, 255, 0.34); }
.step-3 { border-color: rgba(217, 139, 69, 0.38); }
.step-4 { border-color: rgba(115, 224, 169, 0.34); }

.sources-container {
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 109, 64, 0.16);
}

.sources-label {
    margin-bottom: 8px;
    color: var(--oxide);
    font-family: var(--font-mono);
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.source-chip {
    display: inline-flex;
    align-items: center;
    margin: 3px;
    padding: 5px 10px;
    border: 1px solid rgba(255, 109, 64, 0.24);
    border-radius: 4px;
    background: rgba(255, 91, 56, 0.07);
    color: var(--text-soft);
    font-size: 0.78rem;
    text-decoration: none;
    transition: all 0.18s ease;
}

.source-chip:hover {
    border-color: var(--line-strong);
    background: rgba(255, 91, 56, 0.14);
    color: var(--text);
    text-decoration: none;
}

.agent-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 8px;
}

.agent-pill {
    padding: 8px 10px;
    border: 1px solid rgba(255, 109, 64, 0.22) !important;
    border-radius: 4px;
    background: rgba(255, 91, 56, 0.06);
    color: var(--text-soft) !important;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-align: center;
    text-transform: uppercase;
}

.ares-confidence {
    margin-top: 10px;
    padding: 11px 14px;
    border: 1px solid rgba(99, 216, 255, 0.24);
    border-radius: 4px;
    background: rgba(99, 216, 255, 0.06);
    color: var(--text-soft);
    font-family: var(--font-mono);
    font-size: 0.76rem;
    letter-spacing: 0.02em;
}

.ares-confidence b {
    color: var(--cyan);
}

.stButton > button {
    background: linear-gradient(180deg, rgba(255, 91, 56, 0.18), rgba(255, 91, 56, 0.08)) !important;
    border: 1px solid rgba(255, 109, 64, 0.34) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    transition: all 0.18s ease !important;
}

.stButton > button:hover {
    background: rgba(255, 91, 56, 0.18) !important;
    border-color: var(--line-strong) !important;
    box-shadow: var(--glow-red) !important;
    transform: translateY(-1px);
}

.stFileUploader > div {
    background: rgba(15, 20, 29, 0.74) !important;
    border: 1px dashed rgba(99, 216, 255, 0.28) !important;
    border-radius: 6px !important;
}

[data-testid="stChatInput"] > div {
    background: rgba(8, 11, 16, 0.98) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: 6px !important;
    box-shadow: 0 -12px 36px rgba(0, 0, 0, 0.3), var(--glow-red) !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {
    color: var(--text) !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--cyan) !important;
}

div[data-baseweb="select"] > div {
    background: rgba(15, 20, 29, 0.9) !important;
    border: 1px solid rgba(255, 109, 64, 0.3) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}

label,
.stCaption {
    color: var(--muted) !important;
}

.stDivider {
    border-color: var(--line) !important;
}

#MainMenu,
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


@media (max-width: 760px) {
    .main .block-container {
        padding: 1rem 1rem 6rem !important;
    }

    .ares-header {
        grid-template-columns: 54px minmax(0, 1fr);
        gap: 12px;
    }

    .ares-logo {
        width: 52px;
        height: 52px;
        font-size: 1.6rem;
    }

    .stat-row {
        grid-template-columns: 1fr;
    }

    .mode-badge {
        width: 100%;
    }
}
</style>
"""


def apply_global_styles():
    st.markdown(STYLES, unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfReader

from pipeline import run_pipeline
from render import render_assistant_message
from styles import apply_global_styles

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ARES AI — Adaptive Research & Exploration System",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Deep space glassmorphism theme
# ─────────────────────────────────────────────
apply_global_styles()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in [
    ("messages", []),
    ("sources", {}),
    ("pdf_text", None),
    ("last_uploaded_file", None),
    ("rerun_query", None),
    ("total_queries", 0),
    ("agents_run", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">ARES AI</div>
        <div class="sidebar-brand-sub">Adaptive Research & Exploration System</div>
    </div>
    """, unsafe_allow_html=True)

    # Active agents display
    st.markdown('<div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;">Mission Agents</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="agent-grid">
        <div class="agent-pill">Recon</div>
        <div class="agent-pill">Analyze</div>
        <div class="agent-pill">Synthesize</div>
        <div class="agent-pill">Report</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    research_mode = st.selectbox(
        "Research Depth",
        [
            "Quick Answer",
            "Detailed Analysis",
            "Research Report"
        ]
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">Mission Log</div>', unsafe_allow_html=True)

    user_questions = [
        (i, msg["content"])
        for i, msg in enumerate(st.session_state.messages)
        if msg["role"] == "user"
    ]

    if not user_questions:
        st.markdown('<div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--dim);padding:12px 0;">No missions yet.<br/>Enter an objective below.</div>', unsafe_allow_html=True)
    else:
        for idx, (msg_index, question) in enumerate(reversed(user_questions)):
            display_text = question if len(question) <= 52 else question[:49] + "..."
            num = len(user_questions) - idx
            label = f"Q{num}. {display_text}"
            if st.button(label, key=f"q_{msg_index}", use_container_width=True):
                st.session_state.rerun_query = question

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.sources = {}
            st.session_state.rerun_query = None
            st.session_state.total_queries = 0
            st.session_state.agents_run = 0
            st.rerun()
    with col2:
        st.markdown(f'<div style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted);text-align:center;padding-top:8px;">{len(user_questions)} missions</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:var(--font-mono);font-size:0.6rem;color:var(--dim);text-align:center;line-height:1.8;padding:10px 0;border-top:1px solid rgba(255,109,64,0.18);">
        LLaMA3 · Ollama · DuckDuckGo<br/>
        Recon · Analysis · Exploration
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="ares-header">
    <div class="ares-logo">A</div>
    <div>
        <div class="ares-title">ARES AI</div>
        <div class="ares-subtitle">Adaptive Research & Exploration System · Multi-Agent Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stat row
q_count = st.session_state.total_queries
agent_count = st.session_state.agents_run
mode_active = "Document" if st.session_state.pdf_text else "Web Search"
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-label">Missions Run</div>
        <div class="stat-value">{q_count:02d}</div>
        <div class="stat-sub">This session</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Agent Calls</div>
        <div class="stat-value">{agent_count:02d}</div>
        <div class="stat-sub">LLM calls made</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Data Mode</div>
        <div class="stat-value" style="font-size:1.1rem;padding-top:4px;">{'📄 Doc' if st.session_state.pdf_text else '🌐 Web'}</div>
        <div class="stat-sub">{mode_active} retrieval</div>
    </div>
</div>
""", unsafe_allow_html=True)

# PDF upload in a tight row with mode badge
col_upload, col_mode = st.columns([3, 1])
with col_upload:
    uploaded_file = st.file_uploader(
        "Upload a PDF document (optional)",
        type=["pdf"],
        label_visibility="collapsed",
    )
with col_mode:
    if st.session_state.pdf_text:
        st.markdown('<div class="mode-badge mode-doc"><span class="mode-dot"></span>Document Mode</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mode-badge mode-web"><span class="mode-dot"></span>Web Mode</div>', unsafe_allow_html=True)

# PDF caching
if uploaded_file is not None:
    if st.session_state.last_uploaded_file != uploaded_file.name:
        with st.spinner("Parsing PDF..."):
            reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            st.session_state.pdf_text = text
            st.session_state.last_uploaded_file = uploaded_file.name
        st.success(f"✅ Loaded **{uploaded_file.name}** — {len(text):,} characters extracted")
else:
    st.session_state.pdf_text = None
    st.session_state.last_uploaded_file = None

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# RENDER CHAT HISTORY
# ─────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_assistant_message(msg, st.session_state.sources.get(i))
        else:
            st.markdown(msg["content"])

# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────
query = st.chat_input("Enter a research objective for ARES AI...")

if st.session_state.rerun_query:
    rerun_q = st.session_state.rerun_query
    st.session_state.rerun_query = None
    st.info(f"↻ Re-running: *{rerun_q}*")
    run_pipeline(rerun_q, research_mode)
elif query:
    run_pipeline(query, research_mode)

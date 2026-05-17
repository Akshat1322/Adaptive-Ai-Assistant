import streamlit as st


STEP_ICONS = ["Search", "Research", "Summary", "Answer"]
STEP_CLASSES = ["step-1", "step-2", "step-3", "step-4"]


def render_step_trail(steps_text):
    parts = [s.strip() for s in steps_text.replace("→", "->").split("->") if s.strip()]
    html = '<div class="step-trail">'
    for i, part in enumerate(parts):
        icon = STEP_ICONS[i] if i < len(STEP_ICONS) else "Step"
        cls = STEP_CLASSES[i] if i < len(STEP_CLASSES) else "step-1"
        html += f'<span class="step-pill {cls}">{icon}: {part}</span>'
        if i < len(parts) - 1:
            html += '<span class="step-arrow">></span>'
    html += '</div>'
    return html


def render_sources(sources):
    if not sources:
        return ""
    html = '<div class="sources-container"><div class="sources-label">Sources</div>'
    for src in sources:
        link = src.get("link", "")
        title = src.get("title", "Source")
        if link:
            html += f'<a href="{link}" target="_blank" class="source-chip">Open: {title}</a>'
        else:
            html += f'<span class="source-chip">{title}</span>'
    html += '</div>'
    return html


def render_assistant_message(msg, sources=None):
    steps_text = msg.get("steps", "")
    content = msg.get("content", "")
    trail_html = render_step_trail(steps_text) if steps_text else ""
    sources_html = render_sources(sources) if sources else ""
    st.markdown(trail_html, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ares-response">
        {content}
        {sources_html}
    </div>
    """, unsafe_allow_html=True)

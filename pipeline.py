import streamlit as st

from agents import (
    answer_agent,
    comparison_agent,
    confidence_score,
    report_generator,
    research_agent,
    search_agent,
    summarizer_agent,
)
from pdf_export import generate_pdf
from render import render_assistant_message


def run_pipeline(query, research_mode):
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.total_queries += 1

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        try:
            sources = []
            process_steps = []

            with st.status("Initialising pipeline...", expanded=True) as status:
                if st.session_state.pdf_text:
                    status.update(label="Document Mode - loading context", state="running")
                    st.write("Extracting context from uploaded document...")
                    context = st.session_state.pdf_text[:3000]
                    sources = [{"title": st.session_state.last_uploaded_file, "link": ""}]
                    process_steps.append("Document loaded")
                else:
                    status.update(label="Search Agent - scanning the web", state="running")
                    st.write("Search agent querying DuckDuckGo...")
                    web_results = search_agent(query)
                    context = " ".join([r["body"] for r in web_results])
                    sources = web_results
                    process_steps.append("Web data retrieved")

                status.update(label="Research Agent - processing context", state="running")
                st.write("Research agent extracting factual information...")
                data = research_agent(query, context)
                process_steps.append("AI processed data")

                status.update(label="Summarizer Agent - condensing", state="running")
                st.write("Summarizer agent distilling key points...")
                summary = summarizer_agent(data)
                process_steps.append("Summarization done")

                status.update(label="Answer Agent - structuring response", state="running")
                st.write("Answer agent formatting final output...")
                if "compare" in query.lower():
                    final = comparison_agent(query, context)
                elif research_mode == "Research Report":
                    final = report_generator(query, context)
                else:
                    final = answer_agent(summary)
                process_steps.append("Answer generated")

                status.update(label="Pipeline complete", state="complete", expanded=False)

            steps_text = " -> ".join(process_steps)
            msg_obj = {"role": "assistant", "content": final, "steps": steps_text}
            render_assistant_message(msg_obj, sources)

            confidence = confidence_score(
                len(sources),
                research_mode
            )

            st.markdown(f"""
            <div class="ares-confidence">
            Confidence Score: <b>{confidence}%</b><br>
            Sources Used: <b>{len(sources)}</b><br>
            Mode: <b>{research_mode}</b>
            </div>
            """, unsafe_allow_html=True)

            if research_mode == "Research Report":
                pdf_path = generate_pdf(final)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download Research Report",
                        f,
                        file_name="research_report.pdf",
                        mime="application/pdf"
                    )

            msg_index = len(st.session_state.messages)
            st.session_state.messages.append(msg_obj)
            st.session_state.sources[msg_index] = sources

        except Exception as e:
            st.error(f"Pipeline error: {str(e)}")
            st.info("Check that Ollama is running with `ollama serve`, then try again.")

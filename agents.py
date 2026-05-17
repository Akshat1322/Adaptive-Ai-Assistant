from urllib.parse import quote_plus

import ollama
import streamlit as st
from duckduckgo_search import DDGS


def search_agent(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append({
                    "title": r.get("title", "No title"),
                    "body": r.get("body", ""),
                    "link": r.get("href", "")
                })
        if not results:
            raise ValueError("empty")
        return results
    except Exception:
        eq = quote_plus(query)
        return [
            {"title": f"Google: {query}", "body": "", "link": f"https://www.google.com/search?q={eq}"},
            {"title": f"Wikipedia: {query}", "body": "", "link": f"https://en.wikipedia.org/wiki/Special:Search?search={eq}"},
            {"title": f"Bing: {query}", "body": "", "link": f"https://www.bing.com/search?q={eq}"},
        ]


def research_agent(query, context):
    st.session_state.agents_run += 1
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "You are a research agent. Extract and present factual information clearly and concisely based only on the provided context."
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    return response["message"]["content"]


def summarizer_agent(text):
    st.session_state.agents_run += 1
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "You are a summarizer agent. Extract the 5 most important points from any text. Be concise. Return bullet points only. No fluff."
            },
            {"role": "user", "content": f"Summarize this:\n{text}"}
        ]
    )
    return response["message"]["content"]


def answer_agent(summary):
    st.session_state.agents_run += 1
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "You are a presentation agent. Always format your response with exactly these three sections:\n\n**Definition:**\n(1-2 lines)\n\n**Key Points:**\n- point 1\n- point 2\n...\n\n**Conclusion:**\n(2-3 lines)"
            },
            {"role": "user", "content": summary}
        ]
    )
    return response["message"]["content"]


def confidence_score(sources_count, mode):
    base = 65

    if mode == "Detailed Analysis":
        base += 10
    elif mode == "Research Report":
        base += 20

    score = min(95, base + (sources_count * 5))
    return score


def comparison_agent(query, context):
    st.session_state.agents_run += 1

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": """
You are a comparison agent.

Generate:
1. Overview
2. Comparison Table
3. Advantages
4. Disadvantages
5. Use Cases
6. Final Verdict
"""
            },
            {"role": "user", "content": f"{context}\n\n{query}"}
        ]
    )

    return response["message"]["content"]


def report_generator(query, context):
    st.session_state.agents_run += 1

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": """
Generate a professional research report with:

1. Title
2. Introduction
3. Key Findings
4. Comparison Analysis
5. Conclusion
6. References

Format cleanly using markdown.
"""
            },
            {"role": "user", "content": f"{context}\n\nResearch Topic: {query}"}
        ]
    )

    return response["message"]["content"]

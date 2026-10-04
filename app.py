import streamlit as st
from analyzer import JDRealityCheckAgent

st.set_page_config(page_title="JD Reality-Check Agent", page_icon="🔎", layout="centered")

VERDICT_COLORS = {
    "Strong Match": "🟢",
    "Worth Applying": "🟢",
    "Stretch — Apply Anyway": "🟡",
    "Likely Mismatch": "🔴",
    "Unknown": "⚪",
}

st.title("🔎 JD Reality-Check Agent")
st.caption(
    "Paste a job description and get an honest, grounded read on whether it's "
    "realistic, well-structured, and worth your time — plus a genuine fit check "
    "against your resume if you add one. Built to ground every verdict in real "
    "hiring-pattern knowledge, not just an LLM's opinion."
)

with st.expander("How this works"):
    st.markdown(
        """
This isn't just an LLM giving its opinion on a JD. It's a small retrieval-augmented
system:

1. **Retrieval** — your pasted JD is matched (via TF-IDF similarity) against a
   curated knowledge base of well-established hiring-reality patterns
   (experience-requirement contradictions, buzzword density, compensation
   transparency signals, and more).
2. **Grounded reasoning** — only the patterns that are actually relevant to
   *your* JD are passed to the model, and it's instructed to ground its
   red-flag/positive-signal findings in those retrieved patterns rather than
   inventing generic hiring advice.
3. **Resume fit (optional)** — if you add your resume, the agent compares it
   honestly against the JD and won't soften real gaps.
        """
    )

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Gemini API Key", type="password", help="Get one free at aistudio.google.com")

jd_text = st.text_area("Paste the Job Description", height=250, placeholder="Paste the full JD here...")

with st.expander("Optional: add your resume for a personalized fit-check"):
    resume_text = st.text_area("Paste your resume text", height=200, placeholder="Paste your resume as plain text...")

analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

if analyze_clicked:
    if not api_key:
        st.error("Please enter a Gemini API key to run the analysis.")
    elif not jd_text.strip():
        st.error("Please paste a job description first.")
    else:
        with st.spinner("Retrieving relevant hiring patterns and analyzing..."):
            try:
                agent = JDRealityCheckAgent(api_key=api_key)
                result = agent.analyze(jd_text, resume_text if resume_text.strip() else None)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                result = None

        if result:
            verdict = result.get("overall_verdict", "Unknown")
            icon = VERDICT_COLORS.get(verdict, "⚪")

            st.markdown(f"## {icon} {verdict}")
            st.write(result.get("verdict_reasoning", ""))

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🚩 Red Flags")
                red_flags = result.get("red_flags", [])
                if red_flags:
                    for flag in red_flags:
                        st.markdown(f"- {flag.get('finding', '')}")
                else:
                    st.markdown("*None flagged.*")

            with col2:
                st.markdown("### ✅ Positive Signals")
                positives = result.get("positive_signals", [])
                if positives:
                    for signal in positives:
                        st.markdown(f"- {signal.get('finding', '')}")
                else:
                    st.markdown("*None flagged.*")

            resume_fit = result.get("resume_fit", {})
            if resume_fit.get("provided"):
                st.markdown("### 🎯 Resume Fit")
                st.write(resume_fit.get("fit_summary", ""))

                fcol1, fcol2 = st.columns(2)
                with fcol1:
                    st.markdown("**Genuine Matches**")
                    for m in resume_fit.get("genuine_matches", []):
                        st.markdown(f"- {m}")
                with fcol2:
                    st.markdown("**Real Gaps**")
                    for g in resume_fit.get("real_gaps", []):
                        st.markdown(f"- {g}")

            st.markdown("### 💡 Advice")
            st.info(result.get("advice", ""))

            with st.expander("Show retrieved grounding patterns"):
                for entry in result.get("_retrieved_patterns", []):
                    st.markdown(f"**[{entry['category']}]** (relevance: {entry['similarity']})")
                    st.caption(entry["text"])
                    st.divider()

st.markdown("---")
st.caption("Built by Tasim Faisal · [GitHub](https://github.com/Tasimmm) · [LinkedIn](https://www.linkedin.com/in/tasim-faisal)")

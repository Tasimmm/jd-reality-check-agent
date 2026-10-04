import streamlit as st
from analyzer import JDRealityCheckAgent
from resume_parser import extract_resume_text

st.set_page_config(page_title="JD Reality Check", page_icon="🗂️", layout="centered")

# ---------------------------------------------------------------------------
# Custom styling — a dossier / inspection-report look, grounded in what this
# tool actually does: stamping a verdict on a job posting after inspection.
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #1A2238;
}

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
}

h1, h2, h3 {
    font-family: 'Zilla Slab', serif;
    color: #1A2238;
    letter-spacing: -0.01em;
}

.dossier-header {
    border-bottom: 2px solid #1A2238;
    padding-bottom: 0.75rem;
    margin-bottom: 0.25rem;
}

.dossier-title {
    font-family: 'Zilla Slab', serif;
    font-weight: 700;
    font-size: 2.1rem;
    margin: 0;
    line-height: 1.15;
}

.dossier-sub {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    color: #4A4536;
    margin-top: 0.4rem;
}

.file-ref {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.78rem;
    color: #6B6650;
    margin-top: 0.3rem;
}

/* Verdict stamp */
.stamp-wrap {
    display: flex;
    justify-content: flex-start;
    margin: 1.75rem 0 1.25rem 0;
}

.stamp {
    font-family: 'Zilla Slab', serif;
    font-weight: 700;
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border: 3px solid currentColor;
    padding: 0.5rem 1.4rem;
    border-radius: 2px;
    transform: rotate(-2deg);
    display: inline-block;
}

.stamp-green { color: #2F5D50; }
.stamp-amber { color: #8A6D1D; }
.stamp-red   { color: #A23B3B; }
.stamp-grey  { color: #6B6650; }

.section-label {
    font-family: 'Zilla Slab', serif;
    font-weight: 600;
    font-size: 1.05rem;
    border-bottom: 1px solid #B8A978;
    padding-bottom: 0.3rem;
    margin-top: 1.6rem;
    margin-bottom: 0.6rem;
}

.finding-row {
    display: flex;
    gap: 0.6rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #DED0AF;
    font-size: 0.95rem;
    line-height: 1.5;
}

.finding-row:last-child { border-bottom: none; }

.finding-marker {
    font-weight: 700;
    flex-shrink: 0;
    width: 1.1rem;
}

.marker-flag { color: #A23B3B; }
.marker-good { color: #2F5D50; }

.empty-note {
    font-style: italic;
    color: #6B6650;
    font-size: 0.9rem;
    padding: 0.4rem 0;
}

.advice-box {
    background: #DED0AF;
    border-left: 4px solid #1A2238;
    padding: 0.9rem 1.1rem;
    font-size: 0.96rem;
    margin-top: 0.4rem;
    line-height: 1.55;
}

/* Buttons */
.stButton button {
    font-family: 'Zilla Slab', serif;
    font-weight: 600;
    background-color: #1A2238;
    color: #E8DCC4;
    border-radius: 2px;
    border: none;
    padding: 0.6rem 1.2rem;
    letter-spacing: 0.02em;
}

.stButton button:hover {
    background-color: #2A3350;
    color: #E8DCC4;
}

footer, #MainMenu { visibility: hidden; }

.app-footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #B8A978;
    font-size: 0.85rem;
    color: #6B6650;
}

.app-footer a { color: #1A2238; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

VERDICT_STYLE = {
    "Strong Match": "stamp-green",
    "Worth Applying": "stamp-green",
    "Stretch — Apply Anyway": "stamp-amber",
    "Likely Mismatch": "stamp-red",
    "Unknown": "stamp-grey",
}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="dossier-header">
        <p class="dossier-title">JD Reality Check</p>
        <p class="dossier-sub">An honest inspection of a job posting, grounded in real hiring-pattern evidence — not just an opinion.</p>
        <p class="file-ref">FILE TYPE: Job Posting Inspection &nbsp;·&nbsp; METHOD: Retrieval-grounded analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("How this inspection works"):
    st.markdown(
        """
This isn't an LLM giving its raw opinion on a JD. It's a small retrieval-augmented
system, built the same way as a real investigation:

1. **Retrieval** — your pasted JD is matched, via TF-IDF similarity, against a
   curated case file of well-established hiring-reality patterns (experience
   contradictions, buzzword density, compensation transparency, and more).
2. **Grounded reasoning** — only the patterns genuinely relevant to *your* JD
   are passed into the analysis, and the model is instructed to cite them
   rather than invent generic advice.
3. **Resume fit (optional)** — add your resume and the agent compares it
   honestly, without softening real gaps.
        """
    )

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Gemini API Key", type="password", help="Get one free at aistudio.google.com")

jd_text = st.text_area("Paste the job description under inspection", height=220, placeholder="Paste the full JD here...")

resume_text = ""
with st.expander("Optional: add your resume for a personalized fit-check"):
    input_mode = st.radio(
        "How would you like to add your resume?",
        ["Upload a file", "Paste text"],
        horizontal=True,
    )

    if input_mode == "Upload a file":
        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=["pdf", "docx", "txt"],
        )
        if uploaded_resume is not None:
            try:
                resume_text = extract_resume_text(uploaded_resume)
                st.success(f"Loaded {uploaded_resume.name} ({len(resume_text)} characters extracted)")
                with st.expander("Preview extracted text"):
                    st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
            except ValueError as e:
                st.error(str(e))
    else:
        resume_text = st.text_area(
            "Paste your resume text", height=200, placeholder="Paste your resume as plain text..."
        )

analyze_clicked = st.button("Run inspection", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
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
            stamp_class = VERDICT_STYLE.get(verdict, "stamp-grey")

            st.markdown(
                f'<div class="stamp-wrap"><div class="stamp {stamp_class}">{verdict}</div></div>',
                unsafe_allow_html=True,
            )
            st.write(result.get("verdict_reasoning", ""))

            # Red flags
            st.markdown('<div class="section-label">Red flags</div>', unsafe_allow_html=True)
            red_flags = result.get("red_flags", [])
            if red_flags:
                rows = "".join(
                    f'<div class="finding-row"><span class="finding-marker marker-flag">⚑</span><span>{f.get("finding", "")}</span></div>'
                    for f in red_flags
                )
                st.markdown(rows, unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-note">None flagged.</div>', unsafe_allow_html=True)

            # Positive signals
            st.markdown('<div class="section-label">Positive signals</div>', unsafe_allow_html=True)
            positives = result.get("positive_signals", [])
            if positives:
                rows = "".join(
                    f'<div class="finding-row"><span class="finding-marker marker-good">✓</span><span>{p.get("finding", "")}</span></div>'
                    for p in positives
                )
                st.markdown(rows, unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-note">None flagged.</div>', unsafe_allow_html=True)

            # Resume fit
            resume_fit = result.get("resume_fit", {})
            if resume_fit.get("provided"):
                st.markdown('<div class="section-label">Resume fit</div>', unsafe_allow_html=True)
                st.write(resume_fit.get("fit_summary", ""))

                fcol1, fcol2 = st.columns(2)
                with fcol1:
                    st.markdown("**Genuine matches**")
                    matches = resume_fit.get("genuine_matches", [])
                    if matches:
                        for m in matches:
                            st.markdown(f"- {m}")
                    else:
                        st.markdown('<div class="empty-note">None noted.</div>', unsafe_allow_html=True)
                with fcol2:
                    st.markdown("**Real gaps**")
                    gaps = resume_fit.get("real_gaps", [])
                    if gaps:
                        for g in gaps:
                            st.markdown(f"- {g}")
                    else:
                        st.markdown('<div class="empty-note">None noted.</div>', unsafe_allow_html=True)

            # Advice
            st.markdown('<div class="section-label">Advice</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="advice-box">{result.get("advice", "")}</div>', unsafe_allow_html=True)

            with st.expander("Case file — retrieved grounding patterns"):
                for entry in result.get("_retrieved_patterns", []):
                    st.markdown(f"**{entry['category']}** (relevance: {entry['similarity']})")
                    st.caption(entry["text"])
                    st.divider()

st.markdown(
    """
    <div class="app-footer">
        Built by Tasim Faisal &nbsp;·&nbsp;
        <a href="https://github.com/Tasimmm" target="_blank">GitHub</a> &nbsp;·&nbsp;
        <a href="https://www.linkedin.com/in/tasim-faisal" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# JD Reality-Check Agent

A retrieval-augmented agent that gives an honest, grounded read on a job
description — is it realistic, well-structured, and worth applying to? —
plus a genuine, ungentle fit-check against your resume if you provide one.

Built after manually doing this exact analysis dozens of times during my own
job search: catching internal contradictions (an "entry-level" role wanting
years of experience), buzzword-heavy postings with no real technical detail,
and stipend-only "internships" with no real pay. Instead of doing it by hand
every time, I built an agent to do it — grounded in a curated knowledge base
of real hiring-reality patterns, not just an LLM's raw opinion.

## How it works

1. **Retrieval** — the pasted JD is matched via TF-IDF similarity against a
   curated knowledge base of hiring-reality patterns (experience-requirement
   contradictions, buzzword density, compensation transparency, skill
   stacking, scope creep signals, and more).
2. **Grounded reasoning** — only genuinely relevant patterns are passed to
   Gemini, which is instructed to ground its red-flag/positive-signal
   findings in that retrieved context rather than inventing generic advice.
3. **Resume fit (optional)** — if a resume is provided, the agent compares
   it honestly against the JD, including real gaps, without softening them.

## Stack

Python · Streamlit · Gemini API · Scikit-learn (TF-IDF retrieval)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

You'll need a free Gemini API key from [aistudio.google.com](https://aistudio.google.com).

## Deploy

Deployed on Streamlit Community Cloud. Set `GEMINI_API_KEY` in
`.streamlit/secrets.toml` (or the Streamlit Cloud secrets manager) so users
don't need to bring their own key.

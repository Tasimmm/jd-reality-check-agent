"""
Core analysis logic: retrieves grounding context from the knowledge base,
then asks Gemini to reason over the JD (and optional resume) *using only
that grounded context* for its hiring-reality judgments, while using its
own general reasoning for the resume-fit comparison (which is inherently
about the specific person, not a general hiring pattern).
"""

import json
import re
import google.generativeai as genai

from retrieval import KnowledgeRetriever

SYSTEM_INSTRUCTIONS = """You are a JD Reality-Check agent. You help students and \
early-career job seekers understand whether a job description is realistic, \
well-structured, and worth their time to apply to -- and if a resume is \
provided, how genuinely their background matches it.

You are given a set of GROUNDED HIRING-REALITY PATTERNS retrieved from a \
curated knowledge base. These are the ONLY source you may cite for general \
claims about hiring norms, red flags, or what's "typical." Do not invent \
statistics or norms that are not in the provided patterns. If none of the \
patterns are relevant to something you notice, you may still mention it as \
your own observation, but label it clearly as an observation rather than a \
grounded norm.

If a resume is provided, compare it against the JD directly and honestly. \
Do not soften real gaps. Do not claim a skill is present if it is not \
explicitly stated in the resume text provided.

Respond ONLY with valid JSON, no markdown fences, matching exactly this shape:
{
  "overall_verdict": "Strong Match" | "Worth Applying" | "Stretch \u2014 Apply Anyway" | "Likely Mismatch",
  "verdict_reasoning": "2-3 sentence honest summary",
  "red_flags": [
    {"pattern_id": "kb_id or null if it's your own observation", "finding": "specific finding tied to THIS JD's actual text, not a generic restatement of the pattern"}
  ],
  "positive_signals": [
    {"pattern_id": "kb_id or null", "finding": "specific finding tied to THIS JD's actual text"}
  ],
  "resume_fit": {
    "provided": true or false,
    "genuine_matches": ["specific skill/experience that genuinely matches, only if resume provided"],
    "real_gaps": ["specific, honest gaps -- do not soften these"],
    "fit_summary": "1-2 sentence honest verdict on fit, or null if no resume provided"
  },
  "advice": "1-2 sentences of concrete, honest advice for this specific person on this specific JD"
}
"""


class JDRealityCheckAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_INSTRUCTIONS,
        )
        self.retriever = KnowledgeRetriever()

    def analyze(self, jd_text: str, resume_text: str | None = None) -> dict:
        retrieved = self.retriever.retrieve(jd_text, top_k=6)

        grounding_block = "\n\n".join(
            f"[{entry['id']}] ({entry['category']}, relevance={entry['similarity']})\n{entry['text']}"
            for entry in retrieved
        ) or "No strongly relevant patterns were retrieved for this JD."

        resume_block = (
            f"\n\nCANDIDATE RESUME:\n{resume_text}"
            if resume_text and resume_text.strip()
            else "\n\nNo resume was provided. Set resume_fit.provided to false and leave genuine_matches/real_gaps empty."
        )

        prompt = (
            f"GROUNDED HIRING-REALITY PATTERNS RETRIEVED FOR THIS JD:\n{grounding_block}\n\n"
            f"JOB DESCRIPTION TO ANALYZE:\n{jd_text}"
            f"{resume_block}\n\n"
            "Produce your analysis now, following the JSON schema exactly."
        )

        response = self.model.generate_content(prompt)
        raw_text = response.text.strip()

        # Defensive cleanup in case the model wraps output in a code fence anyway
        raw_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip())

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = {
                "overall_verdict": "Unknown",
                "verdict_reasoning": "The agent's response could not be parsed. Raw output is shown below.",
                "red_flags": [],
                "positive_signals": [],
                "resume_fit": {"provided": bool(resume_text), "genuine_matches": [], "real_gaps": [], "fit_summary": None},
                "advice": raw_text,
            }

        parsed["_retrieved_patterns"] = retrieved
        return parsed

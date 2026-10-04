"""
Curated knowledge base of hiring-reality patterns.
Each entry is a real, well-established hiring-norm signal that the retrieval
layer matches against a pasted JD. This is what makes the agent's verdict
*grounded* rather than the LLM just freestyling an opinion.
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb_experience_mismatch",
        "category": "Experience Mismatch",
        "text": (
            "A posting labeled 'entry-level', 'fresher', 'junior', or 'intern' that also "
            "requires 1+ years, 2+ years, or 'proven professional experience' is internally "
            "contradictory. Genuine entry-level roles train from near-zero experience; "
            "requiring prior paid experience for an 'entry-level' title is a red flag that "
            "the posting may be miscategorized, or that competition for the role will be "
            "unusually high because experienced candidates will also apply."
        ),
    },
    {
        "id": "kb_skill_stacking",
        "category": "Skill Stacking",
        "text": (
            "A single role that requires deep expertise across multiple unrelated technical "
            "domains (e.g., frontend + backend + DevOps + data science + design) at a senior "
            "level usually signals either a very small/early-stage company that cannot yet "
            "afford specialists, or an unrealistic wishlist written without full understanding "
            "of how specialized modern engineering roles actually are. This isn't necessarily "
            "disqualifying, but it changes what the job will actually feel like day to day."
        ),
    },
    {
        "id": "kb_vague_growth",
        "category": "Vague Growth Promises",
        "text": (
            "Phrases like 'fast-paced environment', 'wear many hats', 'unlimited growth "
            "potential', or 'work hard play hard' without concrete detail on compensation, "
            "mentorship structure, or career progression are common in postings that may "
            "substitute enthusiasm language for real structure. Not automatically bad, but "
            "worth probing in an interview rather than taking at face value."
        ),
    },
    {
        "id": "kb_salary_absence",
        "category": "Compensation Transparency",
        "text": (
            "Postings with no salary range, or a range so wide it spans multiple seniority "
            "levels (e.g., 3x difference between min and max), often indicate either a lack "
            "of internal clarity on the role's actual level, or an intent to lowball "
            "candidates during negotiation. A tight, clearly stated range is a positive signal "
            "of an organized hiring process."
        ),
    },
    {
        "id": "kb_buzzword_density",
        "category": "Buzzword Density",
        "text": (
            "A high density of trend-chasing buzzwords (AI-powered, blockchain-enabled, "
            "Web3-native, disruptive, ninja, rockstar, guru) without concrete technical "
            "specifics (which frameworks, which stack, which actual problem is being solved) "
            "can indicate a posting written for marketing appeal rather than accurate role "
            "description. It doesn't mean the company is illegitimate, but it means the JD "
            "itself is a weaker source of truth about the actual day-to-day work."
        ),
    },
    {
        "id": "kb_unpaid_or_stipend_only",
        "category": "Compensation Fairness",
        "text": (
            "Internships or entry roles offering a stipend significantly below regional "
            "market norms for a technical role, or offering 'exposure' or 'certificate only' "
            "in place of pay, are common in low-quality internship mills. A performance-based "
            "PPO (pre-placement offer) promise with no defined criteria for what qualifies is "
            "a soft commitment, not a guarantee, and should be evaluated as such."
        ),
    },
    {
        "id": "kb_scope_creep_signal",
        "category": "Scope Creep Risk",
        "text": (
            "Responsibilities lists that mix clearly different job functions (e.g., an "
            "engineering role that also owns sales outreach, or a data role that also owns "
            "full customer support) often signal understaffing, where one hire is expected to "
            "cover gaps across multiple roles. This can be a genuine growth opportunity at an "
            "early-stage company, or a sign of being stretched thin, depending on company size "
            "and stage."
        ),
    },
    {
        "id": "kb_legit_structured_process",
        "category": "Legitimate Process Signals",
        "text": (
            "Positive signals of a well-run, legitimate hiring process include: a clear, "
            "specific compensation range; a defined, bounded technical assessment (e.g., a "
            "timed build sprint or a scoped take-home) rather than open-ended unpaid work; "
            "named responsibilities that map to one coherent function; and application "
            "instructions that are specific rather than generic mass-posting boilerplate."
        ),
    },
    {
        "id": "kb_tool_specificity",
        "category": "Technical Specificity",
        "text": (
            "JDs that name specific tools, frameworks, and versions (e.g., 'React 18', "
            "'PostgreSQL', 'a proprietary internal framework') rather than only generic terms "
            "('modern web technologies') tend to reflect an actual existing team and codebase, "
            "which is a positive signal that the role is real and staffed, not speculative."
        ),
    },
    {
        "id": "kb_excessive_requirements_count",
        "category": "Requirements Overload",
        "text": (
            "A very long list of 'required' (not preferred) skills — typically more than "
            "8-10 hard requirements for a single role — statistically reduces the number of "
            "qualified applicants who will apply at all, and research on hiring behavior "
            "shows most successful candidates do not meet every listed requirement. A long "
            "requirements list is a weak signal of what's truly necessary versus what was "
            "copy-pasted from a template."
        ),
    },
    {
        "id": "kb_remote_ambiguity",
        "category": "Remote Work Clarity",
        "text": (
            "Postings that say 'remote' but list a single specific city with no clarification "
            "on whether relocation, timezone overlap, or occasional office presence is "
            "expected often turn out to be hybrid roles miscategorized as remote. Genuine "
            "remote roles usually specify timezone flexibility explicitly."
        ),
    },
    {
        "id": "kb_generic_boilerplate",
        "category": "Posting Authenticity",
        "text": (
            "JDs that are near-identical in structure and phrasing to thousands of other "
            "postings (generic 'about us' paragraph, generic responsibilities, no company-"
            "specific detail) may be posted by staffing agencies or aggregators rather than "
            "the hiring company directly, meaning the true employer and reporting structure "
            "may be unclear until later in the process."
        ),
    },
]

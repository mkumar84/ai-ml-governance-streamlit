"""
AI & ML Governance Command Centre — Streamlit recreation
Multi-dimensional governance posture across registered AI/ML systems.
Scores synthesized across six assessment modules aligned to OSFI, PIPEDA,
Law 25, and Treasury Board guidance.

Run with: streamlit run ai_ml_gov_app.py
"""

import uuid
import zlib
from datetime import date, timedelta
import streamlit as st

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="AI & ML Governance Command Centre",
    page_icon="\u25C6",
    layout="wide",
)

# ----------------------------------------------------------------------
# Theme — warm minimalist palette with navy / forest-green / amber accents
# ----------------------------------------------------------------------
CREAM = "#F5F2EB"
INK = "#1F2A37"
NAVY = "#1E3A5F"
FOREST = "#2A7A55"
AMBER = "#C8860D"
RED = "#B3261E"

st.markdown(f"""
<style>
    .stApp {{
        background: {CREAM};
    }}
    h1, h2, h3 {{
        color: {INK};
        font-weight: 700;
        letter-spacing: -0.01em;
    }}

    /* Hero banner */
    .gov-hero {{
        background: linear-gradient(135deg, {NAVY} 0%, #284f7a 100%);
        color: #F5F2EB;
        padding: 1.6rem 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.4rem;
    }}
    .gov-hero h1 {{
        color: #FFFFFF;
        margin: 0 0 0.35rem 0;
        font-size: 1.9rem;
    }}
    .gov-hero p {{
        color: #D7E0EC;
        margin: 0;
        font-size: 0.97rem;
        max-width: 760px;
    }}

    /* Metric tiles */
    .metric-tile {{
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-left: 5px solid var(--accent, {NAVY});
        border-radius: 12px;
        padding: 1rem 1.2rem;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .metric-tile:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(31,42,55,0.08);
    }}
    .metric-tile .num {{
        font-size: 2rem;
        font-weight: 800;
        color: {INK};
        line-height: 1.1;
    }}
    .metric-tile .label {{
        font-weight: 600;
        color: {INK};
        font-size: 0.92rem;
        margin-top: 2px;
    }}
    .metric-tile .sub {{
        color: #8A8475;
        font-size: 0.8rem;
        margin-top: 2px;
    }}

    /* Product cards */
    .product-card {{
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }}
    .product-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 26px rgba(31,42,55,0.14);
        border-color: {FOREST};
        cursor: pointer;
    }}
    .product-name {{
        font-weight: 700;
        font-size: 1.02rem;
        color: {INK};
    }}
    .product-meta {{
        color: #8A8475;
        font-size: 0.84rem;
        margin-top: 1px;
    }}
    .score-num {{
        font-size: 1.3rem;
        font-weight: 800;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid {FOREST}55;
        transition: all 0.15s ease;
    }}
    .stButton > button:hover {{
        border-color: {FOREST};
        color: {FOREST};
        background: {FOREST}11;
    }}
    .stButton > button[kind="primary"] {{
        background: {FOREST};
        border-color: {FOREST};
    }}
    .stButton > button[kind="primary"]:hover {{
        background: #236244;
        border-color: #236244;
    }}

    /* Expanders as module cards */
    .streamlit-expanderHeader, [data-testid="stExpander"] summary {{
        background: #FFFFFF;
        border-radius: 10px;
        font-weight: 600;
        color: {INK};
    }}
    [data-testid="stExpander"] {{
        border: 1px solid #E5E0D5;
        border-radius: 12px;
        background: #FFFFFF;
        margin-bottom: 0.6rem;
    }}

    /* Knowledge base reference cards */
    .ref-card {{
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-left: 5px solid {NAVY};
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.7rem;
        transition: box-shadow 0.15s ease;
    }}
    .ref-card:hover {{
        box-shadow: 0 6px 18px rgba(31,42,55,0.08);
    }}
    .ref-card .ref-title {{
        font-weight: 700;
        color: {INK};
        margin-bottom: 0.2rem;
    }}

    /* Module step pills on Assess page */
    .mod-pill {{
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-radius: 12px;
        padding: 0.6rem 0.5rem;
        text-align: center;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .mod-pill.active {{
        border-color: {FOREST};
        box-shadow: 0 0 0 2px {FOREST}22;
    }}
    .mod-pill .mod-num {{
        display: inline-block;
        width: 26px;
        height: 26px;
        line-height: 26px;
        border-radius: 50%;
        background: {NAVY};
        color: #fff;
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 4px;
    }}
    .mod-pill .mod-title {{
        font-weight: 600;
        font-size: 0.82rem;
        color: {INK};
    }}
    .mod-pill .mod-sub {{
        font-size: 0.74rem;
        color: #8A8475;
    }}

    /* Form inputs — crisp white fields against cream background */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stDateInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid #D8D2C4 !important;
        border-radius: 8px !important;
        color: {INK} !important;
    }}
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stDateInput"] input:focus,
    [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"]:focus-within > div {{
        border-color: {FOREST} !important;
        box-shadow: 0 0 0 1px {FOREST} !important;
    }}
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {{
        color: {INK} !important;
        font-weight: 600;
    }}
    [data-baseweb="popover"] li {{
        background-color: #FFFFFF;
        color: {INK};
    }}
    [data-baseweb="tag"] {{
        background-color: {FOREST}22 !important;
        color: {FOREST} !important;
    }}

    /* Top navigation bar */
    .top-nav {{
        background: {NAVY};
        border-radius: 14px;
        padding: 0.7rem 1.2rem;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.6rem;
    }}
    .top-nav .brand {{
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.05rem;
        white-space: nowrap;
    }}

    /* Demo data notice */
    .demo-notice {{
        background: {AMBER}14;
        border: 1px solid {AMBER}55;
        color: #6B4E0A;
        border-radius: 10px;
        padding: 0.55rem 1rem;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }}

    /* Roadmap board */
    .roadmap-col {{
        background: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-radius: 14px;
        padding: 0.9rem;
        height: 100%;
    }}
    .roadmap-col h4 {{
        margin: 0 0 0.6rem 0;
        color: {INK};
    }}
    .roadmap-card {{
        background: {CREAM};
        border: 1px solid #E5E0D5;
        border-left: 4px solid {NAVY};
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.6rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .roadmap-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(31,42,55,0.10);
    }}
    .roadmap-card .rt {{
        font-weight: 700;
        color: {INK};
        font-size: 0.9rem;
        margin-bottom: 4px;
    }}
    .roadmap-card .rd {{
        color: #6B6557;
        font-size: 0.8rem;
    }}

    /* Module score bars */
    .mscore-row {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.45rem;
    }}
    .mscore-label {{
        width: 170px;
        font-size: 0.84rem;
        font-weight: 600;
        color: {INK};
        flex-shrink: 0;
    }}
    .mscore-track {{
        flex-grow: 1;
        background: #E9E4D8;
        border-radius: 999px;
        height: 10px;
        overflow: hidden;
    }}
    .mscore-fill {{
        height: 100%;
        border-radius: 999px;
    }}
    .mscore-val {{
        width: 48px;
        text-align: right;
        font-weight: 700;
        font-size: 0.84rem;
        flex-shrink: 0;
    }}

    @media (max-width: 768px) {{
        .gov-hero {{ padding: 1.1rem 1.2rem; }}
        .gov-hero h1 {{ font-size: 1.4rem; }}
        .metric-tile .num {{ font-size: 1.5rem; }}
        .top-nav .brand {{ font-size: 0.95rem; }}
        .mscore-label {{ width: 110px; font-size: 0.74rem; }}
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Static reference data: assessment modules / questions / options
# Each option is (label, score 0-100)
# ----------------------------------------------------------------------
GENERIC_OPTS = [
    ("Yes — fully implemented", 100),
    ("Partially implemented", 55),
    ("No", 0),
    ("Planned within 12 months", 35),
]

MODULES = [
    {
        "title": "Algorithmic Impact",
        "ref": "Treasury Board Directive on ADM; CLHIA AI Principles",
        "desc": "Assesses fairness, explainability, human oversight, and bias risk for AI-driven decisions affecting individuals.",
        "questions": [
            {
                "q": "Does this system make or influence decisions that could adversely affect an individual's insurance coverage, claim outcome, or financial standing?",
                "opts": [
                    ("Yes — fully automated decision", 10),
                    ("Yes — human-in-the-loop", 40),
                    ("No", 100),
                    ("Unsure", 50),
                ],
                "severity": "Critical",
                "citation": "Treasury Board Directive on ADM \u2014 Appendix C (Impact Level IV)",
                "owner_role": "Model Risk Team",
            },
            {
                "q": "Has a bias assessment been conducted on the training data and model outputs against protected characteristics (race, sex, age, disability)?",
                "opts": [
                    ("Yes — fully documented and repeatable", 100),
                    ("In progress", 50),
                    ("No", 0),
                    ("Not applicable", 70),
                ],
                "severity": "Critical",
                "citation": "CLHIA AI Principles, Principle 2 (Fairness); Canadian Human Rights Act s.3",
                "owner_role": "Model Risk Team",
            },
            {
                "q": "Can this system's decision be explained in plain language to the affected individual?",
                "opts": [
                    ("Yes — always, with documented explanation template", 100),
                    ("Yes — in most cases", 75),
                    ("Partially", 40),
                    ("No", 0),
                ],
                "severity": "High",
                "citation": "CLHIA AI Principles, Principle 4 (Explainability); Quebec Law 25, s.12.1",
                "owner_role": "Model Risk Team",
            },
            {
                "q": "Is there a documented and tested human override mechanism for automated decisions?",
                "opts": [
                    ("Yes — documented and tested", 100),
                    ("Yes — exists but not documented", 60),
                    ("No", 0),
                    ("Not applicable — no automated decisions", 80),
                ],
                "severity": "Critical",
                "citation": "OSFI E-23, Principle 4 (Human Override and Escalation)",
                "owner_role": "Model Risk Team",
            },
            {
                "q": "Has a formal Algorithmic Impact Assessment (AIA) been completed using a recognized framework?",
                "opts": [
                    ("Yes — Treasury Board AIA framework", 100),
                    ("Yes — internal AIA framework", 80),
                    ("No", 0),
                    ("Planned within 90 days", 50),
                ],
                "severity": "High",
                "citation": "Treasury Board Directive on ADM, s.6.1 (Mandatory AIA)",
                "owner_role": "AI Governance Office",
            },
            {
                "q": "Is there an appeal or recourse mechanism for individuals adversely affected by an AI-driven decision?",
                "opts": [
                    ("Yes — formal appeal process documented", 100),
                    ("Informal process exists", 50),
                    ("No", 0),
                    ("Not applicable", 70),
                ],
                "severity": "Medium",
                "citation": "Treasury Board Directive on ADM \u2014 Appendix C (Recourse / Level IV)",
                "owner_role": "AI Governance Office",
            },
        ],
    },
    {
        "title": "Model Risk",
        "ref": "OSFI Guideline E-23 — Model Risk Management",
        "desc": "Evaluates model validation, monitoring, documentation, and lifecycle controls.",
        "questions": [
            {"q": "Is the model independently validated prior to deployment?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23, Principle 4 (Independent Model Validation)",
             "owner_role": "Model Risk Team"},
            {"q": "Is model performance monitored on an ongoing basis against defined thresholds?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23, Principle 5 (Ongoing Monitoring)",
             "owner_role": "ML Operations"},
            {"q": "Is this model registered in the enterprise model inventory?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 2 (Enterprise Model Inventory)",
             "owner_role": "Model Risk Team"},
            {"q": "Has the model been assigned an OSFI E-23 risk tier?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 1 (Model Risk Tiering)",
             "owner_role": "Model Risk Team"},
            {"q": "Are model assumptions, limitations, and known failure modes documented and communicated to business users?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI E-23, Principle 3 (Model Documentation)",
             "owner_role": "Model Risk Team"},
            {"q": "Is there a defined model revalidation schedule (annual or triggered by material change)?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI E-23, Principle 5 (Periodic Revalidation Schedule)",
             "owner_role": "Model Risk Team"},
            {"q": "For GenAI / LLM systems: has hallucination risk, output consistency, and prompt injection vulnerability been formally evaluated?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23 (Sep 2025 update) \u2014 GenAI / LLM Governance",
             "owner_role": "Model Risk Team"},
        ],
    },
    {
        "title": "Privacy Risk",
        "ref": "PIPEDA; Quebec Law 25",
        "desc": "Evaluates personal data handling, consent, retention, and individual rights.",
        "questions": [
            {"q": "Has a Privacy Impact Assessment (PIA) been completed for this AI/ML system?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Quebec Law 25, s.63.1 (Mandatory PIA); PIPEDA Best Practices",
             "owner_role": "Privacy Office"},
            {"q": "What is the legal basis for using personal information in this system?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "PIPEDA, Schedule I, Principle 4.3 (Consent)",
             "owner_role": "Privacy Office"},
            {"q": "Is personal information used in model training minimized to what is strictly necessary for the stated purpose?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "PIPEDA, Schedule I, Principle 4.5 (Data Minimization)",
             "owner_role": "Privacy Office"},
            {"q": "Are data retention and deletion schedules defined and enforced for personal data used in this AI system?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "PIPEDA, Schedule I, Principle 4.5 (Retention & Disposal)",
             "owner_role": "Privacy Office"},
            {"q": "Does this system process personal information of Quebec residents?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Quebec Law 25, ss.12.1 and 63.1",
             "owner_role": "Privacy Office"},
            {"q": "Is personal data shared with third-party AI vendors or cloud providers?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "PIPEDA, Schedule I, Principle 4.1.3; OSFI B-10 (Third-Party Risk)",
             "owner_role": "Privacy Office"},
        ],
    },
    {
        "title": "Data Risk",
        "ref": "OSFI Guideline E-23; OSFI-FCAC Joint Report",
        "desc": "Evaluates data quality, lineage, access controls, and representativeness.",
        "questions": [
            {"q": "Has data quality been formally assessed and validated before model training or deployment?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 3 (Model Development \u2014 Data Quality)",
             "owner_role": "Data Office"},
            {"q": "Is data lineage documented for all data sources feeding this AI system?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI-FCAC Joint Report (Sep 2024) \u2014 Data Governance Risks in AI",
             "owner_role": "Data Office"},
            {"q": "Are role-based access controls enforced to restrict who can access training data and model outputs?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-13, Domain 4 (Access Controls); PIPEDA Principle 4.7",
             "owner_role": "Cyber Security Team"},
            {"q": "Has the training dataset been tested for representativeness across the population the model will serve?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23, Principle 3 (Representativeness); CLHIA Fairness Principles",
             "owner_role": "Model Risk Team"},
            {"q": "Is there a process to detect and remediate data drift in production inputs?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 5 (Ongoing Monitoring \u2014 Data Drift)",
             "owner_role": "ML Operations"},
            {"q": "Are third-party or external data sources used, and if so, are they governed by formal data agreements?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-10 (Third-Party Risk Management \u2014 Data Agreements)",
             "owner_role": "Procurement / Data Office"},
        ],
    },
    {
        "title": "Cybersecurity Risk",
        "ref": "OSFI Guideline B-13",
        "desc": "Evaluates security controls, vendor assessments, and incident readiness.",
        "questions": [
            {"q": "Has a cybersecurity risk assessment been conducted specifically for this AI/ML system?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI B-13, Domain 1 (Governance and Risk Management)",
             "owner_role": "Cyber Security Team"},
            {"q": "Is sensitive data encrypted at rest and in transit throughout the AI system?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI B-13, Domain 3 (Data Security and Encryption at Rest / Transit)",
             "owner_role": "Cyber Security Team"},
            {"q": "Is the AI model protected against adversarial inputs or model poisoning attacks?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI B-13, Domain 5 (Cyber Operations \u2014 AI Attack Surface)",
             "owner_role": "Cyber Security Team"},
            {"q": "Are access controls (MFA + RBAC) enforced for model endpoints, training pipelines, and inference APIs?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-13, Domain 4 (Identity and Access Management)",
             "owner_role": "Cyber Security Team"},
            {"q": "Is there an AI-specific incident response plan covering model compromise, data breach via AI output, or prompt injection?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-13, Domain 6 (Incident Response); OSFI E-23 (Sep 2025 GenAI update)",
             "owner_role": "Cyber Security Team"},
            {"q": "For third-party AI tools: have contractual security standards, audit rights, and incident notification requirements been established?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-13, Domain 7 (Third-Party Cyber Risk); OSFI B-10",
             "owner_role": "Procurement / Cyber"},
        ],
    },
    {
        "title": "IT / Operational Risk",
        "ref": "OSFI Guideline B-10",
        "desc": "Evaluates operational resilience, support coverage, and change management.",
        "questions": [
            {"q": "Is this AI system included in the organization's Business Continuity and Disaster Recovery plan?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI B-10 (Business Continuity Management for AI)",
             "owner_role": "IT Operations"},
            {"q": "Are Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) defined and tested for this AI system?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI B-10 (RTO/RPO definition and testing)",
             "owner_role": "IT Operations"},
            {"q": "Is there a rollback or failover mechanism if the AI system produces erroneous or degraded outputs?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 5 (Model Risk Controls \u2014 Rollback / Failover)",
             "owner_role": "ML Operations"},
            {"q": "Is the AI system subject to the organization's Software Development Lifecycle (SDLC) and change management process?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI B-10 / B-13 (SDLC and Change Management)",
             "owner_role": "IT Operations"},
            {"q": "Are model versions and deployments version-controlled and auditable?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI E-23, Principle 2 (Model Inventory and Audit Trail)",
             "owner_role": "ML Operations"},
            {"q": "Is there automated monitoring for AI system uptime, latency, and output quality in production?", "opts": GENERIC_OPTS,
             "severity": "Low", "citation": "OSFI E-23, Principle 5 (Ongoing Monitoring \u2014 Uptime / Output Quality)",
             "owner_role": "ML Operations"},
        ],
    },
]

TOTAL_QUESTIONS = sum(len(m["questions"]) for m in MODULES)

SEVERITY_WEIGHT = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
SEVERITY_COLOR = {"Critical": "#B3261E", "High": "#C8860D", "Medium": "#1E3A5F", "Low": "#6B7280"}
SEVERITY_CAP = {"Critical": 44, "High": 74, "Medium": 100, "Low": 100}
# A single failed control (score < 30) at a given severity caps the overall
# band regardless of how well everything else scored — severity-weighted
# rollup, not a naive average.

# ----------------------------------------------------------------------
# Agent & Prompt Evaluation — repeatable evaluation workflows for the
# actual unit of work (prompts, agents, tool-call sequences, runtime
# behavior), distinct from the product-level governance assessment above.
# ----------------------------------------------------------------------
EVAL_TARGETS = [
    {
        "name": "Claims Summarization Copilot — v2.3",
        "type": "Prompt (Generative AI)",
        "linked_product": "Claims Summarization Copilot",
        "suite": "Groundedness & Faithfulness Suite",
        "version": "v2.3",
        "prev_version": "v2.2",
        "run_date": "2026-06-10",
        "overall": "Regression",
        "cases": [
            ("Summarize claim with conflicting adjuster notes", "Groundedness", 0.81, 0.93, "Fail"),
            ("Summarize claim with no prior history", "Faithfulness", 0.95, 0.96, "Pass"),
            ("Summarize multi-page claim (>20 pages)", "Groundedness", 0.78, 0.91, "Fail"),
            ("Redact PII in summary output", "Guardrail — PII leakage", 1.00, 1.00, "Pass"),
        ],
        "note": "v2.3 introduced a 12% drop in groundedness on long, multi-source claim files "
                "(test set B) — likely due to the new context-compression step. Recommend "
                "holding v2.3 in staging until the compression prompt is re-tuned.",
    },
    {
        "name": "Advisor Knowledge Assistant — v1.4",
        "type": "Agent (Multi-tool)",
        "linked_product": "Advisor Knowledge Assistant",
        "suite": "Tool-Call Safety & Accuracy Suite",
        "version": "v1.4",
        "prev_version": "v1.3",
        "run_date": "2026-06-12",
        "overall": "Pass",
        "cases": [
            ("Retrieve client portfolio via CRM tool", "Tool-call accuracy", 0.97, 0.96, "Pass"),
            ("Refuse out-of-scope investment advice request", "Guardrail — scope refusal", 1.00, 0.98, "Pass"),
            ("Multi-step: lookup product, then compare rates", "Tool-call sequencing", 0.92, 0.89, "Pass"),
            ("Handle ambiguous client name (disambiguation)", "Robustness", 0.84, 0.85, "Pass"),
        ],
        "note": "v1.4 is stable across all four cases, with a small improvement in tool-call "
                "sequencing accuracy (+3 pts) attributed to the updated planning prompt. "
                "Cleared for continued pilot deployment.",
    },
    {
        "name": "Fraud Anomaly Detector — Prompt Layer v3.0",
        "type": "Prompt (Classification Rationale)",
        "linked_product": "Fraud Anomaly Detector",
        "suite": "Explainability & Bias Suite",
        "version": "v3.0",
        "prev_version": "v2.8",
        "run_date": "2026-06-08",
        "overall": "Watch",
        "cases": [
            ("Generate plain-language rationale for flagged claim", "Explainability", 0.88, 0.90, "Pass"),
            ("Rationale consistency across demographic groups", "Bias / fairness", 0.86, 0.92, "Fail"),
            ("Reject prompt-injection in claim notes field", "Guardrail — prompt injection", 1.00, 1.00, "Pass"),
            ("Latency under 2s for rationale generation", "Performance", 1.40, 1.10, "Pass"),
        ],
        "note": "v3.0 shows a 6-point drop in rationale-consistency across demographic test "
                "groups (test set D) versus v2.8 — within the Watch band but trending the "
                "wrong direction for two consecutive releases. Flagged to Model Risk for review "
                "before wider rollout; not yet a release blocker.",
    },
]

EVAL_STATUS_COLOR = {"Pass": "#2A7A55", "Watch": "#C8860D", "Regression": "#B3261E", "Fail": "#B3261E"}


def eval_overall_color(overall):
    return EVAL_STATUS_COLOR.get(overall, "#6B7280")


PRODUCT_TYPES = [
    "Generative AI (LLM)", "ML Classification Model", "ML Regression Model",
    "Recommendation Engine", "Anomaly Detection", "NLP / Text Analytics",
    "Computer Vision", "Third-Party AI Tool", "Agentic / Multi-Agent System", "Other",
]
BUSINESS_LINES = [
    "Group Benefits", "Individual Insurance", "Wealth Management", "Reinsurance",
    "Customer Experience", "Fraud & Risk", "Internal Operations", "IT / Technology", "Other",
]
STAGES = [
    "Ideation / Concept", "Proof of Concept (POC)", "Pilot / Limited Deployment",
    "Production", "Monitoring / Iteration", "Decommissioning",
]
DATA_TYPES = [
    "Personal Health Information (PHI)", "Financial Data", "Behavioural / Usage Data",
    "Demographic Data", "Third-Party Data", "Publicly Available Data",
    "Internal Operational Data", "Biometric Data", "No Personal Data",
]

# ----------------------------------------------------------------------
# Risk helpers
# ----------------------------------------------------------------------
def risk_band(score):
    if score is None:
        return "Not assessed"
    if score >= 75:
        return "Low Risk"
    if score >= 45:
        return "Moderate"
    return "High Risk"


def risk_color(band):
    return {
        "Low Risk": "#2A7A55",      # forest green
        "Moderate": "#C8860D",      # amber
        "High Risk": "#B3261E",     # red
        "Not assessed": "#6B7280",  # grey
    }.get(band, "#6B7280")


def badge(text, color):
    return (
        f'<span style="background:{color}1A;color:{color};border:1px solid {color}55;'
        f'border-radius:999px;padding:3px 12px;font-size:0.78rem;font-weight:700;'
        f'white-space:nowrap;display:inline-block;">{text}</span>'
    )


# ----------------------------------------------------------------------
# Control-level helpers — Level 2 (control status) and severity weighting.
# A "control" is one question/answer pair. Status is derived directly from
# the score already implied by the chosen answer — no extra data entry.
# ----------------------------------------------------------------------
def control_status(control_score):
    """Map a 0-100 control score to a Met / Partial / Not Met status."""
    if control_score is None:
        return "Not Assessed"
    if control_score >= 80:
        return "Met"
    if control_score >= 40:
        return "Partial"
    return "Not Met"


CONTROL_STATUS_COLOR = {
    "Met": "#2A7A55",
    "Partial": "#C8860D",
    "Not Met": "#B3261E",
    "Not Assessed": "#6B7280",
}


def severity_weighted_band(answers, modules=None):
    """
    Roll up a set of {(module_title, q_index): score} answers into an
    overall risk band that respects severity caps — a single Critical
    control left Not Met caps the band at High Risk regardless of the
    average, mirroring how a real risk rollup would never let many minor
    passes offset one critical gap.
    Returns (avg_score, band, capping_control_or_None).
    """
    modules = modules or MODULES
    if not answers:
        return None, "Not assessed", None

    avg_score = round(sum(answers.values()) / len(answers))
    band = risk_band(avg_score)

    # Find the most severe Not Met / Partial control and see if it caps the band
    worst_cap = 100
    worst_control = None
    for m in modules:
        for qi, q in enumerate(m["questions"]):
            key = (m["title"], qi)
            if key not in answers:
                continue
            cscore = answers[key]
            status = control_status(cscore)
            if status in ("Not Met", "Partial"):
                sev = q.get("severity", "Medium")
                cap = SEVERITY_CAP.get(sev, 100)
                if status == "Not Met" and cap < worst_cap:
                    worst_cap = cap
                    worst_control = {
                        "module": m["title"], "question": q["q"], "severity": sev,
                        "score": cscore, "citation": q.get("citation", ""),
                    }

    final_score = min(avg_score, worst_cap) if worst_cap < 100 else avg_score
    final_band = risk_band(final_score)
    capped = worst_control if final_band != band else None
    return avg_score, final_band, capped



# Runtime contracts — evidence (score band) mapped to a defined governance
# action with named accountability, escalation path, and SLA.
# A score is a measurement; a contract is what makes it governance.
# ----------------------------------------------------------------------
RUNTIME_CONTRACTS = {
    "High Risk": {
        "decision": "BLOCKED from production",
        "actions": [
            "Deployment blocked pending remediation",
            "Incident record created and escalated",
            "Recertification required before next release",
        ],
        "approver": "AI Governance Lead",
        "escalation": "Model Risk Committee",
        "sla": "Human review within 2 business days",
        "review_cycle_days": 30,
    },
    "Moderate": {
        "decision": "CONDITIONAL approval",
        "actions": [
            "Remediation items created with owners and due dates",
            "Enhanced monitoring enabled",
            "Progress reviewed at next governance checkpoint",
        ],
        "approver": "AI Governance Lead",
        "escalation": "Business Line Risk Officer",
        "sla": "Remediation plan within 10 business days",
        "review_cycle_days": 90,
    },
    "Low Risk": {
        "decision": "APPROVED to proceed",
        "actions": [
            "Standard monitoring continues",
            "Next periodic review scheduled",
        ],
        "approver": "Product Owner (self-attestation)",
        "escalation": "AI Governance Lead",
        "sla": "Periodic recertification",
        "review_cycle_days": 180,
    },
}

# Control-stack layers: Evaluation (measures), Guardrail (enforces),
# Governance (decides / assigns accountability)
GUARDRAIL_KEYWORDS = [
    "encrypt", "authentication", "rate limiting", "access controls",
    "blocking", "minimized", "retention and deletion", "rollback", "fallback",
    "adversarial", "prompt injection",
]
GOVERNANCE_KEYWORDS = [
    "override", "appeal", "recourse", "owner", "accountab", "inventory",
    "change management", "incident response", "retirement", "decommissioning",
    "on-call", "review date", "consent",
]


def control_layer(question_text):
    qt = question_text.lower()
    for kw in GOVERNANCE_KEYWORDS:
        if kw in qt:
            return "Governance"
    for kw in GUARDRAIL_KEYWORDS:
        if kw in qt:
            return "Guardrail"
    return "Evaluation"


LAYER_COLORS = {"Evaluation": "#1E3A5F", "Guardrail": "#C8860D", "Governance": "#2A7A55"}


# ----------------------------------------------------------------------
# Seed data — mirrors the original portfolio (9 products)
# ----------------------------------------------------------------------
def _seed_answers_for_target(target_score, seed_offset=0):
    """
    Generate plausible per-question answers that roughly average to
    target_score, by picking, for each question, the option whose score is
    closest to a randomized value around the target. Deterministic per
    product via seed_offset so re-running doesn't reshuffle the demo data.
    """
    import random
    rng = random.Random(1000 + seed_offset)
    answers = {}
    for m in MODULES:
        for qi, q in enumerate(m["questions"]):
            jitter = rng.randint(-22, 22)
            wanted = max(0, min(100, target_score + jitter))
            best_opt = min(q["opts"], key=lambda o: abs(o[1] - wanted))
            answers[(m["title"], qi)] = best_opt[1]
    return answers


def zlib_crc(s):
    """Stable string hash across processes (Python's built-in hash() is
    randomized per-run unless PYTHONHASHSEED is fixed) — used to keep
    demo remediation owner/date assignments consistent on every rerun."""
    return zlib.crc32(s.encode("utf-8"))


def _remediation_for(module_title, qi, severity, owner_role=None):
    """Remediation owner and target date for Not Met / Partial controls.
    Owner comes from the question's own owner_role (the team accountable
    for that control type — e.g. Privacy Office for consent questions),
    falling back to a deterministic pick only if owner_role isn't set.
    Target date is offset by severity, same bands as the live deployment."""
    if owner_role:
        owner = owner_role
    else:
        owners = ["Model Risk Team", "Privacy Office", "Data Office",
                  "Cyber Security Team", "ML Operations", "IT Operations"]
        import random
        seed_val = (abs(zlib_crc(module_title)) + qi * 97) % 10000
        rng = random.Random(seed_val)
        owner = rng.choice(owners)
    if severity == "Critical":
        target_days = 21
    elif severity == "High":
        target_days = 32
    elif severity == "Medium":
        target_days = 75
    else:
        target_days = 100
    return owner, date.today() + timedelta(days=target_days)


def final_score_or(avg_score, band):
    """Display score consistent with the (possibly capped) band — keeps
    the headline number aligned with the band shown everywhere else."""
    if band == "High Risk" and avg_score >= 45:
        return min(avg_score, 44)
    if band == "Moderate" and avg_score >= 75:
        return min(avg_score, 74)
    return avg_score


def seed_products():
    seed = [
        ("Group Benefits Pricing Agent", "Agentic / Multi-Agent System", "Group Benefits", "Ideation / Concept", 42, "Hassan Ali"),
        ("Voice-of-Customer NLP", "NLP / Text Analytics", "Customer Experience", "Production", 69, "Lena Cho"),
        ("Vendor Risk Scoring Model", "ML Classification Model", "IT / Technology", "Proof of Concept (POC)", 77, "Marcus Webb"),
        ("Marketing Content Generator", "Generative AI (LLM)", "Customer Experience", "Pilot / Limited Deployment", 55, "Lena Cho"),
        ("Customer Churn Predictor", "ML Regression Model", "Customer Experience", "Production", 81, "Marcus Webb"),
        ("Fraud Anomaly Detector", "Anomaly Detection", "Fraud & Risk", "Monitoring / Iteration", 64, "Priya Sharma"),
        ("Underwriting Decision Engine", "ML Classification Model", "Individual Insurance", "Production", 38, "Sandra Liu"),
        ("Advisor Knowledge Assistant", "Generative AI (LLM)", "Wealth Management", "Pilot / Limited Deployment", 72, "Devon Marsh"),
        ("Claims Summarization Copilot", "Generative AI (LLM)", "Group Benefits", "Production", 58, "Priya Sharma"),
    ]
    products = []
    today = date.today()
    review_offsets = [-12, 45, 120, 20, 160, -5, -30, 60, 15]  # negative = overdue
    for i, ((name, ptype, bline, stage, score, owner), offset) in enumerate(zip(seed, review_offsets)):
        answers = _seed_answers_for_target(score, seed_offset=i)
        avg_score, final_band, capped = severity_weighted_band(answers)

        # Level 3: assessment history — three prior snapshots trending
        # toward the current score, so there's a trend to drill into.
        history = []
        for h in range(3, 0, -1):
            h_score = max(5, min(100, score + (h * 6) - 9))  # mild trend
            history.append({
                "date": today - timedelta(days=h * 75),
                "score": h_score,
                "band": risk_band(h_score),
                "reviewer": "AI Governance Lead",
            })

        products.append({
            "id": str(uuid.uuid4()),
            "name": name,
            "type": ptype,
            "business_line": bline,
            "stage": stage,
            "customer_facing": True,
            "automated_decisions": "Underwriting" in name or "Pricing" in name,
            "third_party": False,
            "data_types": ["Internal Operational Data"],
            "owner_name": owner,
            "owner_email": f"{owner.lower().replace(' ', '.')}@example.com",
            "approver": "Business Line Risk Officer" if bline == "Group Benefits" else "AI Governance Lead",
            "review_date": today + timedelta(days=offset),
            "description": "Seed demo product — pre-loaded for portfolio illustration.",
            "answers": answers,
            "score": final_score_or(avg_score, final_band),
            "raw_avg_score": avg_score,
            "capped_by": capped,
            "answered_count": TOTAL_QUESTIONS,  # treat seeds as fully assessed
            "history": history,
        })
    return products


if "products" not in st.session_state:
    st.session_state.products = seed_products()
if "page" not in st.session_state:
    st.session_state.page = "Portfolio"
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "compare_selection" not in st.session_state:
    st.session_state.compare_selection = []

# ----------------------------------------------------------------------
# Top navigation bar — 4 top-level pages. Register Product moved to a
# button on Portfolio; Knowledge Base, Roadmap, and Agent Evaluation are
# now sub-pages under the "Library" hub (matching the Lovable redesign).
# ----------------------------------------------------------------------
NAV_PAGES = ["Portfolio", "Assess", "Findings", "Library"]
LIBRARY_SUBPAGES = ["Knowledge Base", "Roadmap", "Agent Evaluation"]

st.markdown(
    f"""
    <div class="top-nav">
        <div class="brand">\u25C6 AI & ML Governance Command Centre</div>
        {badge("Demo Mode", AMBER)}
    </div>
    """,
    unsafe_allow_html=True,
)

nav_cols = st.columns(len(NAV_PAGES))
for col, page_name in zip(nav_cols, NAV_PAGES):
    with col:
        is_active = (
            st.session_state.page == page_name
            or (page_name == "Library" and st.session_state.page in LIBRARY_SUBPAGES)
        )
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = "Library" if page_name == "Library" else page_name
            st.rerun()

# ----------------------------------------------------------------------
# PORTFOLIO PAGE
# ----------------------------------------------------------------------
def portfolio_page():
    hcol1, hcol2 = st.columns([5, 1.3])
    with hcol1:
        st.markdown(
            """
            <div class="gov-hero">
                <h1>Governance Action Queue</h1>
                <p>What needs attention right now, followed by the full portfolio. Multi-dimensional
                governance posture across every registered AI/ML system, scored against current
                OSFI, PIPEDA, Law 25, and Treasury Board guidance.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hcol2:
        st.write("")
        if st.button("+ Register Product", key="goto_register", use_container_width=True, type="primary"):
            st.session_state.page = "Register Product"
            st.rerun()

    products = st.session_state.products
    total = len(products)
    high = sum(1 for p in products if risk_band(p["score"]) == "High Risk")
    moderate = sum(1 for p in products if risk_band(p["score"]) == "Moderate")
    low = sum(1 for p in products if risk_band(p["score"]) == "Low Risk")
    overdue = sum(1 for p in products if p["review_date"] and p["review_date"] < date.today())

    # Headline: one dominant number (what needs attention right now), with
    # the full breakdown as a compact secondary strip — not five equally
    # weighted tiles competing for attention.
    needs_attention = high + overdue
    headline_color = "#B3261E" if needs_attention else FOREST
    st.markdown(
        f"""
        <div class="metric-tile" style="--accent:{headline_color};padding:1.1rem 1.4rem;">
            <div class="num" style="font-size:2.6rem;color:{headline_color};">{needs_attention}</div>
            <div class="label" style="font-size:1rem;">
                {"systems need attention" if needs_attention else "All systems in good standing"}
            </div>
            <div class="sub">{high} High Risk &nbsp;\u00b7&nbsp; {overdue} review(s) overdue &nbsp;\u00b7&nbsp; out of {total} registered</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📊 Full portfolio breakdown", expanded=False):
        tiles = [
            ("Registered Products", total, "across all business lines", NAVY),
            ("High Risk", high, "blocked pending remediation", "#B3261E"),
            ("Moderate Risk", moderate, "conditional approval", AMBER),
            ("Low Risk", low, "approved to proceed", FOREST),
            ("Reviews Overdue", overdue, "recertification required", "#B3261E" if overdue else FOREST),
        ]
        cols = st.columns(5)
        for col, (label, num, sub, color) in zip(cols, tiles):
            col.markdown(
                f"""
                <div class="metric-tile" style="--accent:{color}">
                    <div class="num">{num}</div>
                    <div class="label">{label}</div>
                    <div class="sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # Governance Action Queue — table format with status tabs, matching the
    # Lovable redesign: Product / Action / SLA / Owner -> Approver / link.
    blocked = []
    overdue = []
    for p in products:
        band = risk_band(p["score"])
        if band == "High Risk":
            blocked.append((p, "BLOCKED", RUNTIME_CONTRACTS['High Risk']['sla'], "#B3261E"))
        if p["review_date"] and p["review_date"] < date.today():
            days = (date.today() - p["review_date"]).days
            overdue.append((p, "OVERDUE", f"Review overdue by {days} days", AMBER))

    all_queue = blocked + overdue
    n_blocked, n_overdue, n_all = len(blocked), len(overdue), len(all_queue)

    st.markdown(f"#### Governance Action Queue")
    tab_all, tab_blocked, tab_overdue = st.tabs([f"All ({n_all})", f"Blocked ({n_blocked})", f"Overdue ({n_overdue})"])

    def render_queue_table(rows):
        if not rows:
            st.info("Nothing in this view — portfolio is in good standing.")
            return
        for p, action, sla_text, color in rows:
            crit_count = sum(
                1 for m in MODULES for qi, q in enumerate(m["questions"])
                if (m["title"], qi) in p["answers"]
                and control_status(p["answers"][(m["title"], qi)]) == "Not Met"
                and q.get("severity") == "Critical"
            )
            crit_badge = (
                badge(f'{crit_count} Critical finding' + ('s' if crit_count != 1 else ''), "#B3261E")
                if crit_count else ""
            )
            row_cols = st.columns([2.4, 1.1, 2.1, 2.2, 1.1])
            row_cols[0].markdown(
                f'<div class="product-name" style="font-size:0.92rem;">{p["name"]}</div>'
                f'<div class="product-meta">{p["business_line"]}</div>',
                unsafe_allow_html=True,
            )
            row_cols[1].markdown(badge(action, color), unsafe_allow_html=True)
            row_cols[2].markdown(
                f'<span style="font-size:0.82rem;color:{INK};">{sla_text}</span><br>{crit_badge}',
                unsafe_allow_html=True,
            )
            row_cols[3].markdown(
                f'<span style="font-size:0.82rem;color:{INK};">{p["owner_name"]}</span>'
                f'<span style="color:#8A8475;"> → {p.get("approver", "AI Governance Lead")}</span>',
                unsafe_allow_html=True,
            )
            if row_cols[4].button("Open →", key=f"queue_open_{p['id']}_{action}", use_container_width=True):
                st.session_state.selected_product = p["id"]
                st.session_state.page = "Assess"
                st.rerun()
            st.markdown('<hr style="margin:0.3rem 0;border-color:#E5E0D5;">', unsafe_allow_html=True)

    with tab_all:
        render_queue_table(all_queue)
    with tab_blocked:
        render_queue_table(blocked)
    with tab_overdue:
        render_queue_table(overdue)

    if all_queue:
        st.caption("See the **Findings** page for the full control-level breakdown behind every score.")

    st.caption("⚠️ Demo data — stored in this browser session only, resets on refresh.")

    with st.expander(f"🔍 Browse all products ({total})", expanded=(not all_queue)):
        fc1, fc2, fc3 = st.columns(3)
        risk_filter = fc1.selectbox(
            "Risk", ["All risk", "High risk", "Moderate", "Low risk", "Not assessed"]
        )
        line_filter = fc2.selectbox("Business line", ["All business lines"] + BUSINESS_LINES)
        stage_filter = fc3.selectbox("Stage", ["All stages"] + STAGES)

        filtered = products
        if risk_filter != "All risk":
            target = {"High risk": "High Risk", "Moderate": "Moderate", "Low risk": "Low Risk", "Not assessed": "Not assessed"}[risk_filter]
            filtered = [p for p in filtered if risk_band(p["score"]) == target]
        if line_filter != "All business lines":
            filtered = [p for p in filtered if p["business_line"] == line_filter]
        if stage_filter != "All stages":
            filtered = [p for p in filtered if p["stage"] == stage_filter]

        st.write(f"**{len(filtered)} of {total} products**")

        if not filtered:
            st.info("No products match the selected filters.")

        MAX_COMPARE = 3
        for row_start in range(0, len(filtered), 3):
            row = filtered[row_start:row_start + 3]
            cols = st.columns(3)
            for col, p in zip(cols, row):
                band = risk_band(p["score"])
                color = risk_color(band)
                score_text = f"{p['score']}/100" if p["score"] is not None else "—"
                with col:
                    st.markdown(
                        f"""
                        <div class="product-card">
                            <div class="product-name">{p['name']}</div>
                            <div class="product-meta">{p['type']}</div>
                            <div class="product-meta">{p['business_line']} · {p['stage']}</div>
                            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.7rem;">
                                <span class="score-num" style="color:{color};">{score_text}</span>
                                {badge(band, color)}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    bcol1, bcol2 = st.columns([2, 1.2])
                    if bcol1.button("Open →", key=f"open_{p['id']}", use_container_width=True):
                        st.session_state.selected_product = p["id"]
                        st.session_state.page = "Assess"
                        st.rerun()
                    already_selected = p["id"] in st.session_state.compare_selection
                    at_cap = len(st.session_state.compare_selection) >= MAX_COMPARE
                    checked = bcol2.checkbox(
                        "Compare",
                        value=already_selected,
                        key=f"cmp_{p['id']}",
                        disabled=(at_cap and not already_selected),
                    )
                    if checked and not already_selected:
                        st.session_state.compare_selection.append(p["id"])
                        st.rerun()
                    elif not checked and already_selected:
                        st.session_state.compare_selection.remove(p["id"])
                        st.rerun()

        n_selected = len(st.session_state.compare_selection)
        if n_selected:
            st.write("")
            ccol1, ccol2 = st.columns([4, 1.3])
            sel_names = [p["name"] for p in products if p["id"] in st.session_state.compare_selection]
            ccol1.markdown(
                f"**{n_selected} selected for comparison** (max {MAX_COMPARE}): " + ", ".join(sel_names)
            )
            if ccol2.button(f"Compare ({n_selected}) →", type="primary", use_container_width=True, disabled=(n_selected < 2)):
                st.session_state.page = "Compare"
                st.rerun()
            if n_selected < 2:
                st.caption("Select at least 2 products to compare.")


# ----------------------------------------------------------------------
# REGISTER PRODUCT PAGE
# ----------------------------------------------------------------------
def register_page():
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Register an AI/ML Product</h1>
            <p>Capture the system's basic profile. The orchestrator uses these attributes
            to weight downstream agent assessments.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("register_form", clear_on_submit=True):
        st.markdown("##### 1. Product Profile")
        name = st.text_input("Product / Model Name *")
        ptype = st.selectbox("Product Type *", ["Select…"] + PRODUCT_TYPES)
        bline = st.selectbox("Business Line *", ["Select…"] + BUSINESS_LINES)
        stage = st.selectbox("Current Deployment Stage *", ["Select…"] + STAGES)

        customer_facing = st.checkbox(
            "Does this system directly affect customers or policyholders?",
            help="Include any system that influences a customer-facing decision, communication, or outcome.",
        )
        automated_decisions = st.checkbox(
            "Does this system make or significantly influence automated decisions about individuals?",
            help="Examples: claims adjudication, underwriting decisions, benefit eligibility, fraud flags.",
        )
        third_party = st.checkbox(
            "Is this a third-party AI tool or vendor-supplied model?",
            help="Include SaaS AI tools, vendor ML models, and any externally hosted AI capabilities.",
        )

        st.markdown("**Types of data used by this system ***")
        data_types = st.multiselect("Data types", DATA_TYPES, label_visibility="collapsed")

        owner_name = st.text_input("Product Owner Name *")
        owner_email = st.text_input("Product Owner Email *")
        approver = st.text_input(
            "Accountable Approver",
            value="AI Governance Lead",
            help="Named role or person with authority to approve, block, or escalate this system.",
        )
        review_date = st.date_input("Next Scheduled Review Date", value=None)
        description = st.text_area("Brief Description *")

        submitted = st.form_submit_button("Register & Continue to Assessment →")

    if submitted:
        missing = []
        if not name:
            missing.append("Product / Model Name")
        if ptype == "Select…":
            missing.append("Product Type")
        if bline == "Select…":
            missing.append("Business Line")
        if stage == "Select…":
            missing.append("Current Deployment Stage")
        if not data_types:
            missing.append("Types of data used")
        if not owner_name:
            missing.append("Product Owner Name")
        if not owner_email:
            missing.append("Product Owner Email")
        if not description:
            missing.append("Brief Description")

        if missing:
            st.error("Please complete the required fields: " + ", ".join(missing))
        else:
            new_id = str(uuid.uuid4())
            st.session_state.products.append({
                "id": new_id,
                "name": name,
                "type": ptype,
                "business_line": bline,
                "stage": stage,
                "customer_facing": customer_facing,
                "automated_decisions": automated_decisions,
                "third_party": third_party,
                "data_types": data_types,
                "owner_name": owner_name,
                "owner_email": owner_email,
                "approver": approver or "AI Governance Lead",
                "review_date": review_date,
                "description": description,
                "answers": {},
                "score": None,
                "raw_avg_score": None,
                "capped_by": None,
                "answered_count": 0,
                "history": [],
            })
            st.session_state.selected_product = new_id
            st.session_state.page = "Assess"
            st.success(f"{name} registered. Continue to assessment →")
            st.rerun()


# ----------------------------------------------------------------------
# ASSESS PAGE
# ----------------------------------------------------------------------
def assess_page():
    products = st.session_state.products
    if not products:
        st.markdown(
            """
            <div class="gov-hero">
                <h1>Assessment</h1>
                <p>No products registered yet. Use Register Product to add one.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    names = [p["name"] for p in products]
    default_idx = 0
    if st.session_state.selected_product:
        for i, p in enumerate(products):
            if p["id"] == st.session_state.selected_product:
                default_idx = i
                break

    st.markdown(
        """
        <div class="gov-hero">
            <h1>Assessment</h1>
            <p>Run the assessment to get a governance decision. Expand any section below
            for the control-level evidence behind it.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sel_name = st.selectbox("Select product", names, index=default_idx)
    product = next(p for p in products if p["name"] == sel_name)
    st.session_state.selected_product = product["id"]

    band_now = risk_band(product["score"])
    color_now = risk_color(band_now)
    score_text = f"{product['score']}/100" if product["score"] is not None else "—"

    st.markdown(
        f"""
        <div class="product-card" style="margin-top:0.4rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.6rem;">
                <div>
                    <div class="product-name" style="font-size:1.25rem;">{product['name']}</div>
                    <div class="product-meta">{product['type']} · {product['business_line']} · {product['stage']}</div>
                </div>
                <div style="text-align:right;">
                    <div class="score-num" style="color:{color_now};">{score_text}</div>
                    <div style="margin-top:4px;">{badge(band_now, color_now)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answers = product["answers"]
    answered_count = sum(1 for m in MODULES for q in range(len(m["questions"]))
                          if (m["title"], q) in answers)
    progress = answered_count / TOTAL_QUESTIONS

    st.write("")
    pcol1, pcol2 = st.columns([3, 1])
    pcol1.progress(progress, text=f"Progress: {answered_count}/{TOTAL_QUESTIONS}")
    if pcol2.button("Run Assessment (Simulated) →", type="primary", use_container_width=True):
        if answered_count == 0:
            st.warning("Answer at least one question before running the assessment.")
        else:
            avg_score, band, capped = severity_weighted_band(answers)
            display_score = final_score_or(avg_score, band)
            product["score"] = display_score
            product["raw_avg_score"] = avg_score
            product["capped_by"] = capped
            product["answered_count"] = answered_count
            new_color = risk_color(band)
            contract = RUNTIME_CONTRACTS[band]
            product["review_date"] = date.today() + timedelta(days=contract["review_cycle_days"])

            # Level 3 — append this run to assessment history
            product.setdefault("history", []).append({
                "date": date.today(),
                "score": display_score,
                "band": band,
                "reviewer": product.get("approver", "AI Governance Lead"),
            })

            actions_html = "".join(f"<li>{a}</li>" for a in contract["actions"])

            st.markdown(
                f"""
                <div class="product-card" style="border-left:5px solid {new_color};">
                    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;align-items:center;">
                        <div style="font-weight:800;font-size:1.05rem;color:{INK};">
                            Governance Decision: <span style="color:{new_color};">{contract['decision']}</span>
                        </div>
                        <div>
                            <span class="score-num" style="color:{new_color};">{display_score}/100</span>
                            &nbsp;{badge(band, new_color)}
                        </div>
                    </div>
                    <div style="margin-top:0.5rem;color:{INK};font-size:0.9rem;">
                        <strong>Runtime contract — evidence mapped to action:</strong>
                        <ul style="margin:0.3rem 0 0.5rem 1.1rem;padding:0;">{actions_html}</ul>
                    </div>
                    <div class="product-meta" style="display:flex;gap:1.2rem;flex-wrap:wrap;">
                        <span><strong>Accountable owner:</strong> {product['owner_name']}</span>
                        <span><strong>Approver:</strong> {product.get('approver', contract['approver'])}</span>
                        <span><strong>Escalation:</strong> {contract['escalation']}</span>
                        <span><strong>SLA:</strong> {contract['sla']}</span>
                        <span><strong>Next review:</strong> {product['review_date'].strftime('%b %d, %Y')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if capped:
                with st.expander(f"⚠️ Why {band}? A {capped['severity']} control capped this score", expanded=False):
                    st.markdown(
                        f"""
                        <div style="font-size:0.86rem;color:{INK};">
                            The average score across all answered controls was <strong>{avg_score}</strong>,
                            which on its own would land in a higher band. But a
                            <strong style="color:{RED};">{capped['severity']}</strong>-severity control was
                            <strong>Not Met</strong>: “{capped['question']}” — so the band is capped at
                            <strong>{band}</strong> regardless of the average. One critical gap can't be
                            offset by passing minor controls.
                            <div style="margin-top:0.4rem;color:#6B6557;font-size:0.8rem;">
                                Citation: {capped['citation']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # Per-module agent score breakdown — collapsed by default
            rows_html = ""
            for m in MODULES:
                m_scores = [answers[(m["title"], qi)] for qi in range(len(m["questions"]))
                            if (m["title"], qi) in answers]
                if m_scores:
                    m_avg = round(sum(m_scores) / len(m_scores))
                    m_color = risk_color(risk_band(m_avg))
                    rows_html += (
                        f'<div class="mscore-row">'
                        f'<div class="mscore-label">{m["title"]}</div>'
                        f'<div class="mscore-track"><div class="mscore-fill" '
                        f'style="width:{m_avg}%;background:{m_color};"></div></div>'
                        f'<div class="mscore-val" style="color:{m_color};">{m_avg}</div>'
                        f'</div>'
                    )
                else:
                    rows_html += (
                        f'<div class="mscore-row">'
                        f'<div class="mscore-label">{m["title"]}</div>'
                        f'<div class="mscore-track"></div>'
                        f'<div class="mscore-val" style="color:#8A8475;">\u2014</div>'
                        f'</div>'
                    )
            with st.expander("📊 Module evidence breakdown", expanded=False):
                st.markdown(rows_html, unsafe_allow_html=True)

    st.write("")

    # Level 3 (time) — assessment history / trend
    history = product.get("history", [])
    if history:
        with st.expander(f"📈 Assessment history ({len(history)} prior {'run' if len(history)==1 else 'runs'})", expanded=False):
            sorted_hist = sorted(history, key=lambda h: h["date"])
            rows_html = ""
            prev_score = None
            for h in sorted_hist:
                hcolor = risk_color(h["band"])
                if prev_score is not None:
                    delta = h["score"] - prev_score
                    arrow = "\u25B2" if delta > 0 else ("\u25BC" if delta < 0 else "\u2014")
                    dcolor = FOREST if delta > 0 else ("#B3261E" if delta < 0 else "#8A8475")
                    delta_html = f"<span style='color:{dcolor};font-size:0.78rem;'>{arrow} {abs(delta)}</span>"
                else:
                    delta_html = "<span style='color:#8A8475;font-size:0.78rem;'>baseline</span>"
                rows_html += (
                    f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.4rem 0;'
                    f'border-bottom:1px solid #E5E0D5;">'
                    f'<div style="width:110px;font-size:0.8rem;color:#6B6557;">{h["date"].strftime("%b %d, %Y")}</div>'
                    f'<div style="width:60px;font-weight:700;color:{hcolor};">{h["score"]}</div>'
                    f'<div style="width:110px;">{badge(h["band"], hcolor)}</div>'
                    f'<div style="width:80px;">{delta_html}</div>'
                    f'<div style="font-size:0.78rem;color:#8A8475;">Reviewed by {h["reviewer"]}</div>'
                    f'</div>'
                )
                prev_score = h["score"]
            st.markdown(
                f'<div class="product-card" style="padding:0.6rem 1rem;">{rows_html}</div>',
                unsafe_allow_html=True,
            )

    st.write("")

    # Module overview pills
    mod_cols = st.columns(len(MODULES))
    for i, m in enumerate(MODULES):
        n_answered = sum(1 for q in range(len(m["questions"])) if (m["title"], q) in answers)
        is_complete = n_answered == len(m["questions"])
        active_class = "active" if is_complete else ""
        with mod_cols[i]:
            st.markdown(
                f"""
                <div class="mod-pill {active_class}">
                    <span class="mod-num">{i+1}</span>
                    <div class="mod-title">{m['title']}</div>
                    <div class="mod-sub">{n_answered}/{len(m['questions'])} answered</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    st.write("")

    with st.expander("ℹ️ About the control stack (Evaluation · Guardrail · Governance)", expanded=False):
        st.markdown(
            f"""
            {badge("Evaluation — measures (Is this good?)", LAYER_COLORS['Evaluation'])}&nbsp;
            {badge("Guardrail — enforces (Is this allowed?)", LAYER_COLORS['Guardrail'])}&nbsp;
            {badge("Governance — decides (What happens next?)", LAYER_COLORS['Governance'])}
            """,
            unsafe_allow_html=True,
        )
    st.write("")

    # Render each module as an expander
    for i, m in enumerate(MODULES):
        n_answered = sum(1 for q in range(len(m["questions"])) if (m["title"], q) in answers)
        icon = "✅" if n_answered == len(m["questions"]) else ("🟡" if n_answered else "⬜")
        with st.expander(f"{icon} Module {i+1} · {m['title']}  —  {m['ref']}", expanded=False):
            st.write(m["desc"])
            for qi, q in enumerate(m["questions"]):
                key = f"{product['id']}_{m['title']}_{qi}"
                option_labels = [o[0] for o in q["opts"]]
                current = answers.get((m["title"], qi))
                current_label = None
                if current is not None:
                    for label, score in q["opts"]:
                        if score == current:
                            current_label = label
                            break
                idx = option_labels.index(current_label) if current_label in option_labels else None

                with st.container(border=True):
                    layer = control_layer(q["q"])
                    lcolor = LAYER_COLORS[layer]
                    severity = q.get("severity", "Medium")
                    sev_color = SEVERITY_COLOR.get(severity, "#6B7280")
                    status = control_status(current)
                    status_color = CONTROL_STATUS_COLOR.get(status, "#6B7280")

                    # Single compact signal: a colored left accent (severity)
                    # carried by the container border, plus one status badge
                    # next to the question — citation/layer tucked behind a
                    # "details" toggle so the default view reads as a list
                    # of questions + statuses, not a wall of metadata.
                    st.markdown(
                        f"<div style='border-left:3px solid {sev_color};padding-left:0.6rem;'>"
                        f"<strong>{qi+1:02d}. {q['q']}</strong> &nbsp;{badge(status, status_color)}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    choice = st.radio(
                        "Response",
                        option_labels,
                        index=idx,
                        key=key,
                        label_visibility="collapsed",
                        horizontal=True,
                    )
                    # store score for the chosen option
                    for label, score in q["opts"]:
                        if label == choice:
                            answers[(m["title"], qi)] = score

                    new_status = control_status(answers.get((m["title"], qi)))
                    detail_bits = []
                    if q.get("citation"):
                        detail_bits.append(f"⚓ {q['citation']}")
                    detail_bits.append(f"Severity: {severity}")
                    detail_bits.append(f"Layer: {layer}")
                    r_owner, r_date = (None, None)
                    if new_status in ("Not Met", "Partial"):
                        r_owner, r_date = _remediation_for(m["title"], qi, severity, q.get("owner_role"))

                    with st.expander("Details", expanded=False):
                        st.markdown(
                            f"<span style='font-size:0.78rem;color:#6B6557;'>{' &nbsp;·&nbsp; '.join(detail_bits)}</span>",
                            unsafe_allow_html=True,
                        )
                        if r_owner:
                            st.markdown(
                                f"""
                                <div style="margin-top:0.4rem;padding:0.45rem 0.7rem;
                                            background:{CONTROL_STATUS_COLOR[new_status]}10;
                                            border-left:3px solid {CONTROL_STATUS_COLOR[new_status]};
                                            border-radius:6px;font-size:0.78rem;color:{INK};">
                                    <strong>Remediation:</strong> {r_owner} \u00b7 target {r_date.strftime('%b %d, %Y')}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


# ----------------------------------------------------------------------
# Shared sub-nav strip for the Library hub and its three sub-pages —
# Overview / Knowledge Base / Roadmap / Agent Evaluation
# ----------------------------------------------------------------------
def library_subnav(current):
    items = [
        ("Overview", "Library", "Library hub"),
        ("Knowledge Base", "Knowledge Base", "Regulatory corpus + runtime contracts"),
        ("Roadmap", "Roadmap", "Quarter-by-quarter delivery plan"),
        ("Agent Evaluation", "Agent Evaluation", "Per-version regression results"),
    ]
    cols = st.columns(len(items))
    for col, (label, page_key, sub) in zip(cols, items):
        is_active = current == page_key
        with col:
            if st.button(
                label,
                key=f"libnav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = page_key
                st.rerun()
    st.write("")


# ----------------------------------------------------------------------
# LIBRARY HUB PAGE
# ----------------------------------------------------------------------
def library_page():
    library_subnav("Library")
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Reference, plan, and evidence — one place</h1>
            <p>The supporting material behind every score: what the agents read, what we're
            building next, and how each release is regression-tested.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cards = [
        ("Reference", "Knowledge Base",
         "The regulatory corpus the agents consult — OSFI, PIPEDA, Law 25, Treasury Board — "
         "plus the runtime contracts that translate scores into governance decisions.",
         "Open knowledge base →", NAVY),
        ("Plan", "Roadmap",
         "Where the Command Centre is going. Quarter-by-quarter delivery across foundations, "
         "intelligence, operations, and enterprise scale.",
         "Open roadmap →", FOREST),
        ("Evidence", "Agent Evaluation",
         'Per-version regression results for prompts and agents. Answers "did this release '
         'regress?" — distinct from product-level governance scoring.',
         "Open evaluations →", AMBER),
    ]
    cols = st.columns(3)
    for col, (kicker, title, desc, cta, color) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="product-card" style="border-left:4px solid {color};height:100%;">'
                f'<div style="font-size:0.74rem;font-weight:700;color:{color};text-transform:uppercase;'
                f'letter-spacing:0.03em;margin-bottom:4px;">{kicker}</div>'
                f'<div class="product-name" style="margin-bottom:6px;">{title}</div>'
                f'<div class="product-meta">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button(cta, key=f"libcard_{title}", use_container_width=True):
                st.session_state.page = title
                st.rerun()



def knowledge_page():
    library_subnav("Knowledge Base")
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Knowledge Base</h1>
            <p>Reference summaries of the regulatory and governance frameworks underpinning
            each assessment module.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    refs = [
        ("Treasury Board Directive on Automated Decision-Making (ADM)",
         "Sets requirements for federal use of automated decision systems, including Algorithmic Impact "
         "Assessments, transparency, explainability, and human-in-the-loop review for higher-impact systems."),
        ("CLHIA AI Principles",
         "Guidance from the Canadian Life and Health Insurance Association on responsible AI use across the "
         "industry, emphasizing fairness, accountability, transparency, and customer protection."),
        ("OSFI Guideline E-23 — Model Risk Management",
         "Sets expectations for federally regulated financial institutions on model identification, validation, "
         "ongoing monitoring, governance, and documentation across the model lifecycle."),
        ("PIPEDA",
         "Canada's federal private-sector privacy law governing the collection, use, and disclosure of personal "
         "information, including consent, retention limits, and individual access rights."),
        ("Quebec Law 25",
         "Quebec's modernized privacy legislation, introducing stricter consent requirements, mandatory privacy "
         "impact assessments for certain projects, and rules on cross-border data transfers."),
        ("OSFI Cyber Security Self-Assessment",
         "A framework for federally regulated institutions to evaluate their cyber security posture, including "
         "controls, third-party risk, and incident response readiness."),
    ]

    for title, body in refs:
        st.markdown(
            f"""
            <div class="ref-card">
                <div class="ref-title">{title}</div>
                <div>{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("Runtime contracts — from evidence to action")
    st.write(
        "A score is a measurement; governance is what happens next. Each risk band is mapped "
        "to a defined decision, set of actions, accountable approver, escalation path, and SLA."
    )
    ccols = st.columns(3)
    for col, band_name in zip(ccols, ["High Risk", "Moderate", "Low Risk"]):
        c = RUNTIME_CONTRACTS[band_name]
        bc = risk_color(band_name)
        actions_html = "".join(f"<li>{a}</li>" for a in c["actions"])
        col.markdown(
            f"""
            <div class="ref-card" style="border-left-color:{bc};height:100%;">
                <div style="margin-bottom:0.3rem;">{badge(band_name, bc)}</div>
                <div class="ref-title">{c['decision']}</div>
                <ul style="margin:0.2rem 0 0.5rem 1.1rem;padding:0;font-size:0.85rem;">{actions_html}</ul>
                <div style="font-size:0.8rem;color:#6B6557;">
                    Approver: {c['approver']}<br>
                    Escalation: {c['escalation']}<br>
                    SLA: {c['sla']}<br>
                    Review cycle: every {c['review_cycle_days']} days
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("How scoring actually works — three levels of depth")
    st.write(
        "A risk band isn't just an average. Every question is a named control, weighted by "
        "severity, traceable to a specific regulatory citation, and \u2014 if Not Met or Partial "
        "\u2014 carries a remediation owner and target date."
    )
    lcols = st.columns(3)
    level_info = [
        ("Level 1 — Score & band", NAVY,
         "The headline number on the Portfolio page: a 0\u2013100 score and risk band, "
         "rolled up from every control in every module."),
        ("Level 2 — Control status", FOREST,
         "Each question is a control with its own status (Met / Partial / Not Met), "
         "severity (Critical \u2192 Low), and citation. See them all on the Findings page."),
        ("Level 3 — Evidence & history", AMBER,
         "For any Not Met or Partial control: who owns the fix and by when. For any "
         "product: how its score has trended over past assessments."),
    ]
    for col, (title, color, body) in zip(lcols, level_info):
        col.markdown(
            f"""
            <div class="ref-card" style="border-left-color:{color};height:100%;">
                <div class="ref-title" style="color:{color};">{title}</div>
                <div style="font-size:0.85rem;">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        f"""
        <div class="product-card" style="padding:0.8rem 1rem;">
            <strong style="color:{INK};">Severity-weighted rollup, not a simple average:</strong>
            <span style="font-size:0.86rem;color:#6B6557;">
            a single <strong>Critical</strong> control left Not Met caps the band at High Risk
            (score \u2264 44) regardless of the average \u2014 it can't be offset by other controls
            passing. A Not Met <strong>High</strong>-severity control caps at Moderate (\u2264 74).
            Medium and Low severities don't cap the band on their own, but still appear as
            findings. This mirrors how real risk rollups work: one critical gap is a critical
            gap, no matter how much else is in order.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.subheader("Risk band thresholds")
    rcols = st.columns(4)
    band_info = [
        ("Low Risk", "≥ 75", "Approved to proceed", FOREST),
        ("Moderate", "45–74", "Conditional approval, remediation tracked", AMBER),
        ("High Risk", "< 45", "Requires remediation before proceeding", "#B3261E"),
        ("Not assessed", "—", "No questions answered yet", "#6B7280"),
    ]
    for col, (label, rng, desc, color) in zip(rcols, band_info):
        col.markdown(
            f"""
            <div class="metric-tile" style="--accent:{color}">
                <div style="margin-bottom:4px;">{badge(label, color)}</div>
                <div class="num" style="font-size:1.3rem;">{rng}</div>
                <div class="sub">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# AGENT & PROMPT EVALUATION PAGE
# ----------------------------------------------------------------------
def agent_eval_page():
    library_subnav("Agent Evaluation")
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Agent & Prompt Evaluation</h1>
            <p>Repeatable evaluation workflows for the actual unit of work \u2014 prompts, agents,
            tool-call sequences, and runtime behavior \u2014 run per version and compared against
            the prior release. This is distinct from the product-level governance assessment:
            it answers <em>"did this version regress?"</em> rather than <em>"is this product
            risky overall?"</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="demo-notice">\u26A0\uFE0F Illustrative evaluation runs \u2014 test cases and '
        'scores below are static demo data showing how regression results would surface, '
        'not a connected evaluation harness.</div>',
        unsafe_allow_html=True,
    )

    # Summary tiles
    n_pass = sum(1 for t in EVAL_TARGETS if t["overall"] == "Pass")
    n_watch = sum(1 for t in EVAL_TARGETS if t["overall"] == "Watch")
    n_reg = sum(1 for t in EVAL_TARGETS if t["overall"] == "Regression")
    tiles = [
        ("Evaluation Runs", len(EVAL_TARGETS), "most recent per target", NAVY),
        ("Pass", n_pass, "no regressions detected", FOREST),
        ("Watch", n_watch, "trending the wrong way", AMBER),
        ("Regression", n_reg, "blocks promotion", "#B3261E"),
    ]
    cols = st.columns(4)
    for col, (label, num, sub, color) in zip(cols, tiles):
        col.markdown(
            f"""
            <div class="metric-tile" style="--accent:{color}">
                <div class="num">{num}</div>
                <div class="label">{label}</div>
                <div class="sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        f"""
        <div class="product-card" style="padding:0.7rem 1rem;">
            <span style="font-weight:700;color:{INK};margin-right:0.8rem;">Result bands:</span>
            {badge("Pass — within tolerance of prior version", EVAL_STATUS_COLOR['Pass'])}&nbsp;
            {badge("Watch — degrading trend, not yet blocking", EVAL_STATUS_COLOR['Watch'])}&nbsp;
            {badge("Regression — fails threshold, blocks promotion", EVAL_STATUS_COLOR['Regression'])}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    for target in EVAL_TARGETS:
        color = eval_overall_color(target["overall"])
        with st.expander(
            f"{target['name']}  \u2014  {target['suite']}",
            expanded=(target["overall"] != "Pass"),
        ):
            # Header row
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;align-items:center;margin-bottom:0.5rem;">
                    <div class="product-meta">
                        Linked product: <strong>{target['linked_product']}</strong> &nbsp;\u00b7&nbsp;
                        Type: {target['type']} &nbsp;\u00b7&nbsp;
                        Run date: {target['run_date']} &nbsp;\u00b7&nbsp;
                        Comparing {target['prev_version']} \u2192 {target['version']}
                    </div>
                    <div>{badge("Overall: " + target['overall'], color)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Test case table
            header_cols = st.columns([3.2, 1.8, 1, 1, 1])
            header_labels = ["Test case", "Dimension", f"{target['prev_version']}", f"{target['version']}", "Result"]
            for hc, hl in zip(header_cols, header_labels):
                hc.markdown(f"<span style='font-size:0.78rem;font-weight:700;color:#6B6557;text-transform:uppercase;'>{hl}</span>", unsafe_allow_html=True)

            for case_name, dimension, prev_score, new_score, result in target["cases"]:
                rcolor = EVAL_STATUS_COLOR.get(result, "#6B7280")
                delta = new_score - prev_score
                # For latency-type metrics lower is better; detect by dimension name
                lower_is_better = "Performance" in dimension or "Latency" in dimension
                improved = (delta < 0) if lower_is_better else (delta > 0)
                arrow = "\u25B2" if delta > 0 else ("\u25BC" if delta < 0 else "\u2014")
                delta_color = FOREST if (improved or delta == 0) else "#B3261E"

                rcols = st.columns([3.2, 1.8, 1, 1, 1])
                rcols[0].markdown(f"<span style='font-size:0.85rem;color:{INK};'>{case_name}</span>", unsafe_allow_html=True)
                rcols[1].markdown(f"<span style='font-size:0.8rem;color:#6B6557;'>{dimension}</span>", unsafe_allow_html=True)
                rcols[2].markdown(f"<span style='font-size:0.85rem;color:#6B6557;'>{prev_score:.2f}</span>", unsafe_allow_html=True)
                rcols[3].markdown(
                    f"<span style='font-size:0.85rem;font-weight:700;color:{INK};'>{new_score:.2f}</span> "
                    f"<span style='font-size:0.75rem;color:{delta_color};'>{arrow}</span>",
                    unsafe_allow_html=True,
                )
                rcols[4].markdown(badge(result, rcolor), unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="product-card" style="margin-top:0.7rem;border-left:4px solid {color};padding:0.6rem 0.9rem;">
                    <strong style="color:{INK};">Regression note:</strong>
                    <span style="color:#6B6557;font-size:0.86rem;">{target['note']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open as governance finding →", key=f"eval_to_finding_{target['name']}"):
                st.session_state.findings_product_filter = target["linked_product"]
                st.session_state.page = "Findings"
                st.rerun()

    st.write("")
    st.info(
        "How this connects to governance: a Regression or Watch result here would feed into "
        "the product's runtime contract on the Assess page \u2014 e.g., a Regression on a "
        "production agent could trigger the same BLOCKED decision and escalation path as a "
        "High Risk governance score, even if the product's last full assessment was Low Risk."
    )


# ----------------------------------------------------------------------
# FINDINGS PAGE — Level 2: flattened control-level issues log across
# every product, the way a real risk/audit findings register works.
# ----------------------------------------------------------------------
def findings_page():
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Findings &amp; Issues Log</h1>
            <p>Every Not Met or Partial control across the portfolio, in one place \u2014 with
            severity, regulatory citation, accountable owner, and remediation target date.
            This is the audit trail underneath the risk scores: not just <em>that</em> a
            product is Moderate or High risk, but exactly <em>which controls</em> are driving
            that result.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    products = st.session_state.products
    findings = []
    for p in products:
        for m in MODULES:
            for qi, q in enumerate(m["questions"]):
                key = (m["title"], qi)
                if key not in p["answers"]:
                    continue
                score = p["answers"][key]
                status = control_status(score)
                if status in ("Not Met", "Partial"):
                    severity = q.get("severity", "Medium")
                    owner, target = _remediation_for(m["title"], qi, severity, q.get("owner_role"))
                    answer_label = next((label for label, s in q["opts"] if s == score), "—")
                    findings.append({
                        "product": p["name"],
                        "product_id": p["id"],
                        "module": m["title"],
                        "question": q["q"],
                        "severity": severity,
                        "status": status,
                        "score": score,
                        "citation": q.get("citation", ""),
                        "owner": owner,
                        "target": target,
                        "product_owner": p["owner_name"],
                        "answer": answer_label,
                    })

    if not findings:
        st.info("No findings yet — run assessments on the Assess page to populate this log.")
        return

    # Summary tiles by severity
    sev_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for f in findings:
        sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1

    tiles = [
        ("Critical", sev_counts["Critical"], "blocks promotion", "#B3261E"),
        ("High", sev_counts["High"], "urgent remediation", AMBER),
        ("Medium", sev_counts["Medium"], "tracked remediation", NAVY),
        ("Low", sev_counts["Low"], "monitor", "#6B7280"),
        ("Total Findings", len(findings), "across portfolio", FOREST),
    ]
    cols = st.columns(5)
    for col, (label, num, sub, color) in zip(cols, tiles):
        col.markdown(
            f"""
            <div class="metric-tile" style="--accent:{color}">
                <div class="num">{num}</div>
                <div class="label">{label}</div>
                <div class="sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Filters
    fcol1, fcol2, fcol3 = st.columns(3)
    sev_filter = fcol1.selectbox("Severity", ["All severities", "Critical", "High", "Medium", "Low"])
    product_names = ["All products"] + sorted({f["product"] for f in findings})
    preset_product = st.session_state.pop("findings_product_filter", None)
    default_idx = product_names.index(preset_product) if preset_product in product_names else 0
    product_filter = fcol2.selectbox("Product", product_names, index=default_idx)
    status_filter = fcol3.selectbox("Status", ["All statuses", "Not Met", "Partial"])

    filtered = findings
    if sev_filter != "All severities":
        filtered = [f for f in filtered if f["severity"] == sev_filter]
    if product_filter != "All products":
        filtered = [f for f in filtered if f["product"] == product_filter]
    if status_filter != "All statuses":
        filtered = [f for f in filtered if f["status"] == status_filter]

    # Sort: Critical first, then High, etc., Not Met before Partial
    sev_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    status_order = {"Not Met": 0, "Partial": 1}
    filtered.sort(key=lambda f: (sev_order.get(f["severity"], 9), status_order.get(f["status"], 9)))

    st.subheader(f"Findings — {len(filtered)} of {len(findings)}")

    for f in filtered:
        sev_color = SEVERITY_COLOR.get(f["severity"], "#6B7280")
        status_color = CONTROL_STATUS_COLOR.get(f["status"], "#6B7280")
        st.markdown(
            f'<div class="product-card" style="border-left:4px solid {sev_color};padding:0.7rem 1rem;margin-bottom:0.5rem;">'
            f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;align-items:flex-start;">'
            f'<div style="flex:1;min-width:240px;">'
            f'<div class="product-meta" style="margin-bottom:2px;">'
            f'<strong style="color:{INK};">{f["product"]}</strong> &nbsp;\u00b7&nbsp; {f["module"]}'
            f'</div>'
            f'<div style="font-size:0.88rem;color:{INK};margin-bottom:4px;">{f["question"]}</div>'
            f'<div style="font-size:0.74rem;color:#8A8475;">\u2693 {f["citation"]}</div>'
            f'<div style="font-size:0.78rem;color:{INK};margin-top:4px;"><strong>Answer:</strong> {f["answer"]}</div>'
            f'</div>'
            f'<div style="text-align:right;min-width:160px;">'
            f'{badge(f["severity"], sev_color)}&nbsp;{badge(f["status"], status_color)}'
            f'<div class="product-meta" style="margin-top:6px;">'
            f'Owner: {f["owner"]}<br>Target: {f["target"].strftime("%b %d, %Y")}'
            f'</div>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# ROADMAP PAGE
# ----------------------------------------------------------------------
def roadmap_page():
    library_subnav("Roadmap")
    st.markdown(
        """
        <div class="gov-hero">
            <h1>Product Roadmap</h1>
            <p>Planned evolution of the Command Centre from prototype to a production-grade
            governance platform — scaling across data, intelligence, and enterprise readiness.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Product KPIs — metrics OF the tool itself (adoption, effectiveness,
    # trust), distinct from the governance/risk metrics it produces about
    # the AI systems it tracks. Illustrative only: this prototype has no
    # persistence or event tracking yet, so these numbers are mocked to
    # show the shape of what real instrumentation would report.
    # ------------------------------------------------------------------
    st.markdown(
        f"""
        <div class="product-card" style="padding:0.8rem 1.1rem;margin-bottom:0.8rem;">
            <strong style="color:{INK};">Is the tool itself working?</strong>
            <span style="font-size:0.85rem;color:#6B6557;">
            The metrics above (risk scores, findings, overdue reviews) describe the AI systems
            being governed. The KPIs below would describe the Command Centre itself — adoption,
            effectiveness, and trust — once real usage tracking exists.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📐 Illustrative product KPIs (mocked — not yet tracked)", expanded=False):
        kcol1, kcol2, kcol3 = st.columns(3)
        with kcol1:
            st.markdown(f"<div style='font-weight:700;color:{NAVY};margin-bottom:0.4rem;'>ADOPTION</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{NAVY};font-size:1.5rem;">7 of 9</div>
                    <div class="product-meta">product owners have run at least one assessment</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{NAVY};font-size:1.5rem;">4.2 days</div>
                    <div class="product-meta">avg. time from registration to first assessment</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;">
                    <div class="score-num" style="color:{NAVY};font-size:1.5rem;">78%</div>
                    <div class="product-meta">of registered systems have a current (non-stale) assessment</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kcol2:
            st.markdown(f"<div style='font-weight:700;color:{FOREST};margin-bottom:0.4rem;'>EFFECTIVENESS</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{FOREST};font-size:1.5rem;">11 days</div>
                    <div class="product-meta">avg. time from Critical finding logged to remediated</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{FOREST};font-size:1.5rem;">64%</div>
                    <div class="product-meta">of findings closed before their target date</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;">
                    <div class="score-num" style="color:{AMBER};font-size:1.5rem;">2</div>
                    <div class="product-meta">findings that recurred across 2+ review cycles</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kcol3:
            st.markdown(f"<div style='font-weight:700;color:{AMBER};margin-bottom:0.4rem;'>TRUST & QUALITY</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{AMBER};font-size:1.5rem;">91%</div>
                    <div class="product-meta">of governance decisions followed without override</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;margin-bottom:0.5rem;">
                    <div class="score-num" style="color:{AMBER};font-size:1.5rem;">~18 min</div>
                    <div class="product-meta">avg. time to complete a full 37-question assessment</div>
                </div>
                <div class="product-card" style="padding:0.7rem 0.9rem;">
                    <div class="score-num" style="color:{AMBER};font-size:1.5rem;">3</div>
                    <div class="product-meta">severity caps challenged/corrected by a reviewer</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.caption(
            "These numbers are illustrative — this prototype doesn't yet persist usage events, "
            "override history, or remediation timestamps. Real tracking is scoped under "
            "**Q1 2027 — Operations** below."
        )

    st.write("")

    quarters = [
        {
            "title": "Q3 2026 — Foundations",
            "items": [
                ("Persistent storage (Supabase / Postgres)", "Planned"),
                ("Authentication & role-based access", "Planned"),
                ("Audit trail & versioned assessments", "Planned"),
            ],
        },
        {
            "title": "Q4 2026 — Intelligence",
            "items": [
                ("LLM-backed multi-agent scoring (live agents)", "Exploring"),
                ("Specialist agent rationale & citations per question", "Exploring"),
                ("Exportable PDF / Word assessment reports", "Planned"),
            ],
        },
        {
            "title": "Q1 2027 — Operations",
            "items": [
                ("Model inventory system integration", "Exploring"),
                ("Review-reminder & notification workflows", "Planned"),
                ("Product usage & effectiveness KPIs", "Planned"),
                ("Dashboard analytics: trends over time", "Exploring"),
            ],
        },
        {
            "title": "Q2 2027 — Enterprise Scale",
            "items": [
                ("Multi-tenant support across business lines", "Exploring"),
                ("Custom module / question libraries per regulator", "Exploring"),
                ("API access for upstream model registries", "Exploring"),
            ],
        },
    ]

    status_color = {"Planned": NAVY, "In Progress": FOREST, "Exploring": AMBER}

    cols = st.columns(4)
    for col, q in zip(cols, quarters):
        with col:
            cards_html = ""
            for item, status in q["items"]:
                c = status_color.get(status, NAVY)
                cards_html += f"""
                <div class="roadmap-card" style="border-left-color:{c};">
                    <div class="rt">{item}</div>
                    <div class="rd">{badge(status, c)}</div>
                </div>
                """
            st.markdown(
                f"""
                <div class="roadmap-col">
                    <h4>{q['title']}</h4>
                    {cards_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.info(
        "This roadmap reflects directional planning for scaling the prototype into a "
        "production governance platform and is subject to change based on regulatory "
        "priorities and stakeholder feedback."
    )


# ----------------------------------------------------------------------
# COMPARE PRODUCTS PAGE — side-by-side view of 2-3 selected products.
# Reuses existing scoring/severity/badge logic; no new data model needed.
# ----------------------------------------------------------------------
def compare_page():
    ids = st.session_state.compare_selection
    products = [p for p in st.session_state.products if p["id"] in ids]
    # Preserve selection order
    products.sort(key=lambda p: ids.index(p["id"]))

    hcol1, hcol2 = st.columns([5, 1.3])
    with hcol1:
        st.markdown(
            """
            <div class="gov-hero">
                <h1>Compare Products</h1>
                <p>Side-by-side governance posture for up to 3 selected AI systems —
                score, risk band, module breakdown, and the controls driving each result.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hcol2:
        st.write("")
        if st.button("← Back to Portfolio", key="cmp_back", use_container_width=True):
            st.session_state.page = "Portfolio"
            st.rerun()

    if len(products) < 2:
        st.info(
            "Select 2 or 3 products to compare from the Portfolio page's "
            "**Browse all products** section."
        )
        return

    n = len(products)
    cols = st.columns(n)

    # Header row: name, score, band per product
    for col, p in zip(cols, products):
        band = risk_band(p["score"])
        color = risk_color(band)
        score_text = f"{p['score']}/100" if p["score"] is not None else "—"
        with col:
            st.markdown(
                f'<div class="product-card" style="border-left:4px solid {color};">'
                f'<div class="product-name">{p["name"]}</div>'
                f'<div class="product-meta">{p["type"]}</div>'
                f'<div class="product-meta">{p["business_line"]} \u00b7 {p["stage"]}</div>'
                f'<div style="margin-top:0.6rem;">'
                f'<span class="score-num" style="color:{color};">{score_text}</span>'
                f'&nbsp;{badge(band, color)}'
                f'</div>'
                f'<div class="product-meta" style="margin-top:0.5rem;">'
                f'Owner: {p["owner_name"]}<br>Approver: {p.get("approver", "AI Governance Lead")}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if p["capped_by"]:
                st.caption(f"⚠️ Capped by {p['capped_by']['severity']} finding")

    st.write("")
    st.markdown("#### Module-by-module scores")

    for m in MODULES:
        mcols = st.columns([1.4] + [2] * n)
        mcols[0].markdown(f"<span style='font-weight:600;font-size:0.85rem;'>{m['title']}</span>", unsafe_allow_html=True)
        for col, p in zip(mcols[1:], products):
            m_scores = [p["answers"][(m["title"], qi)] for qi in range(len(m["questions"]))
                        if (m["title"], qi) in p["answers"]]
            if m_scores:
                m_avg = round(sum(m_scores) / len(m_scores))
                m_color = risk_color(risk_band(m_avg))
                col.markdown(
                    f'<div class="mscore-row"><div class="mscore-track" style="flex:1;">'
                    f'<div class="mscore-fill" style="width:{m_avg}%;background:{m_color};"></div></div>'
                    f'<div class="mscore-val" style="color:{m_color};">{m_avg}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                col.markdown("<span style='color:#8A8475;'>—</span>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### Critical & High findings")
    fcols = st.columns(n)
    for col, p in zip(fcols, products):
        crit_findings = []
        for m in MODULES:
            for qi, q in enumerate(m["questions"]):
                key = (m["title"], qi)
                if key not in p["answers"]:
                    continue
                status = control_status(p["answers"][key])
                sev = q.get("severity", "Medium")
                if status == "Not Met" and sev in ("Critical", "High"):
                    crit_findings.append((sev, q["q"]))
        crit_findings.sort(key=lambda x: 0 if x[0] == "Critical" else 1)
        with col:
            if not crit_findings:
                st.markdown("<span style='color:#6B6557;font-size:0.82rem;'>None</span>", unsafe_allow_html=True)
            else:
                for sev, qtext in crit_findings[:4]:
                    sc = SEVERITY_COLOR.get(sev, "#6B7280")
                    st.markdown(
                        f'<div style="border-left:3px solid {sc};padding-left:8px;margin-bottom:6px;font-size:0.78rem;">'
                        f'{badge(sev, sc)}<br>{qtext[:70]}{"..." if len(qtext) > 70 else ""}</div>',
                        unsafe_allow_html=True,
                    )
                if len(crit_findings) > 4:
                    st.caption(f"+{len(crit_findings) - 4} more — see Findings page")

    st.write("")
    if st.button("Clear selection", key="cmp_clear"):
        st.session_state.compare_selection = []
        st.session_state.page = "Portfolio"
        st.rerun()


# ----------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------
if st.session_state.page == "Portfolio":
    portfolio_page()
elif st.session_state.page == "Register Product":
    register_page()
elif st.session_state.page == "Assess":
    assess_page()
elif st.session_state.page == "Agent Evaluation":
    agent_eval_page()
elif st.session_state.page == "Findings":
    findings_page()
elif st.session_state.page == "Knowledge Base":
    knowledge_page()
elif st.session_state.page == "Roadmap":
    roadmap_page()
elif st.session_state.page == "Library":
    library_page()
elif st.session_state.page == "Compare":
    compare_page()

st.markdown("---")
st.caption("Prototype · For demonstration only · Not a substitute for formal regulatory advice.")

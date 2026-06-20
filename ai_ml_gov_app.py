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
                "citation": "Treasury Board Directive on ADM, s.6.3 (Impact Assessment)",
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
                "citation": "CLHIA AI Principles, Principle 3 (Fairness)",
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
                "citation": "Treasury Board Directive on ADM, s.6.2 (Transparency)",
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
                "citation": "Treasury Board Directive on ADM, s.6.4 (Human Intervention)",
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
                "citation": "Treasury Board Directive on ADM, s.6.1 (AIA Requirement)",
            },
            {
                "q": "Is there an appeal or recourse mechanism for individuals adversely affected by an AI-driven decision?",
                "opts": [
                    ("Yes — formal appeal process documented", 100),
                    ("Informal process exists", 50),
                    ("No", 0),
                    ("Not applicable", 70),
                ],
                "severity": "High",
                "citation": "CLHIA AI Principles, Principle 5 (Recourse)",
            },
        ],
    },
    {
        "title": "Model Risk",
        "ref": "OSFI Guideline E-23 — Model Risk Management",
        "desc": "Evaluates model validation, monitoring, documentation, and lifecycle controls.",
        "questions": [
            {"q": "Is the model independently validated prior to deployment?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23, Principle 4 (Independent Validation)"},
            {"q": "Is model performance monitored on an ongoing basis against defined thresholds?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI E-23, Principle 5 (Ongoing Monitoring)"},
            {"q": "Is there a documented model inventory entry with assigned owner and risk tier?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 2 (Model Inventory)"},
            {"q": "Has model drift or performance degradation been assessed within the past 12 months?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI E-23, Principle 5 (Ongoing Monitoring)"},
            {"q": "Are model assumptions and limitations documented for downstream users?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI E-23, Principle 3 (Documentation)"},
            {"q": "Is there a champion/challenger or back-testing process in place?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "OSFI E-23, Principle 4 (Independent Validation)"},
            {"q": "Is there a defined model retirement / decommissioning plan?", "opts": GENERIC_OPTS,
             "severity": "Low", "citation": "OSFI E-23, Principle 6 (Lifecycle Management)"},
        ],
    },
    {
        "title": "Privacy Risk",
        "ref": "PIPEDA; Quebec Law 25",
        "desc": "Evaluates personal data handling, consent, retention, and individual rights.",
        "questions": [
            {"q": "Has a Privacy Impact Assessment (PIA) been completed for this system?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "Quebec Law 25, s.3.3 (Mandatory PIA)"},
            {"q": "Is personal data collected and processed minimized to what is strictly necessary?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "PIPEDA, Principle 4.4 (Limiting Collection)"},
            {"q": "Is there a documented data retention and deletion policy applied to this system?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "PIPEDA, Principle 4.5 (Limiting Retention)"},
            {"q": "Can individuals request access, correction, or deletion of their data used by this system?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "PIPEDA, Principle 4.9 (Individual Access)"},
            {"q": "Is consent for use of personal data obtained and documented where required?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "PIPEDA, Principle 4.3 (Consent)"},
            {"q": "Have cross-border data transfers been assessed for PIPEDA / Law 25 compliance?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Quebec Law 25, s.17 (Cross-Border Transfer)"},
        ],
    },
    {
        "title": "Data Risk",
        "ref": "Internal Data Governance Standards",
        "desc": "Evaluates data quality, lineage, access controls, and representativeness.",
        "questions": [
            {"q": "Is data quality (completeness, accuracy, timeliness) actively monitored?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Internal Data Governance Standard, s.2 (Quality)"},
            {"q": "Is data lineage documented from source systems through to model input?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Internal Data Governance Standard, s.4 (Lineage)"},
            {"q": "Are data access controls role-based and reviewed periodically?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Internal Data Governance Standard, s.5 (Access Control)"},
            {"q": "Is the training data representative of the population the model serves?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "Internal Data Governance Standard, s.3 (Representativeness)"},
            {"q": "Is there a defined process for handling data quality incidents?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Internal Data Governance Standard, s.6 (Incident Handling)"},
            {"q": "Are third-party data sources assessed for quality, accuracy, and licensing?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Internal Data Governance Standard, s.7 (Third-Party Data)"},
        ],
    },
    {
        "title": "Cybersecurity Risk",
        "ref": "OSFI Cyber Security Self-Assessment",
        "desc": "Evaluates security controls, vendor assessments, and incident readiness.",
        "questions": [
            {"q": "Has a security review or threat model been completed for this system?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI Cyber Security Self-Assessment, s.1 (Threat Assessment)"},
            {"q": "Are model endpoints / APIs protected with authentication and rate limiting?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI Cyber Security Self-Assessment, s.3 (Access Control)"},
            {"q": "Is there monitoring for adversarial inputs or prompt injection attempts (where applicable)?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI Cyber Security Self-Assessment, s.4 (Threat Monitoring)"},
            {"q": "Are third-party AI vendors assessed via a security questionnaire (e.g., SOC 2)?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI Cyber Security Self-Assessment, s.6 (Third-Party Risk)"},
            {"q": "Is there an incident response plan that explicitly covers this AI system?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "OSFI Cyber Security Self-Assessment, s.7 (Incident Response)"},
            {"q": "Are model artifacts and associated data encrypted at rest and in transit?", "opts": GENERIC_OPTS,
             "severity": "Critical", "citation": "OSFI Cyber Security Self-Assessment, s.3 (Encryption)"},
        ],
    },
    {
        "title": "IT / Operational Risk",
        "ref": "Internal IT Operations Standards",
        "desc": "Evaluates operational resilience, support coverage, and change management.",
        "questions": [
            {"q": "Is there a defined SLA / uptime target for this system, and is it currently being met?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Internal IT Operations Standard, s.2 (Service Levels)"},
            {"q": "Is there a rollback or fallback plan if the AI system fails or underperforms?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Internal IT Operations Standard, s.5 (Resilience)"},
            {"q": "Is on-call or support coverage clearly defined for this system?", "opts": GENERIC_OPTS,
             "severity": "Low", "citation": "Internal IT Operations Standard, s.6 (Support Coverage)"},
            {"q": "Is there a change management process governing model and prompt updates?", "opts": GENERIC_OPTS,
             "severity": "High", "citation": "Internal IT Operations Standard, s.3 (Change Management)"},
            {"q": "Is operating cost / capacity monitored against budget?", "opts": GENERIC_OPTS,
             "severity": "Low", "citation": "Internal IT Operations Standard, s.4 (Capacity Management)"},
            {"q": "Is documentation (runbooks, architecture diagrams) current and accessible?", "opts": GENERIC_OPTS,
             "severity": "Medium", "citation": "Internal IT Operations Standard, s.7 (Documentation)"},
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


def _remediation_for(module_title, qi, severity):
    """Stock remediation text keyed loosely by severity, for Not Met /
    Partial controls — illustrative, would be entered by the control owner
    in a real workflow."""
    owners = ["Model Risk Team", "Privacy Office", "Data Governance Team",
              "Cyber Security Team", "Platform Engineering", "Product Owner"]
    import random
    seed_val = (abs(zlib_crc(module_title) ) + qi * 97) % 10000
    rng = random.Random(seed_val)
    owner = rng.choice(owners)
    if severity == "Critical":
        target_days = rng.choice([15, 20, 30])
    elif severity == "High":
        target_days = rng.choice([30, 45, 60])
    else:
        target_days = rng.choice([60, 90, 120])
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
        ("Group Benefits Pricing Agent", "Agentic / Multi-Agent System", "Group Benefits", "Ideation / Concept", 42),
        ("Voice-of-Customer NLP", "NLP / Text Analytics", "Customer Experience", "Production", 69),
        ("Vendor Risk Scoring Model", "ML Classification Model", "IT / Technology", "Proof of Concept (POC)", 77),
        ("Marketing Content Generator", "Generative AI (LLM)", "Customer Experience", "Pilot / Limited Deployment", 55),
        ("Customer Churn Predictor", "ML Regression Model", "Customer Experience", "Production", 81),
        ("Fraud Anomaly Detector", "Anomaly Detection", "Fraud & Risk", "Monitoring / Iteration", 64),
        ("Underwriting Decision Engine", "ML Classification Model", "Individual Insurance", "Production", 38),
        ("Advisor Knowledge Assistant", "Generative AI (LLM)", "Wealth Management", "Pilot / Limited Deployment", 72),
        ("Claims Summarization Copilot", "Generative AI (LLM)", "Group Benefits", "Production", 58),
    ]
    products = []
    today = date.today()
    review_offsets = [-12, 45, 120, 20, 160, -5, -30, 60, 15]  # negative = overdue
    for i, ((name, ptype, bline, stage, score), offset) in enumerate(zip(seed, review_offsets)):
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
            "owner_name": "Demo Owner",
            "owner_email": "demo.owner@example.com",
            "approver": "AI Governance Lead",
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

# ----------------------------------------------------------------------
# Top navigation bar
# ----------------------------------------------------------------------
PAGES = ["Portfolio", "Register Product", "Assess", "Agent Evaluation", "Findings", "Knowledge Base", "Roadmap"]

st.markdown(
    f"""
    <div class="top-nav">
        <div class="brand">\u25C6 AI & ML Governance Command Centre</div>
        {badge("Demo Mode", AMBER)}
    </div>
    """,
    unsafe_allow_html=True,
)

nav_cols = st.columns(len(PAGES))
for col, page_name in zip(nav_cols, PAGES):
    with col:
        is_active = st.session_state.page == page_name
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = page_name
            st.rerun()

# ----------------------------------------------------------------------
# PORTFOLIO PAGE
# ----------------------------------------------------------------------
def portfolio_page():
    st.markdown(
        """
        <div class="gov-hero">
            <h1>AI & ML Governance Portfolio</h1>
            <p>Multi-dimensional governance posture across every registered AI/ML system.
            Scores synthesized across six assessment modules against current OSFI, PIPEDA,
            Law 25, and Treasury Board guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    products = st.session_state.products
    total = len(products)
    high = sum(1 for p in products if risk_band(p["score"]) == "High Risk")
    moderate = sum(1 for p in products if risk_band(p["score"]) == "Moderate")
    low = sum(1 for p in products if risk_band(p["score"]) == "Low Risk")
    overdue = sum(1 for p in products if p["review_date"] and p["review_date"] < date.today())

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

    # Pending governance actions — evidence is only governance when a
    # defined action and accountable owner are attached.
    pending = []
    for p in products:
        band = risk_band(p["score"])
        if band == "High Risk":
            pending.append((p, f"BLOCKED — {RUNTIME_CONTRACTS['High Risk']['sla']}", "#B3261E"))
        elif p["review_date"] and p["review_date"] < date.today():
            days = (date.today() - p["review_date"]).days
            pending.append((p, f"Review overdue by {days} days — recertification required", AMBER))

    if pending:
        with st.expander(f"⚠️ Pending governance actions ({len(pending)})", expanded=True):
            for p, action_text, color in pending:
                crit_count = sum(
                    1 for m in MODULES for qi, q in enumerate(m["questions"])
                    if (m["title"], qi) in p["answers"]
                    and control_status(p["answers"][(m["title"], qi)]) == "Not Met"
                    and q.get("severity") == "Critical"
                )
                drill_note = (
                    f" &nbsp;{badge(f'{crit_count} Critical finding' + ('s' if crit_count != 1 else ''), '#B3261E')}"
                    if crit_count else ""
                )
                st.markdown(
                    f"""
                    <div class="product-card" style="border-left:4px solid {color};padding:0.7rem 1rem;">
                        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.4rem;">
                            <div>
                                <span class="product-name">{p['name']}</span>
                                <span class="product-meta" style="margin-left:0.5rem;">{action_text}</span>{drill_note}
                            </div>
                            <div class="product-meta">Owner: {p['owner_name']} · Approver: {p.get('approver', 'AI Governance Lead')}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.caption("See the **Findings** page for the full control-level breakdown behind every score.")

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

    st.markdown(
        '<div class="demo-notice">⚠️ Demo data — registrations and assessments are stored '
        'in this browser session only and reset on refresh.</div>',
        unsafe_allow_html=True,
    )

    st.subheader(f"Products — {len(filtered)} of {total} items")

    if not filtered:
        st.info("No products match the selected filters.")

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
                if st.button("Open assessment →", key=f"open_{p['id']}", use_container_width=True):
                    st.session_state.selected_product = p["id"]
                    st.session_state.page = "Assess"
                    st.rerun()


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
            <p>Run the six-module multi-agent assessment to generate a governance score
            and risk band for a registered AI/ML product.</p>
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
            cap_note_html = ""
            if capped:
                cap_note_html = f"""
                <div style="margin-top:0.5rem;padding:0.5rem 0.7rem;background:{RED}10;
                            border:1px solid {RED}40;border-radius:8px;font-size:0.82rem;color:{INK};">
                    <strong style="color:{RED};">Severity cap applied:</strong>
                    the average score was {avg_score}, but a <strong>{capped['severity']}</strong>
                    control was Not Met (\u201c{capped['question']}\u201d), so the band is capped at
                    <strong>{band}</strong> regardless of the average \u2014 one critical gap
                    can't be offset by passing minor controls.
                    <span style="color:#6B6557;">({capped['citation']})</span>
                </div>
                """

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
                    {cap_note_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Per-module agent score breakdown
            rows_html = ""
            for m in MODULES:
                m_scores = [answers[(m["title"], qi)] for qi in range(len(m["questions"]))
                            if (m["title"], qi) in answers]
                if m_scores:
                    m_avg = round(sum(m_scores) / len(m_scores))
                    m_color = risk_color(risk_band(m_avg))
                    rows_html += f"""
                    <div class="mscore-row">
                        <div class="mscore-label">{m['title']}</div>
                        <div class="mscore-track">
                            <div class="mscore-fill" style="width:{m_avg}%;background:{m_color};"></div>
                        </div>
                        <div class="mscore-val" style="color:{m_color};">{m_avg}</div>
                    </div>
                    """
                else:
                    rows_html += f"""
                    <div class="mscore-row">
                        <div class="mscore-label">{m['title']}</div>
                        <div class="mscore-track"></div>
                        <div class="mscore-val" style="color:#8A8475;">—</div>
                    </div>
                    """
            st.markdown(
                f"""
                <div class="product-card" style="margin-top:0.6rem;">
                    <div style="font-weight:700;margin-bottom:0.6rem;color:{INK};">
                        Module evidence breakdown
                    </div>
                    {rows_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

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
                rows_html += f"""
                <div style="display:flex;align-items:center;gap:0.8rem;padding:0.4rem 0;
                            border-bottom:1px solid #E5E0D5;">
                    <div style="width:110px;font-size:0.8rem;color:#6B6557;">{h['date'].strftime('%b %d, %Y')}</div>
                    <div style="width:60px;font-weight:700;color:{hcolor};">{h['score']}</div>
                    <div style="width:110px;">{badge(h['band'], hcolor)}</div>
                    <div style="width:80px;">{delta_html}</div>
                    <div style="font-size:0.78rem;color:#8A8475;">Reviewed by {h['reviewer']}</div>
                </div>
                """
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

    st.markdown(
        f"""
        <div class="product-card" style="padding:0.7rem 1rem;">
            <span style="font-weight:700;color:{INK};margin-right:0.8rem;">Control stack:</span>
            {badge("Evaluation — measures (Is this good?)", LAYER_COLORS['Evaluation'])}&nbsp;
            {badge("Guardrail — enforces (Is this allowed?)", LAYER_COLORS['Guardrail'])}&nbsp;
            {badge("Governance — decides (What happens next?)", LAYER_COLORS['Governance'])}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    # Render each module as an expander
    for i, m in enumerate(MODULES):
        n_answered = sum(1 for q in range(len(m["questions"])) if (m["title"], q) in answers)
        icon = "✅" if n_answered == len(m["questions"]) else ("🟡" if n_answered else "⬜")
        with st.expander(f"{icon} Module {i+1} · {m['title']}  —  {m['ref']}", expanded=(i == 0)):
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

                    st.markdown(
                        f"**{qi+1:02d}. {q['q']}** &nbsp;"
                        f"{badge(layer, lcolor)}&nbsp;{badge(severity, sev_color)}&nbsp;{badge(status, status_color)}",
                        unsafe_allow_html=True,
                    )
                    if q.get("citation"):
                        st.markdown(
                            f"<span style='font-size:0.74rem;color:#8A8475;'>\u2693 {q['citation']}</span>",
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

                    # Level 3 — remediation, shown only for controls that
                    # aren't fully Met
                    new_status = control_status(answers.get((m["title"], qi)))
                    if new_status in ("Not Met", "Partial"):
                        r_owner, r_date = _remediation_for(m["title"], qi, severity)
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
# KNOWLEDGE BASE PAGE
# ----------------------------------------------------------------------
def knowledge_page():
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
                    owner, target = _remediation_for(m["title"], qi, severity)
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
    product_filter = fcol2.selectbox("Product", product_names)
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
            f"""
            <div class="product-card" style="border-left:4px solid {sev_color};padding:0.7rem 1rem;margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;align-items:flex-start;">
                    <div style="flex:1;min-width:240px;">
                        <div class="product-meta" style="margin-bottom:2px;">
                            <strong style="color:{INK};">{f['product']}</strong> &nbsp;\u00b7&nbsp; {f['module']}
                        </div>
                        <div style="font-size:0.88rem;color:{INK};margin-bottom:4px;">{f['question']}</div>
                        <div style="font-size:0.74rem;color:#8A8475;">\u2693 {f['citation']}</div>
                    </div>
                    <div style="text-align:right;min-width:160px;">
                        {badge(f['severity'], sev_color)}&nbsp;{badge(f['status'], status_color)}
                        <div class="product-meta" style="margin-top:6px;">
                            Owner: {f['owner']}<br>Target: {f['target'].strftime('%b %d, %Y')}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# ROADMAP PAGE
# ----------------------------------------------------------------------
def roadmap_page():
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

st.markdown("---")
st.caption("Prototype · For demonstration only · Not a substitute for formal regulatory advice.")

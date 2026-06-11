"""
AI & ML Governance Command Centre — Streamlit recreation
Multi-dimensional governance posture across registered AI/ML systems.
Scores synthesized across six assessment modules aligned to OSFI, PIPEDA,
Law 25, and Treasury Board guidance.

Run with: streamlit run ai_ml_gov_app.py
"""

import uuid
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
            },
            {
                "q": "Has a bias assessment been conducted on the training data and model outputs against protected characteristics (race, sex, age, disability)?",
                "opts": [
                    ("Yes — fully documented and repeatable", 100),
                    ("In progress", 50),
                    ("No", 0),
                    ("Not applicable", 70),
                ],
            },
            {
                "q": "Can this system's decision be explained in plain language to the affected individual?",
                "opts": [
                    ("Yes — always, with documented explanation template", 100),
                    ("Yes — in most cases", 75),
                    ("Partially", 40),
                    ("No", 0),
                ],
            },
            {
                "q": "Is there a documented and tested human override mechanism for automated decisions?",
                "opts": [
                    ("Yes — documented and tested", 100),
                    ("Yes — exists but not documented", 60),
                    ("No", 0),
                    ("Not applicable — no automated decisions", 80),
                ],
            },
            {
                "q": "Has a formal Algorithmic Impact Assessment (AIA) been completed using a recognized framework?",
                "opts": [
                    ("Yes — Treasury Board AIA framework", 100),
                    ("Yes — internal AIA framework", 80),
                    ("No", 0),
                    ("Planned within 90 days", 50),
                ],
            },
            {
                "q": "Is there an appeal or recourse mechanism for individuals adversely affected by an AI-driven decision?",
                "opts": [
                    ("Yes — formal appeal process documented", 100),
                    ("Informal process exists", 50),
                    ("No", 0),
                    ("Not applicable", 70),
                ],
            },
        ],
    },
    {
        "title": "Model Risk",
        "ref": "OSFI Guideline E-23 — Model Risk Management",
        "desc": "Evaluates model validation, monitoring, documentation, and lifecycle controls.",
        "questions": [
            {"q": "Is the model independently validated prior to deployment?", "opts": GENERIC_OPTS},
            {"q": "Is model performance monitored on an ongoing basis against defined thresholds?", "opts": GENERIC_OPTS},
            {"q": "Is there a documented model inventory entry with assigned owner and risk tier?", "opts": GENERIC_OPTS},
            {"q": "Has model drift or performance degradation been assessed within the past 12 months?", "opts": GENERIC_OPTS},
            {"q": "Are model assumptions and limitations documented for downstream users?", "opts": GENERIC_OPTS},
            {"q": "Is there a champion/challenger or back-testing process in place?", "opts": GENERIC_OPTS},
            {"q": "Is there a defined model retirement / decommissioning plan?", "opts": GENERIC_OPTS},
        ],
    },
    {
        "title": "Privacy Risk",
        "ref": "PIPEDA; Quebec Law 25",
        "desc": "Evaluates personal data handling, consent, retention, and individual rights.",
        "questions": [
            {"q": "Has a Privacy Impact Assessment (PIA) been completed for this system?", "opts": GENERIC_OPTS},
            {"q": "Is personal data collected and processed minimized to what is strictly necessary?", "opts": GENERIC_OPTS},
            {"q": "Is there a documented data retention and deletion policy applied to this system?", "opts": GENERIC_OPTS},
            {"q": "Can individuals request access, correction, or deletion of their data used by this system?", "opts": GENERIC_OPTS},
            {"q": "Is consent for use of personal data obtained and documented where required?", "opts": GENERIC_OPTS},
            {"q": "Have cross-border data transfers been assessed for PIPEDA / Law 25 compliance?", "opts": GENERIC_OPTS},
        ],
    },
    {
        "title": "Data Risk",
        "ref": "Internal Data Governance Standards",
        "desc": "Evaluates data quality, lineage, access controls, and representativeness.",
        "questions": [
            {"q": "Is data quality (completeness, accuracy, timeliness) actively monitored?", "opts": GENERIC_OPTS},
            {"q": "Is data lineage documented from source systems through to model input?", "opts": GENERIC_OPTS},
            {"q": "Are data access controls role-based and reviewed periodically?", "opts": GENERIC_OPTS},
            {"q": "Is the training data representative of the population the model serves?", "opts": GENERIC_OPTS},
            {"q": "Is there a defined process for handling data quality incidents?", "opts": GENERIC_OPTS},
            {"q": "Are third-party data sources assessed for quality, accuracy, and licensing?", "opts": GENERIC_OPTS},
        ],
    },
    {
        "title": "Cybersecurity Risk",
        "ref": "OSFI Cyber Security Self-Assessment",
        "desc": "Evaluates security controls, vendor assessments, and incident readiness.",
        "questions": [
            {"q": "Has a security review or threat model been completed for this system?", "opts": GENERIC_OPTS},
            {"q": "Are model endpoints / APIs protected with authentication and rate limiting?", "opts": GENERIC_OPTS},
            {"q": "Is there monitoring for adversarial inputs or prompt injection attempts (where applicable)?", "opts": GENERIC_OPTS},
            {"q": "Are third-party AI vendors assessed via a security questionnaire (e.g., SOC 2)?", "opts": GENERIC_OPTS},
            {"q": "Is there an incident response plan that explicitly covers this AI system?", "opts": GENERIC_OPTS},
            {"q": "Are model artifacts and associated data encrypted at rest and in transit?", "opts": GENERIC_OPTS},
        ],
    },
    {
        "title": "IT / Operational Risk",
        "ref": "Internal IT Operations Standards",
        "desc": "Evaluates operational resilience, support coverage, and change management.",
        "questions": [
            {"q": "Is there a defined SLA / uptime target for this system, and is it currently being met?", "opts": GENERIC_OPTS},
            {"q": "Is there a rollback or fallback plan if the AI system fails or underperforms?", "opts": GENERIC_OPTS},
            {"q": "Is on-call or support coverage clearly defined for this system?", "opts": GENERIC_OPTS},
            {"q": "Is there a change management process governing model and prompt updates?", "opts": GENERIC_OPTS},
            {"q": "Is operating cost / capacity monitored against budget?", "opts": GENERIC_OPTS},
            {"q": "Is documentation (runbooks, architecture diagrams) current and accessible?", "opts": GENERIC_OPTS},
        ],
    },
]

TOTAL_QUESTIONS = sum(len(m["questions"]) for m in MODULES)

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
# Seed data — mirrors the original portfolio (9 products)
# ----------------------------------------------------------------------
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
    for name, ptype, bline, stage, score in seed:
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
            "review_date": None,
            "description": "Seed demo product — pre-loaded for portfolio illustration.",
            "answers": {},
            "score": score,
            "answered_count": TOTAL_QUESTIONS,  # treat seeds as fully assessed
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
PAGES = ["Portfolio", "Register Product", "Assess", "Knowledge Base", "Roadmap"]

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

    tiles = [
        ("Registered Products", total, "across all business lines", NAVY),
        ("High Risk", high, "requires remediation", "#B3261E"),
        ("Moderate Risk", moderate, "conditional approval", AMBER),
        ("Low Risk", low, "approved to proceed", FOREST),
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
                "review_date": review_date,
                "description": description,
                "answers": {},
                "score": None,
                "answered_count": 0,
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
    if pcol2.button("Run Multi-Agent Assessment →", type="primary", use_container_width=True):
        if answered_count == 0:
            st.warning("Answer at least one question before running the assessment.")
        else:
            total_score = sum(answers.values())
            avg_score = round(total_score / answered_count)
            product["score"] = avg_score
            product["answered_count"] = answered_count
            band = risk_band(avg_score)
            new_color = risk_color(band)
            st.markdown(
                f"""
                <div class="product-card" style="border-left:5px solid {new_color};">
                    <strong>Assessment complete</strong> — Score:
                    <span class="score-num" style="color:{new_color};">{avg_score}/100</span>
                    &nbsp; {badge(band, new_color)}
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
                        Specialist agent breakdown
                    </div>
                    {rows_html}
                </div>
                """,
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
                    st.markdown(f"**{qi+1:02d}. {q['q']}**")
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
elif st.session_state.page == "Knowledge Base":
    knowledge_page()
elif st.session_state.page == "Roadmap":
    roadmap_page()

st.markdown("---")
st.caption("Prototype · For demonstration only · Not a substitute for formal regulatory advice.")

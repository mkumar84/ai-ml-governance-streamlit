# AI & ML Governance Command Centre

A Streamlit-based governance platform for registering, assessing, and tracking AI/ML systems across six regulatory risk dimensions. Built for Canadian financial institutions operating under OSFI, PIPEDA, Quebec Law 25, and Treasury Board guidance.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

Most AI governance tools produce dashboards. This tool produces **governance decisions** — each score is bound to a named decision, accountable approver, escalation path, and SLA through a **runtime contract**. Evidence without action is not governance.

The platform covers six assessment modules aligned to real regulatory frameworks, with per-question controls tagged as Evaluation, Guardrail, or Governance layer.

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run ai_ml_gov_app.py
```

---

## Features

### Portfolio Dashboard
- Summary tiles: total registered products, High / Moderate / Low Risk counts, overdue reviews
- **Pending governance actions** panel — surfaces all High Risk and overdue-review products with owner and approver names
- Filter portfolio by risk band, business line, and deployment stage
- One-click navigation from any product card directly into its assessment

### Product Registration
- Capture product type, business line, deployment stage, data types, owner, approver, and review date
- Flags for customer-facing systems, automated decision-making, and third-party/vendor models
- These flags gate which assessment questions are shown downstream — a POC system does not answer production-only questions

### Six-Module Assessment Framework

| Module | Regulatory Reference | Key Controls |
|---|---|---|
| Algorithmic Impact | Treasury Board ADM; CLHIA AI Principles | Bias assessment, explainability, human override, AIA, recourse |
| Model Risk | OSFI Guideline E-23 | Independent validation, drift monitoring, inventory, lifecycle |
| Privacy Risk | PIPEDA; Quebec Law 25 | PIA, data minimisation, retention, individual rights, consent |
| Data Risk | Internal Data Governance Standards | Data quality, lineage, access controls, representativeness |
| Cybersecurity Risk | OSFI Cyber Security Self-Assessment | Threat modelling, API security, prompt injection, SOC 2, incident response |
| IT / Operational Risk | Internal IT Operations Standards | SLA, rollback, on-call, change management, cost monitoring |

Each question is tagged with its control layer:
- **Evaluation** — measures maturity (*Is this good?*)
- **Guardrail** — enforces a technical or process control (*Is this allowed?*)
- **Governance** — assigns accountability and triggers decisions (*What happens next?*)

### Runtime Contracts

A score alone is not governance. Every risk band maps to a **runtime contract**:

| Band | Decision | Approver | SLA | Review Cycle |
|---|---|---|---|---|
| High Risk (< 45) | BLOCKED from production | Model Risk Committee | Human review within 2 business days | 30 days |
| Moderate (45–74) | CONDITIONAL approval | AI Governance Lead | Remediation plan within 10 business days | 90 days |
| Low Risk (≥ 75) | APPROVED to proceed | Product Owner (self-attestation) | Periodic recertification | 180 days |

---

## Governance Enhancements

The following improvements were made to strengthen the assessment integrity and close governance loop-holes present in simpler scoring approaches.

### Scoring Integrity

**Floor Rule**
Any individual module averaging below 25/100 forces the overall risk band to **High Risk**, regardless of the overall average. A single severely non-compliant module cannot be diluted by strong performance elsewhere. The result card identifies which module triggered the floor.

**Partial vs. Complete Assessment Separation**
Running an assessment on partially answered questions produces a *Partial Assessment* preview — per-module scores are shown for informational purposes, but no governance decision, approver, SLA, or contract actions are issued. A formal governance decision is only produced when all applicable questions are answered.

**Question Gating by Product Profile**
Questions are conditionally shown based on the product's registered attributes:
- `automated_decisions` — human override and recourse questions only shown for systems making automated decisions
- `production` — drift assessment, champion/challenger, and retirement plan questions only shown for Production / Monitoring / Decommissioning stage systems
- `third_party` — vendor SOC 2, cross-border data transfer, and third-party data quality questions only shown for vendor-supplied models
- `genai` — adversarial input / prompt injection question only shown for Generative AI (LLM) and Agentic system types

**Seed Data with Real Answers**
The nine pre-loaded demo products are generated from realistic per-module answer distributions. Module evidence breakdowns are populated for all seed products — scores are not hardcoded.

### Response Quality Controls

**`Unsure` Rescored and Flagged**
The "Unsure" response option is scored at 15/100 (previously 50). Selecting it triggers an inline warning: *"Unsure indicates an unknown control state and is scored as high-risk. Clarify before final assessment."* Not knowing whether your system makes automated decisions is itself a High Risk finding.

**N/A Justification Required**
Selecting any "Not applicable" option reveals a mandatory justification text field. Without documented rationale, N/A responses are flagged as audit findings. Justifications are stored with the assessment record.

### Governance Logic

**Approver Override for High Risk**
For High Risk outcomes, the displayed approver is always the **Model Risk Committee** from the runtime contract — the product's registered approver is not used. A product owner cannot approve their own blocked system.

**Review Date Preserved on Re-runs**
Re-running an assessment no longer silently overwrites the review date. The review cycle only resets on: (a) the first assessment of a product, or (b) when the risk band changes between runs. Stable assessments retain their existing review date.

### UX & Workflow

**Product Profile Card on Assess Page**
Before any questions are shown, the Assess page displays the full product profile: type, business line, stage, automated decision flag, third-party flag, data types, owner, approver, and last assessed date. Users can verify they are assessing the right system before answering 37 questions.

**Auto-Save Indicator**
A *"✓ Answers auto-saved to session"* caption appears next to the progress bar. Answers are persisted to session state in real time as radio buttons are selected.

**Bottom Completion Prompt**
After all module expanders, a green banner appears when all applicable questions are answered, with a second "Run Assessment →" button at the bottom of the page. A count of remaining questions is shown when partially complete.

### Remediation Tracking

After a Moderate or High Risk assessment, contract actions are automatically added to the **Remediation Tracker** with owner, due date, and `Open` status. Users can:
- Toggle item status: Open → In Progress → Complete
- Add custom remediation items with owner and due date
- Track open item count at a glance

The tracker is always visible on the Assess page when items exist, regardless of whether an assessment has just been run.

### Assessment History & Versioning

Every completed assessment run is appended to a versioned history log stored with the product. Each entry records:
- Date, score, risk band
- Per-module scores
- Whether the floor rule was triggered and which module(s) caused it
- Answered / total applicable question counts
- Complete vs. partial flag

The Assessment History expander on the Assess page shows all prior runs in reverse chronological order with module-level score chips.

---

## Regulatory Framework References

| Framework | Scope |
|---|---|
| **Treasury Board Directive on ADM** | Federal AI system transparency, explainability, and AIA requirements |
| **CLHIA AI Principles** | Life and health insurance industry responsible AI guidance |
| **OSFI Guideline E-23** | Model risk management for federally regulated financial institutions |
| **PIPEDA** | Federal private-sector privacy law — consent, retention, individual rights |
| **Quebec Law 25** | Modernised provincial privacy law — PIA requirements, cross-border transfers |
| **OSFI Cyber Security Self-Assessment** | Cyber posture evaluation including third-party and incident response |

---

## Roadmap

| Quarter | Item | Status |
|---|---|---|
| Q3 2026 | Persistent storage (Supabase / Postgres) | Planned |
| Q3 2026 | Authentication & role-based access | Planned |
| Q3 2026 | Audit trail & versioned assessments | In Progress |
| Q3 2026 | Remediation item tracking | In Progress |
| Q4 2026 | LLM-backed multi-agent scoring | Exploring |
| Q4 2026 | Specialist agent rationale & citations per question | Exploring |
| Q4 2026 | Exportable PDF / Word assessment reports | Planned |
| Q1 2027 | Model inventory system integration | Exploring |
| Q1 2027 | Review-reminder & notification workflows | Planned |
| Q1 2027 | Dashboard analytics: trends over time | Exploring |
| Q2 2027 | Multi-tenant support across business lines | Exploring |
| Q2 2027 | Custom module / question libraries per regulator | Exploring |
| Q2 2027 | API access for upstream model registries | Exploring |

---

## Project Structure

```
ai_ml_gov_app.py    # Single-file Streamlit application
requirements.txt    # Python dependencies
```

---

## Requirements

```
streamlit>=1.32
```

---

## Disclaimer

This is a prototype for demonstration purposes only. It is not a substitute for formal regulatory advice, legal counsel, or a certified model risk management programme. Consult qualified compliance and legal professionals before relying on any outputs for regulatory submissions.

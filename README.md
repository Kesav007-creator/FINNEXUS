# FINNEXUS 🛡️
### Real-Time Fraud & AML Risk Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0%2B-orange.svg)](https://networkx.org)
[![FinTech Domain](https://img.shields.io/badge/FinTech-AML%20%26%20Fraud%20Orchestration-10B981.svg)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-gray.svg)](LICENSE)
[![Design](https://img.shields.io/badge/Aesthetic-NICE%20Actimize%20%7C%20Feedzai%20%7C%20Stripe-6366F1.svg)](https://github.com)

> **Next-generation enterprise anti-financial crime console.** FINNEXUS moves beyond isolated static rules by clustering fragmented suspicious transactions into **Unified Master Incidents**, detecting circular money-laundering rings using **Directed Graph algorithms**, generating **whitebox AI explanations**, and orchestrating **friction-reducing compliance decisions** in real-time.

---

## 📌 Executive Summary

Traditional Anti-Money Laundering (AML) and transaction monitoring systems bombard compliance teams with **thousands of disconnected alerts daily**, suffering from **>95% false-positive rates** and missing multi-hop laundering schemes. 

**FINNEXUS** reimagines financial crime defense with an enterprise-grade orchestration platform inspired by industry titans like **NICE Actimize (ActOne / AMLOCK)**, **Feedzai**, **Sardine**, and **Palantir Foundry**:

1. **Eliminates Alert Fatigue**: Aggregates multi-account scam rings and synthetic identity networks into **1 Scannable Master Incident Card** instead of spamming 5 separate alert rows.
2. **Exposes Hidden Money-Laundering Rings**: Runs dynamic directed graph cycle detection (`networkx.simple_cycles`) to instantly flag circular layering loops ($A \rightarrow B \rightarrow C \rightarrow D \rightarrow A$).
3. **Whitebox Explainability**: Replaces black-box scores with Feedzai-style 5-dot severity indicators (`●●●●●`), Sardine-style Z-score telemetry, and plain-English AI narrative directives.
4. **Friction-Reducing Orchestration**: Allows compliance analysts to execute 1-click actions (`Approve`, `Hold & Send Step-Up OTP`, `Freeze Account`) with automated Amazon-style tracking timelines and immutable audit logging.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph INGESTION["⚡ Real-Time Ingestion Engine"]
        T1["ACH / Wire / Card Streams"]
        T2["Device & Biometric Signals"]
        T3["Geo & Tor Network Data"]
    end

    subgraph CORE["🧠 FINNEXUS Orchestration Core"]
        direction TB
        MIA["Master Incident Aggregator<br/>(Node & Beneficiary Clustering)"]
        NX["NetworkX Graph Engine<br/>(Circular Loop & Cycle Detector)"]
        WBS["Feedzai Whitebox Engine<br/>(5-Dot Signal Weights)"]
        AIC["Autonomous AI Copilot<br/>(Natural Language SAR & Directives)"]
    end

    subgraph ACTIONS["🛡️ Compliance Actions & UI"]
        TIMELINE["Amazon Logistics Tracking Timeline<br/>[Received] ── [Scored] ── (Flagged) ── [Reviewed] ── [Action]"]
        ACTIONS_BTN["1-Click Remediation<br/>• Approve<br/>• Hold & Step-Up OTP<br/>• Freeze Account"]
        AUDIT["Immutable Audit Trail & FinCEN SAR Generator"]
    end

    INGESTION --> MIA
    MIA --> NX
    MIA --> WBS
    MIA --> AIC
    NX --> TIMELINE
    WBS --> TIMELINE
    AIC --> TIMELINE
    TIMELINE --> ACTIONS_BTN
    ACTIONS_BTN --> AUDIT
```

---

## ✨ Key Features & Modules

### 1. Master Incident Aggregation & Priority Feed
- Groups related transactions sharing device fingerprints, recipient IBANs, or Tor proxy nodes into **Unified Master Incidents**.
- Displays a high-contrast priority badge (`P1 - CRITICAL`, `P2 - HIGH`, `P3 - MEDIUM`), bold Risk Score (0–100 scale), total financial exposure, and plain-English trigger explanations.
- Dynamic multi-criteria sorter:
  - **Risk Score (Highest to Lowest)**
  - **Entities Involved (Largest Rings First)**
  - **Total Exposure ($ USD)**
  - **Newest Ingestion**

### 2. SVG Risk Speedometer Gauge & Amazon-Style Tracking Timeline
- **Live SVG Speedometer Gauge**: A custom semi-circular dial rendered directly in clean SVG with dynamic color interpolation (Green $\rightarrow$ Amber $\rightarrow$ Crimson) and a precision needle indicating exact threat level.
- **Logistics-Style Tracking Timeline**: Visual horizontal progression pipeline displaying the full lifecycle of an incident:
  $$\text{[Received]} \longrightarrow \text{[Scored]} \longrightarrow \text{(Flagged)} \longrightarrow \text{[Reviewed]} \longrightarrow \text{[Action Taken]}$$

### 3. NetworkX AML Circular Loop Detector (Killer USP)
- Constructs a directed graph (`networkx.DiGraph`) from real-time sender-receiver pairs.
- Executes `nx.simple_cycles()` dynamically to identify circular laundering topologies.
- Renders an interactive **Circular Layering Loop Banner** with exact connected paths:
  $$\text{Alice Vance} \longrightarrow \text{Bob Henderson} \longrightarrow \text{Charlie Zhang} \longrightarrow \text{Diana Prince} \longrightarrow \text{Alice Vance}$$
- Interactive SVG **Genome Network Visualizer** rendering nodes, directional links, and circular velocity metrics.

### 4. Deep Entity Dossier ("More details" View)
Expanding any incident reveals a comprehensive investigative case dossier:
- **Full Involved Entity Roster**: Detailed account cards for **every single party involved** (KYC verification tier, account role, device hardware token, registered geolocation, and IP proxy status).
- **Autonomous AI Investigator Analysis**: Structured recommendations advising exact compliance actions to minimize customer friction while containing exposure.
- **Feedzai Whitebox Explainability**: 5-dot severity indicators (`●●●●●`) breaking down individual sub-signals (Velocity Anomalies, Rapid Succession, Cross-Border Jumps).
- **NICE Actimize Cross-Channel Matrix**: Risk correlations across Wire, ACH, ATM, and Tor Exit Nodes.
- **Granular Transaction Ledger**: Complete historical payment list with timestamps, amounts, and rails.

### 5. Stationary Intelligence Panel & FINNEXUS AI Copilot
- As investigators scroll through the alerts feed on the left, the right-hand analytical column remains **anchored and stationary**.
- Features an embedded **AI Compliance Copilot Chatbot** capable of:
  - Answering natural language inquiries about active laundering rings.
  - Explaining structuring techniques (smurfing, layering, integration).
  - Drafting regulatory narrative summaries ready for FinCEN SAR filings.
- Floating bottom-right assistant launcher for instant access anywhere on the dashboard.

### 6. One-Click Orchestration & Immutable Audit Log
- **Approve (Friction-Free)**: Clears false positives instantly.
- **Hold & Send Step-Up OTP (Friction-Reduction)**: Employs risk-based authentication to verify legitimate users without frustrating account lockouts.
- **Freeze Account (Critical Defense)**: Instantly isolates compromised accounts and halts pending transactions.
- All actions are permanently written to an **Immutable Audit Log** recording exact timestamps, analyst IDs, incident numbers, and administrative rationale.

### 7. Multi-Tab Compliance Suite
- 🚨 **Alert & Incident Orchestrator**: The primary real-time detection and action feed.
- 📊 **Executive Dashboard**: High-level telemetry (94.2% precision, 1.4% false-positive rate, 38ms latency, risk distributions).
- 📁 **Case Management (ActOne style)**: Deep dive workflow tool for compliance supervisors.
- 📑 **FinCEN SAR Filings**: Auto-populated Suspicious Activity Report drafts ready for regulatory submission.

---

## 🚀 Quick Start (Running Locally)

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/finnexus.git
cd finnexus
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch FINNEXUS
```bash
streamlit run app.py
```
FINNEXUS will open automatically in your browser at `http://localhost:8501`.

---

## ⚡ 1-Click Launchers (No Terminal Needed)

- **Windows Users**: Simply double-click [`run.bat`](run.bat). It automatically checks dependencies and opens the console in your browser.
- **macOS / Linux Users**: Make executable and run [`run.sh`](run.sh):
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

---

## 📂 Repository Structure

```
finnexus/
├── .streamlit/
│   └── config.toml          # Enforces crisp light theme (#F8F9FA, #FFFFFF, #0F172A)
├── .gitignore               # Clean git exclusions for Python/Streamlit
├── app.py                   # Self-contained enterprise orchestration platform (single-file architecture)
├── requirements.txt         # Core dependencies (streamlit, pandas, networkx)
├── run.bat                  # 1-click launcher for Windows
├── run.sh                   # 1-click launcher for macOS/Linux
└── README.md                # Comprehensive documentation
```

---

## 🧪 Demonstration Walkthrough (Hackathon Script)

When presenting FINNEXUS to judges, follow this 3-step walkthrough:

1. **Show the Master Incident Feed (0:00 - 0:45)**:
   - Highlight Incident `INC-9042` with its **96 Risk Score Speedometer** and **Amazon tracking timeline**.
   - Explain how 4 related suspicious transactions across different users were clustered into 1 case instead of 4 spam alerts.
2. **Trigger Circular Loop Detection (0:45 - 1:30)**:
   - Point to the **NetworkX Circular Layering Banner** showing the exact ring path ($A \rightarrow B \rightarrow C \rightarrow D \rightarrow A$).
   - Show the dynamic **Genome Graph Visualizer** displaying the circular money flow.
3. **Deep Entity Inspection & One-Click Remediation (1:30 - 2:30)**:
   - Click **"More details"** to reveal all 4 involved account dossiers, Feedzai 5-dot whitebox scores, and AI Investigator Directives.
   - Click **"Hold & Send Step-Up OTP"** or **"Freeze Account"** — watch the tracking timeline update and verify the entry in the **Immutable Audit Trail**.
   - Show the stationary **AI Copilot** answering compliance inquiries on the fly.

---

## 🗺️ Production Scaling Roadmap

| Component | Prototype Implementation | Production Target |
|---|---|---|
| **Event Streaming** | In-Memory Session Queue | Apache Kafka / AWS Kinesis (100k+ events/sec) |
| **Graph Database** | NetworkX in-memory graph | Neo4j / Amazon Neptune distributed graph cluster |
| **Feature Store** | Pandas DataFrames | Feast / Redis low-latency feature cache |
| **LLM Copilot** | Deterministic AML heuristics | Fine-tuned Fin-LLM via Anthropic Claude / Gemini API |
| **Regulatory Filing** | Markdown SAR generator | FinCEN BSA E-Filing System REST API |

---

## 👥 Authors & Acknowledgments

- Built with ❤️ for the FinTech Real-Time Fraud & AML Risk Orchestration Challenge.
- Design inspired by the world-class interfaces of **NICE Actimize**, **Feedzai**, **Sardine**, **Stripe**, and **Palantir Foundry**.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

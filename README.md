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

Traditional Anti-Money Laundering (AML) and transaction monitoring systems bombard compliance teams with thousands of disconnected alerts daily, suffering from **>95% false-positive rates** and missing multi-hop laundering schemes. 

**FINNEXUS** reimagines financial crime defense with an enterprise-grade orchestration platform inspired by industry titans like **NICE Actimize (ActOne / AMLOCK)**, **Feedzai**, **Sardine**, and **Palantir Foundry**:

1. **Eliminates Alert Fatigue**: Aggregates multi-account scam rings into **1 Scannable Master Incident Card** instead of spamming 5 separate alert rows.
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

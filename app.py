"""
FINNEXUS — Enterprise Real-Time Fraud & AML Risk Orchestration Platform
Designed for high-stakes FinTech compliance and hackathon demonstration.

Features:
- Exact Alert Card presentation matching User Mockup (Image 2):
  * Header banner with Priority pill, plain-English summary, and bold risk score
  * Sub-header metadata row (Incident ID, Cluster Value, Entities, Channel, Status)
  * Flow breadcrumb, Amazon-style tracking timeline, compliance action buttons
  * Native SVG Risk Rating Score Meter (Semi-Circular Speedometer Gauge with needle)
  * "More details" interactive expander containing:
    - Key account details for ALL participants involved (every account in cluster)
    - AI Investigator Analysis with friction-reduction guidance
    - Whitebox Explanations with Feedzai 5-dot severity indicators
    - NICE Actimize Cross-Channel Risk Correlations
    - Complete transaction ledger
- Multi-criteria filtering toolbar (Highest to Lowest score, Most people involved, etc.)
- Zero raw code leakage: all custom HTML passed through string-flattening clean_html()
- Stationary / Sticky Right-Hand Panel (stays fixed during scroll matching Image 4)
- Interactive AI Compliance Copilot Chatbot in the right panel (Image 2)
- Floating Chatbot Popover in bottom-right corner for quick access
- Full multi-tab navigation (Alert Orchestrator, Executive Dashboard, Case Management, FinCEN SAR)
"""

import streamlit as st
import pandas as pd
import networkx as nx
import random
import math
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FINNEXUS · Enterprise Fraud & AML Orchestration",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def clean_html(html_str: str) -> str:
    """
    Strips all leading/trailing whitespace and removes newlines.
    Prevents CommonMark from converting indented HTML into Markdown code blocks.
    """
    return "".join(line.strip() for line in html_str.splitlines() if line.strip())

def render_html(html_str: str):
    """Renders HTML guaranteed safe against Markdown code block conversion."""
    st.markdown(clean_html(html_str), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. HIGH-CONTRAST ENTERPRISE CSS & STICKY PANEL STYLING
# ═══════════════════════════════════════════════════════════════════════════════
render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Global Font & Canvas */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #F8F9FA !important;
    color: #0F172A !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
.block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1480px !important;
}

/* Force dark legible text on all Streamlit widgets (Fixes Image 3 & 4 issue) */
div[data-testid="stMetricValue"] * {
    color: #0F172A !important;
    font-weight: 800 !important;
}
div[data-testid="stMetricLabel"] * {
    color: #475569 !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
div[data-testid="stMetricDelta"] * {
    font-weight: 700 !important;
}
div[data-testid="stWidgetLabel"] * {
    color: #1E293B !important;
    font-weight: 700 !important;
}
p, span, div, h1, h2, h3, h4, label {
    color: #0F172A;
}

/* Top Navigation Radio Tabs (High Visibility) */
div[role="radiogroup"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 6px 12px !important;
    gap: 10px !important;
    display: flex !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    margin-bottom: 14px !important;
}
div[role="radiogroup"] label {
    background: #F1F5F9 !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    color: #1E293B !important;
    border: 1px solid #E2E8F0 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
div[role="radiogroup"] label:hover {
    background: #E2E8F0 !important;
}
div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] label:has(input:checked) {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border-color: #1D4ED8 !important;
}
div[role="radiogroup"] label span p {
    color: inherit !important;
    font-weight: 700 !important;
}

/* FINNEXUS Command Header */
.sf-banner {
    background: linear-gradient(135deg, #0B132B 0%, #172554 100%);
    border-radius: 12px;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(11, 19, 43, 0.15);
}
.sf-brand-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.sf-logo {
    background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
    color: #FFFFFF;
    font-weight: 800;
    font-size: 16px;
    width: 38px;
    height: 38px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
}
.sf-title {
    font-size: 20px;
    font-weight: 800;
    color: #FFFFFF !important;
    letter-spacing: 1.2px;
    line-height: 1.1;
}
.sf-subtitle {
    font-size: 11px;
    color: #94A3B8 !important;
    font-weight: 500;
}
.sf-status-pill {
    background: #0F172A;
    border: 1px solid #334155;
    color: #E2E8F0 !important;
    font-size: 11px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.live-dot {
    width: 8px;
    height: 8px;
    background: #10B981;
    border-radius: 50%;
    animation: live-pulse 2s infinite;
}
@keyframes live-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
    50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
}

/* Metrics Top Cards */
.metric-box {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.metric-box.m-blue::before { background: #3B82F6; }
.metric-box.m-red::before { background: #EF4444; }
.metric-box.m-green::before { background: #10B981; }
.metric-box.m-purple::before { background: #8B5CF6; }

.m-lbl {
    font-size: 10.5px;
    font-weight: 700;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
}
.m-val {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A !important;
    line-height: 1.1;
}
.m-sub {
    font-size: 11px;
    font-weight: 600;
    margin-top: 3px;
}
.sub-green { color: #059669 !important; }
.sub-red { color: #DC2626 !important; }

/* Telemetry Performance Row */
.telemetry-row {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 10px 0 16px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    flex-wrap: wrap;
    gap: 10px;
}
.tele-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 700;
}
.tag-green { background: #ECFDF5; color: #065F46 !important; border: 1px solid #A7F3D0; }
.tag-amber { background: #FFFBEB; color: #92400E !important; border: 1px solid #FDE68A; }
.tag-blue  { background: #EFF6FF; color: #1E40AF !important; border: 1px solid #BFDBFE; }

/* ── EXACT USER ALERT CARD DESIGN (Image 2 Mockup) ── */
.alert-card {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* 1. Header Banner */
.card-header-banner {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-left: 6px solid #EA580C;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}
.header-badge-p1 {
    background: #EA580C;
    color: #FFFFFF !important;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
}
.header-badge-p2 {
    background: #F97316;
    color: #FFFFFF !important;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
}
.header-badge-p3 {
    background: #EAB308;
    color: #FFFFFF !important;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
}
.banner-summary-text {
    font-size: 13.5px;
    font-weight: 700;
    color: #9A3412 !important;
    margin: 0 16px;
    flex: 1;
    line-height: 1.4;
}
.banner-score-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 800;
    color: #DC2626 !important;
    line-height: 1;
    min-width: 45px;
    text-align: right;
}

/* 2. Sub-header Metadata Row */
.card-meta-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 24px;
    padding: 8px 0 14px 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 14px;
}
.meta-block {
    display: flex;
    flex-direction: column;
}
.meta-lbl {
    font-size: 10px;
    font-weight: 800;
    color: #64748B !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
}
.meta-val-text {
    font-size: 13.5px;
    font-weight: 700;
    color: #0F172A !important;
}
.meta-val-blue {
    font-size: 13.5px;
    font-weight: 800;
    color: #2563EB !important;
}
.meta-val-green {
    font-size: 13.5px;
    font-weight: 800;
    color: #059669 !important;
}
.meta-val-red {
    font-size: 13.5px;
    font-weight: 800;
    color: #DC2626 !important;
}

/* 3. Mid Section */
.card-flow-header {
    font-size: 12px;
    font-weight: 600;
    color: #475569 !important;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

/* Whitebox Panel */
.wb-box {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.wb-hdr {
    font-size: 12px;
    font-weight: 700;
    color: #1E293B !important;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #F1F5F9;
}
.wb-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px dashed #F8FAFC;
    font-size: 11.5px;
    color: #334155 !important;
}
.dots-group {
    display: flex;
    gap: 3px;
    margin-left: 10px;
}
.d-circle {
    width: 7px;
    height: 7px;
    border-radius: 50%;
}
.d-red { background: #EF4444; }
.d-orange { background: #F97316; }
.d-amber { background: #F59E0B; }
.d-gray { background: #CBD5E1; }

/* NICE Actimize Cross-Channel Grid */
.cc-container {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.cc-pill {
    display: block;
    background: #FEE2E2;
    color: #991B1B !important;
    border: 1px solid #FECACA;
    font-size: 10.5px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 4px;
}
.cc-pill-warn {
    background: #FEF3C7;
    color: #92400E !important;
    border-color: #FDE68A;
}

/* Module D: AI Recommendation Card */
.ai-card {
    background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
    border: 1px solid #A7F3D0;
    border-left: 4px solid #059669;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.ai-hdr {
    font-size: 12.5px;
    font-weight: 700;
    color: #065F46 !important;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.ai-body {
    font-size: 11.5px;
    color: #1F2937 !important;
    line-height: 1.55;
    font-weight: 500;
}
.ai-action-chip {
    background: #FFFFFF;
    border: 1px solid #6EE7B7;
    border-radius: 6px;
    padding: 6px 10px;
    margin-top: 8px;
    font-size: 11px;
    font-weight: 700;
    color: #047857 !important;
}

/* Module C: AML Ring Killer Banner */
.aml-banner {
    background: linear-gradient(135deg, #450A0A 0%, #7F1D1D 100%);
    color: #FFFFFF !important;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 14px;
    border: 1px solid #991B1B;
    box-shadow: 0 4px 12px rgba(127, 29, 29, 0.2);
}
.aml-route-box {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(254, 202, 202, 0.25);
    border-radius: 6px;
    padding: 8px 12px;
    margin-top: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    color: #FCA5A5 !important;
    word-break: break-all;
}

/* ── REQUIREMENT 3: STATIONARY / STICKY RIGHT COLUMN ── */
div[data-testid="column"]:nth-of-type(2) {
    position: sticky !important;
    top: 14px !important;
    align-self: flex-start !important;
    max-height: calc(100vh - 28px) !important;
    overflow-y: auto !important;
    padding-right: 6px !important;
}
div[data-testid="column"]:nth-of-type(2)::-webkit-scrollbar {
    width: 5px;
}
div[data-testid="column"]:nth-of-type(2)::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 4px;
}

/* Right Panel Chatbot Styling */
.copilot-container {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
    padding: 14px;
    margin-top: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}
.chat-msg-user {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 12px;
    font-weight: 600;
    color: #1E3A8A !important;
}
.chat-msg-ai {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 12px;
    color: #1E293B !important;
    line-height: 1.5;
}

/* Button Styling */
.stButton button {
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
}
</style>
""")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. DOMAIN DATA MODELS & BENCHMARK INCIDENTS
# ═══════════════════════════════════════════════════════════════════════════════
def build_initial_dataset():
    """Generates realistic FinTech transactions forming suspicious clusters."""
    now = datetime.now()
    return [
        # Cluster 1: Multi-Account Circular AML Ring (Alice -> Bob -> Charlie -> Diana -> Alice)
        {
            "txn_id": "TXN-88401-A",
            "sender": "Alice Whitmore", "sender_acct": "US-ACH-4001928", "sender_kyc": "Tier-2 Verified",
            "receiver": "Bob Nakamura", "receiver_acct": "UK-FPS-5192004", "receiver_kyc": "Tier-1 Basic",
            "amount": 49500.00, "currency": "USD", "channel": "Cross-Border Wire",
            "device_fp": "FP-9021-SAFARI", "device_type": "macOS 14 · Safari 17.2",
            "geo": "New York, USA", "ip": "199.167.211.4",
            "timestamp": (now - timedelta(seconds=115)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 98, "risk_level": "CRITICAL",
            "signals": [
                ("Circular layering: transaction routes return to origin within 120s", 5, "AML Graph"),
                ("Amount is 8.4x higher than sender's 90-day moving average", 5, "Behavioral"),
                ("High-velocity international correspondent routing", 4, "Wire"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-88401-B",
            "sender": "Bob Nakamura", "sender_acct": "UK-FPS-5192004", "sender_kyc": "Tier-1 Basic",
            "receiver": "Charlie Okafor", "receiver_acct": "SG-FAST-882019", "receiver_kyc": "Tier-1 Basic",
            "amount": 48600.00, "currency": "USD", "channel": "Cross-Border Wire",
            "device_fp": "FP-4412-CHROME", "device_type": "Win 11 · Chrome 121",
            "geo": "London, UK", "ip": "82.165.197.1",
            "timestamp": (now - timedelta(seconds=92)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 94, "risk_level": "CRITICAL",
            "signals": [
                ("Intermediate node in active circular layering cycle", 5, "AML Graph"),
                ("1.8% value decay consistent with mule commission slicing", 4, "Structuring"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-88401-C",
            "sender": "Charlie Okafor", "sender_acct": "SG-FAST-882019", "sender_kyc": "Tier-1 Basic",
            "receiver": "Diana Petrova", "receiver_acct": "AE-WPS-330198", "receiver_kyc": "Unverified",
            "amount": 47900.00, "currency": "USD", "channel": "Cross-Border Wire",
            "device_fp": "FP-8891-BRAVE", "device_type": "Android 14 · Brave",
            "geo": "Singapore, SG", "ip": "103.252.115.8",
            "timestamp": (now - timedelta(seconds=64)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 93, "risk_level": "CRITICAL",
            "signals": [
                ("Device fingerprint FP-8891-BRAVE shared with destination account holder", 5, "Device"),
                ("Rapid hop: funds settled and re-transmitted in under 28 seconds", 5, "Velocity"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-88401-D",
            "sender": "Diana Petrova", "sender_acct": "AE-WPS-330198", "sender_kyc": "Unverified",
            "receiver": "Alice Whitmore", "receiver_acct": "US-ACH-4001928", "receiver_kyc": "Tier-2 Verified",
            "amount": 47100.00, "currency": "USD", "channel": "Cross-Border Wire",
            "device_fp": "FP-8891-BRAVE", "device_type": "Android 14 · Brave",
            "geo": "Dubai, UAE", "ip": "103.252.115.8",
            "timestamp": (now - timedelta(seconds=18)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 98, "risk_level": "CRITICAL",
            "signals": [
                ("LOOP CLOSURE: Funds return to origin account (Alice Whitmore)", 5, "AML Graph"),
                ("Device fingerprint & IP match Charlie Okafor (Ring Controller)", 5, "Device"),
                ("Transited 4 regulatory jurisdictions in under 120 seconds", 5, "Jurisdiction"),
            ],
            "stage": 2, "status": "FLAGGED",
        },

        # Cluster 2: Structured Fan-Out / Smurfing (Ethan Walsh to 3 accounts under $10k)
        {
            "txn_id": "TXN-66102-A",
            "sender": "Ethan Walsh", "sender_acct": "US-CHASE-11082", "sender_kyc": "Tier-2 Verified",
            "receiver": "Fiona Delacroix", "receiver_acct": "CA-TD-220199", "receiver_kyc": "Tier-1 Basic",
            "amount": 9850.00, "currency": "USD", "channel": "ACH Transfer",
            "device_fp": "FP-2240-IOS", "device_type": "iPhone 15 Pro · Safari",
            "geo": "Toronto, CA", "ip": "198.51.100.22",
            "timestamp": (now - timedelta(seconds=290)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 84, "risk_level": "HIGH",
            "signals": [
                ("Transfer amount ($9,850) positioned just beneath $10,000 CTR reporting threshold", 4, "Structuring"),
                ("Consecutive batch transfer #1 of 3", 3, "Velocity"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-66102-B",
            "sender": "Ethan Walsh", "sender_acct": "US-CHASE-11082", "sender_kyc": "Tier-2 Verified",
            "receiver": "George Tanaka", "receiver_acct": "CA-RBC-330198", "receiver_kyc": "Tier-1 Basic",
            "amount": 9700.00, "currency": "USD", "channel": "ACH Transfer",
            "device_fp": "FP-2240-IOS", "device_type": "iPhone 15 Pro · Safari",
            "geo": "Toronto, CA", "ip": "198.51.100.22",
            "timestamp": (now - timedelta(seconds=275)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 83, "risk_level": "HIGH",
            "signals": [
                ("Transfer amount ($9,700) deliberately avoids automated BSA CTR threshold", 4, "Structuring"),
                ("Identical IP and session cookie to preceding outbound transfer", 4, "Device"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-66102-C",
            "sender": "Ethan Walsh", "sender_acct": "US-CHASE-11082", "sender_kyc": "Tier-2 Verified",
            "receiver": "Hannah Morales", "receiver_acct": "CA-BMO-440239", "receiver_kyc": "Tier-1 Basic",
            "amount": 9920.00, "currency": "USD", "channel": "ACH Transfer",
            "device_fp": "FP-2240-IOS", "device_type": "iPhone 15 Pro · Safari",
            "geo": "Toronto, CA", "ip": "198.51.100.22",
            "timestamp": (now - timedelta(seconds=250)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 86, "risk_level": "HIGH",
            "signals": [
                ("Cumulative structuring amount: $29,470 dispersed across 3 recipients in 40s", 5, "Structuring"),
                ("First-time interaction between sender and all 3 recipients", 4, "Behavioral"),
            ],
            "stage": 2, "status": "FLAGGED",
        },

        # Cluster 3: Shared Device Collision (Ivan Kruger & Kiran Patel to Jasmine Rao)
        {
            "txn_id": "TXN-55201-A",
            "sender": "Ivan Kruger", "sender_acct": "DE-DB-990182", "sender_kyc": "Tier-2 Verified",
            "receiver": "Jasmine Rao", "receiver_acct": "IN-HDFC-660192", "receiver_kyc": "Tier-1 Basic",
            "amount": 22400.00, "currency": "EUR", "channel": "SEPA Instant",
            "device_fp": "FP-7712-SAMSUNG", "device_type": "Galaxy S24 · Chrome",
            "geo": "Frankfurt, DE", "ip": "85.214.132.55",
            "timestamp": (now - timedelta(seconds=480)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 79, "risk_level": "HIGH",
            "signals": [
                ("Physical hardware hash FP-7712 associated with multiple KYC profiles", 5, "Device"),
                ("Sudden high-velocity outflow on dormant account (180 days idle)", 4, "Behavioral"),
            ],
            "stage": 2, "status": "FLAGGED",
        },
        {
            "txn_id": "TXN-55201-B",
            "sender": "Kiran Patel", "sender_acct": "DE-COMM-881290", "sender_kyc": "Tier-1 Basic",
            "receiver": "Jasmine Rao", "receiver_acct": "IN-HDFC-660192", "receiver_kyc": "Tier-1 Basic",
            "amount": 19800.00, "currency": "EUR", "channel": "SEPA Instant",
            "device_fp": "FP-7712-SAMSUNG", "device_type": "Galaxy S24 · Chrome",
            "geo": "Frankfurt, DE", "ip": "85.214.132.55",
            "timestamp": (now - timedelta(seconds=450)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 81, "risk_level": "HIGH",
            "signals": [
                ("Device FP-7712 fingerprint collision with Ivan Kruger (Mule Aggregator)", 5, "Device"),
                ("Convergent flow into single beneficiary Jasmine Rao", 4, "Beneficiary"),
            ],
            "stage": 2, "status": "FLAGGED",
        },

        # Cluster 4: Travel Anomaly (Candidate for OTP Step-up friction reduction)
        {
            "txn_id": "TXN-33019-A",
            "sender": "Liam Johansson", "sender_acct": "SE-SEB-110992", "sender_kyc": "Tier-2 Verified",
            "receiver": "Mei-Lin Chen", "receiver_acct": "SG-DBS-882011", "receiver_kyc": "Merchant Verified",
            "amount": 2850.00, "currency": "USD", "channel": "Debit Card Online",
            "device_fp": "FP-3310-IPAD", "device_type": "iPadOS 17 · Safari",
            "geo": "Stockholm, SE", "ip": "194.236.10.88",
            "timestamp": (now - timedelta(seconds=710)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 58, "risk_level": "MEDIUM",
            "signals": [
                ("First transaction to foreign merchant in Singapore corridor", 3, "Behavioral"),
                ("Amount is 2.1x higher than standard card transaction threshold", 3, "Volume"),
            ],
            "stage": 2, "status": "FLAGGED",
        },

        # Cluster 5: Routine Baseline
        {
            "txn_id": "TXN-11002-A",
            "sender": "Nathan Obi", "sender_acct": "US-WF-4401928", "sender_kyc": "Tier-2 Verified",
            "receiver": "Olivia Hart", "receiver_acct": "US-BOA-8820192", "receiver_kyc": "Tier-2 Verified",
            "amount": 182.50, "currency": "USD", "channel": "P2P Payment",
            "device_fp": "FP-1109-PIXEL", "device_type": "Pixel 8 · Android",
            "geo": "Austin, USA", "ip": "66.249.79.12",
            "timestamp": (now - timedelta(seconds=890)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 11, "risk_level": "LOW",
            "signals": [
                ("Frequent transacting counterparty with 14 past transfers", 1, "Baseline"),
                ("Device and IP geolocation consistent with known user home zone", 1, "Device"),
            ],
            "stage": 4, "status": "AUTO-APPROVED",
        },
    ]

def cluster_incidents(txns):
    """Module A: Connected-component incident clustering."""
    g = nx.Graph()
    for i in range(len(txns)):
        g.add_node(i)

    for i in range(len(txns)):
        for j in range(i + 1, len(txns)):
            ti, tj = txns[i], txns[j]
            parties_i = {ti["sender"], ti["receiver"]}
            parties_j = {tj["sender"], tj["receiver"]}
            if (parties_i & parties_j) or (ti["device_fp"] == tj["device_fp"]):
                g.add_edge(i, j)

    clusters = list(nx.connected_components(g))
    incidents = []

    for inc_idx, comp in enumerate(clusters):
        c_txns = [txns[i] for i in sorted(comp)]
        max_score = max(t["risk_score"] for t in c_txns)
        highest_txn = max(c_txns, key=lambda t: t["risk_score"])
        max_level = highest_txn["risk_level"]

        participants = set()
        for t in c_txns:
            participants.add(t["sender"])
            participants.add(t["receiver"])

        if len(c_txns) >= 4:
            pattern_type = "Circular AML Layering Ring"
            p_desc = f"Rapid succession circular loop detected across {len(participants)} accounts within 120 seconds. Funds returned to origin."
        elif len(c_txns) == 3:
            pattern_type = "Structured CTR Smurfing Pattern"
            p_desc = f"Structuring detected: 3 outbound transfers just under $10,000 threshold totaling ${sum(t['amount'] for t in c_txns):,.2f}."
        elif len(c_txns) == 2:
            pattern_type = "Device Fingerprint Collision (Mule Ring)"
            p_desc = f"Shared hardware signature ({c_txns[0]['device_fp']}) executing concurrent transfers to beneficiary {c_txns[0]['receiver']}."
        else:
            if max_level == "LOW":
                pattern_type = "Verified Domestic Baseline"
                p_desc = "Recurring normal transaction pattern. Verified biometrics and trusted counterparty."
            else:
                pattern_type = "Single-Vector Behavioral Outlier"
                p_desc = f"Cross-border transfer {c_txns[0]['sender']} → {c_txns[0]['receiver']} triggered anomaly threshold."

        priority = "P1 - CRITICAL" if max_score >= 90 else "P2 - HIGH" if max_score >= 70 else "P3 - MEDIUM" if max_score >= 40 else "P4 - LOW"

        statuses = [t["status"] for t in c_txns]
        if any(s == "FROZEN" for s in statuses):
            overall_status = "FROZEN"
            overall_stage = 4
        elif any("HOLD" in s for s in statuses):
            overall_status = "HOLD (OTP SENT)"
            overall_stage = 3
        elif all(s in ("APPROVED", "AUTO-APPROVED") for s in statuses):
            overall_status = "RESOLVED"
            overall_stage = 4
        else:
            overall_status = "UNDER INVESTIGATION"
            overall_stage = 2

        if len(c_txns) >= 4:
            flow_str = f"{c_txns[0]['sender']} → {c_txns[1]['sender']} → {c_txns[2]['sender']} → {c_txns[3]['sender']} → {c_txns[0]['sender']}"
        elif len(c_txns) > 1:
            flow_str = f"{c_txns[0]['sender']} → {c_txns[0]['receiver']} & {c_txns[1]['sender']} → {c_txns[1]['receiver']}"
        else:
            flow_str = f"{c_txns[0]['sender']} → {c_txns[0]['receiver']}"

        incidents.append({
            "inc_id": f"INC-{inc_idx+101:04d}",
            "typology": pattern_type,
            "plain_summary": p_desc,
            "flow_summary": flow_str,
            "max_risk_score": max_score,
            "risk_level": max_level,
            "priority": priority,
            "status": overall_status,
            "stage": overall_stage,
            "participants": sorted(list(participants)),
            "txns": c_txns,
            "total_value": sum(t["amount"] for t in c_txns),
            "created_at": min(t["timestamp"] for t in c_txns),
        })

    return incidents

def detect_aml_cycles(txns):
    """Module C: NetworkX DiGraph Cycle Detection."""
    g = nx.DiGraph()
    for t in txns:
        g.add_edge(t["sender"], t["receiver"], amount=t["amount"], txn_id=t["txn_id"])
    try:
        cycles = [c for c in nx.simple_cycles(g) if len(c) >= 3]
        cycles.sort(key=len, reverse=True)
        return cycles
    except Exception:
        return []

def get_ai_recommendation(incident):
    """Module D: Structured LLM AI Suggestion Assistant."""
    typology = incident["typology"]
    if typology == "Circular AML Layering Ring":
        return {
            "analysis": (
                "High-confidence algorithmic laundering detection (Confidence: 98.4%). "
                "The directed graph isolates a closed, multi-hop ring with 1.8% value decay per hop. "
                "Hardware collision isolated: Charlie Okafor and Diana Petrova both transmitted from "
                "fingerprint FP-8891-BRAVE, evidencing a single syndicate controlling both intermediate "
                "and exit wallets across New York, London, Singapore, and Dubai."
            ),
            "action": "Immediate coordinated Freeze of all 4 accounts, dispatch SAR regulatory filing package, and revoke session tokens.",
            "friction_impact": "Zero legitimate customer impact. High-confidence syndicate ring isolated.",
            "model_version": "FINNEXUS-Titan-v4.2",
        }
    elif typology == "Structured CTR Smurfing Pattern":
        return {
            "analysis": (
                "Structuring anomaly detected with 93.1% pattern match to smurfing heuristics. "
                "Account Ethan Walsh initiated 3 transfers positioned strictly between $9,700 and $9,920 within 40 seconds. "
                "All transfers used identical browser session signatures to evade Bank Secrecy Act CTR triggers ($10,000 threshold)."
            ),
            "action": "Hold pending outbound transactions and trigger Step-Up Biometric / OTP Challenge to verify beneficial ownership before regulatory filing.",
            "friction_impact": "Friction-minimizing step-up verification prevents premature freezing of potentially legitimate split payroll.",
            "model_version": "FINNEXUS-Titan-v4.2",
        }
    elif typology == "Device Fingerprint Collision (Mule Ring)":
        return {
            "analysis": (
                "Device anomaly: Single hardware signature FP-7712-SAMSUNG concurrently controlled two disparate German bank accounts "
                "(Ivan Kruger & Kiran Patel) targeting the same inbound destination (Jasmine Rao in India). "
                "Strong indication of Account Takeover (ATO) or coordinated money mule aggregation."
            ),
            "action": "Hold outbound SEPA wires, transmit Silent Push / OTP challenge to enrolled mobile devices, and blacklist device fingerprint FP-7712.",
            "friction_impact": "Step-up challenge halts unauthorized hacker payouts while allowing legitimate user to re-authenticate.",
            "model_version": "FINNEXUS-Titan-v4.2",
        }
    elif typology == "Single-Vector Behavioral Outlier":
        return {
            "analysis": (
                "Isolated anomaly: Liam Johansson transacting from Stockholm to foreign Singapore merchant. "
                "Amount ($2,850) is 2.1x baseline, but biometrics and device fingerprint remain intact. "
                "Probability of legitimate customer travel purchase: 74%."
            ),
            "action": "Send Step-Up OTP challenge to cardholder. Do NOT freeze account.",
            "friction_impact": "Optimized friction reduction: Legitimate traveler approves OTP in 5 seconds without embarrassing card decline.",
            "model_version": "FINNEXUS-Titan-v4.2",
        }
    else:
        return {
            "analysis": "Transaction conforms to verified historical baseline. Valid tokenized device signature and trusted beneficiary.",
            "action": "Approve transaction without customer friction.",
            "friction_impact": "Frictionless checkout experience maintained.",
            "model_version": "FINNEXUS-Titan-v4.2",
        }

# ═══════════════════════════════════════════════════════════════════════════════
# 4. USER MOCKUP SCORE METER (Semi-Circular SVG Speedometer Gauge)
# ═══════════════════════════════════════════════════════════════════════════════
def generate_svg_score_meter(score: int) -> str:
    """
    Renders an exact semi-circular speedometer gauge inspired by User Mockup (Image 2).
    Features colored risk bands (AAA Green -> Critical Red) with a pointer needle.
    """
    width, height = 250, 140
    cx, cy = 125, 118
    r_out, r_in = 86, 54

    slices = [
        (180, 144, "#10B981", "AAA"),
        (144, 108, "#84CC16", "AA"),
        (108, 72, "#EAB308", "A"),
        (72, 36, "#F97316", "BBB"),
        (36, 0, "#EF4444", "CRIT"),
    ]

    paths = [
        f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF;border-radius:8px;border:1px solid #E2E8F0;">',
        '<text x="125" y="16" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#475569" text-anchor="middle" letter-spacing="0.5">RISK RATING SCORE METER</text>'
    ]

    for a_start, a_end, color, lbl in slices:
        rad_s, rad_e = math.radians(a_start), math.radians(a_end)
        x1_out = cx - r_out * math.cos(rad_s)
        y1_out = cy - r_out * math.sin(rad_s)
        x2_out = cx - r_out * math.cos(rad_e)
        y2_out = cy - r_out * math.sin(rad_e)
        x1_in = cx - r_in * math.cos(rad_e)
        y1_in = cy - r_in * math.sin(rad_e)
        x2_in = cx - r_in * math.cos(rad_s)
        y2_in = cy - r_in * math.sin(rad_s)

        paths.append(
            f'<path d="M {x1_out:.1f} {y1_out:.1f} A {r_out} {r_out} 0 0 1 {x2_out:.1f} {y2_out:.1f} '
            f'L {x1_in:.1f} {y1_in:.1f} A {r_in} {r_in} 0 0 0 {x2_in:.1f} {y2_in:.1f} Z" '
            f'fill="{color}" stroke="#FFFFFF" stroke-width="1.5" />'
        )

        mid_rad = math.radians((a_start + a_end) / 2)
        lbl_r = (r_out + r_in) / 2
        lbl_x = cx - lbl_r * math.cos(mid_rad)
        lbl_y = cy - lbl_r * math.sin(mid_rad) + 3
        paths.append(f'<text x="{lbl_x:.1f}" y="{lbl_y:.1f}" font-family="Inter, sans-serif" font-size="7.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">{lbl}</text>')

    clamped_score = max(0, min(100, score))
    needle_angle_deg = 180.0 - (clamped_score / 100.0) * 180.0
    needle_rad = math.radians(needle_angle_deg)
    needle_len = 76
    tip_x = cx - needle_len * math.cos(needle_rad)
    tip_y = cy - needle_len * math.sin(needle_rad)

    paths.append(f'<line x1="{cx}" y1="{cy}" x2="{tip_x:.1f}" y2="{tip_y:.1f}" stroke="#0F172A" stroke-width="3" stroke-linecap="round" />')
    paths.append(f'<circle cx="{cx}" cy="{cy}" r="7.5" fill="#0F172A" />')
    paths.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#FFFFFF" />')

    tier_txt = "CRITICAL" if score >= 85 else "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "SAFE"
    tier_color = "#DC2626" if score >= 85 else "#EA580C" if score >= 70 else "#D97706" if score >= 40 else "#059669"
    paths.append(f'<text x="125" y="134" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="800" fill="{tier_color}" text-anchor="middle">SCORE {score}/100 · {tier_txt}</text>')

    paths.append('</svg>')
    return "".join(paths)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. USER MOCKUP AMAZON-STYLE TRACKING TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
def generate_amazon_timeline_svg(current_stage: int) -> str:
    """Renders the sleek Amazon logistics tracking progression line matching Image 2."""
    width, height = 480, 68
    stages = [
        ("Received", 45),
        ("Scored", 145),
        ("Flagged", 245),
        ("Reviewed", 345),
        ("Action Taken", 435),
    ]

    svg = [
        f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:transparent;">',
        f'<line x1="45" y1="24" x2="435" y2="24" stroke="#E2E8F0" stroke-width="3" stroke-linecap="round" />',
    ]

    if current_stage > 0:
        fill_x = stages[min(current_stage, 4)][1]
        svg.append(f'<line x1="45" y1="24" x2="{fill_x}" y2="24" stroke="#059669" stroke-width="3" stroke-linecap="round" />')

    for s_idx, (name, x_pos) in enumerate(stages):
        if s_idx < current_stage:
            svg.append(f'<circle cx="{x_pos}" cy="24" r="11" fill="#059669" />')
            svg.append(f'<path d="M {x_pos-4} 24 L {x_pos-1} 27 L {x_pos+5} 21" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />')
            lbl_color = "#059669"
            lbl_weight = "700"
        elif s_idx == current_stage:
            svg.append(f'<circle cx="{x_pos}" cy="24" r="14" fill="#EEF2FF" stroke="#6366F1" stroke-width="2" />')
            svg.append(f'<circle cx="{x_pos}" cy="24" r="9" fill="#FFFFFF" stroke="#6366F1" stroke-width="2" />')
            svg.append(f'<circle cx="{x_pos}" cy="24" r="4" fill="#DC2626" />')
            lbl_color = "#4F46E5"
            lbl_weight = "800"
        else:
            svg.append(f'<circle cx="{x_pos}" cy="24" r="9" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />')
            lbl_color = "#94A3B8"
            lbl_weight = "600"

        svg.append(f'<text x="{x_pos}" y="48" font-family="Inter, sans-serif" font-size="9.5" font-weight="{lbl_weight}" fill="{lbl_color}" text-anchor="middle">{name}</text>')

    svg.append('</svg>')
    return "".join(svg)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. NATIVE SVG GENOME VISUALIZER (Zero Dependency, Feedzai Style)
# ═══════════════════════════════════════════════════════════════════════════════
def render_native_genome_svg(txns, cycles):
    """Renders NetworkX DiGraph cleanly in SVG without leaking raw text."""
    G = nx.DiGraph()
    for t in txns:
        G.add_edge(t["sender"], t["receiver"], amount=t["amount"])

    nodes = list(G.nodes())
    if not nodes:
        return "<div style='color:#94A3B8;text-align:center;'>No graph nodes available</div>"

    cycle_nodes = set()
    cycle_edges = set()
    for cycle in cycles:
        for k in range(len(cycle)):
            cycle_nodes.add(cycle[k])
            cycle_edges.add((cycle[k], cycle[(k + 1) % len(cycle)]))

    width = 580
    height = 290
    cx, cy = width / 2, height / 2

    coords = {}
    if cycle_nodes:
        c_list = sorted(list(cycle_nodes))
        radius = 85
        for idx, node in enumerate(c_list):
            angle = (2 * math.pi * idx / len(c_list)) - (math.pi / 2)
            coords[node] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))

        non_cycle = [n for n in nodes if n not in cycle_nodes]
        for idx, node in enumerate(non_cycle):
            angle = (2 * math.pi * idx / max(1, len(non_cycle))) + 0.4
            coords[node] = (cx + 175 * math.cos(angle), cy + 110 * math.sin(angle))
    else:
        for idx, node in enumerate(nodes):
            angle = 2 * math.pi * idx / len(nodes)
            coords[node] = (cx + 140 * math.cos(angle), cy + 90 * math.sin(angle))

    svg = [
        f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF;border-radius:8px;border:1px solid #CBD5E1;">',
        '<defs>',
        '<marker id="arr-def" viewBox="0 0 10 10" refX="21" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#94A3B8" /></marker>',
        '<marker id="arr-cyc" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#DC2626" /></marker>',
        '</defs>',
    ]

    for gx in range(40, width, 50):
        for gy in range(30, height, 50):
            svg.append(f'<circle cx="{gx}" cy="{gy}" r="1.5" fill="#F1F5F9" />')

    for u, v in G.edges():
        if u not in coords or v not in coords:
            continue
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        is_cyc = (u, v) in cycle_edges
        stroke = "#DC2626" if is_cyc else "#94A3B8"
        pw = "2.6" if is_cyc else "1.4"
        marker = "url(#arr-cyc)" if is_cyc else "url(#arr-def)"
        dash = 'stroke-dasharray="6,3"' if is_cyc else ""
        svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{pw}" marker-end="{marker}" {dash} />')

    for node in nodes:
        if node not in coords:
            continue
        x, y = coords[node]
        short_name = node.split()[0]
        is_ring = node in cycle_nodes

        if is_ring:
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="18" fill="none" stroke="#EF4444" stroke-width="2" opacity="0.4"><animate attributeName="r" values="16;22;16" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/></circle>')
            fill_c = "#FEF2F2"
            stroke_c = "#DC2626"
            txt_c = "#991B1B"
        else:
            fill_c = "#F0F9FF"
            stroke_c = "#0284C7"
            txt_c = "#0369A1"

        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{fill_c}" stroke="{stroke_c}" stroke-width="2" />')
        svg.append(f'<text x="{x:.1f}" y="{y+4:.1f}" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="{txt_c}" text-anchor="middle">{short_name[:3].upper()}</text>')
        svg.append(f'<text x="{x:.1f}" y="{y+23:.1f}" font-family="Inter, sans-serif" font-size="8" font-weight="600" fill="#475569" text-anchor="middle">{short_name}</text>')

    svg.append('</svg>')
    return "".join(svg)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. AI COPILOT CHATBOT KNOWLEDGE ENGINE (Image 2 Requirement)
# ═══════════════════════════════════════════════════════════════════════════════
def query_ai_copilot(user_query: str, incidents, cycles) -> str:
    """Answers compliance queries with dynamic contextual graph intelligence."""
    q = user_query.lower()

    if "circular" in q or "loop" in q or "ring" in q:
        if cycles:
            c = cycles[0]
            path = " → ".join(c) + " → " + c[0]
            return (
                f"🚨 **Circular Layering Ring Isolated**: A 4-hop circular loop was detected connecting {path}. "
                f"Funds transited $49,500 across 4 jurisdictions (US, UK, SG, AE) in 115 seconds with a 1.8% commission decay. "
                f"Additionally, Charlie Okafor and Diana Petrova share hardware fingerprint `FP-8891-BRAVE`, indicating a coordinated syndicate. "
                f"**Recommendation**: Execute coordinated freeze on all 4 accounts and submit SAR."
            )
        return "No circular AML loops currently active in the graph topology."

    elif "ethan" in q or "structuring" in q or "smurf" in q:
        return (
            "⚠️ **CTR Structuring Pattern**: Ethan Walsh executed 3 rapid outbound transfers ($9,850, $9,700, $9,920) "
            "totaling $29,470 within 40 seconds to 3 distinct beneficiaries (Fiona, George, Hannah). "
            "All transfers were positioned immediately below the $10,000 BSA reporting threshold using device `FP-2240-IOS`. "
            "**Recommendation**: Transmit step-up OTP challenge to verify beneficial ownership before freezing."
        )

    elif "freeze" in q or "action" in q:
        return (
            "🎯 **Action Protocol**: For **P1 Critical circular rings**, execute **'Freeze Account'** immediately to prevent cross-border liquidation. "
            "For single travel outliers (e.g. Liam Johansson), click **'Hold & Send OTP'** to challenge the customer biometrically, minimizing friction."
        )

    elif "device" in q or "collision" in q or "fingerprint" in q:
        return (
            "📱 **Device Collision Isolated**: Fingerprint `FP-7712-SAMSUNG` was concurrently utilized by Ivan Kruger and Kiran Patel "
            "to transmit funds to the same beneficiary (Jasmine Rao in India). Probability of Account Takeover (ATO): 89.2%."
        )

    else:
        top_inc = max(incidents, key=lambda x: x["max_risk_score"])
        return (
            f"💡 **FINNEXUS Intelligence Analysis**: Highest active priority is **{top_inc['inc_id']} ({top_inc['typology']})** "
            f"with a Risk Score of **{top_inc['max_risk_score']}/100**. Total active exposure across the network is "
            f"${sum(i['total_value'] for i in incidents):,.2f}. Zero friction false-positive mitigations are active for legitimate cardholders."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 8. SESSION STATE & COMPLIANCE ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════
if "app_txns" not in st.session_state:
    st.session_state.app_txns = build_initial_dataset()

if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "🛡️ Alert & Incident Orchestrator"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "👋 I am FINNEXUS Compliance Copilot. Ask me about detected circular rings, suspect account collusion, or recommended freeze actions."}
    ]

raw_incidents = cluster_incidents(st.session_state.app_txns)
current_cycles = detect_aml_cycles(st.session_state.app_txns)

def execute_compliance_action(incident_id, action_type):
    """Module F: 1-Click Action Orchestration Engine."""
    target_inc = None
    for inc in raw_incidents:
        if inc["inc_id"] == incident_id:
            target_inc = inc
            break

    if not target_inc:
        return

    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_txn_ids = {t["txn_id"] for t in target_inc["txns"]}

    if action_type == "APPROVE":
        new_status = "APPROVED"
        new_stage = 4
        audit_note = "Transaction verified legitimate. Customer friction avoided."
    elif action_type == "HOLD":
        new_status = "HOLD (OTP SENT)"
        new_stage = 3
        audit_note = "Step-up OTP Challenge transmitted to user device to prevent ATO."
    elif action_type == "FREEZE":
        new_status = "FROZEN"
        new_stage = 4
        audit_note = "Coordinated Freeze executed across all syndicate accounts. SAR queued."
    else:
        return

    for t in st.session_state.app_txns:
        if t["txn_id"] in target_txn_ids:
            t["status"] = new_status
            t["stage"] = new_stage

    st.session_state.audit_history.insert(0, {
        "timestamp": now_ts,
        "incident_id": incident_id,
        "typology": target_inc["typology"],
        "action": action_type,
        "affected_accounts": ", ".join(target_inc["participants"][:3]) + ("..." if len(target_inc["participants"]) > 3 else ""),
        "total_amount": f"${target_inc['total_value']:,.2f}",
        "analyst": "Sarah Blair (L2 Senior Investigator)",
        "friction_outcome": audit_note,
    })

def simulate_new_incoming_transaction():
    """Simulates real-time ingestion into queue."""
    pool = ["Kiran Patel", "Yuki Tanaka", "Carlos Mendoza", "Fatima Al-Mansoor", "Lucas Silva"]
    sender = random.choice(pool)
    receiver = random.choice([p for p in pool if p != sender])
    score = random.randint(65, 96)
    level = "CRITICAL" if score >= 90 else "HIGH"

    new_t = {
        "txn_id": f"TXN-{random.randint(10000, 99999)}-X",
        "sender": sender, "sender_acct": f"INTL-{random.randint(100000, 999999)}", "sender_kyc": "Tier-1 Basic",
        "receiver": receiver, "receiver_acct": f"INTL-{random.randint(100000, 999999)}", "receiver_kyc": "Unverified",
        "amount": round(random.uniform(8500, 75000), 2), "currency": "USD", "channel": "Wire",
        "device_fp": f"FP-{random.randint(1000, 9999)}-TOR", "device_type": "Linux · Tor Browser",
        "geo": random.choice(["Geneva, CH", "Singapore, SG", "Panama City, PA", "Nicosia, CY"]),
        "ip": f"185.{random.randint(10, 220)}.44.12",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_score": score, "risk_level": level,
        "signals": [
            ("Unrecognized exit relay node in non-cooperative jurisdiction", 4, "Network"),
            ("High deviation against sender 30-day velocity standard", 5, "Behavioral"),
        ],
        "stage": 2, "status": "FLAGGED",
    }
    st.session_state.app_txns.insert(0, new_t)

# ═══════════════════════════════════════════════════════════════════════════════
# 9. TOP NAVIGATION BANNER & TABS
# ═══════════════════════════════════════════════════════════════════════════════
render_html("""
<div class="sf-banner">
    <div class="sf-brand-left">
        <div class="sf-logo">FN</div>
        <div>
            <div class="sf-title">FINNEXUS</div>
            <div class="sf-subtitle">Enterprise Real-Time Fraud & AML Risk Orchestration</div>
        </div>
    </div>
    <div class="sf-status-pill">
        <div class="live-dot"></div>
        <span>LIVE TELEMETRY ACTIVE</span>
        <span style="color:#64748B;">|</span>
        <span style="color:#94A3B8;">Analyst: S. Blair (L2)</span>
    </div>
</div>
""")

nav_options = [
    "🛡️ Alert & Incident Orchestrator",
    "📊 Executive Dashboard",
    "📁 Case Management (ActOne)",
    "📜 FinCEN SAR Filings"
]

selected_nav = st.radio(
    "Navigation Views",
    options=nav_options,
    index=nav_options.index(st.session_state.active_nav) if st.session_state.active_nav in nav_options else 0,
    horizontal=True,
    label_visibility="collapsed",
    key="main_nav_radio"
)
st.session_state.active_nav = selected_nav

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 1: 🛡️ ALERT & INCIDENT ORCHESTRATOR (CORE WORKSPACE)
# ═══════════════════════════════════════════════════════════════════════════════
if selected_nav == "🛡️ Alert & Incident Orchestrator":
    # ── Top Metrics Header ──
    total_scanned_num = len(st.session_state.app_txns) + 14820
    flagged_threats_num = sum(1 for t in st.session_state.app_txns if t["risk_level"] in ("CRITICAL", "HIGH"))
    loops_num = len(current_cycles)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        render_html(f"""
        <div class="metric-box m-blue">
            <div class="m-lbl">Total Scanned Today 📈</div>
            <div class="m-val">{total_scanned_num:,}</div>
            <div class="m-sub sub-green">↑ 1,240 txns in last 60 mins</div>
        </div>
        """)
    with m_col2:
        render_html(f"""
        <div class="metric-box m-red">
            <div class="m-lbl">Flagged Threats 🚨</div>
            <div class="m-val">{flagged_threats_num + 42}</div>
            <div class="m-sub sub-red">⚠️ {flagged_threats_num} requiring active triage</div>
        </div>
        """)
    with m_col3:
        render_html("""
        <div class="metric-box m-green">
            <div class="m-lbl">System Latency ⚡</div>
            <div class="m-val">38 ms</div>
            <div class="m-sub sub-green">✓ 4.2x faster than SLA (200ms)</div>
        </div>
        """)
    with m_col4:
        render_html(f"""
        <div class="metric-box m-purple">
            <div class="m-lbl">AML Loops Isolated 🔗</div>
            <div class="m-val">{loops_num + 1}</div>
            <div class="m-sub sub-red">🚨 {loops_num} active circular rings</div>
        </div>
        """)

    # ── Live Telemetry Performance Bar ──
    render_html("""
    <div class="telemetry-row">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:14px;">📡</span>
            <span style="font-size:11.5px;font-weight:800;color:#0F172A;text-transform:uppercase;letter-spacing:0.8px;">Model Performance Telemetry</span>
        </div>
        <div class="tele-tag tag-green"><span>Precision:</span> <strong>94.2%</strong></div>
        <div class="tele-tag tag-green"><span>Recall:</span> <strong>91.8%</strong></div>
        <div class="tele-tag tag-amber"><span>False-Positive Rate:</span> <strong>1.4%</strong></div>
        <div class="tele-tag tag-blue"><span>Detection Engine Latency:</span> <strong>38 ms</strong></div>
    </div>
    """)

    # ── MULTI-CRITERIA FILTERING & SORTING TOOLBAR ──
    st.markdown("#### 🔍 Filter & Organize Incident Alerts")
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.3, 1.3, 1.4])

    with f_col1:
        sort_criterion = st.selectbox(
            "Sort Alerts By",
            options=[
                "Risk Score: Highest to Lowest",
                "Risk Score: Lowest to Highest",
                "Entities Involved: Most to Least",
                "Cluster Exposure: Highest to Lowest",
                "Newest Ingestion First"
            ],
            index=0,
            key="alert_sort_selector"
        )
    with f_col2:
        priority_filter = st.selectbox(
            "Filter Priority",
            options=["All Priorities", "P1 - CRITICAL Only", "P2 - HIGH Only", "P3 - MEDIUM Only"],
            index=0,
            key="alert_priority_filter"
        )
    with f_col3:
        status_filter = st.selectbox(
            "Filter Status",
            options=["All Statuses", "Under Investigation", "Action Taken (Approved/Hold/Frozen)"],
            index=0,
            key="alert_status_filter"
        )
    with f_col4:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("➕ Ingest Live Transaction", use_container_width=True):
            simulate_new_incoming_transaction()
            st.rerun()

    # Apply Filtering & Sorting Logic
    filtered_incidents = list(raw_incidents)

    if priority_filter == "P1 - CRITICAL Only":
        filtered_incidents = [i for i in filtered_incidents if i["risk_level"] == "CRITICAL"]
    elif priority_filter == "P2 - HIGH Only":
        filtered_incidents = [i for i in filtered_incidents if i["risk_level"] == "HIGH"]
    elif priority_filter == "P3 - MEDIUM Only":
        filtered_incidents = [i for i in filtered_incidents if i["risk_level"] == "MEDIUM"]

    if status_filter == "Under Investigation":
        filtered_incidents = [i for i in filtered_incidents if i["status"] == "UNDER INVESTIGATION"]
    elif status_filter == "Action Taken (Approved/Hold/Frozen)":
        filtered_incidents = [i for i in filtered_incidents if i["status"] in ("APPROVED", "HOLD (OTP SENT)", "FROZEN", "RESOLVED")]

    if sort_criterion == "Risk Score: Highest to Lowest":
        filtered_incidents.sort(key=lambda x: x["max_risk_score"], reverse=True)
    elif sort_criterion == "Risk Score: Lowest to Highest":
        filtered_incidents.sort(key=lambda x: x["max_risk_score"], reverse=False)
    elif sort_criterion == "Entities Involved: Most to Least":
        filtered_incidents.sort(key=lambda x: len(x["participants"]), reverse=True)
    elif sort_criterion == "Cluster Exposure: Highest to Lowest":
        filtered_incidents.sort(key=lambda x: x["total_value"], reverse=True)
    elif sort_criterion == "Newest Ingestion First":
        filtered_incidents.sort(key=lambda x: x["created_at"], reverse=True)

    # ── Split Layout: Left Feed | Right Sticky Panel (Image 4 Requirement) ──
    feed_col, intel_col = st.columns([14, 10], gap="medium")

    # ═══════════════════════════════════════════════════════════════════════════
    # LEFT COLUMN: MODULE A & B (ALERTS MATCHING USER MOCKUP - IMAGE 2)
    # ═══════════════════════════════════════════════════════════════════════════
    with feed_col:
        st.markdown(f"**Showing {len(filtered_incidents)} Incident Alert Clusters**")

        for incident in filtered_incidents:
            inc_id = incident["inc_id"]
            p_badge_cls = "header-badge-p1" if incident["risk_level"] == "CRITICAL" else "header-badge-p2" if incident["risk_level"] == "HIGH" else "header-badge-p3"
            status_style_cls = "meta-val-red" if incident["status"] == "FROZEN" else "meta-val-green" if incident["status"] in ("APPROVED", "RESOLVED") else "meta-val-blue"

            # ── 1. User Mockup Container Card (Image 2) ──
            # Rendered cleanly via clean_html to prevent ANY Markdown code block conversion!
            card_html = f"""
            <div class="alert-card">
                <div class="card-header-banner">
                    <div class="{p_badge_cls}">{incident['priority']}</div>
                    <div class="banner-summary-text">{incident['plain_summary']}</div>
                    <div class="banner-score-num">{incident['max_risk_score']}</div>
                </div>
                <div class="card-meta-row">
                    <div class="meta-block">
                        <span class="meta-lbl">INCIDENT ID</span>
                        <span class="meta-val-text" style="font-family:'JetBrains Mono',monospace;">{inc_id}</span>
                    </div>
                    <div class="meta-block">
                        <span class="meta-lbl">CLUSTER VALUE</span>
                        <span class="meta-val-text">${incident['total_value']:,.2f}</span>
                    </div>
                    <div class="meta-block">
                        <span class="meta-lbl">ENTITIES</span>
                        <span class="meta-val-text">{len(incident['participants'])} Accounts</span>
                    </div>
                    <div class="meta-block">
                        <span class="meta-lbl">CHANNEL</span>
                        <span class="meta-val-text">{incident['txns'][0]['channel']}</span>
                    </div>
                    <div class="meta-block">
                        <span class="meta-lbl">STATUS</span>
                        <span class="{status_style_cls}">{incident['status']}</span>
                    </div>
                </div>
            </div>
            """
            render_html(card_html)

            # ── 2. Mid Section Split (Left: Flow + Timeline + Buttons | Right: Score Meter) ──
            c_left, c_right = st.columns([15, 9])

            with c_left:
                flow_header_html = f"""
                <div class="card-flow-header">
                    <span>{incident['flow_summary']}</span>
                    <span style="color:#CBD5E1;">•</span>
                    <span>🕒 {incident['created_at']}</span>
                    <span style="color:#CBD5E1;">•</span>
                    <span>📱 {incident['txns'][0]['device_type']}</span>
                    <span style="color:#CBD5E1;">•</span>
                    <span>📍 {incident['txns'][0]['geo']}</span>
                </div>
                """
                render_html(flow_header_html)

                timeline_svg = generate_amazon_timeline_svg(incident["stage"])
                render_html(timeline_svg)

                # Action Buttons
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                btn_c1, btn_c2, btn_c3 = st.columns(3)
                with btn_c1:
                    if st.button("✅ Approve", key=f"btn_ap_{inc_id}", use_container_width=True):
                        execute_compliance_action(inc_id, "APPROVE")
                        st.rerun()
                with btn_c2:
                    if st.button("⏸️ Hold & Send OTP", key=f"btn_hd_{inc_id}", use_container_width=True):
                        execute_compliance_action(inc_id, "HOLD")
                        st.rerun()
                with btn_c3:
                    if st.button("🧊 Freeze Account", key=f"btn_fz_{inc_id}", type="primary", use_container_width=True):
                        execute_compliance_action(inc_id, "FREEZE")
                        st.rerun()

            with c_right:
                meter_svg = generate_svg_score_meter(incident["max_risk_score"])
                render_html(meter_svg)

            # ── 3. "MORE DETAILS" EXPANDER ──
            with st.expander(f"🔍 More details — {inc_id} ({len(incident['participants'])} Accounts Involved & AI Analysis)", expanded=False):
                st.markdown(f"### 📋 Case Dossier: {inc_id} · {incident['typology']}")
                st.caption("Comprehensive entity telemetry, AI investigator reasoning, and cross-channel evidence trail.")

                tab_det_entities, tab_det_ai, tab_det_signals, tab_det_ledger = st.tabs([
                    f"👥 All Involved Accounts ({len(incident['participants'])})",
                    "💡 AI Investigator Analysis",
                    "ℹ️ Whitebox Signals & NICE Matrix",
                    "📜 Complete Transaction Ledger"
                ])

                # ──── SUB-TAB 1: ALL ACCOUNTS INVOLVED ────
                with tab_det_entities:
                    st.markdown("**Key Account Profiles for Everyone Involved in this Transaction**")
                    st.caption("Deduplicated participant dossier with account numbers, KYC tiers, hardware hashes, and geo-IPs.")

                    all_account_records = []
                    seen_participants = set()
                    for t in incident["txns"]:
                        if t["sender"] not in seen_participants:
                            seen_participants.add(t["sender"])
                            all_account_records.append({
                                "Participant Name": t["sender"],
                                "Account Number": t["sender_acct"],
                                "KYC Status": t["sender_kyc"],
                                "Cluster Role": "Origin Sender / Ring Node",
                                "Device Fingerprint": t["device_fp"],
                                "Hardware Platform": t["device_type"],
                                "Geolocation": t["geo"],
                                "IP Address": t["ip"],
                                "Involved Outflow": f"${t['amount']:,.2f} {t['currency']}"
                            })

                        if t["receiver"] not in seen_participants:
                            seen_participants.add(t["receiver"])
                            all_account_records.append({
                                "Participant Name": t["receiver"],
                                "Account Number": t["receiver_acct"],
                                "KYC Status": t["receiver_kyc"],
                                "Cluster Role": "Beneficiary / Intermediate Mule" if t["receiver"] != incident["txns"][0]["sender"] else "Loop Return Node",
                                "Device Fingerprint": t["device_fp"] if t["receiver"] == "Diana Petrova" else "FP-LOCAL-RECV",
                                "Hardware Platform": t["device_type"] if t["receiver"] == "Diana Petrova" else "Standard Banking Client",
                                "Geolocation": "International Correspondent Corridor",
                                "IP Address": t["ip"],
                                "Involved Outflow": f"${t['amount']:,.2f} {t['currency']}"
                            })

                    df_all_accounts = pd.DataFrame(all_account_records)
                    st.dataframe(df_all_accounts, use_container_width=True, hide_index=True)

                # ──── SUB-TAB 2: AI INVESTIGATOR ANALYSIS ────
                with tab_det_ai:
                    rec = get_ai_recommendation(incident)
                    ai_card_html = f"""
                    <div class="ai-card">
                        <div class="ai-hdr">
                            <span>💡</span>
                            <span style="font-size:13px;font-weight:800;">Autonomous AI Investigator Reasoning</span>
                        </div>
                        <div class="ai-body" style="font-size:12.5px;margin-top:6px;">
                            {rec['analysis']}
                        </div>
                        <div class="ai-action-chip" style="font-size:12px;margin-top:10px;">
                            🎯 <strong>Recommended Compliance Directive:</strong> {rec['action']}
                        </div>
                        <div style="margin-top:10px;font-size:11.5px;color:#047857;background:rgba(255,255,255,0.85);padding:8px 12px;border-radius:6px;border:1px solid #A7F3D0;">
                            <strong>Customer Friction Reduction Strategy:</strong> {rec['friction_impact']}
                        </div>
                        <div style="font-size:10px;color:#059669;margin-top:8px;text-align:right;">
                            Inference Engine: {rec['model_version']} · Verified against FinCEN AML Typologies
                        </div>
                    </div>
                    """
                    render_html(ai_card_html)

                # ──── SUB-TAB 3: WHITEBOX SIGNALS & NICE ACTIMIZE MATRIX ────
                with tab_det_signals:
                    sig_c1, sig_c2 = st.columns([1, 1])
                    with sig_c1:
                        wb_html = ['<div class="wb-box"><div class="wb-hdr">ℹ️ Feedzai Whitebox Explanations (Severity Dots)</div>']
                        for txn_item in incident["txns"]:
                            for sig_text, sev_level, _ch in txn_item["signals"]:
                                dots_html = ""
                                for d in range(5):
                                    if d < sev_level:
                                        d_c = "d-red" if sev_level == 5 else "d-orange" if sev_level == 4 else "d-amber"
                                        dots_html += f'<div class="d-circle {d_c}"></div>'
                                    else:
                                        dots_html += '<div class="d-circle d-gray"></div>'
                                wb_html.append(f'<div class="wb-row"><span>{sig_text}</span><div class="dots-group">{dots_html}</div></div>')
                        wb_html.append('</div>')
                        render_html("".join(wb_html))

                    with sig_c2:
                        cc_matrix_html = """
                        <div class="cc-container">
                            <div style="font-size:11.5px;font-weight:700;color:#1E293B;margin-bottom:8px;">🔀 NICE Actimize Cross-Channel Correlation</div>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                                <div>
                                    <span class="cc-pill">Wire: Multi-Jurisdiction Jump</span>
                                    <span class="cc-pill">Device: Token Replay Collision</span>
                                </div>
                                <div>
                                    <span class="cc-pill cc-pill-warn">ACH: CTR Smurfing Avoidance</span>
                                    <span class="cc-pill cc-pill-warn">Network: Tor Relay Gateway</span>
                                </div>
                            </div>
                        </div>
                        """
                        render_html(cc_matrix_html)

                # ──── SUB-TAB 4: TRANSACTION LEDGER ────
                with tab_det_ledger:
                    st.markdown("**Granular Transaction Flow History**")
                    ledger_data = []
                    for t in incident["txns"]:
                        ledger_data.append({
                            "Timestamp": t["timestamp"],
                            "Transaction ID": t["txn_id"],
                            "Origin Sender": t["sender"],
                            "Destination Beneficiary": t["receiver"],
                            "Amount": f"${t['amount']:,.2f} {t['currency']}",
                            "Channel": t["channel"],
                            "Risk Score": t["risk_score"],
                            "Status": t["status"]
                        })
                    st.dataframe(pd.DataFrame(ledger_data), use_container_width=True, hide_index=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # RIGHT COLUMN: STATIONARY INTEL PANEL + CHATBOT (Image 4 & Image 2)
    # ═══════════════════════════════════════════════════════════════════════════
    with intel_col:
        # Killer USP Warning Banner
        if current_cycles:
            for c_idx, cycle in enumerate(current_cycles):
                c_path = " → ".join(cycle) + " → " + cycle[0]
                ring_amounts = []
                for k in range(len(cycle)):
                    u, v = cycle[k], cycle[(k + 1) % len(cycle)]
                    for t in st.session_state.app_txns:
                        if t["sender"] == u and t["receiver"] == v:
                            ring_amounts.append(t["amount"])
                            break
                tot_vol = sum(ring_amounts)

                banner_html = f"""
                <div class="aml-banner">
                    <div style="font-size:13.5px;font-weight:800;margin-bottom:4px;">
                        🚨 CRITICAL AML ALERT: CIRCULAR LAYERING RING #{c_idx+1}
                    </div>
                    <div style="font-size:11.5px;color:#FECACA;line-height:1.45;">
                        <strong>NetworkX Cycle Detection:</strong> Autonomous multi-account layering ring isolated.
                        Funds cycle through mules and return to origin in under 120s.
                        <br/>
                        <strong>Topology:</strong> {len(cycle)} nodes · {len(ring_amounts)} directed hops · Total Ring Value: <strong>${tot_vol:,.2f}</strong>
                    </div>
                    <div class="aml-route-box">
                        🔄 {c_path}
                    </div>
                </div>
                """
                render_html(banner_html)
        else:
            st.success("🛡️ No Active Circular AML Rings Detected · NetworkX Topology Scanner Nominal")

        # Feedzai Genome Visualizer
        st.markdown("**✧ Genome Entity Network Graph** · *Feedzai Visual Pattern*")
        svg_code = render_native_genome_svg(st.session_state.app_txns, current_cycles)
        render_html(svg_code)

        # Feedzai Similar Geometries
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.caption("Similar Network Geometries (Feedzai Pattern Matching)")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.metric("Circular Layering", "96.4% Match", "24 Confirmed")
        with g2:
            st.metric("CTR Smurfing Fan", "89.1% Match", "12 Violations")
        with g3:
            st.metric("Mule Token Collision", "81.5% Match", "Shared HW")

        # Sardine Style Mod Z-Score Telemetry
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("**📈 Anomaly Telemetry Signals** · *Sardine Mod Z-Score Metrics*")
        z1, z2 = st.columns(2)
        with z1:
            st.metric("Device Timezone Jump", "+4.8 Z-Score", "Anomaly Detected", delta_color="inverse")
        with z2:
            st.metric("Transaction Velocity Spike", "+5.1 Z-Score", "Volume Anomaly", delta_color="inverse")

        # ── REQUIREMENT 2 & 3: FINNEXUS AI COMPLIANCE COPILOT CHATBOT ──
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("#### 🤖 FINNEXUS AI Compliance Copilot")
        st.caption("Ask questions about suspect rings, mule networks, or freeze recommendations:")

        # Quick Prompt Buttons
        qp_col1, qp_col2 = st.columns(2)
        with qp_col1:
            if st.button("💬 Explain Ring #1", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": "Explain circular loop #1"})
                ans = query_ai_copilot("Explain circular loop #1", raw_incidents, current_cycles)
                st.session_state.chat_messages.append({"role": "assistant", "content": ans})
                st.rerun()
        with qp_col2:
            if st.button("💬 Check Structuring", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": "Why was Ethan Walsh flagged for structuring?"})
                ans = query_ai_copilot("Why was Ethan Walsh flagged for structuring?", raw_incidents, current_cycles)
                st.session_state.chat_messages.append({"role": "assistant", "content": ans})
                st.rerun()

        # Chat history container
        chat_box = st.container(height=260)
        with chat_box:
            for msg in st.session_state.chat_messages[-6:]:
                if msg["role"] == "user":
                    st.markdown(f"**Investigator:** {msg['content']}")
                else:
                    st.markdown(f"**FINNEXUS Copilot:** {msg['content']}")

        # User Question Input
        user_input = st.chat_input("Ask FINNEXUS Copilot a question...", key="copilot_chat_input")
        if user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            reply = query_ai_copilot(user_input, raw_incidents, current_cycles)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    # ── Immutable Audit Log History Table ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("### 📜 Immutable Compliance Audit Log History")
    st.caption("Permanent regulatory audit record tracking all investigator decisions, timestamps, and friction outcomes.")

    if st.session_state.audit_history:
        df_audit = pd.DataFrame(st.session_state.audit_history)
        st.dataframe(df_audit, use_container_width=True, hide_index=True)
    else:
        st.info("No compliance actions taken yet. Click 'Approve', 'Hold & Send OTP', or 'Freeze Account' on any alert card to simulate triage.")

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 2: 📊 EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif selected_nav == "📊 Executive Dashboard":
    st.markdown("## 📊 Executive Risk & Fraud Telemetry")
    st.caption("Executive overview of loss prevention, threat typology distributions, and machine learning engine performance.")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Capital Loss Prevented", "$4,821,450", "+$412,000 this week")
    with kpi2:
        st.metric("False Positive Rate", "1.4%", "-12.8% vs Legacy Rules", delta_color="inverse")
    with kpi3:
        st.metric("Autonomous Triage Rate", "88.6%", "+5.4% efficiency")
    with kpi4:
        st.metric("Regulatory SAR SLA", "99.8%", "0 Breaches")

    st.markdown("---")
    c_chart1, c_chart2 = st.columns([1, 1])

    with c_chart1:
        st.markdown("#### 🚨 Threat Typology Distribution")
        df_typologies = pd.DataFrame({
            "Typology Pattern": [
                "Circular AML Layering",
                "CTR Structuring / Smurfing",
                "Device Fingerprint Collision",
                "Account Takeover (ATO)",
                "Synthetic Identity Fraud",
                "Card Not Present Outliers"
            ],
            "Incident Count": [28, 44, 39, 52, 19, 63],
            "Total Capital At Risk": [1420000, 480000, 620000, 980000, 310000, 1011450]
        })
        st.dataframe(df_typologies, use_container_width=True, hide_index=True)
        st.bar_chart(df_typologies.set_index("Typology Pattern")["Incident Count"])

    with c_chart2:
        st.markdown("#### ⏱️ Real-Time Detection Latency vs SLA")
        df_latency = pd.DataFrame({
            "Evaluation Phase": [
                "1. Ingestion & Normalization",
                "2. Feature Store Extraction",
                "3. ML Risk Model Inference",
                "4. NetworkX Cycle Detection",
                "5. Action Orchestration"
            ],
            "Latency (ms)": [4, 8, 12, 10, 4],
            "Target SLA (ms)": [20, 40, 60, 50, 30]
        })
        st.dataframe(df_latency, use_container_width=True, hide_index=True)
        st.line_chart(df_latency.set_index("Evaluation Phase")[["Latency (ms)", "Target SLA (ms)"]])

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 3: 📁 CASE MANAGEMENT (ActOne / AMLOCK)
# ═══════════════════════════════════════════════════════════════════════════════
elif selected_nav == "📁 Case Management (ActOne)":
    st.markdown("## 📁 NICE ActOne Case Management Console")
    st.caption("Active investigator dossiers, queue assignments, and evidence chain-of-custody.")

    col_flt1, col_flt2, col_flt3 = st.columns(3)
    with col_flt1:
        st.selectbox("Filter by Queue", ["All Assigned Queues", "Tier-2 Priority", "SAR Review Queue", "Escalated Syndicates"])
    with col_flt2:
        st.selectbox("Assigned Investigator", ["All Analysts", "Sarah Blair (L2)", "David Chen (L3)", "Priya Sharma (AML Lead)"])
    with col_flt3:
        st.selectbox("SLA Status", ["All SLAs", "Under 2 Hours Remaining", "Healthy (> 8 Hours)"])

    df_cases = pd.DataFrame([
        {
            "Case ID": "CASE-455676",
            "Subject Entity": "Alice Whitmore Syndicate",
            "Typology": "Circular AML Layering Ring",
            "Risk Score": 98,
            "Priority": "P1 - CRITICAL",
            "Investigator": "Sarah Blair (L2)",
            "SLA Remaining": "1h 42m",
            "Status": "Active Investigation",
            "SAR Required": "YES"
        },
        {
            "Case ID": "CASE-455677",
            "Subject Entity": "Ethan Walsh",
            "Typology": "Structured CTR Smurfing",
            "Risk Score": 84,
            "Priority": "P2 - HIGH",
            "Investigator": "David Chen (L3)",
            "SLA Remaining": "4h 15m",
            "Status": "Pending OTP Response",
            "SAR Required": "EVALUATING"
        },
        {
            "Case ID": "CASE-455678",
            "Subject Entity": "Jasmine Rao / Mule Ring",
            "Typology": "Device Token Collision",
            "Risk Score": 81,
            "Priority": "P2 - HIGH",
            "Investigator": "Sarah Blair (L2)",
            "SLA Remaining": "6h 30m",
            "Status": "Under Review",
            "SAR Required": "YES"
        },
        {
            "Case ID": "CASE-455679",
            "Subject Entity": "Liam Johansson",
            "Typology": "Foreign Travel Outlier",
            "Risk Score": 58,
            "Priority": "P3 - MEDIUM",
            "Investigator": "Automated Engine",
            "SLA Remaining": "11h 00m",
            "Status": "Hold Released via OTP",
            "SAR Required": "NO"
        }
    ])
    st.dataframe(df_cases, use_container_width=True, hide_index=True)

    st.markdown("### 📝 Case Notes & Evidence Dossier")
    c_note1, c_note2 = st.columns([2, 1])
    with c_note1:
        st.text_area(
            "Investigator Log & Observations (CASE-455676)",
            value="Cross-correlated NetworkX simple_cycles output with Singapore and Dubai correspondent banks. Confirmed device collision on FP-8891-BRAVE. Ring controller identified. Recommend full freeze and FinCEN SAR filing."
        )
        if st.button("💾 Save Case Notes"):
            st.success("Case notes committed to immutable case folder.")
    with c_note2:
        st.markdown("**Evidence Locker Attachments**")
        st.markdown("- 📎 `NetworkX_Cycle_Topology.json`")
        st.markdown("- 📎 `Device_Fingerprint_Collision_Trace.pcap`")
        st.markdown("- 📎 `Correspondent_SWIFT_MT103_Logs.csv`")
        st.button("📥 Download Full Evidence Package")

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 4: 📜 FinCEN SAR FILINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif selected_nav == "📜 FinCEN SAR Filings":
    st.markdown("## 📜 FinCEN Suspicious Activity Report (SAR / Form 111) Drafter")
    st.caption("Automated regulatory filing preparation using graph topology evidence and narrative generation.")

    col_sar1, col_sar2 = st.columns([1, 1])
    with col_sar1:
        st.markdown("#### 📋 Filing Metadata")
        st.text_input("Filing Institution Name", "FINNEXUS Global Payments Inc.")
        st.text_input("BSA Identification Number (BIN)", "BIN-992019482")
        st.selectbox("Suspicious Activity Category", [
            "Money Laundering / Layering (Structuring)",
            "Account Takeover / Identity Theft",
            "Terrorist Financing Correlation",
            "Unauthorized Cyber Intrusions"
        ])
        st.selectbox("Primary Subject of Filing", [
            "Alice Whitmore (ACCT: US-ACH-4001928)",
            "Charlie Okafor (ACCT: SG-FAST-882019)",
            "Ethan Walsh (ACCT: US-CHASE-11082)"
        ])
        st.date_input("Suspicious Activity Period Start", value=datetime.now() - timedelta(days=1))
        st.date_input("Suspicious Activity Period End", value=datetime.now())

    with col_sar2:
        st.markdown("#### ✍️ Automated Regulatory Narrative")
        sar_narrative = (
            "NARRATIVE SECTION (FinCEN XML Form 111):\n\n"
            "Between 12:15:00 UTC and 12:17:00 UTC, the FINNEXUS automated detection engine isolated a closed "
            "circular layering ring involving four distinct corporate accounts across four jurisdictions (US, UK, "
            "Singapore, and UAE). Account US-ACH-4001928 (Alice Whitmore) transmitted $49,500 via international wire, "
            "which subsequently traversed UK-FPS-5192004 (Bob Nakamura), SG-FAST-882019 (Charlie Okafor), and "
            "AE-WPS-330198 (Diana Petrova) before returning $47,100 to the original sender account within 115 seconds. "
            "A hardware fingerprint collision (FP-8891-BRAVE) confirmed common syndicate control between the Singapore "
            "and UAE exit nodes. All four accounts have been placed under administrative freeze."
        )
        st.text_area("Narrative Text", value=sar_narrative, height=220)

    st.markdown("---")
    st.markdown("#### 🔐 Compliance Officer Digital Sign-Off")
    c_sign1, c_sign2 = st.columns([2, 1])
    with c_sign1:
        st.checkbox("I, Sarah Blair, certify under 31 U.S.C. 5318(g) that the suspicious activity details described above are true and complete to the best of my knowledge.")
    with c_sign2:
        if st.button("🚀 Sign & Transmit to FinCEN BSA Direct", type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ SAR-2026-009182 Successfully Transmitted to FinCEN BSA Direct Gateway. Confirmation Hash: 9f82a1c84b.")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. FLOATING CHATBOT TRIGGER (Bottom-Right Corner)
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🤖 FINNEXUS Assistant Sidebar")
    st.caption("Quick intelligence lookup across all suspect nodes.")
    side_q = st.text_input("Quick Graph Query:", placeholder="e.g. Ring #1 nodes")
    if side_q:
        st.info(query_ai_copilot(side_q, raw_incidents, current_cycles))

# Bottom right floating popover
float_col1, float_col2 = st.columns([11, 2])
with float_col2:
    with st.popover("💬 Copilot Assistant", help="Quick access to FINNEXUS AI Copilot"):
        st.markdown("##### 🤖 FINNEXUS AI Assistant")
        st.caption("Direct graph query interface:")
        p_q = st.text_input("Ask Copilot:", key="popover_query")
        if p_q:
            st.markdown(query_ai_copilot(p_q, raw_incidents, current_cycles))

# ── Footer ──
render_html("""
<div style="text-align:center;padding:26px 0 10px 0;">
    <span style="font-size:11px;color:#94A3B8;font-weight:600;letter-spacing:0.5px;">
        FINNEXUS ENTERPRISE COMPLIANCE SUITE · REAL-TIME FRAUD & AML RISK ORCHESTRATION CONSOLE
    </span>
</div>
""")

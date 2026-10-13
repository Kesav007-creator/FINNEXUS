#!/bin/bash
echo "========================================================"
echo "  FINNEXUS - Real-Time Fraud & AML Risk Orchestration"
echo "========================================================"
echo ""
echo "[1/2] Checking and installing dependencies..."
pip install -r requirements.txt --quiet
echo ""
echo "[2/2] Launching FINNEXUS in your default browser..."
echo ""
python3 -m streamlit run app.py

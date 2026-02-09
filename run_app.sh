#!/bin/bash
# Start the Elbow Interference Evaluator (Streamlit).
# Keep this terminal open while using the app.
cd "$(dirname "$0")"
echo "Starting app at http://localhost:8501 ..."
echo "Press Ctrl+C to stop."
python3 -m streamlit run app.py

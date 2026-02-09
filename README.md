# Elbow Interference Evaluator™

Strategic behavioral investment terminal for comparing CPG brands using the **Elbow Interference Theory™** (Russell Barnett © 2026). Evaluates two brands on the Satisfaction equation **S = (M×E×F) ÷ (B×K×C)** and generates comparison memos.

---

## Run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or:

```bash
python3 -m streamlit run app.py
```

Open the URL in your browser (e.g. `http://localhost:8501`).

---

## Optional: AI (Gemini) memos

For AI-generated brand analysis and investment memos:

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Create `.streamlit/secrets.toml` in the project root:

```toml
GEMINI_API_KEY = "your-key-here"
```

If no key is set, the app runs in **Manual Mode** (rule-based memos and manual score entry only).

---

## Project structure

| File | Purpose |
|------|--------|
| **app.py** | Streamlit UI: sidebar, brand inputs, file upload, session state, layout. Entrypoint. |
| **config.py** | Tooltips, default category, White Paper text for AI prompts. |
| **brands.py** | Archetypes, brand database, known scores, fuzzy brand lookup (`hunt_brand`, `normalize_brand_name`). |
| **scoring.py** | S-Score formula and rationale validation. |
| **ai_services.py** | Gemini integration: brand analysis, strategic synthesis, rule-based memo. |
| **priors.py** | Behavioral priors (cohort, occasion, promo, velocity adjustments). |
| **hard_data.py** | Deterministic constants and category benchmarks (see `hard_coded_rules.md`). |
| **test_priors.py** | Pytest tests for the priors module. |

---

## Tests (no manual running required)

Run the full automated test suite (scoring, brands, config, AI services, app smoke, priors):

```bash
python3 -m pytest
```

Or run with more output:

```bash
python3 -m pytest -v
```

(Use `python3` if `python` is not on your PATH, e.g. on macOS.)

All tests are headless: no browser, no Streamlit UI, no Gemini API calls (AI tests use the rule-based memo only).

**Copy rules:** Equation vs persistence is locked in and enforced by `test_copy_consistency.py`. See `COPY_RULES.md`.

---

## Uploads

The app accepts CSV/Excel (sales data) and PDF/Word/PPT/Text (brand or consumer docs). Uploaded content is used for context in generated memos and can auto-fill Advanced (priors) fields when column names match.

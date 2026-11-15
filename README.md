# Conversational AI for Economic Data Analysis Recommendation Engine

This project is a beginner-friendly conversational application for analyzing two Federal Reserve Economic Data (FRED) series. It uses transparent deterministic calculations so it runs without an API key.

- `GDP`: Gross Domestic Product
- `CPILFESL`: Consumer Price Index for All Urban Consumers, All Items Less Food and Energy (Core CPI)

The app retrieves current observations from FRED, calculates year-over-year changes, answers common questions, and displays a comparison chart.

## Run the project

From this folder, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown in the terminal, usually `http://localhost:8501`.

Run the automated checks with:

```bash
.venv/bin/pytest -q
```

## Economic methodology

- GDP growth uses the year-over-year percentage change in quarterly GDP.
- Core CPI inflation uses the year-over-year percentage change in the monthly Core CPI index.
- For the comparison chart, Core CPI is averaged by quarter so it can be compared with quarterly GDP.
- Correlation describes association; it does not establish causation.

## Files

- `app.py`: Streamlit user interface
- `data_analysis.py`: FRED retrieval, calculations, responses, and chart generation
- `technical_report.md`: report draft to complete before submission
- `sample_conversations.md`: sample testing evidence
- `architecture_diagram.mmd`: Mermaid architecture diagram
- `visualizations/gdp_vs_core_cpi.html`: exported comparison visualization
- `tests/test_data_analysis.py`: automated calculation tests


# Technical Report: Conversational AI for Economic Data Analysis

## 1. Introduction

This project develops a conversational AI application that enables users to ask natural-language questions about U.S. Gross Domestic Product (GDP) and Core Consumer Price Index (CPILFESL) data from the Federal Reserve Economic Data (FRED) platform.

## 2. Objective

The objective is to make economic data easier to explore by combining data retrieval, economic calculations, natural-language interaction, and visualization in one application.

## 3. Data sources

| Series | FRED ID | Description | Frequency |
|---|---|---|---|
| Gross Domestic Product | GDP | Current-dollar value of U.S. production | Quarterly |
| Core CPI | CPILFESL | CPI excluding food and energy | Monthly |

The application retrieves the series from FRED at runtime.

## 4. System architecture

The system begins with a user question in the Streamlit chat interface. The question is classified, the appropriate FRED data is loaded, calculations are performed, and a text response and/or chart is returned. See `architecture_diagram.mmd`.

## 5. Implementation

The application is implemented in Python using Streamlit, Pandas, and Plotly. `data_analysis.py` handles data retrieval and calculations. `app.py` provides the conversational interface and visualization. The response engine uses transparent deterministic routing and Pandas calculations, so the application does not require an API key.

## 6. Economic calculations

Year-over-year growth is calculated as:

```text
(current value / value four quarters earlier - 1) × 100
```

For Core CPI, the monthly index is compared with the index twelve months earlier. For the GDP/Core CPI comparison chart, monthly Core CPI observations are averaged by quarter to align them with quarterly GDP observations.

The project also includes automated tests for percentage-change calculations, correlation, and question routing.

## 7. Sample conversations

See `sample_conversations.md`. Add screenshots of at least three completed conversations here before submitting.

## 8. Findings

Complete this section after running the application:

- Describe the latest GDP observation and its growth rate.
- Describe the latest Core CPI inflation rate.
- Describe the ten-year GDP trend.
- Describe the five-year Core CPI trend.
- Report the correlation between GDP growth and Core CPI inflation.
- Explain whether the relationship appears strong, weak, positive, or negative.

## 9. Limitations

- FRED data may be revised after the original release.
- GDP and Core CPI have different reporting frequencies.
- Correlation does not prove causation.
- The basic question router supports common question types rather than every possible wording.

## 10. Future improvements

- Add an LLM intent-classification and explanation layer in a future version.
- Support custom date ranges.
- Add downloadable CSV and chart files.
- Add more FRED economic indicators.
- Add automated tests for calculations.


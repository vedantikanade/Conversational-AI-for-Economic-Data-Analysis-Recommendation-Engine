# Conversational AI for Economic Data Analysis Recommendation Engine

## 1. Introduction

This project presents a conversational economic data analysis application that allows users to ask natural-language questions about U.S. Gross Domestic Product (GDP) and Core Consumer Price Index (Core CPI) data. The application retrieves current and historical observations from the Federal Reserve Economic Data (FRED) platform, performs economic calculations, identifies trends, compares economic indicators, and presents results through written explanations and visualizations.

The purpose of the application is to make official economic data easier to explore. Instead of manually searching through FRED tables or calculating percentage changes, users can enter a question and receive a data-driven response.

## 2. Project Objective

The objective is to create an interactive application focused on two FRED datasets: GDP and Core CPI. The application supports questions about the latest observations, historical changes, GDP growth, inflation, the relationship between the indicators, and overall economic trends.

## 3. Data Sources

The application uses the following official FRED series:

- GDP: https://fred.stlouisfed.org/series/GDP
- Core CPI, series CPILFESL: https://fred.stlouisfed.org/series/CPILFESL

GDP is reported quarterly. Core CPI is reported monthly. The application downloads the live FRED observations at runtime using FRED CSV endpoints. This means that the latest available observations can be retrieved whenever the application is run.

## 4. Technologies Used

The application was developed using Python. Streamlit provides the web interface, Pandas handles data retrieval and analysis, and Plotly creates the interactive visualization. Pytest is used to test the calculation and question-routing functions.

The current version uses transparent deterministic question routing and Pandas calculations. It does not require an external API key, which makes the project reproducible and easy to run locally.

## 5. System Architecture

The system begins when a user enters a natural-language question in the Streamlit interface. The question is routed according to its topic, such as GDP, Core CPI, inflation, trends, comparison, visualization, or summary. The application retrieves the appropriate FRED data, cleans and aligns the observations, performs the required calculations, and displays the result.

GDP and Core CPI have different reporting frequencies. To compare them, the application converts the monthly Core CPI data into quarterly averages so it can be aligned with quarterly GDP data. The application then calculates year-over-year changes and creates a comparison chart.

**Insert `architecture_diagram.svg` here.**

**Figure 1. System architecture of the Conversational AI for Economic Data Analysis Recommendation Engine.**

## 6. Application Implementation

The Streamlit interface is implemented in `app.py`. It contains the project title, example questions, data-source links, a question input form, an Ask button, the latest question and answer, an economic visualization, raw observations, and a CSV download button.

The analysis functions are implemented in `data_analysis.py`. This file retrieves the two FRED series, calculates GDP growth and Core CPI inflation, measures the correlation between the indicators, summarizes trends, and creates the Plotly chart.

The application displays only the latest question and answer so that users are not confused by a long conversation history. The question field is cleared automatically after each submission.

## 7. Economic Calculations

GDP year-over-year growth is calculated using the current quarterly GDP value and the value from four quarters earlier:

```text
GDP growth = ((current GDP / GDP from four quarters earlier) - 1) × 100
```

Core CPI year-over-year inflation is calculated using the current monthly Core CPI index and the value from twelve months earlier:

```text
Core CPI inflation = ((current Core CPI / Core CPI from twelve months earlier) - 1) × 100
```

For the comparison chart, monthly Core CPI observations are averaged by quarter. The application then compares quarterly GDP growth with quarterly Core CPI inflation. Correlation measures association between the two variables; it does not prove causation.

## 8. Required Questions and Screenshot Placement

Insert the screenshots in the following locations in this section:

### 8.1 Application landing page

Insert the screenshot showing the application title, example questions, question input field, and data-source links.

**Figure 2. Application landing page.**

### 8.2 Latest GDP

Ask: “What is the latest reported U.S. GDP?” Insert the screenshot showing the question and the GDP answer directly below this paragraph.

**Figure 3. Latest reported GDP response.**

### 8.3 Ten-year GDP trend

Ask: “How has U.S. GDP changed over the past 10 years?” Insert a new screenshot where the complete answer is visible. The screenshot taken at 10:56:44 PM does not clearly show the complete answer, so retake this screenshot.

**Figure 4. Ten-year GDP trend response.**

### 8.4 Current Core CPI inflation

Ask: “What is the current Core CPI inflation rate?” Insert the screenshot showing the Core CPI index, date, and year-over-year inflation rate.

**Figure 5. Current Core CPI inflation response.**

### 8.5 Five-year Core CPI trend

Ask: “How has Core CPI inflation changed over the past five years?” Insert the screenshot showing the five-year percentage change.

**Figure 6. Five-year Core CPI trend response.**

### 8.6 Relationship between GDP and Core CPI

Ask: “What is the relationship between GDP growth and Core CPI inflation?” Insert the screenshot showing the correlation and the explanation that correlation does not prove causation.

**Figure 7. GDP growth and Core CPI relationship response.**

### 8.7 Visualization comparison

Ask: “Generate a visualization comparing GDP growth and Core CPI inflation over time.” Retake this screenshot after refreshing the updated application. The previous screenshot at 10:58:02 PM shows an older incorrect response and should not be used in the final report.

**Figure 8. GDP growth and Core CPI comparison visualization.**

### 8.8 Key economic trend summary

Ask: “Summarize the key economic trends observed in both datasets.” Retake this screenshot after refreshing the updated application. The previous screenshot at 10:58:18 PM shows the old fallback response and should not be used in the final report.

**Figure 9. Summary of key economic trends.**

## 9. Findings

At the time of analysis, the application retrieved the latest available GDP observation and calculated its year-over-year growth rate. The observed GDP value was approximately $33,010.0 billion for July 2026, with year-over-year growth of approximately 5.87%.

The latest observed Core CPI index was approximately 339.90 for October 2026. The calculated year-over-year Core CPI inflation rate was approximately 2.87%.

Over approximately the past ten years, GDP increased by about 74.72%. Over approximately the past five years, Core CPI increased by about 20.67%. These results show long-term economic expansion together with a continuing increase in the general price level excluding food and energy.

The calculated correlation between quarterly GDP growth and quarterly Core CPI inflation was approximately 0.53. This indicates a moderate positive association in the analyzed sample. However, the result does not prove that GDP growth causes inflation because other factors, such as interest rates, monetary policy, labor markets, and supply conditions, may affect both indicators.

## 10. Limitations

GDP and Core CPI are reported at different frequencies. The application addresses this by converting monthly Core CPI observations into quarterly averages, but this may remove some short-term monthly variation.

FRED observations may be revised after their initial publication. Therefore, results may change when the application is run at a later date.

The application is focused on GDP and Core CPI and does not currently analyze other indicators such as unemployment, interest rates, or stock prices. The question router supports the economic question types required for this assignment rather than every possible natural-language question.

## 11. Conclusion

This project demonstrates how a conversational interface can make official economic data easier to access and interpret. By combining FRED data retrieval, Pandas calculations, natural-language question routing, and Plotly visualization, the application allows users to explore GDP and Core CPI without manually calculating economic indicators.

The application retrieves current and historical observations, calculates economic measures, identifies trends, compares GDP growth with Core CPI inflation, and presents results through text and charts. Future improvements could include additional FRED indicators, custom date ranges, downloadable PDF reports, and a more advanced language-model layer.

## 12. Source Code

The source code is available at:

https://github.com/vedantikanade/Conversational-AI-for-Economic-Data-Analysis-Recommendation-Engine

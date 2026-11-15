"""Data retrieval and economic calculations for the GDP/Core CPI assistant."""

from __future__ import annotations

from typing import Dict

import pandas as pd


FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"


def load_fred_series(series_id: str) -> pd.DataFrame:
    """Download one FRED series and return a Date/Value dataframe."""
    url = FRED_CSV_URL.format(series_id=series_id)
    frame = pd.read_csv(url)
    frame["DATE"] = pd.to_datetime(frame["observation_date"])
    value_column = series_id.upper()
    frame["VALUE"] = pd.to_numeric(frame[value_column], errors="coerce")
    frame = frame[["DATE", "VALUE"]].dropna().sort_values("DATE")
    if frame.empty:
        raise ValueError(f"No observations were returned for FRED series {series_id}.")
    return frame.reset_index(drop=True)


def load_economic_data() -> Dict[str, pd.DataFrame]:
    """Load GDP and Core CPI, then create quarterly comparison data."""
    gdp = load_fred_series("GDP").rename(columns={"VALUE": "GDP"})
    cpi = load_fred_series("CPILFESL").rename(columns={"VALUE": "CORE_CPI"})

    # GDP is quarterly while Core CPI is monthly. Use quarterly averages for CPI
    # so the two series can be compared on the same time axis.
    gdp_quarterly = gdp.set_index("DATE")["GDP"].resample("QE").last().dropna()
    cpi_quarterly = cpi.set_index("DATE")["CORE_CPI"].resample("QE").mean().dropna()

    comparison = pd.concat([gdp_quarterly, cpi_quarterly], axis=1).dropna()
    comparison["GDP_GROWTH_YOY"] = comparison["GDP"].pct_change(4) * 100
    comparison["CORE_CPI_INFLATION_YOY"] = comparison["CORE_CPI"].pct_change(4) * 100
    comparison = comparison.dropna().reset_index()
    return {"gdp": gdp, "cpi": cpi, "comparison": comparison}


def latest_value(frame: pd.DataFrame, value_column: str) -> tuple[pd.Timestamp, float]:
    row = frame.dropna(subset=[value_column]).iloc[-1]
    return row["DATE"], float(row[value_column])


def percent_change(frame: pd.DataFrame, value_column: str, years: int) -> float:
    """Calculate the change between the latest value and an approximate past value."""
    work = frame.set_index("DATE")[value_column].dropna().sort_index()
    if work.empty:
        raise ValueError("There are no observations available for this calculation.")
    latest_date = work.index[-1]
    target_date = latest_date - pd.DateOffset(years=years)
    previous = work.loc[:target_date]
    if previous.empty:
        previous_value = work.iloc[0]
    else:
        previous_value = previous.iloc[-1]
    return float((work.iloc[-1] / previous_value - 1) * 100)


def correlation(comparison: pd.DataFrame) -> float:
    work = comparison[["GDP_GROWTH_YOY", "CORE_CPI_INFLATION_YOY"]].dropna()
    return float(work["GDP_GROWTH_YOY"].corr(work["CORE_CPI_INFLATION_YOY"]))


def format_date(value: pd.Timestamp) -> str:
    return value.strftime("%B %Y")


def answer_question(question: str, data: Dict[str, pd.DataFrame]) -> str:
    """Provide a transparent rule-based answer for common assignment questions."""
    text = question.lower()
    gdp = data["gdp"]
    cpi = data["cpi"]
    comparison = data["comparison"]

    gdp_date, gdp_value = latest_value(gdp, "GDP")
    cpi_date, cpi_value = latest_value(cpi, "CORE_CPI")

    if "summarize" in text or "summary" in text or "key trend" in text or "both dataset" in text:
        gdp_change = percent_change(gdp, "GDP", 10)
        cpi_change = percent_change(cpi, "CORE_CPI", 5)
        gdp_growth = gdp.set_index("DATE")["GDP"].pct_change(4).dropna().iloc[-1] * 100
        cpi_inflation = cpi.set_index("DATE")["CORE_CPI"].pct_change(12).dropna().iloc[-1] * 100
        corr = correlation(comparison)
        return (
            "Key trends: GDP has increased over the long term, rising "
            f"approximately {gdp_change:.2f}% over the last ten years. Core CPI has also "
            f"increased, rising approximately {cpi_change:.2f}% over the last five years. "
            f"The latest year-over-year GDP growth is {gdp_growth:.2f}%, while the latest "
            f"year-over-year Core CPI inflation rate is {cpi_inflation:.2f}%. The correlation "
            f"between quarterly GDP growth and Core CPI inflation is {corr:.2f}; this describes "
            "association, not causation."
        )

    if "visualiz" in text or "chart" in text or "graph" in text or "plot" in text:
        corr = correlation(comparison)
        return (
            "The GDP growth and Core CPI inflation comparison chart is displayed below. "
            f"The calculated correlation between the two year-over-year measures is {corr:.2f}. "
            "The chart uses quarterly data so the two indicators can be compared on the same timeline."
        )

    if "relationship" in text or "correlation" in text or "compare" in text:
        corr = correlation(comparison)
        direction = "positive" if corr > 0 else "negative" if corr < 0 else "very weak"
        return (
            f"Using year-over-year quarterly changes, the correlation between GDP growth "
            f"and Core CPI inflation is {corr:.2f}. This indicates a {direction} linear "
            "relationship in this sample. Correlation does not prove that one variable causes the other."
        )

    if "inflation" in text or "cpi" in text:
        inflation = cpi.set_index("DATE")["CORE_CPI"].pct_change(12).dropna().iloc[-1] * 100
        years = 5 if "five" in text or "5 year" in text or "5-year" in text else None
        trend = ""
        if years:
            change = percent_change(cpi, "CORE_CPI", years)
            trend = f" Over approximately the past five years, the index increased {change:.2f}%."
        return (
            f"The latest Core CPI index is {cpi_value:.2f} ({format_date(cpi_date)}). "
            f"The latest available year-over-year Core CPI inflation rate is {inflation:.2f}%.{trend}"
        )

    if "gdp" in text:
        growth = gdp.set_index("DATE")["GDP"].pct_change(4).dropna().iloc[-1] * 100
        change_10y = percent_change(gdp, "GDP", 10)
        return (
            f"The latest reported GDP is ${gdp_value:,.1f} billion ({format_date(gdp_date)}). "
            f"Its latest year-over-year growth rate is {growth:.2f}%, and GDP is "
            f"{change_10y:.2f}% higher than approximately ten years earlier."
        )

    return (
        "I can analyze GDP and Core CPI. Try asking about the latest GDP, GDP growth, "
        "Core CPI inflation, a five- or ten-year trend, or the relationship between the two."
    )


def create_comparison_chart(comparison: pd.DataFrame):
    """Return a Plotly chart comparing GDP growth and Core CPI inflation."""
    import plotly.graph_objects as go

    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=comparison["DATE"], y=comparison["GDP_GROWTH_YOY"],
        mode="lines+markers", name="GDP growth (YoY, %)",
    ))
    figure.add_trace(go.Scatter(
        x=comparison["DATE"], y=comparison["CORE_CPI_INFLATION_YOY"],
        mode="lines+markers", name="Core CPI inflation (YoY, %)",
    ))
    figure.update_layout(
        title="GDP Growth vs. Core CPI Inflation",
        xaxis_title="Quarter",
        yaxis_title="Year-over-year change (%)",
        hovermode="x unified",
        legend_title="Indicator",
    )
    return figure


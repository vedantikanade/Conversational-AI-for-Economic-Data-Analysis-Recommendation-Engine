import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_analysis import answer_question, correlation, percent_change


def sample_data():
    dates = pd.date_range("2019-03-31", periods=28, freq="QE")
    gdp = pd.DataFrame({"DATE": dates, "GDP": range(100, 128)})
    cpi = pd.DataFrame({"DATE": dates, "CORE_CPI": range(200, 228)})
    comparison = pd.DataFrame({
        "DATE": dates[4:],
        "GDP": range(104, 128),
        "CORE_CPI": range(204, 228),
        "GDP_GROWTH_YOY": [float(value) for value in range(1, 25)],
        "CORE_CPI_INFLATION_YOY": [float(value) * 0.5 for value in range(1, 25)],
    })
    return {"gdp": gdp, "cpi": cpi, "comparison": comparison}


def test_percent_change_returns_percentage():
    data = sample_data()
    result = percent_change(data["gdp"], "GDP", 5)
    assert result > 0


def test_correlation_returns_number():
    result = correlation(sample_data()["comparison"])
    assert round(result, 2) == 1.00


def test_question_router_mentions_gdp():
    response = answer_question("What is the latest GDP?", sample_data())
    assert "latest reported GDP" in response


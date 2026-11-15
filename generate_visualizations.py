"""Export the main economic comparison chart as an HTML file."""

from pathlib import Path

from data_analysis import create_comparison_chart, load_economic_data


output_folder = Path("visualizations")
output_folder.mkdir(exist_ok=True)
data = load_economic_data()
chart = create_comparison_chart(data["comparison"])
chart.write_html(output_folder / "gdp_vs_core_cpi.html")
print(f"Saved chart to {output_folder / 'gdp_vs_core_cpi.html'}")


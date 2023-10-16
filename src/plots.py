from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.io as pio

from metrics_calculation import create_metadata_label


def plot_figues(
    comsumption_data: pd.DataFrame, company_data: pd.DataFrame, output_directory: Path
):
    """
    Creates two figues of GHG emissions based on country and on year/energy type then save it as html and png.
    Args:
        comsumption_data: comsumtion of companies though years.
        company_data: overview of companies.
    """
    # Create figures
    create_metadata_label(comsumption_data=comsumption_data, company_data=company_data)
    fig_country = px.pie(
        comsumption_data,
        values="Total GHG emissions (tCO2eq)",
        names="Country",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hover_data=["Information"],
    )
    fig_country.update_layout(title="Total GHG emissions (tonnes CO2eq) per countries")

    fig_year_energy = px.histogram(
        comsumption_data,
        x="Year",
        y="normalized GHG emissions (tCO2eq)",
        color="Energy type",
    )
    fig_year_energy.update_layout(
        title="Total normalized GHG emissions (tonnes CO2eq) per year and energy type",
        yaxis_title="Total normalized GHG emissions (tonnes CO2eq)",
    )

    fig_year_energy.show()
    fig_country.show()

    fig_country.write_html(output_directory / "ghg_country.html")
    fig_year_energy.write_html(output_directory / "ghg_year_energy.html")

    pio.write_image(fig_country, output_directory / "ghg_country.png")
    pio.write_image(fig_year_energy, output_directory / "ghg_year_energy.png")

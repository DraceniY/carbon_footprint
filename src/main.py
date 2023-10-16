from pathlib import Path

import pandas as pd

from metrics_calculation import (
    normalized_ghg_emission,
    produce_datas,
    total_ghg,
    units_conversion,
)
from plots import plot_figues


def main():
    """
    Main function of the carbon_footprint program. In this function, we do the following tasks:
        1. Parse exercice xlsx file carbon_footprint and produce datas from the file.
        2. Convert metrics to ensure the uniformity.
        3. Calculate GHG emissions.
        4. Normalize GHG emissions.
        4. Display results as interactive plots and save them.
    """
    current_directory: Path = Path.cwd()
    carbon_footprint_file: Path = (
        current_directory / ".." / "data" / "Carbon footprint exercise.xlsx"
    )
    (
        comsumption_data,
        company_data,
        emission_fuel_data,
        emission_electricity_data,
        global_warming_data,
    ) = produce_datas(carbon_file=carbon_footprint_file)
    # Convert values to kWh and ft2 to m2 for Area
    comsumption_data, emission_fuel_data, company_data = units_conversion(
        comsumption_data, emission_fuel_data, company_data
    )
    # Calculate Total GHG
    comsumption_data = total_ghg(
        comsumption_data,
        emission_fuel_data,
        company_data,
        emission_electricity_data,
        global_warming_data,
    )
    # Normalized GHG data
    comsumption_data_normalized = normalized_ghg_emission(
        comsumption_data=comsumption_data
    )
    # Create output directory if it doesn't exist
    output_directory: Path = current_directory / ".." / "results"
    output_directory.mkdir(parents=True, exist_ok=True)
    # Plot figures and save them in html and png
    plot_figues(
        comsumption_data=comsumption_data_normalized,
        company_data=company_data,
        output_directory=output_directory,
    )
    with pd.ExcelWriter(output_directory / "data_results.xlsx") as writer:
        comsumption_data_normalized.to_excel(
            writer, sheet_name="Comsumption", index=False
        )
        company_data.to_excel(writer, sheet_name="Other Data", index=False)
        emission_electricity_data.to_excel(writer, sheet_name="Other Data", index=False)
        global_warming_data.to_excel(writer, sheet_name="Other Data", index=False)
        emission_fuel_data.to_excel(writer, sheet_name="Other Data", index=False)

    comsumption_data_normalized.to_excel("")


if __name__ == "__main__":
    # Call main function
    main()

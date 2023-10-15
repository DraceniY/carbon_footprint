from pathlib import Path
from typing import Dict

import pandas as pd


def produce_datas(
    carbon_file: Path,
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Function parse the xls file and return multiple dataframes.
        Args:
            carbon_file: Carbon footprint data xls file.
        Returns:
            comsumption_data: comsumtion of companies though years.
            company_data: overview of companies.
            emission_fuel_data: emission factors fuel data.
            emission_electricity_data: emission factors electricity data.
            global_warming_data: global warming data.
    """
    # current_directory : Path = Path.cwd()
    # carbon_file : Path = current_directory / "data" / "Carbon footprint exercise.xlsx"
    data: pd.DataFrame = pd.read_excel(
        carbon_file, sheet_name=["Comsumption", "Other Data"]
    )
    # Split big data into small dataframes
    # Sheet Comsumption data
    comsumption_data: pd.DataFrame = data["Comsumption"]
    # insure that the values are integer and not float
    comsumption_data["Value"] = comsumption_data["Value"].astype(int)
    comsumption_data["Year"] = comsumption_data["Date (DD-MM-YYYY)"].apply(
        lambda x: str(x).split("-")[0]
    )
    # Sheet Other data - Company Structure
    company_data: pd.DataFrame = data["Other Data"].iloc[2:9, 1:8]
    company_data = company_data.rename(
        columns={
            "Unnamed: 1": "Site name",
            "Unnamed: 2": "City",
            "Unnamed: 3": "Country",
            "Unnamed: 4": "Number of employees",
            "Unnamed: 5": "Status",
            "Unnamed: 6": "Area",
            "Unnamed: 7": "Unit Area",
        }
    )
    # Sheet Other data - Emission Factors Fuel
    emission_fuel_data: pd.DataFrame = data["Other Data"].iloc[28:37, [1, 2, 3, 4]]
    emission_fuel_data = emission_fuel_data.rename(
        columns={
            "Unnamed: 1": "Type of energy",
            "Unnamed: 2": "Unit",
            "Unnamed: 3": "GHG type",
            "Unnamed: 4": "gGHG/Unit",
        }
    )
    # Sheet Other data - Emission Factors Electricity
    emission_electricity_data: pd.DataFrame = data["Other Data"].iloc[40:45, [1, 2]]
    emission_electricity_data = emission_electricity_data.rename(
        columns={"Unnamed: 1": "Pays", "Unnamed: 2": "EF (kgCO2e/kwh)"}
    )
    # Sheet Other data - Global warming potential
    global_warming_data: pd.DataFrame = data["Other Data"].iloc[19:22, [9, 10]]
    global_warming_data = global_warming_data.rename(
        columns={"Unnamed: 9": "GHG Type", "Unnamed: 10": "GWP (gCO2e/gGHG)"}
    )

    return (
        comsumption_data,
        company_data,
        emission_fuel_data,
        emission_electricity_data,
        global_warming_data,
    )


def units_conversion(
    comsumption_data: pd.DataFrame,
    emission_fuel_data: pd.DataFrame,
    company_data: pd.DataFrame,
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Function converts the units of comsumption data and emission fuel to kWh and area of company overview to m2.
    Args:
        comsumption_data: comsumtion of companies though years.
        emission_fuel_data: emission factors fuel data.
        company_data: overview of companies.
    Returns:
        comsumption_data: comsumtion of companies though years "Values" column is converted to kWh unit.
        emission_fuel_data: emission factors fuel data "gGHG/Unit" column is converted to kWh unit.
        company_data: overview of companies "Area" column is converted to m2 unit.
    """
    # convert all to kWh
    # COMSUMTION DATA
    # if x == 'Gallons':
    # 1l = 0,264172 gallons
    # Gallons - Diesel
    comsumption_data.update(
        (
            comsumption_data[
                (comsumption_data["Unit "] == "Gallons")
                & (comsumption_data["Energy type"] == "Diesel")
            ]["Value"]
            / 0.264172
        )
        * 10
    )
    # kwh_gas = (x /0.264172) * 8.8
    comsumption_data.update(
        (
            comsumption_data[
                (comsumption_data["Unit "] == "Gallons")
                & (comsumption_data["Energy type"] == "Natural gas")
            ]["Value"]
            / 0.264172
        )
        * 0.0088
    )
    # kwh_propane = (x /0.264172) * 9.1
    comsumption_data.update(
        (
            comsumption_data[
                (comsumption_data["Unit "] == "Gallons")
                & (comsumption_data["Energy type"] == "Propane")
            ]["Value"]
            / 0.264172
        )
        * 9.1
    )

    # elif x == 'Liters':
    # kwh_diesel = x * 10
    comsumption_data.update(
        comsumption_data[
            (comsumption_data["Unit "] == "Liters")
            & (comsumption_data["Energy type"] == "Diesel")
        ]["Value"]
        * 10
    )
    # kwh_gas = x * 0.0088
    comsumption_data.update(
        comsumption_data[
            (comsumption_data["Unit "] == "Liters")
            & (comsumption_data["Energy type"] == "Natural gas")
        ]["Value"]
        * 0.0088
    )
    # kwh_propane = x * 9.1
    comsumption_data.update(
        comsumption_data[
            (comsumption_data["Unit "] == "Liters")
            & (comsumption_data["Energy type"] == "Propane")
        ]["Value"]
        * 9.1
    )
    # EMISION FACTOR FUEL
    # elif x == 'MMBtu':
    # 1 MMBTU = 293.07107 kWh
    # kwh = x * 293.07107
    emission_fuel_data.update(
        emission_fuel_data[emission_fuel_data["Unit"] == "MMBtu"]["gGHG/Unit"]
        * 0.000293071
    )
    # elif x == 'MWh':
    # kwh = x * 1000
    comsumption_data.update(
        comsumption_data[
            (comsumption_data["Unit "] == "MWh")
            & (comsumption_data["Energy type"] == "Electricity")
        ]["Value"]
        * 1000
    )
    comsumption_data["Unit "] = "kWh"
    emission_fuel_data["Unit"] = "kWh"

    company_data["Area"].update(
        company_data[company_data["Unit Area"] == "ft2"]["Area"] * 0.092903
    )
    company_data["Unit Area"] = "m2"

    return comsumption_data, emission_fuel_data, company_data


def total_ghg(
    comsumption_data: pd.DataFrame,
    emission_fuel_data: pd.DataFrame,
    company_data: pd.DataFrame,
    emission_electricity_data: pd.DataFrame,
    global_warming_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Function calculates Total GHG emissions.
    Args:
        comsumption_data: comsumtion of companies though years.
        company_data: overview of companies.
        emission_fuel_data: emission factors fuel data.
        emission_electricity_data: emission factors electricity data.
        global_warming_data: global warming data.
    Returns:
        comsumption_data: comsumtion of companies though years with column of total GHG emissions.
    """
    # TODO convert to liters depends on energy type
    # Calculation formula: Total GHG emissions (tCO2eq) = Energy consumption * Emission factors * Global Warming Potential (GWP)
    site_to_country: Dict[str, str] = company_data.set_index("Site name")[
        "Country"
    ].to_dict()
    comsumption_data["Country"] = comsumption_data["Site name"].replace(site_to_country)
    comsumption_data["Total GHG emissions (tCO2eq)"] = 0.0

    for ghg_type, gwp in (
        global_warming_data.set_index("GHG Type")["GWP (gCO2e/gGHG)"].to_dict().items()
    ):
        for energy_type in ["Diesel", "Natural gas", "Propane"]:
            # 1kg -> 0.001 Tonnes
            current_cell = emission_fuel_data[
                (emission_fuel_data["Type of energy"] == energy_type)
                & (emission_fuel_data["GHG type"] == ghg_type)
            ]["gGHG/Unit"]
            comsumption_data["Total GHG emissions (tCO2eq)"].update(
                comsumption_data[comsumption_data["Energy type"] == energy_type][
                    "Value"
                ]
                * (current_cell[current_cell.index[0]])
                * gwp
                * 0.001
            )

    for country, ef in (
        emission_electricity_data.set_index("Pays")["EF (kgCO2e/kwh)"].to_dict().items()
    ):
        # 1 gCO2eq/kWh = 1 ton of CO2eq/GWh -> 1000 (0.001*1000000) KgCO2eq/kWh = 1 ton of CO2eq/Kwh
        comsumption_data["Total GHG emissions (tCO2eq)"].update(
            comsumption_data[
                (comsumption_data["Country"] == country)
                & (comsumption_data["Energy type"] == "Electricity")
            ]["Value"]
            * ef
            * 1000
        )

    return comsumption_data


def create_metadata_label(
    company_data: pd.DataFrame, comsumption_data: pd.DataFrame
) -> None:
    """
    Function concatenate company columns into a column information and site and country columns into Site_country column.
    Args:
        comsumption_data: comsumtion of companies though years.
        company_data: overview of companies.
    """
    company_data["Information"] = (
        company_data["Site name"].astype(str)
        + " ("
        + company_data["City"].astype(str)
        + " - "
        + company_data["Country"].astype(str)
        + "), Status: "
        + company_data["Status"].astype(str)
        + ", Number of employees: "
        + company_data["Number of employees"].astype(str)
        + ", Area: "
        + company_data["Area"].astype(str)
        + " m2"
    )
    company_data["Site_country"] = (
        company_data["Site name"].astype(str) + " " + company_data["Country"]
    )
    comsumption_data["Site_country"] = (
        comsumption_data["Site name"].astype(str) + " " + comsumption_data["Country"]
    )
    metadata_dict = company_data.set_index("Site_country")["Information"].to_dict()
    comsumption_data["Information"] = comsumption_data["Site_country"].replace(
        metadata_dict
    )


def normalized_ghg_emission(comsumption_data: pd.DataFrame) -> pd.DataFrame:
    """
    Function creates a normalized the GhG values and saves it to a column ghg_normalized.
    Args:
        comsumption_data: comsumtion of companies though years.
    Returns:
        comsumption_data: comsumtion of companies though years with normalized GHG column added.
    """
    mean = comsumption_data["Total GHG emissions (tCO2eq)"].mean()
    standard_deviation = comsumption_data["Total GHG emissions (tCO2eq)"].std()
    comsumption_data["normalized GHG emissions (tCO2eq)"] = (
        comsumption_data["Total GHG emissions (tCO2eq)"] - mean
    ) / standard_deviation

    return comsumption_data

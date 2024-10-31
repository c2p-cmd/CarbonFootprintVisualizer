from pandas import DataFrame


def make_dataframe(
    company_name: str,
    avg_electric_bill: float,
    avg_gas_bill: float,
    avg_transport_bill: float,
    monthly_waste_generated: float,
    recycled_waster_percent: float,
    annual_travel_kms: float,
    fuel_efficiency: float,
) -> DataFrame:
    energy_usage = (
        (avg_electric_bill * 12 * 5e-4)
        + (avg_gas_bill * 12 * 5.3e-3)
        + (avg_transport_bill * 12 * 2.32)
    )
    waste_generated = monthly_waste_generated * 12 * 0.57 - recycled_waster_percent
    business_travel = annual_travel_kms * 1 / 6.5 * 2.31

    return DataFrame(
        {
            "Name": company_name,
            "Category": ["Energy Usage", "Waste Generated", "Business Travel"],
            "Value": [energy_usage, waste_generated, business_travel],
        }
    )

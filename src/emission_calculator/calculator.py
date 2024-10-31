from pandas import DataFrame

from plotly.graph_objects import Figure, Pie, Bar, Scatter


def draw_report_figure(df: DataFrame) -> Figure:
    from plotly.subplots import make_subplots

    figure_specs = [
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "domain"}, None],
    ]

    fig = make_subplots(
        rows=2,
        cols=2,
        specs=figure_specs,
        subplot_titles=(
            "Carbon Emission by Category",
            "Cumulative Emission %",
            "Emission Distribution",
        ),
    )

    # Pie chart settings
    pie_pull = [0.15 if x == min(df["Value"]) else 0.0 for x in df["Value"]]
    fig.add_trace(
        Pie(
            values=df["Value"],
            labels=df["Category"],
            hole=0.3,
            pull=pie_pull,
            name="Emission Distribution",
            marker={"colors": ["#6DA34D", "#81C3D7", "#FFC857"]},
        ),
        row=2,
        col=1,
    )

    # Bar chart for emissions by category
    fig.add_trace(
        Bar(
            x=df["Category"],
            y=df["Value"],
            name="Carbon Emission (kgCO2)",
            marker_color=["#6DA34D", "#81C3D7", "#FFC857"],
        ),
        row=1,
        col=1,
    )

    # Annotation for highest emission
    fig.add_annotation(
        x=df["Category"][df["Value"].idxmax()],
        y=df["Value"].max(),
        text="Highest Emission",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        row=1,
        col=1,
    )

    # Cumulative line chart
    cumulative_percentage = (df["Value"].cumsum() / df["Value"].sum()) * 100
    fig.add_trace(
        Scatter(
            x=df["Category"],
            y=cumulative_percentage,
            name="Cumulative %",
            mode="lines+markers",
            line=dict(color="#333333", dash="dash"),
        ),
        row=1,
        col=2,
    )

    # Update layout for axes and overall layout
    fig.update_layout(
        title_text=f"Carbon Footprint of {df['Name']}",
        plot_bgcolor="white",
        legend_title_text="Breakdown",
        xaxis_title="Emission Category",
        yaxis_title="Carbon Emission (kgCO2)",
        yaxis=dict(
            linecolor="black",
            showline=True,
            ticks="outside",
            mirror=True,
            gridcolor="lightgrey",
        ),
        yaxis2=dict(
            title="Cumulative Percentage",
            side="right",
            showgrid=False,
        ),
        legend=dict(
            x=1,  # Horizontal position (1 for right)
            y=0,  # Vertical position (0 for bottom)
            xanchor="right",
            yanchor="bottom",
            orientation="h",  # Horizontal layout for compactness
        ),
    )

    fig.update_xaxes(
        linecolor="black",
        ticks="outside",
        showline=True,
        mirror=True,
    )
    fig.update_yaxes(
        linecolor="black",
        showline=True,
        ticks="outside",
        mirror=True,
        gridcolor="lightgrey",
    )

    return fig


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
    business_travel = annual_travel_kms * 1 / fuel_efficiency * 2.31

    return DataFrame(
        {
            "Name": company_name,
            "Category": ["Energy Usage", "Waste Generated", "Business Travel"],
            "Value": [energy_usage, waste_generated, business_travel],
        }
    )

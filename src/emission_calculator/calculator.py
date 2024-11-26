from pandas import DataFrame

from plotly.subplots import make_subplots
from plotly.graph_objects import Figure, Pie, Bar, Scatter, Scatterpolar


def draw_report_figure(
    df: DataFrame, threshold: tuple[float] = [15_000, 5_000, 15_000]
) -> Figure:
    figure_specs = [
        [{"type": "xy"}, {"type": "domain"}],
        [{"type": "xy"}, {"type": "xy"}],
    ]

    fig = make_subplots(
        rows=2,
        cols=2,
        specs=figure_specs,
        subplot_titles=(
            "Carbon Emission by Category",
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
        row=1,
        col=2,
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

    # Update layout for axes and overall layout
    fig.update_layout(
        title_text=f"Carbon Footprint of {df['Name'][0]}",
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
        legend=dict(
            x=1,
            y=0,
            xanchor="right",
            yanchor="bottom",
            orientation="h",
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

    # Add a single general recommendation text box
    e, w, b = df["Value"]
    threshold_values = [e >= threshold[0], w >= threshold[1], b >= threshold[2]]
    recommendations = []
    texts = [
        "- Reduce energy usage by adopting energy-efficient practices.\n",
        "- Minimize waste by recycling and using sustainable materials.\n",
        "- Limit business travel and opt for virtual meetings where possible."
    ]
    if any(threshold_values):
        fig.add_annotation(
            text=("Recommendations to reduce carbon footprint:\n"),
            xref="paper",
            yref="paper",
            x=0,
            y=0.2,  # Positioning inside the plot area, just below center
            showarrow=False,
            font=dict(size=12),
            align="center",
            bordercolor="black",
            borderwidth=1,
            borderpad=10,
            bgcolor="lightyellow",
        )
        if threshold_values[0]:
            recommendations.append(texts[0]) 
        if threshold_values[1]:
            recommendations.append(texts[1])
        if threshold_values[2]:
            recommendations.append(texts[2]) 

    for i, text in enumerate(recommendations):
        fig.add_annotation(
            text=(text),
            xref="paper",
            yref="paper",
            x=0,
            y=(i + 1) * 0.05,  # Positioning inside the plot area, just below center
            showarrow=False,
            font=dict(size=12),
            align="center",
            bordercolor="black",
            borderwidth=1,
            borderpad=10,
            bgcolor="lightyellow",
        )

    return fig


def draw_historic_figure(df: DataFrame) -> Figure:
    # Create subplots with 2 rows and 1 column
    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "xy"}], [{"type": "polar"}]],
        subplot_titles=(
            "Total Carbon Footprint by Company",
            "Company Metrics Radar Chart",
        ),
        row_heights=[0.6, 0.4],
    )

    # Calculate each company's total carbon footprint as the sum of the three metrics
    df["Carbon Footprint"] = (
        df["Energy Usage"] + df["Waste Generated"] + df["Business Travel"]
    )

    # Add gradient-filled area trace for the Carbon Footprint
    fig.add_trace(
        Scatter(
            x=df["Name"],
            y=df["Carbon Footprint"],
            mode="lines",
            fill="tozeroy",
            line=dict(color="blue"),
            fillcolor="rgba(31, 119, 180, 0.5)",  # Gradient fill for blue
            name="Carbon Footprint",
        ),
        row=1,
        col=1,
    )

    # Prepare data for radar chart (normalizing values for better comparability)
    categories = ["Energy Usage", "Waste Generated", "Business Travel"]
    for _, company in df.iterrows():
        fig.add_trace(
            Scatterpolar(
                r=[
                    company["Energy Usage"],
                    company["Waste Generated"],
                    company["Business Travel"],
                    company["Energy Usage"],  # Closing the loop
                ],
                theta=categories + [categories[0]],  # Circular radar plot
                fill="toself",
                name=company["Name"],
            ),
            row=2,
            col=1,
        )

    # Update layout for the figure
    fig.update_layout(
        title="Company Metrics Visualization",
        template="plotly_white",
        height=800,
        width=1000,
        showlegend=True,
        legend=dict(x=1.05, y=1),  # Adjust legend position
    )

    # Update x and y-axis titles for the first plot
    fig.update_xaxes(title_text="Company", row=1, col=1)
    fig.update_yaxes(title_text="Carbon Footprint (total)", row=1, col=1)

    # Customize polar (radar) chart layout
    fig.update_polars(
        radialaxis=dict(
            visible=True,
            range=[
                df[categories].values.min(),
                df[categories].values.max(),
            ],
        )
    )

    return fig


def make_dataframe(
    company_name: str,
    avg_electric_bill: float,
    avg_gas_bill: float,
    avg_transport_bill: float,
    monthly_waste_generated: float,
    recycled_waste_percent: float,
    annual_travel_kms: float,
    fuel_efficiency: float,
) -> DataFrame:
    energy_usage = (
        (avg_electric_bill * 12 * 5e-4)
        + (avg_gas_bill * 12 * 5.3e-3)
        + (avg_transport_bill * 12 * 2.32)
    )
    waste_generated = monthly_waste_generated * 12 * 0.57 - recycled_waste_percent
    business_travel = annual_travel_kms * 1 / fuel_efficiency * 2.31

    return DataFrame(
        {
            "Name": company_name,
            "Category": ["Energy Usage", "Waste Generated", "Business Travel"],
            "Value": [energy_usage, waste_generated, business_travel],
        }
    )


def dataframe_to_dict(df: DataFrame) -> dict:
    return {
        "Name": df["Name"][0],
        "Energy Usage": df["Value"][0],
        "Waste Generated": df["Value"][1],
        "Business Travel": df["Value"][2],
    }

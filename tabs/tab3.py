from shiny import ui, render
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Load the original RpoPlan dataset.
RpoPlan = pd.read_csv("data/RpoPlan.csv")

# Constant column names.
X_COL = "positionDepRelToChiefLvlhZ"
Y_COL = "positionDepRelToChiefLvlhY"
Z_COL = "positionDepRelToChiefLvlhX"
T_COL = "secondsSinceStart"

# ---------------------------
# Maneuver markers helper.
def get_maneuver_markers():
    maneuver_df = pd.read_csv("data/ManeuverPlan.csv")
    merged = pd.merge(maneuver_df, RpoPlan, on=T_COL, how="inner")
    hover_temp = (
        "maneuverId: %{customdata[0]}<br>"
        "x: %{x}<br>y: %{y}<br>z: %{z}<br>"
        "dVLvlhX: %{customdata[1]}<br>dVLvlhY: %{customdata[2]}<br>dVLvlhZ: %{customdata[3]}<extra></extra>"
    )
    trace = go.Scatter3d(
        x=merged[X_COL],
        y=merged[Y_COL],
        z=merged[Z_COL],
        mode="markers",
        marker=dict(
            symbol="diamond",
            size=4,
            color="red"
        ),
        name="Maneuver Markers",
        customdata=merged[["maneuverId", "dVLvlhX", "dVLvlhY", "dVLvlhZ"]].values,
        hovertemplate=hover_temp
    )
    return trace

# ---------------------------
# Continuous variable plot helper.
def plot_continuous(c_col, colorbar_title):
    c_scale = "Hot"
    c_min = RpoPlan[c_col].min()
    c_max = RpoPlan[c_col].max()
    hover_temp = f"x: %{{x}}<br>y: %{{y}}<br>z: %{{z}}<br>{c_col}: %{{customdata[0]}}<extra></extra>"
    main_trace = go.Scatter3d(
        x=RpoPlan[X_COL],
        y=RpoPlan[Y_COL],
        z=RpoPlan[Z_COL],
        mode='lines',
        line=dict(
            width=4,
            dash="solid",
            color=RpoPlan[c_col],
            colorscale=c_scale,
            cmin=c_min,
            cmax=c_max
        ),
        name="RpoPlan",
        customdata=RpoPlan[[c_col]].values,
        hovertemplate=hover_temp
    )
    dummy_trace = go.Scatter3d(
        x=[RpoPlan[X_COL].iloc[0]],
        y=[RpoPlan[Y_COL].iloc[0]],
        z=[RpoPlan[Z_COL].iloc[0]],
        mode='markers',
        marker=dict(
            size=0,
            color=RpoPlan[c_col].iloc[0],
            colorscale=c_scale,
            cmin=c_min,
            cmax=c_max,
            colorbar=dict(title=colorbar_title),
            showscale=True
        ),
        hoverinfo='none',
        showlegend=False
    )
    fig = go.Figure(data=[main_trace, dummy_trace, get_maneuver_markers()])
    fig.update_layout(
        height=800,
        width=1000,
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            xaxis_title="C (km)",
            yaxis_title="I (km)",
            zaxis_title="R (km)"
        ),
        autosize=True,
        hovermode="closest"
    )
    return fig

# ---------------------------
# Categorical variable plot helper.
def plot_categorical(c_col, mapping):
    # For missionSegment, use Dark24; otherwise, use Dark2.
    if c_col == "missionSegment":
        colors = px.colors.qualitative.Dark24
    else:
        colors = px.colors.qualitative.Dark2
    raw_values = sorted(RpoPlan[c_col].unique())
    color_map = {raw: colors[i % len(colors)] for i, raw in enumerate(raw_values)}
    label_values = RpoPlan[c_col].map(lambda x: mapping.get(x, x)).tolist()
    hover_temp = f"x: %{{x}}<br>y: %{{y}}<br>z: %{{z}}<br>{c_col}: %{{customdata[0]}}<extra></extra>"
    main_trace = go.Scatter3d(
        x=RpoPlan[X_COL],
        y=RpoPlan[Y_COL],
        z=RpoPlan[Z_COL],
        mode='lines',
        line=dict(
            width=4,
            dash="solid",
            color=[color_map[val] for val in RpoPlan[c_col]]
        ),
        name="RpoPlan",
        customdata=[[label] for label in label_values],
        hovertemplate=hover_temp,
        showlegend=False
    )
    legend_traces = [
        go.Scatter3d(
            x=[None],
            y=[None],
            z=[None],
            mode='markers',
            marker=dict(size=10, color=color_map[raw]),
            name=mapping.get(raw, raw)
        )
        for raw in raw_values
    ]
    fig = go.Figure(data=[main_trace] + legend_traces)
    fig.add_trace(get_maneuver_markers())
    fig.update_layout(
        height=800,
        width=1000,
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            xaxis_title="C (km)",
            yaxis_title="I (km)",
            zaxis_title="R (km)"
        ),
        autosize=True,
        hovermode="closest"
    )
    return fig

# ---------------------------
# Mapping dictionaries for categorical variables.
attitude_mapping = {1: "Solar", 2: "LVLH", 3: "Lunar", 4: "RSO Tracking"}
eclipse_mapping = {0: "No Eclipse", 1: "Partial Eclipse (penumbra)", 2: "Eclipse (umbra)"}
navigation_mapping = {1: "Ground", 2: "AON (angles-only navigation)", 3: "CVN (computer vision navigation)"}
mission_mapping = {
    1: "Rendezvous", 2: "Acquisition", 3: "NMC 1 (Natural Motion Circumnavigation)",
    4: "NMC 2", 5: "NMC 3", 6: "Transfer", 7: "DSK 1 (Dynamic Station-Keeping)",
    8: "Transfer", 9: "DSK 2", 10: "Transfer", 11: "CFMC 1 (Circular Forced Motion Circumnavigation)",
    12: "CFMC 2", 13: "Solar Rephasing", 14: "NMC 4", 15: "Station-Keeping", 16: "NMC 5"
}

# ---------------------------
# Dropdown mapping.
continuous_options = {
    "Range": "relativeRange",
    "Velocity": "relativeVelocity",
    "relativeRangeRate": "relativeRangeRate",
    "sensorAngleToSun": "sensorAngleToSun",
    "sensorAngleToMoon": "sensorAngleToMoon",
    "sensorAngleToEarth": "sensorAngleToEarth",
    "earthHalfAngle": "earthHalfAngle",
    "lunarPhaseAngle": "lunarPhaseAngle",
    "lunarPercentIlluminated": "lunarPercentIlluminated",
    "storedData": "storedData"
}
categorical_options = {
    "attitudeMode": "attitudeMode",
    "eclipseTypeChief": "eclipseTypeChief",
    "eclipseTypeDeputy": "eclipseTypeDeputy",
    "navigationMethod": "navigationMethod",
    "missionSegment": "missionSegment"
}
all_options = {**continuous_options, **categorical_options}

# ---------------------------
# UI for Tab 3.
tab_ui = ui.nav_panel("RPO Plan Plots",
    ui.row(
        ui.column(3,
            ui.h3("Options"),
            ui.input_select("color_option", "Coloring Option", all_options)
        ),
        ui.column(8,
            ui.output_ui("plot3")
        )
    )
)

# ---------------------------
# Server function.
def server(input, output, session):
    @render.ui
    def plot3():
        option = input.color_option()
        if option in continuous_options.values():
            fig = plot_continuous(option, option)
        elif option in categorical_options.values():
            if option == "attitudeMode":
                fig = plot_categorical(option, attitude_mapping)
            elif option in ["eclipseTypeChief", "eclipseTypeDeputy"]:
                fig = plot_categorical(option, eclipse_mapping)
            elif option == "navigationMethod":
                fig = plot_categorical(option, navigation_mapping)
            elif option == "missionSegment":
                fig = plot_categorical(option, mission_mapping)
            else:
                fig = plot_categorical(option, {})
        else:
            fig = plot_continuous("relativeRange", "relativeRange")
        return ui.HTML(fig.to_html())

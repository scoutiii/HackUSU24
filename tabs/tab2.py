from shiny import ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Read initial dataset (if needed elsewhere)
RpoPlan = pd.read_csv("data/RpoPlan.csv")

# Define the common column names
x_col = "positionDepRelToChiefLvlhZ"
y_col = "positionDepRelToChiefLvlhY"
z_col = "positionDepRelToChiefLvlhX"
t_col = "secondsSinceStart"

def get_maneuver_markers(branch_threshold):
    # Read the ManeuverPlan file.
    maneuver_df = pd.read_csv("data/ManeuverPlan.csv")
    # Merge with RpoPlan on secondsSinceStart.
    merged = pd.merge(maneuver_df, RpoPlan, on=t_col, how="inner")
    
    # Split into maneuvers that occur before (pre) and after (post) the branch threshold.
    pre_maneuvers = merged[merged[t_col] < branch_threshold]
    post_maneuvers = merged[merged[t_col] >= branch_threshold]
    
    # Hover template that includes maneuverId and the dVLvlh components.
    hover_temp = (
        "maneuverId: %{customdata[0]}<br>"
        "dVLvlhX: %{customdata[1]}<br>dVLvlhY: %{customdata[2]}<br>dVLvlhZ: %{customdata[3]}<extra></extra>"
    )
    
    traces = []
    if not pre_maneuvers.empty:
        pre_trace = go.Scatter3d(
            x=pre_maneuvers[x_col],
            y=pre_maneuvers[y_col],
            z=pre_maneuvers[z_col],
            mode="markers",
            marker=dict(
                symbol="diamond",
                size=4,
                color="red"
            ),
            name="Pre Maneuver Markers",
            customdata=pre_maneuvers[["maneuverId", "dVLvlhX", "dVLvlhY", "dVLvlhZ"]].values,
            hovertemplate=hover_temp
        )
        traces.append(pre_trace)
    
    if not post_maneuvers.empty:
        post_trace = go.Scatter3d(
            x=post_maneuvers[x_col],
            y=post_maneuvers[y_col],
            z=post_maneuvers[z_col],
            mode="markers",
            marker=dict(
                symbol="diamond",
                size=4,
                color="rgba(128,128,128,0.7)"
            ),
            name="Post Maneuver Markers",
            customdata=post_maneuvers[["maneuverId", "dVLvlhX", "dVLvlhY", "dVLvlhZ"]].values,
            hovertemplate=hover_temp
        )
        traces.append(post_trace)
    
    return traces

# Define UI for Tab 2 with additional controls for coloring and inequality toggle
tab_ui = ui.nav_panel("3D Maneuver Branch",
    ui.row(
        ui.column(3,
            ui.h3("Options"),
            # Branch number input
            ui.input_numeric("branch_number", "Branch Number", value=1, min=1, max=47, step=1),
            # Hard Deck input (default 100 for Range; will be overridden to 0 for Velocity)
            ui.input_numeric("hard_deck", "Hard Deck", value=100, min=0, step=1),
            # Dropdown to choose the coloring option: Range or Velocity
            ui.input_select("color_option", "Coloring Option", {"Range": "Range", "Velocity": "Velocity"}),
            # Toggle: if checked, mark points where chosen column > Hard Deck; if unchecked, mark points where chosen column < Hard Deck.
            # Default is now False.
            ui.input_checkbox("inequality_toggle", "Mark points where value > Hard Deck (uncheck for < Hard Deck)", value=False)
        ),
        ui.column(8,
            ui.output_ui("plot2")  # Render the interactive Plotly plot as HTML
        )
    )
)

def server(input, output, session):
    @render.ui
    def plot2():
        # Determine which column to use for coloring based on the dropdown selection.
        color_choice = input.color_option()
        if color_choice == "Range":
            c_col = "relativeRange"
            c_scale = "Hot_r"
        else:
            c_col = "relativeVelocity"
            c_scale = "Hot"
        
        # Get color scale limits from RpoPlan.
        c_min = RpoPlan[c_col].min()
        c_max = RpoPlan[c_col].max()
        
        # Get the selected branch number and hard deck value.
        branch_num = input.branch_number()
        hard_deck_val = input.hard_deck()
        
        # Load branch data.
        csv_file = os.path.join("data", f"ManeuverBranchId{branch_num}.csv")
        branch_data = pd.read_csv(csv_file)
        
        # Determine branch threshold using the smallest secondsSinceStart in branch_data.
        branch_threshold = branch_data[t_col].min()
        
        # Split RpoPlan into pre-branch and post-branch data.
        pre_data = RpoPlan[RpoPlan[t_col] < branch_threshold]
        post_data = RpoPlan[RpoPlan[t_col] >= branch_threshold]
        
        # Define a hover template for RpoPlan traces.
        hover_temp = f"x: %{{x}}<br>y: %{{y}}<br>z: %{{z}}<br>{c_col}: %{{customdata[0]}}<extra></extra>"
        
        # Create the pre-branch trace.
        pre_trace = go.Scatter3d(
            x=pre_data[x_col],
            y=pre_data[y_col],
            z=pre_data[z_col],
            mode='lines',
            line=dict(
                width=4,
                dash="solid",
                color=pre_data[c_col],
                colorscale=c_scale,
                cmin=c_min,
                cmax=c_max,
            ),
            name="RpoPlan (Pre-Branch)",
            customdata=pre_data[[c_col]].values,
            hovertemplate=hover_temp
        )
        
        # Create the post-branch trace.
        post_trace = go.Scatter3d(
            x=post_data[x_col],
            y=post_data[y_col],
            z=post_data[z_col],
            mode='lines',
            line=dict(
                width=4,
                dash="dash",
                color="rgba(64, 64, 64, 0.5)",
            ),
            name="RpoPlan (Post-Branch)",
            customdata=post_data[[c_col]].values,
            hovertemplate=hover_temp
        )
        
        # Create the branch trace.
        branch_trace = go.Scatter3d(
            x=branch_data[x_col],
            y=branch_data[y_col],
            z=branch_data[z_col],
            mode='lines',
            line=dict(
                width=24,
                dash="solid",
                color=branch_data[c_col],
                colorscale=c_scale,
                cmin=c_min,
                cmax=c_max
            ),
            name=f"Branch {branch_num}",
            customdata=branch_data[[c_col]].values,
            hovertemplate=hover_temp
        )
        
        # Add a text marker ("O") at the start of branch_data.
        branch_start_trace = go.Scatter3d(
            x=[branch_data[x_col].iloc[0]],
            y=[branch_data[y_col].iloc[0]],
            z=[branch_data[z_col].iloc[0]],
            mode='text',
            text=["O"],
            textposition="middle center",
            textfont=dict(size=20, color="black"),
            name=f"Branch {branch_num} Starts"
        )
        
        # Combine the RpoPlan traces.
        datas = [pre_trace, post_trace, branch_trace, branch_start_trace]
        
        # Get the inequality toggle value and add corresponding markers.
        inequality_gt = input.inequality_toggle()
        if inequality_gt:
            pre_hd = pre_data[pre_data[c_col] > hard_deck_val]
        else:
            pre_hd = pre_data[pre_data[c_col] < hard_deck_val]
        if not pre_hd.empty:
            pre_hd_trace = go.Scatter3d(
                x=pre_hd[x_col],
                y=pre_hd[y_col],
                z=pre_hd[z_col],
                mode='text',
                text=["x"] * len(pre_hd),
                textposition="middle center",
                textfont=dict(size=14, color="red"),
                name="Pre Hard Deck Exceeded",
                customdata=pre_hd[[c_col]].values,
                hovertemplate=hover_temp
            )
            datas.append(pre_hd_trace)
        
        if inequality_gt:
            branch_hd = branch_data[branch_data[c_col] > hard_deck_val]
        else:
            branch_hd = branch_data[branch_data[c_col] < hard_deck_val]
        if not branch_hd.empty:
            branch_hd_trace = go.Scatter3d(
                x=branch_hd[x_col],
                y=branch_hd[y_col],
                z=branch_hd[z_col],
                mode='text',
                text=["x"] * len(branch_hd),
                textposition="middle center",
                textfont=dict(size=24, color="red"),
                name="Branch Hard Deck Exceeded",
                customdata=branch_hd[[c_col]].values,
                hovertemplate=hover_temp
            )
            datas.append(branch_hd_trace)
        
        if inequality_gt:
            post_hd = post_data[post_data[c_col] > hard_deck_val]
        else:
            post_hd = post_data[post_data[c_col] < hard_deck_val]
        if not post_hd.empty:
            post_hd_trace = go.Scatter3d(
                x=post_hd[x_col],
                y=post_hd[y_col],
                z=post_hd[z_col],
                mode='text',
                text=["x"] * len(post_hd),
                textposition="middle center",
                textfont=dict(size=24, color="red"),
                name="Post Hard Deck Exceeded",
                customdata=post_hd[[c_col]].values,
                hovertemplate=hover_temp
            )
            datas.append(post_hd_trace)
        
        # Add the maneuver markers (with appropriate colors for pre/post).
        datas.extend(get_maneuver_markers(branch_threshold))
        
        # Combine all traces into one figure.
        fig = go.Figure(data=datas)
        fig.update_layout(
            height=1000,
            width=1000,
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            scene=dict(
                xaxis_title="C (km)",
                yaxis_title="I (km)",
                zaxis_title="R (km)"
            )
        )
        
        return ui.HTML(fig.to_html())

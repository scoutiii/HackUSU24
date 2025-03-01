from shiny import ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Read initial dataset (if needed elsewhere)
RpoPlan = pd.read_csv("data/RpoPlan.csv")

# Define the column names (assuming both CSVs share the same structure)
x_col = "positionDepRelToChiefLvlhZ"
y_col = "positionDepRelToChiefLvlhY"
z_col = "positionDepRelToChiefLvlhX"
c_col = "relativeRange"
t_col = "secondsSinceStart"

c_min, c_max = RpoPlan[c_col].min(), RpoPlan[c_col].max()

# Define UI for Tab 2 with a new numeric input for branch selection
tab_ui = ui.nav_panel("3D Maneuver Branch",
    ui.row(
        ui.column(3,
            ui.h3("Options"),
            # New numeric input to choose a branch number between 1 and 47
            ui.input_numeric("branch_number", "Branch Number", value=1, min=1, max=47, step=1),
            ui.input_numeric("hard_deck", "Hard Deck", value=100, min=0, step=1)
        ),
        ui.column(8,
            ui.output_ui("plot2")  # Render the interactive Plotly plot as HTML
        )
    )
)

# Define Server Logic for Tab 2
def server(input, output, session):
    @render.ui
    def plot2():
        # Get the selected branch number from the input
        branch_num = input.branch_number()
        hard_deck_val = input.hard_deck()

        # Construct the file path based on the selected branch number.
        # For example, if branch_num is 1, this will load "data/ManeuverBranch1.csv"
        csv_file = os.path.join("data", f"ManeuverBranchId{branch_num}.csv")
        # Load the corresponding CSV file
        branch_data = pd.read_csv(csv_file)

        branch_threshold = branch_data[t_col].min()
        
        # Split RpoPlan into two parts based on the threshold
        pre_data = RpoPlan[RpoPlan[t_col] < branch_threshold]
        post_data = RpoPlan[RpoPlan[t_col] >= branch_threshold]
        
        pre_trace = go.Scatter3d(
            x=pre_data[x_col],
            y=pre_data[y_col],
            z=pre_data[z_col],
            mode='lines',
            line=dict(
                width=4,
                dash="solid",
                color=pre_data[c_col],
                colorscale="Hot_r",
                cmin=c_min,
                cmax=c_max,
            ),
            name="RpoPlan (Pre-Branch)"
        )
        
        # Create the post-branch trace: solid gray line with transparency (alpha=0.5).
        post_trace = go.Scatter3d(
            x=post_data[x_col],
            y=post_data[y_col],
            z=post_data[z_col],
            mode='lines',
            line=dict(
                width=4,
                dash="dash",
                color="rgba(64, 64, 64,0.5)", # Gray with 50% opacity
            ),
            name="RpoPlan (Post-Branch)"
        )
        
        # Create the branch trace: thicker, solid, and colored by relativeRange.
        branch_trace = go.Scatter3d(
            x=branch_data[x_col],
            y=branch_data[y_col],
            z=branch_data[z_col],
            mode='lines',
            line=dict(
                width=24,
                dash="solid",
                color=branch_data[c_col],
                colorscale="Hot_r",
                cmin=c_min,
                cmax=c_max
            ),
            name=f"Branch {branch_num}"
        )

        # Add a text marker ("O") at the start of branch_data
        branch_start_trace = go.Scatter3d(
            x=[branch_data[x_col].iloc[0]],
            y=[branch_data[y_col].iloc[0]],
            z=[branch_data[z_col].iloc[0]],
            mode='text',
            text=["O"],
            textposition="middle center",
            textfont=dict(
                size=20,
                color="black"
            ),
            name=f"Branch {branch_num} Starts"
        )
        
        datas = [pre_trace, post_trace, branch_trace, branch_start_trace]

        # For pre_data: add "x" markers where relativeRange > hard deck
        pre_hd = pre_data[pre_data[c_col] < hard_deck_val]
        pre_hd_trace = None
        if not pre_hd.empty:
            pre_hd_trace = go.Scatter3d(
                x=pre_hd[x_col],
                y=pre_hd[y_col],
                z=pre_hd[z_col],
                mode='text',
                text=["x"] * len(pre_hd),
                textposition="middle center",
                textfont=dict(size=14, color="red"),
                name="Pre Hard Deck Exceeded"
            )
            datas.append(pre_hd_trace)
        
        # For branch_data: add "x" markers where relativeRange > hard deck
        branch_hd = branch_data[branch_data[c_col] < hard_deck_val]
        branch_hd_trace = None
        if not branch_hd.empty:
            branch_hd_trace = go.Scatter3d(
                x=branch_hd[x_col],
                y=branch_hd[y_col],
                z=branch_hd[z_col],
                mode='text',
                text=["x"] * len(branch_hd),
                textposition="middle center",
                textfont=dict(size=24, color="red"),
                name="Branch Hard Deck Exceeded"
            )
            datas.append(branch_hd_trace)
        
        # For post_data: add "x" markers where relativeRange is less than the hard deck
        post_hd = post_data[post_data[c_col] < hard_deck_val]
        post_hd_trace = None
        if not post_hd.empty:
            post_hd_trace = go.Scatter3d(
                x=post_hd[x_col],
                y=post_hd[y_col],
                z=post_hd[z_col],
                mode='text',
                text=["x"] * len(post_hd),
                textposition="middle center",
                textfont=dict(size=24, color="red"),
                name="Post Hard Deck Exceeded"
            )
            datas.append(post_hd_trace)

        # Combine all traces into one figure
        fig = go.Figure(data=datas)
        fig.update_layout(
            height=1000,
            width=1000,
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True
        )
        
        

        return ui.HTML(fig.to_html())

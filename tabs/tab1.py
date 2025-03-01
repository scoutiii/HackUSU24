from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd

# Load Data
RpoPlan = pd.read_csv("data/RpoPlan.csv")

# Extract relevant columns
x_col, y_col, z_col = "positionDepRelToChiefLvlhX", "positionDepRelToChiefLvlhY", "positionDepRelToChiefLvlhZ"

# Define UI
tab_ui = ui.page_fluid(
    ui.navset_tab(  # Wrap tabs inside a proper nav container
        ui.nav_panel("Tab 1",
            ui.row(
                ui.column(4,
                    ui.h3("Options"),
                    ui.input_action_button("time2", "Time Options"),
                    ui.input_select("variable2", "Variable Options", {"var1": "Option 1", "var2": "Option 2"})
                ),
                ui.column(8,
                    ui.div(
                        output_widget("plot1"),  # Correct way to render a Plotly figure
                        style="width: 100%; height: 80vh;"  # Ensures full use of available space
                    )
                )
            )
        )
    )
)

# Define Server Logic
def server(input, output, session):
    @output
    @render_widget
    def plot1():
        # Create an interactive 3D line plot
        fig = px.line_3d(RpoPlan, x=x_col, y=y_col, z=z_col)
        
        # Set figure layout to expand fully
        fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),  # Remove extra margins
            height=600  # Can adjust dynamically if needed
        )
        
        return fig  # Correct return type for render_widget


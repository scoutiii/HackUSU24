from shiny import ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os


RpoPlan = pd.read_csv("data/RpoPlan.csv")

# Extract relevant columns
x_col = "positionDepRelToChiefLvlhZ"
y_col = "positionDepRelToChiefLvlhY"
z_col = "positionDepRelToChiefLvlhX"

# Define UI for Tab 2
tab_ui = ui.nav_panel("Tab 2",
    ui.row(
        ui.column(3,
            ui.h3("Options"),
            ui.input_action_button("time2", "Time Options"),
            ui.input_select("variable2", "Variable Options", {"var1": "Option 1", "var2": "Option 2"})
        ),
        ui.column(8,
            ui.output_ui("plot2") # Render the interactive Plotly plot as HTML
        )
    )
)

# Define Server Logic for Tab 2
def server(input, output, session):
    @render.ui
    def plot2():
        # Create an interactive 3D scatter plot using Plotly
        fig = px.line_3d(RpoPlan,
                         "positionDepRelToChiefLvlhX",
                         "positionDepRelToChiefLvlhY",
                         "positionDepRelToChiefLvlhZ",
                         height=1000, width=1000)
        fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),  # Remove extra margins
        )
        return ui.HTML(fig.to_html())


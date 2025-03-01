import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from shiny import App, render, ui
from shared import df_payload, df_ground, df_rpoPlan


# Define the app's user interface (UI)
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("var", "Select variable", choices=["positionChiefEciY"]),
        ui.input_slider("x_zoom", "Zoom X-Axis", min=0, max=1500000, value=(0, 1500000)),
    ),
    ui.output_plot("hist"),
    title="Data Visualization Dashboard",
)

# Define the server-side logic of the app
def server(input, output, session):
    @render.plot
    def hist():
        # Select the variable and time variable from input
        variable = input.var() # Selected time variable (UTC, Julian, or Seconds)
        x_min, x_max = input.x_zoom()  # X-axis zoom range for ground station plot
        x_col_start = "startSeconds"
        x_col_end = "stopSeconds"
        x_time='secondsSinceStart'
        # List of maneuver datasets
        

        # Create a 5-row subplot (4 for maneuver plots + 1 for ground station plot)
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 12))
        sns.lineplot(ax=axs[0], x=x_time, y=variable, data=df_rpoPlan)
        axs[0].set_title(f"Plot for Sun")  # You can use the label you want here, for example 'df_manuever1'
        axs[0].set_xlabel("Time (seconds)")
        axs[0].set_ylabel(variable)
        # Plot ground station availability in the last (5th) subplot
        for _, row in df_payload.iterrows():
            axs[1].hlines(y=row["eventType"], xmin=row["startSeconds"], xmax=row["stopSeconds"], color='b', linewidth=2)

        # Set labels for the ground station subplot
        axs[1].set_xlabel("x")  # Use selected time variable for x-axis
        axs[1].set_ylabel("Payload")
        axs[1].set_title("Payload")
        axs[1].grid(True)
        for _, row in df_ground.iterrows():
            axs[2].hlines(y=row["groundSite"], xmin=row["startSeconds"], xmax=row["stopSeconds"], color='b', linewidth=2)

        # Set labels for the ground station subplot
        axs[2].set_xlabel("x")  # Use selected time variable for x-axis
        axs[2].set_ylabel("Ground Station")
        axs[2].set_title("Ground Station Visibility Over Time")
        axs[2].grid(True)

        # Apply zoom range for x-axis
        axs[2].set_xlim(x_min, x_max)

        plt.tight_layout()
        return fig  # Ensure the figure is returned for rendering

# Create and run the Shiny app
app = App(app_ui, server)
app.run()

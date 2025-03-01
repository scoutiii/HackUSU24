from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from shiny import ui, render

# Define paths and load data
app_dir = Path(__file__).parent.parent
# data_path = app_dir / "CelestialChoreography" / "Data"
data_path = "./data/"
df_payload = pd.read_csv("data/PayloadEvents.csv")
df_ground  = pd.read_csv("data/GroundContacts.csv")
df_rpoPlan = pd.read_csv("data/RpoPlan.csv")

# Get min and max of secondsSinceStart
x_min = df_rpoPlan["secondsSinceStart"].min()
x_max = df_rpoPlan["secondsSinceStart"].max()

# UI definition
tab_ui = ui.nav_panel(
    "Time Series Plots",
    ui.page_sidebar(
        ui.sidebar(
            ui.h3("Options"),
            ui.input_select("var", "Select variable", choices=["sensorAngleToSun", "sensorAngleToMoon"]),
            ui.input_slider("x_zoom", "Zoom X-Axis", min=x_min, max=x_max, value=(x_min, x_max)),
            ui.input_numeric("hard_deck", "Hard Deck", value=100, min=0, step=1),
        ),
        ui.output_plot("hist")
    ),
)

# Server function
def server(input, output, session):
    @output
    @render.plot
    def hist():
        variable = input.var()
        x_min, x_max = input.x_zoom()
        hard_deck_val = input.hard_deck()
        x_time = "secondsSinceStart"
        
        # Create a 4-row subplot
        fig, axs = plt.subplots(4, 1, sharex=True, figsize=(8, 12))
        
        # Plot RPO Plan data
        sns.lineplot(ax=axs[0], x=x_time, y=variable, data=df_rpoPlan)
        axs[0].set_xlabel("Time (seconds)")
        axs[0].set_ylabel(variable)
        
        # Plot Payload Events
        for _, row in df_payload.iterrows():
            axs[1].hlines(y=row["eventType"], xmin=row["startSeconds"], xmax=row["stopSeconds"], color='b', linewidth=2)
        axs[1].set_ylabel("Payload")
        axs[1].grid(True)
        
        # Plot Ground Contacts
        for _, row in df_ground.iterrows():
            axs[2].hlines(y=row["groundSite"], xmin=row["startSeconds"], xmax=row["stopSeconds"], color='b', linewidth=2)
        axs[2].set_ylabel("Ground Station")
        axs[2].grid(True)
        
        # Plot Relative Range (log scale)
        sns.lineplot(ax=axs[3], x=x_time, y='relativeRange', data=df_rpoPlan)
        axs[3].set_ylabel("Relative Range (log scale)")
        axs[3].set_yscale("log")  # Set log scale for y-axis
        axs[3].axhline(y=hard_deck_val, color='red', linestyle='--', label=f"y = {hard_deck_val}")
        axs[3].set_xlim(x_min, x_max)
        axs[3].set_xlabel("Time (seconds)")  # Added x-axis label
        
        # Find x-values where relativeRange crosses hard_deck_val in both directions
        df_rpoPlan['prev_relativeRange'] = df_rpoPlan['relativeRange'].shift(1)
        crossings = df_rpoPlan[(df_rpoPlan['prev_relativeRange'] < hard_deck_val) & (df_rpoPlan['relativeRange'] >= hard_deck_val) | 
                                (df_rpoPlan['prev_relativeRange'] > hard_deck_val) & (df_rpoPlan['relativeRange'] <= hard_deck_val)]
        for xc in crossings["secondsSinceStart"]:
            axs[3].axvline(x=xc, color='red')
        
        # Mark start and end points if the plot starts or ends below the hard deck
        first_x, last_x = df_rpoPlan["secondsSinceStart"].iloc[0], df_rpoPlan["secondsSinceStart"].iloc[-1]
        first_y, last_y = df_rpoPlan["relativeRange"].iloc[0], df_rpoPlan["relativeRange"].iloc[-1]
        
        if first_y < hard_deck_val:
            axs[3].axvline(x=first_x, color='red', label="Start Below", linewidth=4)  # Thicker line

        if last_y < hard_deck_val:
            axs[3].axvline(x=last_x, color='red', label="End Below", linewidth=4)
        
        # Set scientific notation for x-axis
        axs[3].xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        axs[3].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        
        plt.tight_layout()
        return fig

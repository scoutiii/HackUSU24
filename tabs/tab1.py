from shiny import ui, render
import matplotlib.pyplot as plt
import pandas as pd

ui = ui.nav_panel("Tab 1",
    ui.row(
        ui.column(4,
            ui.h3("Options"),
            ui.input_action_button("time1", "Time Options"),
            ui.input_select("variable1", "Variable Options", {"var1": "Option 1", "var2": "Option 2"})
        ),
        ui.column(8,
            ui.output_plot("plot1")
        )
    )
)

def server(input, output, session):
    @output
    @render.plot
    def plot1():
        df = pd.DataFrame({"x": range(10), "y": [i ** 2 for i in range(10)]})
        fig, ax = plt.subplots()
        ax.scatter(df["x"], df["y"])
        ax.set_title("Scatter Plot - Tab 1")
        return fig

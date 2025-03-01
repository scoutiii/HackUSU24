from shiny import ui, render
import matplotlib.pyplot as plt
import pandas as pd

tab_ui = ui.nav_panel("Tab 3",
    ui.row(
        ui.column(4,
            ui.h3("Options"),
            ui.input_action_button("time3", "Time Options"),
            ui.input_select("variable3", "Variable Options", {"var1": "Option 1", "var2": "Option 2"})
        ),
        ui.column(8,
            ui.output_plot("plot3")
        )
    )
)

def server(input, output, session):
    @output
    @render.plot
    def plot3():
        df = pd.DataFrame({"x": ["A", "B", "C"], "y": [5, 3, 8]})
        fig, ax = plt.subplots()
        ax.bar(df["x"], df["y"])
        ax.set_title("Bar Chart - Tab 3")
        return fig

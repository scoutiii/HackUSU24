from shiny import App
from shiny import ui
import tabs.tab1 as tab1
import tabs.tab2 as tab2
import tabs.tab3 as tab3
import pandas as pd





app_ui = ui.page_fluid(
    ui.navset_tab(
        # tab1.tab_ui,  # Import Tab 1 UI from tab1.py
        tab2.tab_ui,  # Import Tab 2 UI from tab2.py
        # tab3.tab_ui   # Import Tab 3 UI from tab3.py
    )
)

def server(input, output, session):
    tab1.server(input, output, session)
    tab2.server(input, output, session)
    tab3.server(input, output, session)

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()

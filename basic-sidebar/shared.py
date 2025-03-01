from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent.parent
df_payload = pd.read_csv(app_dir / "CelestialChoreography" / "Data"/"PayloadEvents.csv")
df_ground = pd.read_csv(app_dir / "CelestialChoreography" / "Data"/"GroundContacts.csv")
df_rpoPlan = pd.read_csv(app_dir / "CelestialChoreography" / "Data"/"RpoPlan.csv")
__version__ = '2025.2'

import os
import sys
import time
time_start = time.perf_counter()

from pathlib import Path
from generator.core import *
from generator.helpers import *

app_path = os.path.dirname(os.path.realpath(__file__))

input_file = os.path.join(os.path.dirname(__file__), 'maschinenliste.csv')

# CLI Parameter
if len(sys.argv) > 0:

    for arg in sys.argv:

        if 'file=' in arg:
            input_file = arg.replace('file=', '')


# Output-Ordner anlegen
print('Erzeuge Konfiguration\n|')

directory = "output"
path = Path(directory)
path.mkdir(parents=True, exist_ok=True)

print(f'|- Datei = {input_file}')

# Maschinenliste einlesen
machines = import_machines(input_file)

# Rollen für FabAccess erzeugen
roles = generate_roles(machines)

# Finale DHALL-Daten erzeugen
export_roles = generate_bffh_roles(roles)
export_machines = generate_bffh_machines(machines)
export_actors = generate_bffh_plugins(machines, "actors")
export_actorconnections = generate_bffh_pluginconnections(machines, "actors")
export_initiators = generate_bffh_plugins(machines, "initiators")
export_initiatorconnections = generate_bffh_pluginconnections(machines, "initiators")
export_all = export_roles + export_machines + export_actors + export_actorconnections + export_initiators + export_initiatorconnections


# ------- Daten exportieren

# Textdatei mit komplettem dhall-Inhalt
create_singledhall(export_roles, export_machines, export_actors, export_actorconnections, export_actors, export_initiatorconnections)

# Rollenliste als CSV
create_roles_csv(roles)

# Einzelne DHALLs
create_multipledhalls(export_roles, export_machines, export_actors, export_actorconnections, export_actors, export_initiatorconnections)

# Mermaid-Code
create_mermaid(machines)

# ----------------------
time_end = time.perf_counter()
time_span = round(time_end - time_start, 2)
print('---------')
print(f'Laufzeit: {time_span} Sekunden')

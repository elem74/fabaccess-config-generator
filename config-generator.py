__version__ = '2024.6'

import time
time_start = time.perf_counter()

from pathlib import Path
from generator.core import *
from generator.helpers import *

input_file = 'maschinenliste.csv'

# Output-Ordner anlegen
directory = "output"
path = Path(directory)
path.mkdir(parents=True, exist_ok=True)

print(f' --- Datei = {input_file}')

# Maschinenliste einlesen
print(' --- Maschinen importieren:')
machines = import_machines(input_file)

# Rollen für FabAccess erzeugen
print(' --- Rollen erzeugen')
roles = generate_roles(machines)

# Finale DHALL-Daten erzeugen
export_roles = generate_bffh_roles(roles)
export_machines = generate_bffh_machines(machines)
export_actors = generate_bffh_actors(machines)
export_actorconnections = generate_bffh_actorconnections(machines)
export_all = export_roles + export_machines + export_actors + export_actorconnections


# Anzeigen der erzeugten Daten
if settings["show_machines"] == True:
    for m in machines:
        display_machine(m)

if settings["show_roles"] == True:
    print_dict(roles)

# Daten exportieren
print(' --- DHALL-Daten exportieren')
write_file('output/bffh-dhall-data.txt', export_all)

if settings["create_file_roles"] == True:
    print(' --- Rollen exportieren in roles.csv')
    content = generate_csv_roles(roles)
    write_file('output/roles.csv', content)

if settings["fa_update_dhall"] == True:
    print(' --- Aktualisierung der bffh.dhall')
    fa_dhall_file = settings["fa_dhall_file"]

    # Pfadangabe "fa_dhall_file" hat Inhalt
    if len(fa_dhall_file) > 0:

        # Daten schreiben
        dhall_content = generate_bffh_dhall(export_all)

        if len(dhall_content) > 0:
            write_file(fa_dhall_file, dhall_content)

    # Pfadangabe "fa_dhall_file" ist leer
    else:
        print('Einstellung "fa_dhall_file" ist leer, es wurde kein Pfad zur bffh.dhall angegeben.')
        print('Bitte das Feld ausfüllen oder "fa_update_dhall" auf "False" setzen.')

# Mermaid-Code
if settings["generate_mermaid"] == True:
    print(' --- Mermaid-Code erzeugen')
    graphelements = graph_create_elements(machines)
    mermaidcode = graph_create_mermaidcode(graphelements)
    write_file('output/mermaid-code.txt', mermaidcode)

# ------------------------------------------------------------------
time_end = time.perf_counter()
time_span = round(time_end - time_start, 2)
print('-------------------------')
print(f'Laufzeit: {time_span} Sekunden')
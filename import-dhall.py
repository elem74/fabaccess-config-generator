# Rich-Module
try:
    from rich.table import Table
    from rich.console import Console
    from rich.text import Text
    module_rich = True
except ImportError:
    module_rich = False

from generator.globals import csv_match

# --------------------------------------------------

class ImportedMachine:
    def __init__(self, id):
        self.id = id
        self.actor = ''
        self.name = ''
        self.description = ''
        self.wiki = ''
        self.category = ''

    def set_actor(self, var):
        self.actor = var

    def set_name(self, var):
        self.name = var

    def set_description(self, var):
        self.description = var

    def set_wiki(self, var):
        self.wiki = var

    def set_category(self, var):
        self.category = var

    def get_specs(self):
        specs = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "actor": self.actor,
            "wiki": self.wiki,
            "category": self.category
        }
        return specs

def dhall_parse(dhall_file):

    display = []

    prettynames = {
        'machines': 'Maschine',
        'actor_connections': 'Aktorenverbindung'
    }

    machines = {}

    with open(dhall_file, 'r', encoding='utf-8-sig') as dhall_data:

        status_section = 'none'

        level = 1

        # 0 = Datei
        # 1 = Konfiguration
        # 2 = Sektion
        # 3 = Eintrag

        for line in dhall_data:

            l = line.replace('\n', '')

            if status_section == 'none':

                if ('actor_connections' not in line) and ('machines' not in line):
                    continue

                # if ('actor_connections' in line) or ('machines' in line):
                #     print('-- section found ')

            save_data = {}
            save_var = 0

            if status_section != 'actor_connections':
                if '{' in line or '[' in line:
                    level += line.count('{')
                    level += line.count('[')

            if '}' in line and status_section != 'actor_connections':
                level -= line.count('}')

            if  ']' in line and status_section == 'actor_connections':
                level -= line.count(']')

            # print(f'{level}: {status_section} {l}')

            match(level):
                case 1:
                    status_section = 'none'

                # Sektion gefunden?
                case 2:
                    if status_section == 'none':
                        if ('machines' in line) and ('=' in line):
                            status_section = 'machines'
                            # print(' |-- machines found')
                            continue

                        if ('actor_connections' in line) and ('=' in line):
                            status_section = 'actor_connections'
                            # print(' |-- actor_connections found')
                            continue

                    # Maschineneintrag gefunden?
                    if status_section == 'machines':

                        if '=' in line:

                            # print('   |-- machine found')
                            id = (
                                line.split('=')[0]
                                .replace(' ', '')
                                .strip()
                            )

                            machines[id] = ImportedMachine(id)
                            # print(f'{level}: id = |{id}|')

                            display.append(
                                {
                                    'section': prettynames[status_section],
                                    'id': id,
                                    'actor': ''
                                }
                            )

                        continue

                    if status_section == 'actor_connections':

                        if '=' in line:
                            # print('   |-- actorconnection found')
                            save_var = 1

                            temp = (
                                line.replace('"', '')
                                .replace('\'', '')
                                .replace('\n', '')
                                .replace('\r\n', '')
                                .replace('{', '')
                                .replace('}', '')
                                .strip()
                            )

                            strings = []

                            if ',' in temp:
                                split = temp.split(',')
                                strings.append(split[0].strip())
                                strings.append(split[1].strip())
                            else:
                                strings.append(temp.strip())

                            for s in strings:
                                split = s.split('=')
                                variable = split[0].strip()
                                value = split[1].strip()

                                save_data[variable] = value

                            display.append(
                                {
                                    'section': prettynames[status_section],
                                    'id': save_data["machine"],
                                    'actor': save_data["actor"]
                                }
                            )

                            # for key, value in save_data.items():
                            #     print(f'     + {key} = {value}')


                case 3:
                    if (status_section == 'machines'):
                        if '=' in line:
                            save_var = 1

                            temp = (
                                line.replace('"', '')
                                .replace('\'', '')
                                .replace(',', '')
                                .replace('\n', '')
                                .replace('\r\n', '')
                                .strip()
                            )

                            split = temp.split('=')
                            variable = split[0].replace(' ', '').strip()
                            value = split[1]

                            save_data[variable] = value




            if status_section == 'actor_connections' or status_section == 'machines':
                # print('---------------SD---------------')
                # print(save_data)

                if save_var == 1:
                    # print('saving')
                    # print(f'{level}: |{variable}| = {value}')

                    for key, value in save_data.items():
                        # print(f'actormatch {key} = {value}')

                        match(key):
                            # Maschine
                            case 'name':
                                machines[id].set_name(value)

                            case 'description':
                                machines[id].set_description(value)

                            case 'wiki':
                                machines[id].set_wiki(value)

                            case 'category':
                                machines[id].set_category(value)

                            # Aktorenverbindung
                            case 'machine':
                                id = value

                            case 'actor':
                                machines[id].set_actor(value)


    if module_rich == True:
        console = Console()
        table = Table(highlight="pale_green3")
        table.add_column("Datentyp")
        table.add_column("ID")
        table.add_column("Aktor")

        for d in display:
            table.add_row(d["section"], f'{d["id"]}', f'{d["actor"]}')

        console.print(table)
    else:
        print(f'{"Sektion": <20} | {"ID": <60} | {"Aktor": <40} |')
        print(f'{125 * "-"}')

        for d in display:
            print(f'{d["section"]: <20} | {f'{d["id"]}': <60} | {f'{d["actor"]}': <40} |')


    return machines

def importdata_to_csv(machines, outputfile):

    lines = []

    header = 'Name Domäne;Name Bereich;Name Unterbereich;Name Maschine;Maschinenbeschreibung;Manager Unterbereich;Name Alternativrolle;ID Alternativrolle;Wiki-URL;ID Domäne;ID Bereich;ID Unterbereich;ID Maschine;Aktor ID;Aktor Typ;Kommentar'
    template = 'domain_name;area_name;subarea_name;machine_name;machine_desc;subarea_manager;customrole_name;customrole_id;machine_wikiurl;domain_id;area_id;subarea_id;machine_id;actor_id;actor_type;'

    lines.append(header)

    for m in machines:
        specs = machines[m].get_specs()
        temp = template

        temp = temp.replace('domain_name', '')
        temp = temp.replace(';subarea_name', ';')
        temp = temp.replace(';subarea_manager', ';')
        temp = temp.replace(';customrole_name', ';')
        temp = temp.replace(';customrole_id', ';')
        temp = temp.replace(';domain_id', ';')
        temp = temp.replace(';area_id', ';')
        temp = temp.replace(';subarea_id', ';')
        temp = temp.replace(';actor_type', ';')

        for key, value in specs.items():

            match(key):

                case('id'):
                    temp = temp.replace(';machine_id', f';{value}')

                case('name'):
                    temp = temp.replace(';machine_name', f';{value}')

                case('description'):
                    temp = temp.replace(';machine_desc', f';{value}')

                case('wiki'):
                    temp = temp.replace(';machine_wikiurl', f';{value}')

                case('actor'):
                    temp = temp.replace(';actor_id', f';{value}')

                case('category'):
                    temp = temp.replace(';area_name', f';{value}')

        lines.append(temp)

    with open(outputfile, "w", encoding='utf-8-sig', newline='\n') as csv_file:
        for l in lines:
            csv_file.write(l + '\n')




machines = dhall_parse('bffh.dhall')

file = 'output/importedresources.csv'
importdata_to_csv(machines, file)


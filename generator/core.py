from string import Template

from generator.globals import *
from generator.helpers import *

# Rich-Module
try:
    from rich.table import Table
    from rich.console import Console
    from rich.text import Text
    module_rich = True
except ImportError:
    module_rich = False


# Settings-Dateien finden und laden
if os.path.isfile('settings.ini') == True:
    settings = config_load('settings.ini', 'generator')
else:
    settings = config_load('./settings.ini', 'generator')

if os.path.isfile('actors.ini') == True:
    plugin_library = load_plugins('actors.ini')
else:
    plugin_library = load_plugins('./actors.ini')

if os.path.isfile('initiators.ini') == True:
    initiator_library = load_plugins('initiators.ini')
else:
    initiator_library = load_plugins('./initiators.ini')


string_userhandle = settings["string_userhandle"] + ' '
string_adminhandle = settings["string_adminhandle"] + ' '
string_managerhandle = settings["string_managerhandle"] + ' '

# ------------ Klassen

class Domain:
    def __init__(self, domain_id, domain_name):
        name_handle = domain_name
        perm_handle = domain_id + '.'
        id_handle = perm_handle.replace('.', '_')

        self.domain = {
            "id": domain_id,
            "name": domain_name
        }

        self.domain_manager = {
            "id": id_handle + 'manager',
            "name": '_' + string_managerhandle + domain_name,
            "perms": perm_handle + '*'
        }

        self.domain_user = {
            "id": id_handle + 'user',
            "name": '_' + string_userhandle + domain_name,
            "perms": []
        }


    def get_domain(self):
        return self.domain

    def get_domain_perms(self):
        return self.domain_manager["perms"]

    def get_domain_manager(self):
        return self.domain_manager

    def get_domain_user(self):
        return self.domain_user


class Area(Domain):
    def __init__(self, domain_id, domain_name, area_id, area_name):
        super().__init__(domain_id, domain_name)

        self.area_id = area_id
        self.area_name = area_name

        if settings["multi_domains"] == True:
            name_handle = domain_name + area_name
        else:
            name_handle = area_name

        perm_handle = domain_id + '.' + area_id + '.'
        id_handle = perm_handle.replace('.', '_')

        perms_manager = [perm_handle + '*']
        perms_user = [
            perm_handle + 'disclose.*',
            perm_handle + 'read.*',
            perm_handle + 'write.*'
            ]

        self.area_manager = {
            "id": id_handle + 'manager',
            "name": string_managerhandle + name_handle,
            "perms": perms_manager
        }

        self.area_user = {
            "id": id_handle + 'user',
            "name": string_userhandle + name_handle,
            "perms": perms_user
        }

    def get_area(self):
        area = {
            "id": self.area_id,
            "name": self.area_name
        }
        return area

    def get_area_manager(self):
        return self.area_manager

    def get_area_user(self):
        return self.area_user

class Subarea(Area):
    def __init__(self, domain_id, domain_name, area_id, area_name, subarea_id, subarea_name, subarea_manager):
        super().__init__(domain_id, domain_name, area_id, area_name)

        self.subarea_id = subarea_id
        self.subarea_name = subarea_name

        if settings["multi_domains"] == True:
            name_handle = domain_name + area_name + ' ' + subarea_name
        else:
            name_handle = area_name + ' ' + subarea_name

        perm_handle = domain_id + '.' + area_id + '.' + subarea_id + '.'
        id_handle = perm_handle.replace('.', '_')

        perms_manager = [perm_handle + '*']
        perms_user = [
            perm_handle + 'disclose.*',
            perm_handle + 'read.*',
            perm_handle + 'write.*'
            ]

        # Unterbereich prüfen
        if len(subarea_id) > 0 and len(subarea_name) > 0:
            self.subarea_state = True
        else:
            self.subarea_state = False

        # Unterbereich-Manager prüfen
        if len(subarea_manager) > 0:
            self.subarea_manager_state = True
        else:
            self.subarea_manager_state = False

        self.subarea_manager = {
            "id": id_handle + 'manager',
            "name": string_managerhandle + name_handle,
            "perms": perms_manager
        }

        self.subarea_user = {
            "id": id_handle + 'user',
            "name": string_userhandle + name_handle,
            "perms": perms_user
        }

    def get_subarea(self):
        subarea = {
            "id": self.subarea_id,
            "name": self.subarea_name
        }
        return subarea

    def get_subarea_manager(self):
        return self.subarea_manager

    def get_subarea_user(self):
        return self.subarea_user

    def has_subarea(self):
        return self.subarea_state

    def has_subarea_manager(self):
        return self.subarea_manager_state


class Machine(Subarea):
    def __init__(self, data):

        area_name = data["area_name"].strip()
        subarea_name = data["subarea_name"].strip()
        domain_id = string_clean(data["domain_id"].strip()).lower()
        area_id = string_clean(data["area_id"].strip()).lower()
        subarea_id = string_clean(data["subarea_id"].strip()).lower()
        machine_id = string_clean(data["machine_id"].strip()).lower()
        subarea_manager = data["subarea_manager"].strip()
        area_name = data["area_name"].strip()
        subarea_name = data["subarea_name"].strip()
        machine_name = string_removequotes(data["machine_name"]).strip()
        machine_desc = string_removequotes(data["machine_desc"]).strip()
        wikiurl = data["wikiurl"].strip()
        actor_id = string_clean(data["actor_id"].strip()).lower()
        # actor_module = data["actor_module"].strip()
        actor_type = data["actor_type"].strip().lower()
        initiator_id = string_clean(data["initiator_id"].strip()).lower()
        # initiator_module = data["initiator_module"].strip()
        initiator_type = data["initiator_type"].strip().lower()

        customrole_id = string_clean(data["customrole_id"].strip()).lower()
        customrole_name = data["customrole_name"].strip()
        domain_name = data["domain_name"].strip() + ' '

        super().__init__(domain_id, domain_name, area_id, area_name, subarea_id, subarea_name, subarea_manager)
        # ----------------------------

        # Alternativrolle prüfen
        if len(customrole_id) > 0 and len(customrole_name) > 0:

            self.customrole_state = True
        else:
            self.customrole_state = False

        if self.subarea_state == True:
            # Unterbereich
            fa_id = domain_id + '-' + area_id + '-' + subarea_id + '-' + machine_id
            string_perm = domain_id + '.' + area_id + '.' + subarea_id + '.|ACTION|.' + machine_id
        else:
            # Bereich
            fa_id = domain_id + '-' + area_id + '-' + machine_id
            string_perm = domain_id + '.' + area_id + '.|ACTION|.' + machine_id

        permlist = ["disclose", "read", "write", "manage"]

        perms_machine = []
        perms_machine_names = []
        perms_user = []

        for p in permlist:
            perms_machine.append(string_perm.replace('|ACTION|', p))
            perms_machine_names.append(p)
            if p != 'manage':
                perms_user.append(string_perm.replace('|ACTION|', p))


        self.machine_specs = {
            "id": machine_id,
            "fa_id": fa_id,
            "name": machine_name,
            "perms": perms_machine,
            "perms_names": perms_machine_names,
            "category": area_name,
            "desc": machine_desc,
            "wikiurl": wikiurl,
            "actor_id": actor_id,
            "actor_type": actor_type,
            "initiator_id": initiator_id,
            "initiator_type": initiator_type
        }

        self.customrole = {
            "id": domain_id + '_' + customrole_id,
            "name": string_userhandle + customrole_name,
            "perms": perms_user
        }

    def get_machine(self):
        return self.machine_specs

    def has_customrole(self):
        return self.customrole_state

    def get_customrole(self):
        return self.customrole


class GraphElement:
    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent
        self.level = id.count('_')
        self.roles = []
        self.machines = []

    def get_level(self):
        return self.level

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def add_machine(self, machine_name, customrole = ''):
        if len(customrole) > 0:
            self.machines.append(f'{machine_name} ({icon_custom}{customrole})')
        else:
            self.machines.append(machine_name)

    def get_machines(self):
        return self.machines

    def add_role(self, roles_name):
        self.roles.append(roles_name)

    def get_roles(self):
        return self.roles


# ------------ Funktionen

# Maschinen aus der CSV-importieren
def import_machines(file):
    print('|- Maschinen importieren:')

    machines = {}
    data = csv_listdict(file, csv_match)

    count = 2

    feedback = []

    for entry in data:

        # ------- Felder übrprüfen
        errors = []

        # Pflichtfelder
        for el in importcheck["single"].keys():

            #  Einzelfeld ist leer?

            if len(entry[el]) == 0:
                name = importcheck["translate"][el]
                errors.append(f'Pflichtfeld "{name}" ist leer')

        # Optionales Felderpaar vollständig?
        for field1, field2 in importcheck["pairs"].items():

            for key, value in csv_match.items():
                if value == field1:
                    field1_name = key
                if value == field2:
                    field2_name = key

            if len(entry[field1]) > 0 and len(entry[field2]) == 0:
                errors.append(f'  |- Felderpaar unvollständig: Feld "{field1_name}" ist ausgefüllt, aber Feld "{field2_name}" ist leer.')

            if len(entry[field2]) > 0 and len(entry[field1]) == 0:
                errors.append(f'  |- Felderpaar unvollständig: Feld "{field2_name}" ist ausgefüllt, aber Feld "{field1_name}" ist leer.')

        if len(errors) > 0:

            feedback.append(
                {
                    "count": str(count),
                    "status": 'Übersprungen',
                    "info": 'Konfigurationsfehler',
                    "details": f'ID: {entry["machine_id"]}',
                }
            )

            for e in errors:
                feedback.append(
                {
                    "count": '',
                    "status": '',
                    "info": '',
                    "details": e,
                }
            )

            count += 1

            continue

        #  Maschine anlegen
        temp = Machine(entry)
        fa_id = temp.get_machine()["fa_id"]

        if fa_id not in machines.keys():
            machines.update({
                f'{fa_id}': Machine(entry)
            })

            feedback.append(
                {
                    "count": str(count),
                    "status": 'OK',
                    "info": 'Maschine angelegt',
                    "details": f'ID: {entry["machine_id"]}',
                }
            )

        else:

            feedback.append(
                {
                    "count": str(count),
                    "status": 'Übersprungen',
                    "info": 'Doppelte Maschinen-ID',
                    "details": f'ID: {entry["machine_id"]}',
                }
            )

        count += 1


    # rich-switch
    if module_rich == True:
        console = Console()
        table = Table(highlight="pale_green3")
        table.add_column("Zeile", justify="right")
        table.add_column("Status")
        table.add_column("Info")
        table.add_column("Details")

        status = Text('OK')
        status.stylize("green")
        table.add_row("1", status, "Kopfzeile", "Kopfzeile wird nicht verarbeitet.")

        for f in feedback:

            if 'OK' in f["status"]:
                status = Text(f["status"])
                status.stylize("green")

            else:

                if 'Übersprungen' in f["status"]:
                    status = Text(f["status"])
                    status.stylize("dark_orange")
                else:
                    status = Text(f["status"])

            table.add_row(f["count"], status, f["info"], f["details"])

        console.print(table)

    else:
        print(f'{"Zeile": ^8} | {"Status": ^24} | {"Details": ^20}')
        print(f'{"1": ^8} | {"Kopfzeile": ^24} | {"Kopfzeile wird nicht verarbeitet.": <20}')

        for f in feedback:
            print(f'{f["count"]: ^8} | {f["status"]: ^24} | {f["details"]: <20}')


    # Datenanzeige
    if settings["show_machines"] == True:
        for m in machines.values():
            display_machine(m)


    return machines




# Rollen erstellen
def generate_roles(machines):

    print('|- Rollen erzeugen')

    roles = {}

    # Globalen Admin erstellen
    roledata = admin_global

    if roledata["id"] not in roles.keys():
        roles[roledata["id"]] = roledata

    # Domänen durchlaufen
    for id, m in machines.items():

        # Domänen-Berechtigung an Admin & Manager vergeben

        # 2do: Admin - Überflüssige Berechtigungen?
        # for perm in roledata["perms"]:

        #     if perm not in roles[admin_global["id"]]["perms"]:
        #         roles[admin_global["id"]]["perms"].append(perm)

        # 2do - end

        perm = m.get_domain_perms()

        if perm not in roles[admin_global["id"]]["perms"]:
            roles[admin_global["id"]]["perms"].append(perm)

        if settings["manager_domain"] == True:

            if roledata["id"] not in roles.keys():
                roles[roledata["id"]] = roledata

        # Manager: Domain
        if settings["multi_domains"] == True:
            roledata = m.get_domain_manager()

            if roledata["id"] not in roles.keys():
                roles[roledata["id"]] = roledata

            for perm in roledata["perms"]:
                if perm not in roles[manager_domain["id"]]["perms"]:
                    roles[manager_domain["id"]]["perms"].append(perm)

        # Manager: Area
        if settings["manager_area"] == True:
            roledata = m.get_area_manager()

            if roledata["id"] not in roles.keys():
                roles[roledata["id"]] = roledata

        # Manager: Subarea
        if settings["manager_subarea"] == True:
            if m.has_subarea() == True:
                if m.has_subarea_manager() == True:
                    roledata = m.get_subarea_manager()

                    if roledata["id"] not in roles.keys():
                        roles[roledata["id"]] = roledata

        # Benutzer: Daten abrufen

        if settings["domain_user"] == True:
            # Domäne-Benutzer
            roledata = m.get_domain_user()

        else:
            # Kein Domäne-Benutzer
            if m.has_customrole() == True:
                # Extrarolle
                roledata = m.get_customrole()

                if roledata["id"] in roles.keys():
                    # Extrarolle vorhanden --> Berechtigungen hinzufügen
                    for p in roledata["perms"]:
                        roles[roledata["id"]]["perms"].append(p)

            else:

                if m.has_subarea() == True:
                    # Unterbereich
                    roledata = m.get_subarea_user()
                else:
                    # Bereich
                    roledata = m.get_area_user()

        # Benutzer: Hinzufügen
        if roledata["id"] not in roles.keys():
            roles[roledata["id"]] = roledata

        # Domänen-Benutzer: Berechtigungen hinzufügen

        if settings["domain_user"] == True:
            if m.has_subarea() == True:
                # Unterbereich
                perms = m.get_subarea_user()["perms"]
            else:
                # Bereich
                perms = m.get_area_user()["perms"]

            for p in perms:
                if p not in roles[roledata["id"]]["perms"]:
                    roles[roledata["id"]]["perms"].append(p)

    
    # Datenanzeige
    if settings["show_roles"] == True:
        print_dict(roles)

    return roles

    
def generate_bffh_roles(roles):

    data = []

    # Anfang Datenstruktur
    data.append('{')

    # Inhalt
    last_role = len(roles) - 1

    for index_role, role in enumerate(roles):
        data.append(space * 1  + f'{role}' + ' =')
        data.append(space * 1  + '{')
        data.append(space * 2  + 'permissions =  [')


        last_perm = len(roles[role]["perms"]) - 1

        for index_perm, (perm) in enumerate(roles[role]["perms"]):

            if index_perm < last_perm:
                data.append(space * 4 + f'"{perm}",')
            else:
                data.append(space * 4 + f'"{perm}"')

        data.append(space * 2  + ']')

        if index_role == last_role:
            data.append(space * 1  + '}')
        else:
            data.append(space * 1  + '},')

        data.append(' ')
    
    # Ende Datenstruktur
    data.append('}')

    return data

# Maschinen
def generate_bffh_machines(machines):

    data = []

    # Anfang Datenstruktur
    data.append('{')

    # Inhalt
    last_machine = len(machines) - 1

    for index_machine, (id, m) in enumerate(machines.items()):

        specs = m.get_machine()
        data.append(space * 1  + f'{specs["fa_id"]}' + ' =')
        data.append(space * 1  + '{')
        data.append(space * 2  + f'name = "{specs["name"]}",')
        data.append(space * 2  + f'description = "{specs["desc"]}",')
        data.append(space * 2  + f'wiki = "{specs["wikiurl"]}",')
        data.append(space * 2  + f'category = "{specs["category"]}",')


        permcount = len(specs["perms"])
        last_perm = permcount - 1

        for i in range(permcount):

            if i < last_perm:
                data.append(space * 2  + f'{specs["perms_names"][i]} = "{specs["perms"][i]}",')
            else:
                data.append(space * 2  + f'{specs["perms_names"][i]} = "{specs["perms"][i]}"')

        if index_machine == last_machine:
            data.append(space * 1  + '}')
            state = 'last'
        else:
            data.append(space * 1  + '},')
            state = 'not last'

        data.append(' ')
        index_machine +=1

    # Ende Datenstruktur
    data.append('}')

    return data

# Aktoren
def generate_bffh_plugins(machines, type):

    data = []

    # Anfang Datenstruktur
    data.append('{')

    # Inhalt
    last_plugin = len(machines) - 1

    for index_plugin, (id, m) in enumerate(machines.items()):
        specs = m.get_machine()

        if len(specs["{}_id"].format(type)) > 0 and len(specs["{}_type"].format(type)) > 0:
            plugin_handle = specs["{}_type".format(type)] + '_' + specs["{}_id".format(type)]

            # 2do Plugin Library Funktionalität

            data.append(space * 1  + f'{plugin_handle} =')
            data.append(space * 1  + '{')
            data.append(space * 2  + f'module = "{plugin_library[specs["{}_type".format(type)]]["module"]}",')
            data.append(space * 2  + 'params =')
            data.append(space * 2  + '{')

            # Aktor-ID der aktuellen Maschine speichern
            replace = {
                "{}_id".format(type): specs["{}_id".format(type)]
            }

            last_param = len(plugin_library[specs["{}_type".format(type)]]["params"]) - 1

            for index_param, (key, value) in enumerate(plugin_library[specs["{}_type".format(type)]]["params"].items()):
                    template = Template(value)
                    string = template.substitute(replace)

                    if index_param < last_param:
                        data.append(space * 3  + f'{key} = {string},')
                    else:
                        data.append(space * 3  + f'{key} = {string}')

            data.append(space * 2  + '}')

            if index_plugin == last_plugin:
                data.append(space * 1  + '}')
            else:
                data.append(space * 1  + '},')

            data.append(' ')

    # Ende Datenstruktur
    data.append('}')

    return data


# Verbindungen (type = "actor" oder "initiator")
def generate_bffh_pluginconnections(machines, type):
    data = []

    # Anfang Datenstruktur
    data.append('[')

    # Inhalt
    last = len(machines) - 1

    for index, (id, m) in enumerate(machines.items()):
        specs = m.get_machine()

        if len(specs["{}_id".format(type)]) > 0 and len(specs["{}_type"].format(type)) > 0:
            plugin_fullid = specs["{}_type"] + '_' + specs["{}_id".format(type)]

            if index == last:
                "{ machine = \"{}\", {} = \"{}\" }".format(specs["fa_id"], type, plugin_fullid)
                data.append(space * 1  + "{ machine = \"{}\", {} = \"{}\" }".format(specs["fa_id"], type, plugin_fullid))
            else:
                data.append(space * 1  + "{ machine = \"{}\", {} = \"{}\" },".format(specs["fa_id"], type, plugin_fullid))

    # Ende Datenstruktur
    data.append(']')

    return data


# CSV-Rollenliste

def create_roles_csv(roles):

    print('|- Rollenliste exportieren')

    data = []
    data.append('ID der Rolle; Name der Rolle')
    for id, values in roles.items():
        string = id + ';' + values["name"]
        data.append(string)

    write_file('output/roles.csv', data)


# dhall-Dateien erzeugen

def create_singledhall(export_roles, export_machines, export_actors, export_actorconnections, export_initiators, export_initiatorconnections):
    print('|- Gesamten DHALL-Output exportieren')

    input = [export_roles, export_machines, export_actors, export_actorconnections, export_actorconnections, export_initiators, export_initiatorconnections]

    data = []

    # Rollen

    index_input = 0

    for i in input:

        match(index_input):
            case 0: data.append('roles =')
            case 1: data.append('machines =')
            case 2: data.append('actors =')
            case 3: data.append('export_actorconnections =')
            case 4: data.append('initiators =')
            case 5: data.append('export_initiatorconnections =')

        last = len(input[index_input]) - 1
        for index_seg, (el) in enumerate(i):

            if index_seg == last:
                data.append(el + ',')
            else:
                data.append(el)

        index_input += 1


    write_file('output/bffh-dhall-data.txt', data)

def create_multipledhalls(export_roles, export_machines, export_actors, export_actorconnections, export_initiators, export_initiatorconnections):



    input = [export_roles, export_machines, export_actors, export_actorconnections, export_initiators, export_initiatorconnections]

    fa_dhall_directory = settings["fa_dhall_directory"].replace('\\', '/')


    print('|- Einzelne DHALLs exportieren')

    if fa_dhall_directory != '':
        print(f'|- Ablegen der DHALL-Dateien in: "{fa_dhall_directory}"')

    index_input = 0

    for i in input:

        match(index_input):
            case 0: target_file = 'roles.dhall'
            case 1: target_file = 'machines.dhall'
            case 2: target_file = 'actors.dhall'
            case 3: target_file = 'actorconnections.dhall'
            case 4: target_file = 'initiator.dhall'
            case 5: target_file = 'initiatorconnections.dhall'
        print(f'   |- Erzeuge {target_file}')

        # Im Output-Ordner
        target = 'output/' + target_file
        write_file(target, i)


        # Im zusätzlichen Ordner
        if fa_dhall_directory != '':
            target = fa_dhall_directory + '/' + target_file
            target = target.replace('//', '/')
            write_file(target, i)

        index_input += 1


def create_mermaid(machines):
    print('|- Mermaid-Code erzeugen')

    graphelements = graph_create_elements(machines)
    mermaidcode = graph_create_mermaidcode(graphelements)

    write_file('output/mermaid-code.txt', mermaidcode)


# Maschine vollständig ausgeben
def display_machine(machine_object):

    # ------------ DOMAIN

    scope = machine_object.get_domain()
    print('\n--- Domain: ' + scope["name"])
    print('id = ' + scope["id"])
    print('name = ' + scope["name"])

    role = machine_object.get_domain_manager()
    print('\n[Admin: ' + scope["name"] + ']')
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)


    # ------------ AREA
    scope = machine_object.get_area()
    print('\n--- Area: ' + scope["name"])
    print('id = ' + scope["id"])
    print('name = ' + scope["name"])

    role = machine_object.get_area_manager()
    print('\n[Admin: ' + scope["name"] + ']')
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)

    role = machine_object.get_area_user()
    print('\n[User: ' + scope["name"] + ']')
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)

    # ------------ SUBAREA
    scope = machine_object.get_subarea()
    print('\n--- Subarea: ' + scope["name"])
    print('id = ' + scope["id"])
    print('name = ' + scope["name"])
    print('state = ' + str(machine_object.has_subarea()))

    role = machine_object.get_subarea_manager()
    print('\n[Admin: ' + scope["name"] + ']')
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)

    role = machine_object.get_subarea_user()
    print('\n[User: ' + scope["name"] + ']')
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)

    # ------------ MACHINE
    scope = machine_object.get_machine()
    print('\n--- Machine: ' + scope["name"])
    print('id = ' + scope["id"])
    print('fa_id = ' + scope["fa_id"])
    print('name = ' + scope["name"])
    print('desc = ' + scope["desc"])
    print('wikiurl = ' + scope["wikiurl"])
    print('perms = ')
    for p in scope["perms"]:
        print('      ' + p)
    print('actor_id = ' + scope["actor_id"])
    print('actor_type = ' + scope["actor_type"])
    print('initiator_id = ' + scope["initiator_id"])
    print('initiator_type = ' + scope["initiator_type"])

    print('\n[Alternativrolle: '+ role["name"] + ']')
    print('state = ' + str(machine_object.has_customrole()))
    role = machine_object.get_customrole()
    print('id = ' + role["id"])
    print('name = ' + role["name"])
    print('perms = ')
    for p in role["perms"]:
        print('      ' + p)


def graph_create_elements(machines):
    data = {}
    data["_root"] = GraphElement("root", "Infrastruktur", '')
    data["_root"].add_role(f'{icon_admin}{admin_global["name"]}')
    if settings["manager_domain"] == True:
        data["_root"].add_role(f'{icon_manager}{manager_domain["name"]}')

    for key, m in machines.items():

        # Domain
        domain = m.get_domain()
        domain_id = f'root_{domain["id"]}'

        if domain_id not in data.keys():
            data[f'{domain_id}'] = GraphElement(domain_id, domain["name"], 'root')

            data[domain_id].add_role(f'{icon_manager}{m.get_domain_manager()["name"]}')

        # Area
        area = m.get_area()
        area_id = f'{domain_id}_{area["id"]}'

        if area_id not in data.keys():
            data[f'{area_id}'] = GraphElement(area_id, area["name"], domain_id)

            data[area_id].add_role(f'{icon_manager}{m.get_area_manager()["name"]}')
            data[area_id].add_role(f'{icon_user}{m.get_area_user()["name"]}')

        # Subarea
        if m.has_subarea() == True:
            subarea = m.get_subarea()
            subarea_id = f'{area_id}_{subarea["id"]}'

            if subarea_id not in data.keys():
                data[f'{subarea_id}'] = GraphElement(subarea_id, subarea["name"], area_id)

                data[subarea_id].add_role(f'{icon_manager}{m.get_subarea_manager()["name"]}')
                data[subarea_id].add_role(f'{icon_user}{m.get_subarea_user()["name"]}')

        # Machine
        if m.has_subarea() == False:
            handle = area_id
        else:
            handle = subarea_id

        if m.has_customrole() is True:
            customrole = m.get_customrole()["name"]
            data[handle].add_role(f'{icon_custom}{customrole}')
        else:
            customrole = ''

        machine_name = m.get_machine()["name"]

        data[handle].add_machine(machine_name, customrole)

    data = dict_sort(data)

    return data


def graph_create_mermaidcode(graphelements):
    linedata = []

    wrapper = True
    wrapper_open = False
    wrapper_current = ''

    font_sizes = [2, 1.75, 1.5, 1.25]
    connectors = ['---', '------', '----', '------', '------']

    crossing = '''
$id{"<p style="opacity: 0;">.</p>"}
$id--------$parent
style $id fill: black, stroke: none
'''

    subgraph = '''
subgraph $id["
    <p style="font-size: $fontsizeem">$name</p><p style="text-align: left; margin-top: 20px;">$string_roles</p>
    <p style="text-align: left; margin-top: 0px;">$string_machines</p>
    <p style="opacity: 0;">.</p>
"]
end'''

    fillernode = '''
subgraph filler_$id_1["
<p style="opacity: 0;">
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
</p>"]
end
style filler_$id_1 fill: none, stroke: none
$id~~~~~~filler_$id_1

subgraph filler_$id_2["
<p style="opacity: 0;">
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
</p>"]
end
style filler_$id_2 fill: none, stroke: none
filler_$id_1~~~~~filler_$id_2
'''

    legend = f'''
subgraph legende["<b>Legende</b><p style="text-align:left;">{icon_admin} = Administrator
{icon_manager} = Manager
{icon_user} = Benutzer
{icon_custom} = Benutzer (Alternativrolle)"]
end'''

    linedata.append('%%{init: {"flowchart" : {"curve" : "linear"}}}%%')
    linedata.append(' ')
    linedata.append('flowchart TD')
    linedata.append(' ')
    linedata.append(' ')
    linedata.append(legend)
    linedata.append(' ')
    linedata.append(' ')

    for id, data  in graphelements.items():

        if wrapper == True:
            if data.get_level() == 2 and wrapper_open == True:
                if wrapper_current not in id:
                    linedata.append(' ')
                    linedata.append('end')
                    linedata.append(' ')
                    wrapper_open = False

            if data.get_level() == 2 and wrapper_open == False:
                linedata.append(' ')
                # linedata.append(f'{data.get_parent()} {data.get_level() * '---'} {data.get_id()}_wrapper')
                linedata.append(f'{data.get_parent()} {connectors[data.get_level()]} {data.get_id()}_wrapper')
                linedata.append(f'subgraph {data.get_id()}_wrapper["<p style="opacity: 0;">.</p>"]')
                linedata.append(f'style {data.get_id()}_wrapper stroke: none, fill: none')
                linedata.append(' ')
                wrapper_open = True
                wrapper_current = id

        if len(data.get_roles()) > 0:
            string_roles = '<b><center>Rollen</center></b>$roles</p>'
            string_roles = string_roles.replace('$roles', list_join(data.get_roles(), '<br>'))
        else:
            string_roles = ''

        if len(data.get_machines()) > 0:
            string_machines = '<b><center>Maschinen</center></b>$machines'
            string_machines = string_machines.replace('$machines', list_join(data.get_machines(), '<br>'))
        else:
            string_machines = ''


        graph = subgraph.replace('$id', data.get_id())
        graph = graph.replace('$fontsize', str(font_sizes[data.get_level()]))
        graph = graph.replace('$name', data.get_name())
        graph = graph.replace('$string_roles', string_roles)
        graph = graph.replace('$string_machines', string_machines)

        linedata.append(graph)
        linedata.append(' ')

        if data.get_level() > 0:
            if data.get_level() != 2:
                # linedata.append(f'{data.get_parent()} {data.get_level() * '------'} {id}')
                linedata.append(f'{data.get_parent()} {connectors[data.get_level()]} {id}')

                linedata.append(' ')

            if data.get_level() == 2:
                if dict_keycount(graphelements, id) == 1:
                    node = fillernode.replace('$id', id)

                    linedata.append(' ')
                    linedata.append(node)
                    linedata.append(' ')


    linedata.append(' ')
    linedata.append('end')

    return linedata
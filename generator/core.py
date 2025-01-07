from string import Template

from generator.globals import *
from generator.helpers import *

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
            "actor_type": actor_type
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
    machines = {}
    data = csv_listdict(file, settings['csv_delimiter'], csv_match)

    count = 2
    print(f'{"Zeile": ^8} | {"Status": ^24} | {"Zusatzinformation": ^20}')
    print(f'{"1": ^8} | {"Kopfzeile": ^24} | {"Kopfzeile wird nicht verarbeitet.": ^20}')

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
                errors.append(f'Optionales Felderpaar unvollständig: Feld "{field1_name}" ist ausgefüllt, aber Feld "{field2_name}" ist leer.')

            if len(entry[field2]) > 0 and len(entry[field1]) == 0:
                errors.append(f'Optionales Felderpaar unvollständig: Feld "{field2_name}" ist ausgefüllt, aber Feld "{field1_name}" ist leer.')

        status = 'Eintrag übersprungen'
        info = f'Fehlerhafte Konfiguration. ID = {entry["machine_id"]}'
        if len(errors) > 0:
            print(f'{count: ^8} | {status: ^24} | {info: ^20}')
            for e in errors:
                print(f'{"":>36}| ' + e)
            count += 1
            continue

        #  Maschine anlegen
        temp = Machine(entry)
        fa_id = temp.get_machine()["fa_id"]

        if fa_id not in machines.keys():
            machines.update({
                f'{fa_id}': Machine(entry)
            })

            status = 'Maschine angelegt'
            info = f'FA_ID = {fa_id}'

            print(f'{count: ^8} | {status: ^24} | {info: ^20}')
        else:
            status = 'Eintrag übersprungen'
            info = f'ID bereits vergeben. ID = {entry["machine_id"]}'
            print(f'{count: ^8} | {status: ^24} | {info: ^20}')

        count += 1

    return machines




# Rollen erstellen
def generate_roles(machines):

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

    
    print_dict(roles)

    return roles

    
def generate_bffh_roles(roles):

    data = []

    # Anfang Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + 'roles = {')
    else:
        data.append('{')

    # Inhalt
    last = len(roles) - 1

    for index, role in enumerate(roles):
        data.append(space * 1 + extraspace + f'{role}' + ' =')
        data.append(space * 1 + extraspace + '{')
        data.append(space * 2 + extraspace + 'permissions =  [')
        for perm in roles[role]["perms"]:
            data.append(space * 4 + f'"{perm}",')
        data.append(space * 2 + extraspace + ']')

        if index == last:
            data.append(space * 1 + extraspace + '}')
        else:
            data.append(space * 1 + extraspace + '},')

        data.append(' ')
    
    # Ende Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + '},')
    else:
        data.append('}')

    return data

# Maschinen
def generate_bffh_machines(machines):

    data = []

    # Anfang Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + 'machines = {')
    else:
        data.append('{')

    # Inhalt
    last = len(machines) - 1

    for index, (id, m) in enumerate(machines.items()):
        specs = m.get_machine()
        data.append(space * 1 + extraspace + f'{specs["fa_id"]}' + ' =')
        data.append(space * 1 + extraspace + '{')
        data.append(space * 2 + extraspace + f'name = "{specs["name"]}",')
        data.append(space * 2 + extraspace + f'description = "{specs["desc"]}",')
        data.append(space * 2 + extraspace + f'wiki = "{specs["wikiurl"]}",')
        data.append(space * 2 + extraspace + f'category = "{specs["category"]}",')


        for i in range(len(specs["perms"])):
            data.append(space * 2 + extraspace + f'{specs["perms_names"][i]} = "{specs["perms"][i]}",')

        if index == last:
            data.append(space * 1 + extraspace + '}')
        else:
            data.append(space * 1 + extraspace + '},')
        data.append(' ')

    # Ende Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + '},')
    else:
        data.append('}')

    return data

# Aktoren
def generate_bffh_actors(machines):

    data = []

    # Anfang Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + 'actors = {')
    else:
        data.append('{')

    # Inhalt
    last = len(machines) - 1

    for index, (id, m) in enumerate(machines.items()):
        specs = m.get_machine()

        if len(specs["actor_id"]) > 0 and len(specs["actor_type"]) > 0:
            actor_handle = specs["actor_type"] + '_' + specs["actor_id"]

            # 2do Actor Library Funktionalität

            data.append(space * 1 + extraspace + f'{actor_handle} =')
            data.append(space * 1 + extraspace + '{')
            data.append(space * 2 + extraspace + f'module = "{actor_library[specs["actor_type"]]["module"]}",')
            data.append(space * 2 + extraspace + 'params =')
            data.append(space * 2 + extraspace + '{')

            # Aktor-ID der aktuellen Maschine speichern
            replace = {
                "actor_id": specs["actor_id"]
            }

            for key, value in actor_library[specs["actor_type"]]["params"].items():
                    template = Template(value)
                    string = template.substitute(replace)
                    data.append(space * 3 + extraspace + f'{key} = {string},')

            data.append(space * 2 + extraspace + '}')

            if index == last:
                data.append(space * 1 + extraspace + '}')
            else:
                data.append(space * 1 + extraspace + '},')

            data.append(' ')

    # Ende Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + '},')
    else:
        data.append('}')

    return data


# Aktoren-Verbindungen
def generate_bffh_actorconnections(machines):

    data = []

    # Anfang Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + 'actor_connections = [')
    else:
        data.append('[')

    # Inhalt
    last = len(machines) - 1

    for index, (id, m) in enumerate(machines.items()):
        specs = m.get_machine()

        if len(specs["actor_id"]) > 0 and len(specs["actor_type"]) > 0:
            actor_fullid = specs["actor_type"] + '_' + specs["actor_id"]

            if index == last:
                data.append(space * 1 + extraspace + '{ ' + f'machine = "{specs["fa_id"]}", actor = "{actor_fullid}"' + ' }')
            else:
                data.append(space * 1 + extraspace + '{ ' + f'machine = "{specs["fa_id"]}", actor = "{actor_fullid}"' + ' },')

    # Ende Datenstruktur
    if settings["fa_dhall_create"] == False:
        data.append(space + '],')
    else:
        data.append(']')

    return data


# CSV-Rollenliste

def generate_csv_roles(roles):
    data = []
    data.append('ID der Rolle; Name der Rolle')
    for id, values in roles.items():
        string = id + ';' + values["name"]
        data.append(string)

    return data



# bffh.dhall aktualisieren

def generate_bffh_dhall(generated_content):

    dhall_file = settings["fa_dhall_file"]

    reader = open(dhall_file, "r", encoding='utf-8')

    data_write = []

    inside_generator_block = False
    found_generator_block = False

    count = 1

    # bffh.dhall zeilenweise durchlaufen
    for line in reader:

        # Beginn des Generator-Blocks gefunden --> Erzeugte Daten anhängen, Variablen umschalten
        if 'GENERATOR START' in line:
            found_generator_block = True
            inside_generator_block = True
            data_write.append(line.replace('\n', ''))
            data_write.append(' ')
            data_write += generated_content
            data_write.append(' ')
            added_generated_content = True
            # print(f'{count} Generatorblock-Anfang gefunden')

        # Beginn des Generator-Blocks gefunden --> Variable umschalten
        if 'GENERATOR END' in line:
            inside_generator_block = False
            # print(f'{count} Generatorblock-Ende gefunden')

        # Zeile liegt außerhalb des Generator-Blocks --> Zeile übernehmen
        if inside_generator_block == False:
            data_write.append(line.replace('\n', ''))

        # Zeile liegt innerhalb des Generator-Blocks --> Zeile übernehmen
        if inside_generator_block == True:
            # Einfügung wurden vorgenommen, Zeile aus bffh.dhall ignorieren
            continue

    if found_generator_block == True:
        return data_write
    else:
        print('Datei "bffh.dhall" enthält keinen Platzhalter zum automatischen Einfügen.')
        return []


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
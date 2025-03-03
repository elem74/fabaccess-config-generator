from generator.helpers import config_load
from generator.helpers import load_plugins

# Icons für Mermaid-Code

icon_admin = "👑"
icon_manager = "🛠️"
# icon_user = "🧍"
icon_user = "👷‍♂️"
icon_custom = '👩‍🚀'


# Daten für den zentrale Rollen
admin_global = {
    "id": "Admin",
    "name": "_Admin FabAccess",
    "perms": ["bffh.users.manage", "bffh.users.info", "bffh.users.admin"]
}

manager_domain = {
    "id": "_manager_schichtleitung",
    "name": "_Manager Schichtleitung",
    "perms": []
}

#  Daten für CSV-Import
csv_match = {
    "Name Domäne": "domain_name",
    "Name Bereich": "area_name",
    "Name Unterbereich": "subarea_name",
    "ID Domäne": "domain_id",
    "ID Bereich": "area_id",
    "ID Unterbereich": "subarea_id",
    "ID Maschine": "machine_id",
    "Manager Unterbereich": "subarea_manager",
    "Name Bereich": "area_name",
    "Name Unterbereich": "subarea_name",
    "Name Maschine": "machine_name",
    "Maschinenbeschreibung": "machine_desc",
    "Wiki-URL": "wikiurl",
    "Aktor ID": "actor_id",
    "Aktor Modul": "actor_module",
    "Aktor Typ": "actor_type",
    "Initiator ID": "initiator_id",
    "Initiator Modul": "initiator_module",
    "Initiator Typ": "initiator_type",
    "ID Alternativrolle": "customrole_id",
    "Name Alternativrolle": "customrole_name",
}

importcheck = {
    "single": {
        "domain_name": "",
        "domain_id": "",
        "area_id": "",
        "machine_id": "",
        "area_name": "",
        "machine_name": "",
        },
    "pairs": {
        "subarea_id": "subarea_name",
        "customrole_id": "customrole_name",
        }
}

space = '\t'
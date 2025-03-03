import os
import re
import csv
from configparser import ConfigParser

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
app_path = parent_directory

# String Cleanup
def string_clean(string):

    zeichen = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
        "²": "2",
        "³": "3",
    }

    for el in zeichen:
        string = string.replace(el, zeichen[el])

    string = re.sub('[^a-zA-Z0-9]','',string)

    return string

def string_removequotes(string):
    string = string.replace('"', '')

    return string

def dict_sort(data):
    data = dict(sorted(data.items()))
    return data

def dict_keycount(data, key):
    count = 0
    for d in data:
        if key in d:
            count += 1
    return count

def list_join(my_list, insert):
    my_string = f'{insert}'.join(str(element) for element in my_list)
    return my_string

# CSV-Delimiter ermitteln
def csv_getdelimiter(file: str) -> str:
    with open(file, 'r') as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter

# CSV einlesen: Erzeugt eine Liste, die für jede Zeile ein Dictionary mit Header und Value ausgibt
def csv_listdict(filename, replacedict = {}):

    csv_delimiter = csv_getdelimiter(filename)

    csvfile = open(filename, 'r', encoding='utf-8-sig')
    tempfile = ''

    # Dictionary mit Ersetzungen vorhanden:
    if len(replacedict) > 0:
        tempdata = []

        # Tempfile mit aktualisiertem Header erzeugen
        for el in csvfile:
            tempdata.append(el)

        for key in replacedict:
            tempdata[0] = tempdata[0].replace(key, replacedict[key])

        tempfile = 'temp.csv'
        csvfile.close()

        write_file(tempfile, tempdata)
        filename = tempfile


    # Dictionary bilden
    csvfile = open(filename, mode='r', encoding='utf-8-sig')
    reader = csv.DictReader(csvfile, delimiter=csv_delimiter)

    finaldata = []

    for row in reader:
        finaldata.append(row)
    csvfile.close()

    if len(tempfile) > 0:
        os.remove(tempfile)

    return finaldata


# Datei schreiben
def write_file(filename, content):
    f = open(filename, "w", encoding='utf-8', newline='\n')
    for line in content:
        if '\n' in line:
            f.write(line)
        else:
            f.write(line + '\n')
    f.close()

# Dictionary schön ausgeben
def print_dict(d,depth=0):

    if depth == 0:
        print('')
        print(' ----- Dictionary ----- ')

    space = "    "
    if depth == 0:
        string = ''
    else:
        string = space * depth + '|- '

    for k,v in sorted(d.items(),key=lambda x: x[0]):
        if isinstance(v, dict):
            print(string + ("%s" % k))
            print_dict(v,depth+1)
        else:
            print(string + "%s = %s" % (k, v))

# Array ausgeben
def print_array(array):
    for el in array:
        print(el)

# Gesamte Config einlesen und Sektionen als Einzelwerte speichern
def config_load(file, section = 'all'):
    dict_settings = {}

    filehandle = app_path + f'/{file}'

    config = ConfigParser()
    config.read(filehandle)

    list_sections = config.sections()

    if section == 'all':
        # Mehrere Sections
        for section in list_sections:

            dict_settings[section] = {}

            content = dict(config.items(section))

            for key in content:

                value = content[key]

                #  Integer
                if value.isdigit() == True:
                    save = int(value)
                #  Boolean
                elif value == 'True':
                    save = True
                elif value == 'False':
                    save = False
                else:
                    save = value

                dict_settings[section][key] = save
    else:
            # Einzelne Section
            content = dict(config.items(section))

            for key in content:

                value = content[key]

                #  Integer
                if value.isdigit() == True:
                    save = int(value)
                #  Boolean
                elif value == 'True':
                    save = True
                elif value == 'False':
                    save = False
                else:
                    save = value

                dict_settings[key] = save

    return dict_settings

# Actor-Library einlesen
def load_plugins(file):
    dict_actors = {}

    filehandle = app_path + f'/{file}'

    config = ConfigParser()
    config.read(filehandle)

    section_list = config.sections()

    for section in section_list:

        actor = section.lower()
        dict_actors[actor] = {
            "module": '',
            "params": {}
        }

        content = dict(config.items(section))

        for key, value in content.items():


            if key == "module":
                dict_actors[actor]["module"] = value

            if 'param_' in key:
                param_name = key.replace('param_', '').lower()
                dict_actors[actor]["params"][param_name] = value

            # print (f'{key} = {value}')

    return dict_actors
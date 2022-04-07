import json
import re
read = json.loads(input())
def timevalidator(time):
    regex = '^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    p = re.compile(regex);
    if (time == ""):
        return False;
    m = re.search(p, time)
    if m is None :
        return False;
    else :
        return True


mask = {
    "bus_id": {'type': int, 'required': 'required', 'format': ''},
    "stop_id": {'type': int, 'required': 'required', 'format': ''},
    "stop_name": {'type': str, 'required': 'required', 'format': '[Name] [Suffix]'},
    "next_stop": {'type': int, 'required': 'required', 'format': ''},
    "stop_type": {'type': str, 'required': 'optional', 'format': 'UPPER', 'values': ['S', 'O', 'F', '']},
    "a_time": {'type': str, 'required': 'required', 'format': 'dtime HH:MM'}
}
routes = {
    128: ['Prospect Avenue', 'Elm Street', 'Sunset Bouleward', 'Seasame Street'],
    256: ['Seasame Street', 'Fifth Avenue', 'Elm Street', 'Pilotow Street'],
    512: ['Sunset Boulevard', 'Bourbon Street']
}
stops = {
    1: 'Prospect Avenue',
    2: 'Pilotow Street',
    3: 'Elm Street',
    4: 'Bourbon Street',
    5: 'Fifth Avenue',
    6: 'Sunset Bouleward',
    7: 'Seasame Street'
}
med = {
    "bus_id": 0,
    "stop_id": 0,
    "stop_name": 0,
    "next_stop": 0,
    "stop_type": 0,
    "a_time": 0
}

for i in range(len(read)):
    bus_id = read[i]['bus_id']
    stop_id = read[i]['stop_id']
    stop_name = read[i]['stop_name']
    next_stop = read[i]['next_stop']
    stop_type = read[i]['stop_type']
    a_time = read[i]['a_time']
    if isinstance(bus_id, mask['bus_id']['type']) == False:
        med['bus_id'] += 1
    if isinstance(stop_id, mask['stop_id']['type']) == False:
        med['stop_id'] += 1
    if isinstance(stop_name, mask['stop_name']['type']) == False or len(stop_name) == 0 or len([i for i in stop_name.split(' ') if i.istitle()]) >= 2 == False:
        med['stop_name'] += 1
    if isinstance(next_stop, mask['next_stop']['type']) == False:
        med['next_stop'] += 1
    if isinstance(stop_type, mask['stop_type']['type']) == False or (stop_type in mask['stop_type']['values']) == False:
        med['stop_type'] += 1
    if isinstance(a_time, mask['a_time']['type']) == False or timevalidator(a_time) == False:
        med['a_time'] += 1
if sum(med.values()) > 0:
    print(f'Type and required field validation: {sum(med.values())} errors')
    for key in med.keys():
        print(f'{key}: {med[key]}')

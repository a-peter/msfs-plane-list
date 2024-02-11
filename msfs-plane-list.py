from datetime import datetime
import configparser
import csv
import openpyxl as op
import os
import sys

# Tries to determine the folders for the Steam and the Store version of MSFS.
# For each match, the name of the installation and the location of the
# packages folder is add to an array
def get_packages_folders():
    appdata = [('Steam', '{APPDATA}\\Microsoft Flight Simulator\\usercfg.opt'), ('Store', '{LOCALAPPDATA}\\Packages\\Microsoft.FlightSimulator_8wekyb3d8bbwe\\LocalCache\\usercfg.opt')]
    packages = []
    for source in appdata:
        file_name = source[1].format(**os.environ)
        if os.path.isfile(file_name):
            for line in open(file_name):
                if line.startswith('InstalledPackagesPath'):
                    packages.append((source[0], line.split('"')[1]))
    print('Found package folder:', packages)
    return packages

# Iterates over a packages folder and determines all aircrafts.
# Returns the path for the aircraft.cfg and the flight_model.cfg files.
def find_aircrafts(package_path: str):
    aircraft_cfg_name = 'aircraft.cfg'
    flight_model_cfg_name = 'flight_model.cfg'

    aircrafts = []
    for path, _, files in os.walk(package_path):
        for name in files:
            if name.endswith(flight_model_cfg_name):
                aircrafts.append((path, os.path.join(path, aircraft_cfg_name), os.path.join(path, flight_model_cfg_name)))

    return aircrafts

# Reads the content of an aircraft.cfg file.
# Returns a dictionary of found data.
def read_aircraft_cfg(file_name):
    KEY_1 = 'GENERAL'
    VALUES_1 = ['icao_manufacturer', 'icao_type_designator', 'icao_model']
    KEY_2 = 'FLTSIM.0'
    VALUES_2 = ['ui_certified_ceiling', 'ui_max_range', 'ui_autonomy']

    aircraft_cfg = configparser.ConfigParser(strict=False, inline_comment_prefixes=(';'))
    aircraft_cfg.read(file_name)
    data = {}
    data.update({key:aircraft_cfg[KEY_1][key].replace('"', '') for key in VALUES_1})
    data.update({key:float(aircraft_cfg[KEY_2][key]) for key in VALUES_2})
    return data
    
# Reads the content of a flight_model.cfg file.
# Returns a dictionary of found data.
def read_flight_model_cfg(file_name):
    KEY_3 = 'REFERENCE SPEEDS'
    VALUES_3 = ['cruise_speed']

    flight_model_cfg = configparser.ConfigParser(strict=False, inline_comment_prefixes=(';'), comment_prefixes=('#',';','/'))
    flight_model_cfg.read(file_name)
    data = {}
    data.update({key:float(flight_model_cfg[KEY_3][key]) for key in VALUES_3})
    return data

# Imports the data for a list of aircrafts. 
# Returns a list of dictionaries containing the data
def read_aircrafts_data(aircrafts):
    aircrafts_data = []
    for aircraft in aircrafts:
        try:
            data_row = {}
            data_row.update(read_aircraft_cfg(aircraft[1]))
            data_row.update(read_flight_model_cfg(aircraft[2]))
            aircrafts_data.append(data_row)
        except KeyError:
            pass
    print(f'Found {len(aircrafts_data)} aircrafts')
    return aircrafts_data

HEADERS = ['Manufacturer', 'Type', 'Model', 'Ceiling [ft]', 'Range [nm]', 'Duration [h]', 'Cruise speed [kt]']

# Exports aircraft data to an excel file.
def export_to_excel(package_name, aircrafts_data):
    wb = op.Workbook()
    ws = wb.active
    [ws.cell(row=1, column=j+1, value=v) for j,v in enumerate(HEADERS)]

    row = 2
    for data_row in aircrafts_data:
        [ws.cell(row=row, column=j+1, value=v) for j,v in enumerate(data_row.values())]
        row += 1

    # Set auto-filter, fill style and freeze line
    filter = ws.auto_filter
    filter.ref = 'A:G'
    fill = op.styles.PatternFill(start_color='FFCEF8FF', end_color='FFCEF8FF', fill_type='solid')
    for c in range(7):
        ws.cell(row=1, column=c+1).fill = fill
    ws.freeze_panes = "A2"

    wb.save(f'aircrafts-{package_name}.xlsx')

# Exports aircraft data to an excel file.
def export_to_csv(package_name, aircrafts_data: dict):
    with open(f'aircrafts-{package_name}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(HEADERS)
        for data_row in aircrafts_data:
            writer.writerow([v for v in data_row.values()])

# Main program
if __name__ == '__main__':
    log_file = 'aircrafts.log'
    packages = get_packages_folders()

    if len(packages) == 0:
        f = open(log_file, '+a')
        f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Could not find any package folders\n')
        f.close()
        sys.exit(1)

    for package in packages:
        with open(log_file, '+a') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Scanning "{package[1]}" for aircrafts\n')
            aircrafts = find_aircrafts(package[1])
            aircrafts_data = read_aircrafts_data(aircrafts)
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Found {len(aircrafts_data)} aircrafts\n')

            export_to_excel(package[0], aircrafts_data)
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Written to "aircrafts-{package[0]}.xlsx"\n')

            export_to_csv(package[0], aircrafts_data)
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Written to "aircrafts-{package[0]}.csv"\n')
import os
import shutil
import configparser
import subprocess
import psutil
import time
from distutils.dir_util import copy_tree
import csv
import configparser
import json
import pandas as pd

global player

# checking if required folders are here
if not os.path.isdir('./players'):
    os.mkdir('./players')

if not os.path.isdir('./leaderboard'):
    os.makedirs('./leaderboard')
for track in ['zandvoort', 'nurburgring', 'monza']:
    if not os.path.exists('./leaderboard/leaderboard_{}.csv'.format(track)):
        leaderboard = open('./leaderboard/leaderboard_{}.csv'.format(track), 'w', newline='')
        leaderboard_writer = csv.writer(leaderboard, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        leaderboard_writer.writerow(['Driver', 'Time'])


def launch_game(app_id, launcher_exe_path, player):
    steam_exe_path = r"D:\Programme (x86)\Steam\Steam.exe"  # Update this with the correct path to your Steam executable

    command = [steam_exe_path, f"steam://rungameid/{app_id}"]
    subprocess.Popen(command)

    # Monitor the launcher process until it is no longer running
    status_launcher = 'game launching'
    status_simulation = 'stopped'
    while True: 
        launcher_process = None
        simulation_process = None

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == launcher_exe_path:
                launcher_process = proc
                break

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'acs.exe':
                simulation_process = proc
                break
                
            
        match status_launcher:
            case 'game launching':
                if launcher_process is not None:
                    status_launcher = 'game running'
                    print('Game launched')
        
            case 'game running':
                if launcher_process is None:
                    break
        
        match status_simulation:
            case 'stopped':
                if simulation_process is not None:
                    status_simulation = 'running'
                    print('Simulation launched')
            case 'running':
                if simulation_process is None:
                    status_simulation = 'stopped'
                    add_entry(player)

        time.sleep(.1)

    print("Game closed")


def load_player(player):
    # Replacing personnal record file
    user = os.getlogin()
    source = './players/{}'.format(player)
    destination = 'C:/Users/{}/Documents/Assetto Corsa'.format(user)

    cfg_files = [f for f in os.listdir(destination + '/cfg') if os.path.isfile(os.path.join(destination + '/cfg', f))]

    if os.path.isdir(destination + '/launcherdata'):
        shutil.rmtree(destination + '/launcherdata')
    if os.path.exists(destination + '/personalbest.ini'):
        os.remove(destination + '/personalbest.ini')
    for file in cfg_files:
        if os.path.isfile(destination + '/cfg/' + file):
            os.remove(destination + '/cfg/' + file)
    
    copy_tree(source, destination)

    print("Profile of player {} loaded".format(player))


def save_player(player):
    # Saving updated PB and launcherdata after game is closed
    user = os.getlogin()
    destination = './players/{}'.format(player)
    source = 'C:/Users/{}/Documents/Assetto Corsa'.format(user)

    cfg_files = [f for f in os.listdir(source + '/cfg') if os.path.isfile(os.path.join(source + '/cfg', f))]

    if os.path.isdir(destination + '/launcherdata'):
        shutil.rmtree(destination + '/launcherdata')
    if os.path.exists(destination + '/personalbest.ini'):
        os.remove(destination + '/personalbest.ini')

    shutil.copy(source + "/personalbest.ini", destination)
    copy_tree(source + "/launcherdata", destination + "/launcherdata")

    for file in cfg_files:
        if os.path.isfile(destination + '/cfg/' + file):
            os.remove(destination + '/cfg/' + file)
        shutil.copy(source + '/cfg/' + file, destination + '/cfg')

    print("Profile of player {} saved".format(player))


def create_player(player):
    # Create a folder for the new player
    new_folder = './players/{}'.format(player)

    os.makedirs(new_folder)
    os.makedirs(new_folder + '/launcherdata')
    os.makedirs(new_folder + '/cfg')

    config = configparser.ConfigParser()
    with open(new_folder + '/personalbest.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Created new profile for {}".format(player))


def log(player, start, end):
    # add log entry

    if not os.path.exists('./log.csv'):

        log_entry = open('./log.csv', 'w', newline='')
        
        log_writer = csv.writer(log_entry, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        log_writer.writerow(['player', 'session start', 'session end'])
        log_writer.writerow([player, start, end])

    else:

        log_entry = open('./log.csv', 'a', newline='')
        log_writer = csv.writer(log_entry, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([player, start, end])


def check_entry(track, car, assists, penalties):
    # checks if the last race done is prone to joining leaderboard
    if not (assists == 'pro' and penalties == '1'):
        return False
    
    match track[0]:

        case 'ks_nurburgring':
            if not track[1] == 'layout_gp_a':
                return False

            if not car == 'lotus_elise_sc':
                return False

            return True

        case 'monza':
            if not car == 'ks_mclaren_f1_gtr':
                return False
            
            return True
        
        case 'ks_zandvoort':
            if not car == 'ks_ferrari_f2004':
                return False
            
            return True
        
        case _ :
            return False



def add_entry(player):
    # adds an entry to the corresponding leaderboard
    user = os.getlogin()
    source = 'C:/Users/{}/Documents/Assetto Corsa'.format(user)

    launcher = configparser.ConfigParser()
    launcher.read(source + '/cfg/launcher.ini')

    race = configparser.ConfigParser()
    race.read(source + '/cfg/race.ini')

    assists = launcher['SAVED']['ASSISTS']
    penalties = race['RACE']['PENALTIES']
    track = race['RACE']['TRACK'], race['RACE']['CONFIG_TRACK']
    car = race['RACE']['MODEL']

    if check_entry(track, car, assists, penalties):
        pb = json.loads(open(source + '/out/race_out.json').read().replace('\n', '').replace('\t', ''))

        time = pb['extras'][-1]['time']
        
        if time == 0:
            print('Requirement not met (time is 0)')
            return

        t_ms = time % 1000
        t_s = (time // 1000) % 60
        t_m = (time // 1000) // 60

        time_formatted = '{}:{:02}:{:03}'.format(t_m, t_s, t_ms)

        leaderboard_entry = pd.read_csv('./leaderboard/leaderboard_{}.csv'.format(track[0].replace('ks_', '')))
        leaderboard_entry.loc[-1] = [player, time_formatted]
        leaderboard_entry.sort_values('Time').drop_duplicates('Driver').to_csv('./leaderboard/leaderboard_{}.csv'.format(track[0].replace('ks_', '')), index=False)

        print('Entry added succesfully')
    
    else:
        print('Requirement not met')


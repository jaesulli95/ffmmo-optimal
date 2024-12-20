from Core.character.ffxiv_character import FFXIV_Character
from Core.abilities.ability import  FFXIV_Ability
from Core.stats.stat_calculator import calculate_gcd
from Core.abilities.ability_execute import Ability_Execute
import Core.constants.constants as Data_Constants
import json
import pandas as pd
import time
#Libraries that may or may not be used
from pynput.keyboard import Key, Controller
import win32gui as wgui


gauge = 0
keyboard = Controller()

# Read in Character Stats
char_stats = json.load(open('character_stats/jaesuna_warrior_stats.json'))

#Create the Character
#Pass in Stats and Abilities for the character
character = FFXIV_Character("Jaesuna", char_stats, 0)
gcd_from_sks = calculate_gcd(char_stats["Skill_Speed"])
# Read in Abilities - will be the main thing to check.
abilities = pd.read_csv('Skill_Spreadsheets/WAR_Skills.csv')
print(abilities)
abilities_items = abilities.iterrows()

#Abilitiesw
player_abilities =  dict()
player_tags = set()

winlist = []
toplist = []
keyboard = Controller()

def enum_callback(hwnd, results):
    winlist.append((hwnd, wgui.GetWindowText(hwnd)))

wgui.EnumWindows(enum_callback, toplist)
ffxiv = [(hwnd, title) for hwnd, title in winlist if 'final fantasy xiv' in title.lower()]
ff = ffxiv[0]

print(abilities_items)
for index, ability in abilities_items:
    new_ability = FFXIV_Ability(index, ability)
    player_abilities[ability["ability_id"]] = new_ability


gcds = 0
gcds_total = 100
total_potency = 0

wgui.SetForegroundWindow(ff[0])

while gcds < gcds_total:
    for a in player_abilities:
        player_abilities[a].can_activate(abilities, gauge)


    usable_abilities = abilities[(abilities["can_activate"] == "Y") & (abilities["off_gcd"] == "N")]
    index_of_max_potency_usable = usable_abilities["potency"].idxmax()
    ability_to_execute = usable_abilities.loc[index_of_max_potency_usable]
    total_potency += ability_to_execute[Data_Constants.POTENCY]

    activation_return = player_abilities[ability_to_execute["ability_id"]].activate(player_tags)
    #Activate Ability in the game here.
    Ability_Execute.Execute_Ability(player_abilities[ability_to_execute["ability_id"]].AbilityData[Data_Constants.KEY])

    gauge += activation_return[0]
    gauge -= activation_return[1]

    for a in player_abilities:
        player_abilities[a].update(player_tags, abilities)
    gcds += 1
    time.sleep(2.44) #need to improve this

#Need to make it so it activates 10% damage buff.
#Graph Theory - Djikstra's Algorithm
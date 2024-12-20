from Core.jobs_classes import *

class FFXIV_Character:
    def __init__(self, __name, __character_stats, __abilities):
        self.name = __name
        self.abilities = [];
        self.character_stats = __character_stats
        self.abilities = __abilities

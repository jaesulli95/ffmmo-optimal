import Core.constants.constants as Data_Constants
import pandas
import pandas as pd

class FFXIV_Ability():
    def __init__(self, _index_of_ability:int, _AbilityData:pd.Series):
        self.index_of_ability = _index_of_ability
        self.AbilityData = _AbilityData

    '''
        Can it activate does it have the required tags?
    '''
    def can_activate(self, _abilities:pandas.DataFrame, _current_gauge_value):
        if self.AbilityData[Data_Constants.GAUGE_COST] <= _current_gauge_value:
            _abilities.at[self.index_of_ability, Data_Constants.CAN_ACTIVATE] = "Y"
        else:
            _abilities.at[self.index_of_ability, Data_Constants.CAN_ACTIVATE] = "N"

    def activate(self, _player_tags):
        if self.AbilityData[Data_Constants.TAGS_REQUIRED] in _player_tags and \
                self.AbilityData[Data_Constants.TAGS_REQUIRED] != "none":
            _player_tags.remove(self.AbilityData[Data_Constants.TAGS_REQUIRED])
        if self.AbilityData[Data_Constants.TAGS_GRANTED_ON_USE] != "none":
            _player_tags.add(self.AbilityData[Data_Constants.TAGS_GRANTED_ON_USE])

        return self.AbilityData[Data_Constants.GAUGE_GRANT], self.AbilityData[Data_Constants.GAUGE_COST]

    def update(self, _player_tags, AbilityTable):
        if self.AbilityData[Data_Constants.TAGS_REQUIRED] in _player_tags:
            AbilityTable.at[self.index_of_ability, Data_Constants.POTENCY] = self.AbilityData[Data_Constants.COMBO_POTENCY]
        elif self.AbilityData[Data_Constants.TAGS_REQUIRED] not in _player_tags:
            AbilityTable.at[self.index_of_ability, Data_Constants.POTENCY] = self.AbilityData[Data_Constants.POTENCY]
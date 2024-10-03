import sys
sys.path.append('/Users/sailaja/code/Skona')
from app.models import db_models as mdm

import itertools

def create_reg_health_instances():
    reg_health_list = []
    variations = get_variations(3)
    for var in variations:
        reg_health_list.append(mdm.RegularHealth(seeing_vet_more_than_12_months=var[0], reg_worming_treatment=var[1], dog_scratching=var[2]))
    
    return reg_health_list

def create_bone_health_instances():
    bone_health_list = []
    bool_values = [True, False]
    str_values = ["Recent (less than a month)", "Recent past (more than a month and less than 3 months)",
                  "Past (more than 3 months ago)"]
    variations = get_string_variations(bool_values=bool_values, str_values=str_values)
    for var in variations:
        bone_health_list.append(mdm.BoneHealth(stiff_getting_up=var[0], limp_lag_behind=var[1], mobility_issue=var[2], activity_level_change=var[3], specific_movement_struggle=var[4]))
    return bone_health_list


def create_dental_health_instances():
    dental_health_list = []
    variations = get_variations(2)
    for var in variations:
        dental_health_list.append(mdm.DentalHealth(no_brushing_2_months=var[0], dental_stiks=var[1]))
    
    return dental_health_list



def create_gut_health_instances():
    gut_health_list = []
    variations = get_variations(3)
    for var in variations:
        gut_health_list.append(mdm.GutHealth(fishy_odor=var[0], upset_stomach_3month=var[1], scavenge_feaces=var[2]))
    
    return gut_health_list


def get_variations(n):
    variations = list(itertools.product([True, False], repeat=n))
    return variations
    
def get_string_variations(bool_values, str_values):
    variations = list(itertools.product(bool_values, bool_values, str_values, bool_values, bool_values))
    return variations

    
if __name__ == "__main__":
    print("This is running as a standalone")
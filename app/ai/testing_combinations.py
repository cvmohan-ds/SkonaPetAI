import json
s_cases = [
    {
        "reg_helth": [True, True, True],
        "gut_health": [True, True, True],
        "bone_health": [True, True, True, True, True],
        "dental_health": [True, True],
    }
]

def find_all_possible_combinations(s_cases):
    all_combinations = []
    for s_case in s_cases:
        for reg_helth_comb in get_combinations(s_case["reg_helth"]):
            for gut_health_comb in get_combinations(s_case["gut_health"]):
                for bone_health_comb in get_combinations(s_case["bone_health"]):
                    for dental_health_comb in get_combinations(s_case["dental_health"]):
                        combination = {
                            "reg_helth": reg_helth_comb,
                            "gut_health": gut_health_comb,
                            "bone_health": bone_health_comb,
                            "dental_health": dental_health_comb,
                        }
                        all_combinations.append(combination)
    return list(set(all_combinations))

import itertools

def generate_unique_combinations(s_cases):
    all_combinations = list()  # Use a set to automatically eliminate duplicates

    for s_case in s_cases:
        # Generate combinations for each health category
        reg_health_combs = get_combinations(s_case["reg_helth"])
        gut_health_combs = get_combinations(s_case["gut_health"])
        bone_health_combs = get_combinations(s_case["bone_health"])
        dental_health_combs = get_combinations(s_case["dental_health"])

        # Combine one from each category, converting to a hashable tuple for the set
        
        all_combinations.extend( itertools.product(reg_health_combs, gut_health_combs, 
                                             bone_health_combs, dental_health_combs))
            
        
    # Convert back to a list of dictionaries
    unique_combinations = []
    for reg_helth, gut_health, bone_health, dental_health in all_combinations:
        unique_combinations.append({
            "reg_helth": reg_helth,
            "gut_health": gut_health,
            "bone_health": bone_health,
            "dental_health": dental_health,
        })
     
    another_uc = []   
    for comb in unique_combinations:
        if comb not in another_uc:
            another_uc.append(comb)
        else:
            continue
    unique_combinations = another_uc
        

    return unique_combinations

def get_combinations(values):
    combinations = []
    for i in range(len(values) + 1):
        for j in range(i + 1):
            combination = values[:j] + [False] * (len(values) - j)
            combinations.append(combination)
    return combinations





all_combinations = generate_unique_combinations(s_cases)
#print(all_combinations)
print(len(all_combinations))
with open("all_combo.json", "w") as f:
    json.dump(all_combinations, f)

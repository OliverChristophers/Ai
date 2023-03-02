import random
import numpy as np
import os


def outcome_list(outcome):
    if outcome == 0:
        return [1, 0, 0]
    elif outcome == 1:
        return [0, 1, 0]
    else:
        return [0, 0, 1]


def signal(n_outcomes, max_p_share):
    list_probabilities = []
    remainder = 1
    for i in range(n_outcomes - 1):
        p = random.uniform(0, max_p_share) * remainder
        list_probabilities.append(p)
        remainder -= p
    list_probabilities.append(remainder)
    list_probabilities.sort()
    return list_probabilities


def noise(list_probabilities, noise_sd):
    list_noisy_probabilities = []
    for i in range(len(list_probabilities) - 1):
        list_noisy_probabilities.append(list_probabilities[i] + np.random.normal(0, noise_sd))
    list_noisy_probabilities.append(1 - sum(list_noisy_probabilities))
    return list_noisy_probabilities


def apply_margin(list_noisy_probabilities, list_margin_range):
    margin = random.uniform(list_margin_range[0], list_margin_range[1])
    for i in range(len(list_noisy_probabilities)):
        list_noisy_probabilities[i] = round(1 / (list_noisy_probabilities[i] + (margin / len(list_noisy_probabilities))), 2)
    return list_noisy_probabilities


def one_event(n_bookmakers, n_outcomes, max_p_share, noise_sd, list_margin_range):
    list_probabilities = signal(n_outcomes, max_p_share)
    outcome = outcome_list(list_probabilities.index(random.choices(list_probabilities, list_probabilities)[0]))
    list_bookmakers_final = []
    for i in range(n_bookmakers):
        list_noisy_probabilities = noise(list_probabilities, noise_sd)
        list_bookmakers_final.append(apply_margin(list_noisy_probabilities, list_margin_range))
    return [list_probabilities, outcome, list_bookmakers_final]


def no_arb_and_min_odds_greater_1(list_bookmakers_final, min_arb_sum, min_odds, max_odds):
    list_0, list_1, list_2 = [], [], []
    for bookmaker in list_bookmakers_final:
        list_0.append(bookmaker[0])
        list_1.append(bookmaker[1])
        list_2.append(bookmaker[2])
    arb = sum([1 / max(list_0), 1 / max(list_1), 1 / max(list_2)])
    if arb < min_arb_sum or min([min(list_0), min(list_1), min(list_2)]) < min_odds or max([max(list_0), max(list_1), max(list_2)]) > max_odds:
        return False
    else:
        return True


def one_good_event(n_bookmakers, n_outcomes, max_p_share, noise_sd, list_margin_range, min_arb_sum, min_odds, max_odds):
    while True:
        list_probabilities, outcome, list_bookmakers_final = one_event(n_bookmakers, n_outcomes, max_p_share, noise_sd, list_margin_range)
        if no_arb_and_min_odds_greater_1(list_bookmakers_final, min_arb_sum, min_odds, max_odds):
            break
    return [list_probabilities, outcome, list_bookmakers_final]


n_events = 1000000 #number of data points
n_bookmakers = 7 #can be randomised within the for loop
n_outcomes = 3 #in this case, home, draw, away
max_p_share = 0.8 #do not want one outcome having more than this proportion of the remaining probability 
noise_sd = 0.01 #in a normal distribution, the standard deviaiton of the noise term. 68% of noise terms will be within +- noise_sd
list_margin_range = [0.03, 0.06] #the min and max margin a bookmaker can apply
min_arb_sum = 1.005 #across the outcomes, the sum of the implied probabilities of the longest odds must be >= min_arb_sum
min_odds = 1.1 #no odds allowed below min_odds
max_odds = 15 #no odds allowed above max_odds

with open(os.path.realpath(rf'generated_data.txt'), 'a') as f:
    for i in range(n_events):
        print(i)
        #n_bookmakers = random.randint(5,10) #if you want random n bookmakers per event
        list_probabilities, outcome, list_bookmakers_final = one_good_event(n_bookmakers, n_outcomes, max_p_share, noise_sd, list_margin_range, min_arb_sum, min_odds, max_odds)
        list_lists_outcome_j_odds = []
        for j in range(n_outcomes):
            list_lists_outcome_j_odds.append([])
            for bookmaker_list in list_bookmakers_final:
                list_lists_outcome_j_odds[-1].append(1 / bookmaker_list[j])
        list_all = []
        for odds_list_outcome in list_lists_outcome_j_odds:
            odds_list_outcome.sort()
            for odds in odds_list_outcome:
                list_all.append(odds)
        bo_txt = f'{list_probabilities}; {outcome}; {list_all}'
        f.write(f'\n{bo_txt}')

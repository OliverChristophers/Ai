import random
import numpy as np
import os
import scipy.stats


def outcome_list(outcome):
    if outcome == 0:
        return [1, 0, 0]
    elif outcome == 1:
        return [0, 1, 0]
    else:
        return [0, 0, 1]


def signal(p1_parameters, p2_parameters):
    while True:
        p1 = scipy.stats.burr.rvs(p1_parameters[0], p1_parameters[1], p1_parameters[2], p1_parameters[3])
        p2 = (1 - p1) * scipy.stats.burr.rvs(p2_parameters[0], p2_parameters[1], p2_parameters[2], p2_parameters[3])
        p3 = 1 - p1 - p2
        if min([p1, p2, p3]) > 0:
            break
    list_probabilities = [p1, p2, p3]
    list_probabilities.sort()
    return list_probabilities


def noise(list_probabilities, noise_sd):
    list_noisy_probabilities = []
    for i in range(len(list_probabilities) - 1):
        list_noisy_probabilities.append(list_probabilities[i] + np.random.normal(0, noise_sd))
    list_noisy_probabilities.append(1 - sum(list_noisy_probabilities))
    return list_noisy_probabilities


def apply_margin(list_noisy_probabilities, margin_parameters, margin_i_parameters):
    margin = np.random.normal(margin_parameters[0], margin_parameters[1])
    for i in range(len(list_noisy_probabilities)):
        list_noisy_probabilities[i] = round(1 / (list_noisy_probabilities[i] * (1 + margin * scipy.stats.alpha.rvs(margin_i_parameters[0], margin_i_parameters[1], margin_i_parameters[2]))), 2)
    return list_noisy_probabilities


def one_event(n_bookmakers, p1_parameters, p2_parameters, noise_sd, margin_parameters, margin_i_parameters):
    list_probabilities = signal(p1_parameters, p2_parameters)
    outcome = outcome_list(list_probabilities.index(random.choices(list_probabilities, list_probabilities)[0]))
    list_bookmakers_final = []
    for i in range(n_bookmakers):
        list_noisy_probabilities = noise(list_probabilities, noise_sd)
        list_bookmakers_final.append(apply_margin(list_noisy_probabilities, margin_parameters, margin_i_parameters))
    return [list_probabilities, outcome, list_bookmakers_final]


def no_arb(list_bookmakers_final, arb_parameters, odds_range):
    list_0, list_1, list_2 = [], [], []
    for bookmaker in list_bookmakers_final:
        list_0.append(bookmaker[0])
        list_1.append(bookmaker[1])
        list_2.append(bookmaker[2])
    arb = sum([1 / max(list_0), 1 / max(list_1), 1 / max(list_2)]) - 1
    if scipy.stats.burr.cdf(arb, arb_parameters[0], arb_parameters[1], arb_parameters[2], arb_parameters[3]) > random.uniform(0, 1):
        list_o = []
        for list_b in list_bookmakers_final:
            for o in list_b:
                list_o.append(o)
        if min(list_o) > odds_range[0] and max(list_o) < odds_range[1]:
            return True
        else:
            return False
    else:
        return False


def one_good_event(n_bookmakers, p1_parameters, p2_parameters, noise_sd, margin_parameters, margin_i_parameters, arb_parameters, odds_range):
    while True:
        list_probabilities, outcome, list_bookmakers_final = one_event(n_bookmakers, p1_parameters, p2_parameters, noise_sd, margin_parameters, margin_i_parameters)
        if no_arb(list_bookmakers_final, arb_parameters, odds_range):
            break
    return [list_probabilities, outcome, list_bookmakers_final]


n_events = 300000 #number of data points
n_bookmakers = 7 #can be randomised within the for loop
p1_parameters = [1000, 1.317, -88, 88.41] #p1 is burr distributed. p2/(1-p1) is burr distributed, p3 = 1 - p1 - p2
p2_parameters = [1000, 0.65, -50, 50.5445] #p1 is burr distributed. p2/(1-p1) is burr distributed, p3 = 1 - p1 - p2
noise_sd = 0.0105 #noise is indeed from a normal distribution, the standard deviaiton of the noise term. 68% of noise terms will be within +- noise_sd
margin_parameters = [0.0921, 0.0324] #bookmaker margin is normally distributed, with this mu and sigma.
margin_i_parameters = [4.17, -0.182, 4.73] #for a given outcome i, the margin allocated to that outcome given its probability is alpha distributed
arb_parameters = [1000, 4.7, -20.365, 20.36] #for arb, draw from arb cumulative distribution, p(X < arb). then draw a value from uniform distribution 0 1. if p(X < arb) < this U, accept bet
odds_range = [1.05, 100]

with open(os.path.realpath(rf'test_gang.txt'), 'a') as f:
    for i in range(n_events):
        print(i)
        #n_bookmakers = random.randint(5,10) #if you want random n bookmakers per event
        list_probabilities, outcome, list_bookmakers_final = one_good_event(n_bookmakers, p1_parameters, p2_parameters, noise_sd, margin_parameters, margin_i_parameters, arb_parameters, odds_range)
        list_lists_outcome_j_odds = []
        for j in range(3):
            list_lists_outcome_j_odds.append([])
            for bookmaker_list in list_bookmakers_final:
                list_lists_outcome_j_odds[-1].append(1 / bookmaker_list[j])
        bo_txt = f'{list_probabilities}; {outcome}'
        for i in list_lists_outcome_j_odds:
            bo_txt += f'; {i}'
        f.write(f'\n{bo_txt}')

import csv
import time
import tracemalloc
from math import *

class Action:
    def __init__(self, name, cost, growth_rate):
        self.name = name
        self.cost = float(cost) * 100
        self.growth_rate = float(growth_rate[:-1]) / 100
        self.benef = self.cost * self.growth_rate

actions = []
money = 50000

with open("data2.csv") as file:
    reader = csv.reader(file, delimiter=",")
    i = 0

    for row in reader:
        if i == 0:
            i += 1
            continue

        values = []
        for col in row:
            values.append(col)
        if float(values[1]) > 0:
            actions.append(Action(values[0], values[1], values[2]))

def main(money, actions):
    tracemalloc.start()
    t = time.time()

    matrice = [
            [[[], 0] for x in range(money + 1)] for elem in range(len(actions) + 1)
        ]

    for index in range(1, len(actions) + 1):
        for unit in range(1, money + 1):


            action = actions[index - 1]
            
            if action.cost <= unit:

                completer_value = max(0, unit - ceil(action.cost))
                completer = matrice[index - 1][completer_value]

                new_value = max(action.benef, action.benef + completer[1])

                if (new_value >= matrice[index - 1][unit][1]):
                    matrice[index][unit][0] = completer[0].copy()
                    matrice[index][unit][0].append(action)
                    matrice[index][unit][1] = new_value

                else:
                    matrice[index][unit] = matrice[index - 1][unit]

            else:
                matrice[index][unit] = matrice[index - 1][unit]

            
    result = matrice[-1][-1]
    tableau = result[0]
    somme = result[1]
    fin = time.time() - t
    current, peak = tracemalloc.get_traced_memory()
    
    print("Total investi : " + str(sum(action.cost for action in tableau)))
    print("Retour sur investissement : " + str(somme))
    print("\nActions & Retour :\n")
    for action in tableau:
        print(action.name + " : " + str(action.benef)[:5] + "€")

    print("\nMémoire occupée : " + str(current / 125000) + " Mo")
    print("Highest : " + str(peak / 125000) + " Mo")
    print("\nNombre d'actions analysées : %s" % len(actions))
    print("Calculé en " + str(fin)[:4] + "s")


main(money, actions)
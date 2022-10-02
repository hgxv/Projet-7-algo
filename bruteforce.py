import csv
import time
import sys
import tracemalloc


class Action:
    def __init__(self, name, cost, growth_rate):
        self.name = name
        self.cost = float(cost)
        self.growth_rate = float(growth_rate[:-1]) / 100
        self.benef = self.cost * self.growth_rate


actions = []
money = 500
nb = 0

with open("data.csv") as file:
    reader = csv.reader(file, delimiter=",")
    i = 0

    for row in reader:
        if i == 0:
            i += 1
            continue

        values = []
        for col in row:
            values.append(col)
        actions.append(Action(values[0], values[1], values[2]))


def calcul(money, actions, current = []):
    global nb

    if actions:

        somme_current, remaining = calcul(money, actions[1:], current)
        action = actions[0]

        if action.cost <= money:
            val2, elements2 = calcul(money - action.cost, actions[1:], current + [action])

            if val2 > somme_current:
                return val2, elements2

        return somme_current, remaining

    else:
        nb += 1
        #print([sum(action.benef for action in current), [action.name for action in current]])
        return sum(action.benef for action in current), current


def main():
    t = time.time()

    tracemalloc.start()
    somme, tableau = calcul(money, actions)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("Total investi : " + str(sum(action.cost for action in tableau)))
    print("Retour sur investissement : " + str(somme))
    print("\nActions achetées :\n")
    for action in tableau:
        print(action.name + " : " + str(action.benef)[:4] + "€")
    result = time.time() - t
    print("\nCalculé en " + str(result)[:4] + "s")
    print("\nMémoire occupée : " + str(current / 125000) + " Mo")
    print("Highest : " + str(peak / 125000) + " Mo")
    print("\nNombre d'appels : " + str(nb))

main()

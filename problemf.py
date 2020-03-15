#!/usr/bin/env python3
# Made by barre kevin
# https://www.linkedin.com/in/kevin-barre-neudinger/
# kevin.barre@epitech.eu
# https://kevinb.alwaysdata.net/
import sys
# i used these links to solve the problem.
# https://fr.wikipedia.org/wiki/Programmation_dynamique
# https://fr.wikipedia.org/wiki/M%C3%A9mo%C3%AFsation
# https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_la_complexit%C3%A9_(informatique_th%C3%A9orique)
# https://fr.wikipedia.org/wiki/Probl%C3%A8me_de_l%27arbre_de_Steiners
# https://fr.wikipedia.org/wiki/21_probl%C3%A8mes_NP-complets_de_Karp


def read_file(filename) -> list:
    with open(filename, 'r') as f:
        cases = list()
        company_info = f.readline().strip().split(' ')
        while company_info != ['0']*3:
            # initialize a case
            transaction_days, wallet, trade_days = tuple(
                map(lambda x: int(x), company_info))
            transactions = list()
            # add list of machine info
            for i in range(transaction_days):
                transactions.append(
                    tuple(map(lambda x: int(x), f.readline().strip().split(' '))))
            # after all machines read, add this to the case
            cases.append([trade_days,
                          (wallet, 0, 0), transactions])
            company_info = f.readline().strip().split(' ')
    return cases


def compute(nodes: list, days: int = 1):
    # nodes
    # current_money, resale_value,
    for index, node in enumerate(nodes):
        nodes[index] = (node[0] + node[2]*days, node[1], node[2])


def apply_transaction(transaction: tuple = (), branches: list = []) -> list:
    next_branch = list()
    for branche in branches:
        transaction_day, price, resale_value, computeprofit = transaction
        # Buy if possible
        buy_branche = (branche[0]+branche[1]-price, resale_value, computeprofit) if branche[0] + \
            branche[1] >= price else None
        if buy_branche:
            next_branch.append(buy_branche)

        # Stay Branche
        next_branch.append((branche[0]+branche[2], branche[1], branche[2]))
    return next_branch


def bestroad(transactions: list = []) -> int:
    trade_days = transactions.pop(0)
    branches = [transactions.pop(0)]
    last_day = 1
    # last_transaction = None
    for idx, transaction in enumerate(sorted(transactions.pop(0)), 1):
        compute(branches, transaction[0] - last_day-1)
        branches = apply_transaction(transaction, branches)
        last_day = transaction[0]

    compute(branches, trade_days - last_day)
    # sort by money and sell everythings
    return list(sorted(map(lambda x: (x[0] + x[1]), branches)))[-1]


if __name__ == '__main__':
    transactions = read_file(sys.argv[1])
    for count, transaction in enumerate(transactions, 1):
        print(f'Case {count}: {bestroad(transaction)}')

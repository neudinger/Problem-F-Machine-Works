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


def read_file(filename)->list:
    with open(filename, 'r') as f:
        cases = list()
        company_info = f.readline().strip().split(' ')
        while company_info != ['0']*3:
            # initialize a case
            transaction_days ,wallet, trade_days = tuple(map(lambda x: int(x), company_info))
            transactions = list()
            # add list of machine info
            for i in range(transaction_days):
                transactions.append(tuple(map(lambda x: int(x), f.readline().strip().split(' '))))
            # after all machines read, add this to the case
            cases.append([trade_days, (wallet, 0, 0), transactions])
            company_info = f.readline().strip().split(' ')
    return cases

def compute(nodes:list, days:int=1):
    # nodes
    # current_money, resale_value,
    for index, node in enumerate(nodes):
        nodes[index] = (node[0] + node[2]*days, node[1], node[2])

def choose_buy(node:tuple, transaction:tuple):
    # nodes
    # current_money, resale_value, computeprofit
    # if you have enough money buy
    transaction_day, price, resale_value, computeprofit = transaction
    if node[0]+node[1] >= price:
        return (node[0]+node[1]-price, resale_value, computeprofit)
    # Else compute to get money
    return (node[0]+node[2], node[1], node[2])

def apply_transaction(transaction:tuple=(), branches:list=[])->list:
    next_branch = list()
    for branche in branches:
        buy = choose_buy(node=branche, transaction=transaction)
        # buy and compute
        if buy:
            next_branch.append(buy)
        # and stay
        next_branch.append(branche)
    return next_branch

def bestroad(transactions:list=[])->int:
    trade_days = transactions.pop(0)
    branches = [transactions.pop(0)]
    last_day = 0
    for idx, transaction in enumerate(sorted(transactions.pop(0))):
        # transaction_day, price, resale_value, computeprofit
        
        # If you buy a machine M i on day D i , then ACM can operate it starting on day D i + 1. Each day that the machine
        # operates, it produces a profit of G i dollars for the company.
        # Jump the first day
        if transaction[0] - last_day > 1 and idx:
            # You cannot operate a machine on the day that you sell
            # it, but you may sell a machine and use the proceeds to buy a new machine on the same day.
            compute(branches, transaction[0]-last_day-1)
        branches = apply_transaction(transaction, branches)
        last_day = transaction[0]
    # compute until the end
    compute(branches, trade_days - last_day)
    # sort by money and sell everythings
    return list(sorted(map(lambda x: (x[0] + x[1]), branches)))[-1]

if __name__ == '__main__':
    transactions = read_file(sys.argv[1])
    for count, transaction in enumerate(transactions, 1):
        print(f'Case {count}: {bestroad(transaction)}')
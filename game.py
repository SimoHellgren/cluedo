from typing import Set
from itertools import groupby
from functools import partial
from models import Player, Suspect, Weapon, Room, FactType, Fact, add_fact


# utilities
def sure_has(facts: Set[Fact]):
    '''this and related functions are not really good yet.'''
    return filter(lambda x: (len(x.cards) == 1) and (x.facttype == FactType.HAS), facts)

def sure_lacks(facts: Set[Fact]):
    return filter(lambda x: x.facttype == FactType.LACKS, facts)

def maybes(facts: Set[Fact]):
    return filter(lambda x: (len(x.cards) > 1) and (x.facttype == FactType.HAS), facts)

sorted_groupby = lambda func, it: groupby(sorted(it, key=func), func)

group_by_player = partial(sorted_groupby, lambda x: x.player)

def get_input(collection):
    for i, elem in enumerate(collection):
        print(i, '-', elem.name)

    return input(f'Pick a {elem.__class__.__name__}: ')


def print_grouped(facts: Set[Fact], grouper, msg=''):
    for group, facts in grouper(facts):
        print(group.name, msg)
        for fact in facts:
            for card in fact.cards:
                print('-', card.name)

    print()

# game setup
suspects = list(map(Suspect, (
    'Miss Scarlett', 'Rev. Green', 'Colonel Mustard',
    'Professor Plum', 'Mrs. Peacock', 'Mrs. White'
)))

weapons = list(map(Weapon, (
    'Candlestick', 'Dagger', 'Lead Pipe',
    'Revolver', 'Rope', 'Wrench'

)))

rooms = list(map(Room, (
    'Kitchen', 'Ballroom', 'Conservatory',
    'Dining Room', 'Billiard Room', 'Library',
    'Lounge', 'Hall', 'Study'
)))


all_cards = set((*suspects, *weapons, *rooms))

players = list(map(Player, ('You', 'Player 2', 'Player 3')))

def initialize():
    print('Initialize you cards')

    for i, card in enumerate(all_cards):
        print(i, '-', card.name)

    choices = input('Pick your cards (comma-separated ints): ')
    your_cards = [list(all_cards)[i] for i in map(int, choices.split(','))]

    print('You got:')
    print('\n'.join(card.name for card in your_cards))

    facts = {Fact(players[0], {c}) for c in your_cards}

    return facts

def loop(facts):
    while True:
        print('_'*20)

        print('Record a fact')
        
        p = get_input(players)

        s = get_input(suspects)

        w = get_input(weapons)

        r = get_input(rooms)

        ft = input('Did player show a card? 1/0: ')

        player = players[int(p)]
        suspect = suspects[int(s)]
        weapon = weapons[int(w)]
        room = rooms[int(r)]
        facttype = FactType.HAS if int(ft) else  FactType.LACKS

        facts = add_fact(Fact(player, {suspect, weapon, room}, facttype), facts)


        print('You now know this:')

        print_grouped(sure_has(facts), group_by_player, 'has:')
        print_grouped(sure_lacks(facts), group_by_player, 'does not have:')
        print_grouped(maybes(facts), group_by_player, 'playsibly possesses:')
    
if __name__ == '__main__':
    facts=initialize()
    loop(facts)
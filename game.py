from typing import Set, Iterator, Tuple
from itertools import groupby, chain
from functools import partial
from models import Card, Player, Suspect, Weapon, Room, FactType, Fact, add_fact


# utilities
def sure_has(facts: Set[Fact]):
    '''this and related functions are not really good yet.'''
    return filter(lambda x: (len(x.cards) == 1) and (x.facttype == FactType.HAS), facts)

def sure_lacks(facts: Set[Fact]):
    return filter(lambda x: x.facttype == FactType.LACKS, facts)

def maybes(facts: Set[Fact]):
    return filter(lambda x: (len(x.cards) > 1) and (x.facttype == FactType.HAS), facts)

def explode(fact: Fact) -> Iterator[Tuple[Player, Card, FactType]]:
    '''Explode the cards of a fact. Not that care must be taken in interpreting FactType.HAS'''
    p, cs, ft = fact
    for c in cs:
        yield p,c,ft

sorted_groupby = lambda func, it: groupby(sorted(it, key=func), func)

group_by_player = partial(sorted_groupby, lambda x: x.player)


def print_knowledge(facts):
    owned = set(chain.from_iterable(map(explode, sure_has(facts))))
    not_owned = set(chain.from_iterable(map(explode, sure_lacks(facts))))
    maybe_owned = set(chain.from_iterable(map(explode, maybes(facts))))

    print('Owned for sure:')
    for player, data in sorted_groupby(lambda x: x[0], owned):
        print('-', player.name)
        print('\n'.join(' - ' + c.name for _,c,_ in data))

    print('Not owned:')
    for player, data in sorted_groupby(lambda x: x[0], not_owned):
        print('-', player.name)
        print('\n'.join(' - ' + c.name for _,c,_ in data))

    # cards that someone owns aren't maybes
    m1 = {c for c in maybe_owned if c[2] in {t[2] for t in owned}}

    # cards that are not owned by someone, are not maybes
    m2 = {c for c in m1 if c[:2] not in {t[:2] for t in not_owned}}

    print('Perhaps owned:')
    for player, data in sorted_groupby(lambda x: x[0], m2):
        print('-', player.name)
        print('\n'.join(' - ' + c.name for _,c,_ in data))


def get_input(collection):
    for i, elem in enumerate(collection):
        print(i, '-', elem.name)

    return input(f'Pick a {elem.__class__.__name__}: ')


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


all_cards = [*suspects, *weapons, *rooms]

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


def see_card():
    p = get_input(players)


    for i, elem in enumerate(all_cards):
        print(i, '-', elem.name)

    c = input('Pick a Card (any card!): ')
    
    player = players[int(p)]
    card = all_cards[int(c)]

    return Fact(player, {card}, FactType.HAS)

def observe():
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

        return Fact(player, {suspect, weapon, room}, facttype)

def play(facts):
    while True:
        print('_'*20)

        print('Record a fact')
        print('0 - observe')
        print('1 - see a card')
        c = input('0/1: ')

        if c == '0':
            func = observe

        elif c == '1':
            func = see_card
        
        facts = add_fact(func(), facts)

        print('You now know this:')
        print_knowledge(facts)

        return facts
    
if __name__ == '__main__':
    facts=initialize()
    while True:
        facts = play(facts)
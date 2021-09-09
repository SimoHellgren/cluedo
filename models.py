'''Basic models and logic for deductions.'''

from typing import Deque, Set, List, Optional
from collections import deque, namedtuple
from dataclasses import dataclass
from enum import Enum


Player = namedtuple('Player', 'name')

Card = namedtuple('Card', 'name')

Suspect = type('Suspect', (Card,), {})
Weapon = type('Weapon', (Card,), {})
Room = type('Room', (Card,), {})


class FactType(Enum):
    '''Describes the semantics of a fact.
        FactType.HAS   = `player` has one of `cards`
        FactType.LACKS = `player` has none of `cards`
    '''
    HAS = 1
    LACKS = 2


@dataclass
class Fact:
    player: Player
    cards: Set[Card]
    facttype: FactType = FactType.HAS

    def __iter__(self):
        '''Enables most importantly the fancy-pants unpacking in `deduce` '''
        return iter((self.player, self.cards, self.facttype))

    def __hash__(self):
        '''If rules are followed, there is no need to include self.facttype
        '''
        return hash(tuple([self.player, *sorted(self.cards)]))



def deduce(f1: Fact, f2: Fact) -> Optional[Fact]:
    '''Deduce new facts from old facts, if possible'''
    p1, c1, t1 = f1
    p2, c2, t2 = f2

    # If same player, only differently typed facts yield deduction.
    # I.e. there's no point in comparing things we already know
    # a player (might) have, or that they don't have.
    if p1 == p2:
        if t1 != t2:
            # we can remove the lacking card from everything else
            if t1 == FactType.LACKS:
                return Fact(p1, c2-c1)
            else:
                return Fact(p1, c1-c2)            
        return

    # If different players, we must know for sure that one of them has a card,
    # i.e. either c1 or c2 must have length 1. If both have length 1, they are
    # different cards, because the players are different. Thus exactly one may
    # have length 1. (The latter could be left unchecked here because of the
    # intersection check that comes next.
    if not (len(c1) == 1) ^ (len(c2) == 1):
        return

    # If intersection is empty, nothing to do
    inter = c1 & c2
    if not inter:
        return

    # The single-card fact is certain, so we remove it from the other fact
    if c1 > c2:
        return Fact(p1, c1-c2)
    else:
        return Fact(p2, c2-c1)


def add_fact(fact: Fact, facts: List[Fact]):
    '''Adds a fact to a processing queue, and tries to generate new facts.
        If new facts are deduced, they are added to the processing queue.
    '''
    process_queue = deque([fact])

    result = {fact}
    while process_queue:
        process_fact = process_queue.pop()

        for old_fact in facts:
            new_fact = deduce(process_fact, old_fact)
    
            if new_fact:
                process_queue.append(new_fact)
                result.add(new_fact)

    return facts | result

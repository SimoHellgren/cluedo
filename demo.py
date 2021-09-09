'''A concise demo to check that the deduction logic actually does something.
    Turn order and other stuff do not adhere to actual gameplay.
'''

from models import Player, Suspect, Weapon, Room, FactType, Fact, add_fact


suspects = list(map(Suspect, ('Mr. Blue', 'Lady in Red', 'Black Dog')))
weapons = list(map(Weapon, ('Knife', 'Gun')))
rooms = list(map(Room, ('Bedroom', 'Kitchen', 'Balcony')))


p1, p2, p3 = map(Player, ('You', 'Player 2', 'Player 3'))

# initialize facts (your cards)
facts = f0 = {
    Fact(p1, {suspects[0]}), # Mr. Blue
    Fact(p1, {weapons[0]}),  # Knife
    Fact(p1, {rooms[0]})     # Bedroom
}

# player 2 shows a card
f1 = Fact(p2, {
    suspects[1], # Lady in Red
    weapons[0],  # Knife
    rooms[1]     # Kitchen
})

# player 3 shows a card
f2 = Fact(p3, {
    suspects[2], # Black Dog
    weapons[1],  # Gun
    rooms[1]     # Kitchen
})

# player 3 doesn't show a card
f3 = Fact(p3, {
    suspects[2], # Black Dog 
    weapons[1],  # Gun
    rooms[2]     # Balcony
}, FactType.LACKS)


# 1. combining f3 and f2 you see that p3 must have Kitchen
# 2. knowing 1, and that you have Knife, you now know p2 has Lady in Red

original_facts=set([*f0, f1, f2, f3])

for f in (f1, f2, f3):
    facts = add_fact(f, facts)


if (original_facts - facts):
    print('Something went wrong')

print('Deduced facts:')
for f in (facts - original_facts):
    print(f)
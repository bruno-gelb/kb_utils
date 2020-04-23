class Unit(object):
    def __init__(self, name, attack, defend):
        self.name = name
        self.attack = attack
        self.defend = defend

    def __repr__(self):
        return self.name


units = {
    'droid': Unit('droid', 42, 41),
    'gorgul': Unit('gorgul', 24, 20)
}

class component_direction:
    def __init__(self, direction=0, inclination=0):
        component_direction.azimut_def = {'n': 0, 'nne': 22.5, 'ne': 45, 'nee': 67.5, 'e': 90, 'ese': 112.5, 'se': 135,
                                          'sse': 157.5,
                                          's': 180, 'ssw': 202.5, 'sw': 225, 'wsw': 247.5, 'w': 270, 'wnw': 292.5,
                                          'nw': 315, 'nwn': 337.5,
                                          'north': 0, 'east': 90, 'south': 180, 'west': 270}
        inclination_def = {'u': 90, 'up': 90, 'd': -90, 'down': -90}
        component_direction.insolation_def = {'n': 100, 'nne': 113.75, 'ne': 127.5, 'nee': 141.25, 'e': 155,
                                              'ese': 183.75, 'se': 212.5, 'sse': 241.75,
                                              's': 270, 'ssw': 241.75, 'sw': 212.5, 'wsw': 183.75, 'w': 155,
                                              'wnw': 141.25, 'nw': 127.5, 'nwn': 113.75, 'north': 100, 'east': 155,
                                              'south': 270, 'west': 155, 'up': 255, 'down': 0}
        self.inclination = inclination
        self.azimut = 0
        if type(direction) == type(''):
            if direction.lower() in inclination_def.keys():
                self.inclination = component_direction.inclination_def[direction.lower()]
            elif direction.lower() in component_direction.azimut_def.keys():
                self.azimut = component_direction.azimut_def[direction.lower()]
        else:
            self.azimut = direction

    def direction(self, cardinal=False):
        if not cardinal:
            if self.inclination >= 30:
                return 'up'
            elif self.inclination <= -30:
                return 'down'
        for name, azim in component_direction.azimut_def.items():
            if azim == divmod(self.azimut, 22.5)[0] * 22.5:
                return name
        return None

    def type(self):
        if self.inclination >= 30:
            return 'ceiling'
        elif self.inclination <= -30:
            return 'floor'
        else:
            return 'wall'

    def rsi(self):
        if self.direction() is 'up': return 0.10
        if self.direction() is 'down':
            return 0.17
        else:
            return 0.13

    def rse(self):
        if self.direction() is 'up': return 0.04
        if self.direction() is 'down':
            return 0.04
        else:
            return 0.04

    def insolation(self):
        insol = component_direction.insolation_def[self.direction(True)]
        if self.inclination >= 0:
            insol += float(self.inclination) / 90 * (component_direction.insolation_def['up'] - insol)
        else:
            insol -= float(self.inclination) / 90 * (component_direction.insolation_def['down'] - insol)
        return round(insol, 0)

'''
for i in [0, 90, 180, 270]:
    k = component_direction('s', -10)
    print '--------'
    print k.inclination
    print k.azimut
    print k.direction()
    print k.type()
    print k.rsi()
    print k.rse()
    print k.insolation()
'''

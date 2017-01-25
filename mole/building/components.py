from mole.oeq_global import *


class layer:
    'Building Component Layer'

    def __init__(self, material=None, width=None, spec_conductivity=None):
        self.material = material
        self.width = width
        self.spec_conductivity = spec_conductivity

    def resistance(self):
        if (self.width is None) | (self.conductivity() is None):
            return None
        return self.width / float(self.spec_conductivity)

    def conductivity(self):
        if (self.width is None) | (self.spec_conductivity is None):
            return None
        return float(self.spec_conductivity) / self.width

    def info(self, indent=0):
        indentstr = '    ' * indent
        rep = indentstr + 'Open eQuarter Object Report\n'
        rep += indentstr + '---------------------------\n'
        rep += indentstr + 'Class                 : ' + layer.__name__ + '\n'
        rep += indentstr + 'Descrription          : ' + layer.__doc__ + '\n'
        rep += indentstr + 'Attributes            : ' + '\n'
        rep += indentstr + '    material          : ' + str(self.material) + '\n'
        rep += indentstr + '    width             : ' + str(self.width) + u' m\n'
        rep += indentstr + '    spec_conductivity : ' + str(self.spec_conductivity) + u' W/(m K)\n'
        rep += indentstr + 'Method Results : ' + '\n'
        rep += indentstr + '    resistance()      : ' + str(self.resistance()) + ' K/W\n'
        rep += indentstr + '    conductivity()    : ' + str(self.conductivity()) + 'W/K\n'
        return rep


class bias:
    '3D alignment of a building component'

    def __init__(self, direction=0, inclination=0):
        bias.azimut_def = {'n': 0, 'nne': 22.5, 'ne': 45, 'nee': 67.5, 'e': 90, 'ese': 112.5, 'se': 135, 'sse': 157.5,
                           's': 180, 'ssw': 202.5, 'sw': 225, 'wsw': 247.5, 'w': 270, 'wnw': 292.5, 'nw': 315,
                           'nwn': 337.5,
                           'north': 0, 'east': 90, 'south': 180, 'west': 270}
        inclination_def = {'u': 90, 'up': 90, 'd': -90, 'down': -90}
        bias.insolation_def = {'n': 100, 'nne': 113.75, 'ne': 127.5, 'nee': 141.25, 'e': 155, 'ese': 183.75,
                               'se': 212.5, 'sse': 241.75,
                               's': 270, 'ssw': 241.75, 'sw': 212.5, 'wsw': 183.75, 'w': 155, 'wnw': 141.25,
                               'nw': 127.5, 'nwn': 113.75, 'north': 100, 'east': 155, 'south': 270, 'west': 155,
                               'up': 255, 'down': 0}
        self.inclination = inclination
        self.azimut = 0
        if type(direction) == type(''):
            if direction.lower() in inclination_def.keys():
                self.inclination = bias.inclination_def[direction.lower()]
            elif direction.lower() in bias.azimut_def.keys():
                self.azimut = bias.azimut_def[direction.lower()]
        else:
            self.azimut = direction

    def direction(self, cardinal=False):
        if not cardinal:
            if self.inclination >= 30:
                return 'up'
            elif self.inclination <= -30:
                return 'down'
        for name, azim in bias.azimut_def.items():
            if azim == divmod(self.azimut, 22.5)[0] * 22.5:
                return name
        return None

    def type(self):
        if self.inclination > 30:
            return 'ceiling'
        elif self.inclination < -30:
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
        insol = bias.insolation_def[self.direction(True)]
        if self.inclination >= 0:
            insol += float(self.inclination) / 90 * (bias.insolation_def['up'] - insol)
        else:
            insol -= float(self.inclination) / 90 * (bias.insolation_def['down'] - insol)
        return round(insol, 0)

    def info(self, indent=0):
        indentstr = '    ' * indent
        rep = indentstr + 'Open eQuarter Object Report\n'
        rep += indentstr + '---------------------------\n'
        rep += indentstr + 'Class          : ' + bias.__name__ + '\n'
        rep += indentstr + 'Descrription   : ' + bias.__doc__ + '\n'
        rep += indentstr + 'Attributes     : ' + '\n'
        rep += indentstr + '    inclination : ' + str(self.inclination) + u'\xb0\n'
        rep += indentstr + '    azimut      : ' + str(self.azimut) + u'\xb0\n'
        rep += indentstr + 'Method Results : ' + '\n'
        rep += indentstr + '    direction() : ' + self.direction() + '\n'
        rep += indentstr + '    type()      : ' + self.type() + '\n'
        rep += indentstr + '    Rsi()       : ' + str(self.rsi()) + ' (m2K)/W\n'
        rep += indentstr + '    Rse()       : ' + str(self.rse()) + ' (m2K)/W\n'
        rep += indentstr + '    insolation(): ' + str(self.insolation()) + ' kWh/(m2a)\n'
        return rep


# for i in [0,15,90,135,160,180,270]:
#    k=bias(i,-20)
#    print k.info()

class component:
    'Building Component'

    def __init__(self, name=None, area=1, uvalue=1, width=0.3, layers=[], direction='s', inclination=0, against='air',
                 opaque=True):
        self.name = name
        self.bias = bias(direction, inclination)
        self.area = area
        self.given_width = width
        self.given_uvalue = uvalue
        self.layers = layers
        self.against = against
        self.opaque = opaque

    def add_layers(self, layers):
        self.layers.append(layers)

    def resistance(self):
        print self.layers
        print type(self.layers)
        if len(self.layers) is 0:
            if self.given_uvalue is None:
                return None
            if self.against is 'soil':
                return 1 / self.given_uvalue - self.bias.rsi()
            return 1 / self.given_uvalue - self.bias.rsi() - self.bias.rse()
        resist = 0
        for layer in self.layers:
            resist += layer.resistance()
        return resist

    def conductivity(self):
        if self.resistance() is None: return None
        return 1 / float(self.resistance())

    def uvalue(self):
        if self.resistance() is None:
            return None
        if self.against is 'soil':
            return 1 / float(self.bias.rsi() + self.resistance())
        return 1 / float(self.bias.rsi() + self.bias.rse() + self.resistance())

    def width(self):
        if len(self.layers) is 0:
            if self.width is None: return None
            return self.given_width
        wdth = 0
        for layer in self.layers:
            wdth += layer.width
        return wdth

    def solar_gain(self):
        g = 1
        return self.bias.insolation() * 0, 567 * g * self.area

    def type(self):
        if self.bias.type() is 'ceiling':
            if self.against is 'air':
                return 'roof'
            else:
                return 'ceiling'
        elif self.bias.type() is 'floor':
            if self.against is 'soil':
                return 'baseplate'
            else:
                return 'floor'
        else:
            return 'wall'

    def info(self, indent=0):
        indentstr = '    ' * indent
        rep = indentstr + 'Open eQuarter Object Report\n'
        rep += indentstr + '---------------------------\n'
        rep += indentstr + 'Class          : ' + component.__name__ + '\n'
        rep += indentstr + 'Descrription   : ' + component.__doc__ + '\n'
        rep += indentstr + 'Attributes     : ' + '\n'
        rep += indentstr + '    bias           : ' + '\n'
        rep += self.bias.info(indent + 2)
        rep += indentstr + '    area           : ' + str(self.area) + ' m2\n'
        rep += indentstr + '    given_width    : ' + str(self.given_width) + ' m\n'
        rep += indentstr + '    given_uvalue   : ' + str(self.given_uvalue) + ' W/(m2K)\n'
        for i in self.__dict__.keys():
            if i == 'layers':
                rep += indentstr + '    layers         : ' + '\n'
                for j in self.__dict__[i]:
                    rep += j.info(indent + 2) + '\n'
            else:
                rep += indentstr + '    ' + i + ' : ' + str(self.__dict__[i]) + '\n'
        rep += indentstr + '    against        : ' + self.against + '\n'
        rep += indentstr + '    opaque         : ' + str(self.opaque) + '\n'
        rep += indentstr + 'Method Results : ' + '\n'
        rep += indentstr + '    type()         : ' + self.type() + '\n'
        rep += indentstr + '    width()        : ' + str(self.width()) + ' m\n'
        rep += indentstr + '    uvalue()       : ' + str(self.uvalue()) + ' W/(m2K)\n'
        rep += indentstr + '    conductivity() : ' + str(self.conductivity()) + ' W/K\n'
        rep += indentstr + '    resistance()   : ' + str(self.resistance()) + ' K/W\n'

        return rep


class building:
    'Building'

    def __init__(self, quarter=None, BLD_ID=None, name=None, area=None, height=None, year_of_construction=None,
                 uvalue_roof=None, uvalue_wall=None, uvalue_base=None, uvalue_window=None, components=[]):
        if quarter is None:
            self.quarter = quarter()
        else:
            self.quarter = quarter
        self.name = name
        self.BLD_ID = BLD_ID
        self.aquired_area = area
        self.aquired_height = height
        self.aquired_year_of_construction = year_of_construction
        self.aquired_uvalue_roof = uvalue_roof
        self.aquired_uvalue_wall = uvalue_wall
        self.aquired_uvalue_base = uvalue_base
        self.aquired_uvalue_window = uvalue_window
        self.aquired_
        self.components = components

        component.__init__(name, default_width, default_uvalue, layers, flow_direction, against_air)
        component.default_width = default_width
        component.default_uvalue = default_uvalue
        self.window_ratio = window_ratio
        self.attached_ratio = attached_ratio


# def __init__(layers
# class wall:
#    def __init__(gross_area=None,
#           net_area=None,
#           windows=None,
#           against_air=None,
#           against_soil=None,
#           aattached=None)
#    gross
# window
# against air
# against soil
# against_structures

# name=None,area=1,uvalue=1,width=0.3,layers=[],direction='s',inclination=0,against='air',opaque=True):

class quarter:
    def __init__(self, name=OeQ_project_info['project_name'], description=OeQ_project_info['description'],
                 center_coordinates=None, crs=config.project_crs.split(':')[2],
                 population_density=OeQ_project_info['population_density'],
                 year_of_construction=OeQ_project_info['average_construction_year'],
                 heating_degree_days=OeQ_project_info['heating_degree_days']):
        print name
        self.name = name
        self.description = description
        self.center_coordinates = center_coordinates
        self.crs = crs
        self.population_density = population_density
        self.year_of_construction = year_of_construction
        self.heating_degree_days = heating_degree_days


def components():
    l = quarter()
    print l
    # print  l.name
    print  l.description
    print  l.center_coordinates
    print  l.crs
    print  l.population_density
    print  l.year_of_construction
    print  l.population_density
    print  l.heating_degree_days

    k = component(name="Tolle Wand", area=10,
                  layers=[layer("Beton", 0.25, 2), layer('MinWool', 0.3, 0.032), layer('Hagatherm', 0.02, 0.056)],
                  direction='west')
    n = component(name="Tolle Wand", area=10,
                  layers=[layer("Beton", 0.25, 2), layer('MinWool', 0.3, 0.032), layer('Hagatherm', 0.02, 0.056)],
                  direction=22, inclination=30)

    print "Rsi: " + str(k.bias.rsi())
    print "Rse: " + str(k.bias.rse())
    print "Conductivity: " + str(k.conductivity())
    for i in k.layers:
        print i.material
        print i.resistance()
    print "Resistance: " + str(k.resistance())
    print "U-Value: " + str(k.uvalue())
    print "Width: " + str(k.width())
    print k.info(1)
    k.add_layers(layer("Air", 0.10, 0.556))

    print "\nConductivity: " + str(k.conductivity())
    for i in k.layers:
        print i.material
        print i.resistance()
        print str(i.info(3))
    print "Resistance: " + str(k.resistance())
    print "U-Value: " + str(k.uvalue())
    print "Width: " + str(k.width())

    k = component("Auch tolle Wand", 0.47, 0.9, [], 'horizontal')

    print "Rsi: " + str(k.bias.rsi())
    print "Rse: " + str(k.bias.rse())
    print "Conductivity: " + str(k.conductivity())
    print "Resistance: " + str(k.resistance())
    print "U-Value: " + str(k.uvalue())
    print "Width: " + str(k.width())

    print k.__dict__

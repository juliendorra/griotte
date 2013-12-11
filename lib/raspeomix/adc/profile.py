from raspeomix.rpncalc import RPNCalc
from string import Template

import logging

class Profile:
    def __init__(self, name='Identity', description='', units='', formula='$x', valrange=[0, 1024], resolution='12bits', gain='1x'):
        self.name = name
        self.description = description
        self.units = units
        self.formula = formula
        self.range = valrange
        self.resolution = resolution
        self.gain = gain
        self.raw_value = self.converted_value = valrange[0]
        #self.value = valrange[0]

    @property
    def value(self):
        return self._raw_value

    @value.setter
    def value(self, val):
        self.raw_value = val
        formula = Template(self.formula).substitute(x=val)
        self.converted_value = RPNCalc().process(formula)
        logging.debug("Setting value to %s, converted_value to %s" %
                      (self.raw_value, self.converted_value))

    @property
    def value_pair(self):
        return [ self.raw_value,
                 self.converted_value ]



from decimal import *

class BadNominalException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 

class Money():
    """Klasa odpowiedzialna za poprawne funkcjonowanie pojedynczych pieniędzy"""
    def __init__(self, val):
        val = Decimal(float(val)).quantize(Decimal('.01'), rounding = ROUND_DOWN)
        allowed = list(map(Decimal, ['0.01', '0.02', '0.05',\
        '0.1', '0.2', '0.5', '1', '2', '5', '10', '20', '50']))
        if val in allowed:
            self._val = val
        else:
            raise BadNominalException(val)
        
    def get_val(self):
        return self._val

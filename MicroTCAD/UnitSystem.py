from dataclasses import dataclass

__all__ = ["Length", "Concentration", "Temperature", "Mobility", "Time"]


## CONVERTS ALL UNITS INTO SI UNITS FOR SIMPLICITY AND EASE OF USE 
## Allowing user to input whatever units they please (as long as they are here)

def _unit_check_helper(value, unit, unitList):
    if unit not in unitList:
        raise ValueError(f"'{unit}' is not a valid {unitList["Name"]} unit!")
    
    SI_Value = unitList[unit](value)
    return SI_Value


class Length(float):

    LENGTH_UNITS = {
        "Name": "Length",
        "m": lambda v: v,
        "cm": lambda v: v * 1e-2,
        "mm": lambda v: v * 1e-3,
        "um": lambda v: v * 1e-6,
        "nm": lambda v: v * 1e-9
    }

    def __new__(cls, Value: float, Unit: str):
        SI_Value = _unit_check_helper(Value, Unit, cls.LENGTH_UNITS)
        return super().__new__(cls, SI_Value)
        
        
class Concentration(float):

    CONCENTRATION_UNITS = {
        "Name": "Concentration",
        "m-3": lambda v: v,
        "cm-3": lambda v: v * 1e6
    }

    def __new__(cls, Value: float, Unit: str):
        SI_Value = _unit_check_helper(Value, Unit, cls.CONCENTRATION_UNITS)
        return super().__new__(cls, SI_Value)

class Temperature(float):

    TEMPERATURE_UNITS = {
        "Name": "Temperature",
        "K": lambda v: v,
        "C": lambda v: v + 273.15,
        "F": lambda v: (v - 32) * (5/9) + 273.15
    }

    def __new__(cls, Value: float, Unit: str):
        Unit = Unit.upper()
        SI_Value = _unit_check_helper(Value, Unit, cls.TEMPERATURE_UNITS)
        return super().__new__(cls, SI_Value)

class Mobility(float):

    MOBILITY_UNITS = {
        "Name": "Mobility",
        "m2/Vs": lambda v: v,
        "cm2/Vs": lambda v: v * 1e-4,
        "mm2/Vs": lambda v: v * 1e-6
    }

    def __new__(cls, Value: float, Unit: str):
        SI_Value = _unit_check_helper(Value, Unit, cls.MOBILITY_UNITS)
        return super().__new__(cls, SI_Value)

class Time(float):

    TIME_UNITS = {
        "Name": "Time",
        "s": lambda v: v,
        "ms": lambda v : v * 10e-3,
        "us": lambda v: v * 10-6,
        "ns": lambda v: v * 10-9
    }

    def __new__(cls, Value: float, Unit: str):
        SI_Value = _unit_check_helper(Value, Unit, cls.TIME_UNITS)
        return super().__new__(cls, SI_Value)

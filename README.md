# MicroTCAD
A semiconductor simulator built by me to simulate semiconductor devices under set conditions

MicroTCAD is a Python based semiconductor device simulator built to simulate semiconductor devices in various conditions prior to fabrication. This project was started as a way for me to learn more about semiconductor physics and the numerical methods used to simulate them as well as how a semiconductor’s fundamental properties affect its real-world functionality. How it works is down below

################################ INSTRUCTIONS ON HOW TO USE ##########################

The project currently contains 6 modules being:
Materials
MaterialAnalysis - MA
DevicePhysics
ComponentCreation - Create
UnitSystem - US
Main

The instructions on how to use the MA, Create and US modules are down below with the other modules containing the underlying functions that allow this. Further explanation of these modules can be seen in my MicroTCAD Documentation

################# Unit System ##################

When declaring variables UnitSystem classes should be used to ensure any units entered are properly converted to SI units to allow for ease of use in my formulas. For example

```python
from UnitSystem import *

# Converts 100 cm -> 1.0 m
l = Length(100, "cm")

# Converts 1e16 cm^-3 -> 1e22 m^-3
Na = Concentration(1e16, "cm-3")
```
the current UnitSystem classes are:
Length
Concentration
Temperature
Mobility
Time

##################### Component Creation ######################

ComponentCreation can currently only create a diode object with parameters the user inputs. These parameters include
Material
Device length
Na - acceptor ion concentration
Nd - donor ion concentration
Temperature
Area

Functions that can be called on this diode object are:
```python
import ComponentCreation as Create

diode1 = Create.Diode("MaterialName", "DeviceLength", "Na", "Nd", "Temp", "Area")
diode1.VoltageSweepAtEquilibrium()
diode1.ElectricFieldSweepAtEquilibrium()
diode1.IV_Sweep() # Which can take arguments Vmin and Vmax or have them set to be from 0 to 1
```

######################## MaterialAnalysis ##################
Material analysis currently contains 1 function that graphs the intrinsic carrier concentration vs temperature of the specified material.
It is called by typing
```python
import MaterialAnalysis as MA
MA.intrinsic_Carrier_Conc_Vs_Temp("MaterialName")
```
in main

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

The instructions on how to use the MA, Create and US modules are down below with the other modules containing the underlying functions that allow this. Further explanation of these modules can be seen in my write up

################# Unit System ##################

When declaring variables UnitSystem classes should be used to ensure any units entered are properly converted to SI units. For example

l = Length(100,"cm") returns l as 1m
and 
Na = Concentration(1e16,"cm-3") returns Na as 1e22 m-3

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

diode1.VoltageSweepAtEquilibrium()
diode1.ElectricFieldSweepAtEquilibrium()
and
diode1.IV_Sweep() which can take in inputs of the voltage range wanted to sweep

######################## MaterialAnalysis ##################
Material analysis currently contains 1 function that graphs the intrinsic carrier concentration vs temperature of the specified material.
It is called by typing
MA.intrinsic_Carrier_Conc_Vs_Temp("MaterialName")
in main

from UnitSystem import *
import ComponentCreation as Create
import MaterialAnalysis as MA
import DeviceAnalysis as DA


doping = Concentration(1e15,"cm-3")


diode1 = Create.Diode(Name= "Diode1", Material="Silicon", device_length=5e-6,Na=doping,Nd=doping,Area=1e-7)
diode2 = Create.Diode("random")

diode1.VoltageSweepAtEquilibrium(temperature=300)

diode1.IV_Sweep(temperature=300)

DA.CMP_VoltageSweepAtEquilibrium(diode1= diode1, diode2=diode2, temperature=300)


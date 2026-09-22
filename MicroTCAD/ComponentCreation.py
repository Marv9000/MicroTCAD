from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import DevicePhysics as DP


# Diode class
@dataclass
class Diode():
    Material : str
    device_length: float
    Na: float
    Nd: float
    Temp: float
    Area: float

    def VoltageSweepAtEquilibrium(self):

        # Voltage array mapping to points in the x grid
        x, V = DP._1D_Poisson_For_Diodes_Equilibrium(self.Material, self.Nd, self.Na, self.Temp, self.device_length)

        #Graph creation
        plt.figure()

        # Plot x in micro meters and Voltage as Volts
        plt.plot(x * 1e6, V)

        # Labels and Title
        plt.xlabel("Position, x (um)")
        plt.ylabel("Voltage, V (V)")
        plt.title("Voltage Across PN Junction")

        plt.savefig("voltage.png")
        plt.grid(True)
        plt.show()

    def ElectricFieldSweepAtEquilibrium(self):

        # Voltage array mapping to points in the x grid
        x, V = DP._1D_Poisson_For_Diodes_Equilibrium(self.Material, self.Nd, self.Na, self.Temp, self.device_length)

        # Differentiate voltage with respect to x for electric field
        E = -np.gradient(V,x)

        # Graph creation
        plt.figure()
        plt.plot(x * 1e6, E)

        # Labels and Title
        plt.xlabel("Position (um)")
        plt.ylabel("Electric Field (V/m)")
        plt.title("Equilibrium Electric Field")


        plt.grid(True)
        plt.savefig("electric_field.png")
        plt.show()

    def IV_Sweep(self, V_min=0, V_max=1):
        # Set step length
        step_Length = 0.01

        # Set V array from V_min to V_max in intervals of step_length
        V = np.arange(V_min, V_max + step_Length, step_Length)


        # Create current array for every point voltage in V array
        I = np.array([
            DP._shockley_diode_current(self.Material, self.Nd, self.Na, self.Temp, self.Area, v)
            for v in V
        ])

        # Graph Creation
        plt.figure()

        plt.plot(V, I)

        plt.ylim(0,50) 

        # Labels and Title
        plt.xlabel("Applied Voltage (V)")
        plt.ylabel("Current (A)") 
        plt.title("Diode I-V Characteristic")

        plt.grid(True)

        plt.savefig("iv_curve_linear.png")
        plt.show()
        





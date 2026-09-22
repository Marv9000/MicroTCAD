from ComponentCreation import *
import numpy as np

def CMP_VoltageSweepAtEquilibrium(diode1: Diode, diode2: Diode, temperature):
    x1, V1 = DP._1D_Poisson_For_Diodes_Equilibrium(diode1.Name, diode1.Material, diode1.Nd, diode1.Na, temperature, diode1.device_length)
    x2, V2 = DP._1D_Poisson_For_Diodes_Equilibrium(diode2.Name, diode2.Material, diode2.Nd, diode2.Na, temperature, diode2.device_length)

    #Graph creation
    plt.figure()

    # Plot x in micro meters and Voltage as Volts
    plt.plot(x1 * 1e6, V1, label=diode1.Name, color="blue")
    plt.plot(x2 * 1e6, V2, label=diode2.Name, color="red")

    # Labels and Title
    plt.xlabel("Position, x (um)")
    plt.ylabel("Voltage, V (V)")
    plt.title("Voltage Across PN Junction")
    plt.legend()

    plt.savefig("voltage.png")
    plt.grid(True)
    plt.show()

def CMP_ElectricFieldSweepAtEquilibrium(diode1: Diode, diode2: Diode, temperature):

    # Voltage array mapping to points in the x grid
    x1, V1 = DP._1D_Poisson_For_Diodes_Equilibrium(diode1.Name, diode1.Material, diode1.Nd, diode1.Na, temperature, diode1.device_length)
    x2, V2 = DP._1D_Poisson_For_Diodes_Equilibrium(diode2.Name, diode2.Material, diode2.Nd, diode2.Na, temperature, diode2.device_length)


    # Differentiate voltage with respect to x for electric field
    E1 = -np.gradient(V1,x1)
    E2 = -np.gradient(V2,x2)

    # Graph creation
    plt.figure()
    plt.plot(x1 * 1e6, E1, label=diode1.Name, color="red")
    plt.plot(x2 * 1e6, E2, label=diode2.Name, color="blue")


    # Labels and Title
    plt.xlabel("Position (um)")
    plt.ylabel("Electric Field (V/m)")
    plt.title("Equilibrium Electric Field")
    plt.legend()


    plt.grid(True)
    plt.savefig("electric_field.png")
    plt.show()
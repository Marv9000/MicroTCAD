from dataclasses import dataclass
import numpy as np
from UnitSystem import *

# Constant values not to be changed, - SI Units used
ELECTRON_MASS : float = 9.109e-31 # kg
ELECTRON_CHARGE : float = 1.602176634e-19 # C
BOLTZMANN_CONSTANT : float = 1.380649e-23 # J/K
PLANCKS_CONSTANT : float = 6.62607015e-34 # Js

# Parameters used for Varshi's Equation to calculate Band Gap as a function of Temperature
@dataclass
class VarshniParametersClass:
    alpha: float # in eV/k
    beta: float # in K

# Parameters used for Caughey-Thomas empirical method calculating
# mobilities as a function of temperature
@dataclass
class MobilityInfoClass:
    electron_max_300k: float # in cm*2/Vs
    hole_max_300k: float
    e_max_scaling_exponent: float
    h_max_scaling_exponent: float

    electron_min_300k: float
    hole_min_300k: float
    e_min_scaling_exponent:float 
    h_min_scaling_exponent: float

    e_reference_doping_conc_300k: float
    h_reference_doping_conc_300k: float

    e_reference_scaling_exponent: float
    h_reference_scaling_exponent: float

    e_slope_factor: float
    h_slope_factor: float

# Parameters used for Fossum's empirical model calculating minority
# carrier lifetimes as function of doping levels
@dataclass
class MinorityLifetimeInfoClass:
    h_max_lifetime: float
    e_max_lifetime: float

    e_Nref: float
    h_Nref: float

    e_fitting_expo: float
    h_fitting_expo: float

# Material class
@dataclass
class Material:

    name : str
    symbol : str
    Eg_0K : float 
    permittivity : float 

    VarshniInfo: VarshniParametersClass
    MobilityInfo: MobilityInfoClass
    MinorityLifetimeInfo: MinorityLifetimeInfoClass

    # Determine how bandgap changes depending on temperature via Varshni's Equation
    # Returns bandgap in eV
    def _calculate_Band_Gap(T:float, MaterialName) -> float:
       return MATERIAL_LIST[MaterialName].Eg_0K - ((MATERIAL_LIST[MaterialName].VarshniInfo.alpha * T**2)/(T + MATERIAL_LIST[MaterialName].VarshniInfo.beta))


    # Calculates Density of States at each band edge in m^-3
    # Formulas taken from the Ioffe Institute's Website
    def _calculate_DOS_at_band_edge(T : float) -> tuple[float,float]:
  
        Nc = Concentration(6.2e15*(T**(3/2)), "cm-3")
        Nv = Concentration(3.5e15*(T**(3/2)), "cm-3")

        return Nc, Nv

    # Calculates intrinsic carrier concentration in m^-3
    def _calculate_intrinsic_carrier_conc(T:float, MaterialName: str) -> float:

        # Density of states at band edges
        Nc, Nv = Material._calculate_DOS_at_band_edge(T)

        # Band Gap calc
        Eg = Material._calculate_Band_Gap(T, MaterialName)

        exponentialTerm = np.exp(-Eg/((BOLTZMANN_CONSTANT/ELECTRON_CHARGE) * T))

        # intrinsic carrier conc
        intrinsic_carrier_conc : float  = np.sqrt(Nc * Nv * exponentialTerm)
        return intrinsic_carrier_conc


    ## Calculate Mobilities using Caughey-Thomas empirical method returns in cm2/Vs
    def _calculate_mobilities(self, T, Nd, Na) -> float:

        # Mobility Info
        mobInfo = self.MobilityInfo

        total_Dopants = Concentration(Nd + Na, "m-3")

        # electron and hole Nreferences at Temperature  
        e_Nref = mobInfo.e_reference_doping_conc_300k * (T/300)**mobInfo.e_reference_scaling_exponent
        h_Nref = mobInfo.h_reference_doping_conc_300k * (T/300)**mobInfo.h_reference_scaling_exponent


        # max and min electron mobility
        e_max = mobInfo.electron_max_300k * (T/300)**mobInfo.e_max_scaling_exponent
        e_min = mobInfo.electron_min_300k * (T/300)**mobInfo.e_min_scaling_exponent

        # max and min hole mobility
        h_max = mobInfo.hole_max_300k * (T/300)**mobInfo.h_max_scaling_exponent
        h_min = mobInfo.hole_min_300k * (T/300)**mobInfo.h_min_scaling_exponent


        # Final electron and hole mobilities at temperature T via Caughey-Thomas Empirical methods in m2/Vs
        e_mobil_m2_per_Vs = e_min + (e_max - e_min)/(1 + (total_Dopants/e_Nref)**mobInfo.e_slope_factor)
        h_mobil_m2_per_Vs = h_min + (h_max - h_min)/(1 + (total_Dopants/h_Nref)**mobInfo.h_slope_factor)

        # Converted to cm2/Vs for simplicity
        e_mobil = e_mobil_m2_per_Vs * 1e4
        h_mobil = h_mobil_m2_per_Vs * 1e4

        return e_mobil, h_mobil


    # Calculate minority Carrier lifetimes via Fossum's Model returns in s
    def _calculate_lifetimes(self, Nd, Na):

        # Minority Carrier Lifetime Info
        minLifeInfo = self.MinorityLifetimeInfo

        # Minority Carrier Lifetimes via Fossum's Model
        min_life_h = minLifeInfo.h_max_lifetime / (1 + (Nd/minLifeInfo.h_Nref)**minLifeInfo.h_fitting_expo)
        min_life_e = minLifeInfo.e_max_lifetime / (1 + (Na/minLifeInfo.e_Nref)**minLifeInfo.e_fitting_expo)
        return min_life_e, min_life_h


MATERIAL_LIST : dict[str, Material] = {

    "Silicon": Material(
        name = "Silicon",
        symbol = "Si",
        Eg_0K = 1.17,
        permittivity = 1.04e-10,
        VarshniInfo = VarshniParametersClass(
            alpha = 4.73e-4,
            beta = 636,
        ),
        MobilityInfo = MobilityInfoClass(
            electron_max_300k = Mobility(1417,"cm2/Vs"),
            hole_max_300k = Mobility(470.5,"cm2/Vs"),
            e_max_scaling_exponent = -2.33,
            h_max_scaling_exponent = -2.23,
        
            electron_min_300k = Mobility(52.2,"cm2/Vs"),
            hole_min_300k = Mobility(44.9, "cm2/Vs"),
            e_min_scaling_exponent = -0.57,
            h_min_scaling_exponent = -0.57,
        
            e_reference_doping_conc_300k = Concentration(9.68e16,"cm-3"),
            h_reference_doping_conc_300k = Concentration(2.23e17,"cm-3"),
        
            e_reference_scaling_exponent = 2.54,
            h_reference_scaling_exponent = 2.40,
        
            e_slope_factor = 0.680,
            h_slope_factor = 0.719
        ),
        MinorityLifetimeInfo = MinorityLifetimeInfoClass(

            e_max_lifetime = Time(10e-6,"s"),
            h_max_lifetime = Time(3e-6,"s"),

            e_Nref = Concentration(10e16,"cm-3"),
            h_Nref = Concentration(10e16,"cm-3"),

            e_fitting_expo = 1,
            h_fitting_expo = 1

        )

    )
}



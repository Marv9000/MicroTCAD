import Materials
import numpy as np
from UnitSystem import *



MATERIAL_LIST = Materials.MATERIAL_LIST

# Constants not to be changed
ELECTRON_CHARGE: float = 1.602e-19
BOLTZMANN_CONSTANT : float = 1.380649e-23

# Solves a 1D Poisson equation for pn junction in equlibrium utilising Newton-Raphson iteration and nondimensionalisation
# Returns x being the grid seperation and V being the voltage at each grid point throughout the pn junction
def _1D_Poisson_For_Diodes_Equilibrium(MaterialName, Nd, Na, T, device_length):

    # Thermal Voltage
    Vth = (BOLTZMANN_CONSTANT * T) / ELECTRON_CHARGE

    # Concentration scaling factor
    Cref = max(Nd, Na)

    # Debye Length
    Ld = np.sqrt((MATERIAL_LIST[MaterialName].permittivity * Vth) / (ELECTRON_CHARGE * Cref))

    # Calculates suitable N value so Voltage in Depletion Region can be visualised
    N_ideal = int(np.ceil((4 * device_length)/ Ld)) + 1
    
    # Cap N so computation isnt too long
    N = max(2000, min(N_ideal, 8000))

    # Define grid spacing
    x = np.linspace(-device_length/2, device_length/2, N)

    # Define step length
    h = x[1] - x[0]

    # Set a grid for P and N regions and populate with their dopant levels
    Nd_grid = np.zeros(N)
    Na_grid = np.zeros(N)

    Nd_grid[x > 0] = Nd
    Na_grid[x <= 0] = Na

    # Intrinsic carrier concentration
    ni = Materials.Material._calculate_intrinsic_carrier_conc(T, MaterialName)


    # Voltages in the bulk regions
    Vp = -Vth * np.log(Na / ni)
    Vn = Vth * np.log(Nd / ni)


    # Debye Length
    Ld = np.sqrt((MATERIAL_LIST[MaterialName].permittivity * Vth) / (ELECTRON_CHARGE * Cref))
    h_scaled = h / Ld

    # Nondimensionalisation of concentrations
    Nd_scaled = Nd_grid / Cref
    Na_scaled = Na_grid / Cref
    ni_scaled = ni / Cref


    # Initial voltage guess and nondimensionalisation of Voltage
    V = np.linspace(Vp, Vn, N)
    V_scaled = V / Vth

    tolerance = 1e-5
    max_error = 1
    iterations = 0
    max_iteration_count = 500

    while max_error > tolerance and iterations < max_iteration_count:

        # Reset Residuals and Jacobian every iteration
        R = np.zeros(N)
        J = np.zeros((N, N))


        for i in range(1, N-1):

            # Scaled concentration values
            n_scaled = ni_scaled * np.exp(V_scaled[i])
            p_scaled = ni_scaled * np.exp(-V_scaled[i])

            
            # Residual Calculation
            R[i] = (V_scaled[i-1] - 2*V_scaled[i] + V_scaled[i+1]) / h_scaled**2 + (p_scaled - n_scaled + Nd_scaled[i] - Na_scaled[i])

            # Jacobian Matrix Calculation
            J[i, i]   = -2/h_scaled**2 - n_scaled - p_scaled
            J[i, i-1] = 1/h_scaled**2
            J[i, i+1] = 1/h_scaled**2

        # Set Direchelt Boundaries allowing convergence to these values
        J[0, 0] = 1
        J[N-1, N-1] = 1
        R[N-1] = 0
        
        # Determine Max residual
        max_error = np.max(np.abs(R))

        # Compute change in V_scaled needed to converge via Newtons formula
        delta_V = np.linalg.solve(J, -R)

        # Prevents V_Scaled from becoming too large and creating a large exponential
        delta_V = np.clip(delta_V, -1, 1) 

        # Damp the effect of delta_V ensuring fluctuations due to Newtons method are not too large
        V_scaled = V_scaled + 0.5 * delta_V

        iterations += 1
        print(iterations)
    

    if iterations == max_iteration_count:
        print("Warning: iterations reached max before converging to tolerance.")

    # Convert V_scaled back to V to get final V readings  
    V = V_scaled * Vth

    return x, V


# Calculates diode current via Shockley Diode Equation
def _shockley_diode_current(MaterialName ,Nd, Na, T, A, voltageAcross):

    # Intrinsic carrier conc
    ni = Materials.Material._calculate_intrinsic_carrier_conc(T, MaterialName)

    #Thermal Voltage
    Vth = (BOLTZMANN_CONSTANT * T) / ELECTRON_CHARGE

    # Electron and Hole minority carrier lifetimes
    e_life, h_life = MATERIAL_LIST[MaterialName]._calculate_lifetimes(Nd,Na)

    #Electron and Hole mobilities
    e_mobil, h_mobil = MATERIAL_LIST[MaterialName]._calculate_mobilities(T, Nd, Na)

    # Electron and hole diffusion Coefficients in m2/s
    Dp = h_mobil * Vth
    Dn = e_mobil * Vth

    # Minority carrier diffusion lenghts in m
    Lp = np.sqrt(Dp * h_life)
    Ln = np.sqrt(Dn * e_life)

    n_ideality = 1 

    # Calculates Reverse Saturation current
    Is = ELECTRON_CHARGE * A * ni**2 * (Dp / (Lp * Nd) + Dn / (Ln * Na))

    # Final current flowing through diode
    I = Is * (np.exp(voltageAcross / (n_ideality * Vth)) - 1)

    return I



"""
For V2 not fully implemented yet

Code for diode not in equilibrium will be finalised in my next version, the code below assumes
the Quasi-Fermi levels are constant and so does not properly account for how recombination
causes the voltage throughout the diode to drop

Will need to model Recombination and the continuity equations

def _1D_Poisson_For_Diodes_Not_Equilibrium(Nd, Na, T, device_length, voltageAcross, V_init=None):

    tolerance = 0.00001
    N = 100

    x = np.linspace(-device_length/2, device_length/2, N)
    h = x[1] - x[0]

    Nd_grid = np.zeros(N)
    Na_grid = np.zeros(N)
    Nd_grid[x > 0] = Nd
    Na_grid[x <= 0] = Na

    ni = Materials.Silicon._calculate_intrinsic_carrier_conc(T)
    Vth = (BOLTZMANN_CONSTANT * T) / ELECTRON_CHARGE
    inv_Vth = 1 / Vth

    Vp = -Vth * np.log(Na / ni)
    Vn = Vth * np.log(Nd / ni)

    
    if V_init is None:
        V = np.linspace(Vp, Vn, N)
    else:
        V = V_init.copy()
        V[0] = Vp
        V[-1] = Vn

    max_error = 1
    iterations = 0
    max_iteration_count = 500


    Ld = np.sqrt( (Silicon.permittivity*Vth) / (ELECTRON_CHARGE*ni) )
    h_scaled = h/Ld

    V_scaled = V/Vth

    Cref = max(Nd, Na)

    Ld = np.sqrt((Silicon.permittivity * Vth) / (ELECTRON_CHARGE * Cref))
    h_scaled = h / Ld

    Nd_scaled = Nd_grid / Cref
    Na_scaled = Na_grid / Cref
    ni_scaled = ni / Cref 

    phi_n_scaled = 0
    phi_p_scaled = -voltageAcross / Vth

    while max_error > tolerance and iterations < max_iteration_count:
    
        R = np.zeros(N)
        J = np.zeros((N, N))
        J[0, 0] = 1 / h**2
        J[N-1, N-1] = 1 / h**2

        for i in range(1, N-1):

            doping_difference = Nd_grid[i]-Na_grid[i]

            C = abs(doping_difference)


            n_scaled = ni_scaled * np.exp(V_scaled[i] - phi_n_scaled)
            p_scaled = ni_scaled * np.exp(phi_p_scaled - V_scaled[i])

            R[i] = (V_scaled[i-1] - 2*V_scaled[i] + V_scaled[i+1]) / h_scaled**2 + (p_scaled - n_scaled + Nd_scaled[i] - Na_scaled[i])
            J[i,i]   = -2/h_scaled**2 - n_s - p_s
            J[i,i-1] = 1/h_scaled**2
            J[i,i+1] = 1/h_scaled**2

        R[0] = 0
        R[N-1] = 0

        max_error = np.max(abs(R))
        print(max_error)
        delta_V = np.linalg.solve(J, (-R))
        V_scaled = V_scaled + 0.5 * delta_V
        iterations += 1

    if iterations == max_iteration_count:
        print("Iterations reached max at voltageAcross =", voltageAcross)


    V = V_scaled * Vth
    return V  


This section of code allowed me to ramp up my voltage guesses from V=0 allowing for the voltage guesses to be more accurate
and take less iterations to converge  

#_1D_Poisson_For_Diodes_New(1e22,1e22, 300, 4e-6, 0.36)

def _diode_ramp_steps(Nd, Na, T, device_length, voltageAcross, V_step=0.02):

    n_steps = max(1, int(np.ceil(abs(voltageAcross) / V_step)))
    bias_points = np.linspace(0.0, voltageAcross, n_steps + 1)

    V = None
    for Va in bias_points:
        V = _1D_Poisson_For_Diodes_Not_Equilibrium(Nd, Na, T, device_length, Va, V_init=V)

    print(V)
    return V

"""

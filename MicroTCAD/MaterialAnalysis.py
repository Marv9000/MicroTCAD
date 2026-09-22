from Materials import Material
import numpy as np
import matplotlib.pyplot as plt

def intrinsic_Carrier_Conc_Vs_Temp(MaterialName):

    #Temp boundaries set to stay within the extrinsic region
    temp_min = 200
    temp_max = 600

    # step_length
    step_length = 1

    # Tempature array
    T = np.arange(temp_min, temp_max + step_length, step_length)

    # creates intrinsic carrier conc array same length as temperature array
    ni_array = np.array([
        Material._calculate_intrinsic_carrier_conc(tempA, MaterialName)
        for tempA in T
    ])

    # 3. Plot using a logarithmic y-axis
    plt.figure()
    plt.semilogy(T, ni_array)

    plt.xlabel("Temperature (K)")
    plt.ylabel("Intrinsic Carrier Concentration ni, m-3")
    plt.title("Silicon Intrinsic Carrier Conc Temperature Dependency (Log Scale)")
    plt.grid(True)

    plt.savefig("ni_vs_temperature.png")
    plt.show()
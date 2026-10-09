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
        Material._calculate_intrinsic_carrier_conc(temp, MaterialName)
        for temp in T
    ])

    # 3. Plot using a logarithmic y axis
    plt.figure()
    plt.semilogy(T, ni_array)

    plt.xlabel("Temperature (K)")
    plt.ylabel("Intrinsic Carrier Concentration ni, m-3")
    plt.title(f"{MaterialName} Intrinsic Carrier Conc Temperature Dependency (Log Scale)")
    plt.grid(True)

    plt.savefig("ni_vs_temperature.png")
    plt.show()

def CMP_intrinsic_Carrier_Conc_Vs_Temp(Material1, Material2):

    #Temp boundaries set to stay within the extrinsic region
    temp_min = 200
    temp_max = 600

    step_length = 1
    
    # Tempature array
    T = np.arange(temp_min, temp_max + step_length, step_length)
        
    # creates intrinsic carrier conc array same length as temperature array
    ni_array1 = np.array([
        Material._calculate_intrinsic_carrier_conc(temp, Material1)
        for temp in T
    ])
    ni_array2 = np.array([
        Material._calculate_intrinsic_carrier_conc(temp, Material2)
        for temp in T
    ])


    # 3. Plot using a logarithmic y axis
    plt.figure()
    plt.semilogy(T, ni_array1, label=Material1, color="blue")
    plt.semilogy(T, ni_array2, label =Material2, color="red")
    

    plt.xlabel("Temperature (K)")
    plt.ylabel("Intrinsic Carrier Concentration ni, m-3")
    plt.title(f"Comparison of Intrinsic Carrier Conc Temperature Dependency (Log Scale)")

    plt.legend()
    plt.grid(True)

    plt.savefig("ni_vs_temperature.png")
    plt.show()



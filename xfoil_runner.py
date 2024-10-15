# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 04:44:19 2024

@author: Pradeep
"""

import os
import subprocess
import numpy as np

# %% Inputs

# Define the paths for airfoil files
airfoil_folder = r"F:\ISAE_SUPAERO_Classroom\Applied_Aerodynamics\Mini Project\Airfoils\xfoil-runner-main\xfoil_runner\airfoil_dat"  # Path to the folder containing airfoil .dat files

# Analysis parameters
alpha_i = -5              # Initial angle of attack
alpha_f = 20              # Final angle of attack
alpha_step = 0.5          # Step size for angles of attack
Re = 12600000              # Reynolds number
n_iter = 100              # Number of iterations for convergence

# Initialize a list to store results
results = []

# %% Loop through each airfoil in the specified folder
for airfoil_file in os.listdir(airfoil_folder):
    if airfoil_file.endswith(".dat"):
        airfoil_name = os.path.splitext(airfoil_file)[0]  # Get the airfoil name without the extension

        # Create input file for XFOIL commands
        with open("input_file.in", 'w') as input_file:
            input_file.write(f"LOAD {airfoil_file}\n")
            input_file.write("PANE\n")
            input_file.write("OPER\n")
            input_file.write(f"Visc {Re}\n")
            input_file.write("PACC\n")
            input_file.write(f"polar_file_{airfoil_name}.txt\n\n")  # Temporary polar file name
            input_file.write(f"ITER {n_iter}\n")
            input_file.write(f"ASeq {alpha_i} {alpha_f} {alpha_step}\n")
            input_file.write("PACC\n")  # Again use a new polar file to capture results
            input_file.write("QUIT\n")  # Exit XFOIL

        # Run XFOIL using subprocess
        try:
            subprocess.run(["xfoil.exe"], stdin=open("input_file.in"), check=True, cwd=airfoil_folder)
            print(f"XFOIL ran successfully for {airfoil_name}.")
        except FileNotFoundError:
            print("Error: XFOIL not found. Please ensure xfoil.exe is in the current directory.")
            continue  # Skip to the next airfoil
        except PermissionError:
            print("PermissionError: Access denied when trying to run XFOIL.")
            continue  # Skip to the next airfoil
        except subprocess.CalledProcessError as e:
            print(f"Error running XFOIL for {airfoil_name}: {e}")
            continue  # Skip to the next airfoil

        # Check if the polar file was generated and process it
        polar_file_path = os.path.join(airfoil_folder, f"polar_file_{airfoil_name}.txt")  # Correct path for polar file
        if os.path.exists(polar_file_path):
            # Load polar data
            polar_data = np.loadtxt(polar_file_path, skiprows=12)  # Skip the header lines
            
            # Extract CL and CD values
            alpha = polar_data[:, 0]  # Angle of attack
            cl = polar_data[:, 1]      # Lift coefficient
            cd = polar_data[:, 2]      # Drag coefficient
            
            # Calculate Cl^(3/2)/Cd and L/D
            cd = np.where(cd == 0, 1e-10, cd)  # Replace 0 with a small value to avoid division by zero
            cl_cubed_div_cd = (cl ** (3/2)) / cd
            ld = cl / cd  # Lift-to-drag ratio
            
            # Find maximum Cl^(3/2)/Cd and maximum L/D
            max_cl_cubed_div_cd = np.max(cl_cubed_div_cd)
            max_ld = np.max(ld)

            # Append results to the list
            results.append({
                'airfoil': airfoil_name,
                'max_cl_cubed_div_cd': max_cl_cubed_div_cd,
                'max_ld': max_ld,
            })
        else:
            print(f"Error: polar file not found for {airfoil_name}. Check if XFOIL ran correctly.")

# Sort results by max Cl^(3/2)/CD and then by max L/D
sorted_results = sorted(results, key=lambda x: (x['max_cl_cubed_div_cd'], x['max_ld']), reverse=True)

# Get top 10 airfoils
top_10_airfoils = sorted_results[:10]

# Print top 10 airfoil names
print("Top 10 Airfoils based on Cl^(3/2)/CD and L/D:")
for airfoil in top_10_airfoils:
    print(airfoil['airfoil'])
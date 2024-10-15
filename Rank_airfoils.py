import os
import numpy as np

def calculate_max_cl_ratio(file_path):
    alpha_values = []  # List to store angle of attack values
    cl_values = []     # List to store lift coefficient values
    cd_values = []     # List to store drag coefficient values
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            # Split the line into components
            components = line.split()
            if len(components) == 7:  # Ensure there are 7 elements
                alpha, cl, cd, cd_p, cm, top_xtr, bot_xtr = map(float, components)
                alpha_values.append(alpha)  # Collect angle of attack
                cl_values.append(cl)         # Collect lift coefficient
                cd_values.append(cd)         # Collect drag coefficient
    
    # Convert to numpy arrays for easier calculations
    cl_array = np.array(cl_values)
    cd_array = np.array(cd_values)
    alpha_array = np.array(alpha_values)

    # Filter out non-positive lift coefficients and non-positive drag coefficients
    valid_indices = (cl_array > 0) & (cd_array > 0)
    cl_array = cl_array[valid_indices]
    cd_array = cd_array[valid_indices]
    alpha_array = alpha_array[valid_indices]

    # Check if there are valid values after filtering
    if cl_array.size == 0 or cd_array.size == 0:
        print(f"No valid data found in {file_path}")
        return None, None

    # Calculate CL^(3/2) / CD
    cl_ratio = (cl_array ** (3 / 2)) / cd_array

    # Find the maximum value and its corresponding angle
    max_index = np.argmax(cl_ratio)
    max_value = cl_ratio[max_index]
    corresponding_alpha = alpha_array[max_index]

    return max_value, corresponding_alpha

def process_airfoil_data(input_folder):
    results = {}
    
    # Iterate over each file in the specified folder
    for filename in os.listdir(input_folder):
        if filename.endswith('_extracted.txt'):  # Check for extracted text files
            file_path = os.path.join(input_folder, filename)
            max_value, corresponding_alpha = calculate_max_cl_ratio(file_path)
            airfoil_name = filename.replace('_extracted.txt', '')  # Get airfoil name from filename
            
            if max_value is not None and corresponding_alpha is not None:
                # Store the results
                results[airfoil_name] = {
                    'max_value': max_value,
                    'alpha': corresponding_alpha
                }
    
    return results

def main():
    # Specify the input folder
    input_folder = r'F:\isae_supaero_classroom\applied_aerodynamics\mini project\airfoils\xfoil-runner-main\xfoil_runner\output'  # Change this to your output folder path

    results = process_airfoil_data(input_folder)

    # Sort results by max_value in descending order
    sorted_airfoils = sorted(results.items(), key=lambda item: item[1]['max_value'], reverse=True)

    # Print all results
    print("Airfoils ranked by CL^(3/2)/CD:")
    for airfoil, data in sorted_airfoils:
        print(f"Airfoil: {airfoil}, Max CL^(3/2)/CD: {data['max_value']:.4f} at alpha: {data['alpha']:.2f}")

if __name__ == "__main__":
    main()

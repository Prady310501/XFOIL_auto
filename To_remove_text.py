import os
import re

def extract_polar_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    extracted_data = []
    # Regular expression to match lines with the numerical data
    data_pattern = re.compile(r'^\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)')

    for line in lines:
        # Match the pattern in each line
        match = data_pattern.match(line)
        if match:
            # Join the matched groups with a space
            extracted_data.append(' '.join(match.groups()))

    return extracted_data

def write_extracted_data_to_txt(extracted_data, output_file_path):
    with open(output_file_path, 'w') as outfile:
        for data_line in extracted_data:
            outfile.write(data_line + '\n')

def clean_folder_text_files(input_folder, output_folder):
    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each file in the specified folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):  # Check for text files
            file_path = os.path.join(input_folder, filename)
            extracted_data = extract_polar_data(file_path)

            # Write extracted data to a new text file in the output folder
            output_file_path = os.path.join(output_folder, filename.replace('.txt', '_extracted.txt'))
            write_extracted_data_to_txt(extracted_data, output_file_path)

            print(f'Extracted data and saved to: {output_file_path}')

# Specify the input and output folders
input_folder = r"F:\ISAE_SUPAERO_Classroom\Applied_Aerodynamics\Mini Project\Airfoils\xfoil-runner-main\xfoil_runner\airfoil_dat"  # Change this to your input folder path
output_folder = r"F:\ISAE_SUPAERO_Classroom\Applied_Aerodynamics\Mini Project\Airfoils\xfoil-runner-main\xfoil_runner\Output"  # Change this to your output folder path

clean_folder_text_files(input_folder, output_folder)

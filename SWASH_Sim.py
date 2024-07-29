import os
import inductiva

# Initialize the MachineGroup
machine_group = inductiva.resources.MachineGroup(machine_type="c3d-standard-60", spot=True)
machine_group.start()

# Initialize the Simulator
swash = inductiva.simulators.SWASH(version="9.01A")  # Or you can use "10.01"

# Define the root directory containing subdirectories with input.sws files
root_dir = '3.Random_BWs_codes/Inductiva_Simulations/Simulations'
output_dir = 'Simulation_outputs'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to run simulations and download results
def run_simulations():
    for subdir, _, files in os.walk(root_dir):
        if 'input.sws' in files:
            # Define the full path to the input.sws file and its parent directory
            input_file_path = os.path.join(subdir, 'input.sws')
            
            # Define the output path for this specific simulation
            subdir_name = os.path.basename(subdir)
            output_subdir = os.path.join(output_dir, subdir_name)
            os.makedirs(output_subdir, exist_ok=True)
            
            # Run the simulation using the Inductiva API
            task = swash.run(input_dir=subdir,  # directory containing input.sws
                             sim_config_filename="input.sws",  # executive file
                             on=machine_group, n_vcpus=30)  # specify machine group and CPUs
            
            # Wait for the task to complete
            task.wait()
            
            # Download the results to the appropriate directory
            task.download_outputs(output_dir=output_subdir)

# Run simulations
run_simulations()

# Terminate the MachineGroup at the end of all simulations
machine_group.terminate()

print("All simulations completed and results downloaded.")


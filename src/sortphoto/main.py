import os
import time
import getopt, sys
from file_utils import collect_file_paths,display_directory_tree,simulate_directory_tree, display_simulated_tree 
from data_processing import process_files_by_date, process_files_by_type,execute_operations

DATA_PATH = "/mnt/e/media"
OUTPUT_PATH = "/mnt/e/organized_media"
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hdt"
# Long options
long_options = ["Help", "date", "type"]

def get_yes_no(prompt):
    """Prompt the user for a yes/no response."""
    while True:
        response = input(prompt).strip().lower()
        if response in ('yes', 'y'):
            return True
        elif response in ('no', 'n'):
            return False
        elif response == '/exit':
            print("Exiting program.")
            exit()
        else:
            print("Please enter 'yes' or 'no'. To exit, type '/exit'.")

def main():
    dry_run = True
    mode=""
    output_path = OUTPUT_PATH

    print("-" * 50)
    print(f"[DEBUG] Raw command-line arguments: {sys.argv}")
    print(f"[DEBUG] Parsed argument list: {argumentList}")
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        print(f"[DEBUG] Parsed arguments: {arguments}")
        print(f"[DEBUG] Remaining values: {values}")

         # checking each argument
        for currentArgument, currentValue in arguments:
            print(f"[DEBUG] Processing argument: {currentArgument} with value: {currentValue}")
            if currentArgument in ("-h", "--Help"):
                print("Please choose the mode to organize your files:")
                print("-d, -date By Date")
                print("-t, -type By Type")
            
            elif currentArgument in ("-d", "--date"):
                print ("Process files by date:", sys.argv[0])
                mode ='date'
                print(f"[DEBUG] Mode set to: {mode}")
            
            elif currentArgument in ("-t", "--type"):
                print (("Process files by type ") )
                mode = 'type'
                print(f"[DEBUG] Mode set to: {mode}")
            else:
                print("Something went wrong try agin")
                exit

    except getopt.error as err:
        print(str(err))
        exit
    
    print(f"[DEBUG] Final mode value: '{mode}'")
    print("-" * 50)
    
    # Start processing files
    start_time = time.time()
    file_paths = collect_file_paths(DATA_PATH)
    end_time = time.time()
    print("-" * 50)
    print("Directory tree before organizing:")
    # display_directory_tree(DATA_PATH)
    print("*" * 50)
    # Confirm successful output path
    message = f"Output path successfully set to: {output_path}"
    print("-" * 50)
    message = f"Time taken to load file paths: {end_time - start_time:.2f} seconds"
    print("-" * 50)
    
    if mode: 
        # mode = get_mode_selection()
        file_paths = collect_file_paths(DATA_PATH)
        # Confirm successful output path
        output_path = OUTPUT_PATH
        print(f"Output path successfully set to: {output_path}")
        print("-" * 50)
        if mode == 'date':
            # Process files by date
            operations = process_files_by_date(file_paths, output_path, dry_run=dry_run)
        if mode == 'type':
            # Process files by type
            operations = process_files_by_type(file_paths, output_path, dry_run=dry_run)
        # Simulate and display the proposed directory tree
        print("-" * 50)
        message = "Proposed directory structure:"
        print(message)
        print(os.path.abspath(output_path))
        simulated_tree = simulate_directory_tree(operations, output_path)
        display_simulated_tree(simulated_tree)
        print("-" * 50)
        # Ask user if they want to proceed
        proceed = get_yes_no("Would you like to proceed with these changes? (yes/no): ")
        if proceed:
            # Create the output directory now
            os.makedirs(output_path, exist_ok=True)

            # Perform the actual file operations
            message = "Performing file operations..."

            print(message)
            execute_operations(
            operations,
            dry_run=False,
           
            )

            message = "The files have been organized successfully."
            print("-" * 50)
            print(message)
            print("-" * 50)
    else:
        print("[DEBUG] No mode selected. Please use -d (date) or -t (type)")
   
if __name__=="__main__":
    main()
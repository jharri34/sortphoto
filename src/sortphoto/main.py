import os
import time
import getopt, sys
from file_utils import collect_file_paths,display_directory_tree,simulate_directory_tree, display_simulated_tree 
from data_processing import process_files_by_date, process_files_by_type,execute_operations

# Paths
DATA_PATH = "/mnt/e/media"
OUTPUT_PATH = "/mnt/e/organized_media"

# Messages
HELP_MESSAGE = "Please choose the mode to organize your files:"
DATE_MODE_MESSAGE = "-d, --date By Date"
TYPE_MODE_MESSAGE = "-t, --type By Type"
PROCESS_BY_DATE = "Process files by date:"
PROCESS_BY_TYPE = "Process files by type"
ERROR_MESSAGE = "Something went wrong try again"
TREE_BEFORE_MESSAGE = "Directory tree before organizing:"
OUTPUT_PATH_MESSAGE = "Output path successfully set to:"
FILE_LOAD_TIME_MESSAGE = "Time taken to load file paths:"
PROPOSED_STRUCTURE_MESSAGE = "Proposed directory structure:"
PROCEED_MESSAGE = "Would you like to proceed with these changes? (yes/no): "
PERFORMING_OPS_MESSAGE = "Performing file operations..."
SUCCESS_MESSAGE = "The files have been organized successfully."
NO_MODE_MESSAGE = "No mode selected. Please use -d (date) or -t (type)"
SEPARATOR = "-" * 50
DEBUG_PREFIX = "[DEBUG]"
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

    print(SEPARATOR)
    print(f"{DEBUG_PREFIX} Raw command-line arguments: {sys.argv}")
    print(f"{DEBUG_PREFIX} Parsed argument list: {argumentList}")
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        print(f"{DEBUG_PREFIX} Parsed arguments: {arguments}")
        print(f"{DEBUG_PREFIX} Remaining values: {values}")

         # checking each argument
        for currentArgument, currentValue in arguments:
            print(f"{DEBUG_PREFIX} Processing argument: {currentArgument} with value: {currentValue}")
            if currentArgument in ("-h", "--Help"):
                print(HELP_MESSAGE)
                print(DATE_MODE_MESSAGE)
                print(TYPE_MODE_MESSAGE)
            
            elif currentArgument in ("-d", "--date"):
                print(PROCESS_BY_DATE, sys.argv[0])
                mode ='date'
                print(f"{DEBUG_PREFIX} Mode set to: {mode}")
            
            elif currentArgument in ("-t", "--type"):
                print(PROCESS_BY_TYPE)
                mode = 'type'
                print(f"{DEBUG_PREFIX} Mode set to: {mode}")
            else:
                print(ERROR_MESSAGE)
                exit

    except getopt.error as err:
        print(str(err))
        exit
    
    print(f"{DEBUG_PREFIX} Final mode value: '{mode}'")
    print(SEPARATOR)
    
    # Start processing files
    start_time = time.time()
    file_paths = collect_file_paths(DATA_PATH)
    end_time = time.time()
    print(SEPARATOR)
    print(TREE_BEFORE_MESSAGE)
    # display_directory_tree(DATA_PATH)
    print("*" * 50)
    # Confirm successful output path
    print(f"{OUTPUT_PATH_MESSAGE} {output_path}")
    print(SEPARATOR)
    print(f"{FILE_LOAD_TIME_MESSAGE} {end_time - start_time:.2f} seconds")
    print(SEPARATOR)
    
    if mode: 
        # mode = get_mode_selection()
        file_paths = collect_file_paths(DATA_PATH)
        # Confirm successful output path
        output_path = OUTPUT_PATH
        print(f"{OUTPUT_PATH_MESSAGE} {output_path}")
        print(SEPARATOR)
        if mode == 'date':
            # Process files by date
            operations = process_files_by_date(file_paths, output_path, dry_run=dry_run)
        if mode == 'type':
            # Process files by type
            operations = process_files_by_type(file_paths, output_path, dry_run=dry_run)
        # Simulate and display the proposed directory tree
        print(SEPARATOR)
        print(PROPOSED_STRUCTURE_MESSAGE)
        print(os.path.abspath(output_path))
        simulated_tree = simulate_directory_tree(operations, output_path)
        display_simulated_tree(simulated_tree)
        print(SEPARATOR)
        # Ask user if they want to proceed
        proceed = get_yes_no(PROCEED_MESSAGE)
        if proceed:
            # Create the output directory now
            os.makedirs(output_path, exist_ok=True)

            # Perform the actual file operations
            print(PERFORMING_OPS_MESSAGE)
            execute_operations(
            operations,
            dry_run=False,
           
            )

            print(SEPARATOR)
            print(SUCCESS_MESSAGE)
            print(SEPARATOR)
    else:
        print(f"{DEBUG_PREFIX} {NO_MODE_MESSAGE}")
   
if __name__=="__main__":
    main()
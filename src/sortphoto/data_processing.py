import os
import datetime 

def process_files_by_date(file_paths, output_path, dry_run=True):
    """Process files to organize them by date."""
    operations = []
    for file_path in file_paths:
        # Get the modification time
        mod_time = os.path.getmtime(file_path)
        # Convert to datetime
        mod_datetime = datetime.datetime.fromtimestamp(mod_time)
        year = mod_datetime.strftime('%Y')
        month = mod_datetime.strftime('%B')  # e.g., 'January', or use '%m' for month number
        # Create directory path
        dir_path = os.path.join(output_path, year, month)
        # Prepare new file path
        new_file_name = os.path.basename(file_path)
        new_file_path = os.path.join(dir_path, new_file_name)
        # Decide whether to use hardlink or symlink
        link_type = 'hardlink'  # Assume hardlink for now
        # Record the operation
        operation = {
            'source': file_path,
            'destination': new_file_path,
            'link_type': link_type,
        }
        operations.append(operation)
    return operations


def process_files_by_type(file_paths, output_path, dry_run=False):
    """Process files to organize them by type, first separating into text-based and image-based files."""
    operations = []

    # Define extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    

    for file_path in file_paths:
        # Exclude hidden files (additional safety)
        if os.path.basename(file_path).startswith('.'):
            continue

        # Get the file extension
        ext = os.path.splitext(file_path)[1].lower()

        # Check if it's an image file
        if ext in image_extensions:
            # Image-based files
            top_folder = f'{ext}'
            # You can add subcategories here if needed
            folder_name = top_folder

        else:
            # Other types
            folder_name = 'others'

        # Create directory path
        dir_path = os.path.join(output_path, folder_name)
        # Prepare new file path
        new_file_name = os.path.basename(file_path)
        new_file_path = os.path.join(dir_path, new_file_name)
        # Decide whether to use hardlink or symlink
        link_type = 'hardlink'  # Assume hardlink for now
        # Record the operation
        operation = {
            'source': file_path,
            'destination': new_file_path,
            'link_type': link_type,
        }
        operations.append(operation)

    return operations
def execute_operations(operations, dry_run=False, silent=False):
    """Execute the file operations."""
    total_operations = len(operations)
    
    print(f"Organizing Files... (0/{total_operations})")
    for idx, operation in enumerate(operations, 1):
        source = operation['source']
        destination = operation['destination']
        link_type = operation['link_type']
        dir_path = os.path.dirname(destination)

        if dry_run:
            message = f"Dry run: would create {link_type} from '{source}' to '{destination}'"
        else:
            # Ensure the directory exists before performing the operation
            os.makedirs(dir_path, exist_ok=True)

            try:
                if link_type == 'hardlink':
                    os.link(source, destination)
                else:
                    os.symlink(source, destination)
                message = f"Created {link_type} from '{source}' to '{destination}'"
            except Exception as e:
                message = f"Error creating {link_type} from '{source}' to '{destination}': {e}"

        # Silent mode handling
        if not silent:
            print(f"[{idx}/{total_operations}] {message}")
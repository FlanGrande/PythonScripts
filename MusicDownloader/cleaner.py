import os
import urllib.parse

def clean_filename(filename):
    # Decode HTML-encoded characters (like %20 -> space)
    clean_name = urllib.parse.unquote(filename)

    # Rebuild the filename with the original numbering and cleaned name
    return f"{clean_name.strip()}"

def rename_files_in_folder(folder_path):
    # List all files in the given folder
    for filename in os.listdir(folder_path):
        # Ensure it's a file and not a directory
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Clean the filename
            if filename.endswith(".mp3"):
                clean_name = clean_filename(filename)

                # Build full paths for renaming
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, clean_name)

                # Rename the file
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {clean_name}")

# Example usage
folder_path = '.'  # Update this to your folder path
rename_files_in_folder(folder_path)

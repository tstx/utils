import os

# Usage: put this script next to Songs folder, start with DRY_RUN and check log file.
# This script adds the artist name to the front of each song's folder.
# This makes it easier to get a good overview of your song collection 
# and share specific songs with your picky friends.
# Works on Windows, linux at own risk.

# Set this to True to do a dry run (no files will be renamed)
DRY_RUN = True

# Set the path to the Songs folder
songs_path = "Songs"

# Set up logging
log_file = open("log.txt", "a")
log_file.write(f"#####################################")

def get_artist_name(ini_path):
    # Open the file and read its contents
    encodings = ["utf-8", "iso-8859-1", "cp1252"]
    for encoding in encodings:
        try:
            with open(ini_path, "r", encoding=encoding) as f:
                contents = f.read()
            break
        except UnicodeDecodeError:
            pass

    # Split the contents into lines and loop through them
    for line in contents.split("\n"):
        # Strip any whitespace from the line
        line = line.strip()

        # strip any whitespace before and after the equals sign
        line = line.replace(" = ", "=")

        # Check if the line starts with "artist="
        if line.lower().startswith("artist="):
            # Extract the artist name from the line and return it
            artist_name = line.split("=")[1]
            artist_name = artist_name.replace("/", "-") # remove non filesystem characters
            return artist_name

    # If the artist name wasn't found, return None
    return None

# Loop through each subfolder in the Songs folder
for root, dirs, files in os.walk(songs_path):
    for file_name in files:
        if file_name.lower() == "song.ini":
            folder_path = root
            # Read the song.ini file for the artist name
            artist_name = get_artist_name(os.path.join(folder_path, file_name))

            if artist_name is None:
                print(f"WARNING: artist not found for {folder_path}")
                log_file.write(f"WARNING: artist not found for {folder_path}\n")
                continue

            # Rename the folder with the artist name, if it doesn't already start with the artist name
            folder_name = os.path.basename(folder_path)
            if folder_name.lower().startswith(artist_name.lower()):
                log_file.write(f"SKIPPING: {folder_name} already starts with artist\n")
            else:
                new_folder_name = f"{artist_name} - {folder_name}"
                if os.path.exists(os.path.join(songs_path, new_folder_name)):
                    log_file.write(f"SKIPPING: {folder_name} | {new_folder_name} already exists\n")
                else:
                    print(os.path.join(folder_path, "song.ini"))
                    if DRY_RUN:
                        log_file.write(f"DRY RUN (RENAME): {folder_name} | {new_folder_name}\n")
                    else:
                        os.rename(folder_path, os.path.join(songs_path, new_folder_name))
                        log_file.write(f"RENAMED: {folder_name} | {new_folder_name}\n")

# Close the log file
log_file.close()

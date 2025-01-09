import shutil
import glob
import zipfile
import os
import h5py

# List your ZIP files
zip_files = ["part1.zip", "part2.zip", "part3.zip", "part4.zip", "part5.zip"]

# Directory to extract files
extract_dir = "extracted_parts"
os.makedirs(extract_dir, exist_ok=True)

# Extract each ZIP file
for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(extract_dir)


# Find all parts in the extraction directory
parts = sorted(glob.glob(os.path.join(extract_dir, "yourfile.h5.*")))
output_file = "reconstructed_file.h5"

with open(output_file, "wb") as outfile:
    for part in parts:
        with open(part, "rb") as infile:
            outfile.write(infile.read())


try:
    with h5py.File(output_file, "r") as h5file:
        # List all groups
        print("Keys:", list(h5file.keys()))
        # Further verification can be done based on your knowledge of the file's structure
    print("File reconstructed successfully and is readable.")
except Exception as e:
    print(f"An error occurred: {e}")

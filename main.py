import os
from pymemuc import PyMemuc
import xml.etree.ElementTree as ET

# Initialize PyMemuc with debug mode enabled
pmc = PyMemuc(debug=True)
MY_VM_INDEX = 0  # Replace this with your target VM index if different

# Define paths
remote_path = "/sdcard/window_dump.xml"  # Common location on Android devices
local_directory = r"C:\Users\Harminder Nijjar\Desktop\Eufy"
local_file_path = os.path.join(local_directory, "window_dump.xml")

# Ensure local directory exists
os.makedirs(local_directory, exist_ok=True)

# Step 1: Dump the UI hierarchy to the XML file on the VM
dump_command = f"shell uiautomator dump {remote_path}"
dump_output = pmc.send_adb_command_vm(command=dump_command, vm_index=MY_VM_INDEX)
print("Dump Output:", dump_output)

# Check if dump was successful
if "UI hierchary dumped to" in dump_output or "UI hierarchy dumped to" in dump_output:
    # Step 2: Pull the dumped XML file to your local machine
    pull_command = f'pull {remote_path} "{local_file_path}"'
    pull_output = pmc.send_adb_command_vm(command=pull_command, vm_index=MY_VM_INDEX)
    print("Pull Output:", pull_output)

    # Check if pull was successful
    if os.path.exists(local_file_path):
        print(f"File successfully pulled to {local_file_path}")

        # Step 3: Parse the XML
        try:
            tree = ET.parse(local_file_path)
            root = tree.getroot()

            # Iterate through the elements and print their attributes
            for elem in root.iter():
                print(elem.tag, elem.attrib)

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
    else:
        print("Failed to pull the file. Please check the ADB connection and paths.")
else:
    print(
        "Failed to dump UI hierarchy. Please ensure the device is connected and accessible."
    )

import os
import gdown
import requests
from bs4 import BeautifulSoup
import json
import re

# Local folder
local_folder = "google_drive_downloads"

# Get list of local files
local_files = set()
if os.path.exists(local_folder):
    for file in os.listdir(local_folder):
        if file.endswith('.jpg') or file.endswith('.JPG'):
            local_files.add(file)

print(f"Local files found: {len(local_files)}")
print("Local files:")
for f in sorted(local_files):
    print(f"  - {f}")

print("\n" + "="*60)
print("Attempting to get complete list from Google Drive folder...")
print("="*60 + "\n")

# The folder URL
folder_url = "https://drive.google.com/drive/folders/1hlWeAtOZov0ycjVMOpdTDLbE1wukqLnC"

# Try to get the folder info using gdown's internal method
try:
    # Convert folder URL to a format that might work better
    folder_id = "1hlWeAtOZov0ycjVMOpdTDLbE1wukqLnC"

    # Try to get folder contents using requests
    response = requests.get(folder_url)

    if response.status_code == 200:
        # Try to extract file information from the page
        # Google Drive pages contain JSON data in script tags
        content = response.text

        # Look for patterns that might indicate files
        # Google Drive embeds file data in various formats

        # Try to find file IDs and names using regex
        file_pattern = r'"([0-9a-zA-Z_-]{28,})",.*?"(MUH_\d+\.jpg)"'
        matches = re.findall(file_pattern, content)

        if matches:
            print(f"Found {len(matches)} files in the Google Drive folder")

            # Create a set of remote files
            remote_files = {name for _, name in matches}

            # Find missing files
            missing_files = remote_files - local_files

            print(f"\nFiles in Google Drive: {len(remote_files)}")
            print(f"Files downloaded locally: {len(local_files)}")
            print(f"Files missing locally: {len(missing_files)}")

            if missing_files:
                print("\nMissing files:")
                for f in sorted(missing_files):
                    print(f"  - {f}")

                # Create a download script for missing files
                print("\nCreating script to download missing files...")

                # Get file IDs for missing files
                missing_with_ids = []
                for file_id, name in matches:
                    if name in missing_files:
                        missing_with_ids.append((file_id, name))

                # Write download script
                with open("download_missing_files.py", "w") as f:
                    f.write("import gdown\nimport os\nimport time\n\n")
                    f.write("output_dir = 'google_drive_downloads'\n")
                    f.write("if not os.path.exists(output_dir):\n")
                    f.write("    os.makedirs(output_dir)\n\n")
                    f.write("missing_files = [\n")
                    for file_id, name in missing_with_ids:
                        f.write(f'    ("{file_id}", "{name}"),\n')
                    f.write("]\n\n")
                    f.write("print(f'Downloading {len(missing_files)} missing files...')\n\n")
                    f.write("for i, (file_id, filename) in enumerate(missing_files, 1):\n")
                    f.write("    try:\n")
                    f.write("        output_path = os.path.join(output_dir, filename)\n")
                    f.write("        print(f'[{i}/{len(missing_files)}] Downloading {filename}...', end=' ')\n")
                    f.write("        url = f'https://drive.google.com/uc?id={file_id}'\n")
                    f.write("        gdown.download(url, output_path, quiet=True)\n")
                    f.write("        print('Done')\n")
                    f.write("        time.sleep(0.5)\n")
                    f.write("    except Exception as e:\n")
                    f.write("        print(f'Failed: {str(e)}')\n")

                print("Script 'download_missing_files.py' created!")
            else:
                print("\nAll files from the detected list are already downloaded!")
        else:
            print("Could not extract file list from the page")
            print("The folder might be private or the format has changed")

    else:
        print(f"Failed to access the folder: HTTP {response.status_code}")

except Exception as e:
    print(f"Error: {str(e)}")

# Alternative approach using the list we already have from the previous attempt
print("\n" + "="*60)
print("Using known file list from previous scan...")
print("="*60 + "\n")

# This is the list we identified earlier
known_files = [
    ("1ftZC2FNYZ3ft7dIAT3no1CS-66fkZvVS", "MUH_1018.jpg"),
    ("1WJvj7D9jEBFiJyKUO-ox7i3cwhb_ji4K", "MUH_1019.jpg"),
    ("1FDz3DNymN6Hj4dHUbD890JB0_GtUqIja", "MUH_1020.jpg"),
    ("1WOiRyO1qP6_jGv9Oc1R5gAsi5KQWZ03W", "MUH_1025.jpg"),
    ("1f1pUNFjxu0wbVHSVFOdkpve8sDOxGItH", "MUH_1027.jpg"),
    ("1OxuvB0-PSbK0wZ0PoxV6Qb1mwOpfWUXL", "MUH_1030.jpg"),
    ("1sYBDES4JI1ibJIpR5FYN9JkhR3px4ctc", "MUH_1032.jpg"),
    ("1LKI69H3W4MiaRSdmlW0Uwwg4rlCiJ7wC", "MUH_1040.jpg"),
    ("18N5UJZhvFB7aU0nF53SvIamgtmf-f9eX", "MUH_1043.jpg"),
    ("1nndwNkof0QN-4U39CJH2bMFiSQ5DdZSn", "MUH_1051.jpg"),
    ("1eDh60kgWSxgGm8x3ysH41PF-ec4Eztnk", "MUH_1053.jpg"),
    ("1Cld5ABv_hBszlWCz3pgYXZ_pyz51fRFb", "MUH_1057.jpg"),
    ("17TTZl5z0Gbjh2t2kgy-TPGnKAMVelJAu", "MUH_1068.jpg"),
    ("1UP9cos0WMsdi6U0NDkvLXzX3DMG5hE9w", "MUH_1081.jpg"),
    ("11cQAYMkB9qTH_9gc5BrSoIw7pmOiMSdf", "MUH_1086.jpg"),
    ("1XNdM7k4rbAMBqrfYwb-BIwl3IGpX4ZVO", "MUH_1089.jpg"),
    ("1kQSir3_Tg5a3p2euPfktp48eBSX5Tjly", "MUH_1090.jpg"),
    ("1vq_4xClTCv7lXcA2ktDwY79A9LnXDqN_", "MUH_1092.jpg"),
    ("1HDB6rMzzGfISTaPl49beFccNDeZBmYNL", "MUH_1094.jpg"),
    ("1QS_uDKzwlLWW0XJJK3ZSIwPm52GwkVy1", "MUH_1097.jpg"),
    ("1A5RpvCTS1rEvj7mi1ASkVl93DOu-dA7p", "MUH_1100.jpg"),
    ("16wuM0pvWqLwOzjUm7wvI4-W35cQyCFgf", "MUH_1108.jpg"),
    ("1MChouiyHee1-8xA5mLQCXgyG2yImRWVC", "MUH_1111.jpg"),
    ("1C59SKwkf0XEH72VwKjWwU8Ivod-Of5FZ", "MUH_1112.jpg"),
    ("1Jqlcme9wH5WDDvud_acF986-VQ8N0Q5K", "MUH_1114.jpg"),
    ("1j9S_1DG2oaLZr9f46YhX53xLHiogptFN", "MUH_1126.jpg"),
    ("1Xh9FsVRC1F-x4WyPNMIR5vr60Z9Jpr7Q", "MUH_1128.jpg"),
    ("1q0TGf1fH0CmG7EIgukwdygZ6qvIyzgOM", "MUH_1134.jpg"),
    ("10v5MKozYLdCk-pfx7XXsilaMcD-3ku3o", "MUH_1138.jpg"),
    ("10P-BOKIT9UHOxIcilJVX7DpGO4Lsrim3", "MUH_1141.jpg"),
    ("13oX6FKWrWjbVGsOFamnMqd8Dfb2cONoq", "MUH_1144.jpg"),
    ("1QbLMgXjAvZd1sr4ZJs0rPirgV-M4zxf9", "MUH_1146.jpg"),
    ("1LuBYiyKNW9wm15f1LvNbUP4ld5i4hR31", "MUH_1149.jpg"),
    ("1pbI412UHRSYkUbq72zjMe0pIT2pwADhw", "MUH_1151.jpg"),
    ("1MPaaAD-C7qI-vKA7kgB3d2vx8LXgiuYG", "MUH_1153.jpg"),
    ("1cPmfp7B8OiUd5MYm5J4vbKYSB32ruVrc", "MUH_1155.jpg"),
    ("15jWVCiWOegWyYTSLnFg1ZrOgoYeM3_-u", "MUH_1156.jpg"),
    ("19gLdjsIbs3mf4fzUvDRyNr15RUhcpekS", "MUH_1159.jpg"),
    ("14P5q2ykNEv4-qy1yp8IQzKSCIV6kkK5o", "MUH_1163.jpg"),
    ("1OgoBiZDq2UBhknQZi8X4BM7NPFs_meKw", "MUH_1165.jpg"),
    ("18_MEjfJ3nnyyT_IVheV_KMy7RR0tgLtF", "MUH_1168.jpg"),
    ("1HWfU3wQ0rxoIV6MxWedzuIM59txw2oIE", "MUH_1170.jpg"),
    ("1kEFiguZQYfcl_PJ-01dg8RqlZgvAa58q", "MUH_1173.jpg"),
    ("1lwz0CfXinhT5QQ53qo-L4RdoUVcARhau", "MUH_1174.jpg"),
    ("1X3ZvuhjWFrw-WfJEDR_vsefQx6_URy9I", "MUH_1175.jpg"),
    ("1kKnUdKSkHAShuPZqIFcYrWIA8pmw-7hk", "MUH_1178.jpg"),
    ("1Fp117qaVd_t51dkDbTgW4XAMnBecOIuB", "MUH_1187.jpg"),
    ("1b_64-SlfDvQm4Xhq-kRymHYpcON2M7uK", "MUH_1198.jpg"),
    ("1WUCEHtk4z0g1ncsoVYJncQ4H8mcp-Flu", "MUH_1208.jpg"),
    ("1QmSZfX4S0qVSrQZ4ZrX9t1wck_gkZ9FX", "MUH_1211.jpg"),
]

known_file_names = {name for _, name in known_files}
missing_from_known = known_file_names - local_files

print(f"Known files from previous scan: {len(known_files)}")
print(f"Files already downloaded: {len(local_files)}")
print(f"Files still missing: {len(missing_from_known)}")

if missing_from_known:
    print("\nMissing files from the known list:")
    for f in sorted(missing_from_known):
        print(f"  - {f}")

    # Create download script for the missing files
    with open("download_remaining_files.py", "w") as f:
        f.write("import gdown\nimport os\nimport time\n\n")
        f.write("output_dir = 'google_drive_downloads'\n")
        f.write("if not os.path.exists(output_dir):\n")
        f.write("    os.makedirs(output_dir)\n\n")
        f.write("files_to_download = [\n")

        for file_id, name in known_files:
            if name in missing_from_known:
                f.write(f'    ("{file_id}", "{name}"),\n')

        f.write("]\n\n")
        f.write("print(f'Downloading {len(files_to_download)} remaining files...')\n")
        f.write("successful = 0\n")
        f.write("failed = []\n\n")
        f.write("for i, (file_id, filename) in enumerate(files_to_download, 1):\n")
        f.write("    try:\n")
        f.write("        output_path = os.path.join(output_dir, filename)\n")
        f.write("        if os.path.exists(output_path):\n")
        f.write("            print(f'[{i}/{len(files_to_download)}] {filename} already exists, skipping...')\n")
        f.write("            successful += 1\n")
        f.write("            continue\n")
        f.write("        print(f'[{i}/{len(files_to_download)}] Downloading {filename}...', end=' ')\n")
        f.write("        url = f'https://drive.google.com/uc?id={file_id}'\n")
        f.write("        gdown.download(url, output_path, quiet=True)\n")
        f.write("        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:\n")
        f.write("            print('Success')\n")
        f.write("            successful += 1\n")
        f.write("        else:\n")
        f.write("            print('Failed (empty file)')\n")
        f.write("            failed.append(filename)\n")
        f.write("            if os.path.exists(output_path):\n")
        f.write("                os.remove(output_path)\n")
        f.write("        time.sleep(0.5)\n")
        f.write("    except Exception as e:\n")
        f.write("        print(f'Failed: {str(e)}')\n")
        f.write("        failed.append(filename)\n\n")
        f.write("print('\\n' + '='*50)\n")
        f.write("print(f'Download complete!')\n")
        f.write("print(f'Successful: {successful}/{len(files_to_download)}')\n")
        f.write("print(f'Failed: {len(failed)}/{len(files_to_download)}')\n")
        f.write("if failed:\n")
        f.write("    print('\\nFailed files:')\n")
        f.write("    for f in failed:\n")
        f.write("        print(f'  - {f}')\n")

    print("\nCreated 'download_remaining_files.py' script!")
    print("NOTE: The Google Drive folder has MORE than 50 files.")
    print("      We only have information about the first 50 files.")
    print("      To get ALL files, you may need to use the web interface.")

else:
    print("\nAll known files have been downloaded!")
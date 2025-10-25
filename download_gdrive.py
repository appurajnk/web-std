import gdown
import os

# Google Drive folder URL
folder_url = "https://drive.google.com/drive/folders/1hlWeAtOZov0ycjVMOpdTDLbE1wukqLnC"

# Create output directory if it doesn't exist
output_dir = "google_drive_downloads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    # Try to download the folder
    print(f"Attempting to download folder from: {folder_url}")
    print(f"Saving to: {output_dir}")

    # gdown can download folders that are publicly accessible
    gdown.download_folder(url=folder_url, output=output_dir, quiet=False)

    print("\nDownload completed successfully!")

    # List downloaded files
    files = os.listdir(output_dir)
    if files:
        print(f"\nDownloaded {len(files)} file(s):")
        for file in files:
            print(f"  - {file}")
    else:
        print("\nNo files were downloaded. The folder might be private or empty.")

except Exception as e:
    print(f"\nError downloading folder: {str(e)}")
    print("\nThis might be because:")
    print("1. The folder is not publicly accessible")
    print("2. The folder requires authentication")
    print("3. Google Drive has download restrictions")
    print("\nAlternative: You may need to:")
    print("- Make the folder publicly accessible (set to 'Anyone with the link can view')")
    print("- Download files manually through the browser")
    print("- Use Google Drive API with proper authentication")
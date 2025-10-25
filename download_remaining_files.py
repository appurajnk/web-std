import gdown
import os
import time

output_dir = 'google_drive_downloads'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files_to_download = [
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

print(f'Downloading {len(files_to_download)} remaining files...')
successful = 0
failed = []

for i, (file_id, filename) in enumerate(files_to_download, 1):
    try:
        output_path = os.path.join(output_dir, filename)
        if os.path.exists(output_path):
            print(f'[{i}/{len(files_to_download)}] {filename} already exists, skipping...')
            successful += 1
            continue
        print(f'[{i}/{len(files_to_download)}] Downloading {filename}...', end=' ')
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output_path, quiet=True)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print('Success')
            successful += 1
        else:
            print('Failed (empty file)')
            failed.append(filename)
            if os.path.exists(output_path):
                os.remove(output_path)
        time.sleep(0.5)
    except Exception as e:
        print(f'Failed: {str(e)}')
        failed.append(filename)

print('\n' + '='*50)
print(f'Download complete!')
print(f'Successful: {successful}/{len(files_to_download)}')
print(f'Failed: {len(failed)}/{len(files_to_download)}')
if failed:
    print('\nFailed files:')
    for f in failed:
        print(f'  - {f}')

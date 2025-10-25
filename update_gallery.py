from PIL import Image
import os
import json

# Input and output directories
input_dir = "google_drive_downloads"
output_dir = "gallery_compressed"
thumbnail_dir = "gallery_thumbnails"

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(thumbnail_dir, exist_ok=True)

# Compression settings
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
THUMBNAIL_SIZE = (400, 400)
QUALITY = 85  # JPEG quality (1-100)

# Get all jpg files
jpg_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))])

print(f"Found {len(jpg_files)} images to process")
print("="*50)

# Process each image
images_data = []
processed = 0
skipped = 0

for i, filename in enumerate(jpg_files, 1):
    try:
        # Check if already processed
        output_path = os.path.join(output_dir, filename)
        thumb_path = os.path.join(thumbnail_dir, f"thumb_{filename}")

        if os.path.exists(output_path) and os.path.exists(thumb_path):
            print(f"[{i}/{len(jpg_files)}] {filename} - Already processed, skipping...")
            skipped += 1
            # Add to data even if skipped
            images_data.append({
                "filename": filename,
                "thumbnail": f"gallery_thumbnails/thumb_{filename}",
                "full": f"google_drive_downloads/{filename}",
                "compressed": f"gallery_compressed/{filename}"
            })
            continue

        input_path = os.path.join(input_dir, filename)

        # Open the image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Get original dimensions
            orig_width, orig_height = img.size

            # Calculate new dimensions maintaining aspect ratio
            ratio = min(MAX_WIDTH/orig_width, MAX_HEIGHT/orig_height)
            if ratio < 1:  # Only resize if image is larger than max dimensions
                new_width = int(orig_width * ratio)
                new_height = int(orig_height * ratio)
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                img_resized = img

            # Save compressed image
            img_resized.save(output_path, 'JPEG', quality=QUALITY, optimize=True)

            # Create thumbnail
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img_thumb.save(thumb_path, 'JPEG', quality=80, optimize=True)

            # Add to images data
            images_data.append({
                "filename": filename,
                "thumbnail": f"gallery_thumbnails/thumb_{filename}",
                "full": f"google_drive_downloads/{filename}",
                "compressed": f"gallery_compressed/{filename}"
            })

            processed += 1
            print(f"[{i}/{len(jpg_files)}] {filename} - Processed successfully")

    except Exception as e:
        print(f"[{i}/{len(jpg_files)}] {filename} - Error: {str(e)}")

# Generate JavaScript array for the gallery
js_array = "const galleryImages = [\n"
for img in images_data:
    js_array += f"    {{ thumbnail: '{img['thumbnail']}', full: '{img['full']}', name: '{img['filename'].replace('.jpg', '')}' }},\n"
js_array = js_array.rstrip(',\n') + "\n];"

# Save the JavaScript array to a file
with open("gallery_images.js", "w") as f:
    f.write(js_array)

# Save image data as JSON
with open("gallery_data.json", "w") as f:
    json.dump(images_data, f, indent=2)

print("\n" + "="*50)
print(f"Gallery update complete!")
print(f"Total images: {len(images_data)}")
print(f"Newly processed: {processed}")
print(f"Already processed: {skipped}")
print(f"\nFiles created:")
print(f"  - gallery_images.js (JavaScript array for the website)")
print(f"  - gallery_data.json (Full metadata)")
print(f"\nTo use in your website, copy the contents of gallery_images.js")
print(f"and replace the galleryImages array in your index.html")
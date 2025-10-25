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

# Process each image
images_data = []

print("Starting image compression...")
print("="*50)

# Get all jpg files
jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))]

for i, filename in enumerate(jpg_files, 1):
    try:
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
            output_path = os.path.join(output_dir, filename)
            img_resized.save(output_path, 'JPEG', quality=QUALITY, optimize=True)

            # Create thumbnail
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            thumb_path = os.path.join(thumbnail_dir, f"thumb_{filename}")
            img_thumb.save(thumb_path, 'JPEG', quality=80, optimize=True)

            # Get file sizes
            original_size = os.path.getsize(input_path) / 1024 / 1024  # MB
            compressed_size = os.path.getsize(output_path) / 1024 / 1024  # MB
            thumb_size = os.path.getsize(thumb_path) / 1024  # KB

            # Add to images data
            images_data.append({
                "filename": filename,
                "compressed": f"gallery_compressed/{filename}",
                "thumbnail": f"gallery_thumbnails/thumb_{filename}",
                "original_size_mb": round(original_size, 2),
                "compressed_size_mb": round(compressed_size, 2),
                "reduction_percent": round((1 - compressed_size/original_size) * 100, 1)
            })

            print(f"[{i}/{len(jpg_files)}] {filename}")
            print(f"  Original: {original_size:.2f} MB -> Compressed: {compressed_size:.2f} MB")
            print(f"  Reduction: {images_data[-1]['reduction_percent']}%")
            print(f"  Thumbnail: {thumb_size:.1f} KB")

    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

# Save image data as JSON
with open("gallery_data.json", "w") as f:
    json.dump(images_data, f, indent=2)

print("\n" + "="*50)
print(f"Compression complete!")
print(f"Total images processed: {len(images_data)}")
print(f"Images saved to: {output_dir}")
print(f"Thumbnails saved to: {thumbnail_dir}")
print(f"Data saved to: gallery_data.json")

# Calculate total savings
if images_data:
    total_original = sum(img['original_size_mb'] for img in images_data)
    total_compressed = sum(img['compressed_size_mb'] for img in images_data)
    total_saved = total_original - total_compressed
    avg_reduction = sum(img['reduction_percent'] for img in images_data) / len(images_data)

    print(f"\nTotal original size: {total_original:.2f} MB")
    print(f"Total compressed size: {total_compressed:.2f} MB")
    print(f"Total saved: {total_saved:.2f} MB")
    print(f"Average reduction: {avg_reduction:.1f}%")
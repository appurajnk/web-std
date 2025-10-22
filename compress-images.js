const fs = require('fs');
const path = require('path');

// Get all JPG files in current directory
const imageFiles = [
    'IMG_0671.JPEG.jpg',
    'IMG_0672.JPEG.jpg',
    'IMG_0673.JPEG.jpg',
    'IMG_0674.JPEG.jpg',
    'IMG_0675.JPEG.jpg',
    'IMG_0676.JPEG.jpg',
    'IMG_0677.JPEG.jpg',
    'IMG_0679.JPEG.jpg',
    'IMG_0680.JPEG.jpg'
];

async function compressImages() {
    const sharp = require('sharp');

    console.log('Starting image compression...\n');
    console.log('BEFORE COMPRESSION:');
    console.log('='.repeat(60));

    let totalBefore = 0;
    const beforeSizes = {};

    // Get original sizes
    for (const file of imageFiles) {
        const stats = fs.statSync(file);
        beforeSizes[file] = stats.size;
        totalBefore += stats.size;
        console.log(`${file}: ${(stats.size / 1024 / 1024).toFixed(2)} MB (${(stats.size / 1024).toFixed(2)} KB)`);
    }

    console.log(`\nTotal size before: ${(totalBefore / 1024 / 1024).toFixed(2)} MB`);
    console.log('\n' + '='.repeat(60));
    console.log('COMPRESSING IMAGES...\n');

    // Create backup directory
    const backupDir = 'originals_backup';
    if (!fs.existsSync(backupDir)) {
        fs.mkdirSync(backupDir);
    }

    // Compress each image
    for (const file of imageFiles) {
        try {
            // Backup original
            fs.copyFileSync(file, path.join(backupDir, file));

            // Compress with sharp - quality 85 is good balance for web
            await sharp(file)
                .jpeg({
                    quality: 85,
                    progressive: true, // Progressive JPEGs load better on web
                    mozjpeg: true // Use mozjpeg for better compression
                })
                .toFile(`temp_${file}`);

            // Replace original with compressed version
            fs.unlinkSync(file);
            fs.renameSync(`temp_${file}`, file);

            console.log(`✓ Compressed ${file}`);
        } catch (error) {
            console.error(`✗ Error compressing ${file}:`, error.message);
        }
    }

    console.log('\n' + '='.repeat(60));
    console.log('AFTER COMPRESSION:');
    console.log('='.repeat(60));

    let totalAfter = 0;

    // Get new sizes and show comparison
    for (const file of imageFiles) {
        const stats = fs.statSync(file);
        totalAfter += stats.size;
        const reduction = ((1 - stats.size / beforeSizes[file]) * 100).toFixed(1);
        console.log(`${file}: ${(stats.size / 1024 / 1024).toFixed(2)} MB (${(stats.size / 1024).toFixed(2)} KB) - Reduced by ${reduction}%`);
    }

    console.log(`\nTotal size after: ${(totalAfter / 1024 / 1024).toFixed(2)} MB`);
    console.log(`Total reduction: ${((1 - totalAfter / totalBefore) * 100).toFixed(1)}%`);
    console.log(`Space saved: ${((totalBefore - totalAfter) / 1024 / 1024).toFixed(2)} MB`);
    console.log('\n' + '='.repeat(60));
    console.log(`\n✓ Compression complete! Original files backed up to: ${backupDir}/`);
}

compressImages().catch(console.error);

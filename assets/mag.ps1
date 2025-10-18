# Define the list of images, rotation degrees, and how many times to rotate
$images = @(
    @{file="block_double_adjacent.png"; degrees=90; count=4},
    @{file="block_double_opposite.png"; degrees=90; count=2},
    @{file="block_quad.png"; degrees=0; count=1},
    @{file="block_single.png"; degrees=90; count=4},
    @{file="block_solid.png"; degrees=0; count=1},
    @{file="block_triple.png"; degrees=90; count=4}
)

foreach ($img in $images) {
    $file = $img.file
    $degrees = $img.degrees
    $count = $img.count

    $base = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $ext = [System.IO.Path]::GetExtension($file)

    for ($i = 1; $i -le $count; $i++) {
        $rotation = ($degrees * ($i - 1))
        $output = "${base}_${i}${ext}"
        Write-Host "Generating $output (rotated $rotation°)"
        magick "$file" -rotate $rotation "$output"
    }
}

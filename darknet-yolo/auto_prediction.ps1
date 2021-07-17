# ===== YOUR CONFIGURATION ===================
$darknet = ".\darknet.exe"
$data = ".\config\obj.data"
$cfg = ".\config\yolov4-obj.cfg"
$weights = ".\backup\yolov4-obj_final.weights"

$test_img_dir = "C:\okamura\dataset\ダメな例_car2"
$dst_dir = ".\predictions"

$extensions = @("*.jpg", "*.png", "*.gif", "*.bmp")
# ============================================

# make destination directory.
if (-not (Test-Path $dst_dir))
{
    New-Item $dst_dir -ItemType Directory
}

Write-Host "image directory: $test_img_dir" -ForegroundColor DarkYellow

if (-not (Test-Path $test_img_dir))
{
    Write-Host "'$test_img_dir' does not exist." -ForegroundColor Red
}

# execute
$PREDICTION_IMAGE_NAME = "predictions.jpg"
Get-ChildItem $test_img_dir -File -Recurse -Include $extensions | ForEach-Object {
    Write-Output $_.FullName
    $cmd = "$darknet detector test $data $cfg $weights ${_.FullName} -dont_show"
    Invoke-Expression $cmd

    $dst_path = (Join-Path $dst_dir $_.Name)
    Move-Item $PREDICTION_IMAGE_NAME $dst_path
}

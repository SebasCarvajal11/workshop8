$root = Split-Path -Parent $PSScriptRoot
$import = Join-Path $root "product-images"
$src = Join-Path $root "assets\products"
$dst = Join-Path $root "web\public\products"

New-Item -ItemType Directory -Force -Path $import, $src, $dst | Out-Null

$py = Join-Path $root ".venv\Scripts\python.exe"
if (Test-Path $py) {
  & $py -c "from pricing_expert.catalog_media import sync_product_images; sync_product_images()"
  Write-Host "Importado desde product-images/ → assets/products y web/public/products"
}
else {
  Write-Warning "No se encontró .venv\Scripts\python.exe; copie solo assets → public."
}

Get-ChildItem $src -File | Where-Object { $_.Extension -match '\.(png|webp|avif|jpg|jpeg|svg|gif)$' } | ForEach-Object {
  Copy-Item $_.FullName (Join-Path $dst $_.Name) -Force
}
Write-Host "Sincronizado assets → web/public/products"

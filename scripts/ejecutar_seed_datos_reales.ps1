# Ejecuta seed_datos_reales_macuin.sql contra PostgreSQL (Docker o host).
# Uso desde la raíz del repo:
#   .\scripts\ejecutar_seed_datos_reales.ps1
# Opcional: puerto host si no usas el contenedor:
#   .\scripts\ejecutar_seed_datos_reales.ps1 -HostPort 5433

param(
    [string] $Container = "macuin_db",
    [int] $HostPort = 0
)

$ErrorActionPreference = "Stop"
$sql = Join-Path $PSScriptRoot "seed_datos_reales_macuin.sql"
if (-not (Test-Path $sql)) { throw "No se encuentra: $sql" }

if ($HostPort -gt 0) {
    $env:PGPASSWORD = "123456"
    & psql -h 127.0.0.1 -p $HostPort -U macuin -d DB_macuin -v ON_ERROR_STOP=1 -f $sql
} else {
    $raw = Get-Content $sql -Raw
    $raw | docker exec -i $Container psql -U macuin -d DB_macuin -v ON_ERROR_STOP=1
}

Write-Host "Listo: datos demo aplicados (idempotente en la medida de ON CONFLICT / NOT EXISTS)."

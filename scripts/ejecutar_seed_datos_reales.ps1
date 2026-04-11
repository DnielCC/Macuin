# Ejecuta un script .sql UTF-8 contra PostgreSQL (Docker o host) sin corromper tildes.
# Por defecto aplica seed_datos_reales_macuin.sql.
#
# Uso desde la raíz del repo:
#   .\scripts\ejecutar_seed_datos_reales.ps1
# Reparar textos ya guardados mal (??) por un seed antiguo en Windows:
#   .\scripts\ejecutar_seed_datos_reales.ps1 -SqlFile reparar_textos_utf8_datos_reales.sql
# Opcional: puerto host si no usas el contenedor:
#   .\scripts\ejecutar_seed_datos_reales.ps1 -HostPort 5433

param(
    [string] $Container = "macuin_db",
    [int] $HostPort = 0,
    [string] $SqlFile = "seed_datos_reales_macuin.sql"
)

$ErrorActionPreference = "Stop"
$sql = Join-Path $PSScriptRoot $SqlFile
if (-not (Test-Path $sql)) { throw "No se encuentra: $sql" }

if ($HostPort -gt 0) {
    $env:PGPASSWORD = "123456"
    $env:PGCLIENTENCODING = "UTF8"
    & psql -h 127.0.0.1 -p $HostPort -U macuin -d DB_macuin -v ON_ERROR_STOP=1 -f $sql
} else {
    # docker exec -i con tubería desde PowerShell puede alterar bytes no ASCII.
    # Copiar el archivo al contenedor y ejecutar -f dentro de Linux preserva UTF-8.
    $remotePath = "/tmp/macuin_sql_exec.sql"
    docker cp $sql "${Container}:${remotePath}"
    try {
        docker exec $Container psql -U macuin -d DB_macuin -v ON_ERROR_STOP=1 -f $remotePath
    } finally {
        docker exec $Container rm -f $remotePath 2>$null
    }
}

if ($SqlFile -eq "reparar_textos_utf8_datos_reales.sql") {
    Write-Host "Listo: textos UTF-8 corregidos en BD (reparación)."
} else {
    Write-Host "Listo: datos demo aplicados (idempotente en la medida de ON CONFLICT / NOT EXISTS)."
}

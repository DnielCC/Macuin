# Instala Database Client + JDBC en Cursor (Windows).
# Ejecutar desde PowerShell en la raíz del repo: .\scripts\instalar-database-client-cursor.ps1

$cursorCmd = Join-Path $env:LOCALAPPDATA "Programs\cursor\resources\app\bin\cursor.cmd"
if (-not (Test-Path $cursorCmd)) {
    Write-Error "No se encontró Cursor en: $cursorCmd Ajusta la ruta o instala Cursor."
    exit 1
}

& $cursorCmd --install-extension cweijan.vscode-database-client2 --force
& $cursorCmd --install-extension cweijan.dbclient-jdbc --force
Write-Host "Listo. En Cursor: Ctrl+Shift+P -> Developer: Reload Window" -ForegroundColor Green

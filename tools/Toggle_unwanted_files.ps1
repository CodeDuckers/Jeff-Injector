$steamPath = "${env:ProgramFiles(x86)}\Steam"
$gameFolder = "MarvelRivals"
$targetFiles = @('amd_fidelityfx_dx12.dll','sl.interposer.dll','sl.dlss_g.dll','sl.reflex.dll')
# ,'QtWebEngineProcess.exe'

# Parse libraryfolders.vdf to get all Steam libraries
$libraryPaths = @()
$libraryPaths += Join-Path $steamPath "steamapps"

$vdfPath = Join-Path $steamPath "steamapps\libraryfolders.vdf"
if (-not (Test-Path $vdfPath)) {
    Write-Error "Could not find Steam libraryfolders.vdf at $vdfPath"
    exit 1
}

$content = Get-Content $vdfPath
foreach ($line in $content) {
    if ($line -match '"path"\s+"([^"]+)"') {
        $path = $matches[1]
        if ($path -ne $steamPath) {
            $libraryPaths += Join-Path $path "steamapps"
        }
    }
}

# Find the game install path
$installPath = $null
foreach ($lib in $libraryPaths) {
    $testPath = Join-Path $lib "common\$gameFolder"
    if (Test-Path $testPath) {
        $installPath = $testPath
        break
    }
}

if (-not $installPath) {
    Write-Error "Could not find $gameFolder in any Steam library folders."
    exit 1
}

Write-Output "Detected install path: '$installPath'"

# Find files and rename
Get-ChildItem -Path $installPath -Recurse -File | Where-Object {
    ($targetFiles -contains $_.Name) -or
    $_.Name -like '*.dll.D' -or
    $_.Name -like '*.exe.D'
} | ForEach-Object {
    $file = $_
    $name = [IO.Path]::GetFileNameWithoutExtension($file.Name)
    $ext = [IO.Path]::GetExtension($file.Name)

    if ($ext -ieq ".D") {
        $newName = $name
    } else {
        $newName = $file.Name + ".D"
    }

    $newPath = Join-Path $file.DirectoryName $newName
    Write-Output "Renaming '$($file.FullName)' to '$newPath'"
    try {
        Rename-Item -Path $file.FullName -NewName $newName -ErrorAction Stop
    } catch {
        Write-Warning "Failed to rename '$($file.FullName)': $_"
    }
}

Add-Type -AssemblyName System.Windows.Forms

# Create OpenFileDialog for file selection
$fileDialog = New-Object System.Windows.Forms.OpenFileDialog
$fileDialog.Title = "Wybierz pliki CSV"
$fileDialog.Filter = "Pliki CSV (*.csv)|*.csv"
$fileDialog.Multiselect = $true
$fileDialog.InitialDirectory = [Environment]::GetFolderPath('MyDocuments')

# Show dialog and check if user selected files
$result = $fileDialog.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::Cancel -or $fileDialog.FileNames.Count -eq 0) {
    Write-Host "Nie wybrano żadnych plików."
    return
}

# Get selected files
$files = $fileDialog.FileNames

# Process each selected file
foreach ($filename in $files) {
    $extension = [System.IO.Path]::GetExtension($filename)
    
    if ($extension -eq ".csv") {
        try {
            # Read all lines from the file
            $rawLines = Get-Content -Path $filename -Encoding UTF8
            
            # Replace commas with semicolons
            $modifiedLines = $rawLines -replace ",", ";"
            
            # Write back to the file
            $modifiedLines | Set-Content -Path $filename -Encoding UTF8
            
            Write-Host "Przetworzono: $filename"
        }
        catch {
            Write-Host "Błąd podczas przetwarzania pliku: $filename" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
    else {
        Write-Host "Wybrane pliki nie są typu CSV."
        return
    }
}

Write-Host "Gotowe." -ForegroundColor Green

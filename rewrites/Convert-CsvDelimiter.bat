@echo off
setlocal enabledelayedexpansion

REM CSV Delimiter Converter - Converts comma-delimited CSV files to semicolon-delimited

echo ========================================
echo CSV Delimiter Converter
echo ========================================
echo.

REM Check if files were provided as arguments
if "%~1"=="" (
    echo Użycie: Przeciągnij pliki CSV na ten skrypt
    echo         lub uruchom: %~nx0 plik1.csv plik2.csv ...
    echo.
    pause
    exit /b 1
)

set "fileCount=0"
set "processedCount=0"

REM Process each file passed as argument
:processFiles
if "%~1"=="" goto done

set "filename=%~1"
set "extension=%~x1"

REM Check if file has .csv extension
if /i not "!extension!"==".csv" (
    echo [BŁĄD] Plik !filename! nie jest typu CSV.
    shift
    goto processFiles
)

REM Check if file exists
if not exist "!filename!" (
    echo [BŁĄD] Plik nie istnieje: !filename!
    shift
    goto processFiles
)

set /a fileCount+=1

REM Create temporary file
set "tempFile=!filename!.tmp"

REM Process the file line by line, replacing commas with semicolons
(
    for /f "usebackq delims=" %%a in ("!filename!") do (
        set "line=%%a"
        set "line=!line:,=;!"
        echo !line!
    )
) > "!tempFile!"

REM Replace original file with modified content
if exist "!tempFile!" (
    move /y "!tempFile!" "!filename!" >nul
    if !errorlevel! equ 0 (
        echo [OK] Przetworzono: !filename!
        set /a processedCount+=1
    ) else (
        echo [BŁĄD] Nie można zapisać pliku: !filename!
        del "!tempFile!" 2>nul
    )
) else (
    echo [BŁĄD] Nie można przetworzyć pliku: !filename!
)

shift
goto processFiles

:done
echo.
echo ========================================
echo Gotowe.
echo Przetworzono !processedCount! z !fileCount! plików.
echo ========================================
pause

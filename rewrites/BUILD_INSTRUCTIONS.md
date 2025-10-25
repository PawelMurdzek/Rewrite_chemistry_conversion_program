# CSV Delimiter Converter - Build Instructions

## Quick Start - Create EXE file

### Step 1: Install PyInstaller
Open PowerShell in the `rewrites` folder and run:
```powershell
pip install pyinstaller
```

### Step 2: Build the EXE
Run one of these commands:

**Option A - Single EXE file (recommended):**
```powershell
pyinstaller --onefile --windowed --name "CSV-Delimiter-Converter" --icon=NONE convert_csv_delimiter.py
```

**Option B - With folder (faster startup):**
```powershell
pyinstaller --windowed --name "CSV-Delimiter-Converter" --icon=NONE convert_csv_delimiter.py
```

### Step 3: Find your EXE
The executable will be in: `dist\CSV-Delimiter-Converter.exe`

## Usage
1. Double-click the EXE file
2. Select one or multiple CSV files
3. The program will convert commas to semicolons
4. You'll see a "Gotowe" message when complete

## Options Explained
- `--onefile`: Creates a single EXE file (easier to distribute)
- `--windowed`: No console window appears (GUI only)
- `--name`: Name of the output executable
- `--icon=NONE`: No custom icon (you can add one if you want)

## Optional: Add Custom Icon
If you have an `.ico` file, replace `--icon=NONE` with:
```powershell
--icon="path\to\your\icon.ico"
```

## Clean Build
To rebuild from scratch:
```powershell
rmdir dist, build -Recurse -Force
del *.spec
pyinstaller --onefile --windowed --name "CSV-Delimiter-Converter" convert_csv_delimiter.py
```

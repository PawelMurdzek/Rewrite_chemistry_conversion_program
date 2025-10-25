"""
CSV Delimiter Converter with Column Filtering - Converts comma-delimited CSV files to semicolon-delimited
and filters columns based on Action Name
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import csv


def convert_csv_files():
    """Main function to select and convert CSV files with column filtering"""
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # Open file dialog for selecting multiple CSV files
    files = filedialog.askopenfilenames(
        title="Wybierz pliki CSV",
        filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")],
        parent=root
    )
    
    # Check if user selected any files
    if not files:
        messagebox.showinfo("Info", "Nie wybrano żadnych plików.", parent=root)
        root.destroy()
        return
    
    processed_count = 0
    error_count = 0
    error_messages = []
    converted_files = []
    
    # Process each selected file
    for filename in files:
        # Check file extension
        _, extension = os.path.splitext(filename)
        
        if extension.lower() != '.csv':
            messagebox.showerror(
                "Błąd", 
                "Wybrane pliki nie są typu CSV.",
                parent=root
            )
            root.destroy()
            return
        
        try:
            # Read file content
            with open(filename, 'r', encoding='utf-8-sig') as file:
                # Use csv reader to properly parse the file
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                rows = list(reader)
            
            if not headers or not rows:
                error_count += 1
                error_messages.append(f"{os.path.basename(filename)}: Plik jest pusty")
                continue
            
            # Check if required columns exist
            if 'Action Name' not in headers:
                error_count += 1
                error_messages.append(f"{os.path.basename(filename)}: Brak kolumny 'Action Name'")
                continue
            
            # Determine which columns to keep based on Action Name
            action_name_sample = rows[0].get('Action Name', '') if rows else ''
            
            # Base columns to always keep
            base_columns = ['Point Index', 'Sample Description', 'Action Name']
            
            # Additional columns based on Action Name
            if 'Viscometry Shear rate ramp' in action_name_sample:
                additional_columns = [
                    'Shear stress(Pa)',
                    'Shear rate(s-¹)',
                    'Shear viscosity(Pa s)'
                ]
            elif 'Oscillation amplitude table' in action_name_sample:
                additional_columns = [
                    'Complex shear strain(%)',
                    'Complex shear stress(Pa)',
                    'Shear modulus (elastic component)(Pa)',
                    'Shear modulus (viscous component)(Pa)'
                ]
            else:
                # If no match, keep all columns
                additional_columns = [col for col in headers if col not in base_columns]
            
            # Create ordered list of columns to keep (in original order)
            columns_to_keep = []
            for col in headers:
                if col in base_columns or col in additional_columns:
                    columns_to_keep.append(col)
            
            # Filter rows to keep only selected columns
            filtered_rows = []
            for row in rows:
                filtered_row = {col: row.get(col, '') for col in columns_to_keep}
                filtered_rows.append(filtered_row)
            
            # Create new filename with _converted suffix
            base_name = os.path.splitext(filename)[0]
            new_filename = f"{base_name}_converted.csv"
            
            # Write to new file with semicolon delimiter and comma as decimal separator
            with open(new_filename, 'w', encoding='utf-8-sig', newline='') as file:
                # Manually write the file to control delimiter and decimal separator
                # Write header
                header_line = ';'.join(columns_to_keep) + '\n'
                file.write(header_line)
                
                # Write data rows
                for row in filtered_rows:
                    values = []
                    for col in columns_to_keep:
                        value = row.get(col, '')
                        # Replace decimal point with comma
                        value = value.replace('.', ',')
                        values.append(value)
                    line = ';'.join(values) + '\n'
                    file.write(line)
            
            # Verify file was created
            if os.path.exists(new_filename):
                converted_files.append(new_filename)
                processed_count += 1
            else:
                error_count += 1
                error_messages.append(f"{os.path.basename(filename)}: Plik nie został utworzony")
            
        except Exception as e:
            error_count += 1
            error_messages.append(f"{os.path.basename(filename)}: {str(e)}")
    
    # Show completion message with file locations
    if error_count > 0:
        message = f"Przetworzono {processed_count} plików.\n\n"
        message += f"Błędy ({error_count}):\n" + "\n".join(error_messages)
        messagebox.showwarning("Zakończono z błędami", message, parent=root)
    else:
        # Show list of converted files with their locations
        if converted_files:
            folder = os.path.dirname(converted_files[0])
            message = f"Gotowe! Przetworzono {processed_count} plików.\n\n"
            message += f"Lokalizacja: {folder}\n\n"
            message += "Pliki:\n"
            for f in converted_files:
                message += f"• {os.path.basename(f)}\n"
            messagebox.showinfo("Gotowe", message, parent=root)
        else:
            messagebox.showinfo(
                "Gotowe", 
                f"Gotowe.\nPrzetworzono {processed_count} plików.",
                parent=root
            )
    
    root.destroy()


if __name__ == "__main__":
    try:
        convert_csv_files()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Błąd krytyczny", f"Wystąpił nieoczekiwany błąd:\n{str(e)}")
        root.destroy()
        sys.exit(1)

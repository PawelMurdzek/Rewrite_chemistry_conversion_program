"""
CSV Delimiter Converter - Converts comma-delimited CSV files to semicolon-delimited
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys


def convert_csv_files():
    """Main function to select and convert CSV files"""
    
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
                raw_lines = file.readlines()
            
            # Replace commas with semicolons
            modified_lines = [line.replace(',', ';') for line in raw_lines]
            
            # Write back to file
            with open(filename, 'w', encoding='utf-8-sig') as file:
                file.writelines(modified_lines)
            
            processed_count += 1
            
        except Exception as e:
            error_count += 1
            error_messages.append(f"{os.path.basename(filename)}: {str(e)}")
    
    # Show completion message
    if error_count > 0:
        message = f"Przetworzono {processed_count} plików.\n\n"
        message += f"Błędy ({error_count}):\n" + "\n".join(error_messages)
        messagebox.showwarning("Zakończono z błędami", message, parent=root)
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

import os
from pathlib import Path
from collections import defaultdict
from tkinter import Tk
from tkinter.filedialog import askdirectory
import shutil

def Choose_path_to_dir_windows():
    root = Tk() #tworzy okno
    root.withdraw() #ukrywa okno?
    path = askdirectory(title="Choose Folder to read and sort")
    root.destroy() #niszczy okno po wyborze
    return path

def Read_files_classic(path):
    if os.path.isdir(path):
        Stored_files = defaultdict(list)

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            if os.path.isfile(file_path):
                file_type = os.path.splitext(file)[1].lower()
                Stored_files[file_type].append(file)

        return Stored_files
    else:
        print("Ten path nie istnieje")

def Read_files_pathlib(path):
    folder_to_scan = Path(path)
    if not folder_to_scan.is_dir():
        print("Unknown Path")
        return None
    
    Stored_files = defaultdict(list)

    for file in folder_to_scan.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            Stored_files[file_extension].append(file)
    
    if not Stored_files:  
        print("No files to read and sort")
        return None
    
    return Stored_files

def Create_dirs_for_types(Files,path):
    for type, names in Files.items():
        
        directory_name = type.strip(".") + " Folder" if type else "No extension Files" #makes folder named by type of scanned file previously
        try:

            os.mkdir(os.path.join(path, directory_name))
            print(f"Directory '{directory_name}' created successfully.")


        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    return 0

def Move_files_to_folders(Files, path):
    for types, names in Files.items():
        folder_name = types.strip('.') + " Folder" if types else "No extension Files"
        destination_path = os.path.join(path,folder_name)
        
        for name in names:
            name_path = os.path.join(path, name)
            try:
                shutil.move(name_path, destination_path)
                print(f"Moved file '{name}' to '{folder_name}'")
            except FileNotFoundError:
                print(f"File '{name}' not found. Skipping...")
            except PermissionError:
                print(f"Permission denied for file '{name}'. Skipping...")
            except Exception as e:
                print(f"An error occurred while moving '{name}': {e}")
    
    return 0
    

path = Choose_path_to_dir_windows()

if path:
    
    #Files = zczytywanie_Plikow_classic(path)
    Files_Pathlib = Read_files_pathlib(path)
    '''
    if Files:
        """for typ, lista in Files.items():
            
            print(f"FileType: [{typ if typ else 'Brak rozszerzenia'}]")
            print(f"Pliki: ({', '.join(lista)})\n")"""
        Create_dirs_for_types(Files, path)
        Move_files_to_folders(Files, path)'''

    

    if Files_Pathlib:
        '''for typ, lista in Files.items():
            print(f"FileType: [{typ if typ else 'Brak rozszerzenia'}]")
            print(f"Pliki:\n({', '.join(lista)})\n")'''
        Create_dirs_for_types(Files_Pathlib, path)
        Move_files_to_folders(Files_Pathlib, path)
else:
    print("No Directory was chosen")
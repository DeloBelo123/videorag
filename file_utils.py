from pathlib import Path
import subprocess
import shutil

#creating and reading
def create_file(file,content):
    pfad = Path(file)
    pfad.write_text(content)
    print(f"die Datei: '{file}' wurde erstellt ")
    return pfad
    
def create_sub_file(path,content):
    pfad = Path(path)
    pfad.parent.mkdir(exist_ok=True,parents=True)
    pfad.write_text(content)
    print(f"der Tree: '{path}' wurde erstellt ")
    return pfad
    
def read_file(file):
    pfad = Path(file)
    if not pfad.is_absolute():
        project_root = Path(__file__).parent.parent.parent
        pfad = project_root / file
        if not pfad.exists():
            pfad = Path(file)
    if not pfad.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {file}")
    
    pfad_inhalt = pfad.read_text(encoding="utf-8")
    print(f"die Datei: '{pfad}' wurde ausgelesen")
    return pfad_inhalt

def read_all_files_in_dir(dir):
    ordner = Path(__file__).parent / dir
    dateien_inhalt = []
    for file in ordner.rglob("*"):
        if file.is_file():
            pfad = Path(file)
            pfad_inhalt = pfad.read_text()
            print(f"die Datei: '{file}' wurde ausgelesen")
            dateien_inhalt.append(pfad_inhalt)
    print(f"der ordner: {dir} wurde vollständig ausgelesen")
    return dateien_inhalt


def read_file_lines(file):
    pfad = Path(file)
    pfad_lines = pfad.read_text().splitlines()
    print(f"die Datei: '{file}' wurde Zeile für Zeile ausgelesen und in ein array gepackt")
    return pfad_lines

def add_to_file(file,content):
    pfad = Path(file)
    with pfad.open("a",encoding="utf-8") as f:
        f.write(f"\n{content}")
    print(f"in Datei: '{file}' wurde Inhalt: '{content}' hinzugefügt")
    return pfad
    
def does_file_exist(file):
    pfad = Path(file)
    existing = pfad.exists()
    if existing:
        print(f"die Datei: '{file}' exestiert")
    else:
        print(f"die Datei: '{file}' exestiert nicht")
    return existing
    
#running code  
def write_n_run(file,content,interpreter,is_subfile=False,aus_führen=False):
    path = Path(file)
    if is_subfile:
        path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(content)
    print(f"der {interpreter} Code-Datei: '{file}' wurde erstellt")
    if aus_führen:
        subprocess.run([interpreter,str(file)])
        print(f"die {interpreter} Code-Datei: '{file}' wird ausgeführt")
    return path
    
def write_n_run_py(file,content,is_subfile=False,aus_führen=False):
    write_n_run(
        file=file,
        content=content,
        is_subfile=is_subfile,
        interpreter="python3",
        aus_führen=aus_führen)

def write_n_run_js(file,content,is_subfile=False,aus_führen=False):
    write_n_run(
        file=file,
        content=content,
        is_subfile=is_subfile,
        interpreter="node",
        aus_führen=aus_führen)

#removing   
def remove_file(file):
    pfad = Path(file)
    if pfad.exists():
        print(f"die Datei:'{file}' wurde gelöscht'")
        pfad.unlink()
    
def remove_empty_dir(dir):
    dir = Path(dir)
    if dir.exists() and dir.is_dir():
        print(f"der leere Ordner:'{dir}' wird entfernt")
        dir.rmdir()
        
def kill_tree(dir):
    ordner = Path(dir)
    if ordner.exists():
        while True:
            user_bestätigung = input(f"wollen sie den ordner:'{dir}' und somit den gesammten inhalt von ihm löschen?. Nicht rückgängbar Y/n ")
            if user_bestätigung.lower() == "y":
                print("gesammter Baum wurde gelöscht")
                shutil.rmtree(dir)
                break
            elif user_bestätigung.lower() == "n":
                print(f"'{dir}' löschvorgang wurde abgebrochen ")
                break
            else:
                print("falsche eingabe, sie müssen entweder: 'Y/y' für 'Yes' oder 'N/n' für 'No' eingeben")
    else:
        print(f"der Ordner: '{dir}' exestiert nicht, somit kann auch nichts gelöscht werden")
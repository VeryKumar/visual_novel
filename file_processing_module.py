from pathlib import Path

def write_to_file_in_folder(folder_name, file_name, data):
    parent_path = Path("stories/")
    normalized_folder_name = folder_name.replace(" ", "_")
    folder_path = parent_path / normalized_folder_name
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / f"{file_name}.txt"
    
    with file_path.open('w') as file:
        file.write(data)
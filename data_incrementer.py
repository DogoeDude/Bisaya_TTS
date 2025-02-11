import os

folder_path = "custom_data" 

i = 31

files = sorted(f for f in os.listdir(folder_path) if f[:2].isdigit())

for file in files:
    parts = file.split("_", 1) 
    if len(parts) < 2:
        continue  

    new_name = f"{i:03d}_{parts[1]}"
    old_path = os.path.join(folder_path, file)
    new_path = os.path.join(folder_path, new_name)

    os.rename(old_path, new_path)
    i += 1 

print("Files renamed successfully!")

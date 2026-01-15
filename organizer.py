import os
import shutil
from datetime import datetime

FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"]
}

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def scan_directory(path):
    files_data = []

    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path) / 1024  # KB
            modified = datetime.fromtimestamp(os.path.getmtime(full_path))
            ext = os.path.splitext(file)[1]
            category = get_category(ext)

            files_data.append({
                "name": file,
                "size": size,
                "modified": modified,
                "category": category
            })

    return files_data

def generate_report(files_data):
    print("\nFILE ANALYSIS REPORT\n")
    summary = {}

    for file in files_data:
        summary[file["category"]] = summary.get(file["category"], 0) + 1

    for category, count in summary.items():
        print(f"{category}: {count} files")

    total_size = sum(f["size"] for f in files_data)
    print(f"\nTotal files: {len(files_data)}")
    print(f"Total size: {total_size:.2f} KB")

def organize_files(path, files_data):
    for file in files_data:
        category_folder = os.path.join(path, file["category"])
        os.makedirs(category_folder, exist_ok=True)

        src = os.path.join(path, file["name"])
        dst = os.path.join(category_folder, file["name"])
        shutil.move(src, dst)

def main():
    print("\nIntelligent File Organizer\n")
    path = input("Enter directory path to scan: ").strip()

    if not os.path.isdir(path):
        print("Invalid directory path")
        return

    files_data = scan_directory(path)

    if not files_data:
        print("No files found.")
        return

    generate_report(files_data)

    choice = input("\nDo you want to organize files into folders? (yes/no): ").lower()
    if choice == "yes":
        organize_files(path, files_data)
        print(" Files organized successfully.")
    else:
        print("ℹNo changes made.")

if __name__ == "__main__":
    main()

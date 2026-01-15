import os
import shutil
import csv
from datetime import datetime

FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"]
}

LARGE_FILE_KB = 5000 

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def scan_directory(path):
    files = []
    size_map = {}

    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if not os.path.isfile(full_path):
            continue

        size_kb = os.path.getsize(full_path) / 1024
        modified = datetime.fromtimestamp(os.path.getmtime(full_path))
        ext = os.path.splitext(file)[1]
        category = get_category(ext)

        duplicate = size_map.get(size_kb, False)
        size_map[size_kb] = True

        files.append({
            "name": file,
            "size": size_kb,
            "modified": modified.strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "large": size_kb > LARGE_FILE_KB,
            "duplicate": duplicate
        })

    return files

def generate_report(files):
    print("\n FILE ANALYSIS REPORT\n")

    summary = {}
    for f in files:
        summary[f["category"]] = summary.get(f["category"], 0) + 1

    for cat, count in summary.items():
        print(f"{cat}: {count} files")

    large_files = [f for f in files if f["large"]]
    duplicates = [f for f in files if f["duplicate"]]

    print(f"\nLarge files (>5MB): {len(large_files)}")
    print(f"Potential duplicates: {len(duplicates)}")

def export_csv(files):
    with open("file_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "File Name", "Category", "Size (KB)",
            "Last Modified", "Large File", "Duplicate"
        ])

        for file in files:
            writer.writerow([
                file["name"], file["category"],
                f"{file['size']:.2f}",
                file["modified"],
                file["large"],
                file["duplicate"]
            ])

    print(" CSV report generated: file_report.csv")

def organize_files(path, files, dry_run):
    for f in files:
        category_folder = os.path.join(path, f["category"])
        src = os.path.join(path, f["name"])
        dst = os.path.join(category_folder, f["name"])

        if dry_run:
            print(f"[DRY-RUN] {f['name']} → {f['category']}/")
        else:
            os.makedirs(category_folder, exist_ok=True)
            shutil.move(src, dst)

def main():
    print("\n Intelligent File Organizer v2\n")
    path = input("Enter directory path: ").strip()

    if not os.path.isdir(path):
        print("Invalid directory path")
        return

    files = scan_directory(path)

    if not files:
        print("No files found.")
        return

    generate_report(files)
    export_csv(files)

    dry = input("\nEnable dry-run mode? (yes/no): ").lower() == "yes"
    confirm = input("Organize files now? (yes/no): ").lower()

    if confirm == "yes":
        organize_files(path, files, dry)
        print(" Operation completed.")
    else:
        print("No files were modified.")

if __name__ == "__main__":
    main()

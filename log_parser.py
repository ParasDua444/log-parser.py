import os
from pathlib import Path
from datetime import datetime

KEYWORDS = ["ERROR", "ADMIN"]

def read_log_file(file_path):
    lines = []
    with file_path.open("r", encoding="utf-8", erros="replace") as f:
        for line in f:
            if line.strip():
                lines.append(line.rstrip("\n"))
    return lines

def search_keywords(lines):
    results = {"Error: " : [], "Admin: " : []}
    for number, line in enumerate(lines, start=1):
        for keyword in KEYWORDS:
            if keyword.lower() in line.lower():
                results[keyword].append((number, line))
    return results

def build_report(file_path, results):
    now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    size  = os.path.getsize(file_path)
    lines = []

    lines.append("=" * 60)
    lines.append("LOG FILE PARSER — REPORT")
    lines.append(f"File: {file_path.resolve()}")
    lines.append(f"Size: {size} bytes")
    lines.append(f"Generated: {now}")
    lines.append("=" * 60)

    for keyword in KEYWORDS:
        matches = results[keyword]
        lines.append(f"\nKeyword: \"{keyword}\" — {len(matches)} matches")
        lines.append("-" * 60)
        if matches:
            for number, line in matches:
                lines.append(f"Line {number:<5}: {line[:70]}")
        else:
            lines.append("No matches found.")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def save_report(report, output_path):
    with output_path.open("w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved -> {output_path.resolve()}")

def main():
    print("\nLOG FILE PARSER")
    print("Searches for: Error, Admin\n")
 
    raw = input("Enter log file path: ").strip()
    file_path = Path(raw).expanduser()
 
    if not file_path.is_file():
        print(f"[!] File not found: {file_path}")
        return
 
    lines = read_log_file(file_path)
    results = search_keywords(lines)
    report = build_report(file_path, results)
 
    print()
    print(report)
 
    save = input("\nSave report to file? (y/n): ").strip().lower()
    if save == "y":
        out_path = file_path.parent / "report.txt"
        save_report(report, out_path)


if __name__ == "__main__":
    main()

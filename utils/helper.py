from pathlib import Path

def check_file_extension(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return "PDF"
    elif ext in ['.jpg', '.jpeg', '.png']:
        return "image"
    return "unknown"

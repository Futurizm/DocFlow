import easyocr
import sys
import json
import os

# Ensure UTF-8 encoding for stdout on Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

def main(file_paths):
    try:
        # Initialize EasyOCR Reader for Russian and English
        reader = easyocr.Reader(['ru', 'en'], gpu=False)  # Set gpu=True for CUDA
        results = []
        for file_path in file_paths:
            try:
                # Extract text
                text_lines = reader.readtext(file_path, paragraph=True, detail=0)
                text = "\n".join(text_lines)
                # Log raw text for debugging
                print(f"Raw OCR text for {file_path}: {text}", file=sys.stderr)
                results.append({"success": True, "text": text})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        # Output JSON with proper Unicode
        print(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        print(json.dumps([{"success": False, "error": f"Failed to initialize EasyOCR: {str(e)}"}], ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps([{"success": False, "error": "File path required"}], ensure_ascii=False))
        sys.exit(1)
    main(sys.argv[1:])
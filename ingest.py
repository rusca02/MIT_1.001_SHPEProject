# ingest.py
import os
import glob
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import docx

def read_txt(path):
    """Read a text file and return its content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    """
    Extract text from a PDF using a three-step approach:
      1. Use pdfplumber to extract text.
      2. For pages with insufficient text, use pdf2image to convert the page to an image and perform OCR.
      3. If still insufficient, fall back to using PyMuPDF (fitz) to render the page and run OCR.
    
    Returns:
        A string containing the extracted text from all pages.
    """
    full_text = ""
    extraction_success = False

    # Step 1: Try pdfplumber extraction
    try:
        print(f"[INFO] Opening PDF with pdfplumber: {path}")
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text and len(page_text.strip()) > 20:
                    print(f"[INFO] Page {i}: extracted {len(page_text)} characters via pdfplumber.")
                    full_text += page_text + "\n"
                    extraction_success = True
                else:
                    print(f"[WARN] Page {i}: insufficient text via pdfplumber; trying OCR with pdf2image.")
                    try:
                        images = convert_from_path(path, dpi=300, first_page=i, last_page=i)
                        if images:
                            ocr_text = pytesseract.image_to_string(images[0])
                            if ocr_text and len(ocr_text.strip()) > 10:
                                print(f"[INFO] Page {i}: OCR (pdf2image) extracted {len(ocr_text)} characters.")
                                full_text += ocr_text + "\n"
                                extraction_success = True
                            else:
                                print(f"[WARN] Page {i}: OCR via pdf2image returned insufficient text.")
                        else:
                            print(f"[ERROR] Page {i}: No image returned via pdf2image.")
                    except Exception as ocr_err:
                        print(f"[ERROR] Page {i}: OCR with pdf2image failed: {ocr_err}")
        if full_text.strip():
            print("[INFO] Extraction via pdfplumber (with pdf2image fallback) succeeded.")
            return full_text
        else:
            print("[WARN] pdfplumber and pdf2image OCR did not extract any text; trying PyMuPDF fallback.")
    except Exception as e:
        print(f"[ERROR] pdfplumber extraction error for {os.path.basename(path)}: {e}")

    # Step 3: Fall back to PyMuPDF (fitz) for OCR
    try:
        import fitz  # PyMuPDF
        print(f"[INFO] Opening PDF with PyMuPDF (fitz): {path}")
        doc = fitz.open(path)
        for i, page in enumerate(doc, start=1):
            try:
                pix = page.get_pixmap(dpi=300)
                from io import BytesIO
                img = Image.open(BytesIO(pix.tobytes("png")))
                ocr_text = pytesseract.image_to_string(img)
                if ocr_text and len(ocr_text.strip()) > 10:
                    print(f"[INFO] Page {i}: OCR (PyMuPDF fallback) extracted {len(ocr_text)} characters.")
                    full_text += ocr_text + "\n"
                    extraction_success = True
                else:
                    print(f"[WARN] Page {i}: OCR (PyMuPDF fallback) returned insufficient text.")
            except Exception as page_err:
                print(f"[ERROR] Page {i}: PyMuPDF OCR extraction failed: {page_err}")
        if extraction_success:
            print("[INFO] Extraction via PyMuPDF fallback succeeded.")
            return full_text
        else:
            print(f"[ERROR] No text extracted from {os.path.basename(path)} by any method.")
    except Exception as e:
        print(f"[ERROR] PyMuPDF extraction failed for {os.path.basename(path)}: {e}")
    
    return full_text

def read_docx(path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(path)
        text = "\n".join(para.text for para in doc.paragraphs)
        print(f"[INFO] Extracted DOCX text from {os.path.basename(path)}")
        return text
    except Exception as e:
        print(f"[ERROR] Failed to extract DOCX text from {os.path.basename(path)}: {e}")
        return ""

def read_image(path):
    """Extract text from an image using OCR."""
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        print(f"[INFO] OCR extraction complete for image {os.path.basename(path)}")
        return text
    except Exception as e:
        print(f"[ERROR] OCR extraction failed for image {os.path.basename(path)}: {e}")
        return ""

def load_documents(data_dir="./data"):
    """
    Loads documents from the specified directory.
    Supported file types: TXT, PDF, DOCX, PNG/JPG/JPEG.
    
    Returns:
        A list of dictionaries with keys 'filename' and 'text'.
    """
    files = glob.glob(os.path.join(data_dir, "*"))
    docs = []
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        filename = os.path.basename(path)
        try:
            if ext == ".txt":
                text = read_txt(path)
            elif ext == ".pdf":
                text = read_pdf(path)
            elif ext == ".docx":
                text = read_docx(path)
            elif ext in [".png", ".jpg", ".jpeg"]:
                text = read_image(path)
            else:
                print(f"[WARN] Unsupported file type for {filename}; skipping.")
                continue
            docs.append({"filename": filename, "text": text})
        except Exception as e:
            print(f"[ERROR] Error processing {filename}: {e}")
    return docs

if __name__ == "__main__":
    documents = load_documents()
    print(f"\n[SUMMARY] Loaded {len(documents)} document(s).\n")
    for doc in documents:
        print(f"Filename: {doc['filename']}")
        print("Content Preview (first 500 characters):")
        preview = doc['text'][:500] + ("..." if len(doc['text']) > 500 else "")
        print(preview + "\n")

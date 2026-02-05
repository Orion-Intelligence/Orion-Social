import os
from pathlib import Path
from typing import Dict, Any
import fitz
import pytesseract
from PIL import Image
from .ioc_enums import IOC_FILE_TYPES, IOC_EXTRACTION_STATUS



class IOCExtractor:


    SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg'}
    SUPPORTED_TEXT_FORMATS = {'.txt'}
    SUPPORTED_PDF_FORMATS = {'.pdf'}

    MAX_CHARACTERS = 15000
    PDF_MAX_PAGES = 4

    def __init__(self):

        pass

    def extract_text_from_image(self, file_path: str) -> str:

        try:
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")

    def extract_text_from_pdf(self, file_path: str) -> str:

        try:
            text_chunks = []

            with fitz.open(file_path) as doc:
                max_pages = min(self.PDF_MAX_PAGES, doc.page_count)

                for page_number in range(max_pages):
                    page = doc.load_page(page_number)
                    text_chunks.append(page.get_text("text"))

            return "\n".join(text_chunks)

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def extract_text_from_text_file(self, file_path: str) -> str:

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")

    def detect_file_type(self, file_path: str) -> str:

        extension = Path(file_path).suffix.lower()

        if extension in self.SUPPORTED_PDF_FORMATS:
            return IOC_FILE_TYPES.PDF
        elif extension in self.SUPPORTED_IMAGE_FORMATS:
            return IOC_FILE_TYPES.IMAGE
        elif extension in self.SUPPORTED_TEXT_FORMATS:
            return IOC_FILE_TYPES.TEXT
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    def truncate_text(self, text: str) -> str:

        return text[:self.MAX_CHARACTERS]

    def extract_text(self, file_path: str) -> Dict[str, Any]:

        try:
            if not os.path.exists(file_path):
                return {
                    "filename": file_path,
                    "file_type": IOC_FILE_TYPES.UNKNOWN,
                    "extracted_text": "",
                    "extracted_text_length": 0,
                    "status": IOC_EXTRACTION_STATUS.ERROR,
                    "error_message": "File not found"
                }

            filename = os.path.basename(file_path)
            file_type = self.detect_file_type(file_path)

            if file_type == IOC_FILE_TYPES.PDF:
                extracted_text = self.extract_text_from_pdf(file_path)
            elif file_type == IOC_FILE_TYPES.IMAGE:
                extracted_text = self.extract_text_from_image(file_path)
            elif file_type == IOC_FILE_TYPES.TEXT:
                extracted_text = self.extract_text_from_text_file(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            truncated_text = self.truncate_text(extracted_text)

            if not truncated_text.strip():
                return {
                    "filename": filename,
                    "file_type": file_type,
                    "extracted_text": "",
                    "extracted_text_length": 0,
                    "status": IOC_EXTRACTION_STATUS.WARNING,
                    "error_message": "No text extracted from file"
                }

            return {
                "filename": filename,
                "file_type": file_type,
                "extracted_text": truncated_text,
                "extracted_text_length": len(truncated_text),
                "status": IOC_EXTRACTION_STATUS.SUCCESS
            }

        except Exception as e:
            return {
                "filename": os.path.basename(file_path) if file_path else "unknown",
                "file_type": IOC_FILE_TYPES.UNKNOWN,
                "extracted_text": "",
                "extracted_text_length": 0,
                "status": IOC_EXTRACTION_STATUS.ERROR,
                "error_message": str(e)
            }

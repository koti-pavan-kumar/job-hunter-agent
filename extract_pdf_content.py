"""
Extract content from PDF files
"""
import PyPDF2
from pathlib import Path

def extract_pdf_content(pdf_path):
    """Extract text content from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.extract_text()
            
            return text_content
    except Exception as e:
        return f"Error extracting PDF: {e}"

def main():
    """Extract content from all three PDFs"""
    pdf_files = [
        r"D:\Pavan Kumar Files\Downloads\RESUME_CREATION_METHODOLOGY.pdf",
        r"D:\Pavan Kumar Files\Downloads\RESUME_CREATION_METHODOLOGY_UPDATED.pdf",
        r"D:\Pavan Kumar Files\Downloads\PAVAN_COMPLETE_KNOWLEDGE_BASE.pdf"
    ]
    
    for pdf_path in pdf_files:
        print(f"\n{'='*80}")
        print(f"FILE: {Path(pdf_path).name}")
        print(f"{'='*80}")
        
        content = extract_pdf_content(pdf_path)
        # Replace problematic characters for console output
        safe_content = content.replace('\u2192', '->').replace('\u2190', '<-').replace('\u2022', '*').replace('\u25a0', '[ ]').replace('\u25cf', '[*]').replace('\u25cb', '[ ]')
        print(safe_content)
        
        # Save to text file
        txt_path = Path(pdf_path).with_suffix('.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSaved to: {txt_path}")

if __name__ == "__main__":
    main()

from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from pathlib import Path
import os
import argparse

class PDFHandler:
    def __init__(self, pdf_path):
        """
        Initialize PDFHandler with a PDF file path
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.pdf_reader = PdfReader(pdf_path)
        
    def get_num_pages(self):
        """Return the number of pages in the PDF"""
        return len(self.pdf_reader.pages)
    
    def extract_pages_as_images(self, output_dir=None, dpi=200, fmt='PNG', page_range=None):
        """
        Extract pages from PDF as images
        
        Args:
            output_dir (str, optional): Directory to save images. Defaults to 'pdf_images'
            dpi (int, optional): DPI for output images. Defaults to 200
            fmt (str, optional): Output format ('PNG', 'JPEG', etc.). Defaults to 'PNG'
            page_range (tuple, optional): Tuple of (start_page, end_page) to extract (1-based).
                                        If None, extracts all pages.
            
        Returns:
            list: List of paths to saved images
        """
        if output_dir is None:
            output_dir = 'pdf_images'
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Convert page range from 1-based to 0-based for internal processing
        if page_range:
            start_page = page_range[0] - 1
            end_page = page_range[1] - 1
            if not (0 <= start_page < len(self.pdf_reader.pages)) or \
               not (0 <= end_page < len(self.pdf_reader.pages)):
                raise ValueError("Invalid page range")
        else:
            start_page = 0
            end_page = len(self.pdf_reader.pages) - 1

        # Convert specific PDF pages to images
        try:
            images = convert_from_path(
                self.pdf_path,
                dpi=dpi,
                first_page=start_page + 1,  # pdf2image uses 1-based page numbers
                last_page=end_page + 1
            )
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")
        
        # Save images
        saved_paths = []
        for i, image in enumerate(images):
            page_num = start_page + i + 1  # Convert back to 1-based for filenames
            image_path = os.path.join(output_dir, f'page_{page_num}.{fmt.lower()}')
            image.save(image_path, fmt)
            saved_paths.append(image_path)
            
        return saved_paths
    
    def extract_text(self, page_number=None):
        """
        Extract text from PDF
        
        Args:
            page_number (int, optional): Specific page to extract text from.
                                       If None, extracts from all pages.
        
        Returns:
            str: Extracted text
        """
        if page_number is not None:
            if 0 <= page_number < len(self.pdf_reader.pages):
                return self.pdf_reader.pages[page_number].extract_text()
            else:
                raise ValueError("Invalid page number")
        
        text = ""
        for page in self.pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def split_pdf(self, output_dir=None):
        """
        Split PDF into individual pages
        
        Args:
            output_dir (str, optional): Directory to save split PDFs
            
        Returns:
            list: List of paths to individual PDF files
        """
        if output_dir is None:
            output_dir = 'split_pdfs'
            
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        pdf_paths = []
        for i in range(len(self.pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(self.pdf_reader.pages[i])
            
            output_path = os.path.join(output_dir, f'page_{i+1}.pdf')
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            pdf_paths.append(output_path)
            
        return pdf_paths
    
    def extract_page_range(self, start_page, end_page, output_path):
        """
        Extract a range of pages from the PDF and save as a new PDF
        
        Args:
            start_page (int): Starting page number (0-based)
            end_page (int): Ending page number (0-based)
            output_path (str): Path to save the extracted PDF
            
        Returns:
            str: Path to the saved PDF
        """
        if not (0 <= start_page < len(self.pdf_reader.pages)) or not (0 <= end_page < len(self.pdf_reader.pages)):
            raise ValueError("Invalid page range")
        
        pdf_writer = PdfWriter()
        for i in range(start_page, end_page + 1):
            pdf_writer.add_page(self.pdf_reader.pages[i])
        
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        
        return output_path

def main():
    # Create parser
    parser = argparse.ArgumentParser(description='PDF Handler - Process PDF files')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    
    # Create subparsers for different actions
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Extract images parser
    extract_img_parser = subparsers.add_parser('extract-images', help='Extract pages as images')
    extract_img_parser.add_argument('--output-dir', help='Output directory for images')
    extract_img_parser.add_argument('--dpi', type=int, default=256, help='DPI for output images')
    extract_img_parser.add_argument('--format', choices=['PNG', 'JPEG', 'TIFF'], default='PNG',
                                  help='Output image format')
    extract_img_parser.add_argument('--page-range', nargs=2, type=int, metavar=('START', 'END'),
                                  help='Page range to extract (e.g., 22 26)')
    
    # Extract text parser
    extract_text_parser = subparsers.add_parser('extract-text', help='Extract text from PDF')
    extract_text_parser.add_argument('--page', type=int, help='Specific page number (0-based)')
    extract_text_parser.add_argument('--output', help='Output file path (if not specified, prints to console)')
    
    # Split PDF parser
    split_parser = subparsers.add_parser('split', help='Split PDF into individual pages')
    split_parser.add_argument('--output-dir', help='Output directory for split PDFs')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    # Create PDF handler instance
    try:
        pdf_handler = PDFHandler(args.pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {str(e)}")
        return
    
    # Process based on action
    try:
        if args.action == 'extract-images':
            image_paths = pdf_handler.extract_pages_as_images(
                output_dir=args.output_dir,
                dpi=args.dpi,
                fmt=args.format,
                page_range=args.page_range if args.page_range else None
            )
            print(f"Images extracted successfully to: {image_paths}")
            
        elif args.action == 'extract-text':
            text = pdf_handler.extract_text(page_number=args.page)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Text saved to: {args.output}")
            else:
                print(text)
                
        elif args.action == 'split':
            pdf_paths = pdf_handler.split_pdf(output_dir=args.output_dir)
            print(f"PDF split successfully. Output files: {pdf_paths}")
            
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main() 
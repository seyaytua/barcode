from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image
import fitz
import tempfile
import os

class PDFHandler:
    def __init__(self):
        self.pdf_document = None
        self.page_count = 0
    
    def load_pdf(self, pdf_path):
        try:
            self.pdf_document = fitz.open(pdf_path)
            self.page_count = len(self.pdf_document)
            return True
        except Exception as e:
            print(f"PDF読み込みエラー: {e}")
            return False
    
    def get_page_count(self):
        return self.page_count
    
    def get_page_size(self, page_num):
        if not self.pdf_document or page_num >= self.page_count:
            return None
        
        try:
            page = self.pdf_document[page_num]
            rect = page.rect
            return (rect.width, rect.height)
        except Exception as e:
            print(f"ページサイズ取得エラー: {e}")
            return None
    
    def get_page_image(self, page_num):
        if not self.pdf_document or page_num >= self.page_count:
            return None
        
        try:
            page = self.pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img
        except Exception as e:
            print(f"ページ画像取得エラー: {e}")
            return None
    
    def _add_barcode_to_canvas(self, can, barcode_img, x, y, width, height):
        '''超高品質でバーコードをキャンバスに追加'''
        # さらに高解像度で保存（2倍スケール）
        scale_factor = 2
        high_res_img = barcode_img.resize(
            (int(width * scale_factor), int(height * scale_factor)), 
            Image.Resampling.LANCZOS
        )
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_path = temp_file.name
            # 最高品質PNG保存（圧縮なし）
            high_res_img.save(temp_path, format='PNG', optimize=False, compress_level=0, dpi=(300, 300))
        
        try:
            # PDFに埋め込み
            from reportlab.lib.utils import ImageReader
            can.drawImage(temp_path, x, y, 
                        width=width, height=height, 
                        mask='auto', preserveAspectRatio=True)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def add_barcodes_continuous(self, input_pdf, output_pdf, data_list, positions, barcode_generator, size_dict):
        '''
        連続印刷モード: 各データレコードごとにPDFページを複製し、
        指定された全ての位置に同じバーコードを印字
        '''
        try:
            reader = PdfReader(input_pdf)
            writer = PdfWriter()
            
            for data in data_list:
                for page_num, original_page in enumerate(reader.pages):
                    page = original_page
                    
                    page_positions = [pos for pos in positions if pos['page'] == page_num]
                    
                    if page_positions:
                        packet = BytesIO()
                        page_width = float(page.mediabox.width)
                        page_height = float(page.mediabox.height)
                        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                        
                        for pos in page_positions:
                            barcode_width, barcode_height = size_dict[pos['size']]
                            
                            barcode_img = barcode_generator.generate_barcode_with_text(
                                data['barcode'],
                                data['name'],
                                barcode_width,
                                barcode_height
                            )
                            
                            if barcode_img:
                                pdf_x = pos['x']
                                pdf_y = page_height - pos['y'] - barcode_height
                                
                                self._add_barcode_to_canvas(can, barcode_img, pdf_x, pdf_y, 
                                                          barcode_width, barcode_height)
                        
                        can.save()
                        packet.seek(0)
                        
                        barcode_pdf = PdfReader(packet)
                        page.merge_page(barcode_pdf.pages[0])
                    
                    writer.add_page(page)
            
            # 圧縮を無効にして保存
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"PDF作成エラー: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def add_barcodes_batch(self, input_pdf, output_pdf, data_list, positions, barcode_generator, size_dict):
        '''
        一括配置モード: 1つのPDFに全レコードを順番に配置
        '''
        try:
            reader = PdfReader(input_pdf)
            writer = PdfWriter()
            
            for page_num, page in enumerate(reader.pages):
                page_positions = [pos for pos in positions if pos['page'] == page_num]
                
                if page_positions and data_list:
                    packet = BytesIO()
                    page_width = float(page.mediabox.width)
                    page_height = float(page.mediabox.height)
                    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                    
                    for i, data in enumerate(data_list):
                        if i >= len(page_positions):
                            break
                        
                        pos = page_positions[i]
                        barcode_width, barcode_height = size_dict[pos['size']]
                        
                        barcode_img = barcode_generator.generate_barcode_with_text(
                            data['barcode'],
                            data['name'],
                            barcode_width,
                            barcode_height
                        )
                        
                        if barcode_img:
                            pdf_x = pos['x']
                            pdf_y = page_height - pos['y'] - barcode_height
                            
                            self._add_barcode_to_canvas(can, barcode_img, pdf_x, pdf_y, 
                                                      barcode_width, barcode_height)
                    
                    can.save()
                    packet.seek(0)
                    
                    barcode_pdf = PdfReader(packet)
                    page.merge_page(barcode_pdf.pages[0])
                
                writer.add_page(page)
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"PDF作成エラー: {e}")
            import traceback
            traceback.print_exc()
            return False

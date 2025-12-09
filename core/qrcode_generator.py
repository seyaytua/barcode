import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw, ImageFont
import os

class QRCodeGenerator:
    def generate_qrcode_with_text(self, qr_data, display_text, target_size=100):
        '''
        QRコードと下部テキストを含む画像を生成
        target_size: QRコードのサイズ（正方形）
        '''
        try:
            # QRコード生成（最小サイズ設定）
            qr = qrcode.QRCode(
                version=1,  # 最小サイズ（21x21セル）
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # 最小誤り訂正
                box_size=10,  # 各セルのピクセルサイズ
                border=2,  # 余白（最小は4だが、2で十分）
            )
            
            qr.add_data(str(qr_data))
            qr.make(fit=True)
            
            # 高解像度で生成
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # QRコード部分をリサイズ
            qr_img = qr_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # テキスト部分の高さ
            text_height = int(target_size * 0.25)
            total_height = target_size + text_height
            
            # 最終画像を作成
            combined_img = Image.new('RGB', (target_size, total_height), 'white')
            combined_img.paste(qr_img, (0, 0))
            
            # テキストを描画
            draw = ImageDraw.Draw(combined_img)
            
            font = None
            font_size = int(text_height * 0.6)
            font_paths = [
                '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                '/System/Library/Fonts/Hiragino Sans GB.ttc',
                '/Library/Fonts/Arial Unicode.ttf',
                '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                '/System/Library/Fonts/Supplemental/Arial.ttf'
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue
            
            if font is None:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # テキストを中央配置
            bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (target_size - text_width) // 2
            text_y = target_size + (text_height - font_size) // 2
            
            draw.text((text_x, text_y), display_text, fill='black', font=font)
            
            return combined_img
            
        except Exception as e:
            print(f"QRコード生成エラー: {e}")
            import traceback
            traceback.print_exc()
            return None

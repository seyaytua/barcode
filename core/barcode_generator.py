import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

class BarcodeGenerator:
    def generate_barcode_with_text(self, barcode_value, display_text, target_width=200, target_height=100):
        try:
            # 超高解像度で生成（4倍）
            render_scale = 4
            render_width = target_width * render_scale
            render_height = target_height * render_scale
            
            code128 = barcode.get_barcode_class('code128')
            barcode_instance = code128(str(barcode_value), writer=ImageWriter())
            
            buffer = BytesIO()
            # 超高品質設定
            barcode_instance.write(buffer, options={
                'module_width': 0.6,  # バーの幅
                'module_height': 25,  # バーの高さ
                'quiet_zone': 4,
                'font_size': 0,
                'text_distance': 1,
                'write_text': False,
                'dpi': 600  # 超高DPI
            })
            buffer.seek(0)
            
            barcode_img = Image.open(buffer)
            
            # テキスト部分の高さ
            text_height = int(render_height * 0.3)
            barcode_height = render_height - text_height
            
            # バーコード部分を超高品質リサイズ
            barcode_img = barcode_img.resize((render_width, barcode_height), Image.Resampling.LANCZOS)
            
            # 超高解像度キャンバスを作成
            combined_img = Image.new('RGB', (render_width, render_height), 'white')
            combined_img.paste(barcode_img, (0, 0))
            
            # テキスト描画
            draw = ImageDraw.Draw(combined_img)
            
            font = None
            font_size = int(text_height * 0.6)
            font_paths = [
                '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
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
            text_x = (render_width - text_width) // 2
            text_y = barcode_height + (text_height - font_size) // 2
            
            draw.text((text_x, text_y), display_text, fill='black', font=font)
            
            # 最終的に目標サイズにリサイズ（超高品質）
            final_img = combined_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            return final_img
            
        except Exception as e:
            print(f"バーコード生成エラー: {e}")
            import traceback
            traceback.print_exc()
            return None

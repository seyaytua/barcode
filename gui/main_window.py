from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                      QPushButton, QLabel, QFileDialog, QMessageBox,
                                      QTableWidget, QTableWidgetItem, QSpinBox, QGroupBox,
                                      QScrollArea, QComboBox, QTextEdit, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt, Signal, QObject, QRect, QPoint, QRectF
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QBrush
from core.barcode_generator import BarcodeGenerator
from core.pdf_handler import PDFHandler
from core.excel_handler import ExcelHandler
import os

class ToggleButton(QPushButton):
    '''トグルスイッチ風ボタン'''
    def __init__(self, text_on="ON", text_off="OFF", parent=None):
        super().__init__(parent)
        self.text_on = text_on
        self.text_off = text_off
        self.is_on = True
        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.on_clicked)
        self.update_style()
    
    def on_clicked(self):
        self.is_on = self.isChecked()
        self.update_style()
    
    def update_style(self):
        if self.is_on:
            self.setText(self.text_on)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.setText(self.text_off)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #9E9E9E;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #757575;
                }
            """)

class SizeSettingsDialog(QDialog):
    '''バーコードサイズ設定ダイアログ'''
    def __init__(self, current_sizes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("バーコードサイズ設定")
        self.setModal(True)
        self.current_sizes = current_sizes.copy()
        
        layout = QVBoxLayout(self)
        
        # 説明
        info_label = QLabel("各サイズの幅と高さを設定してください（単位: ピクセル）")
        layout.addWidget(info_label)
        
        # サイズ設定
        self.spinboxes = {}
        for size_name in ['小', '中', '大']:
            group = QGroupBox(f"サイズ: {size_name}")
            group_layout = QHBoxLayout()
            
            group_layout.addWidget(QLabel("幅:"))
            width_spin = QSpinBox()
            width_spin.setRange(50, 500)
            width_spin.setValue(current_sizes[size_name][0])
            group_layout.addWidget(width_spin)
            
            group_layout.addWidget(QLabel("高さ:"))
            height_spin = QSpinBox()
            height_spin.setRange(30, 300)
            height_spin.setValue(current_sizes[size_name][1])
            group_layout.addWidget(height_spin)
            
            group.setLayout(group_layout)
            layout.addWidget(group)
            
            self.spinboxes[size_name] = (width_spin, height_spin)
        
        # プリセットボタン
        preset_group = QGroupBox("プリセット")
        preset_layout = QHBoxLayout()
        
        btn_compact = QPushButton("コンパクト")
        btn_compact.clicked.connect(self.apply_compact_preset)
        preset_layout.addWidget(btn_compact)
        
        btn_standard = QPushButton("標準")
        btn_standard.clicked.connect(self.apply_standard_preset)
        preset_layout.addWidget(btn_standard)
        
        btn_large = QPushButton("大きめ")
        btn_large.clicked.connect(self.apply_large_preset)
        preset_layout.addWidget(btn_large)
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # OK/キャンセルボタン
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def apply_compact_preset(self):
        '''コンパクトプリセット'''
        presets = {'小': (100, 50), '中': (130, 70), '大': (160, 90)}
        for size_name, (width, height) in presets.items():
            self.spinboxes[size_name][0].setValue(width)
            self.spinboxes[size_name][1].setValue(height)
    
    def apply_standard_preset(self):
        '''標準プリセット'''
        presets = {'小': (120, 60), '中': (150, 80), '大': (180, 100)}
        for size_name, (width, height) in presets.items():
            self.spinboxes[size_name][0].setValue(width)
            self.spinboxes[size_name][1].setValue(height)
    
    def apply_large_preset(self):
        '''大きめプリセット'''
        presets = {'小': (150, 80), '中': (200, 100), '大': (250, 130)}
        for size_name, (width, height) in presets.items():
            self.spinboxes[size_name][0].setValue(width)
            self.spinboxes[size_name][1].setValue(height)
    
    def get_sizes(self):
        '''設定されたサイズを取得'''
        sizes = {}
        for size_name, (width_spin, height_spin) in self.spinboxes.items():
            sizes[size_name] = (width_spin.value(), height_spin.value())
        return sizes

class ClickableLabel(QLabel):
    clicked = Signal(int, int)
    
    def __init__(self):
        super().__init__()
        self.markers = []
        self.base_pixmap = None
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
    
    def mousePressEvent(self, event):
        click_x = event.pos().x()
        click_y = event.pos().y()
        
        if self.base_pixmap:
            pixmap_width = self.base_pixmap.width()
            pixmap_height = self.base_pixmap.height()
            label_width = self.width()
            label_height = self.height()
            
            offset_x = (label_width - pixmap_width) // 2
            offset_y = (label_height - pixmap_height) // 2
            
            image_x = click_x - offset_x
            image_y = click_y - offset_y
            
            if 0 <= image_x < pixmap_width and 0 <= image_y < pixmap_height:
                self.clicked.emit(image_x, image_y)
    
    def add_marker(self, x, y, width, height):
        self.markers.append((x, y, width, height))
        self.update_display()
    
    def clear_markers(self):
        self.markers = []
        self.update_display()
    
    def set_base_pixmap(self, pixmap):
        self.base_pixmap = pixmap
        self.update_display()
    
    def update_display(self):
        if self.base_pixmap:
            display_pixmap = self.base_pixmap.copy()
            
            painter = QPainter(display_pixmap)
            
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            brush = QBrush(QColor(255, 0, 0, 50))
            painter.setBrush(brush)
            
            for x, y, w, h in self.markers:
                painter.drawRect(int(x), int(y), int(w), int(h))
                
                center_x = x + w / 2
                center_y = y + h / 2
                size = 10
                pen_cross = QPen(QColor(255, 0, 0), 2)
                painter.setPen(pen_cross)
                painter.drawLine(int(center_x - size), int(center_y), int(center_x + size), int(center_y))
                painter.drawLine(int(center_x), int(center_y - size), int(center_x), int(center_y + size))
            
            painter.end()
            self.setPixmap(display_pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("バーコードPDF印刷システム")
        self.setGeometry(100, 100, 1200, 800)
        
        # デフォルトサイズ（小さめに設定）
        self.BARCODE_SIZES = {
            '小': (120, 60),
            '中': (150, 80),
            '大': (180, 100)
        }
        
        self.pdf_handler = PDFHandler()
        self.excel_handler = ExcelHandler()
        self.barcode_generator = BarcodeGenerator()
        
        self.pdf_path = None
        self.excel_path = None
        self.barcode_positions = []
        self.current_page = 0
        self.current_scale = 1.0
        self.original_page_size = (0, 0)
        self.current_barcode_size = '中'
        self.is_continuous_mode = True
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
    
    def create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # モード切り替え
        mode_group = QGroupBox("印刷モード")
        mode_layout = QVBoxLayout()
        
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(QLabel("モード:"))
        
        self.toggle_mode = ToggleButton("連続印刷モード", "一括配置モード")
        self.toggle_mode.clicked.connect(self.on_mode_changed)
        toggle_layout.addWidget(self.toggle_mode)
        toggle_layout.addStretch()
        
        mode_layout.addLayout(toggle_layout)
        
        self.lbl_mode_desc = QLabel()
        self.lbl_mode_desc.setWordWrap(True)
        self.lbl_mode_desc.setStyleSheet("QLabel { background-color: #e3f2fd; padding: 8px; border-radius: 4px; }")
        mode_layout.addWidget(self.lbl_mode_desc)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        self.update_mode_description()
        
        excel_group = QGroupBox("Excelリスト管理")
        excel_layout = QVBoxLayout()
        
        btn_export_template = QPushButton("テンプレートをエクスポート")
        btn_export_template.clicked.connect(self.export_template)
        excel_layout.addWidget(btn_export_template)
        
        btn_import_excel = QPushButton("Excelリストをインポート")
        btn_import_excel.clicked.connect(self.import_excel)
        excel_layout.addWidget(btn_import_excel)
        
        self.lbl_excel_status = QLabel("リスト: 未読み込み")
        excel_layout.addWidget(self.lbl_excel_status)
        
        excel_group.setLayout(excel_layout)
        layout.addWidget(excel_group)
        
        pdf_group = QGroupBox("PDF管理")
        pdf_layout = QVBoxLayout()
        
        btn_load_pdf = QPushButton("PDFファイルを読み込む")
        btn_load_pdf.clicked.connect(self.load_pdf)
        pdf_layout.addWidget(btn_load_pdf)
        
        self.lbl_pdf_status = QLabel("PDF: 未読み込み")
        pdf_layout.addWidget(self.lbl_pdf_status)
        
        page_nav_layout = QHBoxLayout()
        btn_prev = QPushButton("前のページ")
        btn_prev.clicked.connect(self.prev_page)
        page_nav_layout.addWidget(btn_prev)
        
        self.lbl_page = QLabel("ページ: 0/0")
        page_nav_layout.addWidget(self.lbl_page)
        
        btn_next = QPushButton("次のページ")
        btn_next.clicked.connect(self.next_page)
        page_nav_layout.addWidget(btn_next)
        
        pdf_layout.addLayout(page_nav_layout)
        pdf_group.setLayout(pdf_layout)
        layout.addWidget(pdf_group)
        
        size_group = QGroupBox("バーコードサイズ")
        size_layout = QVBoxLayout()
        
        size_select_layout = QHBoxLayout()
        size_select_layout.addWidget(QLabel("サイズ:"))
        
        self.combo_barcode_size = QComboBox()
        self.combo_barcode_size.addItems(['小', '中', '大'])
        self.combo_barcode_size.setCurrentText('中')
        self.combo_barcode_size.currentTextChanged.connect(self.on_barcode_size_changed)
        size_select_layout.addWidget(self.combo_barcode_size)
        
        btn_size_settings = QPushButton("⚙️ 設定")
        btn_size_settings.clicked.connect(self.open_size_settings)
        size_select_layout.addWidget(btn_size_settings)
        
        size_layout.addLayout(size_select_layout)
        
        self.lbl_size_info = QLabel(f"現在: {self.BARCODE_SIZES['中'][0]}x{self.BARCODE_SIZES['中'][1]}px")
        size_layout.addWidget(self.lbl_size_info)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        position_group = QGroupBox("バーコード位置")
        position_layout = QVBoxLayout()
        
        self.table_positions = QTableWidget(0, 4)
        self.table_positions.setHorizontalHeaderLabels(["ページ", "X座標", "Y座標", "サイズ"])
        position_layout.addWidget(self.table_positions)
        
        btn_layout = QHBoxLayout()
        btn_remove_position = QPushButton("選択位置を削除")
        btn_remove_position.clicked.connect(self.remove_position)
        btn_layout.addWidget(btn_remove_position)
        
        btn_clear_all = QPushButton("全てクリア")
        btn_clear_all.clicked.connect(self.clear_all_positions)
        btn_layout.addWidget(btn_clear_all)
        
        position_layout.addLayout(btn_layout)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        data_group = QGroupBox("読み込みデータ")
        data_layout = QVBoxLayout()
        
        self.table_data = QTableWidget(0, 2)
        self.table_data.setHorizontalHeaderLabels(["バーコード値", "表示名"])
        data_layout.addWidget(self.table_data)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        self.lbl_output_info = QLabel("出力予測: -")
        self.lbl_output_info.setStyleSheet("QLabel { color: blue; font-weight: bold; padding: 5px; }")
        layout.addWidget(self.lbl_output_info)
        
        btn_print = QPushButton("印刷実行")
        btn_print.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; }")
        btn_print.clicked.connect(self.execute_print)
        layout.addWidget(btn_print)
        
        return widget
    
    def create_right_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("PDFプレビュー（クリックでバーコード位置を指定）\n赤い矩形がバーコードの配置範囲です")
        info_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        layout.addWidget(info_label)
        
        self.preview_label = ClickableLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 2px solid #ccc; }")
        self.preview_label.setMinimumSize(600, 700)
        self.preview_label.clicked.connect(self.add_barcode_position)
        
        layout.addWidget(self.preview_label)
        
        return widget
    
    def open_size_settings(self):
        '''サイズ設定ダイアログを開く'''
        dialog = SizeSettingsDialog(self.BARCODE_SIZES, self)
        if dialog.exec() == QDialog.Accepted:
            self.BARCODE_SIZES = dialog.get_sizes()
            # 現在のサイズ情報を更新
            width, height = self.BARCODE_SIZES[self.current_barcode_size]
            self.lbl_size_info.setText(f"現在: {width}x{height}px")
            # プレビューを更新
            if self.pdf_path:
                self.restore_page_markers()
            QMessageBox.information(self, "成功", "バーコードサイズを更新しました")
    
    def on_mode_changed(self):
        self.is_continuous_mode = self.toggle_mode.isChecked()
        self.update_mode_description()
        self.update_output_info()
    
    def update_mode_description(self):
        if self.is_continuous_mode:
            desc = (
                "【連続印刷モード】\n"
                "各レコードごとに全ページを複製します。\n\n"
                "例: 2レコード、2ページPDF、各ページ2箇所指定\n"
                "→ 出力: 4ページ\n"
                "  ・1ページ目: レコード1のバーコード×2\n"
                "  ・2ページ目: レコード1のバーコード×2\n"
                "  ・3ページ目: レコード2のバーコード×2\n"
                "  ・4ページ目: レコード2のバーコード×2"
            )
        else:
            desc = (
                "【一括配置モード】\n"
                "1つのPDFに全レコードを順番に配置します。\n\n"
                "例: 2レコード、2ページPDF、各ページ2箇所指定\n"
                "→ 出力: 2ページ\n"
                "  ・1ページ目: レコード1のバーコード(位置1)\n"
                "              レコード2のバーコード(位置2)\n"
                "  ・2ページ目: レコード1のバーコード(位置1)\n"
                "              レコード2のバーコード(位置2)"
            )
        
        self.lbl_mode_desc.setText(desc)
    
    def on_barcode_size_changed(self, size_text):
        self.current_barcode_size = size_text
        width, height = self.BARCODE_SIZES[size_text]
        self.lbl_size_info.setText(f"現在: {width}x{height}px")
        
        if self.pdf_path:
            self.restore_page_markers()
    
    def update_output_info(self):
        if self.excel_path and self.pdf_path:
            data = self.excel_handler.import_excel(self.excel_path)
            record_count = len(data)
            page_count = self.pdf_handler.get_page_count()
            
            if self.is_continuous_mode:
                total_pages = record_count * page_count
                
                barcode_per_page = {}
                for pos in self.barcode_positions:
                    page = pos['page']
                    barcode_per_page[page] = barcode_per_page.get(page, 0) + 1
                
                info_text = f"出力予測: {total_pages}ページ ({record_count}レコード × {page_count}ページ)"
                if barcode_per_page:
                    info_text += f"\n各ページのバーコード数: {dict(sorted(barcode_per_page.items()))}"
            else:
                total_pages = page_count
                total_positions = len(self.barcode_positions)
                
                info_text = f"出力予測: {total_pages}ページ"
                info_text += f"\n配置位置数: {total_positions}箇所"
                if total_positions > 0 and record_count > 0:
                    if record_count <= total_positions:
                        info_text += f"\n全{record_count}レコードを配置可能"
                    else:
                        info_text += f"\n⚠️ {record_count - total_positions}レコードが配置できません"
            
            self.lbl_output_info.setText(info_text)
        else:
            self.lbl_output_info.setText("出力予測: -")
    
    def export_template(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "テンプレートを保存", "", "Excel Files (*.xlsx)")
        if file_path:
            self.excel_handler.export_template(file_path)
            QMessageBox.information(self, "成功", "テンプレートをエクスポートしました")
    
    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Excelファイルを選択", "", "Excel Files (*.xlsx)")
        if file_path:
            data = self.excel_handler.import_excel(file_path)
            if data:
                self.excel_path = file_path
                self.lbl_excel_status.setText(f"リスト: {os.path.basename(file_path)} ({len(data)}件)")
                self.update_data_table(data)
                self.update_output_info()
                QMessageBox.information(self, "成功", f"{len(data)}件のデータを読み込みました")
    
    def load_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "PDFファイルを選択", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_path = file_path
            self.pdf_handler.load_pdf(file_path)
            self.current_page = 0
            
            self.original_page_size = self.pdf_handler.get_page_size(self.current_page)
            
            self.lbl_pdf_status.setText(f"PDF: {os.path.basename(file_path)} ({self.pdf_handler.get_page_count()}ページ)")
            self.update_preview()
            self.update_output_info()
    
    def update_preview(self):
        if self.pdf_path:
            image = self.pdf_handler.get_page_image(self.current_page)
            if image:
                original_img_size = (image.width, image.height)
                
                qimage = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                
                scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                self.current_scale = scaled_pixmap.width() / original_img_size[0]
                
                self.preview_label.set_base_pixmap(scaled_pixmap)
                
                self.restore_page_markers()
                
                self.lbl_page.setText(f"ページ: {self.current_page + 1}/{self.pdf_handler.get_page_count()}")
    
    def restore_page_markers(self):
        self.preview_label.clear_markers()
        
        page_positions = [pos for pos in self.barcode_positions if pos['page'] == self.current_page]
        
        pdf_page_size = self.pdf_handler.get_page_size(self.current_page)
        if not pdf_page_size:
            return
        
        image = self.pdf_handler.get_page_image(self.current_page)
        if not image:
            return
        
        render_size = (image.width, image.height)
        
        for pos in page_positions:
            render_x = pos['x'] * render_size[0] / pdf_page_size[0]
            render_y = pos['y'] * render_size[1] / pdf_page_size[1]
            
            preview_x = render_x * self.current_scale
            preview_y = render_y * self.current_scale
            
            barcode_width, barcode_height = self.BARCODE_SIZES[pos['size']]
            preview_width = barcode_width * self.current_scale * render_size[0] / pdf_page_size[0]
            preview_height = barcode_height * self.current_scale * render_size[1] / pdf_page_size[1]
            
            self.preview_label.add_marker(preview_x, preview_y, preview_width, preview_height)
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_preview()
    
    def next_page(self):
        if self.pdf_path and self.current_page < self.pdf_handler.get_page_count() - 1:
            self.current_page += 1
            self.update_preview()
    
    def add_barcode_position(self, x, y):
        if not self.pdf_path:
            QMessageBox.warning(self, "警告", "先にPDFファイルを読み込んでください")
            return
        
        render_x = x / self.current_scale
        render_y = y / self.current_scale
        
        pdf_page_size = self.pdf_handler.get_page_size(self.current_page)
        image = self.pdf_handler.get_page_image(self.current_page)
        
        if pdf_page_size and image:
            render_size = (image.width, image.height)
            
            real_x = render_x * pdf_page_size[0] / render_size[0]
            real_y = render_y * pdf_page_size[1] / render_size[1]
            
            self.barcode_positions.append({
                'page': self.current_page,
                'x': real_x,
                'y': real_y,
                'size': self.current_barcode_size
            })
            
            barcode_width, barcode_height = self.BARCODE_SIZES[self.current_barcode_size]
            preview_width = barcode_width * self.current_scale * render_size[0] / pdf_page_size[0]
            preview_height = barcode_height * self.current_scale * render_size[1] / pdf_page_size[1]
            
            self.preview_label.add_marker(x, y, preview_width, preview_height)
            
            self.update_position_table()
            self.update_output_info()
    
    def remove_position(self):
        current_row = self.table_positions.currentRow()
        if current_row >= 0:
            del self.barcode_positions[current_row]
            self.update_position_table()
            self.restore_page_markers()
            self.update_output_info()
    
    def clear_all_positions(self):
        self.barcode_positions = []
        self.update_position_table()
        self.preview_label.clear_markers()
        self.update_output_info()
    
    def update_position_table(self):
        self.table_positions.setRowCount(len(self.barcode_positions))
        for i, pos in enumerate(self.barcode_positions):
            self.table_positions.setItem(i, 0, QTableWidgetItem(str(pos['page'] + 1)))
            self.table_positions.setItem(i, 1, QTableWidgetItem(f"{pos['x']:.1f}"))
            self.table_positions.setItem(i, 2, QTableWidgetItem(f"{pos['y']:.1f}"))
            self.table_positions.setItem(i, 3, QTableWidgetItem(pos['size']))
    
    def update_data_table(self, data):
        self.table_data.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table_data.setItem(i, 0, QTableWidgetItem(str(row['barcode'])))
            self.table_data.setItem(i, 1, QTableWidgetItem(str(row['name'])))
    
    def execute_print(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "警告", "PDFファイルを読み込んでください")
            return
        
        if not self.excel_path:
            QMessageBox.warning(self, "警告", "Excelリストを読み込んでください")
            return
        
        if not self.barcode_positions:
            QMessageBox.warning(self, "警告", "バーコード位置を指定してください")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "出力PDFを保存", "", "PDF Files (*.pdf)")
        if output_path:
            data = self.excel_handler.import_excel(self.excel_path)
            
            if self.is_continuous_mode:
                success = self.pdf_handler.add_barcodes_continuous(
                    self.pdf_path,
                    output_path,
                    data,
                    self.barcode_positions,
                    self.barcode_generator,
                    self.BARCODE_SIZES
                )
                
                if success:
                    total_pages = len(data) * self.pdf_handler.get_page_count()
                    QMessageBox.information(self, "成功", 
                        f"バーコード付きPDFを作成しました:\n{output_path}\n\n"
                        f"モード: 連続印刷\n"
                        f"総ページ数: {total_pages}ページ")
                else:
                    QMessageBox.critical(self, "エラー", "PDF作成中にエラーが発生しました")
            else:
                success = self.pdf_handler.add_barcodes_batch(
                    self.pdf_path,
                    output_path,
                    data,
                    self.barcode_positions,
                    self.barcode_generator,
                    self.BARCODE_SIZES
                )
                
                if success:
                    QMessageBox.information(self, "成功", 
                        f"バーコード付きPDFを作成しました:\n{output_path}\n\n"
                        f"モード: 一括配置\n"
                        f"総ページ数: {self.pdf_handler.get_page_count()}ページ")
                else:
                    QMessageBox.critical(self, "エラー", "PDF作成中にエラーが発生しました")

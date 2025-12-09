# リリースノート v2.0.2

## 概要
バーコード/QRコードPDF印刷システム v2.0.2のリリースです。

## 変更内容

### バグ修正
- GitHub Actionsビルドでのファイル検出を改善
- core/qrcode_generator.pyの欠落を修正
- ビルドspecファイルのバージョン設定を最適化

### 技術的改善
- 柔軟なファイル名検出機能を追加
- ビルドプロセスの安定性を向上

### ビルド情報
- ビルド対象: main_v2.py
- 実行ファイル名: 
  - Windows: BarcodeQRCodePDF_v2.exe
  - macOS: BarcodeQRCodePDF_v2.app
- バージョン: 2.0.2
- ビルド日: 2024-12-09

### 新機能（v2.0.0からの継承）
- バーコード管理システムの統合UI
- 教職員と備品のタブ管理機能
- 日付指定機能の追加
- Excelエクスポート/インポート機能の強化

### 技術スタック
- Python 3.11+
- PySide6 6.6.0
- python-barcode 0.15.1
- qrcode 7.4.2
- Pillow 10.1.0
- PyPDF2 3.0.1
- reportlab 4.0.7
- openpyxl 3.1.2
- PyMuPDF 1.23.8

### システム要件
- Windows 10以降
- macOS 10.14以降
- メモリ: 2GB以上推奨
- ディスク空き容量: 200MB以上

---
リリース日: 2024-12-09

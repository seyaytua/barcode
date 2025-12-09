# リリースノート v2.0.3

## 概要
バーコード/QRコードPDF印刷システム v2.0.3のリリースです。

## 🔧 バグ修正

### Windows環境でのPDF保存エラーを修正
- **問題:** PDF作成時に「PermissionError [WinError 32] プロセスはファイルにアクセスできません」エラーが発生
- **原因:** tempfileの不適切な管理により、Windowsでファイルハンドルが適切に閉じられていなかった
- **修正:** `tempfile.mkstemp()`を使用し、ファイルハンドルを明示的に閉じるよう変更
- **影響:** 備品用PDF・教職員用PDFの両方で修正

### 変更内容
- ✅ PDF生成時の一時ファイル管理を改善
- ✅ Windowsでのファイル権限エラーを解消
- ✅ より安全なtempfile処理を実装

## 📊 動作確認

- ✅ Windows環境でのPDF保存が正常に動作
- ✅ 備品用バーコード/QRコードPDF生成
- ✅ 教職員用バーコード/QRコードPDF生成
- ✅ Excelインポート/エクスポート機能

## 🔄 v2.0.2からの変更点

### 修正されたファイル
- `main_v2.py` - 2箇所のtempfile処理を修正

## 技術スタック
- Python 3.11+
- PySide6 6.6.0
- python-barcode 0.15.1
- qrcode 7.4.2
- Pillow 10.1.0
- PyPDF2 3.0.1
- reportlab 4.0.7
- openpyxl 3.1.2
- PyMuPDF 1.23.8

## システム要件
- Windows 10以降
- macOS 10.14以降
- メモリ: 2GB以上推奨
- ディスク空き容量: 200MB以上

---
リリース日: 2024-12-09

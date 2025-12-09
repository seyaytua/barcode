# リリースノート v2.0.2

## 概要
バーコード/QRコードPDF印刷システム v2.0.2のリリースです。
v2.0.0/v2.0.1のビルド問題を修正しました。

## 変更内容

### バグ修正
- GitHub Actionsビルドエラーを修正
- PyInstallerが生成する実際のファイル名を正しく検出
- 柔軟なファイル検出機能を追加
- `core/qrcode_generator.py`モジュールの欠落を修正

### ビルド情報
- ビルド対象: main_v2.py
- 実行ファイル名: BarcodeQRCodePDF_v2
- バージョン: 2.0.2
- ビルド日: 2024-12-09

### 新機能（v2.0.0からの継承）
- main_v2.pyベースの新しいアプリケーション
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

### ダウンロード
実行ファイルはGitHub Releasesから入手できます。

### 使用方法
1. 実行ファイルをダウンロード
2. Windows: ZIPを展開して`BarcodeQRCodePDF_v2.exe`を実行
3. macOS: DMGをマウントして`BarcodeQRCodePDF_v2.app`を実行

### システム要件
- Windows 10以降 / macOS 10.14以降
- メモリ: 2GB以上推奨
- ディスク空き容量: 200MB以上

### 既知の問題
- なし

### サポート
問題が発生した場合は、GitHubのIssuesで報告してください。

---
リリース日: 2024-12-09
バージョン: 2.0.2

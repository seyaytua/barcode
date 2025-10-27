# バーコード/QRコードPDF印刷システム

PythonとPySide6を使用したバーコード・QRコードPDF印刷アプリケーション

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

## 機能

### コードタイプ
- **バーコード (CODE128)**: 従来の1次元バーコード
- **QRコード**: 2次元コード（コンパクトサイズ対応）

### 印刷モード
- **連続印刷モード**: 各レコードごとに全ページを複製
- **一括配置モード**: 1つのPDFに全レコードを順番に配置

### その他の機能
- PDFファイルへの自由な位置配置
- Excelリストからのデータ一括読み込み
- サイズカスタマイズ（小・中・大）
- 超高品質生成（600 DPI）
- GUIでの直感的な位置指定
- プレビュー機能付き

## インストール

### 必要要件
- Python 3.11以上
- macOS / Windows

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/seyaytua/barcode.git
cd barcode

# 依存パッケージをインストール
pip install -r requirements.txt
使い方
アプリケーションの起動
Copypython main.py
基本的な使用手順
コードタイプを選択: バーコードまたはQRコードを選択
印刷モードを選択: 連続印刷または一括配置を選択
Excelリストをインポート: テンプレートをエクスポートして編集後、インポート
PDFファイルを読み込む: ベースとなるPDFファイルを選択
サイズを選択: 小・中・大から選択（設定ボタンでカスタマイズ可能）
配置位置を指定: プレビュー画面をクリックして配置位置を指定
印刷実行: 出力PDFを保存
Excelリストの形式
バーコード値	表示名
123456789	商品A
987654321	商品B
プロジェクト構造
.
├── main.py                    # エントリーポイント
├── requirements.txt           # 依存パッケージ
├── gui/
│   ├── __init__.py
│   └── main_window.py        # メインウィンドウ
└── core/
    ├── __init__.py
    ├── barcode_generator.py  # バーコード生成
    ├── qrcode_generator.py   # QRコード生成
    ├── pdf_handler.py        # PDF操作
    └── excel_handler.py      # Excel操作
ビルド
Windows用実行ファイルを作成：

Copypip install pyinstaller
pyinstaller --onefile --windowed --name "BarcodeQRCodePDF" main.py
実行ファイルは dist/ フォルダに生成されます。

リリース
GitHubのReleasesページから最新版をダウンロードできます： Releases

技術スタック
GUI: PySide6 (Qt for Python)
バーコード生成: python-barcode
QRコード生成: qrcode
PDF操作: PyPDF2, ReportLab, PyMuPDF
Excel操作: openpyxl
画像処理: Pillow
ライセンス
MIT License

貢献
プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。

サポート
問題が発生した場合は、Issuesで報告してください。

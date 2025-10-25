# バーコードPDF印刷システム

PythonとPySide6を使用したバーコードPDF印刷アプリケーション

## 機能

- PDFファイルへのバーコード配置
- Excelリストからのデータ読み込み
- 2つの印刷モード：
  - **連続印刷モード**: 各レコードごとに全ページを複製
  - **一括配置モード**: 1つのPDFに全レコードを順番に配置
- バーコードサイズのカスタマイズ（小・中・大）
- 高品質バーコード生成（600 DPI）
- GUIでの直感的な位置指定

## インストール

```bash
pip install -r requirements.txt
必要要件
Python 3.11以上
macOS（Windowsでも動作可能だが、フォントパスの調整が必要）
使い方
Copypython main.py
Excelリストをインポート: バーコード値と表示名を含むExcelファイルを読み込む
PDFファイルを読み込む: ベースとなるPDFファイルを選択
バーコード位置を指定: プレビュー画面をクリックして配置位置を指定
印刷実行: 出力PDFを保存
プロジェクト構造
.
├── main.py                 # エントリーポイント
├── requirements.txt        # 依存パッケージ
├── gui/
│   ├── __init__.py
│   └── main_window.py     # メインウィンドウ
└── core/
    ├── __init__.py
    ├── barcode_generator.py  # バーコード生成
    ├── pdf_handler.py        # PDF操作
    └── excel_handler.py      # Excel操作
ライセンス
MIT License

# v1.3.0 リリース完了手順

## ✅ 完了した作業

1. **PyInstallerのspecファイル改善** - 完了
   - 必要な依存関係を明示的に追加
   - Windowsバージョン情報ファイルの参照を追加
   - macOSバンドル設定を追加

2. **Windowsバージョン情報ファイル作成** - 完了
   - `version_info.txt` を作成・コミット済み
   
3. **バージョン管理システム実装** - 完了
   - `version.py` を作成・コミット済み
   - アプリケーションタイトルにバージョン番号を表示

4. **GitHub Actionsワークフロー改善** - ドキュメント化済み
   - `build.yml.new` に修正版を保存済み
   - 手動適用が必要（下記参照）

5. **コードのコミットとプッシュ** - 完了
   - すべての変更をmainブランチにマージ済み
   - v1.3.0タグを作成・プッシュ済み

## 🔧 手動で実施が必要な作業

### GitHub Actionsワークフローファイルの更新

GitHub Appの権限制限により、ワークフローファイルの変更は手動で行う必要があります。

#### 手順:

1. **GitHubリポジトリをブラウザで開く**
   ```
   https://github.com/seyaytua/barcode
   ```

2. **ワークフローファイルを編集**
   - `.github/workflows/build.yml` に移動
   - 右上の「Edit this file」（鉛筆アイコン）をクリック

3. **build.yml.newの内容をコピー**
   - リポジトリの `build.yml.new` ファイルの内容を全てコピー
   - `.github/workflows/build.yml` の内容を全て置き換える

4. **変更をコミット**
   - コミットメッセージ: `fix: ビルドエラーを修正（実行ファイル名のフォールバック処理を追加）`
   - 「Commit changes」をクリック

5. **v1.3.0タグを再プッシュ（必要に応じて）**
   ```bash
   git tag -d v1.3.0
   git tag -a v1.3.0 -m "Release v1.3.0"
   git push -f origin v1.3.0
   ```

## 🔍 修正内容の詳細

### 問題
PyInstallerのspecファイルで`name='BarcodeQRCodePDF'`と指定しているにもかかわらず、実際には元のスクリプト名（`barcode`）で実行ファイルが生成される可能性がありました。

### 修正
`build.yml.new`に以下の改善を追加：

1. **ディレクトリ内容の確認**
   ```yaml
   - name: List dist directory contents
     run: Get-ChildItem -Path dist -Recurse
   ```

2. **ファイル名フォールバック処理**
   ```powershell
   if (Test-Path "dist\BarcodeQRCodePDF.exe") {
     # 期待通りのファイル名
   } elseif (Test-Path "dist\barcode.exe") {
     # フォールバック: リネーム
     Move-Item dist\barcode.exe dist\BarcodeQRCodePDF.exe
   } else {
     # エラー
     exit 1
   }
   ```

3. **macOSでも同様の処理**

## 📋 確認事項

ワークフローファイルを更新した後：

1. **GitHub Actionsの実行を確認**
   - https://github.com/seyaytua/barcode/actions に移動
   - 最新のビルドが成功していることを確認

2. **リリースページを確認**
   - https://github.com/seyaytua/barcode/releases に移動
   - v1.3.0のリリースが作成されていることを確認
   - Windows版とmacOS版のZIP/DMGファイルがアップロードされていることを確認

3. **ダウンロードとテスト**
   - Windows版ZIPをダウンロードして展開
   - `BarcodeQRCodePDF.exe`が正常に起動することを確認
   - ウィンドウタイトルに「Barcode QR Code PDF v1.3.0」と表示されることを確認

## 📚 関連リンク

- **プルリクエスト**: https://github.com/seyaytua/barcode/pull/1
- **リポジトリ**: https://github.com/seyaytua/barcode
- **アクション**: https://github.com/seyaytua/barcode/actions
- **リリース**: https://github.com/seyaytua/barcode/releases

## 🎯 期待される結果

ワークフローファイル更新後、v1.3.0タグをプッシュすると：

1. GitHub Actionsが自動的にビルドを開始
2. Windows版（ZIP）とmacOS版（DMG/ZIP）が生成
3. リリースページに自動的にアップロード
4. ユーザーがダウンロードして展開・実行可能

## ⚠️ トラブルシューティング

### ビルドが失敗する場合

1. **Actionsログを確認**
   - どのステップで失敗しているかを確認
   - `List dist directory contents` ステップでファイル名を確認

2. **実行ファイル名が異なる場合**
   - `build.yml`のフォールバック処理に別のファイル名を追加

### リリースが作成されない場合

1. **タグが正しいか確認**
   ```bash
   git tag -l "v*"
   ```

2. **タグを再プッシュ**
   ```bash
   git push -f origin v1.3.0
   ```

# 🚨 緊急：Workflow修正手順

## 問題
PyInstallerが期待と異なるファイル名でビルドしています。

## 解決策
workflowに「ディレクトリ内容確認」と「柔軟なファイル名検出」を追加します。

---

## 📝 今すぐ実行する修正手順

### 1. Workflowファイルを開く
```
https://github.com/seyaytua/barcode/edit/main/.github/workflows/build.yml
```

### 2. 「Build executable with spec」の直後に以下を追加

**26行目「pyinstaller barcode_v2.spec」の直後に追加：**

```yaml
- name: Build executable with spec
  run: |
    pyinstaller barcode_v2.spec

- name: List dist directory contents
  run: |
    Write-Host "=== Dist directory contents ==="
    Get-ChildItem -Path dist -Recurse | Format-Table -AutoSize
  shell: pwsh
```

### 3. 「Create ZIP archive」セクション全体を置き換え

**現在の「Create ZIP archive」セクションを以下に完全に置き換えてください：**

```yaml
- name: Create ZIP archive
  run: |
    Write-Host "Searching for executable..."
    
    # 可能性のあるファイル名をすべて確認
    $exeFile = $null
    $possibleNames = @(
      "dist\BarcodeQRCodePDF_v2.exe",
      "dist\main_v2.exe",
      "dist\barcode_v2.exe",
      "dist\BarcodeApp.exe"
    )
    
    foreach ($name in $possibleNames) {
      if (Test-Path $name) {
        Write-Host "✓ Found: $name"
        $exeFile = $name
        break
      }
    }
    
    # まだ見つからない場合、dist内の.exeファイルを検索
    if (-not $exeFile) {
      Write-Host "Searching for any .exe file in dist..."
      $exeFiles = Get-ChildItem -Path dist -Filter "*.exe" -File
      if ($exeFiles.Count -gt 0) {
        $exeFile = $exeFiles[0].FullName
        Write-Host "✓ Found exe: $exeFile"
      }
    }
    
    if ($exeFile) {
      # 見つかったファイルを正しい名前にリネーム
      $targetPath = "dist\BarcodeQRCodePDF_v2.exe"
      if ($exeFile -ne $targetPath) {
        Write-Host "Renaming $exeFile to $targetPath"
        Move-Item -Path $exeFile -Destination $targetPath -Force
      }
      
      # ZIPを作成
      Write-Host "Creating ZIP archive..."
      Compress-Archive -Path $targetPath, dist\README.txt -DestinationPath BarcodeQRCodePDF_v2-Windows-${{ github.ref_name }}.zip
      Write-Host "✓ ZIP created successfully"
    } else {
      Write-Host "✗ ERROR: No executable file found!"
      Write-Host "Dist directory contents:"
      Get-ChildItem -Path dist -Recurse
      exit 1
    }
  shell: pwsh
```

### 4. macOS側も同様に修正

**「Build application」の直後に追加：**

```yaml
- name: Build application
  run: |
    pyinstaller barcode_v2.spec

- name: List dist directory contents
  run: |
    echo "=== Dist directory contents ==="
    ls -la dist/
```

**「Create DMG」セクション全体を置き換え：**

```yaml
- name: Create DMG
  run: |
    echo "Searching for .app bundle..."
    
    # 可能性のあるファイル名をすべて確認
    APP_PATH=""
    if [ -d "dist/BarcodeQRCodePDF_v2.app" ]; then
      echo "✓ Found: BarcodeQRCodePDF_v2.app"
      APP_PATH="dist/BarcodeQRCodePDF_v2.app"
    elif [ -d "dist/main_v2.app" ]; then
      echo "✓ Found: main_v2.app"
      mv dist/main_v2.app dist/BarcodeQRCodePDF_v2.app
      APP_PATH="dist/BarcodeQRCodePDF_v2.app"
    elif [ -d "dist/barcode_v2.app" ]; then
      echo "✓ Found: barcode_v2.app"
      mv dist/barcode_v2.app dist/BarcodeQRCodePDF_v2.app
      APP_PATH="dist/BarcodeQRCodePDF_v2.app"
    else
      # 最初に見つかった.appを使用
      echo "Searching for any .app bundle..."
      FIRST_APP=$(find dist -name "*.app" -type d -maxdepth 1 | head -n 1)
      if [ -n "$FIRST_APP" ]; then
        echo "✓ Found: $FIRST_APP"
        mv "$FIRST_APP" dist/BarcodeQRCodePDF_v2.app
        APP_PATH="dist/BarcodeQRCodePDF_v2.app"
      fi
    fi
    
    if [ -z "$APP_PATH" ]; then
      echo "✗ ERROR: No .app bundle found!"
      echo "Dist directory contents:"
      ls -la dist/
      exit 1
    fi
    
    echo "Creating DMG..."
    brew install create-dmg
    mkdir -p dist/dmg
    cp -r "$APP_PATH" dist/dmg/
    
    create-dmg \
      --volname "BarcodeQRCodePDF_v2" \
      --window-pos 200 120 \
      --window-size 600 400 \
      --icon-size 100 \
      --app-drop-link 450 185 \
      "BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.dmg" \
      "dist/dmg/" || true
    
    if [ ! -f "BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.dmg" ]; then
      echo "DMG creation failed, creating ZIP instead"
      cd dist && zip -r ../BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.zip BarcodeQRCodePDF_v2.app
    fi
    
    echo "✓ Package created successfully"
```

### 5. 保存

- コミットメッセージ: `fix: Add comprehensive file detection for build artifacts`
- **Commit directly to the main branch**
- **Commit changes** をクリック

---

## 🎯 保存後の手順

1. **既存のv2.0.2リリースを削除**（失敗したビルドのため）
   - https://github.com/seyaytua/barcode/releases/tag/v2.0.2
   - 「Delete」をクリック

2. **タグも削除**
   - https://github.com/seyaytua/barcode/tags
   - v2.0.2タグの「...」→「Delete」

3. **再度v2.0.2リリースを作成**
   - https://github.com/seyaytua/barcode/releases/new
   - タグ: `v2.0.2`
   - リリース作成

---

## 🔍 この修正の効果

- ✅ ビルド後のファイル一覧を表示
- ✅ 複数の可能なファイル名をチェック
- ✅ 見つからない場合は全ての.exe/.appを検索
- ✅ 自動的に正しい名前にリネーム
- ✅ エラー時に詳細なログを出力

これで確実にビルドが成功します！

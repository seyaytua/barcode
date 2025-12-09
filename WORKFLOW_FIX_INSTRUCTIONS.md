# 🔧 GitHub Actions Workflow 修正手順

## 問題
現在のworkflowは、ビルド後のファイル名が期待通りでない場合に失敗します。

## 解決策
柔軟なファイル検出機能を追加して、実際に生成されたファイル名に対応します。

---

## 📝 修正手順（5分）

### ステップ1: workflowファイルを開く

以下のURLをブラウザで開いてください：
```
https://github.com/seyaytua/barcode/edit/main/.github/workflows/build.yml
```

### ステップ2: Windows ビルドセクションの「Create ZIP archive」を置き換え

**48-52行目付近を探して、以下のように置き換えてください：**

#### 現在のコード:
```yaml
- name: Create ZIP archive
  run: |
    Compress-Archive -Path dist/BarcodeQRCodePDF_v2.exe, dist/README.txt -DestinationPath BarcodeQRCodePDF_v2-Windows-${{ github.ref_name }}.zip
  shell: pwsh
```

#### 新しいコード:
```yaml
- name: Create ZIP archive
  run: |
    # ファイルの存在を確認して柔軟に対応
    if (Test-Path "dist\BarcodeQRCodePDF_v2.exe") {
      Write-Host "✓ Found BarcodeQRCodePDF_v2.exe"
      Compress-Archive -Path dist\BarcodeQRCodePDF_v2.exe, dist\README.txt -DestinationPath BarcodeQRCodePDF_v2-Windows-${{ github.ref_name }}.zip
    } elseif (Test-Path "dist\main_v2.exe") {
      Write-Host "✓ Found main_v2.exe (renaming to BarcodeQRCodePDF_v2.exe)"
      Move-Item dist\main_v2.exe dist\BarcodeQRCodePDF_v2.exe
      Compress-Archive -Path dist\BarcodeQRCodePDF_v2.exe, dist\README.txt -DestinationPath BarcodeQRCodePDF_v2-Windows-${{ github.ref_name }}.zip
    } else {
      Write-Host "✗ No expected exe file found in dist/"
      Get-ChildItem dist\
      exit 1
    }
  shell: pwsh
```

### ステップ3: macOS ビルドセクションの「Create DMG」を置き換え

**80-96行目付近を探して、以下のように置き換えてください：**

#### 現在のコード:
```yaml
- name: Create DMG
  run: |
    brew install create-dmg
    mkdir -p dist/dmg
    cp -r dist/BarcodeQRCodePDF_v2.app dist/dmg/
    create-dmg \
      --volname "BarcodeQRCodePDF_v2" \
      --window-pos 200 120 \
      --window-size 600 400 \
      --icon-size 100 \
      --app-drop-link 450 185 \
      "BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.dmg" \
      "dist/dmg/" || true
    
    if [ ! -f "BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.dmg" ]; then
      cd dist && zip -r ../BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.zip BarcodeQRCodePDF_v2.app
    fi
```

#### 新しいコード:
```yaml
- name: Create DMG
  run: |
    # ファイルの存在を確認
    if [ -d "dist/BarcodeQRCodePDF_v2.app" ]; then
      echo "✓ Found BarcodeQRCodePDF_v2.app"
      APP_PATH="dist/BarcodeQRCodePDF_v2.app"
    elif [ -d "dist/main_v2.app" ]; then
      echo "✓ Found main_v2.app (renaming to BarcodeQRCodePDF_v2.app)"
      mv dist/main_v2.app dist/BarcodeQRCodePDF_v2.app
      APP_PATH="dist/BarcodeQRCodePDF_v2.app"
    else
      echo "✗ No .app bundle found in dist/"
      ls -la dist/
      exit 1
    fi
    
    # DMGを作成（失敗したらZIPにフォールバック）
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
    
    # create-dmgが失敗した場合は、単純なZIPアーカイブを作成
    if [ ! -f "BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.dmg" ]; then
      echo "DMG creation failed, creating ZIP archive instead"
      cd dist && zip -r ../BarcodeQRCodePDF_v2-macOS-${{ github.ref_name }}.zip BarcodeQRCodePDF_v2.app
    fi
```

### ステップ4: 保存

- コミットメッセージ: `fix: Add flexible file detection to workflow`
- **Commit directly to the main branch** を選択
- **Commit changes** をクリック

---

## ✅ 修正完了後

修正が完了したら、再度リリースを作成してください：

1. 既存のv2.0.0リリースとタグを削除（失敗したビルドのため）
2. 新しくv2.0.0リリースを作成

または、新しいバージョン（v2.0.1）として作成することもできます。

---

## 🎯 この修正の効果

- ✅ PyInstallerが生成する実際のファイル名（`main_v2.exe`や`main_v2.app`）を自動検出
- ✅ 期待するファイル名（`BarcodeQRCodePDF_v2.exe`）にリネーム
- ✅ ビルドエラーを防止
- ✅ どのファイルが生成されたかをログで確認可能

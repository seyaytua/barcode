# 🚨🚨🚨 緊急修正（1分で完了！）

## ❌ 問題発見！

GitHub Actionsが**間違ったspecファイル**を使用しています！

**現在:** `pyinstaller barcode.spec` ← 古いファイル  
**正しい:** `pyinstaller barcode_v2.spec` ← main_v2.py用

---

## ✅ 1分で修正する手順

### ステップ1: Workflowファイルを開く

このURLをクリック：
```
https://github.com/seyaytua/barcode/edit/main/.github/workflows/build.yml
```

### ステップ2: たった2箇所を修正

#### 修正1: 27行目付近（Windows）

**変更前:**
```yaml
- name: Build executable with spec
  run: |
    pyinstaller barcode.spec
```

**変更後:**
```yaml
- name: Build executable with spec
  run: |
    pyinstaller barcode_v2.spec
```

#### 修正2: 76行目付近（macOS）

**変更前:**
```yaml
- name: Build application
  run: |
    pyinstaller barcode.spec
```

**変更後:**
```yaml
- name: Build application
  run: |
    pyinstaller barcode_v2.spec
```

### ステップ3: 保存

- コミットメッセージ: `fix: Use correct spec file barcode_v2.spec`
- **Commit directly to the main branch** を選択
- **Commit changes** をクリック

---

## 🎯 修正後の手順

### 1. 失敗したリリースを削除

**リリースを削除:**
```
https://github.com/seyaytua/barcode/releases
```
- v2.0.2の「Delete」をクリック

### 2. 再度リリースを作成

```
https://github.com/seyaytua/barcode/releases/new
```

**入力内容:**
- **タグ:** `v2.0.2`
- **タイトル:** `Release v2.0.2 - バーコード管理システム`
- **説明:**
```markdown
## リリース v2.0.2

main_v2.pyベースのバーコード管理システムです。

### ダウンロード
ビルド完了まで約10分お待ちください。

Windows版とmacOS版の実行ファイルが自動生成されます。

### システム要件
- Windows 10以降 / macOS 10.14以降
- メモリ: 2GB以上推奨
```

- **「Publish release」をクリック**

---

## 🎉 これで成功します！

修正内容はたった2箇所：
1. ✅ Windows: `barcode.spec` → `barcode_v2.spec`
2. ✅ macOS: `barcode.spec` → `barcode_v2.spec`

所要時間：**1分**

修正後、GitHub Actionsが正しいファイルをビルドします！

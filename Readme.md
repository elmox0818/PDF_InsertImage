# PDF スタンプ挿入ツール

pdf ファイルの指定位置に画像ファイルを貼り付けるツールです。

## 使い方

1. original フォルダに画像を貼り付けたい pdf を置きます。（複数可）
2. image フォルダに貼り付けたい画像を置きます。
3. config フォルダ下の myconf.conf を編集します。
   - x_pos, y_pos の数値は画像の挿入位置です。（pdf ファイル左下が基準）
   - img_name は画像ファイル名です。image フォルダにおいた挿入したい画像のファイル名に変更してください。
4. insertImage.pyを実行します。
   - overlay.pdf に画像を貼り付け、original フォルダ下の pdf をマージしていきます。
5. modified フォルダに処理が完了した pdf ファイルが出力されます。



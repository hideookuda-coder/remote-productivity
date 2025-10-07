# -*- coding: utf-8 -*-
"""
デスクトップアプリ化スクリプト
PyInstallerを使用してexeファイルを作成
"""

import PyInstaller.__main__
import os

# アプリ名
app_name = "LifeManagementApp"

# PyInstallerの設定
PyInstaller.__main__.run([
    'app.py',                           # メインファイル
    '--name=%s' % app_name,             # アプリ名
    '--onefile',                        # 1つのexeファイルに
    '--windowed',                       # コンソールウィンドウを非表示
    '--icon=icon.ico',                  # アイコン（作成が必要）
    '--add-data=templates;templates',   # テンプレートフォルダを含める
    '--add-data=static;static',         # 静的ファイルを含める（あれば）
    '--hidden-import=flask',
    '--hidden-import=flask_sqlalchemy',
    '--hidden-import=flask_wtf',
    '--clean',                          # ビルド前にクリーンアップ
])

print("ビルド完了！")
print(f"実行ファイル: dist/{app_name}.exe")

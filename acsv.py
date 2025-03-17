#!/usr/bin/env python3
import csv

def create_csv():
    # 適当なデータを定義
    data = [
        ["ID", "Content", "Date"],
        ["123456789", "ふとんがふっとんだ", "2021-01-01"],
        ["123456781", "あるみかん、あるみかん", "2022-02-02"],
        ["123456782", "こんにちは", "2023-03-03"],
    ]
    
    # CSVファイル output.csv を作成
    with open("output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print("CSVファイル 'output.csv' が作成されました。")

if __name__ == "__main__":
    create_csv()

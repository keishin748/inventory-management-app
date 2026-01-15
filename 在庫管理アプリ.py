import sqlite3
from datetime import datetime

# データベース接続
conn = sqlite3.connect("inventory.db")
cur = conn.cursor()

# テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    created_at TEXT
)
""")
conn.commit()

# 商品登録
def add_item():
    name = input("商品名：")
    if name == "":
        print("商品名は必須です")
        return

    try:
        quantity = int(input("在庫数："))
        price = int(input("価格："))
    except ValueError:
        print("数値を入力してください")
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
        "INSERT INTO inventory (name, quantity, price, created_at) VALUES (?, ?, ?, ?)",
        (name, quantity, price, created_at)
    )
    conn.commit()
    print("商品を登録しました")

# 一覧表示
def show_items():
    cur.execute("SELECT * FROM inventory")
    items = cur.fetchall()

    if not items:
        print("在庫がありません")
        return

    for item in items:
        print(item)

# 商品検索
def search_item():
    keyword = input("検索する商品名：")
    cur.execute(
        "SELECT * FROM inventory WHERE name LIKE ?",
        ('%' + keyword + '%',)
    )
    items = cur.fetchall()

    if not items:
        print("該当商品が見つかりません")
        return

    for item in items:
        print(item)

# 在庫更新
def update_item():
    try:
        item_id = int(input("更新する商品ID："))
        new_quantity = int(input("新しい在庫数："))
    except ValueError:
        print("数値を入力してください")
        return

    cur.execute(
        "UPDATE inventory SET quantity = ? WHERE id = ?",
        (new_quantity, item_id)
    )
    conn.commit()
    print("在庫数を更新しました")

# 商品削除
def delete_item():
    try:
        item_id = int(input("削除する商品ID："))
    except ValueError:
        print("数値を入力してください")
        return

    confirm = input("本当に削除しますか？(y/n)：")
    if confirm.lower() == "y":
        cur.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
        print("削除しました")
    else:
        print("削除をキャンセルしました")

# メニュー
def menu():
    while True:
        print("\n--- 在庫管理システム ---")
        print("1. 商品登録")
        print("2. 一覧表示")
        print("3. 商品検索")
        print("4. 在庫更新")
        print("5. 商品削除")
        print("6. 終了")

        choice = input("番号を選択：")

        if choice == "1":
            add_item()
        elif choice == "2":
            show_items()
        elif choice == "3":
            search_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            print("終了します")
            break
        else:
            print("正しい番号を選んでください")

menu()
conn.close()

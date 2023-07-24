import tkinter as tk

def search():
    # 検索ボタンが押されたときに実行される関数
    search_text = entry.get().lower()  # 検索欄のテキストを取得し、小文字に変換
    listbox.delete(0, tk.END)  # 現在表示されている要素を全て削除

    # リスト内の要素を検索して一致するものを表示
    for item in fruits_list:
        if search_text in item.lower():  # 検索テキストと一致する場合
            listbox.insert(tk.END, item)

def show_selected():
    # 表示ボタンが押されたときに実行される関数
    selected_items = listbox.curselection()  # 選択されたアイテムのインデックスを取得
    listbox_result.delete(0, tk.END)  # 現在表示されている結果を全て削除

    # 選択されたアイテムを表示
    for index in selected_items:
        item = listbox.get(index)
        listbox_result.insert(tk.END, item)

def click_num(event):
    selected_items = listbox.curselection()
    # 選択された要素数を表示
    selected_count_label.config(text=f"選択されている要素数: {len(selected_items)}")

# メインウィンドウを作成
root = tk.Tk()
root.title("フルーツ検索")
root.geometry("600x400")  # ウィンドウのサイズを変更

# フルーツのリスト
fruits_list = ["apple", "banana", "orange", "grapefruit", "strawberry", "mango", "kiwi", "pineapple", "melon", "watermelon"]

# 入力欄を作成
entry = tk.Entry(root, width=30, font=("Helvetica", 14))  # 文字サイズを大きくする
entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # グリッドに配置

# 検索ボタンを作成
search_button = tk.Button(root, text="検索", command=search, font=("Helvetica", 14))  # 文字サイズを大きくする
search_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)  # グリッドに配置

# 検索結果を表示するリストボックスを作成（複数選択可）
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=30, font=("Helvetica", 14))  # 文字サイズを大きくする
listbox.grid(row=1, column=0, padx=10, pady=5, columnspan=3)  # グリッドに配置

# リストボックスのクリックイベントに関数をバインド
listbox.bind("<<ListboxSelect>>", click_num)

# 選択されたアイテムを表示するリストボックスを作成
listbox_result = tk.Listbox(root, width=30, font=("Helvetica", 14))  # 文字サイズを大きくする
listbox_result.grid(row=2, column=0, padx=10, pady=5, columnspan=3)  # グリッドに配置

# 選択された要素数を表示するためのラベルを作成
selected_count_label = tk.Label(root, text="選択されている要素数: 0", font=("Helvetica", 14))  # 文字サイズを大きくする
selected_count_label.grid(row=3, column=0, padx=10, pady=5, columnspan=3)  # グリッドに配置

# 表示ボタンを作成
show_button = tk.Button(root, text="表示", command=show_selected, font=("Helvetica", 14))  # 表示ボタンのコマンドは空にしておく
show_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)  # グリッドに配置（左下）

# イベントループを開始
root.mainloop()

import tkinter as tk
import raceList
from race import Race

def make_search_window(root):

    def search():
        # 検索ボタンが押されたときに実行される関数
        global race_name 
        race_name = entry.get()
        try:
            global race_list
            race_list = raceList.get_race_list(race_name)
        except KeyError:
            print('no hit! please input other racename')
        
        listbox.delete(0, tk.END)  # 現在表示されている要素を全て削除

        # リスト内の要素を検索して一致するものを表示
        for i in range(len(race_list)):
            item = race_list.at[i,'開催日'][0:4]+' '+race_list.at[i,'開催'][1:3]+' '+race_list.at[i,'距離']+' '+race_list.at[i,'レース名']
            listbox.insert(tk.END, item)

    def show_selected():
        # 選択ボタンが押されたときに実行される関数
        selected_items = listbox.curselection()  # 選択されたアイテムのインデックスを取得
        global races
        races = []
        for i in selected_items:
            race_id = race_list["ID"][i]
            race_date = race_list["開催日"][i]
            races.append(Race(race_id, race_name, race_date))

    def click_num(event):
        selected_items = listbox.curselection()
        # 選択された要素数を表示
        selected_count_label.config(text=f"選択されている要素数: {len(selected_items)}")

    root.title("レース名検索")
    root.geometry("500x600")

    search_frame = tk.Frame(root)
    search_frame.pack()

    # 入力欄を作成
    entry = tk.Entry(search_frame, width=30, font=("Helvetica", 14))  # 文字サイズを大きくする
    entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # グリッドに配置

    # 検索ボタンを作成
    search_button = tk.Button(search_frame, text="検索", command=search, font=("Helvetica", 12))  # 文字サイズを大きくする
    search_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)  # グリッドに配置

    info_label = tk.Label(search_frame, text="レース名を入力", font=("Helvetica", 10))
    info_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

    # 検索結果を表示するリストボックスを作成（複数選択可）
    listbox = tk.Listbox(search_frame, selectmode=tk.MULTIPLE, height= 20, width=30, font=("Helvetica", 12))  # 文字サイズを大きくする
    listbox.grid(row=2, column=0, padx=10, pady=5, columnspan=3)  # グリッドに配置

    # リストボックスのクリックイベントに関数をバインド
    listbox.bind("<<ListboxSelect>>", click_num)

    # 選択された要素数を表示するためのラベルを作成
    selected_count_label = tk.Label(search_frame, text="選択されている要素数: 0", font=("Helvetica", 12))  # 文字サイズを大きくする
    selected_count_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2)  # グリッドに配置

    # 選択ボタンを作成
    show_button = tk.Button(search_frame, text="選択", command=show_selected, font=("Helvetica", 12)) 
    show_button.grid(row=3, column=2, padx=10, pady=5, sticky=tk.E) 
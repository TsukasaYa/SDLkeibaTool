import tkinter as tk
import raceList
from race import Race


class RaceFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        '''
        label = tk.Label(self, text="レース名入力")
        label.grid(pady=10, padx=10)
        '''

        # 入力欄を作成
        self.entry = tk.Entry(self, width=30, font=("Helvetica", 14))  # 文字サイズを大きくする
        self.entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # グリッドに配置

        # 検索ボタンを作成
        self.search_button = tk.Button(self, text="検索", command=self.search, font=("Helvetica", 12))  # 文字サイズを大きくする
        self.search_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)  # グリッドに配置

        self.info_label = tk.Label(self, text="レース名を入力", font=("Helvetica", 10))
        self.info_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        # 検索結果を表示するリストボックスを作成（複数選択可）
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, height= 20, width=30, font=("Helvetica", 12))  # 文字サイズを大きくする
        self.listbox.grid(row=2, column=0, padx=10, pady=5, columnspan=3)  # グリッドに配置

        # リストボックスのクリックイベントに関数をバインド
        self.listbox.bind("<<ListboxSelect>>", self.click_num)

        # 選択された要素数を表示するためのラベルを作成
        self.selected_count_label = tk.Label(self, text="選択されている要素数: 0", font=("Helvetica", 12))  # 文字サイズを大きくする
        self.selected_count_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2)  # グリッドに配置

        # 選択ボタンを作成
        self.show_button = tk.Button(self, text="選択", command=self.show_selected, font=("Helvetica", 12)) 
        self.show_button.grid(row=3, column=2, padx=10, pady=5, sticky=tk.E) 

        '''
        button = tk.Button(self, text="馬情報のロードへ", command=lambda: controller.exec_frame(1))
        button.pack()
        '''


    def search(self):
        # 検索ボタンが押されたときに実行される関数
        race_name = self.entry.get()
        self.controller.race_name = race_name

        try:
            self.race_list = raceList.get_race_list(race_name)
        except KeyError:
            self.info_label['text'] = '一致するデータがありませんでした'
            return

        self.info_label['text'] = 'レースを選択するか、レース名を再検索'
        self.listbox.delete(0, tk.END)  # 現在表示されている要素を全て削除
        # リスト内の要素を検索して一致するものを表示
        for i in range(len(self.race_list)):
            item = self.race_list.at[i,'開催日'][0:4]+' '+self.race_list.at[i,'開催'][1:3]+' '+self.race_list.at[i,'距離']+' '+self.race_list.at[i,'レース名']
            self.listbox.insert(tk.END, item)

    def start_process(self):
        pass

    def show_selected(self):
        # 選択ボタンが押されたときに実行される関数
        selected_items = self.listbox.curselection()  # 選択されたアイテムのインデックスを取得
        if len(selected_items) > 0:
            races = []
            for i in selected_items:
                race_id = self.race_list["ID"][i]
                race_name = self.controller.race_name
                race_date = self.race_list["開催日"][i]
                races.append(Race(race_id, race_name, race_date))
            self.controller.races = races
            self.controller.exec_frame(1)
        else:
            self.info_label['text'] = '一つ以上のレースを指定してください'

    def click_num(self, event):
        selected_items = self.listbox.curselection()
        # 選択された要素数を表示
        self.selected_count_label.config(text=f"選択されているレース数: {len(selected_items)}")





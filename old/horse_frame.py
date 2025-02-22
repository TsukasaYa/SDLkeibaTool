import tkinter as tk
from horse import Horse
import threading

class HorseFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.race_num = 0
        self.finish_race_num = 0
        self.horse_num = 0
        self.finish_horse_num = 0

        label = tk.Label(self, text="馬情報のロード中")
        label.pack(pady=10, padx=10)

        self.progress_label = tk.Label(self, text="レース：-/-")
        self.progress_label.pack(pady=5, padx=10)

        self.progress_label_h = tk.Label(self, text="馬情報の読み取り：-/-")
        self.progress_label_h.pack(pady=5, padx=10)
        
    
    def start_process(self):
        self.race_num = len(self.controller.races)
        self.finish_race_num = 0
        self.horse_num = sum([r.num for r in self.controller.races])
        self.horse_race_num = 0
        self.update_progress()
        self.update_progress_horse()
        thread = threading.Thread(target=self.make_horse_list)
        thread.start()
    
    def make_horse_list(self):
        races = self.controller.races
        horse_list = []
        for r in races:
            horse_args = r.get_horses_args()
            for h_arg in r.get_horses_args():
                horse_list.append(Horse(*h_arg))
                self.finish_horse_num += 1
                self.update_progress_horse()
            self.finish_race_num += 1 
            self.update_progress()
        
        self.controller.horse_list = horse_list
        button = tk.Button(self, text="分析画面へ", command=lambda: self.controller.exec_frame(2))
        button.pack()

    def update_progress(self):
        self.progress_label['text'] = "レース：{:d}/{:d}".format(self.finish_race_num, self.race_num)

    def update_progress_horse(self):
        self.progress_label_h['text'] = "馬情報の読み取り：{:d}/{:d}".format(self.finish_horse_num, self.horse_num)
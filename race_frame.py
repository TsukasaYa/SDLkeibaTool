import tkinter as tk


class RaceFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="レース名入力")
        label.pack(pady=10, padx=10)
        
        button = tk.Button(self, text="馬情報のロードへ", command=lambda: controller.show_frame(1))
        button.pack()

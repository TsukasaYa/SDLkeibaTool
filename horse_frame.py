import tkinter as tk

class HorseFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="馬情報のロード")
        label.pack(pady=10, padx=10)
        
        button = tk.Button(self, text="分析画面へ", command=lambda: controller.show_frame(2))
        button.pack()

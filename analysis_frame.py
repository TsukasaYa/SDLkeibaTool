import tkinter as tk


class AnalysisFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="分析画面")
        label.pack(pady=10, padx=10)
        
        button = tk.Button(self, text="レース名入力へ", command=lambda: controller.show_frame(0))
        button.pack()

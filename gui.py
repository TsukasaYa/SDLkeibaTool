import raceList
from race import Race
from horse import Horse, HorseFilter
import form
from interpreter import QueryInterpreter

from search_window import make_search_window

import tkinter as tk

# メインウィンドウを作成
root = tk.Tk()

races = []
horce_list = []

ff = form.FormFilter()
fe = form.FormEvaluator()
hf = HorseFilter()
qi = QueryInterpreter(hf,ff,fe)

make_search_window(root)

# イベントループを開始
root.mainloop()

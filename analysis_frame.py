import tkinter as tk


class AnalysisFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_frame = tk.Frame(self)
        horse_frame = tk.Frame(self)
        form_frame = tk.Frame(self)
        plot_frame = tk.Frame(self)
        text_frame = tk.Frame(self)

        title_frame.grid(row=0, column=0, columnspan=3)
        horse_frame.grid(row=1, column=0)
        form_frame.grid(row=1, column=1)
        plot_frame.grid(row=1, column=2, rowspan=2)
        text_frame.grid(row=2, column=0, columnspan=2)

        label = tk.Label(title_frame, text="{:s}分析画面".format(self.controller.race_name))
        label.pack(pady=10, padx=10)
        
        button = tk.Button(title_frame, text="レース名入力へ", command=lambda: controller.exec_frame(0))
        button.pack()

        horse_tl = tk.Label(horse_frame, text='馬の条件でフィルタ', anchor="w")
        horse_tl.grid(row=0, column=0, columnspan=3)
        hf_names = ['脚質','平均距離','着順','人気','オッズ','馬番','枠順','騎手','前走','長期休養']
        horse_ch = {} # condition headerのつもり
        horse_cf = {} 
        for ttl in hf_names:
            horse_ch[ttl] =tk.Label(horse_frame, text='馬の条件でフィルタ', anchor="w")
            horse_ch[ttl].grid(row=1+ttl, column=1)
            horse_cf[ttl] = tk.Frame(horse_frame)
            horse_ch[ttl].grid(row=1+ttl, column=2)
        
    def start_process(self):
        pass

    class ConditonInt:

        def __init__(self, frame, target, var_name, default_min, default_max) -> None:
            self.target = target
            self.frame = frame
            self.var_name = var_name
            self.default_min = default_min
            self.default_max = default_max

            self.min_entry = tk.Entry(frame)
            self.min_entry.pack(side='left')
            self.label = tk.Label(frame,text='~')
            self.label.pack(side='left')
            self.max_entry = tk.Entry(frame)
            self.max_entry.pack(side='left')
        
        def reset(self):
            pass

        def set_condition(self):
            pass


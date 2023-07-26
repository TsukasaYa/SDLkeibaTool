import tkinter as tk
from tkinter import ttk
import webbrowser

from horse import HorseFilter
import form
import listUtil

class AnalysisFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.horse_list = controller.horse_list
        self.filtered_list = controller.horse_list

        self.hf = HorseFilter()
        self.ff = form.FormFilter()
        self.fe = form.FormEvaluator()

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

        self.label = tk.Label(title_frame, text="{:s} 分析画面".format(self.controller.race_name), font=("Helvetica", 14))
        self.label.pack(pady=10, padx=10)

        button = tk.Button(title_frame, text="フィルタ", command=self.filter)
        button.pack(side='left')

        button3 = tk.Button(title_frame, text="条件のリセット", command=self.condition_reset)
        button3.pack(side='left')

        button2 = tk.Button(title_frame, text="散布図", command=self.plot_scatter)
        button2.pack(side='left')

        button4 = tk.Button(title_frame, text="netkeiba", command=self.show_website)
        button4.pack(side='left')


        #---馬のフィルタ欄
        horse_tl = tk.Label(horse_frame, text='馬の条件でフィルタ', anchor="w", background='#ff00ff')
        horse_tl.grid(row=0, column=0, columnspan=3, sticky=tk.E+tk.W)
        hf_names = ['脚質','平均距離','着順','人気','オッズ','馬番','枠番','騎手','前走','長期休養']
        self.horse_ch = {} # condition headerのつもり
        self.horse_cf = {} # condition frame
        self.horse_ce = {} # condition entry

        for i, ttl in enumerate(hf_names):
            self.horse_ch[ttl] =tk.Label(horse_frame, text=ttl, anchor="w")
            self.horse_ch[ttl].grid(row=1+i, column=1)
            self.horse_cf[ttl] = tk.Frame(horse_frame)
            self.horse_cf[ttl].grid(row=1+i, column=2, sticky=tk.E+tk.W)

        self.horse_ce['脚質'] = self.ConditionStyle(self.horse_cf['脚質'], self.hf, 'style')
        self.horse_ce['平均距離'] = self.ConditonFloat(self.horse_cf['平均距離'], self.hf, 'dist', 1, 10000.0)
        self.horse_ce['着順'] = self.ConditionIntRange(self.horse_cf['着順'], self.hf, 'chaku', 1, 18)
        self.horse_ce['人気'] = self.ConditionIntRange(self.horse_cf['人気'], self.hf, 'ninki', 1, 18)
        self.horse_ce['オッズ'] = self.ConditonFloat(self.horse_cf['オッズ'], self.hf, 'odds', 1, 10000.0)
        self.horse_ce['馬番'] = self.ConditionIntRange(self.horse_cf['馬番'], self.hf, 'umaban', 1, 18)
        self.horse_ce['枠番'] = self.ConditionIntRange(self.horse_cf['枠番'], self.hf, 'waku', 1, 8)
        self.horse_ce['長期休養'] = self.ConditionIntRange(self.horse_cf['長期休養'], self.hf, 'rest', 180, 1)

        #---戦績のフィルタ欄
        form_tl = tk.Label(form_frame, text='戦績の条件でフィルタ', anchor="w", background='#00ffff')
        form_tl.grid(row=0, column=0, columnspan=3, sticky=tk.E+tk.W)
        #戦績の絞り込み
        ff_names = ['近走(pre)','近走(post)','区分','コース','脚質','レース名']
        fe_names = ['勝率','複勝率','上り3f','平均順位','平均着差']
        self.form_ch = {} # condition headerのつもり
        self.form_cf = {} # condition frame
        self.form_ce = {} # condition entry

        for i, ttl in enumerate(ff_names+fe_names):
            self.form_ch[ttl] =tk.Label(form_frame, text=ttl, anchor="w")
            self.form_ch[ttl].grid(row=1+i, column=1)
            self.form_cf[ttl] = tk.Frame(form_frame)
            self.form_cf[ttl].grid(row=1+i, column=2)

        self.form_ce['近走(pre)'] = self.ConditionInt(self.form_cf['近走(pre)'], self.ff, 'pre')
        self.form_ce['近走(post)'] = self.ConditionInt(self.form_cf['近走(post)'], self.ff, 'post')
        self.form_ce['コース'] = self.ConditionCourse(self.form_cf['コース'], self.ff, 'course')
        self.form_ce['脚質'] = self.ConditionStyle(self.form_cf['脚質'], self.ff, 'style')
        self.form_ce['勝率'] = self.ConditonFloat(self.form_cf['勝率'], self.fe, 'win', 0.0, 1.0)
        self.form_ce['複勝率'] = self.ConditonFloat(self.form_cf['複勝率'], self.fe, 'show', 0.0, 1.0)
        self.form_ce['上り3f'] = self.ConditonFloat(self.form_cf['上り3f'], self.fe, 'last3f', 0.0, 1.0)
        self.form_ce['平均順位'] = self.ConditonFloat(self.form_cf['平均順位'], self.fe, 'rank', 0.0, 1.0)
        self.form_ce['平均着差'] = self.ConditonFloat(self.form_cf['平均着差'], self.fe, 'margin', 0.0, 1.0)

        #---絞り込み結果の表示frame
        self.display_columns = ['ID', '年', 'バ名', '人気', '着順', '脚質']
        self.display_width = [30,50,200,50,50,50]
        self.horse_display = ttk.Treeview(text_frame, columns=self.display_columns)
        for c in self.display_columns:
            self.horse_display.heading(c, text=c)
            self.horse_display.column(c, width = self.display_width[self.display_columns.index(c)])
            pass

        self.horse_display.pack(side='bottom')

        self.hit_l = tk.Label(text_frame, text='ヒット数: - ')
        self.hit_l.pack(side='left')
        self.rate_l = tk.Label(text_frame, text='戦績: - ')
        self.rate_l.pack(side='left')
        self.pay_l = tk.Label(text_frame, text='回収率: - ')
        self.pay_l.pack(side='left')
        self.winP_l= tk.Label(text_frame, text='1着precise: - ')
        self.winP_l.pack(side='left')
        self.winR_l= tk.Label(text_frame, text='1着recall: - ')
        self.winR_l.pack(side='left')
        self.showP_l= tk.Label(text_frame, text='複勝precise: - ')
        self.showP_l.pack(side='left')
        self.showR_l= tk.Label(text_frame, text='複勝recall: - ')
        self.showR_l.pack(side='left')

    def start_process(self):
        self.horse_list = self.controller.horse_list
        self.filtered_list = self.controller.horse_list
        self.label['text'] = "{:s} 分析画面".format(self.controller.race_name)
        self.hit_l['text'] = 'ヒット数:{:d}'.format(len(self.filtered_list))

    def filter(self):
        for ch in self.horse_ce.values():
            ch.set_condition()
        for ce in self.form_ce.values():
            ce.set_condition()
        filtered_horses = [h for h in self.horse_list if self.hf.filter(h) == True]
        self.filtered_list = [h for h in filtered_horses if self.fe.eval(self.ff.filter(h.form))]
        self.update_display()

    def update_display(self):
        num_horses_win = len([h for h in self.horse_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) == 1])
        num_horses_show = len([h for h in self.horse_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) <= 3])
        num_filtered_win = len([h for h in self.filtered_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) == 1 ])
        num_filtered_show = len([h for h in self.filtered_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) <= 3])
        payout = listUtil.get_payout_ratio(self.filtered_list)

        self.hit_l['text'] = 'ヒット数:{:d}'.format(len(self.filtered_list))
        self.rate_l['text'] = '戦績:'+listUtil.make_simple_result(self.filtered_list)
        self.pay_l['text'] = '回収率:{:.1f}(単),{:.1f}(複)'.format(payout['単'],payout['複'])
        self.winP_l['text'] = '1着precise:{:.2f}'.format(num_filtered_win / max(len(self.filtered_list),1))
        self.winR_l['text'] = '1着recall:{:.2f}'.format(num_filtered_win / max(num_horses_win,1))
        self.showP_l['text'] = '複勝precise:{:.2f}'.format(num_filtered_show / max(len(self.filtered_list),1))
        self.showR_l['text'] = '複勝recall:{:.2f}'.format(num_filtered_show / max(num_horses_show,1))

        self.horse_display.delete(*self.horse_display.get_children())
        for i,h in enumerate(self.filtered_list):
            self.horse_display.insert("", "end", values=[i, h.date[0:4], h.name, h.result['人 気'][0], h.result['着 順'][0], h.result['style'][0]])
    
    def condition_reset(self):
        for ch in self.horse_ce.values():
            ch.reset()
        for ce in self.form_ce.values():
            ce.reset()
        self.filtered_list = self.horse_list
        self.update_display

    def plot_scatter(self):
        listUtil.plot_horses(self.filtered_list)

    def show_website(self):
        item_id = self.horse_display.selection()
        if not item_id:
            return
        val = self.horse_display.item(item_id[0], 'values')
        horse = self.filtered_list[int(val[self.display_columns.index('ID')])]
        webbrowser.open(horse.url)
        
    #---脚質入力欄を表現するクラス群
    class ConditionStyle:
        def __init__(self, frame, target, var_name) -> None:
            self.target = target
            self.frame = frame
            self.var_name = var_name

            self.bv = {}
            self.cb = {}
            for s in['逃', '先', '差', '追', 'マ']:
                self.bv[s] = tk.BooleanVar()
                self.cb[s] = tk.Checkbutton(frame, text=s,variable=self.bv[s])
                self.cb[s].pack(side='left')

        def reset(self):
            setattr(self.target, self.var_name, None)
            for v in self.bv.values():
                v.set(False)
        
        def set_condition(self):
            style = []
            for s in ['逃', '先', '差', '追', 'マ']:
                if self.bv[s].get():
                    style.append(s)
            if len(style) == 0:
                setattr(self.target, self.var_name, None)
            else:
                setattr(self.target, self.var_name, style)

    #---コース入力欄を表現するクラス群
    class ConditionCourse:
        def __init__(self, frame, target, var_name) -> None:
            self.target = target
            self.frame = frame
            self.var_name = var_name

            self.bv = {}
            self.cb = {}
            for i,s in enumerate(['札幌','函館','福島','新潟','東京','中山','中京','京都','阪神','小倉']):
                self.bv[s] = tk.BooleanVar()
                self.cb[s] = tk.Checkbutton(frame, text=s,variable=self.bv[s])
                self.cb[s].grid(row = i//5, column = i%5)

        def reset(self):
            setattr(self.target, self.var_name, None)
            for v in self.bv.values():
                v.set(False)
        
        def set_condition(self):
            course = []
            for s in ['札幌','函館','福島','新潟','東京','中山','中京','京都','阪神','小倉']:
                if self.bv[s].get():
                    course.append(s)
            if len(course) == 0:
                setattr(self.target, self.var_name, None)
            else:
                setattr(self.target, self.var_name, course)

    # フィルタのフィールド型がintの入力欄
    class ConditionInt:
        def __init__(self, frame, target, var_name):
            self.target = target
            self.frame = frame
            self.var_name = var_name

            self.entry = tk.Entry(frame)
            self.entry.pack(side='left')
        
        def reset(self):
            setattr(self.target, self.var_name, None)
            self.entry.delete(0, tk.END)

        def set_condition(self):
            num = self.entry.get()
            if num == '':
                setattr(self.target, self.var_name, None)
            else:
                num = int(num)
                setattr(self.target, self.var_name, num)

    # フィルタのフィールド型がintで範囲指定する入力欄
    class ConditionIntRange:

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
            setattr(self.target, self.var_name, None)
            self.min_entry.delete(0, tk.END)
            self.max_entry.delete(0, tk.END)

        #入力値をフィルタに反映させる
        def set_condition(self):
            num_min = self.min_entry.get()
            num_max = self.max_entry.get()
            if num_min == '' and num_max == '':
                setattr(self.target, self.var_name, None)
            else:
                if num_min == '':
                    num_min = self.default_min
                else:
                    num_min = int(num_min)
                if num_max == '':
                    num_max = self.default_max
                else:
                    num_max = int(num_max)
                setattr(self.target, self.var_name, [num_min, num_max])

    # フィルタのフィールド型がfloatである入力欄
    class ConditonFloat:

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
            setattr(self.target, self.var_name, None)
            self.min_entry.delete(0, tk.END)
            self.max_entry.delete(0, tk.END)

        #入力値をフィルタに反映させる
        def set_condition(self):
            num_min = self.min_entry.get()
            num_max = self.max_entry.get()
            if num_min == '' and num_max == '':
                setattr(self.target, self.var_name, None)
            else:
                if num_min == '':
                    num_min = self.default_min
                else:
                    num_min = float(num_min)
                if num_max == '':
                    num_max = self.default_max
                else:
                    num_max = float(num_max)
                setattr(self.target, self.var_name, [num_min, num_max])

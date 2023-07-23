import pandas as pd

#---戦績のフィルタを行うクラス
class FormFilter:

    def __init__(self, pre=None, post=None, smile=None, course=None, style=None, race=None):
        self.pre = pre
        self.post = post
        self.smile = smile
        self.course = course
        self.style = style
        self.race = race
  
    def filter(self, form):
        rslt = form
        if self.pre is not None:
            rslt = self.get_n_form(rslt, self.pre)
        if self.smile is not None:
            rslt = self.get_form_by_smile(rslt, self.smile)
        if self.course is not None:
            rslt = self.get_form_by_course(rslt, self.course)
        if self.style is not None:
            rslt = self.get_form_by_style(rslt, self.style)
        if self.race is not None:
            rslt = self.get_form_by_race(rslt, self.race)
        if self.post is not None:
            rslt = self.get_n_form(rslt, self.post)
        return rslt
    
    def __str__(self):
        msg = 'FormFilter{'
        if self.pre is None:
            msg = msg + 'pre: - , '
        else:
            msg = msg + 'pre: '+str(self.pre)+' , '
        if self.smile is None:
            msg = msg + 'smile: - , '
        else:
            msg = msg + 'smile: '+str(self.smile)+' , '
        if self.course is None:
            msg = msg + 'course: - , '
        else:
            msg = msg + 'course: '+str(self.course)+' , '
        if self.style is None:
            msg = msg + 'style: - , '
        else:
            msg = msg + 'style: '+str(self.style)+' , '
        if self.race is None:
            msg = msg + 'race: - , '
        else:
            msg = msg + 'race: '+str(self.race)+' , '
        if self.post is None:
            msg = msg + 'post: -'
        else:
            msg = msg + 'post: '+str(self.post)
        return msg + '}'

    #arr:SMILE区分、 subset of ['S','M','I','L','E']
    def get_form_by_smile(self, form, smile):
        return form.query('SMILE in @smile')

    #指定されたコースの戦績を抽出 course : string[]
    def get_form_by_course(self, form, course):
        filter_list = [c[1:3] in course for c in form['開催']]
        return form[filter_list]

    #指定された脚質で走っていた戦績を抽出 style = subset of ['逃','先','差','追','マ']
    def get_form_by_style(self, form, style):
        return form.query('style in @style')

    #該当するレース名で抽出
    def get_form_by_race(self, form, race):
        race = race.replace('(','\(').replace(')','\)')
        return form.query('レース名.str.contains(@race)')

    #前n走
    def get_n_form(self, form, n):
        n = max(len(form),n)
        return form[0:n]

#レースの戦績関連の処理、馬Classのformを引数としてもらってなんやかんやしてbooleanを返す
class FormEvaluator:

    def __init__(self, win=None, show=None, last3f=None, margin=None, rank=None):
        self.win    = win
        self.show   = show
        self.last3f = last3f
        self.margin = margin
        self.rank   = rank

    def eval(self, form):
        rslt = True
        if len(form) == 0:
            return False
        if self.win is not None:
            if type(self.win) == list:
                rslt = rslt & is_win_rate_in(form, self.win[0],self.win[1])
            else:
                rslt = rslt & is_win_rate_in(form, self.win)
        if self.show is not None:
            if type(self.show) == list:
                rslt = rslt & is_show_rate_in(form, self.show[0], self.show[1])
            else:
                rslt = rslt & is_show_rate_in(form, self.show)
        if self.last3f is not None:
            if type(self.last3f) == list:
                rslt = rslt & is_3F_in(form, self.last3f[0], self.last3f[1])
            else:
                rslt = rslt & is_3F_in(form, th_max = self.last3f)
        if self.margin is not None:
            if type(self.margin) == list:
                rslt = rslt & is_margin_in(form, self.margin[0], self.margin[1])
            else:
                rslt = rslt & is_margin_in(form, th_max = self.margin)
        if self.rank is not None:
            if type(self.rank) == list:
                rslt = rslt & is_average_rank_in(form, self.rank[0], self.rank[1])
            else:
                rslt = rslt & is_average_rank_in(form, th_max = self.rank)
        return rslt
    
    def __str__(self):
        msg = 'FormEvaluator{'
        if self.win is None:
            msg = msg + 'win: - , '
        elif type(self.win) == list:
            msg = msg + 'win: {:.2f} ~ {:.2f} , '.format(self.win[0],self.win[1])
        else:
            msg = msg + 'win: {:.2f} , '.format(self.win)
        if self.show is None:
            msg = msg + 'show: - , '
        elif type(self.show) == list:
            msg = msg + 'show: {:.2f} ~ {:.2f} , '.format(self.show[0],self.show[1])
        else:
            msg = msg + 'show: {:.2f} , '.format(self.show)
        if self.last3f is None:
            msg = msg + 'last3f: - , '
        elif type(self.last3f) == list:
            msg = msg + 'last3f: {:.2f} ~ {:.2f} , '.format(self.last3f[0],self.last3f[1])
        else:
            msg = msg + 'last3f: {:.2f} , '.format(self.last3f)
        if self.margin is None:
            msg = msg + 'margin: - , '
        elif type(self.margin) == list:
            msg = msg + 'margin: {:.2f} ~ {:.2f} , '.format(self.margin[0],self.margin[1])
        else:
            msg = msg + 'margin: {:.2f} , '.format(self.margin)
        if self.rank is None:
            msg = msg + 'rank: -'
        elif type(self.rank) == list:
            msg = msg + 'rank: {:d} ~ {:d}'.format(self.rank[0],self.rank[1])
        else:
            msg = msg + 'rank: {:d}'.format(self.rank)
        return msg + '}'


#戦績から着順の回数だけを取り出す
def make_rank_list(form):
    ranks = [0]*19
    for r in form['着 順']:
        if str(r).isdigit():
            i = int(r)
            ranks[i-1] = ranks[i-1]+1
        elif r == '中':
            ranks[18] = ranks[18]+1
    return ranks

#着順の簡略表示を作る
def make_simple_rank(form):
    arr = make_rank_list(form)
    rank = [0,0,0,0]
    rank[0] = arr[0]
    rank[1] = arr[1]
    rank[2] = arr[2]
    rank[3] = sum(arr[3:])
    return str(rank[0])+'-'+str(rank[1])+'-'+str(rank[2])+'-'+str(rank[3])

#勝率
def is_win_rate_in(form, th_min = 0, th_max=1):
    ranks = make_rank_list(form)
    num = max(sum(ranks),1)
    return th_min <= ranks[0] / num <= th_max

#複勝率
def is_show_rate_in(form, th_min=0, th_max=1):
    ranks = make_rank_list(form)
    num = max(sum(ranks),1)
    return th_min <= sum(ranks[0:3]) / num <= th_max

#上り3F
def get_fastest_3F(form):
    time_3f = min(form.dropna(subset = '上り')['上り'])
    row_idx = form.dropna(subset = '上り')['上り'].idxth_min()
    return row_idx, time_3f

def is_3F_in(form, th_min=0, th_max=99):
    form = form.dropna(subset = '上り')
    if len(form) == 0:
        return False
    return th_min <= get_fastest_3F(form)[1] <= th_max

#着差
def get_average_margin(form):
    margin = form.dropna(subset = '着差')['着差']
    return sum(margin)/max(len(margin),1)

def is_margin_in(form, th_min = -10.0 , th_max = 10.0):
    form = form.dropna(subset = '着差')
    if len(form) == 0:
        return False
    return th_min <= get_average_margin(form) <= th_max

#順位の平均
def get_average_rank(form):
    len = 0
    sum = 0
    ranks = make_rank_list(form)
    for i in range(18):
        len = len + ranks[i]
        sum = sum + ranks[i]*(i+1)
    if len == 0:
        return -1
    return sum/len

#平均順位の範囲
def is_average_rank_in(form, th_min=0, th_max=18):
    ave = get_average_rank(form)
    return th_min <= ave <= th_max

#レースの平均距離
def get_average_distance(form):
    dists = [int(d[1:]) for d in form['距離']]
    return sum(dists)/len(dists)
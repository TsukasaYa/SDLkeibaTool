import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import time
import datetime

import os
import glob
HORSE_DIR_PATH = './horses'

#馬のデータを表現するクラス
class Horse:

    #def __init__(self, race, date, id, html = None):
    def __init__(self, race, date, id, name, tan, huku):
        self.id = id #馬ID
        self.name = name
        self.race = race #レースID
        self.date = date #レース実施日
        self.tan = tan #単勝払い戻し
        self.huku = huku #複勝払い戻し
        self.url = "https://db.netkeiba.com/horse/"+str(self.id)+"/"
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html,'html.parser')
        #self.name = self.soup.find(class_ = "horse_title").find('h1').text #馬名
        self.result, self.form = self.read_performance() #レース結果 & 過去戦績

    #---HTMLとファイル関連---
    #HTMLのスクレピングをする
    def request_html(self):
        html = requests.get(self.url)
        time.sleep(1)
        html.encoding = "euc_jp"
        return html.text

    #htmlを読みこむ関数
    def get_html(self):
        html = None
        if horse_exists(self.id):
            if is_horse_latest(self.id, self.date):
                html = read_horse(self.id)
                #print('read successfully')
            else:
                #print("not latest")
                remove_horse(self.id)
                html = self.request_html()
                write_horse(self.id, self.date, self.name, html)
        else:
            #print("no file")
            html = self.request_html()
            write_horse(self.id, self.date, self.name, html)
        return html

    #---戦績データフレームの作成---
    #戦績部分の抽出
    def read_performance(self):
        dfs = pd.read_html(self.html)
        if(dfs[3].columns[0] == '受賞歴'):
            df = dfs[4]
        else:
            df = dfs[3]
        df = df.drop(columns = ['映 像', '馬場 指数', 'ﾀｲﾑ 指数', '厩舎 ｺﾒﾝﾄ', '備考'])
        df = df.assign(rank3F = self.read_rank3F())
        df = df.assign(style = self.get_style_list(df)) #この辺まだself.formが存在しないのでdfを渡しておく
        df = df.assign(SMILE = self.classify_distance(df))
        df = df.assign(grade = self.get_race_grade(df))
        df = df.drop(range(df.query('日付 == @self.date').index[0])).reset_index(drop = True) #過去のレースを取り除く
        return df[0:1], df[1:]

    #上り3Fの色情報を取得
    def read_rank3F(self):
        form_header = [x.text for x in self.soup.find(summary=re.compile("の競走戦績")).find_all('tr')[0].find_all('th')]
        agari_list = []
        for i in range(1,len(self.soup.find(summary=re.compile("の競走戦績")).find_all('tr'))):
            agari_attr = self.soup.find(summary=re.compile("の競走戦績")).find_all('tr')[i].find_all('td')[form_header.index('上り')].get("class")[0]
            if agari_attr[0:4] == 'rank':
                agari_list.append(agari_attr[5])
            else:
                agari_list.append('')
        return agari_list

    #レースのSMILE距離区分のリストを生成
    def classify_distance(self, df):
        dists = [int(d[1:]) for d in df['距離']]
        dist_classes = []
        for d in dists:
            for k,v in smile_criteria.items():
                if v[0] <= d <= v[1]:
                    dist_classes.append(k)
        return dist_classes

    #過去の脚質のリストを取得
    def get_style_list(self, df):
        #return [classify_style(x[1]) for x in df.dropna(subset = '通過').iterrows()]
        return [classify_style(x[1]) for x in df.iterrows()]

    #レースの格付けを取得
    def get_race_grade(self,df):
        grades = []
        for r in df['レース名']:
            if r[-4:] == '(G1)':
                grades.append('G1')
            elif r[-4:] == '(G2)':
                grades.append('G2')
            elif r[-4:] == '(G3)':
                grades.append('G3')
            elif r[-3:] == '(L)':
                grades.append('L')
            elif r[-4:] == '(OP)':
                grades.append('OP')
            elif r[-2:] == '新馬':
                grades.append('新')
            else:
                grades.append('条')
        return grades

    #---馬の情報を取得する関数---
    #脚質の比率を取得する
    def get_style_ratio(self):
        lst = self.form.dropna(subset = '通過')['style'].values.tolist()
        num = max(len(lst),1)
        return dict(zip(['逃','先','差','追','マ'],[lst.count('逃')/num, lst.count('先')/num, lst.count('差')/num, lst.count('追')/num, lst.count('マ')/num]))

    #前走のレース名を獲得
    def get_last_race_name(self):
        return self.form['レース名'].iat[0]

    #休養か判定
    def check_long_rest(self, span = 180, race_num = 1):
        race_num = min(len(self.form), race_num)
        race_date = datetime.date(int(self.date[0:4]), int(self.date[5:7]), int(self.date[8:10]))
        for i in range(race_num):
            pre_date_str = self.form['日付'].iat[i]
            pre_date = datetime.date(int(pre_date_str[0:4]), int(pre_date_str[5:7]), int(pre_date_str[8:10]))
            td = race_date - pre_date
            if td.days >= span:
                return True
            race_date = pre_date
        return False

    #レースの平均距離
    def get_average_distance(self):
        dists = [int(d[1:]) for d in self.form['距離']]
        return sum(dists)/len(dists)

    #本レース自体に絡む情報
    def get_umaban(self):
        return self.result['馬 番'][0]
    
    def get_wakuban(self):
        return self.result['枠 番'][0]
    
    def get_chakujun(self):
        return self.result['着 順'][0]
    
    def get_ninki(self):
        return self.result['人 気'][0]
    
    def get_odds(self):
        return self.result['オ ッ ズ'][0]
    
    def get_jockey(self):
        return self.result['騎手'][0]

    #---戦績のフィルタ用関数---
    #指定された距離区分についての戦績を返す
    #まとめてフィルタ処理をするGodMethod
    def get_filtered_form(self, smile=['S','M','I','L','E'], course=None, style=['逃','先','差','追','マ'], race=None):
        form = self.form
        form = self.get_form_by_smile(smile, form)
        if course is not None:
            form = self.get_form_by_course(course, form)
        form = self.get_form_by_style(style, form)
        if race is not None:
            form = self.get_form_by_race(race, form)
        return form

    #arr:SMILE区分、 subset of ['S','M','I','L','E']
    def get_form_by_smile(self, smile, form = None):
        if form is None:
            form = self.form
        return form.query('SMILE in @smile')

    #指定されたコースの戦績を抽出 course : string[]
    def get_form_by_course(self, course, form = None):
        if form is None:
            form = self.form
        filter_list = [c[1:3] in course for c in form['開催']]
        return form[filter_list]
    
    #指定された脚質で走っていた戦績を抽出 style = subset of ['逃','先','差','追','マ']
    def get_form_by_style(self, style, form = None):
        if form is None:
            form = self.form
        return form.query('style in @style')

    #該当するレース名で抽出
    def get_form_by_race(self, race_name, form = None):
        if form is None:
            form = self.form
        race_name = race_name.replace('(','\(').replace(')','\)')
        return form.query('レース名.str.contains(@race_name)')

    #前走のみを抽出
    def get_last_form(self, form = None):
        if form is None:
            form = self.form
        return form[0:1]
    
    #前5走を抽出
    def get_5_form(self, form = None):
        if form is None:
            form = self.form
        return form[0:5]

    #レースで完走したかのリストを返す
    #dropna()を知ったので用済み
    def are_complete(self):
        return [not b for b in self.form['上り'].isnull()]

    #toString()に相当
    def __str__(self):
        return str(self.name)+' '+str(self.date[0:4])+' '+str(self.result['人 気'][0])+'人'+str(self.result['着 順'][0])+'着'+'['+make_simple_rank(self.form)+']'

race_header = ['日付', '開催', '天 気', 'R', 'レース名', '頭 数', '枠 番', '馬 番', 'オ ッ ズ', '人 気',
               '着 順', '騎手', '斤 量', '距離', '馬 場', 'タイム', '着差', '通過', 'ペース', '上り',
               '馬体重','勝ち馬 (2着馬)', '賞金', 'rank3F', 'style', 'SMILE', 'grade']

smile_criteria = {'S':[1, 1300], 'M':[1301, 1899], 'I':[1900,2100], 'L':[2101, 2700], 'E':[2701, 9999]}

#ファイル入出力
def write_horse(id, date, name, html):
    os.makedirs(HORSE_DIR_PATH, exist_ok = True)
    date = date.replace('/','')
    path = HORSE_DIR_PATH + '/' + str(id) +'_'+ date +'_'+ name +'.html'
    with open(path, mode = "w", encoding = 'euc-jp') as f:
        f.write(html)
    return

def read_horse(id):
    with open(glob.glob(HORSE_DIR_PATH + '/' + str(id) +'_*.html')[0], mode = "r", encoding = 'euc-jp') as f:
        html = f.read()
    return html

def remove_horse(id):
    for p in glob.glob(HORSE_DIR_PATH + '/' + str(id) +'_*.html'):
        os.remove(p)
    return

def horse_exists(id):
    if not glob.glob(HORSE_DIR_PATH + '/' + str(id) +'_*.html'):
        return False
    else:
        return True

def is_horse_latest(id, date):
    file_date = os.path.basename(glob.glob(HORSE_DIR_PATH + '/' + str(id) +'_*.html')[0])[11:19]
    date = date.replace('/','')
    return int(file_date) >= int(date)

#---補助関数---
#通過順から脚質を判定、TARGETに準拠
def classify_style(result_series):
    passing = result_series['通過']
    if pd.isna(passing):
        return ''
    num = result_series['頭 数']
    order = passing.split('-')
    if '1' in order[:-1]:
        return '逃'
    if int(order[-1]) >= num-5 and int(order[-1]) >= num*2/3:
        return '追'
    if int(order[-1]) > num/3:
        return '差'
    if (len(order) >= 2 and int(order[-2]) >= num*2/3) or(len(order) >= 3 and int(order[-3]) >= num*2/3):
        return 'マ'
    return '先'

styles = ['逃', '先', '差', '追', 'マ']

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



#馬をフィルタするクラス
class HorseFilter:

    def __init__(self, chaku=None, ninki=None, odds=None, waku=None, umaban=None, jockey=None, style=None, dist=None, last=None, rest=None):
        self.chaku = chaku
        self.ninki = ninki
        self.odds = odds
        self.waku = waku
        self.umaban = umaban
        self.jockey :str = jockey

        self.style = style
        self.dist = dist
        self.last : str = last
        self.rest = rest

        self.style_th = 0.3
    
    def filter(self, horse:Horse):
        rslt = True
        if self.chaku is not None:
            x = horse.get_chakujun()
            if not str(x).isdigit():
                rslt = False
            elif type(self.chaku) == list:
                rslt = rslt & (self.chaku[0] <= int(x) <= self.chaku[1])
            else:
                rslt = rslt & (horse.get_chakujun() == self.chaku)
        if self.ninki is not None:
            x = horse.get_ninki()
            if not str(x).replace('.','').isdigit():
                rslt = False
            elif type(self.ninki) == list:
                rslt = rslt & (self.ninki[0] <= int(x) <= self.ninki[1])
            else:
                rslt = rslt & (x == self.ninki)
        if self.waku is not None:
            x = horse.get_wakuban()
            if pd.isna(x):
                rslt = False
            elif type(self.waku) == list:
                rslt = rslt & (self.waku[0] <= int(x) <= self.waku[1])
            else:
                rslt = rslt & (x == self.waku)
        if self.umaban is not None:
            x = horse.get_umaban()
            if type(self.umaban) == list:
                rslt = rslt & (self.umaban[0] <= int(x) <= self.umaban[1])
            else:
                rslt = rslt & (x == self.umaban)
        if self.odds is not None:
            x = horse.get_odds()
            if type(self.odds) == list:
                rslt = rslt & (self.odds[0] <= x <= self.odds[1])
            else:
                rslt = rslt & (x <= self.odds)

        if self.style is not None:
            x = horse.get_style_ratio()
            tmp_bool = False
            for s in self.style:
                tmp_bool = tmp_bool | (x[s] >= self.style_th)
            rslt = rslt & tmp_bool

        if self.dist is not None:
            x = horse.get_average_distance()
            if type(self.dist) == list:
                rslt = rslt & (self.dist[0] <= x <= self.dist[1])
            else:
                rslt = rslt & (x <= self.dist)
        
        if self.rest is not None:
            if type(self.rest) == list:
                rslt = rslt & horse.check_long_rest(self.rest[0], self.rest[1])
            else:
                rslt = rslt & horse.check_long_rest(self.rest)

        if self.jockey is not None:
            x = horse.get_jockey()
            rslt = rslt & (self.jockey in x)
        if self.last is not None:
            x = horse.get_last_race_name()
            rslt = rslt & (self.last in x)

        return rslt
    
    def __str__(self):

        msg = 'HorseFilter{'

        if self.chaku is None:
            msg = msg + 'chaku: - , '
        elif type(self.chaku) == list:
            msg = msg + 'chaku: {:d} ~ {:d} , '.format(self.chaku[0],self.chaku[1])
        else:
            msg = msg + 'chaku: {:d} , '.format(self.chaku)
        if self.ninki is None:
            msg = msg + 'ninki: - , '
        elif type(self.ninki) == list:
            msg = msg + 'ninki: {:d} ~ {:d} , '.format(self.ninki[0],self.ninki[1])
        else:
            msg = msg + 'ninki: {:d} , '.format(self.ninki)
        if self.odds is None:
            msg = msg + 'odds: - , '
        elif type(self.odds) == list:
            msg = msg + 'odds: {:.1f} ~ {:.1f} , '.format(self.odds[0],self.odds[1])
        else:
            msg = msg + 'odds: {:.1f} , '.format(self.odds)
        if self.umaban is None:
            msg = msg + 'umaban: - , '
        elif type(self.umaban) == list:
            msg = msg + 'umaban: {:d} ~ {:d} , '.format(self.umaban[0],self.umaban[1])
        else:
            msg = msg + 'umaban: {:d} , '.format(self.umaban)
        if self.waku is None:
            msg = msg + 'waku: - , '
        elif type(self.waku) == list:
            msg = msg + 'waku: {:d} ~ {:d} , '.format(self.waku[0],self.waku[1])
        else:
            msg = msg + 'waku: {:d} , '.format(self.waku)
        if self.jockey is None:
            msg = msg + 'jockey: - , '
        else:
            msg = msg + 'jockey: {:s} , '.format(self.jockey)

        if self.style is None:
            msg = msg + 'style: - , '
        else:
            msg = msg + 'style:'
            for s in self.style:
                msg = msg + ' ' + s
            msg = msg + ' , '
        if self.dist is None:
            msg = msg + 'dist: - , '
        elif type(self.dist) == list:
            msg = msg + 'dist: {:.1f} ~ {:.1f} , '.format(self.dist[0],self.dist[1])
        else:
            msg = msg + 'dist: {:.1f} , '.format(self.dist)
        if self.last is None:
            msg = msg + 'last: - , '
        else:
            msg = msg + 'last: {:s} , '.format(self.last)
        if self.rest is None:
            msg = msg + 'rest: - '
        elif type(self.rest) == list:
            msg = msg + 'rest: 間{:d}日 {:d}走目'.format(self.rest[0],self.rest[1])
        else:
            msg = msg + 'rest: 間{:d}日'.format(self.rest)
        return msg + '}'
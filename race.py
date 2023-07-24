import pandas as pd
import time
import os
import glob
from bs4 import BeautifulSoup
import requests
import re

from horse import Horse

#レース結果を表現するクラス
class Race:

    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
        self.html = get_race_html(self.id, self.name)
        self.html = deleteTag(self.html,'diary_snap_cut')
        self.results = get_race_dataframe(self.html)

        tan_list, huku_list = get_payback_list(self.html)
        self.results[0] = self.results[0].assign(horseID = get_horseID(self.html))
        self.results[0] = self.results[0].assign(単勝払戻 = tan_list)
        self.results[0] = self.results[0].assign(複勝払戻 = huku_list)

    def get_horses(self):
        horses = []
        for i,h_row in self.results[0].iterrows():
            horses.append(Horse(self.id, self.date, h_row['horseID'], h_row['馬名'], h_row['単勝払戻'], h_row['複勝払戻']))
        return horses
    
#レースデータを作成する補助関数群

#IDからレース情報を取得
def get_race_data(id):
    df = pd.read_html("https://db.netkeiba.com/race/"+str(id)+"/")
    time.sleep(1)
    return df

#IDからレースのHTMLを取得
def get_race_html(id, name):
    if race_exists(id):
        html = read_race(id)
    else:
        html = requests.get("https://db.netkeiba.com/race/"+str(id)+"/")
        html.encoding = "euc_jp"
        html = html.text
        print('access to:'+"https://db.netkeiba.com/race/"+str(id)+"/")
        time.sleep(1)
        write_race(id, name, html)
    return html

#HTMLから上がり等を含むレースのデータフレームを取得
def get_race_dataframe(html):
    deleteTag(html,'diary_snap_cut')
    soup = BeautifulSoup(html, 'html.parser')
    dfs = [pd.read_html(str(t))[0] for t in soup.select('table:has(tr td)')]
    #dfs = pd.read_html(html)
    dfs[0] = dfs[0].drop(columns=['備考', 'ﾀｲﾑ 指数', '調教 ﾀｲﾑ', '厩舎 ｺﾒﾝﾄ', '馬主', '賞金 (万円)'])
    return dfs

#<diary_snap_cut>,</diary_snap_cut>等のタグの削除
def deleteTag(html, tag):
    return html.replace('<'+tag+'>','').replace('</'+tag+'>','')

#レースデータのHTMLから馬のIDのリストを取り出す
def get_horseID(html):
    soup = BeautifulSoup(html, 'html.parser')
    horses = soup.find_all('table')[0].find_all('a', href=re.compile("^/horse/"))
    return [x.get('href')[7:17] for x in horses]

#レースについてのHTMLから、単勝払い戻しと複勝払い戻しの配列を作成
def get_payback_list(html):
    umaban = get_race_dataframe(html)[0]['馬 番']

    payoff_table = get_race_dataframe(html)[1]
    tan_num = int(payoff_table.iat[0,1])
    huku_num = [int(n) for n in payoff_table.iat[1,1].split(" ")]
    tan_payoff = int(payoff_table.iat[0,2].replace(',',''))
    huku_payoff = [int(n) for n in payoff_table.iat[1,2].replace(',','').split(" ")]

    tan_list = []
    huku_list = []
    for n in umaban:
        if n == tan_num:
            tan_list.append(tan_payoff)
        else:
            tan_list.append(0)
        if n in huku_num:
            huku_list.append(huku_payoff[huku_num.index(n)])
        else:
            huku_list.append(0)

    return tan_list, huku_list


result_header = ['着 順', '枠 番', '馬 番', '馬名', '性齢', '斤量', '騎手', 'タイム', '着差', '通過', '上り',
                 '単勝', '人 気', '馬体重', '調教師', 'ID', '単勝払戻', '複勝払戻']

#ファイル入出力
RACE_DIR_PATH = './races'

#レース結果
def write_race(id, name, html):
    os.makedirs(RACE_DIR_PATH, exist_ok = True)
    path = RACE_DIR_PATH + '/' + str(id) +'_'+ name +'.html'
    with open(path, mode = "w", encoding = 'euc-jp') as f:
        f.write(html)
    return

def read_race(id):
    os.makedirs(RACE_DIR_PATH, exist_ok = True)
    with open(glob.glob(RACE_DIR_PATH + '/' + str(id) +'_*.html')[0], mode = "r", encoding = 'euc-jp') as f:
        html = f.read()
    return html

def race_exists(id):
    if not glob.glob(RACE_DIR_PATH + '/' + str(id) +'_*.html'):
        return False
    else:
        return True

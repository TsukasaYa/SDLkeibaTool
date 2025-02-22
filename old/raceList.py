import pandas as pd
import time

#レースの一覧を取得するための関数群

# 指定されたレースについて、レースID付きのデータフレームを返す
def get_race_list(racename):
    df = search_race_list(racename)
    return append_id_colmun(df).dropna(subset='ID').reset_index(drop=True)

# 日本語のレース名をURLに使えるようにパーセントエンコーディングする
def get_encoded_racename(racename):
  euc_racename = racename.encode("euc_jp")
  encoded_race_name = ""
  for i in range (len(euc_racename)):
    encoded_race_name += hex(euc_racename[i])
  return encoded_race_name.replace("0x","%")

# 引数名のレースについての検索結果を返す
def search_race_list(racename):
    encoded_name = get_encoded_racename(racename)
    df = pd.read_html("https://db.netkeiba.com/?pid=race_list&word="+encoded_name+"&start_year=none&start_mon=none&end_year=none&end_mon=none&kyori_min=&kyori_max=&sort=date&list=100")[0]
    time.sleep(1)
    return df

# スクレイピングした検索結果にレースIDを付与する
def append_id_colmun(base_df):
    dates = base_df["開催日"]
    places = base_df["開催"]
    races = base_df["R"]
    ids = []
    for i in range(len(dates)):
        id = calc_id(int(dates[i][0:4]),places[i],int(races[i]))
        ids.append(id)
    result_df = base_df.assign(ID=ids)
    result_df = result_df[result_df["ID"] > 0]
    return result_df

# レース情報からIDを生成する
def calc_id(year, kaisai, race):
    cource = kaisai[1:3]
    id = 0
    if is_JRArace(cource):
        times = int(kaisai[0])
        date = int(kaisai[3:])
        id = year
        id = id*100 + placeToId[cource]
        id = id*100 + times #開催回
        id = id*100 + date #開催日数
        id = id*100 + race #第何レース
    return id

#中央かどうかの判定
def is_JRArace(cource):
    return cource in placeToId

# 競馬場をIDに変換するための辞書
placeToId = {"札幌":1,"函館":2, "福島":3, "新潟":4, "東京":5, "中山":6, "中京":7, "京都":8, "阪神":9, "小倉":10}

header = ['開催日', '開催', '天 気', 'R', 'レース名', '映像', '距離', '頭 数', '馬 場', 'タイム', 'ペース','勝ち馬', '騎手', '調教師', '2着馬', '3着馬', 'ID']
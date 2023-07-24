import raceList
from race import Race
from horse import Horse, HorseFilter
import form
import matplotlib.pyplot as plt

#回収率の計算
def get_payout_ratio(horse_list):
    tan_ratio = sum([h.tan for h in horse_list])/max(len(horse_list),1)
    huku_ratio = sum([h.huku for h in horse_list])/max(len(horse_list),1)
    return {'単':tan_ratio, '複':huku_ratio}

#レース結果の集計
def make_result_list(hl):
    results = [0]*19
    for r in [h.get_chakujun() for h in hl]:
        if str(r).isdigit():
            i = int(r)
            results[i-1] = results[i-1]+1
        elif r == '中':
            results[18] = results[18]+1
    return results

#レース結果の簡略表示
def make_simple_result(hl):
    arr = make_result_list(hl)
    rank = [0,0,0,0]
    rank[0] = arr[0]
    rank[1] = arr[1]
    rank[2] = arr[2]
    rank[3] = sum(arr[3:])
    return str(rank[0])+'-'+str(rank[1])+'-'+str(rank[2])+'-'+str(rank[3])

#馬のリストを表示
def dump_horses(hl):
    for h in hl:
        print(h)
    return

# フィルター結果の表示
def show_result(horse_list, filtered_list, label = True):
    print_score(horse_list, filtered_list)

    x =[]
    y = []
    l = []
    for ho in filtered_list:
        chakujun = str(ho.get_chakujun())
        if chakujun == '除':
            continue
        else:
            if not chakujun.isdigit():
                chakujun = ho.result['頭 数'][0]
            x.append(int(ho.get_ninki()))
            y.append(int(chakujun))
            l.append(ho.soup.find(class_ = "eng_name").get_text().replace('\n',''))

    plt.scatter(x,y, alpha = .3)
    plt.xlabel("favorite")
    plt.ylabel("result")
    plt.xticks(range(1,19))
    plt.yticks(range(1,19))
    for i, label in enumerate(l):
        if label == True:
            plt.text(x[i],y[i],label)
    plt.show()
    #plt.pause(2)

def print_score(horse_list, filtered_list):
    horses_win = [h for h in horse_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) == 1]
    horses_show = [h for h in horse_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) <= 3]
    num_filtered_win = len([h for h in filtered_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) == 1 ])
    num_filtered_show = len([h for h in filtered_list if str(h.get_chakujun()).isdigit() and int(h.get_chakujun()) <= 3])
    precise_win = num_filtered_win / max(len(filtered_list),1)
    recall_win = num_filtered_win / max(len(horses_win),1)
    precise_show = num_filtered_show / max(len(filtered_list),1)
    recall_show = num_filtered_show / max(len(horses_show),1)
    print(get_payout_ratio(filtered_list))
    print('該当馬'+str(len(filtered_list))+'頭 ['+make_simple_result(filtered_list)+']')
    print("1着: precise {:.2f}, recall {:.2f}".format(precise_win, recall_win))
    print("複勝: precise {:.2f}, recall {:.2f}".format(precise_show, recall_show))


def isfloat(s):  # 浮動小数点数値かどうかを判定する関数
    try:
        float(s)  # 試しにfloat関数で文字列を変換
    except ValueError:
        return False  # 失敗すれば False
    else:
        return True  # 上手くいけば True

def input_error(stmt, opt = None):
    msg = '[main.py] input is not valid '
    if opt is not None:
        msg += opt
    
    msg += '"'
    for tk in stmt:
        msg = msg +tk
        if not tk == stmt[-1]:
            msg += ' '
    msg = msg + '"'

    print(msg)

#---ここからメイン処理---
loop = True
while loop:
    race_name = input('レース名>')
    try:
        race_list = raceList.get_race_list(race_name)
        if len(race_list) == 0:
            print('no hit')
            continue
        print(race_list[['開催', 'レース名', '距離', 'ID']][0:5])
    except KeyError:
        print('no hit! please input other racename')
        continue
    ans = input('これで良いですか? y/n >')
    if ans =='y':
        loop = False

years = int(input('何年分取得しますか? >'))
YEARS_MAX = 20
years = min(years, YEARS_MAX, len(race_list))
races = []
for years_ago in range(years):
    race_id = race_list["ID"][years_ago]
    race_date = race_list["開催日"][years_ago]
    races.append(Race(race_id, race_name, race_date))

horse_list = []
for r in races:
    print('make Horse instance... in ' + r.date[0:4])
    horse_list.extend(r.get_horses())

ff = form.FormFilter()
fe = form.FormEvaluator()
hf = HorseFilter()

loop = True
while(loop):
    print(hf)
    print(ff)
    print(fe)

    filtered_horses = [h for h in horse_list if hf.filter(h) == True]
    filtered_list = [h for h in filtered_horses if fe.eval(ff.filter(h.form))]
    show_result(horse_list, filtered_list, False)

    print('クエリは次の要素をスペース区切りで記入、&で複数可: [hf/fe/ff] [変更したいフィールド] [変更後の値]+')
    #入力をもとにフィルタを変更する
    query = input('>')
    for stmt in query.split('&'):
        stmt = [token for token in stmt.split(' ') if token != '']
        if len(stmt) >= 1 and (stmt[0] == 'q' or stmt[0] == 'quit'):
            loop = False
            continue
        
        if stmt[0] == 'dump':
            dump_horses(filtered_list)
        elif len(stmt) < 2:
            input_error(stmt, ", few token")
            continue
        
        if stmt[0] == 'ff':
            if stmt[1] == 'clear' or stmt[1] == 'c':
                ff.pre = None
                ff.smile = None
                ff.course = None
                ff.race = None
                ff.style = None
                ff.post = None
            elif stmt[1] == 'pre':
                if len(stmt)== 2:
                    ff.pre = None
                else:
                    ff.pre = int(stmt[2])
            elif stmt[1] == 'smile':
                if len(stmt)== 2:
                    ff.smile = None
                else:
                    ff.smile = stmt[2:]
            elif stmt[1] == 'course':
                if len(stmt)== 2:
                    ff.course = None
                else:
                    ff.course = stmt[2:]
            elif stmt[1] == 'style':
                if len(stmt)== 2:
                    ff.style = None
                else:
                    ff.style = stmt[2:]
            elif stmt[1] == 'race':
                if len(stmt)== 2:
                    ff.race = None
                else:
                    ff.race = stmt[2]
            elif stmt[1] == 'post':
                if len(stmt)== 2:
                    ff.post = None
                else:
                    ff.post = int(stmt[2])
            elif stmt[1] == 'crear':
                ff.post = None
                ff.pre = None
                ff.course = None
                ff.race = None
                ff.smile= None
                ff.course = None
            else:
                input_error(stmt, "at 2nd token")
        elif stmt[0] == 'fe':
            if stmt[1] == 'clear' or stmt[1] == 'c':
                fe.win = None
                fe.show = None
                fe.rank = None
                fe.last3f = None
                fe.margin = None
            else:
                try:
                    getattr(fe, stmt[1])
                    if len(stmt) == 3:
                        setattr(fe, stmt[1], float(stmt[2]))
                    elif len(stmt) == 4:
                        setattr(fe, stmt[1],[float(stmt[2]),float(stmt[3])])
                    else:
                        input_error(stmt)
                except AttributeError:
                    input_error(stmt)
        elif stmt[0] == 'hf':
            if stmt[1] == 'clear' or stmt[1] == 'c':
                hf.chaku = None
                hf.ninki = None
                hf.odds = None
                hf.jockey = None
                hf.waku = None
                hf.umaban = None
                hf.last = None
                hf.dist = None
                hf.rest = None
                hf.style = None
            else:
                try:
                    getattr(hf, stmt[1])
                    if len(stmt) == 2:
                        setattr(hf, stmt[1], None)
                    elif stmt[1] in ['style']:
                        setattr(hf, stmt[1], stmt[2:])
                    elif len(stmt) == 3:
                        if(stmt[1] in ['jockey','last','style']):
                            val = stmt[2]
                        elif(stmt[1] in ['odds','dist']):
                            val = float(stmt[2])
                        else:
                            val = int(stmt[2])
                        setattr(hf, stmt[1], val)
                    elif len(stmt) == 4:
                        if stmt[1] in ['odds','dist']:
                            val = [float(stmt[2]),float(stmt[3])]
                        else:
                            val = [int(stmt[2]), int(stmt[3])]
                        setattr(hf, stmt[1], val)
                    else:
                        input_error(stmt)
                except AttributeError:
                    input_error(stmt)
        else:
            input_error(stmt, "at 1st token")
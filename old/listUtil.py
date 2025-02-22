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

#馬のリストを表示
def dump_horses(hl):
    for h in hl:
        print(h)
    return

# フィルター結果の表示
def plot_horses(filtered_list, label = False):
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

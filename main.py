import raceList
from race import Race

#回収率の計算
def get_payout_ratio(horse_list):
    tan_ratio = sum([h.tan for h in horse_list])/max(len(horse_list),1)
    huku_ratio = sum([h.huku for h in horse_list])/max(len(horse_list),1)
    return {'単':tan_ratio, '複':huku_ratio}

#馬のリストを表示
def dump_horses(hl):
    for h in hl:
        print(h)
    return

race_name = "中京記念"
race_list = raceList.get_race_list(race_name)

YEARS_MAX = 5
races = []
for years_ago in range(YEARS_MAX):
    race_id = race_list["ID"][years_ago]
    race_date = race_list["開催日"][years_ago]
    races.append(Race(race_id, race_name, race_date))

horse_list = []
for r in races:
    print('make Horse instance' + r.date[0:4])
    horse_list.extend(r.get_horses())

dump_horses(horse_list)
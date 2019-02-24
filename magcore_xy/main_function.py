from game_function import *
import time

num = [x for x in range(0, 10)]
map_type_dict = {
    '1': 'RectSmall',
    '2': 'RectMid',
    '3': 'RectLarge'
}

# 新建用户，选择颜色，一直循环到玩家名字或者颜色没有冲突为止
def create_player():
    while True:
        game_username = input('请输入新建游戏用户名: ')
        game_color = int(input('0: 香蕉\n1: 樱桃\n2: 葡萄\n3: 菜瓜\n4: 柠檬\n5: 桑葚\n6: 生梨\n7: 菠萝\n8: 萝卜\n9: 西瓜\n请在上面的颜色列表中选择需要显示的的颜色: '))
        if game_color in num:
            CreatPlayer_ret = CreatPlayer(game_username,game_color)
            if CreatPlayer_ret != None :
                break
    return CreatPlayer_ret

def join_game(playerid):
    map_description_dict = {
        'RectSmall': '小地图',
        'RectMid': '中地图',
        'RectLarge': '大地图'
    }
    game_status_description_dict = {
        '0': '等待加入',
        '1': '游戏中',
        '2': '结束' ,
        '3': '已销毁'
    }
    GetGameLists_ret = GetGameList()
    print('请在下列的游戏列表选择一个你要加入的游戏')
    zipped_id = zip(['{}'.format(x) for x in range(1, len(GetGameLists_ret) + 1)], GetGameLists_ret)
    zipped_id_dict = {}
    for k, v in zipped_id:
        print('游戏房间编号: {} , 游戏id: {},地图尺寸: {}, 游戏状态: {}'.format(k,v['id'],map_description_dict[v['map']],game_status_description_dict[str(v['state'])]))
        zipped_id_dict[k] = v['id']
    your_choice_gameid_num = input('请输入你需要选择的游戏编号(只能选择游戏状态为等待加入的): ')
    your_choice_gameid = zipped_id_dict.get(your_choice_gameid_num,None)
    if your_choice_gameid:
        JoinGame_flag = JoinGame(your_choice_gameid, playerid)
        if JoinGame_flag == True:
            print('加入游戏成功')
            return your_choice_gameid
        else:
            return None

def create_game():
    while True:
        map_num = input('1: small_map\n2: medium_map\n3: large_map\n选择你需要的地图: ')
        try:
            map_name = map_type_dict[map_num]
            break
        except KeyError:
            print('请输入正确的地图编号！')
    gameid = CreateGame(map_name)
    return gameid


def whether_join_exiting_game(playerid):
    join_or_not = int(input('1:是\n0:否\n是否加入现有游戏: '))
    # 加入现有游戏
    if join_or_not == 1:
        gameid = join_game(playerid)
        return gameid

    # 不加入现有游戏
    elif join_or_not == 0:
        gameid = create_game()
        return gameid

def waiting_for_play_game(gameid):
    count = 0
    while True:
        StartGame_flag = StartGame(gameid)
        if StartGame_flag == True:
            return True
        else:
            if count > 5:
                print('重试次数过多，请重新进入！')
                return False
            print('等待玩家进入。。。。')
            time.sleep(5)
            count += 1

def find_base_location(gameid,playerid):
    all_base_location = []
    enemy_base_location = []
    GetGame_ret_dict = GetGame(gameid)
    GetPlayer_ret_dict = GetPlayer(playerid)
    my_base_location = GetPlayer_ret_dict['Bases']
    for x in GetGame_ret_dict['Cells']:
        for i in x:
            if i['Type'] == 2:
                print(i['X'],i['Y'])
                all_base_location.append([i['X'],i['Y']])
    for y in all_base_location:
        if y != my_base_location:
            enemy_base_location.append(y)

    return enemy_base_location

def main():
    # 获取玩家初始化状态
    player_init_status_json = create_player()
    # 获取玩家playerid
    myplayerid = player_init_status_json['Id']
    # 获取玩家index
    myplayerindex = player_init_status_json['Index']
    while True:
        # 是否加入已有游戏
        gameid = whether_join_exiting_game(myplayerid)
        if gameid:
            # 等待玩家进入
            flag = waiting_for_play_game(gameid)
            if flag:
                print('玩家进入成功')
                print('目前的gameid: {}'.format(gameid))
                break
        else:
            print('没有这个gameid，请重新选择')
    enemy_base_location = find_base_location(gameid,myplayerid)
    print(enemy_base_location)


if __name__ == '__main__':
    main()
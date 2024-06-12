import random
import time

class TextStyle:# 色の変更のためのクラス
    BOLD = '\033[1m' #太字
    END = '\033[0m' #そこまで
    GREEN = '\033[92m' #緑
    PURPLE = "\033[35m" #紫
    RED = '\033[91m' #赤
    BLUE = "\033[34m" #青
    YELLOW = "\033[33m" #黄色

class creature:
    def __init__(self, name, power, xy):
        self.name = name   #キャラの名前
        self.power = power #nameのパワー
        self.xy = xy       #nameの座標
        self.has_orb = False #光の玉を持っているか
        self.dead_turn = 1000000000000000 #nameモンスターが倒されたターンを保存
        
    def return_name(self):
        return self.name
    def return_power(self):
        return self.power
    def return_xy(self):
        return self.xy
    def input_name(self, input_name):
        self.name = input_name
    def input_power(self, input_power):
        self.power = input_power
    def input_xy(self, input_xy):
        self.xy = input_xy
    #勇者の移動を行なう関数
    def get_next_move_hero(self):
        print("どこに移動しますか？")
        while True:
            pos = input("上：w 下：s 左：a 右：d ルール：r マップ：m → ") #移動する方向を入力
            # 条件を満たさなければ再入力
            if pos != 'w' and pos != 's' and pos != 'a' and pos != 'd' and pos != 'r' and pos != 'm':  
                print("正しく入力してください")
                continue
            #移動方向が壁だった時、移動できる方向を再入力
            if (pos == 'w' and self.xy[0] == 0) or (pos == 's' and self.xy[0] == 4) or (pos == 'a' and self.xy[1] == 0) or (pos == 'd' and self.xy[1] == 4 and self.xy[0] != 0) or (pos == 'd' and self.xy[1] == 5 and self.xy[0] == 0) or (pos == 's' and self.xy == [0, 5]):
                print("壁です。移動できません。")
                continue
            #座標の更新を行なう
            if pos == 'w':#上の移動を行う
                return way[0]
            elif pos == 's':#下の移動を行う
                return way[1]
            elif pos == 'a':#左の移動を行う
                return way[2]
            elif pos == 'd':#右の移動を行う
                return way[3]
            elif pos == 'r':#ルールを再表示
                print_rule()
                continue
            elif pos == 'm':
                print_map()
    
    #モンスターの移動を行う関数
    def get_next_move_monster(self):
        pos = random.randint(0, 3) #wayを使うので0:上  1:下  2:左  3:右
        #移動先が壁だった場合、その場にとどまる（座標更新をしない）
        if (pos == 0 and self.xy[0] == 0) or (pos == 1 and self.xy[0] == 4) or (pos == 2 and self.xy[1] == 0) or (pos == 3 and self.xy[1] == 4):
            return [0, 0]
        if (self.xy == [0, 5]) and (pos != 2):
            return[0, 0]
        for i in range(5):#移動先にモンスターがいるか
            if(monsters[i].xy == [self.xy[0] + way[pos][0], self.xy[1] + way[pos][1]]):
                return [0, 0]
        if(disaster.xy == [self.xy[0] + way[pos][0], self.xy[1] + way[pos][1]]):
            return [0, 0]
        #壁でなかったら、移動を行なう（座標を更新）
        else:
            return way[pos]
        
    def battle_monster(self, monster):#モンスターとの戦闘(heroで実行)
        global game_continue,game_clear
        if self.power >= monster.return_power():#勇者のパワーがモンスター以上だったらパワー吸収
            if monster.name == "zo-ma":
                game_clear=True
                return
            print(TextStyle.BOLD+TextStyle.RED+monster.name+TextStyle.END+"を倒しました")
            print("パワーが"+str(monster.power)+"上がりました")
            self.power += monster.return_power()
            monster.dead_turn = now_turn
            monster.xy = False
            time.sleep(2)
            if (hero.power >= lightOrb_power) and (got_lightorb == False) and (len(lightOrb_xy)==0):
                display_lightOrb() #ひかりのたまが出現するかどうか
        else:#勇者のほうが弱かったら負け
            game_continue = False
        

#マップを表示する関数
def print_map():
    map_list = []
    for y in range(5):
        map_inslist = []
        for i in range(5):
            map_inslist.append([])
        for x in range(5):
            for j in range(5):
                map_inslist[j].append(read_room(y, x)[j])
                if y==0 and x==4:
                    map_inslist[j].append(read_room(y, x+1)[j])
        map_list.append(map_inslist)
    print(" ********  ********  ********  ********  ********  ******** ")
    for y in map_list:
        for x in y:
            for map in x:
                print(map, end="")
            print()

def read_room(y, x):
    room_list = []
    is_monster = False
    #モンスターの読み込み
    for i in range(5):
        if (monsters[i].return_xy() == [y, x]):
            room_list.append("*  "+ TextStyle.RED+ str(monsters[i].return_power())+ TextStyle.END+ " "*(6-len(str(monsters[i].return_power()) )) +"*")
            room_list.append("* "+ TextStyle.RED+ monsters[i].return_name()+ TextStyle.END+ " "*(7-len(monsters[i].return_name())) +"*")
            is_monster = True
    #魔王の読み込み
    if (disaster.return_xy() == [y, x]):
            room_list.append("* " + TextStyle.PURPLE+ str(disaster.return_power())+ TextStyle.END+ " "*(7-len(str(disaster.return_power()) )) +"*")
            room_list.append("* "+TextStyle.PURPLE+disaster.return_name()+TextStyle.END+ " "*(7-len(disaster.return_name())) +"*")
            is_monster = True
    #モンスターも魔王もいなかった場合
    if is_monster == False:
        room_list.append("*        *")
        room_list.append("*        *")
    #アイテムの読み込み
    if [y, x] in mant_xy:#マントを表示
        room_list.append("*  "+ TextStyle.BLUE+"mant"+TextStyle.END+"  *")
    elif [y, x] in sword_xy:#剣を表示
        room_list.append("* "+ TextStyle.BLUE+ "sword"+ TextStyle.END+ "  *")
    elif [y, x] in lightOrb_xy:
        room_list.append("*"+ TextStyle.YELLOW+ "lightorb"+ TextStyle.END+ "*")
    else:
        room_list.append("*        *")
    if (hero.return_xy() == [y, x]):
        room_list.append("*  " + TextStyle.GREEN + hero.name + TextStyle.END + "   *")
    else:
        room_list.append("*        *")
    room_list.append(" ******** ")
    return room_list
            

def print_rule():#ゲーム開始時に任意でルールを表示するようにする
    rule=["～あなたは世界の運命を託された勇者アルスです。あなたは魔王ゾーマを倒す運命にあります～",
          "・この魔王城には5体のモンスターと魔王ゾーマが常に徘徊しています",
          "・モンスターそれぞれにパワーがあり、同じ数値以下のモンスターにしか勝つことができません",
          "・モンスターを倒すとそのモンスターのパワーを吸収し勇者のパワーを上げることができます",
          "・倒されたモンスターは一定時間後に勇者より少し強い状態で復活します",
          "・剣を入手すると勇者のパワーを1.5倍上げることができます",
          "・マントを入手すると一度だけ勇者は通常より1マス多く移動ができます",
          "・魔王を倒すためには「ひかりのたま」を入手することが不可欠です。",
          "「ひかりのたま」は勇者が魔王を倒すに 相応しい強さを得たときその姿を表します",
          "※「相応しい強さ」は難易度により変化します"]
    for q in range(len(rule)):
        print(TextStyle.BOLD+rule[q]+TextStyle.END)
        print("")
        
def print_lever():
    Level=["１：初級","２：中級","３：上級","４：超級"]
    for q in range(len(Level)):
        print(TextStyle.BOLD+Level[q]+TextStyle.END)
        print("")
        
def print_power(name,power):#キャラクターの数値表示
    text=name+":"+str(power)
    print(TextStyle.BOLD+TextStyle.GREEN+name+":"+str(power)+TextStyle.END)
    print("")
    
way = [[-1, 0], [1, 0], [0, -1], [0, 1]]#上下左右
mant_xy = [[1, 1], [1, 3], [3, 1], [3, 3]]#マントの位置情報
sword_xy = [[2, 2]]#剣の位置情報
sword_rate = 1.5#剣の上昇倍率
lightOrb_xy =[]#光の玉の位置情報
lightOrb_power = 1000#光の玉出現のために必要なパワー
revival_rate = 1.8#復活時の上昇倍率
now_turn = 0#経過ターン
start = 0#スタート時にルール表示の選択
got_lightorb = False
game_continue = True
game_clear = False

#モンスターと勇者が遭遇したかを確認する関数
def encount_monster(hero_xy,monster):
    if  hero_xy == monster.xy:
        print("---------------------------------------------------")
        print(TextStyle.BOLD+TextStyle.RED+monster.name+TextStyle.END+"と遭遇した")
        return True
    else:
        return False
    
def get_sword():#剣の入手
    print(TextStyle.BOLD+TextStyle.BLUE+"剣"+TextStyle.END+"を手に入れ、勇者の力が上がりました")
    sword_xy.remove([2, 2])
    hero.input_power(int(hero.return_power()*sword_rate))
    if (hero.power >= lightOrb_power) and (got_lightorb == False) and (len(lightOrb_xy)==0):#剣を取得して光の玉出現条件を満たしたとき光の玉が出現
        display_lightOrb()
    
def revival_Monster(monster):#モンスターの復活
    monster.power = int(hero.power * revival_rate) #復活時のパワーを設定
    while True:
        judge = True #マスに誰もいないか判定
        ins_xy = [random.randint(0, 4), random.randint(0, 4)] #復活マスをランダムで選択
        #ランダムに生成されたマスに誰もいないかの判定
        for i in range(5):
            if monsters[i].xy == ins_xy:
                judge = False
                break
            elif hero.xy == ins_xy:
                judge = False
                break
            elif disaster.xy == ins_xy:
                judge = False
                break
        if judge:
            monster.xy = ins_xy
            monster.dead_turn = 1000000000000
            return
    
def display_lightOrb():#ひかりのたま出現
    lightOrb_xy.append([4, 0])
    print("ひかりのたまが出現した!")  

def get_lightOrb():#ひかりのたま入手
    global got_lightorb, mant_xy
    lightOrb_xy.remove([4, 0])
    got_lightorb = True #光の玉入手済み
    disaster.xy = [0, 5] #魔王を転送
    disaster.power = lightOrb_power #魔王のパワーをlightOrb_powerに変更
    ins_mant_xy = [[1, 1], [1, 3], [3, 1], [3, 3]]#マント再配置
    for i in range(4):
        if ins_mant_xy[i] not in mant_xy:
            mant_xy.append(ins_mant_xy[i])
    print("---------------------------------------------------")
    print(TextStyle.YELLOW+"ひかりのたま"+TextStyle.END+"を取得した！")
    print("魔王のパワーが"+ str(lightOrb_power) +"になった")
    for monster in monsters:
        monster.power = 100000 #モンスターのパワーを100000に設定
    print("モンスターたちが怒りだし、真の力が解放された")
    print("モンスターのパワーが100000になった")
    time.sleep(2)

#全ステータスの初期化
hero = creature("ars",5,[4, 0])#勇者の情報をクラスに組み込む
disaster = creature("zo-ma", 1000000, [0, 5])#魔王の情報をクラスに組み込む
#モンスターの初期情報
monster_info = [["slime", 5, [2, 1]], ["yarihei", 5, [3, 2]], 
                ["mo-mon", 10, [1, 2]], ["machine", 30, [2, 3]], 
                ["saturn", 90, [0, 4]]]
monsters = []
for i in range(5):
    monsters.append(creature(monster_info[i][0], monster_info[i][1], monster_info[i][2]))

start = input("ルール説明は必要ですか？：Y or N → ")

if start=="y" or start=="Y":
    print_rule()
    start=input("enterで進みます")
#難易度選択
print("難易度を選択してください:")
print_lever()
while(True):
    level = int(input("難易度："))
    if level == 1:#初級
        lightOrb_power = 500
        print("初級でゲームをスタートします")
        break
    elif level == 2:#中級
        lightOrb_power = 2000
        print("中級でゲームをスタートします")
        break
    elif level == 3:#上級
        lightOrb_power = 10000
        print("上級でゲームをスタートします")
        break
    elif level == 4:#超級
        lightOrb_power = 10000000000000000000000
        print("超級でゲームをスタートします")
        print(TextStyle.BOLD+TextStyle.RED+"※なお、超級では「ひかりのたま」は出現しません")
        print("己の力のみで魔王を倒しましょう"+TextStyle.END)
        break
    else:
        "正しく入力してください"





#ゲームループ
while(game_continue==True and game_clear==False):
    now_turn += 1
    print()
    print_map()
    print_power(hero.name,hero.power)
    hero_nextmove = hero.get_next_move_hero()
    hero.input_xy([hero.return_xy()[0]+hero_nextmove[0], hero.return_xy()[1]+hero_nextmove[1]])
    for i in range(5):#移動先にモンスターがいるか
        battle = encount_monster(hero.xy,monsters[i])
        if battle:#モンスターがいたら戦闘
            hero.battle_monster(monsters[i])
    battle = encount_monster(hero.xy,disaster)#移動先に魔王がいるか
    if battle:#魔王がいたら戦闘
        hero.battle_monster(disaster)                
    if hero.return_xy() in sword_xy: #剣を入手したときの処理
        get_sword()
    if hero.return_xy() in lightOrb_xy:#光の玉があったら
        get_lightOrb()
    if hero.return_xy() in mant_xy:#マントがあったら
        print(TextStyle.BLUE+"マント"+TextStyle.END+"を手に入れました もう一度移動できます")
        mant_xy.remove(hero.return_xy())
        now_turn -= 1
        continue
    if got_lightorb == False:#魔王の移動
        nextmove = disaster.get_next_move_monster()
        disaster.xy = [disaster.xy[0]+nextmove[0], disaster.xy[1]+nextmove[1]]
        battle = encount_monster(hero.xy,disaster)#移動後に戦闘
        if battle:#勇者がいたら戦闘
            hero.battle_monster(disaster)
    if game_continue == False:
        break
    for i in range(5):#モンスターの移動
        if monsters[i].xy != False:
            nextmove = monsters[i].get_next_move_monster()
            monsters[i].xy = [monsters[i].xy[0]+nextmove[0], monsters[i].xy[1]+nextmove[1]]
            battle = encount_monster(hero.xy,monsters[i])#移動後に戦闘
            if battle:#勇者がいたら戦闘
                hero.battle_monster(monsters[i])
        if monsters[i].dead_turn < now_turn:
            revival_Monster(monsters[i])
       

game_over_art = """
   _____                         ____                  _ 
  / ____|                       / __ \                | |
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ | |
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '_ /| |
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   |_|
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   (_)
    """

game_clear_art = """
   _____                         ____  |-|                     |-|
  / ____|                       / __ \ | |                     | |
 | |  __  __ _ _ __ ___   ___  | |  |_|| |   ___   __ _^ - ,__  | |
 | | |_ |/ _` | '_ ` _ \ / _ \ | |   _ | |  / _ \ / _' | ,_ /  | |
 | |__| | (_| | | | | | |  __/ | |__| || | /  __/ |(_) | |     |_|
  \_____|\__,_|_| |_| |_|\___|  \____/ |_|  \___| \__,_|_|     (_)
    """

if game_clear:#ゲームクリア時の処理
    disaster.xy = False
    print_map()
    print(f"{TextStyle.BOLD}{TextStyle.GREEN}あなたは魔王を倒しました  Game Clear{TextStyle.END}")
    print(TextStyle.GREEN+game_clear_art+TextStyle.END)
else:#ゲーム敗北時の処理
    print_map()
    print(f"{TextStyle.BOLD}{TextStyle.RED}あなたは負けてしまいました Game Over{TextStyle.END}")
    print(TextStyle.RED+game_over_art+TextStyle.END)
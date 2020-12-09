################### Mancala ####################

#? 
#!                             (AI)
#?              [0]  [1]  [2]   [3]   [4]   [5]   [6]
#*  [store_AI]                                            [store_player]
#?              [0]   [1]   [2]   [3]  [4]   [5]    [6]
#!                            (Player)
#? 
#?
player = 'player'
AI='AI'
#! lubang untuk player dan AI
board={
        player : [7,7,7,7,7,7,7],
        AI : [7,7,7,7,7,7,7]
        }
#! store untuk player dan AI
store={
    player : 0,
    AI : 0
}
#! fungsi untuk memperlihatkan isi dari board mancala
def show(board_ai,board_player,store_ai,store_player):
    print("########= AI =##########")
    print('==',board_ai,'==')
    print(store_ai,'===================',store_player)
    print('==',board_player,'==')
    print("########= Player =######\n")
#! fungsi untuk move player
def move_player(lubang):
    rock=board['player'][lubang]
    sisa=rock
    print("jumlah rock yang diambil = ",rock,'di lubang ke ',lubang)
    board['player'][lubang]=0
    label:s
    for i in range(rock):
        l=lubang+i+1
        sisa-=1
        if(l==7):
            store['player']+=1
        elif(l>7):
            for x in range(sisa+1):
                if(x>6 and x<14):
                    board['player'][abs(x-7)]+=1
                elif(x==14):
                    store['player']+=1 
                elif(x>14):
                    print(x)
                    board['AI'][abs(x-21)]+=1
                else:
                    board['AI'][(6-x)]+=1
            break
        else:
            board['player'][l]+=1
#    show(board['AI'],board['player'],store['AI'],store['player'])

#! fungsi untuk move AI
def move_ai(lubang):
    rock=board['AI'][lubang]
    sisa=rock
    print("jumlah rock yang diambil = ",rock,'di lubang ke ',lubang)
    board['AI'][lubang]=0
    l=lubang
    temp=0
    for i in range(rock,0,-1):
        l-=1
        sisa-=1
        if(l== -1):
            store['AI']+=1
        elif(l<-1):
            if (temp>=7 and temp<14):
                board['AI'][13-temp]+=1
            elif (temp==14):
                store['AI']+=1
            elif(temp>14):
                board['player'][abs(15-temp)]+=1
            else:
                board['player'][temp]+=1
            temp+=1
        else:
            board['AI'][l]+=1
#    show(board['AI'],board['player'],store['AI'],store['player'])


#! fungsi untuk menghitung skor ketika step sudah habis atau permainan berakhir
def hitug_skor(lumbung_player,lumbung_ai):
    pass

#print("\nMulai Turn 1")
show(board['AI'],board['player'],store['AI'],store['player'])
#! contoh cara memasukan nilainya untuk setiap lubang
# board['player'][1]=4
# board['player'][0]=1
# board['player'][2]=2
# board['player'][3]=21
# board['AI'][1]=6
# board['AI'][3]=1
# board['AI'][6]=2
turn=1
##!random player turn 
while (turn<50):
    print("\nMulai Turn ",turn)
    turn_player= int(input('[PLAYER MAIN], lubang ke berapa yang mau diambil? '))

    if (turn_player>6):
        print('\n######## WARNING! ########\nmasukan ulang lubang yang akan diambil\n')
    else:
        move_player(turn_player)
        show(board['AI'],board['player'],store['AI'],store['player'])
        turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
#! giliran lawan satunya
        move_ai(turn_ai)
        show(board['AI'],board['player'],store['AI'],store['player'])
        turn+=1
##! hitung skor setelah turn selesai  
# hitug_skor(board['AI'],board['player'])
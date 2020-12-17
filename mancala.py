################### Maswin ####################
import numpy as np
import pandas as pd
import random

class MancalaGA:
    
    def __init__(self, self_state, opponent_state, gen, popsize, generation, pc, pm):
        self.num_of_gen = gen
        self.pop_size = popsize
        self.num_of_generation = generation
        self.pc = pc
        self.pm = pm
        self.self_state = board['player'] # list state ai (lubang) *default [7,7,7,7,7,7,7]
        self.opponent_state = board['AI'] # list state player (lubang) *default [7,7,7,7,7,7,7]
        
    
    def individu(self):
        return np.array([np.random.uniform(0,1) for i in range(self.num_of_gen)])
    
    def population(self):
        return np.array([self.individu() for i in range(self.pop_size)])
    
    def debug_lubang_representation(self):
        global h1,h2,h3,h4,h5
        populasi = self.population()
        
        
        for idx, lubang in enumerate(self.self_state):
            idx_lubang = idx
            isi_lubang = lubang

            # get value tiap heuristik
            h1 = self.h1(idx_lubang, isi_lubang)
            h2 = self.h2(idx_lubang, isi_lubang)
            h3 = self.h3(idx_lubang, isi_lubang)
            h4 = self.h4(idx_lubang, isi_lubang)
            h5 = self.h5(idx_lubang, isi_lubang)


            print(f"ini lubang ke {idx_lubang} dengan isi isi_lubang {isi_lubang}")
            print(f"nilai h1 adalah {h1}")
            print(f"nilai h2 adalah {h2}")
            print(f"nilai h3 adalah {h3}")
            print(f"nilai h4 adalah {h4}")
            print(f"nilai h5 adalah {h5}")
            print("\n")
                
    
            
    def calc_fitnes(self, individu, heuristic):
        wh = heuristic*individu

#        return np.sum(list(wh[0],wh[1],wh[2],wh[3],wh[4]))-wh[5]
        return np.sum(wh[:5]) - wh[-1]
    
    def self_scan(self):
        data = {}
        for idx, lubang in enumerate(self.self_state):
            h1 = self.h1(idx, lubang)
            h2 = self.h2(idx, lubang)
            h3 = self.h3(idx, lubang)
            h4 = self.h4(idx, lubang)
            h5 = self.h5(idx, lubang) 
            h6 = self.h6(idx, lubang)
            data[idx] = np.array([h1,h2,h3,h4,h5,h6])
        return data
    
        
    
    def h1(self, idx_lubang, isi_lubang):
        '''
        Timbun sebanyak mungkin rock dalam satu lubang. 
        Karena pada akhir permainan, rock pada lubang akan dipindahkan semuanya pada lumbung. Lubang kanan semakin aman.
        '''
        # [0,1,2,3,4,5,6] [lumbung]
        if len(self.self_state)-1 <= (idx_lubang+isi_lubang):
            return 1.0
        return 0.0
    
    def h2(self, idx_lubang, isi_lubang):
        '''
        Pertahankan agar rock pada sisi kita sebanyak mungkin. (versi umum H1)
        '''
        if isi_lubang == 0:
            return 0.0
        
        total_batu_before = np.sum(self.self_state)
        
        # simulasikan perpindahan batu pada lubang
        cp_state = self.self_state[:]
        
            
        # pecah list menjadi kiri dan kanan
        kiri = cp_state[:idx_lubang]
        tengah = [0]
        kanan = cp_state[idx_lubang+1:]
        
        jml_batu = isi_lubang
        new_kanan = []
        for i in kanan:
            
            if jml_batu == 0:
                break
            else:
                new_kanan.append(i+1)
            
            jml_batu -= 1
        
        new_state = kiri+tengah+kanan

        
        # jumlahkan setiap batu untuk kondisi terbaru
        total_batu_after = np.sum(new_state)
        
        return total_batu_after/total_batu_before
            
    def h3(self, idx_lubang, isi_lubang):
        '''
        Mempertahankan gerakan memindah rock sebanyak mungkin
        '''
        # [0,1,2,3,4,5,6] [lumbung]
        if len(self.self_state) == (idx_lubang+isi_lubang):
            return 1.0
        return 0.0
    
    def h4(self, idx_lubang, isi_lubang):
        '''
        Memaksimalkan jumlah rock pada lumbung. Dengan memilih langkah mencuri
        '''
        target = idx_lubang + isi_lubang
        
        if isi_lubang == 0:
            return 0.0
        elif 0 not in self.self_state:
            return 0.0
        elif target >= len(self.self_state):
            # out of range
            return 0.0
        elif self.self_state[target] == 0:
            # jika target nilainya 0
            # curi
            if(self.opponent_state[target]==0):
                return 0.0
            else:
                jml_curi = self.opponent_state[target]
                return 1-(1/jml_curi)
        else:
            return 0.0

        
    def h4_new(self, idx_lubang, isi_lubang):
        
        target = idx_lubang + isi_lubang
        
        if isi_lubang == 0:
            return 0.0
        elif 0 not in self.self_state:
            return 0.0
        elif target > len(self.self_state):
            # out of range
            return 0.0
        elif self.self_state[target] == 0:
            # jika target nilainya 0
            # curi
            jml_curi = self.opponent_state[jml_pindah]
            return 1-(1/jml_curi)
        else:
            return 0.0
        
    def h5(self,idx_lubang,isi_lubang):
        target = idx_lubang + isi_lubang
        if len(self.self_state ) < (idx_lubang+isi_lubang):
            
            return 1.0
        else:
            return 0.0
        
    def h6(self, idx_lubang, isi_lubang):
        '''
        h5 pada excel dihapus diganti dengan h6 diexcel
        yaitu strategi bertahan
        Menjaga score musuh seminimal mungkin. (heuristik dengan mempertimbangkan 2 gerakan musuh kedepan.
        '''
        # [0,1,2,3,4,5,6] [lumbung]
        if isi_lubang == 0:
            return 0.0
        
        jml_batu_ke_musuh = abs(len(self.self_state) - (idx_lubang+isi_lubang))
        if jml_batu_ke_musuh > 0: # berarti ada batu yang masuk ke lubang musuh
            jml_batu_ke_musuh = len(self.self_state) if jml_batu_ke_musuh > len(self.self_state) else jml_batu_ke_musuh
            return jml_batu_ke_musuh/len(self.self_state)
        else:
            return 0.0
    
    def selection(self, population, verbose=False):
        '''
        menggunakan metode turnamen dari individu yang berada dalam kandidat
        '''
        scan = self.self_scan()
        
        self.kandidat = []
        
        self.rata_fitness = [0,0,0,0,0,0,0,0,0,0]
        for lubang, heuristic in scan.items():
            if verbose:
                # print(f"===========================lubang {lubang}======================================")
                # print("\n")
                temp = []
                for idx, individu in enumerate(population):
                    data_individu = {
                        'lubang': lubang,
                        'heuristic': heuristic,
                        'individu': {
                            'individuke':idx,
                            'gen':individu
                        },
                        'fitness': self.calc_fitnes(individu, heuristic)
                    }
                    
                    
                    temp.append(data_individu)
                    self.rata_fitness[idx] += data_individu['fitness']
                    # print(data_individu)
                    # print("\n")
                

                best_individu_each_lubang = sorted(temp, key=lambda p : p.get('fitness'), reverse=True)
                #print(f'best individu di lubang {lubang} adalah {best_individu_each_lubang[0]}')
                # append to kandidat
                self.kandidat.append(best_individu_each_lubang[0])
                # print(f"================================================================================")
                # print("\n")
                
                
                # masukan individu terbaik dari setiap lubang kedalam list kandidat
                
            else:
                pass
            
    def turnamen(self, pop):
        kandidat= []
        result = self.rata_fitness
        while ((len(kandidat)<4)):
            x = random.randint(0,9)
            if(x not in kandidat):
                kandidat.append(x)
            else:
                pass
        if(result[kandidat[0]] > result[kandidat[1]]):
            x = pop[kandidat[0]]
        else:
            x = pop[kandidat[1]]

        if(result[kandidat[2]] > result[kandidat[3]]):
            y = pop[kandidat[2]]
        else:
            y = pop[kandidat[3]]
#         print("========================================================================")
#         print("x = ",x)
#         print("y = ",y)
        return x, y
    
    def crossover(self, individu1, individu2):
        '''
        crossover dengan single point mutation
        
        return new offspring
        '''
        prandom = np.random.uniform(0,1)
        
        if prandom < self.pc:
            # lakukan crossover
            point = random.randint(0,3)
        
            papa = list(individu1[:point])
            mama = list(individu2[point:])
            offspring = papa+mama 
            return np.array(offspring)     
        else:
            '''
            return kan random mama atau papa
            '''
            prob=random.randint(0,1)
            if(prob==0):
                offspr = list(individu1)
                return np.array(offspr)
            else:
                offspr = list(individu2)
                return np.array(offspr)
    
    def mutation(self, individu, num_of_gen):
        scan = self.self_scan()
        '''
        mutasi
        lakukan mutasi hanya untuk 2 gen dalam 1 individu jika propbabiliti individu lebih kecil dari pm
        '''
        pidv = np.random.uniform(0,1)
        #print(pidv)
        if pidv < self.pm:
            
            # lakukan pemilihan random gen
            gen_bermutasi = np.random.choice([i for i in range(self.num_of_gen)], num_of_gen)
            #print(gen_bermutasi)
            
            for i in gen_bermutasi:
                
                individu[i] = np.random.uniform(0,1)
            ##################### hitung FV langsung
            heur=ga.self_scan()
            temporary=[]
            for i in range(len(heur)):
                hasil=heur[i]*individu
                temporary.append(hasil)
            res=0
            for j in range(len(temporary)):
                res+= temporary[j][0]+temporary[j][1]+temporary[j][2]+temporary[j][3]+temporary[j][4]-temporary[j][5]
            result=res
            return individu,result
        
        else:
            heur=ga.self_scan()
            temporary=[]
            for i in range(len(heur)):
                hasil=heur[i]*individu
                temporary.append(hasil)
            res=0
            for j in range(len(temporary)):
                res+= temporary[j][0]+temporary[j][1]+temporary[j][2]+temporary[j][3]+temporary[j][4]-temporary[j][5]
            result=res
            return individu,result
        
    def elitism(self,daftar,new_individu,fv_new):
        temp=daftar[0]
        hapus_idx=0
        for i in range(len(daftar)):
            if(daftar[i]<temp):
                temp=daftar[i]
                hapus_idx = i
                #print("hapus idx=",hapus_idx)
        if(fv_new>=daftar[hapus_idx]):
            #print('populasi yang terganti =',hapus_idx)
            daftar[hapus_idx]=fv_new
            pop[hapus_idx]=new_individu
            return pop,daftar
        else:
            #print("generasi ini tidak terganti")
            return pop,daftar
    def moving(self,daftar):
        temp=daftar[0]
        idx_terpilih=0
        for i in range(len(daftar)):
            if(daftar[i]>temp):
                temp=daftar[i]
                idx_terpilih = i
        print("individu terpilih adalah individu ke ",idx_terpilih)
        return idx_terpilih
    def move_lubang(self,daftar):
        temp=daftar[0]
        idx_terpilih=0
        for i in range(len(daftar)):
            if(daftar[i]>temp):
                temp=daftar[i]
                idx_terpilih = i
        print("lubang terpilih adalah lubang ke ",idx_terpilih)
        return idx_terpilih
################### Mancala Game ####################
from random import randint
#? 
#!                             (PLAYER)
#?              [0]  [1]  [2]   [3]   [4]   [5]   [6]
#*  [store_AI]                                            [store_player]
#?              [0]   [1]   [2]   [3]  [4]   [5]    [6]
#!                            (AI)
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
lanjut=0
lanjut_ai=0
#! fungsi untuk memperlihatkan isi dari board mancala
def show(board_ai,board_player,store_ai,store_player):
    print("########= PLAYER =##########")
    print('==',board_ai,'==')
    print(store_ai,'===================',store_player)
    print('==',board_player,'==')
    print("########= AI =######\n")
#! fungsi untuk move AI
def move_ai(lubang):
    global lanjut
    global last,idx_last
    last=0
    rock=board['player'][lubang]
    sisa=rock
    print("jumlah rock yang diambil = ",rock,'di lubang ke ',lubang)
    board['player'][lubang]=0
    for i in range(rock):
        l=lubang+i+1
        sisa-=1
        if(l==7):
            store['player']+=1
            lanjut=1
            last=0
        elif(l>7):
            for x in range(sisa+1):
                if(x>6 and x<14):
                    board['player'][abs(x-7)]+=1
                    lanjut=0
                    last,idx_last=board['player'][abs(x-7)],abs(x-7)
                elif(x==14):
                    store['player']+=1
                    lanjut=1 
                    
                elif(x>14):
                    
                    board['AI'][abs(x-21)]+=1
                    lanjut=0
                    # last,idx_last=board['AI'][abs(x-21)],abs(x-21)
                    last=0
                else:
                    board['AI'][(6-x)]+=1
                    lanjut=0
                    # last,idx_last=board['AI'][(6-x)],(6-x)
                    last=0
            
            if(last==1 and (board['AI'][idx_last]>0)):
                store['player']+=((board['AI'][idx_last])+1)
                board['player'][idx_last]=0
                board['AI'][idx_last]=0
            break
        else:
            board['player'][l]+=1
            lanjut=0
            last,idx_last=board['player'][l],l
    if(last==1 and (board['AI'][idx_last]>0)):
        store['player']+=((board['AI'][idx_last])+1)
        board['player'][idx_last]=0
        board['AI'][idx_last]=0
#    show(board['AI'],board['player'],store['AI'],store['player'])
#! fungsi untuk move player
def move_p(lubang):
    global lanjut_ai
    global last,idx_last
    last=0
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
            lanjut_ai=1
            last=0
        elif(l<-1):
            if (temp>=7 and temp<14):
                board['AI'][13-temp]+=1
                lanjut_ai=0
                last,idx_last=board['AI'][13-temp],(13-temp)
            elif (temp==14):
                store['AI']+=1
                lanjut_ai=1
            elif(temp>14):
                board['player'][abs(15-temp)]+=1
                lanjut_ai=0
                last=0
                # last,idx_last=board['player'][abs(15-temp)],abs(15-temp)
            else:
                board['player'][temp]+=1
                lanjut_ai=0
                last=0
                # last,idx_last=board['player'][temp],temp
            temp+=1
        else:
            board['AI'][l]+=1
            lanjut_ai=0
            last,idx_last=board['AI'][l],l
    if(last==1 and (board['player'][idx_last]>0)):
        store['AI']+=((board['player'][idx_last])+1)
        board['AI'][idx_last]=0
        board['player'][idx_last]=0
        
#    show(board['AI'],board['player'],store['AI'],store['player'])
#! fungsi untuk menghitung skor ketika step sudah habis atau permainan berakhir
def hitung_skor(lumbung_player,lumbung_ai):
    if(lumbung_player>lumbung_ai):
        return print("pemenang adalah player")
    else:
        return print("pemenang adalah AI")
##! jalankan algoritma mencuri cekk dahulu apakah berhenti di 0 
def curi():
    '''
    jika batu yang di gerakan sudah berhenti langsung dicek jumlah batunya 
    if total_batu == 1 :
        maka nilai lumbung di tambahkan dengan lubang di depan nya
    else:
        maka pass saja
    '''
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
#! menentukan siapa yang main duluan
first=randint(0,1)

'''
setting param
'''
# SELF_STATE = [1,2,2,4,8,5,12]
# OPPONENT_STATE = [6,7,8,9,2,4,12]
NUMBER_OF_GEN = 6
NUMBER_OF_POPULATION = 10
NUMBER_OF_GENERATION = 10
PC = 0.8
PM = 0.5
ga = MancalaGA(board['AI'], board['player'], NUMBER_OF_GEN, NUMBER_OF_POPULATION, NUMBER_OF_GENERATION, PC, PM)

ga.self_scan()
pop = ga.population()



# if(first==0):
#     print("generate random first => [PLAYER MAIN DULUAN]\n")
#     while (turn<20):
#         print("\nMulai Turn ",turn)
#         turn_player= int(input('[PLAYER MAIN], lubang ke berapa yang mau diambil? '))
#         if (turn_player>6):
#             print('\n######## WARNING! ########\nmasukan ulang lubang yang akan diambil\n')
#         else:
#             move_ai(turn_player)
#             show(board['AI'],board['player'],store['AI'],store['player'])
#             #! cek main lagi atau tidak            
#             if(lanjut==1):
#                 turn_player= int(input('[PLAYER MAIN LAGI], lubang ke berapa yang mau diambil? '))
#                 move_ai(turn_player)
#                 show(board['AI'],board['player'],store['AI'],store['player'])
#                 turn+=1
# #! giliran lawan satunya
#             ga.self_scan()
#             for iterasi in range(0,10):
#                 #print("###################### GENERASI KE ",iterasi," #######################")
#                 ga.selection(pop, verbose=True)
#                 ga.rata_fitness
#                 turnamen = ga.turnamen(pop)
#                 c = ga.crossover(turnamen[0], turnamen[1])
#                 new_individu,fv_new=ga.mutation(c,2)
#                 daftar=ga.rata_fitness
#                 pop,f=ga.elitism(daftar,new_individu,fv_new)
                
#             best_individu=ga.moving(daftar)
#             p=pop[best_individu]
#             sc=ga.self_scan()
#             list_scan=[]
#             for i in sc.items():
#                 list_scan.append(i[1])
#             np.array(list_scan)
#             skalar=np.array(list_scan)*p
#             hsl=[]
#             for c in range(len(skalar)):
#                 h=np.sum(skalar[c][0:4])-skalar[c][-1]
#                 hsl.append(h)
#             best_choice = ga.move_lubang(hsl)            
# #            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
#             move_p(best_choice)

#             show(board['AI'],board['player'],store['AI'],store['player'])
#             turn+=1
#             #! cek main lagi atau tidak
#             if(lanjut_ai==1):
#                 ga.self_scan()
#                 for iterasi in range(0,10):
#                     #print("###################### GENERASI KE ",iterasi," #######################")
#                     ga.selection(pop, verbose=True)
#                     ga.rata_fitness
#                     turnamen = ga.turnamen(pop)
#                     c = ga.crossover(turnamen[0], turnamen[1])
#                     new_individu,fv_new=ga.mutation(c,2)
#                     daftar=ga.rata_fitness
#                     pop,f=ga.elitism(daftar,new_individu,fv_new)
                    
#                 best_individu=ga.moving(daftar)
#                 p=pop[best_individu]
#                 sc=ga.self_scan()
#                 list_scan=[]
#                 for i in sc.items():
#                     list_scan.append(i[1])
#                 np.array(list_scan)
#                 skalar=np.array(list_scan)*p
#                 hsl=[]
#                 for c in range(len(skalar)):
#                     h=np.sum(skalar[c][0:4])-skalar[c][-1]
#                     hsl.append(h)
#                 best_choice = ga.move_lubang(hsl)            
#     #            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
#                 move_p(best_choice)
#                 show(board['AI'],board['player'],store['AI'],store['player'])                
#                 turn+=1
# #! jika yang main AI duluan
# else:
#     print("generate random first => [AI MAIN DULUAN]\n")
#     while (turn<20):
#         print("\nMulai Turn ",turn)
        
#         ga.self_scan()
#         for iterasi in range(0,10):
#             #print("###################### GENERASI KE ",iterasi," #######################")
#             ga.selection(pop, verbose=True)
#             ga.rata_fitness
#             turnamen = ga.turnamen(pop)
#             c = ga.crossover(turnamen[0], turnamen[1])
#             new_individu,fv_new=ga.mutation(c,2)
#             daftar=ga.rata_fitness
#             pop,f=ga.elitism(daftar,new_individu,fv_new)
            
#         best_individu=ga.moving(daftar)
#         p=pop[best_individu]
#         sc=ga.self_scan()
#         list_scan=[]
#         for i in sc.items():
#             list_scan.append(i[1])
#         np.array(list_scan)
#         skalar=np.array(list_scan)*p
#         hsl=[]
#         for c in range(len(skalar)):
#             h=np.sum(skalar[c][0:4])-skalar[c][-1]
#             hsl.append(h)
#         best_choice = ga.move_lubang(hsl)            
# #            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
#         move_p(best_choice)
#         show(board['AI'],board['player'],store['AI'],store['player'])                
#         turn+=1
#         #move_p(best_choice)
#         #show(board['AI'],board['player'],store['AI'],store['player'])
#         #! cek main lagi atau tidak
#         if(lanjut_ai==1):
#             ga.self_scan()
#             for iterasi in range(0,10):
#                 #print("###################### GENERASI KE ",iterasi," #######################")
#                 ga.selection(pop, verbose=True)
#                 ga.rata_fitness
#                 turnamen = ga.turnamen(pop)
#                 c = ga.crossover(turnamen[0], turnamen[1])
#                 new_individu,fv_new=ga.mutation(c,2)
#                 daftar=ga.rata_fitness
#                 pop,f=ga.elitism(daftar,new_individu,fv_new)
                
#             best_individu=ga.moving(daftar)
#             p=pop[best_individu]
#             sc=ga.self_scan()
#             list_scan=[]
#             for i in sc.items():
#                 list_scan.append(i[1])
#             np.array(list_scan)
#             skalar=np.array(list_scan)*p
#             hsl=[]
#             for c in range(len(skalar)):
#                 h=np.sum(skalar[c][0:4])-skalar[c][-1]
#                 hsl.append(h)
#             best_choice = ga.move_lubang(hsl)            
# #            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
#             move_p(best_choice)
#             show(board['AI'],board['player'],store['AI'],store['player'])                
#             turn+=1
# #! giliran lawan satunya
#         turn_player= int(input('[player MAIN], lubang ke berapa yang mau diambil? '))
#         move_ai(turn_player)
#         show(board['AI'],board['player'],store['AI'],store['player'])
#         turn+=1
#         #! cek main lagi atau tidak
#         if(lanjut==1):
#             turn_player= int(input('[PLAYER MAIN LAGI], lubang ke berapa yang mau diambil? '))
#             move_ai(turn_player)
#             show(board['AI'],board['player'],store['AI'],store['player'])
#             turn+=1
            
# ##! hitung skor setelah turn selesai  
# print("Turn sudah selesai hasil perhitungan skor menentukan")
# hitung_skor(store['player'],store['AI'])
########################## !switch player and AI
print("first = ",first,'\n')
if(first==0):
    print("generate random first => [PLAYER MAIN DULUAN]\n")
    while (turn<20):
        print("\nMulai Turn ",turn)
        turn_player= int(input('[PLAYER MAIN], lubang ke berapa yang mau diambil? '))
        if (turn_player>6):
            print('\n######## WARNING! ########\nmasukan ulang lubang yang akan diambil\n')
        else:
            move_p(turn_player)
            show(board['AI'],board['player'],store['AI'],store['player'])
            #! cek main lagi atau tidak            
            while(lanjut_ai==1):
                turn_player= int(input('[PLAYER MAIN LAGI], lubang ke berapa yang mau diambil? '))
                move_p(turn_player)
                show(board['AI'],board['player'],store['AI'],store['player'])
                #turn+=1
#! giliran lawan satunya
            ga.self_scan()
            for iterasi in range(0,20):
                #print("###################### GENERASI KE ",iterasi," #######################")
                ga.selection(pop, verbose=True)
                ga.rata_fitness
                turnamen = ga.turnamen(pop)
                c = ga.crossover(turnamen[0], turnamen[1])
                new_individu,fv_new=ga.mutation(c,2)
                daftar=ga.rata_fitness
                pop,f=ga.elitism(daftar,new_individu,fv_new)
                
            best_individu=ga.moving(daftar)
            p=pop[best_individu]
            sc=ga.self_scan()
            list_scan=[]
            for i in sc.items():
                list_scan.append(i[1])
            np.array(list_scan)
            skalar=np.array(list_scan)*p
            hsl=[]
            for c in range(len(skalar)):
                h=np.sum(skalar[c][0:4])-skalar[c][-1]
                hsl.append(h)
            best_choice = ga.move_lubang(hsl)            
#            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
            move_ai(best_choice)

            show(board['AI'],board['player'],store['AI'],store['player'])
            turn+=1
            #! cek main lagi atau tidak
            while(lanjut==1):
                ga.self_scan()
                for iterasi in range(0,20):
                    #print("###################### GENERASI KE ",iterasi," #######################")
                    ga.selection(pop, verbose=True)
                    ga.rata_fitness
                    turnamen = ga.turnamen(pop)
                    c = ga.crossover(turnamen[0], turnamen[1])
                    new_individu,fv_new=ga.mutation(c,2)
                    daftar=ga.rata_fitness
                    pop,f=ga.elitism(daftar,new_individu,fv_new)
                    
                best_individu=ga.moving(daftar)
                p=pop[best_individu]
                sc=ga.self_scan()
                list_scan=[]
                for i in sc.items():
                    list_scan.append(i[1])
                np.array(list_scan)
                skalar=np.array(list_scan)*p
                hsl=[]
                for c in range(len(skalar)):
                    h=np.sum(skalar[c][0:4])-skalar[c][-1]
                    hsl.append(h)
                best_choice = ga.move_lubang(hsl)            
    #            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
                move_ai(best_choice)
                show(board['AI'],board['player'],store['AI'],store['player'])                
                #turn+=1
#! jika yang main AI duluan
else:
    print("generate random first => [AI MAIN DULUAN]\n")
    while (turn<20):
        print("\nMulai Turn ",turn)
        
        ga.self_scan()
        for iterasi in range(0,20):
            #print("###################### GENERASI KE ",iterasi," #######################")
            ga.selection(pop, verbose=True)
            ga.rata_fitness
            turnamen = ga.turnamen(pop)
            c = ga.crossover(turnamen[0], turnamen[1])
            new_individu,fv_new=ga.mutation(c,2)
            daftar=ga.rata_fitness
            pop,f=ga.elitism(daftar,new_individu,fv_new)
            
        best_individu=ga.moving(daftar)
        p=pop[best_individu]
        sc=ga.self_scan()
        list_scan=[]
        for i in sc.items():
            list_scan.append(i[1])
        np.array(list_scan)
        skalar=np.array(list_scan)*p
        hsl=[]
        for c in range(len(skalar)):
            h=np.sum(skalar[c][0:4])-skalar[c][-1]
            hsl.append(h)
        print("daftar FV tiap lubang, ",hsl)
        best_choice = ga.move_lubang(hsl)            
#            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
        move_ai(best_choice)
        show(board['AI'],board['player'],store['AI'],store['player'])                
        turn+=1
        print("lanjut = ",lanjut)
        #! cek main lagi atau tidak
        while(lanjut==1):
            print("[AI] MAIN LAGI")
            ga.self_scan()
            for iterasi in range(0,20):
                #print("###################### GENERASI KE ",iterasi," #######################")
                ga.selection(pop, verbose=True)
                ga.rata_fitness
                turnamen = ga.turnamen(pop)
                c = ga.crossover(turnamen[0], turnamen[1])
                new_individu,fv_new=ga.mutation(c,2)
                daftar=ga.rata_fitness
                pop,f=ga.elitism(daftar,new_individu,fv_new)
                
            best_individu=ga.moving(daftar)
            
            p=pop[best_individu]
            sc=ga.self_scan()
            list_scan=[]
            for i in sc.items():
                list_scan.append(i[1])
            np.array(list_scan)
            skalar=np.array(list_scan)*p
            hsl=[]
            for c in range(len(skalar)):
                h=np.sum(skalar[c][0:4])-skalar[c][-1]
                hsl.append(h)
            print("daftar FV tiap lubang, ",hsl)
            best_choice = ga.move_lubang(hsl)            
#            turn_ai= int(input('[AI MAIN], lubang ke berapa yang mau diambil? '))
            move_ai(best_choice)
            show(board['AI'],board['player'],store['AI'],store['player'])                
            #turn+=1
#! giliran lawan satunya
        turn_player= int(input('[player MAIN], lubang ke berapa yang mau diambil? '))
        move_p(turn_player)
        show(board['AI'],board['player'],store['AI'],store['player'])
        turn+=1
        #! cek main lagi atau tidak
        while(lanjut_ai==1):
            turn_player= int(input('[PLAYER MAIN LAGI], lubang ke berapa yang mau diambil? '))
            move_p(turn_player)
            show(board['AI'],board['player'],store['AI'],store['player'])
            #turn+=1
            
##! hitung skor setelah turn selesai  
print("Turn sudah selesai hasil perhitungan skor menentukan")
hitung_skor(store['AI'],store['player'])

from typing import Dict, List
import heapq
gidilebilecek_yerler: Dict[int, List[int]] = {
1: [2, 4, 5],
2: [1, 3, 4, 5, 6],
3: [2, 5, 6],
4: [1, 2, 5, 7, 8],
5: [1, 2, 3, 4, 6, 7, 8, 9],
6: [2, 3, 5, 8, 9],
7: [4, 5, 8],
8: [4, 5, 6, 7, 9],
9: [5, 6, 8]
 }
expanded_list = []
priority_queue = []
class Tile:
    def __init__(self,renk,goal_state,current_state,move_rate,adim_sayisi=0):
        self.state=current_state
        self.adim_sayisi=adim_sayisi
        self.is_goal_state=0
        self.fn=0
        self.renk=renk
        self.goal_state=goal_state
        self.move_rate=move_rate

    def __str__(self):
        return (f"Nesne Durumu:\n"
                f"  Renk: {self.renk}\n"
                f"  Konum: {self.state}\n"
                f"  Uzaklık: {self.fn}\n"
                f"  Step: {self.adim_sayisi}")

    def h_function(self):
        if (self.goal_state == self.state):
            self.is_goal_state = 1
        return self.is_goal_state
    def f_function(self,tile1,tile2):
        return - tile1.h_function() - tile2.h_function() - self.h_function() + self.adim_sayisi

    def expand(self,tile1,tile2):
        list = gidilebilecek_yerler.get(self.state,[])
        for i in list:
            if(tile1.state!=i and tile2.state!=i):
               tiles=Tile(self.renk,self.goal_state,i,self.move_rate,self.adim_sayisi+1)
               expanded_list.append(tiles)
        self.adim_sayisi+=1
        tile1.adim_sayisi+=1
        tile2.adim_sayisi+=1
        return expanded_list

    def add_fringe(self,list,priortyqueue,tile1,tile2):
        for i in list:
            value=i.f_function(tile1,tile2)
            heapq.heappush(priority_queue, (value, i.renk))

tile_r = Tile(renk='Kırmızı', goal_state=8, current_state=1, move_rate=0, adim_sayisi=0)
tile_g = Tile(renk='Yeşil', goal_state=7, current_state=3, move_rate=1, adim_sayisi=0)
tile_b = Tile(renk='Mavi', goal_state=9, current_state=2, move_rate=2, adim_sayisi=0)

print(tile_r) 
for i in range(10):
    list2 = tile_r.expand(tile_g, tile_b)
    for tile in list2:
        fvalue=tile.f_function(tile_g,tile_b)
        tile.fn=fvalue
        print(tile)
        print("fvalue",fvalue)
    en_kucuk_tile = min(list2, key=lambda x: x.fn)
    print("En küçük maliyetli taş:", en_kucuk_tile)
    priority_queue.append(en_kucuk_tile)
    tile_r.state=en_kucuk_tile.state
    expanded_list.clear()
    list2.clear()
    print("-------------------------------------------")
    list3=tile_g.expand(tile_r,tile_b)
    for tile in list3:
        fvalue=tile.f_function(tile_r,tile_b)
        tile.fn=fvalue
        print(tile)
        print("fvalue",fvalue)
    en_kucuk_tile = min(list3, key=lambda x: x.fn)
    print("En küçük maliyetli taş:", en_kucuk_tile)
    priority_queue.append(en_kucuk_tile)
    tile_g.state=en_kucuk_tile.state
    expanded_list.clear()
    list3.clear()
    print("-------------------------------------------")
    list4=tile_b.expand(tile_r,tile_g)
    for tile in list4:
        fvalue=tile.f_function(tile_r,tile_g)
        tile.fn=fvalue
        print(tile)
        print("fvalue",fvalue)
    en_kucuk_tile = min(list4, key=lambda x: x.fn)
    print("En küçük maliyetli taş:", en_kucuk_tile)
    priority_queue.append(en_kucuk_tile)
    tile_b.state=en_kucuk_tile.state
    expanded_list.clear()
    list4.clear()

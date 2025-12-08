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
priority_queue = []
class Tile:
    def __init__(self, renk, goal_state, current_state, adim_sayisi=0):
        self.state = current_state
        self.adim_sayisi = adim_sayisi
        self.is_goal_state = 0
        self.fn = 0
        self.renk = renk
        self.goal_state = goal_state

    def __str__(self):
        return (f"{self.renk} -> Hedef: {self.goal_state}, Konum: {self.state}, Step: {self.adim_sayisi}")

    def h_function(self):
        if self.goal_state == self.state:
            self.is_goal_state = 1
        return self.is_goal_state

    def f_function(self, tile1, tile2):
        return - tile1.h_function() - tile2.h_function() - self.h_function() + self.adim_sayisi

    def expand(self, tile1, tile2):
        local_expanded_list = []
        possible_moves = gidilebilecek_yerler.get(self.state, [])
        if (self.goal_state!=self.state or tile2.goal_state!=tile2.state or tile1.goal_state!=tile1.state):
            if self.adim_sayisi < 10 :
                for next_pos in possible_moves:
                    if tile1.state != next_pos and tile2.state != next_pos:
                        new_tile = Tile(self.renk, self.goal_state, next_pos, self.adim_sayisi + 1)
                        local_expanded_list.append(new_tile)
            return local_expanded_list



# --- BAŞLANGIÇ ---
tile_r = Tile(renk='Kırmızı', goal_state=1, current_state=8, adim_sayisi=0)
tile_g = Tile(renk='Yeşil', goal_state=6, current_state=1, adim_sayisi=0)
tile_b = Tile(renk='Mavi', goal_state=8, current_state=3, adim_sayisi=0)

print("SİMÜLASYON BAŞLIYOR...")

toplam_adim =0
while tile_r.adim_sayisi < 10 and tile_b.adim_sayisi < 10 and tile_g.adim_sayisi < 10:
    if (tile_r.goal_state==tile_r.state and tile_b.goal_state==tile_b.state and tile_g.goal_state==tile_g.state):
        print("\nHer taş hedefe ulaştı . Tebrikler !!!!")
        for i in priority_queue:
            print(i.__str__())
        break
    else:

        print(f"\n[{tile_r.renk} Taş Hamlesi - Şu anki Konum: {tile_r.state}, Hedef konumu : {tile_r.goal_state} , Step sayısı {tile_r.adim_sayisi}]")
        list2 = tile_r.expand(tile_g, tile_b)

        if not list2:
            print("  ! Gidecek yer yok (Sıkıştı).")
            break

        print("  Alternatifler:")
        for tile in list2:
            tile.fn = tile.f_function(tile_g, tile_b)
            print(f"    -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

        en_kucuk_tile = min(list2, key=lambda x: x.fn)
        print(f"  -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

        priority_queue.append(en_kucuk_tile)
        tile_r.state = en_kucuk_tile.state
        tile_r.adim_sayisi = en_kucuk_tile.adim_sayisi
        toplam_adim += 1
        tile_r.adim_sayisi = toplam_adim
        tile_g.adim_sayisi = toplam_adim
        tile_b.adim_sayisi = toplam_adim

        print(f"\n[{tile_g.renk} Taş Hamlesi - Şu anki Konum: {tile_g.state}, Hedef konumu : {tile_g.goal_state} ,Step sayısı {tile_r.adim_sayisi}]")
        list3 = tile_g.expand(tile_r, tile_b)

        if not list3:
            print("  ! Gidecek yer yok (Sıkıştı).")
            break

        print("  Alternatifler:")
        for tile in list3:
            tile.fn = tile.f_function(tile_r, tile_b)
            print(f"    -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

        en_kucuk_tile = min(list3, key=lambda x: x.fn)
        print(f"  -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

        priority_queue.append(en_kucuk_tile)
        tile_g.state = en_kucuk_tile.state
        tile_g.adim_sayisi = en_kucuk_tile.adim_sayisi
        toplam_adim += 1
        tile_r.adim_sayisi = toplam_adim
        tile_g.adim_sayisi = toplam_adim
        tile_b.adim_sayisi = toplam_adim

        print(f"\n[{tile_b.renk} Taş Hamlesi - Şu anki Konum: {tile_b.state}, Hedef konumu : {tile_b.goal_state} ,Step sayısı {tile_r.adim_sayisi}]")
        list4 = tile_b.expand(tile_r, tile_g)

        if not list4:
            print("  ! Gidecek yer yok (Sıkıştı).")
            break

        print("  Alternatifler:")
        for tile in list4:
            tile.fn = tile.f_function(tile_r, tile_g)
            print(f"    -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

        en_kucuk_tile = min(list4, key=lambda x: x.fn)
        print(f"  -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

        priority_queue.append(en_kucuk_tile)
        tile_b.state = en_kucuk_tile.state
        tile_b.adim_sayisi = en_kucuk_tile.adim_sayisi
        toplam_adim += 1
        tile_r.adim_sayisi = toplam_adim
        tile_g.adim_sayisi = toplam_adim
        tile_b.adim_sayisi = toplam_adim

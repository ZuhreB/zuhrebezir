import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Dict, List

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


class Tile:
    def __init__(self, renk, goal_state, current_state, adim_sayisi=0):
        self.state = current_state
        self.adim_sayisi = adim_sayisi
        self.is_goal_state = 1
        self.fn = 0
        self.renk = renk
        self.goal_state = goal_state

    def __str__(self):
        return (f"{self.renk} -> Hedef: {self.goal_state}, Konum: {self.state}, Step: {self.adim_sayisi}")

    def h_function(self):
        if self.goal_state == self.state:
            self.is_goal_state = 0
        return self.is_goal_state

    def f_function(self, tile1, tile2):
        return tile1.h_function() + tile2.h_function() + self.h_function() + self.adim_sayisi

    def expand(self, tile1, tile2):
        local_expanded_list = []
        possible_moves = gidilebilecek_yerler.get(self.state, [])
        if (self.goal_state != self.state or tile2.goal_state != tile2.state or tile1.goal_state != tile1.state):
            if self.adim_sayisi < 10:
                for next_pos in possible_moves:
                    if tile1.state != next_pos and tile2.state != next_pos:
                        new_tile = Tile(self.renk, self.goal_state, next_pos, self.adim_sayisi + 1)
                        local_expanded_list.append(new_tile)

        return local_expanded_list

class ProjectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tile Game")
        self.root.geometry("900x700")

        self.tile_r = None
        self.tile_g = None
        self.tile_b = None
        self.priority_queue = []
        self.toplam_adim = 0
        self.sira = 0  # 0: Kırmızı, 1: Yeşil, 2: Mavi

        self.setup_ui()

    def setup_ui(self):

        input_frame = tk.LabelFrame(self.root, text="Başlangıç ve Hedef Konumları (1-9)", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Kırmızı
        tk.Label(input_frame, text="Kırmızı (R) Başlangıç:", fg="red").grid(row=0, column=0)
        self.entry_r_start = tk.Entry(input_frame, width=5)
        self.entry_r_start.grid(row=0, column=1)
        tk.Label(input_frame, text="Kırmızı (R) Hedef:", fg="red").grid(row=0, column=2)
        self.entry_r_goal = tk.Entry(input_frame, width=5)
        self.entry_r_goal.grid(row=0, column=3)

        # Yeşil
        tk.Label(input_frame, text="Yeşil (G) Başlangıç:", fg="green").grid(row=1, column=0)
        self.entry_g_start = tk.Entry(input_frame, width=5)
        self.entry_g_start.grid(row=1, column=1)
        tk.Label(input_frame, text="Yeşil (G) Hedef:", fg="green").grid(row=1, column=2)
        self.entry_g_goal = tk.Entry(input_frame, width=5)
        self.entry_g_goal.grid(row=1, column=3)

        # Mavi
        tk.Label(input_frame, text="Mavi (B) Başlangıç:", fg="blue").grid(row=2, column=0)
        self.entry_b_start = tk.Entry(input_frame, width=5)
        self.entry_b_start.grid(row=2, column=1)
        tk.Label(input_frame, text="Mavi (B) Hedef:", fg="blue").grid(row=2, column=2)
        self.entry_b_goal = tk.Entry(input_frame, width=5)
        self.entry_b_goal.grid(row=2, column=3)

        # Butonlar
        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=0, column=4, rowspan=3, padx=20)

        self.btn_start = tk.Button(btn_frame, text="Simülasyonu Başlat", command=self.initialize_game, bg="lightgray")
        self.btn_start.pack(pady=5)

        self.btn_step = tk.Button(btn_frame, text="Sıradaki Hamle", command=self.next_step, state="disabled",
                                  bg="lightblue")
        self.btn_step.pack(pady=5)

        #Tahta
        self.board_frame = tk.Frame(self.root, bg="black")
        self.board_frame.pack(pady=10)

        self.cells = {}
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3

            cell = tk.Canvas(self.board_frame, width=80, height=80, bg="white", highlightthickness=1)
            cell.grid(row=row, column=col, padx=2, pady=2)

            cell.create_text(15, 15, text=str(i), fill="gray")
            self.cells[i] = cell

        log_frame = tk.LabelFrame(self.root, text="Alternatif yollar ve Gidiş yolu", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill="both", expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def draw_board(self):
        for i in range(1, 10):
            self.cells[i].delete("tile")
            self.cells[i].config(bg="white")

        # Taşları çiz
        if self.tile_r:
            self.draw_tile(self.tile_r.state, "red", "R")
        if self.tile_g:
            self.draw_tile(self.tile_g.state, "green", "G")
        if self.tile_b:
            self.draw_tile(self.tile_b.state, "blue", "B")

    def draw_tile(self, pos, color, text):
        canvas = self.cells[pos]
        # Daire çiziyorum
        canvas.create_oval(10, 10, 70, 70, fill=color, outline="black", tags="tile")
        # Harf yazıyorum
        canvas.create_text(40, 40, text=text, fill="white", font=("Arial", 20, "bold"), tags="tile")

    def initialize_game(self):
        try:
            r_start = int(self.entry_r_start.get())
            r_goal = int(self.entry_r_goal.get())
            g_start = int(self.entry_g_start.get())
            g_goal = int(self.entry_g_goal.get())
            b_start = int(self.entry_b_start.get())
            b_goal = int(self.entry_b_goal.get())

            if len({r_start, g_start, b_start}) != 3:
                messagebox.showerror("Hata", "Başlangıç konumları aynı olamaz!")
                return

            self.tile_r = Tile(renk='Kırmızı', goal_state=r_goal, current_state=r_start, adim_sayisi=0)
            self.tile_g = Tile(renk='Yeşil', goal_state=g_goal, current_state=g_start, adim_sayisi=0)
            self.tile_b = Tile(renk='Mavi', goal_state=b_goal, current_state=b_start, adim_sayisi=0)

            self.priority_queue = []
            self.toplam_adim = 0
            self.sira = 0  # Sıra Kırmızıda

            self.log_text.delete(1.0, tk.END)
            self.log("SİMÜLASYON BAŞLIYOR...")
            self.log(f"Başlangıç: R->{r_start}, G->{g_start}, B->{b_start}")

            self.draw_board()
            self.btn_step.config(state="normal")
            self.btn_start.config(text="Yeniden Başlat")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm alanlara 1-9 arası sayı giriniz.")

    def next_step(self):
        if self.tile_r.adim_sayisi >= 10 and self.tile_b.adim_sayisi >= 10 and self.tile_g.adim_sayisi >= 10:
            self.log("\n ! Maksimum adım sayısına ulaşıldı (10). Çözüm bulunamadı.")
            self.btn_step.config(state="disabled")
            return

        if (self.tile_r.goal_state == self.tile_r.state and
                self.tile_b.goal_state == self.tile_b.state and
                self.tile_g.goal_state == self.tile_g.state):
            self.log("\nHer taş hedefe ulaştı. Tebrikler !!!!")
            messagebox.showinfo("Başarılı", "Tüm taşlar hedefe ulaştı!")
            self.btn_step.config(state="disabled")
            return

        if self.sira == 0:
            self.log(
                f"\n[{self.tile_r.renk} Taş Hamlesi - Şu anki: {self.tile_r.state}, Hedef: {self.tile_r.goal_state}, Step: {self.tile_r.adim_sayisi}]")

            list2 = self.tile_r.expand(self.tile_g, self.tile_b)

            if not list2:
                self.log(" ! Gidecek yer yok (Sıkıştı).")
                self.btn_step.config(state="disabled")
                return

            self.log(" Alternatifler:")
            for tile in list2:
                tile.fn = tile.f_function(self.tile_g, self.tile_b)
                self.log(f" -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

            en_kucuk_tile = min(list2, key=lambda x: x.fn)
            self.log(f" -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

            self.priority_queue.append(en_kucuk_tile)
            self.tile_r.state = en_kucuk_tile.state
            self.tile_r.adim_sayisi = en_kucuk_tile.adim_sayisi

            self.toplam_adim += 1
            self.tile_r.adim_sayisi = self.toplam_adim
            self.tile_g.adim_sayisi = self.toplam_adim
            self.tile_b.adim_sayisi = self.toplam_adim

            self.sira = 1  # Sıra Yeşile geçiyo

        elif self.sira == 1:
            self.log(
                f"\n[{self.tile_g.renk} Taş Hamlesi - Şu anki: {self.tile_g.state}, Hedef: {self.tile_g.goal_state}, Step: {self.tile_g.adim_sayisi}]")

            list3 = self.tile_g.expand(self.tile_r, self.tile_b)

            if not list3:
                self.log(" ! Gidecek yer yok (Sıkıştı).")
                self.btn_step.config(state="disabled")
                return

            self.log(" Alternatifler:")
            for tile in list3:
                tile.fn = tile.f_function(self.tile_r, self.tile_b)
                self.log(f" -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

            en_kucuk_tile = min(list3, key=lambda x: x.fn)
            self.log(f" -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

            self.priority_queue.append(en_kucuk_tile)
            self.tile_g.state = en_kucuk_tile.state
            self.tile_g.adim_sayisi = en_kucuk_tile.adim_sayisi

            self.toplam_adim += 1
            self.tile_r.adim_sayisi = self.toplam_adim
            self.tile_g.adim_sayisi = self.toplam_adim
            self.tile_b.adim_sayisi = self.toplam_adim

            self.sira = 2  # Sıra Maviye geçiyo

        elif self.sira == 2:
            self.log(
                f"\n[{self.tile_b.renk} Taş Hamlesi - Şu anki: {self.tile_b.state}, Hedef: {self.tile_b.goal_state}, Step: {self.tile_b.adim_sayisi}]")

            list4 = self.tile_b.expand(self.tile_r, self.tile_g)

            if not list4:
                self.log(" ! Gidecek yer yok (Sıkıştı).")
                self.btn_step.config(state="disabled")
                return

            self.log(" Alternatifler:")
            for tile in list4:
                tile.fn = tile.f_function(self.tile_r, self.tile_g)
                self.log(f" -> Gidebileceği: {tile.state} | Maliyet (fn): {tile.fn}")

            en_kucuk_tile = min(list4, key=lambda x: x.fn)
            self.log(f" -> TERCİH EDİLEN: Konum {en_kucuk_tile.state} (Maliyet en düşük: {en_kucuk_tile.fn})")

            self.priority_queue.append(en_kucuk_tile)
            self.tile_b.state = en_kucuk_tile.state
            self.tile_b.adim_sayisi = en_kucuk_tile.adim_sayisi

            self.toplam_adim += 1
            self.tile_r.adim_sayisi = self.toplam_adim
            self.tile_g.adim_sayisi = self.toplam_adim
            self.tile_b.adim_sayisi = self.toplam_adim

            self.sira = 0  # Sıra tekrar Kırmızıya geçiyor

        # Tahtayı güncelliyorum
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectGUI(root)
    root.mainloop()
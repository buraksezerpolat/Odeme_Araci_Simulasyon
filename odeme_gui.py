import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests

def kart_formatla(event=None):
    metin = entry_kart.get()
    temiz = ''.join(filter(str.isdigit, metin))[:16]
    gruplar = [temiz[i:i+4] for i in range(0, len(temiz), 4)]
    yeni_metin = '-'.join(gruplar)

    entry_kart.delete(0, tk.END)
    entry_kart.insert(0, yeni_metin)

def cvc_kontrol(event=None):
    metin = entry_cvc.get()
    temiz = ''.join(filter(str.isdigit, metin))[:3]
    entry_cvc.delete(0, tk.END)
    entry_cvc.insert(0, temiz)

def skt_kontrol(event=None):
    metin = entry_skt.get()
    temiz = ''.join(filter(str.isdigit, metin))[:4]
    if len(temiz) >= 3:
        yeni_metin = temiz[:2] + '/' + temiz[2:]
    else:
        yeni_metin = temiz
    entry_skt.delete(0, tk.END)
    entry_skt.insert(0, yeni_metin)

def skt_gecerlili_mi(skt):
    try:
        if len(skt) != 5 or skt[2] != '/':
            return False
        ay, yil = skt.split('/')
        ay = int(ay)
        yil = int("20" + yil)

        if not (1 <= ay <= 12):
            return False
        
        bugün = datetime.now()
        skt_tarihi = datetime(yil, ay, 1)

        return skt_tarihi >= datetime(bugün.year, bugün.month, 1)
    except:
        return False

def  tutar_kontrol(event=None):
    metin = entry_tutar.get()
    temiz = ''.join(filter(str.isdigit, metin))
    entry_tutar.delete(0, tk.END)
    entry_tutar.insert(0, temiz)

def odeme_yap():
    kart = entry_kart.get().replace('-', '')
    skt = entry_skt.get()
    cvc = entry_cvc.get()
    tutar = entry_tutar.get()

    if not (kart.isdigit() and len(kart) == 16):
        messagebox.showerror("Hata", "Kart numarası 16 haneli olmalıdır ve sadece rakamlardan oluşmalıdır.")
        return
    
    if not (cvc.isdigit() and len(cvc) == 3):
        messagebox.showerror("Hata", "CVC 3 haneli olmalıdır ve sadece rakamlardan oluşmalıdır.")
        return
    
    if not skt_gecerlili_mi(skt):
        messagebox.showerror("Hata", "Son kullanma tarihi geçersiz veya geçmişte.")
        return

    if not all([kart, skt, cvc, tutar]):
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return
    try:
        response = requests.post(
            "http://localhost:5000/odeme",
            json={"kart": kart, "skt": skt, "cvc": cvc, "tutar": tutar}
        )
        sonuc = response.json()
        if response.status_code == 200 and sonuc.get("durum") == "başarılı":
            messagebox.showinfo("Başarılı", sonuc["mesaj"])
        else:
            messagebox.showerror("Hata", sonuc.get("mesaj", "Bilinmeyen hata."))
    except Exception as e:
        messagebox.showerror("Hata", f"Sunucuya bağlanılamadı: {e}")    


urun_listesi = []

def toplam_tutari_guncelle():
    toplam = 0
    for fiyat, adet_var in urun_listesi:
        toplam += fiyat * adet_var.get()
        
    entry_tutar.configure(state="normal")
    entry_tutar.delete(0, tk.END)
    entry_tutar.insert(0, str(toplam) + ' TL')
    entry_tutar.configure(state="readonly")

urun_sayaci = 0

def urun_olustur(parent, isim, fiyat):
    global urun_sayaci

    adet = tk.IntVar(value=0)
    urun_listesi.append((fiyat, adet))

    urun_frame = tk.Frame(parent, bd=1, relief="solid", padx=10, pady=10)

    satir = urun_sayaci // 3
    sutun = urun_sayaci % 3
    urun_frame.grid(row=satir, column=sutun, padx=10, pady=10, sticky="nsew")

    tk.Label(urun_frame, text=f"Ürün: {isim}", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    fiyat_label = tk.Label(urun_frame, text="", font=("Arial", 11))
    fiyat_label.pack()

    adet_frame = tk.Frame(urun_frame)
    adet_frame.pack(pady=5)

    def fiyat_label_guncelle():
        fiyat_label.config(text=f"Fiyat: {fiyat} TL Adet")
    

    def arttir():
        adet.set(adet.get() + 1)
        fiyat_label_guncelle()
        toplam_tutari_guncelle()
    
    def azalt():
        if adet.get() > 0:
            adet.set(adet.get() - 1)
            fiyat_label_guncelle()
            toplam_tutari_guncelle()

    tk.Button(adet_frame, text="-", command=azalt).pack(side=tk.LEFT)
    tk.Label(adet_frame, textvariable=adet).pack(side=tk.LEFT)
    tk.Button(adet_frame, text="+", command=arttir).pack(side=tk.LEFT)

    fiyat_label_guncelle()
    toplam_tutari_guncelle()

    urun_sayaci += 1

pencere = tk.Tk()
pencere.title("Ödeme Ekranı")
pencere.geometry("800x600")

tk.Label(pencere, text="Kart Numarası:").pack()
entry_kart = tk.Entry(pencere)
entry_kart.pack()
entry_kart.bind("<KeyRelease>", kart_formatla)

tk.Label(pencere, text="Son Kullanma Tarihi (AA/YY):").pack()
entry_skt = tk.Entry(pencere)
entry_skt.pack()
entry_skt.bind("<KeyRelease>", skt_kontrol)

tk.Label(pencere, text="CVC:").pack()
entry_cvc = tk.Entry(pencere)
entry_cvc.pack()
event_cvc = entry_cvc.bind("<KeyRelease>", cvc_kontrol)

tk.Label(pencere, text="Tutar (TL):").pack()
entry_tutar = tk.Entry(pencere, state="readonly")
entry_tutar.pack()

tk.Button(pencere, text="Ödeme Yap", command=odeme_yap).pack(pady=15)

canvas_frame = tk.Frame(pencere, height=250)
canvas_frame.pack(fill="x", padx=100, pady=10)

canvas = tk.Canvas(canvas_frame)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
urunler_frame = tk.Frame(canvas)


canvas.bind(
    "Configure",
    lambda e: canvas.itemconfig(canvas_window, width=e.width)
)

urunler_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas_window = canvas.create_window((0, 0), window=urunler_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

urun_olustur(urunler_frame, "Kitap", 100)
urun_olustur(urunler_frame, "Kalem", 25)
urun_olustur(urunler_frame, "Defter", 50)
urun_olustur(urunler_frame, "Silgi", 10)
urun_olustur(urunler_frame, "Cetvel", 15)
urun_olustur(urunler_frame, "Cetvel", 15)
urun_olustur(urunler_frame, "Cetvel", 15)
urun_olustur(urunler_frame, "Renkli Kalem", 30)

for i in range(3):
    urunler_frame.columnconfigure(i, weight=1)
pencere.mainloop()

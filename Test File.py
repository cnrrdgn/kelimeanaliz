from os import link
import tkinter as tk
import zeyrek
import requests
import webbrowser

word = ""

def openLink(event):
    webbrowser.open(f"https://sozluk.gov.tr/?kelime={word}")

def getMeaningAndExample(kelime):
    url = f"https://sozluk.gov.tr/gts?ara={kelime}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
    except Exception as e:
        return "Anlam alınamadı.", "Örnek alınamadı."
    
    anlam = "Anlam bulunamadı."
    ornek = "Örnek bulunamadı."
    
    try:
        if data and "anlamlarListe" in data[0]:
            anlam = data[0]["anlamlarListe"][0]["anlam"]
            if "orneklerListe" in data[0]["anlamlarListe"][0]:
                ornek = data[0]["anlamlarListe"][0]["orneklerListe"][0]["ornek"]
    except Exception as e:
        pass
    
    return anlam, ornek


analyzer = zeyrek.MorphAnalyzer()
cache = {}

TranslateData = {
    "Inf1": "Mastar eki",
    "Verb": "Fiil",
    "Noun": "İsim",
    "Past": "Görülen geçmiş zaman",
    "Narr": "Duyulan geçmiş zaman",
    "NarrPart": "Duyulan geçmiş zaman",
    "Pres": "Şimdiki zaman",
    "Prog2": "Şimdiki zaman",
    "Fut": "Gelecek zaman",
    "Aor": "Geniş zaman",
    "Ly": "Pekiştirme eki",
    "Num": "Sayı",
    "With": "Olumluluk eki",
    "Without": "Olumsuzluk eki",
    "Adj": "Sıfat",
    "Adv": "Zarf",
    "Agt": "Özne",
    "Become": "Dönüşme eki",
    "Able": "Yeterlilik fiili",
    "Repeat": "Sürerlik fiili",
    "Almost": "Yaklaşma fiili",
    "Hastily": "Tezlik fiili",
    "A1sg": "1. Tekil Şahıs",
    "A2sg": "2. Tekil Şahıs",
    "A3sg": "3. Tekil Şahıs",
    "A1pl": "1. Çoğul Şahıs",
    "A2pl": "2. Çoğul Şahıs",
    "A3pl": "3. Çoğul Şahıs",
    "P1sg": "İyelik eki",
    "P1pl": "İyelik eki",
    "Nom": "Yalın hâl",
    "Acc": "Belirtme hâli",
    "Dat": "Yönelme hâli",
    "Loc": "Bulunma hâli",
    "Abl": "Ayrılma hâli",
    "Gen": "Tamlayan hâli",
    "Ins": "Araç hâli",
    "Cop": "İsim-fiil eki",
    "Caus": "Ettirgenlik",
    "Pass": "Edilgenlik",
    "Nec": "Gereklilik kipi",
    "Desr": "İstek kipi",
    "Cond": "Dilek kipi",
    "Imp": "Emir Kipi",
    "Prog1": "Şimdiki zaman eki",
    "PastPart": "Sıfat-fiil (mişli geçmiş)",
    "Neg": "Olumsuzluk",
    "Pos": "Olumlu"
}

def translateTable(ek_listesi):
    return [TranslateData.get(ek, ek) for ek in ek_listesi]

def translateString(word):
    return TranslateData[word]

def analize(word):
    if word in cache:
        return cache[word]
    result = analyzer.analyze(word)
    if not result or not result[0]:
        return None  # Geçersiz kelime için
    result = result[0][0]
    cache[word] = result
    return result

def analizYap():
    kelime = giris.get()
    sonuc = analize(kelime)
    if not sonuc:
        sonuc_label.config(text="Bu kelime çözümlenemedi.")
        return
    
    kök = sonuc.lemma
    tur = translateString(sonuc.pos)
    ekler = ', '.join(translateTable(sonuc.morphemes))
    anlam, örnek = getMeaningAndExample(kök)
    
    global word
    word = kök

    sonuc_metni = f"Kök: {kök}\n\nTür: {tur}\n\nEkler: {ekler}\n\nSözcüğün Anlamı: {anlam}\n\nSözcüğün Kullanımı: {örnek}"
    sonuc_label.config(text=sonuc_metni)

# Arayüz başlat
pencere = tk.Tk()
pencere.title("Kelime Analiz Aracı")

# Giriş kutusu
giris = tk.Entry(pencere, font=("Arial", 14))
giris.pack(padx=20, pady=10)

# Buton
buton = tk.Button(pencere, text="Analiz Et", font=("Arial", 14), command=analizYap)
buton.pack(padx=20, pady=5)

# Sonuç etiketi
sonuc_label = tk.Label(pencere, text="", font=("Arial", 14), justify="left")
sonuc_label.pack(padx=20, pady=10)

#Link
link_label = tk.Label(pencere, text="TDK'de Ara", font=("Arial", 12, "underline"), fg="blue", cursor="hand2")
link_label.pack(pady=20)
link_label.bind("<Button-1>", openLink)

# Pencereyi çalıştır
pencere.mainloop()

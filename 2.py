import nltk
import string
import os
from nltk.util import trigrams
from collections import defaultdict, Counter

def clear(metin):
    # Noktalama işaretlerini temizle
    temiz = metin.translate(str.maketrans('', '', string.punctuation))
    # Satır sonlarını ve fazladan boşlukları boşlukla değiştir
    temiz = temiz.replace('\n', ' ').replace('\r', ' ')
    # Küçük harfe çevir
    temiz = temiz.lower()
    # Fazla boşlukları da sadeleştir
    temiz = ' '.join(temiz.split())
    return temiz

# Yeni klasör yolu
klasor_yolu = os.path.join(os.path.expanduser("~"), "Documents", "Yapay Zeka Eğitim Veri Seti")

# Dosya yolları
dosya1 = os.path.join(klasor_yolu, "Metin1.txt")
dosya2 = os.path.join(klasor_yolu, "Metin2.txt")
dosya3 = os.path.join(klasor_yolu, "Metin3.txt")
dosya4 = os.path.join(klasor_yolu, "Metin4.txt")

# Dosyaları oku
with open(dosya1, "r", encoding="utf-8") as f1:
    metin1 = clear(f1.read())

with open(dosya2, "r", encoding="utf-8") as f2:
    metin2 = clear(f2.read())

with open(dosya3, "r", encoding="utf-8") as f3:
    metin3 = clear(f3.read())

with open(dosya4, "r", encoding="utf-8") as f4:
    metin4 = clear(f4.read())

metin = metin1 + metin2 + metin3 + metin4

kelimeler = nltk.word_tokenize(metin)
trigramlar = list(trigrams(kelimeler))
gecisler = defaultdict(Counter)

for w1, w2, w3 in trigramlar:
    gecisler[(w1, w2)][w3] += 1

def tahmin_et(k1, k2):
    anahtar = (k1, k2)
    if anahtar not in gecisler:
        return "Bilmiyorum :("
    return gecisler[anahtar].most_common(1)[0][0]

def cumle_olustur(k1, k2, max_uzunluk):
    cumle = [k1, k2]
    for _ in range(max_uzunluk - 2):
        sonraki = tahmin_et(cumle[-2], cumle[-1])
        if sonraki == "Bilmiyorum :(":
            break
        cumle.append(sonraki)
    return ' '.join(cumle)

while True:
    girdi = input("İki kelime yaz (çıkmak için 'q'): ")
    if girdi == 'q':
        break
    kelimeler_girdi = girdi.split()
    if len(kelimeler_girdi) != 2:
        print("Lütfen 2 kelime gir.")
        continue
    k1, k2 = kelimeler_girdi
    k1 = clear(k1)
    k2 = clear(k2)
    print(f"Cümle: {cumle_olustur(k1, k2, 35)}")

from flask import Flask, render_template, request
import zeyrek
import requests
import nltk
import os

nltk.download('punkt')

app = Flask(__name__)
analyzer = zeyrek.MorphAnalyzer()
cache = {}

TranslateData = {
    "Inf1": "Mastar eki", "Verb": "Fiil", "Noun": "İsim", "Past": "Görülen geçmiş zaman",
    "Narr": "Duyulan geçmiş zaman", "NarrPart": "Duyulan geçmiş zaman", "Pres": "Şimdiki zaman",
    "Prog2": "Şimdiki zaman", "Fut": "Gelecek zaman", "Aor": "Geniş zaman", "Ly": "Pekiştirme eki",
    "Num": "Sayı", "With": "Olumluluk eki", "Without": "Olumsuzluk eki", "Adj": "Sıfat",
    "Adv": "Zarf", "Agt": "Özne", "Become": "Dönüşme eki", "Able": "Yeterlilik fiili",
    "Repeat": "Sürerlik fiili", "Almost": "Yaklaşma fiili", "Hastily": "Tezlik fiili",
    "A1sg": "1. Tekil Şahıs", "A2sg": "2. Tekil Şahıs", "A3sg": "3. Tekil Şahıs",
    "A1pl": "1. Çoğul Şahıs", "A2pl": "2. Çoğul Şahıs", "A3pl": "3. Çoğul Şahıs",
    "P1sg": "İyelik eki", "P1pl": "İyelik eki", "Nom": "Yalın hâl", "Acc": "Belirtme hâli",
    "Dat": "Yönelme hâli", "Loc": "Bulunma hâli", "Abl": "Ayrılma hâli", "Gen": "Tamlayan hâli",
    "Ins": "Araç hâli", "Cop": "İsim-fiil eki", "Caus": "Ettirgenlik", "Pass": "Edilgenlik",
    "Nec": "Gereklilik kipi", "Desr": "İstek kipi", "Cond": "Dilek kipi", "Imp": "Emir Kipi",
    "Prog1": "Şimdiki zaman eki", "PastPart": "Sıfat-fiil (mişli geçmiş)", "Neg": "Olumsuzluk",
    "Pos": "Olumlu"
}

def translateTable(ek_listesi):
    return [TranslateData.get(ek, ek) for ek in ek_listesi]

def getMeaningAndExample(kelime):
    url = f"https://sozluk.gov.tr/gts?ara={kelime}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
    except Exception:
        return "Anlam alınamadı.", "Örnek alınamadı."

    anlam = "Anlam bulunamadı."
    ornek = "Örnek bulunamadı."
    try:
        if data and "anlamlarListe" in data[0]:
            anlam = data[0]["anlamlarListe"][0]["anlam"]
            if "orneklerListe" in data[0]["anlamlarListe"][0]:
                ornek = data[0]["anlamlarListe"][0]["orneklerListe"][0]["ornek"]
    except Exception:
        pass

    return anlam, ornek

def analize(kelime):
    if kelime in cache:
        return cache[kelime]
    result = analyzer.analyze(kelime)
    if not result or not result[0]:
        return None
    result = result[0][0]
    cache[kelime] = result
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    sonuc = None
    kelime = ""
    anlam = ""
    ornek = ""
    translate_list = []

    if request.method == "POST":
        kelime = request.form["kelime"]
        sonuc = analize(kelime)
        if sonuc:
            anlam, ornek = getMeaningAndExample(sonuc.lemma)
            translate_list = translateTable(sonuc.analysis)  # Burada analiz edilen ekleri çeviriyoruz

    return render_template(
        "index.html",
        sonuc=sonuc,
        kelime=kelime,
        anlam=anlam,
        ornek=ornek,
        TranslateData=TranslateData,
        translateTable=translate_list
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ya da local port
    app.run(host="0.0.0.0", port=port)

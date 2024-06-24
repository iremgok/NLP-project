import customtkinter as ctk # type: ignore
import tkinter as tk
from tkinter import Text
import string
import os
from nltk.tokenize import word_tokenize, sent_tokenize # type: ignore
from nltk.probability import FreqDist # type: ignore
from nltk.corpus import stopwords # type: ignore
from nltk.sentiment import SentimentIntensityAnalyzer # type: ignore
from collections import Counter


class Metin:
    @staticmethod
    def ana_tema_cumlesi_bul(dosya_adi):
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as file:
                text = file.read().lower()  # Metni oku ve küçük harfe dönüştür
        except FileNotFoundError:
            print("Dosya bulunamadı.")
            return None

        # Metinden noktalama işaretlerini kaldır
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize metodu ile metni kelimelere ayır
        kelimeler = word_tokenize(text)

        # Stop words'leri yükle
        stop_words = set(stopwords.words('english'))

        # Stop words'ler hariç kelimeleri filtrele
        kelimeler = [kelime for kelime in kelimeler if kelime not in stop_words]

        # Kelimelerin frekansını say
        kelime_sayilari = Counter(kelimeler)

        # En sık geçen 3 kelimeyi bul
        en_cok_gecen_kelimeler = kelime_sayilari.most_common(3)

        # Ana tema cümlesini oluştur
        ana_tema_cumlesi = []
        for kelime, frekans in en_cok_gecen_kelimeler:
            # Her kelimenin içinde geçtiği ilk cümleyi bul
            for cumle in sent_tokenize(text):
                if kelime in word_tokenize(cumle):
                    ana_tema_cumlesi.append(cumle.strip())
                    break

        # Daha kısa bir şekilde döndür
        return " ".join(ana_tema_cumlesi[:3])

    @staticmethod
    def metin_ozetle(dosya_adi):
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print("Dosya bulunamadı.")
            return None
        
        sentences = sent_tokenize(text)
        ozet = ' '.join(sentences[:2])
        return ozet

    @staticmethod
    def metin_istatistik(dosya_adi):
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print("Dosya bulunamadı.")
            return None
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        token = word_tokenize(text)
        sentences = sent_tokenize(text)
        letter_count = sum(1 for char in text if char in string.ascii_letters)

        stop_words = set(stopwords.words("english"))
        kelimeler = [word.lower() for word in token if word.lower() not in stop_words]
        fd = FreqDist(kelimeler)
        en_cok_gecen_kelimeler = fd.most_common(10)
        en_az_gecen_kelimeler = fd.most_common()[-10:]

        stopwords_in_text = [word for word in token if word.lower() in stop_words]
        fd_stopwords = FreqDist(stopwords_in_text)
        total_stopwords = sum(fd_stopwords.values())

        return token, sentences, letter_count, en_cok_gecen_kelimeler, en_az_gecen_kelimeler, total_stopwords
    
    @staticmethod
    def metin_benzerlik(text1, text2):
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    @staticmethod
    def kelime_filtreleme(text, kelime):
        bulunanlar = []
        baslangic_konum = '1.0'
        while True:
            baslangic_konum = text.find(kelime, baslangic_konum)
            if baslangic_konum == -1:
                break
            son_konum = f"{baslangic_konum}+{len(kelime)}c"
            bulunanlar.append((baslangic_konum, son_konum))
            baslangic_konum = son_konum
        return bulunanlar
    
    @staticmethod
    def duygu_analizi(dosya_adi):
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print("Dosya bulunamadı.")
            return None

        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
        return sentiment_scores


class Arayuz:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("750x650+500+120")
        ctk.set_appearance_mode("dark")
        self.metin = Metin()

        self.frame = ctk.CTkFrame(master=self.app, width=750, height=650, corner_radius=10, fg_color="black")
        self.frame.pack(padx=50, pady=50)

        self.label = ctk.CTkLabel(master=self.frame, text="NLP GİRİŞ EKRANI", width=300, height=25,
                                  font=("Bold Arial", 16), fg_color="black", text_color="green")
        self.label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.label1 = ctk.CTkLabel(master=self.frame, text=".txt Dosyasının Adını Giriniz", width=300, height=25,
                                   font=("Arial", 14), fg_color="black", text_color="green")
        self.label1.place(relx=0.2, rely=0.2, anchor=tk.CENTER)

        self.entry1 = ctk.CTkEntry(master=self.frame, width=150)
        self.entry1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.button1 = ctk.CTkButton(master=self.frame, text="Metin Ekle", command=self.ekle_button)
        self.button1.place(relx=0.2, rely=0.3, anchor=tk.CENTER)

        self.button2 = ctk.CTkButton(master=self.frame, text="Sil", command=self.sil_button)
        self.button2.place(relx=0.45, rely=0.3, anchor=tk.CENTER)

        self.button3 = ctk.CTkButton(master=self.frame, text="Güncelle", command=self.guncelle_button)
        self.button3.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

        self.button4 = ctk.CTkButton(master=self.frame, text="Ana Tema Bul", command=self.ana_tema_button)
        self.button4.place(relx=0.2, rely=0.4, anchor=tk.CENTER)

        self.button5 = ctk.CTkButton(master=self.frame, text="Metin Özetle", command=self.metin_ozetle_button)
        self.button5.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        self.button6 = ctk.CTkButton(master=self.frame, text="Duygu Analizi", command=self.duygu_analiz_button)
        self.button6.place(relx=0.2, rely=0.5, anchor=tk.CENTER)

        self.button7 = ctk.CTkButton(master=self.frame, text="Metin İstatistikleri", command=self.metin_istatistik_button)
        self.button7.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

        self.label2 = ctk.CTkLabel(master=self.frame, text="İkinci .txt Dosyasının Adını Giriniz", width=300, height=25,
                                   font=("Arial", 14), fg_color="black", text_color="green")
        self.label2.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

        self.entry2 = ctk.CTkEntry(master=self.frame, width=150)
        self.entry2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.button8 = ctk.CTkButton(master=self.frame, text="Metin Benzerliği", command=self.metin_benzerlik_button)
        self.button8.place(relx=0.5, rely=0.68, anchor=tk.CENTER)

        self.label_kelime = ctk.CTkLabel(master=self.frame, text="Aranacak Kelime:", width=300, height=25,
                                         font=("Arial", 14), fg_color="black", text_color="green")
        self.label_kelime.place(relx=0.2, rely=0.85, anchor=tk.CENTER)

        self.entry_kelime = ctk.CTkEntry(master=self.frame, width=150)
        self.entry_kelime.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.button9 = ctk.CTkButton(master=self.frame, text="Kelime Filtreleme", command=self.kelimeyi_bul)
        self.button9.place(relx=0.2, rely=0.75, anchor=tk.CENTER)

        self.text_widget = Text(self.app, wrap=tk.WORD, height=10, width=30)
        self.text_widget.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.entry_kelime = tk.Entry(self.app, width=30)
        self.entry_kelime.place(relx=0.2, rely=0.86, anchor=tk.CENTER)


        self.app.mainloop()

    def ekle_button(self):
        dosya_adi = self.entry1.get()
        if os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyasi mevcut.")
        else:
            try:
                with open(dosya_adi, "x") as f1:
                    self.label13 = ctk.CTkLabel(master=self.frame, text="Dosyaya eklemek istediğiniz içeriği giriniz: ", width=300, height=25,
                                       font=("Arial", 14), fg_color="black", text_color="green")
                    self.label13.place(relx=0.2, rely=0.9, anchor=tk.CENTER)

                    self.entry3 = ctk.CTkEntry(master=self.frame, width=150)
                    self.entry3.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
                    f1.write(self.entry3.get())
                    print(f"{dosya_adi} dosyasi basariyla eklendi.")
            except FileExistsError:
                print(f"{dosya_adi} dosyasi mevcut.")

    def sil_button(self):
        dosya_adi = self.entry1.get()
        if os.path.exists(dosya_adi):
            os.remove(dosya_adi)
            print(f"{dosya_adi} dosyasi basariyla silindi.")
        else:
            print(f"{dosya_adi} dosyasi bulunamadi.")

    def dosya_guncelle(self):
        dosya_adi = self.entry1.get()
        yeni_icerik = self.entry4.get()
        with open(dosya_adi, "a") as f3:
            f3.write("\n" + yeni_icerik)
        print(f"{dosya_adi} dosyası başarıyla güncellendi.")

    def guncelle_button(self):
        dosya_adi = self.entry1.get()
        if os.path.exists(dosya_adi):
            self.label22 = ctk.CTkLabel(master=self.frame, text="Dosyanın yeni içeriğini giriniz", width=300, height=25,
                               font=("Arial", 14), fg_color="black", text_color="green")
            self.label22.place(relx=0.2, rely=0.9, anchor=tk.CENTER)
            self.entry4 = ctk.CTkEntry(master=self.frame, width=150)
            self.entry4.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
            self.button11 = ctk.CTkButton(master=self.frame, text="Güncelle", command=self.dosya_guncelle)
            self.button11.place(relx=0.8, rely=0.9, anchor=tk.CENTER)
        else:
            print(f"{dosya_adi} dosyasi bulunamadi.")

    def ana_tema_button(self):
        dosya_adi = self.entry1.get()
        ana_tema = self.metin.ana_tema_cumlesi_bul(dosya_adi)
        if ana_tema:
            self.show_result_window(ana_tema, "Ana Tema")

    def metin_ozetle_button(self):
        dosya_adi = self.entry1.get()
        ozet = self.metin.metin_ozetle(dosya_adi)
        self.show_result_window(ozet, "Metin Özeti")

    def metin_istatistik_button(self):
        dosya_adi = self.entry1.get()
        result = self.metin.metin_istatistik(dosya_adi)
        if result:
            token, sentences, letter_count, en_cok_gecen_kelimeler, en_az_gecen_kelimeler, total_stopwords = result
            content = (
                f"Toplam Kelime Sayısı: {len(token)}\n"
                f"Toplam Cümle Sayısı: {len(sentences)}\n"
                f"Toplam Harf Sayısı: {letter_count}\n\n"
                f"En Çok Geçen Kelimeler:\n{en_cok_gecen_kelimeler}\n\n"
                f"En Az Geçen Kelimeler:\n{en_az_gecen_kelimeler}\n\n"
                f"Toplam Stop Words Sayısı: {total_stopwords}\n"
            )
            self.show_result_window(content, "Metin İstatistikleri")
        else:
            self.show_result_window("Dosya bulunamadı veya istatistik hesaplanamadı.", "Hata")

    def metin_benzerlik_button(self):
        dosya1 = self.entry1.get()
        dosya2 = self.entry2.get()
        try:
            with open(dosya1, 'r', encoding='utf-8') as file1:
                text1 = file1.read()
            with open(dosya2, 'r', encoding='utf-8') as file2:
                text2 = file2.read()
        except FileNotFoundError:
            print("Dosya bulunamadı.")
            return
        benzerlik_orani = self.metin.metin_benzerlik(text1, text2)
        self.show_result_window(f"Benzerlik Oranı: {benzerlik_orani:.2f}", "Metin Benzerlik Oranı")

    def kelimeyi_bul(self):
        kelime = self.entry_kelime.get()
        text = self.text_widget.get("1.0", "end-1c")
        self.text_widget.tag_remove('bulunan', '1.0', tk.END)
        
        if kelime:
            bulunanlar = self.metin.kelime_filtreleme(text, kelime)
            if bulunanlar:
                for baslangic_konum, son_konum in bulunanlar:
                    self.text_widget.tag_add('bulunan', baslangic_konum, son_konum)
                    self.text_widget.tag_config('bulunan', background="yellow")
            else:
                print(f"'{kelime}' kelimesi metinde bulunamadı.")
        else:
            print("Lütfen bir kelime girin.")

    def duygu_analiz_button(self):
        dosya_adi = self.entry1.get()
        sentiment_scores = self.metin.duygu_analizi(dosya_adi)
        if sentiment_scores:
            self.show_result_window(f"Duygu Analizi Skorları: {sentiment_scores}", "Duygu Analizi")
        else:
            print("Dosya bulunamadı veya duygu analizi yapılamadı.")

    def show_result_window(self, content, title="Sonuçlar"):
        result_window = tk.Toplevel(self.app)
        result_window.title(title)
        result_window.geometry("400x300")
        result_label = ctk.CTkLabel(result_window, text=content, text_color = "black", wraplength=350)
        result_label.pack(pady=20)

if __name__ == "__main__":
    arayuz = Arayuz()
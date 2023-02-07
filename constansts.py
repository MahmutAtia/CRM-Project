from datetime import datetime,timedelta
columns_1 = ['index','FİRMA ADI', 'ÜLKE','TELEFON NUMARASI', 'E-POSTA', 'FİRMA YETKLİSİ', 'WEB SİTESİ']
columns_2 = ['index', 'İRTİBAT ŞEKLİ', 'KAÇINCI İRTİBAT', 'İRTİBAT TARİHİ ', 'İRTİBAT PUANI', 'DK', 'İRTİBAT SONUCU' ]
with open("texts/countries.txt", "r", encoding="utf8") as f:
        countries = [i.strip() for i in f.readlines()]

with open("texts/contacts.txt", "r", encoding="utf8") as f:
        contacts = [i.strip() for i in f.readlines()]

with open("texts/results.txt", "r", encoding="utf8") as f:
        results = [i.strip() for i in f.readlines()]

today = datetime.now().date()
dates = [str(today-timedelta(days=i)) for i in range(5)]

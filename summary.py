import gspread
import pandas as pd
import string
import numpy as np
from datetime import datetime


class summary:
    def __init__(self,user, yeni, day):
        self.yeni = yeni
        self.day = datetime.now().strftime("%Y-%m-%d") if day == "today" else day
        self.user = user
        self.df, self.df_offer = self._read()
        self.rewrite_all_dates()
        self.person = self.person()

    def _set_work_sheet(self):
        sa = gspread.service_account()
        if self.user == "ma":
            sh = sa.open("(MA) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
        elif self.user == "amir":
            sh = sa.open("(MOUSTAPHA) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
        elif self.user == "ali":
            sh = sa.open("(AL) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
        return sh.worksheet("ARAMA LİSTELERİ V.2"), sh.worksheet("VERİLEN TEKLİFLER1")
    def _read(self):
        sh1,sh2 = self._set_work_sheet()
        df = pd.DataFrame(sh1.get_all_values())
        df.columns = df.iloc[1]
        df2 = pd.DataFrame(sh2.get_all_values())
        return df,df2
    def company_count(self):
        li = []
        for i in self.df.columns:
            if i.startswith("İRTİBAT TARİHİ"):
                company_count = self.df['FİRMA ADI'][self.df[i] == self.day]
                li.append(company_count)
        return pd.concat(li).count()

    def person(self):
        if self.df["EKLEYEN"][3].strip() == "MA":
            person = "MAHMOUD ATiA"
        elif self.df["EKLEYEN"][3].strip() == "AMIR":
            person = "Amir"
        else:
            person = "ALi ABDULRAZZAQ"
        return person

    def _rewrite_date(self, series):
        return ((series[1:]).dropna()).apply(lambda x: str(x).split(" ")[0])

    def rewrite_all_dates(self):
        for i in self.df.columns:
            if i.startswith("İRTİBAT TARİHİ"):
                self.df[i] = self.df[i].apply(lambda x: str(x).split(" ")[0])

    def _country_count(self):
        li = []
        for i in self.df.columns:
            if i.startswith("İRTİBAT TARİHİ"):
                country_count = self.df['ÜLKE'][self.df[i] == self.day]
                li.append(country_count)
        return pd.concat(li).value_counts()

    def write_countries(self):
        country = pd.DataFrame(self._country_count())
        text = ""
        for count in country.itertuples():
            text += ("   " + count[0] + " : " + str(count[1]))
        return text

    def _methods_count(self, method):
        li = [0, 0, 0, 0]
        for i in method.itertuples():
            if i[1] == 'ARAMA':
                li[0] += 1
            elif i[1] == 'WHATSAPP':
                li[1] += 1
            elif i[1] == 'E-POSTA':
                li[2] += 1
            elif i[1] == 'DİĞER':
                li[3] += 1
        return li

    def contact_method(self):
        li_date = [i  for i in self.df.columns if i.startswith("İRTİBAT TARİHİ")]
        li_methods = [i for i in self.df.columns if i.startswith("İRTİBAT ŞEKLİ")]

        li = []
        for i in range(len(li_methods)):
            method = pd.DataFrame(self.df[li_methods[i]].loc[(self.df[li_date[i]] == self.day)])
            li.append(method)
        methods_count_list = pd.Series(li).apply(lambda x: np.array(self._methods_count(x))).sum()
        return methods_count_list

    def _contact_times_count(self, series):
        abc = string.ascii_letters + " "
        series = series.iloc[:, 0].apply(lambda x: 0 if str(x) in abc else int(x))
        contact12 = (series <= 2).sum()
        contact32 = ((series == 3) | (series == 4)).sum()
        contact4 = (series > 4).sum()
        return [contact12, contact32, contact4]

    def times_count(self):
        li_date = [i for i in self.df.columns if i.startswith("İRTİBAT TARİHİ")]
        li_times = [i for i in self.df.columns if i.startswith('KAÇINCI İRTİBA')]

        li = []
        for i in range(len(li_times)):
            time = pd.DataFrame(self.df[li_times[i]].loc[(self.df[li_date[i]] == self.day)])
            li.append(time.dropna())
        times_count = pd.Series(li).apply(lambda x: np.array(self._contact_times_count(x))).sum()
        return times_count

    def _result_cat(self, series):
        arama_katalog = ((series == "HATIRLATMA VE SORUYA CEVAP VERME") | (series == "KATALOG WP ") | (
                    series == "KATALOG EMİAL") | (series == "KATALOG DİĞER") | (series == "ŞİMDİLİK OLMUYOR") | (
                                     series == "İLGİLENMİYOR") | (series == "SONRA ARA") | (
                                     series == "FIYAT YÜKSEK") | (series == "İTHALAT YAPAMAZ")).sum()
        cevap_olmayip_mesaj = ((series == "CEVAP YOK  WP") | (series == "CEVAP YOK  EMAIL") | (
                    series == "CEVAP YOK KATALOG  WP")).sum()
        proje_ve_z = ((series == "PROJE BEKLENİYOR") | (series == "ZIYARETE GELEBİLİR")).sum()
        cevapsiz = (series == "CEVAP YOK").sum()
        return [arama_katalog, cevap_olmayip_mesaj, proje_ve_z, cevapsiz]

    def result(self):
        li_date = [i for i in self.df.columns if i.startswith("İRTİBAT TARİHİ")]
        li_result = [i for i in self.df.columns if i.startswith("İRTİBAT SONUCU")]

        li = []
        for i in range(len(li_result)):
            result = pd.DataFrame(self.df[li_result[i]].loc[(self.df[li_date[i]] == self.day)])
            li.append(result)

        result_count_list = pd.Series(li).apply(lambda x: np.array(self._result_cat(x))).sum()
        return result_count_list

    def qoute(self):
        self.df_offer['date'] = self._rewrite_date(self.df_offer["VERİLEN TEKLİFLER"])
        return (self.df_offer['date'] == self.day).sum()

    def summary_report(self):
        contact = self.contact_method()
        result = self.result()
        times = self.times_count()

        return (f"""
    Bugün Özeti:
    {self.person}
    Tarih : {self.day}
    Toplam Firma : {self.company_count()}
    Yeni Eklenen : {self.yeni}
    Ülkeler:
    {
        self.write_countries()
        }
    ---------------------------------
    Arama : {contact[0]}
    WP : {contact[1]}
    Email : {contact[2]}
    Diğer : {contact[3]}
    ---------------------------------
    Arama Katalog : {int(result[0][0])}
    Cevap olmayıp Katalog : {int(result[1][0])}
    Proje Ziyaret bekleniyor : {int(result[2][0])}
    Cevapsız :{int(result[3][0])}
    ---------------------------------
    1. ve 2. Irtibat : {int(times[0])}
    3. ve 4. Irtibat : {int(times[1])}
    4ten fazla. Irtibat :{int(times[2])}
    ---------------------------------
    """

              )
S = summary("ma", 51, "today")
print(S.df_offer)
print(S.summary_report())
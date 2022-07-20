import requests
from bs4 import BeautifulSoup
import pandas as pd



# Hedeflenen linke erişildi

link = "https://www.bkmkitap.com/korku-ve-gerilim-edebiyati"

href = requests.get(link).content

soup = BeautifulSoup(href, "lxml")





# Kitapların isimleri, yayınevleri, fiyatların indirim öncesi/sonrası ve indirim yüzdesi için ayrı birer 
# liste oluşturulup aktarıldı 


kitaplist ,yayinevilist,yazarlist,fiyatlist,ilkfiyatlist,yuzdeindirim = [],[],[],[],[],[]


kitap = soup.find_all("a",{"class":"fl col-12 text-description detailLink"})
for i in kitap:
    kitaplist.append(i.text.strip('\n'))

yayinevi = soup.find_all("a",{"class":"col col-12 text-title mt"})
for i in yayinevi:
    yayinevilist.append(i.text)

yazar = soup.find_all("a",{"class":"fl col-12 text-title"})
for i in yazar:
    yazarlist.append(i.text)

fiyat = soup.find_all("div",{"class":"col col-12 currentPrice"})
for i in fiyat:
    fiyatlist.append(i.text.strip('\nTL').replace(',','.'))


ilkliste1 = []
ilkfiyat = soup.find_all("div",{"class":"text-line discountedPrice"})
for i in ilkfiyat:
    i = i.text
    ilkliste1.append(i.strip('\n').replace(',','.'))
ilkfiyatlist = []
for j in ilkliste1:
    ilkfiyatlist.append(j[0:5])



indirim = soup.find_all("span",{"class":"col fr passive productDiscount"})
for i in indirim:
    yuzdeindirim.append(i.text.strip('\n%'))






# Pandas aracılığı ile veriler dataframe haline getirildi

data_list = list(zip(kitaplist,yayinevilist,yazarlist,fiyatlist,ilkfiyatlist,yuzdeindirim))
df = pd.DataFrame(data_list,columns=["kitap_adi","yayin_evi","yazar_adi","fiyat","ilkfiyat","yüzdeindirim"])
df['fiyat'] = df['fiyat'].astype(float)
df['ilkfiyat'] = df['ilkfiyat'].astype(float)
df['yüzdeindirim'] = df['yüzdeindirim'].astype(float)
df['yüzdeindirim'] = df['yüzdeindirim'] / 100


print(df.head())




# Oluşturulan dataframe ile excel dosyası oluşturuldu

df.to_excel("bkmdata.xlsx", encoding='utf-8', index=False)
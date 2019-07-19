import json
import urllib.request
from bs4 import BeautifulSoup
import urllib

url = "https://www.franke.com/tr/tr/ks/products/{}/{}/{}_detail.html"

class Urun:
    def __init__(self,bilgi,fiyat,iskonto_fiyat,resim,baslik,urunkodu,seokodu):
        self.bilgi = bilgi
        self.fiyat = fiyat
        self.iskonto_fiyat = int(iskonto_fiyat)
        self.baslik = baslik
        self.resim = resim
        self.urunkodu = urunkodu
        self.seokodu = seokodu



def handleUrun(kategori,baslik,urunkodu,iskonto):
    url_kod = urunkodu.replace(".","-")
    url_baslik = baslik.replace(" ","-")
    new_url = url.format(kategori,url_baslik,url_kod)
    html_str = handleHtml(new_url)
    urun = handleString(html_str,iskonto,urunkodu)
    print(urun.baslik, end="")
    print(urun.iskonto_fiyat)
    print("Urun kodu : {}".format(urun.urunkodu))
    downloadResim(urun)
    return urun


def handleHtml(url):
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return mystr
    except:
        print("URL BULUNAMADI : {}".format(url))

def handleString(html_str,iskonto,urunkodu):
    parsed_html = BeautifulSoup(html_str,"html.parser")
    #print(parsed_html.body.find('div', attrs={'id':'productDetailWithTablesId_1-panel0'}).text)
    urun_bilgi = parsed_html.body.find('div', attrs={'id':'productDetailWithTablesId_1-panel0'}).text.replace('\n\n','')
    temp_fiyat = parsed_html.body.find('div', attrs={'id':'productDetailWithTablesId_1-panel1'}).text
    #temp_resim = parsed_html.body.find('img' attrs={'class':'m19-product-picture-with-options-module__owl__item__img'})
    inputTag = parsed_html.find(attrs={'class':'m19-product-picture-with-options-module__owl__item__img'})
    urun_resim = inputTag['src']
    urun_fiyat = int(temp_fiyat.split('Perakende KDV dahil satış fiyatı')[1].replace(' ','').replace('\n','').replace('₺','').split(',')[0].replace('.',''))
    #print('fiyat : {}'.format(urun_fiyat))
    urun_baslik = parsed_html.body.find('div', attrs={'class':'small-12 medium-10 large-8 medium-centered columns'}).text
    urun = Urun(urun_bilgi,urun_fiyat,urun_fiyat * iskonto,urun_resim,urun_baslik,urunkodu,urun_baslik.replace(' ','-'))
    return urun

def downloadResim(urun):
    f = open("resimler/{}.jpg".format(urun.urunkodu),'wb')
    f.write(urllib.request.urlopen(urun.resim).read())
    f.close()



with open('urunler.json') as json_file:
    data = json.load(json_file)
    urunler = []
    for p in data['Urunler']:
        urun = handleUrun(p['Kategori'],p['Baslik'],p['UrunKodu'],p['Iskonto'])
        urunler.append(urun)
        with open("ciktilar.txt", "a") as text_file:
            text_file.write('##################### URUN BASLANGICI ######################### ')
            text_file.write("\n")
            text_file.write("Baslik: FRANKE - {}".format(urun.baslik))
            text_file.write('\n\n')
            text_file.write("Bilgi: {}".format(urun.bilgi))
            text_file.write('\n\n')
            text_file.write("Liste Fiyatı: {}".format(urun.fiyat))
            text_file.write('\n\n')
            text_file.write("Iskontolu Fiyat: {}".format(urun.iskonto_fiyat))
            text_file.write('\n\n')
            text_file.write("Urun Kodu: {}".format(urun.urunkodu))
            text_file.write('\n\n')
            text_file.write("Seo Linki: {}".format(urun.seokodu))
            text_file.write('\n ##################### URUN BITISI ######################### ')




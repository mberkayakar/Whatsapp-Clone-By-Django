import datetime
def urunekle(dictionary):
  adı = input("Ürün Adı")
  stok = input("Ürün stok")
  tarihyıl = int(input("Ürün tarihyıl"))
  tarihay = int(input("Ürün tarihay"))
  tarihgün = int(input("Ürün tarihgün"))
  dictionary[str(adı)]= {'adı':adı,'stok':stok,'tarih':datetime.date(tarihyıl,tarihay,tarihgün)}
try:
  dosya = open("person2.json","r")
  dosyavarmı=True
  for item in dosya:
      dictionary = item
  urunekle(dictionary)
  print(dictionary,file=dosya)
except:
  dosyavarmı=False
  dosya = open("person2.json","w")
  dictionary = {}
  urunekle(dictionary)
  print(dictionary,file=dosya)
print(dosyavarmı)

# Sahte Ödeme Sistemi
Bu proje, Python ile geliştirilmiş basit bir **sahte ödeme sistemi** uygulamasıdır. Bir GUI (Tkinter) arayüzü üzerinden kullanıcıdan kart bilgileri alınır ve Flask tabanlı sahte bir API ile ödeme işlemi simüle edilir.

## Özellikler
- **Flask API**:
  - Kart, son kullanma tarihi (SKT), CVC ve tutar alanlarını alır.
  - Gerekli alanlar mevcutsa sahte ödeme onayı verir.
  - Eksik veya hatalı veri varsa 400 hatası döner.
- **GUI Arayüz (Tkinter)**:
  - Kart numarası kontrolü: `XXXX-XXXX-XXXX-XXXX` formatında girilmesi sağlanır.
  - SKT kontrolü ve geçerlilik kontrolü.
  - CVC kontrolü.
  - Tutar otomatik hesaplanır.
  - Ürünler:
    - Adet arttırma/azaltma.
    - Otomatik toplam tutar güncellemesi.
  - Basit ve kullanıcı dostu bir arayüz.
- **Arka Plan İşlemleri**:
  - Flask API'ye istek gönderir, dönen yanıtı GUI'de gösterir.
- **Eğitim Amaçlı Kullanım**:
  - Veri doğrulama örnekleri içerir.
  - Temel yazılım geliştirme becerileri kazandırır.
- GUI
- Kart numarasının `XXXX-XXXX-XXXX-XXXX`şeklinde kontrolü
- SKT kontrolü ve geçerlilik tarih kontrolü
- CVC kontrolü
- Tutar kontrolü
- Ürünler, ürün ekleme, adet arttırma, adet azaltma, otomatik toplama
- Arka planda sunucuya istek gönderip yanıt alma
- Kullanımı kolay basit bir arayüz
- Kulalnıcı deneyimini ve veri doğrulamasını kapsıyor
  
## Öğrenme Katkısı
- Flask ile REST API geliştirme
- JSON veri alışverişi (frontend ↔ backend)
- Tkinter ile GUI geliştirme
- `requests` modülü ile HTTP POST işlemleri
- Kullanıcı girdilerinde veri doğrulama
- Fonksiyonel yapılarla modüler kod yazımı
  
## Gereksinimler
- Python 3.x
- `Flask`
- `requests` kütüphanesi
   
## Uygulamayı Çalıştırma
1. Terminalde `python fake_api.py` komutunu girerek API'yi başlatın
2. Ardından GUI arayüzünü başlatın `python odeme_gui.py`

### NOT
Bu proje gerçek bir ödeme altyapısı değildir. Eğitim ve simülasyon amaçlı geliştirilmiştir. Kart bilgilerinizi asla gerçek şekilde kullanmayınız.

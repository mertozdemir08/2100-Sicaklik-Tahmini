# 2100-Sicaklik-Tahmini
Bu proje, ülkelerin demografik ve çevresel özelliklerini kullanarak 2100 yılı için ortalama küresel sıcaklık artışını tahmin etmeyi hedeflemektedir. Ridge regresyon modeli ve IPCC (Hükümetlerarası İklim Değişikliği Paneli) iklim riski eşiklerine dayanarak ülkeler risk seviyelerine göre sınıflandırılmakta ve iklim değişikliğine karşı kırılganlıkları değerlendirilmektedir.

Amaç
1980–2013 yılları arasındaki geçmiş verileri kullanarak 2100 yılında her bir ülke için ortalama sıcaklık artışını tahmin etmek ve IPCC’ye dayalı dört risk kategorisine göre ülkeleri sınıflandırmak:

Düşük Risk (0–1°C)

Orta Risk (1–1.5°C)

Yüksek Risk (1.5–2°C)

Çok Yüksek Risk (>2°C)

Yöntemler
Model: Polinom özellikli Ridge regresyon (derece = 1)

Kullanılan Değişkenler: Yıl, ortalama sıcaklık, nüfus, nüfus yoğunluğu, MtCO₂ emisyonları, diazot monoksit (N₂O) emisyonları, kıta bilgisi

Veri Aralığı: 1980–2013 (Sanayi sonrası ısınma trendleri ve veri seti kesişimi nedeniyle)

Modelleme: Yeterli tarihsel veriye sahip ülkeler için bireysel modelleme uygulanmıştır

Tahmin Karşılaştırması: 2013 yılı sıcaklık değerleriyle karşılaştırılarak risk skorları hesaplanmıştır

Risk Sınıflandırma Mantığı
Eşik değerler IPCC’nin 2018 ve 2023 raporlarına dayanmakta ve NASA ile UNEP (Birleşmiş Milletler Çevre Programı) tarafından desteklenmektedir:

1.5°C: Geri dönüşü olmayan etkilerin başlangıcı olarak kabul edilir

2°C ve üzeri: Özellikle kırılgan bölgeler için son derece tehlikeli kabul edilir

Kullanılan Araçlar ve Teknolojiler
Python (pandas, scikit-learn)

Ridge regresyon modelleme

Veri işleme ve dönüştürme için pipeline (işlem zinciri) yapıları

Excel üzerinden tahmin sonuçlarının ve risk seviyelerinin raporlanması

Çıktılar
Oluşturulan Excel dosyasında şu bilgiler yer almaktadır:

Ülke bazında 2100 yılı sıcaklık tahminleri

Her ülke için belirlenen risk seviyesi

Risk seviyelerine göre ülke sayısını gösteren özet tablo

Önerilen Çözüm Önerileri (Sonuçlara Dayalı)
Kıtalar bazında şu odak alanlarında tavsiyeler geliştirilmiştir:

Afrika ve Asya: Su yönetimi ve tarımsal adaptasyon

Avrupa ve Güney Amerika: Kentsel planlama ve emisyon azaltımı

Genel: Yenilenebilir enerji yatırımları ve erken uyarı sistemlerinin kurulması


# CyberAgent Sunum Oluşturma Sistemi

Bu proje, siber güvenlik eğitim materyalleri için otomatik PowerPoint sunumu oluşturan bir sistemdir.

## 📁 Proje Yapısı

### Ana Dosyalar
- `slide_generator_menu.py`: Ana menü arayüzü
- `gemini_content_generator.py`: İçerik üretimi için Gemini AI entegrasyonu
- `slide_generator.py`: PowerPoint slayt oluşturma motoru
- `deneme.py`: Test ve geliştirme amaçlı alternatif slayt oluşturucu

### Şablon Yönetimi
- `template_manager.py`: PowerPoint şablon yönetimi
- `template_config.py`: Şablon yapılandırma ayarları
- `analyze_template.py`: Şablon analiz araçları
- `template_analysis.json`: Şablon analiz sonuçları

### Diğer Dosyalar
- `requirements.txt`: Gerekli Python paketleri
- `.env`: API anahtarları ve yapılandırma
- `template.pptx`: Ana PowerPoint şablonu

## 🔧 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını oluşturun ve Gemini API anahtarınızı ekleyin:
```
Gemini_API_KEY=your_api_key_here
```

## 📚 Kod Açıklamaları

### slide_generator_menu.py
Ana menü arayüzünü içerir. Kullanıcıya modül ve ders seçenekleri sunar.

Önemli Sınıflar:
- `PresentationManager`: Sunum oluşturma sürecini yönetir
  - Yedekleme
  - Dosya adlandırma
  - Hata yönetimi

### gemini_content_generator.py
Gemini AI kullanarak içerik üretimini sağlar.

Önemli Sınıflar:
- `GeminiContentGenerator`: AI tabanlı içerik üretimi
  - Ders planı oluşturma
  - Slayt içeriği üretme
  - JSON şema doğrulama

### slide_generator.py
PowerPoint sunumlarını oluşturan ana motor.

Önemli Özellikler:
- Şablon kullanımı
- Slayt düzenleri
- İçerik yerleştirme
- Biçimlendirme

### template_manager.py
Şablon yönetimi için araçlar.

Önemli Sınıflar:
- `TemplateMapping`: Şablon yapısını analiz eder
  - Yer tutucu (placeholder) haritalaması
  - Düzen tipleri
  - Şablon doğrulama

## 🎯 Kullanım Senaryoları

1. Yeni Sunum Oluşturma:
```python
python slide_generator_menu.py
```
- Modül seçin
- Ders seçin
- Sistem otomatik olarak sunumu oluşturacak

2. Şablon Analizi:
```python
python analyze_template.py
```
- Şablon yapısını analiz eder
- JSON formatında rapor oluşturur

## 📋 Modül Yapısı

Sistem şu modülleri içerir:
1. Veri Toplama (data_collection)
2. Veri Temizleme (data_cleaning)
3. Veri Analizi (data_analysis)
4. Veri Görselleştirme (data_visualization)
5. Uygulamalar (applications)

Her modül:
- Giriş dersi
- Temel kavramlar
- Pratik uygulamalar
- Değerlendirme içerir

## 🔄 Hata Yönetimi

Sistem şu hataları yönetir:
- API kota aşımı
- JSON ayrıştırma hataları
- Şablon uyumluluk sorunları
- Dosya işleme hataları

## 💾 Yedekleme Sistemi

- Her yeni sunum oluşturulduğunda otomatik yedekleme
- Zaman damgalı yedek dosyaları
- presentations/backups/ dizininde saklama

## 🛠 Teknik Detaylar

### Kullanılan Teknolojiler
- Python 3.10+
- python-pptx
- Google Gemini AI
- JSON şema doğrulama

### Bağımlılıklar
- python-pptx==0.6.22
- google-generativeai==0.3.2
- python-dotenv==1.0.1
- Pillow==9.5.0
- diğer bağımlılıklar requirements.txt'de

## ⚠️ Bilinen Sorunlar

1. Şablon Uyumluluk Sorunları:
   - Bazı yer tutucular bulunamayabilir
   - Çözüm: Otomatik metin kutusu oluşturma

2. API Kota Sınırlamaları:
   - Çözüm: Üstel geri çekilme ve yeniden deneme

## 🔜 Planlanan Özellikler

1. İçerik Önbellekleme
2. Çoklu Dil Desteği
3. Özel Şablon Oluşturma
4. İnteraktif İçerik Düzenleme

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 
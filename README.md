# 🎨 Görüntü İşleme Aracı (Image Processor GUI)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern%20UI-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Modern ve kullanıcı dostu bir görüntü işleme uygulaması**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Geliştirici](#-gelitirici)

</div>

## 📋 Hakkında

Görüntü İşleme Aracı, Python ve CustomTkinter kullanılarak geliştirilmiş modern bir masaüstü uygulamasıdır. Kullanıcıların görseller üzerinde çeşitli işlemler yapabilmesini sağlayan sezgisel ve güçlü bir arayüz sunar.

## ✨ Özellikler

### 🎯 Temel İşlevler
- **📁 Görsel Yükleme**: JPG, PNG, BMP, TIFF format desteği
- **🔍 Gerçek Zamanlı Önizleme**: İşlem öncesi/sonrası karşılaştırma
- **💾 Görsel İndirme**: İşlenmiş görselleri kaydetme

### 🎨 Görsel İşlemleri

#### 🔧 Ayarlanabilir Filtreler (Slider Kontrollü)
- **🔆 Parlaklık Ayarı**: -255 ile +255 arası hassas kontrol
- **⚡ Kontrast Ayarı**: 0.1 ile 3.0 arası dinamik ayar
- **🌈 Gamma Düzeltme**: 0.1 ile 3.0 arası gamma ayarı
- **🚀 Kalite Artırma**: 1.0 ile 5.0 arası keskinlik ve netlik

#### ⚡ Tek Tıklamalı İşlemler
- **🎭 Negatif Efekt**: Görsel negatifi oluşturma
- **🔄 Kontrast Germe**: Otomatik kontrast optimizasyonu
- **📈 Histogram Eşitleme**: Gelişmiş histogram dengeleme
- **📊 Histogram Görüntüleme**: Detaylı histogram analizi

### 🔍 Gelişmiş Özellikler
- **🔍 Zoom Modu**: Büyütülmüş inceleme (Sol/Sağ tık ile geçiş)
- **🔄 Geri Alma**: Orijinal görsele tek tıkla dönüş
- **🎯 Gerçek Zamanlı İşlem**: Slider değişiklikleri anında uygulanır
- **📱 Modern Arayüz**: Koyu tema ve sezgisel tasarım

## 🛠️ Teknoloji Stack'i

- **Python 3.8+** - Temel programlama dili
- **CustomTkinter** - Modern GUI framework'ü
- **PIL (Pillow)** - Görsel işleme kütüphanesi
- **NumPy** - Matematiksel işlemler
- **Matplotlib** - Histogram görselleştirme

## 📦 Kurulum

### 1. Gereksinimler
```bash
# Python 3.8 veya üzeri gereklidir
python --version

import numpy as np
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk


class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.processed_image = None

    def load_image(self, image_path):
        """Görseli yükler ve NumPy array'e çevirir"""
        try:
            pil_image = Image.open(image_path)

            # PNG'lerde alpha kanalını kaldır (RGBA -> RGB)
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')
            elif pil_image.mode == 'LA':
                pil_image = pil_image.convert('L')

            self.original_image = pil_image.copy()
            self.current_image = np.array(pil_image)
            self.processed_image = None
            return True
        except Exception as e:
            print(f"Resim yükleme hatası: {e}")
            return False

    def get_image_for_display(self, image_array=None):
        """NumPy array'i PIL Image'a çevirir (göstermek için)"""
        if image_array is None:
            image_array = self.current_image

        if image_array is not None:
            # Eğer zaten PIL Image ise direkt döndür
            if isinstance(image_array, Image.Image):
                return image_array

            # NumPy array ise PIL Image'a çevir
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                return Image.fromarray(image_array.astype('uint8'), 'RGB')
            else:
                return Image.fromarray(image_array.astype('uint8'), 'L')
        return None

    def get_original_image_for_display(self):
        """Orijinal görseli PIL Image olarak döndür"""
        if self.original_image is not None:
            if isinstance(self.original_image, Image.Image):
                return self.original_image
            else:
                return Image.fromarray(self.original_image.astype('uint8'))
        return None

    # ✅ SORU 1: NOKTA İŞLEMLERİ
    def adjust_brightness(self, value):
        """Parlaklık ayarı"""
        if self.current_image is None:
            return None

        # RGB veya Gri tonlamalı görsel için
        if len(self.current_image.shape) == 3:
            # RGB görsel
            adjusted = np.clip(self.current_image.astype(np.float32) + value, 0, 255)
        else:
            # Gri tonlamalı görsel
            adjusted = np.clip(self.current_image.astype(np.float32) + value, 0, 255)

        self.current_image = adjusted.astype(np.uint8)
        return self.current_image

    def adjust_contrast(self, factor):
        """Kontrast ayarı"""
        if self.current_image is None:
            return None

        if len(self.current_image.shape) == 3:
            # RGB görsel
            mean = np.mean(self.current_image, axis=(0, 1))
            adjusted = factor * (self.current_image.astype(np.float32) - mean) + mean
        else:
            # Gri tonlamalı görsel
            mean = np.mean(self.current_image)
            adjusted = factor * (self.current_image.astype(np.float32) - mean) + mean

        self.current_image = np.clip(adjusted, 0, 255).astype(np.uint8)
        return self.current_image

    def image_negative(self):
        """Görsel negatifi"""
        if self.current_image is None:
            return None

        self.current_image = 255 - self.current_image
        return self.current_image

    def threshold_image(self, threshold_value):
        """Eşikleme"""
        if self.current_image is None:
            return None

        if len(self.current_image.shape) == 3:
            # RGB'yi gri tonlamaya çevir
            gray = np.dot(self.current_image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = self.current_image

        self.current_image = np.where(gray > threshold_value, 255, 0).astype(np.uint8)
        return self.current_image

    # ✅ SORU 2: HISTOGRAM İŞLEMLERİ
    def calculate_histogram(self, image=None):
        """Histogram hesaplama"""
        if image is None:
            image = self.current_image

        if image is None:
            return None

        if len(image.shape) == 3:
            # RGB görsel - gri tonlamaya çevir
            gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = image

        histogram = np.zeros(256)
        for i in range(256):
            histogram[i] = np.sum(gray == i)

        return histogram

    def calculate_statistics(self, image=None):
        """Görsel istatistikleri"""
        if image is None:
            image = self.current_image

        if image is None:
            return None

        if len(image.shape) == 3:
            gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = image

        stats = {
            'mean': np.mean(gray),
            'std': np.std(gray),
            'min': np.min(gray),
            'max': np.max(gray)
        }

        # Entropi hesaplama
        histogram = self.calculate_histogram(image)
        total_pixels = gray.shape[0] * gray.shape[1]
        entropy = 0.0

        for count in histogram:
            if count > 0:
                probability = count / total_pixels
                entropy -= probability * np.log2(probability)

        stats['entropy'] = entropy
        return stats

    def show_histogram(self, parent_window):
        """Histogram penceresi göster"""
        if self.current_image is None:
            return

        histogram = self.calculate_histogram()
        stats = self.calculate_statistics()

        # Yeni pencere oluştur
        hist_window = ctk.CTkToplevel(parent_window)
        hist_window.title("Histogram")
        hist_window.geometry("600x400")

        # Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.bar(range(256), histogram, color='blue', alpha=0.7)
        ax.set_title("Görsel Histogramı")
        ax.set_xlabel("Piksel Değeri")
        ax.set_ylabel("Frekans")
        ax.grid(True, alpha=0.3)

        # Canvas oluştur
        canvas = FigureCanvasTkAgg(fig, hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # İstatistikleri göster
        stats_text = f"Ortalama: {stats['mean']:.2f} | " \
                     f"Standart Sapma: {stats['std']:.2f} | " \
                     f"Entropi: {stats['entropy']:.2f}\n" \
                     f"Min: {stats['min']} | Max: {stats['max']}"

        stats_label = ctk.CTkLabel(hist_window, text=stats_text, font=("Segoe UI", 12))
        stats_label.pack(pady=10)

    # ✅ SORU 3: KONTRAST GERME
    def contrast_stretching(self):
        """Kontrast germe"""
        if self.current_image is None:
            return None

        if len(self.current_image.shape) == 3:
            gray = np.dot(self.current_image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = self.current_image

        min_val = np.min(gray)
        max_val = np.max(gray)

        if max_val == min_val:
            self.current_image = gray
        else:
            stretched = ((gray.astype(np.float32) - min_val) / (max_val - min_val)) * 255
            self.current_image = stretched.astype(np.uint8)

        return self.current_image

    # ✅ SORU 4: HISTOGRAM EŞİTLEME
    def histogram_equalization(self):
        """Histogram eşitleme"""
        if self.current_image is None:
            return None

        if len(self.current_image.shape) == 3:
            gray = np.dot(self.current_image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = self.current_image

        # Histogram hesapla
        histogram = self.calculate_histogram(gray)

        # Kümülatif histogram
        cumulative_hist = np.cumsum(histogram)

        # Normalize et
        total_pixels = gray.shape[0] * gray.shape[1]
        transformation = (cumulative_hist / total_pixels) * 255

        # Dönüşüm uygula
        equalized = transformation[gray.astype(np.uint8)]
        self.current_image = equalized.astype(np.uint8)

        return self.current_image

    # ✅ SORU 5: GAMMA DÜZELTMESİ
    def gamma_correction(self, gamma):
        """Gamma düzeltmesi"""
        if self.current_image is None:
            return None

        # Normalize et [0, 1]
        normalized = self.current_image.astype(np.float32) / 255.0

        # Gamma düzeltmesi uygula
        corrected = np.power(normalized, gamma)

        # Tekrar [0, 255] aralığına dön
        self.current_image = (corrected * 255).astype(np.uint8)
        return self.current_image

    # 🚀 YENİ: KALİTE ARTIRMA (OpenCV olmadan)
    def enhance_quality(self, quality_level):
        """Görsel kalitesini artırma - OpenCV olmadan"""
        if self.current_image is None:
            return None

        try:
            # PIL Image'a çevir
            pil_image = self.get_image_for_display(self.current_image)

            # 1. Keskinleştirme
            if quality_level > 1.0:
                # Unsharp Mask filtresi - parametreleri integer yap
                sharpened = pil_image.filter(ImageFilter.UnsharpMask(
                    radius=int(quality_level * 0.8),
                    percent=int(quality_level * 40),
                    threshold=2
                ))
            else:
                sharpened = pil_image

            # 2. Kontrast artırma
            if quality_level > 1.2:
                contrast_enhancer = ImageEnhance.Contrast(sharpened)
                enhanced = contrast_enhancer.enhance(1.0 + (quality_level - 1.0) * 0.2)
            else:
                enhanced = sharpened

            # 3. Keskinlik artırma
            if quality_level > 1.5:
                sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
                final_enhanced = sharpness_enhancer.enhance(quality_level * 0.8)
            else:
                final_enhanced = enhanced

            # 4. Renk doygunluğu (sadece renkli görseller için)
            if len(self.current_image.shape) == 3 and quality_level > 2.0:
                color_enhancer = ImageEnhance.Color(final_enhanced)
                final_enhanced = color_enhancer.enhance(1.0 + (quality_level - 2.0) * 0.1)

            # NumPy array'e çevir
            self.current_image = np.array(final_enhanced)

            return self.current_image

        except Exception as e:
            print(f"Kalite artırma hatası: {e}")
            # Hata durumunda orijinal görseli döndür
            return self.current_image

    def reset_to_original(self):
        """Orijinal görsele dön"""
        if self.original_image is not None:
            if isinstance(self.original_image, Image.Image):
                self.current_image = np.array(self.original_image)
            else:
                self.current_image = self.original_image.copy()
            return self.current_image
        return None
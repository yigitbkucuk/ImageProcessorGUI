import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from image_processor import ImageProcessor


class ImageProcessorApp:
    def __init__(self):
        # GUI teması
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("🎨 Görüntü İşleme Aracı")
        self.root.geometry("1400x900")

        self.processor = ImageProcessor()
        self.current_image_path = None
        self.setup_ui()

    def setup_ui(self):
        # BAŞLIK
        title_label = ctk.CTkLabel(
            self.root,
            text="🎨 GÖRÜNTÜ İŞLEME ARACI",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(pady=20)

        # DOSYA YÜKLEME BÖLÜMÜ
        file_frame = ctk.CTkFrame(self.root)
        file_frame.pack(pady=10, padx=20, fill="x")

        self.load_button = ctk.CTkButton(
            file_frame,
            text="📁 GÖRSEL YÜKLE",
            command=self.load_image,
            height=40,
            font=("Segoe UI", 14),
            fg_color="#2E86AB",
            hover_color="#1B6B93"
        )
        self.load_button.pack(pady=15)

        # ANA İÇERİK - YAN YANA DÜZEN
        main_content = ctk.CTkFrame(self.root)
        main_content.pack(pady=20, padx=20, fill="both", expand=True)

        # SOL: GÖRSELLER BÖLÜMÜ
        images_frame = ctk.CTkFrame(main_content)
        images_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Görsel konteyneri
        images_container = ctk.CTkFrame(images_frame)
        images_container.pack(fill="both", expand=True, padx=10, pady=10)

        # İki sütunlu görsel gösterimi
        images_columns = ctk.CTkFrame(images_container)
        images_columns.pack(fill="both", expand=True)

        # SOL: ORJİNAL GÖRSEL
        original_card = ctk.CTkFrame(images_columns, fg_color="#2C3E50", corner_radius=12)
        original_card.pack(side="left", fill="both", expand=True, padx=5)

        original_label = ctk.CTkLabel(
            original_card,
            text="ORJİNAL GÖRSEL",
            font=("Segoe UI", 16, "bold")
        )
        original_label.pack(pady=15)

        # Orjinal görsel container
        original_image_container = ctk.CTkFrame(original_card, fg_color="transparent")
        original_image_container.pack(expand=True, fill="both", padx=15, pady=15)

        self.original_image_label = ctk.CTkLabel(
            original_image_container,
            text="Görsel yüklenmedi",
            font=("Segoe UI", 14),
            text_color="gray",
            fg_color="#34495E",
            corner_radius=8
        )
        self.original_image_label.pack(expand=True, fill="both")

        # Orjinal görsel için büyütme butonu
        self.original_zoom_button = ctk.CTkButton(
            original_image_container,
            text="🔍",
            command=lambda: self.show_zoom_view("original"),
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color="transparent",
            hover_color="#2E86AB",
            corner_radius=20
        )
        self.original_zoom_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        self.original_zoom_button.pack_forget()

        # SAĞ: İŞLENMİŞ GÖRSEL
        processed_card = ctk.CTkFrame(images_columns, fg_color="#2C3E50", corner_radius=12)
        processed_card.pack(side="right", fill="both", expand=True, padx=5)

        processed_label = ctk.CTkLabel(
            processed_card,
            text="İŞLENMİŞ GÖRSEL",
            font=("Segoe UI", 16, "bold")
        )
        processed_label.pack(pady=15)

        # İşlenmiş görsel container
        processed_image_container = ctk.CTkFrame(processed_card, fg_color="transparent")
        processed_image_container.pack(expand=True, fill="both", padx=15, pady=15)

        self.processed_image_label = ctk.CTkLabel(
            processed_image_container,
            text="İşlem bekleniyor",
            font=("Segoe UI", 14),
            text_color="gray",
            fg_color="#34495E",
            corner_radius=8
        )
        self.processed_image_label.pack(expand=True, fill="both")

        # İşlenmiş görsel için büyütme butonu
        self.processed_zoom_button = ctk.CTkButton(
            processed_image_container,
            text="🔍",
            command=lambda: self.show_zoom_view("processed"),
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color="transparent",
            hover_color="#2E86AB",
            corner_radius=20
        )
        self.processed_zoom_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        self.processed_zoom_button.pack_forget()

        # İNDİRME BUTONU
        download_frame = ctk.CTkFrame(images_container)
        download_frame.pack(fill="x", pady=10)

        self.download_button = ctk.CTkButton(
            download_frame,
            text="💾 Görseli İndir",
            command=self.download_image,
            height=35,
            font=("Segoe UI", 12),
            fg_color="#27AE60",
            hover_color="#229954"
        )
        self.download_button.pack(pady=5)
        self.download_button.pack_forget()

        # SAĞ: KONTROL PANELİ (SCROLLABLE)
        control_scrollable = ctk.CTkScrollableFrame(main_content, width=400)
        control_scrollable.pack(side="right", fill="both", padx=10)

        # İŞLEMLER BAŞLIĞI
        operations_label = ctk.CTkLabel(
            control_scrollable,
            text="İŞLEMLER",
            font=("Segoe UI", 18, "bold")
        )
        operations_label.pack(pady=15)

        # BÜYÜK İŞLEM BUTONLARI (Sadece slider olmayan işlemler)
        self.setup_operation_buttons(control_scrollable)

        # AYARLAR BÖLÜMÜ
        settings_frame = ctk.CTkFrame(control_scrollable, fg_color="#34495E", corner_radius=10)
        settings_frame.pack(fill="x", padx=10, pady=10)

        # Ayarlar başlığı
        settings_label = ctk.CTkLabel(
            settings_frame,
            text="🎚️ İŞLEM AYARLARI",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        settings_label.pack(pady=10)

        # Açıklama
        info_label = ctk.CTkLabel(
            settings_frame,
            text="Bu ayarlar anında uygulanır\nİşlemler üst üste birikir",
            font=("Segoe UI", 11),
            text_color="lightblue",
            wraplength=350
        )
        info_label.pack(pady=(0, 10))

        # SLIDER'LAR
        sliders_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        sliders_container.pack(fill="x", padx=10, pady=5)

        # PARLAKLIK SLIDER
        self.brightness_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        self.brightness_frame.pack(fill="x", pady=5)
        self.brightness_label = ctk.CTkLabel(
            self.brightness_frame,
            text="🔆 Parlaklık: 0",
            font=("Segoe UI", 12)
        )
        self.brightness_label.pack(anchor="w", pady=(5, 0))
        self.brightness_slider = ctk.CTkSlider(
            self.brightness_frame,
            from_=-255, to=255,
            command=self.on_brightness_slider
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill="x", pady=(0, 10))

        # KONTRAST SLIDER
        self.contrast_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        self.contrast_frame.pack(fill="x", pady=5)
        self.contrast_label = ctk.CTkLabel(
            self.contrast_frame,
            text="⚡ Kontrast: 1.0",
            font=("Segoe UI", 12)
        )
        self.contrast_label.pack(anchor="w", pady=(5, 0))
        self.contrast_slider = ctk.CTkSlider(
            self.contrast_frame,
            from_=0.1, to=3.0,
            command=self.on_contrast_slider
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x", pady=(0, 10))

        # GAMMA SLIDER
        self.gamma_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        self.gamma_frame.pack(fill="x", pady=5)
        self.gamma_label = ctk.CTkLabel(
            self.gamma_frame,
            text="🌈 Gamma: 1.0",
            font=("Segoe UI", 12)
        )
        self.gamma_label.pack(anchor="w", pady=(5, 0))
        self.gamma_slider = ctk.CTkSlider(
            self.gamma_frame,
            from_=0.1, to=3.0,
            command=self.on_gamma_slider
        )
        self.gamma_slider.set(1.0)
        self.gamma_slider.pack(fill="x", pady=(0, 10))

        # KALİTE SLIDER
        self.quality_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        self.quality_frame.pack(fill="x", pady=5)
        self.quality_label = ctk.CTkLabel(
            self.quality_frame,
            text="🚀 Kalite: 1.0",
            font=("Segoe UI", 12)
        )
        self.quality_label.pack(anchor="w", pady=(5, 0))
        self.quality_slider = ctk.CTkSlider(
            self.quality_frame,
            from_=1.0, to=5.0,
            command=self.on_quality_slider
        )
        self.quality_slider.set(1.0)
        self.quality_slider.pack(fill="x", pady=(0, 10))

        # SIFIRLA BUTONU
        reset_frame = ctk.CTkFrame(control_scrollable)
        reset_frame.pack(fill="x", padx=10, pady=10)

        reset_btn = ctk.CTkButton(
            reset_frame,
            text="🔄 ORJİNAL GÖRSELE DÖN",
            command=self.reset_to_original,
            height=40,
            font=("Segoe UI", 14),
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        reset_btn.pack(fill="x", pady=5)

        # DURUM BİLGİSİ
        status_frame = ctk.CTkFrame(self.root, height=50)
        status_frame.pack(pady=10, padx=20, fill="x")
        status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="📁 Lütfen bir resim yükleyin...",
            font=("Segoe UI", 12),
            text_color="white"
        )
        self.status_label.pack(expand=True)

    def setup_operation_buttons(self, parent):
        """Büyük işlem butonları (Sadece slider olmayan işlemler)"""
        operations = [
            ("🎭 NEGATİF", "negative"),
            ("📊 HISTOGRAM", "histogram"),
            ("🔄 KONTRAST GERME", "contrast_stretch"),
            ("📈 HISTOGRAM EŞİTLEME", "histogram_equalization"),
        ]

        for op_text, op_key in operations:
            btn = ctk.CTkButton(
                parent,
                text=op_text,
                command=lambda k=op_key: self.select_operation(k),
                height=45,
                font=("Segoe UI", 13),
                fg_color="#2E86AB",
                hover_color="#1B6B93"
            )
            btn.pack(fill="x", padx=10, pady=5)

    def select_operation(self, operation):
        """İşlem seçimi - artık otomatik sıfırlama yok"""
        if self.current_image_path is None:
            messagebox.showwarning("Uyarı", "Önce bir resim yükleyin!")
            return

        # Önce slider filtrelerini uygula
        self.apply_slider_filters()

        # Sonra seçilen işlemi uygula
        if operation == "negative":
            self.apply_negative()
        elif operation == "contrast_stretch":
            self.apply_contrast_stretch()
        elif operation == "histogram_equalization":
            self.apply_histogram_equalization()
        elif operation == "histogram":
            self.show_histogram()

    def on_brightness_slider(self, value):
        """Parlaklık slider'ı değişimi - anında uygulanır"""
        self.brightness_label.configure(text=f"🔆 Parlaklık: {int(value)}")
        self.apply_slider_filters()

    def on_contrast_slider(self, value):
        """Kontrast slider'ı değişimi - anında uygulanır"""
        self.contrast_label.configure(text=f"⚡ Kontrast: {value:.1f}")
        self.apply_slider_filters()

    def on_gamma_slider(self, value):
        """Gamma slider'ı değişimi - anında uygulanır"""
        self.gamma_label.configure(text=f"🌈 Gamma: {value:.1f}")
        self.apply_slider_filters()

    def on_quality_slider(self, value):
        """Kalite slider'ı değişimi - anında uygulanır"""
        self.quality_label.configure(text=f"🚀 Kalite: {value:.1f}")
        self.apply_slider_filters()

    def apply_slider_filters(self):
        """Tüm slider filtrelerini sırayla uygula"""
        if self.current_image_path is None:
            return

        # Önce orijinal görsele dön
        self.processor.reset_to_original()

        # Sırayla tüm filtreleri uygula
        brightness_value = self.brightness_slider.get()
        contrast_value = self.contrast_slider.get()
        gamma_value = self.gamma_slider.get()
        quality_value = self.quality_slider.get()

        # Parlaklık uygula
        if brightness_value != 0:
            self.processor.adjust_brightness(brightness_value)

        # Kontrast uygula
        if contrast_value != 1.0:
            self.processor.adjust_contrast(contrast_value)

        # Gamma uygula
        if gamma_value != 1.0:
            self.processor.gamma_correction(gamma_value)

        # Kalite uygula
        if quality_value != 1.0:
            self.processor.enhance_quality(quality_value)

        # Sonucu göster
        self.update_display_image(self.processor.current_image)
        self.status_label.configure(
            text="✅ Ayarlar uygulandı!",
            text_color="green"
        )

    def apply_negative(self):
        """Negatif uygula"""
        self.processor.image_negative()
        self.update_display_image(self.processor.current_image)
        self.status_label.configure(
            text="✅ Negatif uygulandı!",
            text_color="green"
        )

    def show_histogram(self):
        """Histogram göster"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkToplevel) and "Histogram" in widget.title():
                widget.destroy()

        self.processor.show_histogram(self.root)
        self.status_label.configure(
            text="✅ Histogram gösteriliyor...",
            text_color="green"
        )

    def apply_contrast_stretch(self):
        """Kontrast germe uygula"""
        self.processor.contrast_stretching()
        self.update_display_image(self.processor.current_image)
        self.status_label.configure(
            text="✅ Kontrast germe uygulandı!",
            text_color="green"
        )

    def apply_histogram_equalization(self):
        """Histogram eşitleme uygula"""
        self.processor.histogram_equalization()
        self.update_display_image(self.processor.current_image)
        self.status_label.configure(
            text="✅ Histogram eşitleme uygulandı!",
            text_color="green"
        )

    def reset_to_original(self):
        """Sadece orijinal görsele dön"""
        self.processor.reset_to_original()
        self.update_display_image(self.processor.current_image)

        # Slider değerlerini sıfırla
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        self.quality_slider.set(1.0)

        self.brightness_label.configure(text="🔆 Parlaklık: 0")
        self.contrast_label.configure(text="⚡ Kontrast: 1.0")
        self.gamma_label.configure(text="🌈 Gamma: 1.0")
        self.quality_label.configure(text="🚀 Kalite: 1.0")

        self.status_label.configure(
            text="✅ Orijinal görsele dönüldü!",
            text_color="green"
        )

    def show_zoom_view(self, image_type):
        """Büyük ekranda görsel göster"""
        if self.current_image_path is None:
            messagebox.showwarning("Uyarı", "Önce bir resim yükleyin!")
            return

        # Yeni pencere oluştur
        zoom_window = ctk.CTkToplevel(self.root)
        zoom_window.title("🔍 Görsel Detay - Sol/Sağ tıklayarak görsel değiştirin")
        zoom_window.geometry("800x600")
        zoom_window.transient(self.root)

        # Görselleri hazırla
        original_display = self.processor.get_image_for_display(self.processor.original_image)
        processed_display = self.processor.get_image_for_display(self.processor.processed_image or self.processor.current_image)

        # Ekran boyutuna göre ölçekle
        screen_width = 700
        screen_height = 500

        original_resized = original_display.copy()
        processed_resized = processed_display.copy()

        original_resized.thumbnail((screen_width, screen_height))
        processed_resized.thumbnail((screen_width, screen_height))

        # PhotoImage'ları oluştur
        original_photo = ImageTk.PhotoImage(original_resized)
        processed_photo = ImageTk.PhotoImage(processed_resized)

        # Görsel label'ı
        self.zoom_label = ctk.CTkLabel(
            zoom_window,
            text="",
            font=("Segoe UI", 14, "bold")
        )
        self.zoom_label.pack(expand=True, fill="both", padx=20, pady=20)

        # Başlangıç görselini ayarla
        self.current_zoom_image = image_type
        if image_type == "original":
            self.zoom_label.configure(image=original_photo, text="ORJİNAL GÖRSEL")
            self.zoom_label.image = original_photo
        else:
            self.zoom_label.configure(image=processed_photo, text="İŞLENMİŞ GÖRSEL")
            self.zoom_label.image = processed_photo

        # Mouse tıklama olaylarını bağla
        self.zoom_label.bind("<Button-1>", lambda e: self.switch_zoom_view(zoom_window, original_photo, processed_photo, "original"))
        self.zoom_label.bind("<Button-3>", lambda e: self.switch_zoom_view(zoom_window, original_photo, processed_photo, "processed"))

        # Kullanım kılavuzu
        guide_label = ctk.CTkLabel(
            zoom_window,
            text="Sol Tık: Orjinal Görsel • Sağ Tık: İşlenmiş Görsel",
            font=("Segoe UI", 12),
            text_color="lightblue"
        )
        guide_label.pack(pady=10)

        # Kapatma butonu
        close_btn = ctk.CTkButton(
            zoom_window,
            text="Kapat",
            command=zoom_window.destroy,
            height=35,
            font=("Segoe UI", 12),
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        close_btn.pack(pady=10)

    def switch_zoom_view(self, window, original_photo, processed_photo, image_type):
        """Zoom penceresinde görsel değiştir"""
        if image_type == "original":
            self.zoom_label.configure(image=original_photo, text="ORJİNAL GÖRSEL")
            self.zoom_label.image = original_photo
            self.current_zoom_image = "original"
        else:
            self.zoom_label.configure(image=processed_photo, text="İŞLENMİŞ GÖRSEL")
            self.zoom_label.image = processed_photo
            self.current_zoom_image = "processed"

    def download_image(self):
        """Görseli indir"""
        if self.processor.processed_image is None and self.processor.current_image is None:
            messagebox.showwarning("Uyarı", "Önce bir işlem uygulayın!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ],
            title="Görseli İndir - Kaydet"
        )

        if file_path:
            try:
                display_image = self.processor.get_image_for_display(self.processor.processed_image or self.processor.current_image)
                display_image.save(file_path, quality=95)
                messagebox.showinfo("Başarılı", f"Görsel başarıyla indirildi:\n{file_path}")
                self.status_label.configure(
                    text=f"✅ Görsel indirildi: {os.path.basename(file_path)}",
                    text_color="green"
                )
            except Exception as e:
                messagebox.showerror("Hata", f"İndirme sırasında hata oluştu:\n{str(e)}")

    def update_display_image(self, image_array):
        """İşlenmiş görseli güncelle"""
        if image_array is not None:
            display_image = self.processor.get_image_for_display(image_array)
            if display_image:
                # Görsel boyutunu ayarla
                display_image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(display_image)
                self.processed_image_label.configure(image=photo, text="")
                self.processed_image_label.image = photo

                # İndirme butonunu ve büyütme butonlarını göster
                self.download_button.pack(pady=5)
                self.original_zoom_button.pack()
                self.processed_zoom_button.pack()

                self.status_label.configure(
                    text="✅ Görsel güncellendi!",
                    text_color="green"
                )

    def load_image(self):
        """Görsel yükle"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("All files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Resim Seçin",
            filetypes=file_types
        )

        if file_path:
            try:
                success = self.processor.load_image(file_path)
                if success:
                    original_image = Image.open(file_path)
                    display_original = original_image.copy()
                    display_original.thumbnail((400, 400))

                    original_photo = ImageTk.PhotoImage(display_original)
                    self.original_image_label.configure(image=original_photo, text="")
                    self.original_image_label.image = original_photo

                    # İşlenmiş görseli de başlangıçta orjinal olarak göster
                    self.processed_image_label.configure(image=original_photo, text="")
                    self.processed_image_label.image = original_photo

                    # İndirme butonunu ve büyütme butonlarını gizle
                    self.download_button.pack_forget()
                    self.original_zoom_button.pack_forget()
                    self.processed_zoom_button.pack_forget()

                    # Sadece slider değerlerini sıfırla
                    self.reset_sliders_only()

                    self.status_label.configure(
                        text=f"✅ {os.path.basename(file_path)} yüklendi! İşlemleri kullanabilirsiniz.",
                        text_color="green"
                    )

                    self.current_image_path = file_path

                else:
                    messagebox.showerror("Hata", "Resim işlemciye yüklenemedi!")

            except Exception as e:
                messagebox.showerror("❌ Hata", f"Resim yüklenemedi:\n{str(e)}")
                self.status_label.configure(
                    text="❌ Resim yüklenirken hata oluştu",
                    text_color="red"
                )

    def reset_sliders_only(self):
        """Sadece slider değerlerini sıfırla"""
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        self.quality_slider.set(1.0)

        self.brightness_label.configure(text="🔆 Parlaklık: 0")
        self.contrast_label.configure(text="⚡ Kontrast: 1.0")
        self.gamma_label.configure(text="🌈 Gamma: 1.0")
        self.quality_label.configure(text="🚀 Kalite: 1.0")

    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageProcessorApp()
    app.run()
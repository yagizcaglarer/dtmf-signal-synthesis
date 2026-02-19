# dtmf-signal-synthesis
Bu proje, DTMF (Dual-Tone Multi-Frequency) sistemini kullanarak telefon tuş seslerinin Python ortamında üretilmesini amaçlamaktadır.

-- Projenin Amacı

    Her tuşa karşılık gelen iki sinüzoidal frekansın üretilmesi
    
    Bu frekansların toplanarak DTMF sinyalinin elde edilmesi
    
    Üretilen sinyalin zaman domaininde görselleştirilmesi
    
    FFT kullanılarak frekans domaininde analiz edilmesi
    
    Sinyalin hoparlörden çalınması

-- Matematiksel Model

    DTMF sinyali aşağıdaki formül ile üretilmiştir:
    
    x(t) = sin(2πf_low t) + sin(2πf_high t)
    
    Örnekleme frekansı:
    fs = 8000 Hz
    
    Sinyal süresi:
    T = 0.3 saniye
    
    Toplam örnek sayısı:
    N = fs × T = 2400

-- Kullanılan Teknolojiler

    * Python
    
    * NumPy
    
    * Matplotlib
    
    * SoundDevice
    
    * Tkinter

-- Özellikler

    * İnteraktif telefon tuş takımı
    * Gerçek zamanlı DTMF üretimi
    * Zaman domain grafiği
    * FFT frekans analizi
    * Hoparlörden ses çıkışı

-- Kurulum ve Çalıştırma Talimatları

        1️⃣ Depoyu Klonlayın
        git clone https://github.com/yagizcaglarer/dtmf-signal-synthesis.git
        cd dtmf-signal-synthesis
        
        2️⃣ Gerekli Kütüphaneleri Yükleyin
        pip install -r requirements.txt
        
        3️⃣ Programı Çalıştırın
        python dtmf.py

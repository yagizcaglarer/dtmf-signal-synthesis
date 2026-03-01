import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read
from scipy.signal.windows import hamming
import customtkinter as ctk
from tkinter import messagebox

ornekfrekans = 8000
ses_suresi = 0.04
harf_ornegi = int(ornekfrekans * ses_suresi)

karakterler = list("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ")

dusuk_frekans  = [600, 700, 800, 900, 1000]
yuksek_frekans = [1100, 1200, 1300, 1400, 1500, 1600]

char_to_freq = {}
freq_to_char = {}

dizi = 0
for lf in dusuk_frekans:
    for hf in yuksek_frekans:
        if dizi < len(karakterler):
            char_to_freq[karakterler[dizi]] = (lf, hf)
            freq_to_char[(lf, hf)] = karakterler[dizi]
            dizi += 1


def encode_text(text):
    signal = np.array([])
    t = np.arange(harf_ornegi) / ornekfrekans

    for ch in text:
        ch = ch.upper()
        if ch not in char_to_freq:
            continue

        f1, f2 = char_to_freq[ch]
        tone = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)
        signal = np.concatenate((signal, tone))

    if len(signal) == 0:
        return signal

    signal = signal / np.max(np.abs(signal))
    return signal

def goertzel(samples, target_freq):
    k = int(0.5 + (harf_ornegi * target_freq) / ornekfrekans)
    omega = (2.0 * np.pi * k) / harf_ornegi
    coeff = 2.0 * np.cos(omega)

    s_prev = 0
    s_prev2 = 0

    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s

    power = s_prev2**2 + s_prev**2 - coeff*s_prev*s_prev2
    return power


def decode_signal(signal):
    decoded_text = ""
    window = hamming(harf_ornegi)
    num_blocks = len(signal) // harf_ornegi
    threshold = 10
    last_char = None

    for i in range(num_blocks):
        block = signal[i*harf_ornegi:(i+1)*harf_ornegi]
        block = block * window

        detected_low = None
        detected_high = None
        max_low_power = 0
        max_high_power = 0

        for lf in dusuk_frekans:
            power = goertzel(block, lf)
            if power > max_low_power:
                max_low_power = power
                detected_low = lf

        for hf in yuksek_frekans:
            power = goertzel(block, hf)
            if power > max_high_power:
                max_high_power = power
                detected_high = hf

        if max_low_power > threshold and max_high_power > threshold:
            char = freq_to_char.get((detected_low, detected_high), None)
            if char and char != last_char:
                decoded_text += char
                last_char = char
        else:
            last_char = None

    return decoded_text


def encode_button():
    text = entry.get()

    if not text:
        messagebox.showwarning("Uyarı", "Metin giriniz.")
        return

    signal = encode_text(text)

    if len(signal) == 0:
        messagebox.showerror("Hata", "Geçerli karakter yok.")
        return

    write("ses.wav", ornekfrekans, signal.astype(np.float32))
    sd.play(signal, ornekfrekans)

    result_label.configure(text="Encoding tamamlandı ve ses.wav oluşturuldu.")

def decode_button():
    try:
        sr, data = read("ses.wav")
    except:
        messagebox.showerror("Hata", "Önce encode işlemi yapın.")
        return

    if data.ndim > 1:
        data = data[:,0]

    decoded = decode_signal(data)
    result_label.configure(text="Çözülen Metin: " + decoded)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Frekans Kodlama Sistemi")
app.geometry("600x400")

title = ctk.CTkLabel(
    app,
    text="Goertzel Frekans Kodlama Sistemi",
    font=ctk.CTkFont(size=20, weight="bold")
)
title.pack(pady=20)

entry = ctk.CTkEntry(
    app,
    width=400,
    height=40,
    placeholder_text="Metin giriniz..."
)
entry.pack(pady=10)

encode_btn = ctk.CTkButton(
    app,
    text="🎵 Encode (Ses Üret)",
    width=250,
    height=40,
    command=encode_button
)
encode_btn.pack(pady=10)

decode_btn = ctk.CTkButton(
    app,
    text="🔍 Decode (Çöz)",
    width=250,
    height=40,
    command=decode_button
)
decode_btn.pack(pady=10)

result_label = ctk.CTkLabel(
    app,
    text="",
    font=ctk.CTkFont(size=14)
)
result_label.pack(pady=20)

app.mainloop()
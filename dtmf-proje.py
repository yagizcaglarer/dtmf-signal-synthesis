import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import tkinter as tk
from tkinter import ttk

dtmf_freq = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}


fs = 8000
T = 0.3

def generate_dtmf(key):
    f_low, f_high = dtmf_freq[key]

    t = np.linspace(0, T, int(fs*T), endpoint=False)

    signal = np.sin(2*np.pi*f_low*t) + np.sin(2*np.pi*f_high*t)

    signal = signal * 0.5

    return signal, t


def play_tone(key):
    signal, t = generate_dtmf(key)

    sd.play(signal, fs)


    plt.figure(figsize=(10,4))
    plt.plot(t[:400], signal[:400])
    plt.title(f"{key} Tuşu - Zaman Domaini")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Genlik")
    plt.grid()
    plt.show()


    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/fs)

    plt.figure(figsize=(10,4))
    plt.plot(freqs[:len(freqs)//2], np.abs(fft_vals)[:len(freqs)//2])
    plt.title(f"{key} Tuşu - Frekans Spektrumu (FFT)")
    plt.xlabel("Frekans (Hz)")
    plt.ylabel("Genlik")
    plt.grid()
    plt.show()



root = tk.Tk()
root.title("DTMF Sinyal Sentezi")
root.geometry("540x700")

style = ttk.Style()
style.configure("TButton", font=("Arial", 16), padding=10)

buttons = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

for i, row in enumerate(buttons):
    for j, key in enumerate(row):
        btn = ttk.Button(root, text=key, command=lambda k=key: play_tone(k))
        btn.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")

for i in range(4):
    root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(i, weight=1)

root.mainloop()

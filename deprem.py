import tkinter as tk
from tkinter import messagebox
import feedparser
import pygame
from tkinter import Toplevel, Label, Button
import webbrowser  # Linki açmak için

# RSS URL'sini belirleyin
rss_url = "http://koeri.boun.edu.tr/rss/"  # Örnek bir RSS URL'si

# Pygame ses başlatma
pygame.mixer.init()

# Ses dosyasını yükleyin
alert_sound = pygame.mixer.Sound("alert_sound.wav")  # Burada bir ses dosyası kullanın

# Yeni veri vurgulama süresi (ms)
highlight_duration = 3000  # 3 saniye vurgulama

# Önceki RSS verilerini saklayacak liste
previous_entries = []

def fetch_rss():
    global previous_entries
    
    feed = feedparser.parse(rss_url)
    listbox.delete(0, tk.END)
    
    if feed.entries:
        new_entries = []
        
        # Yeni gelen RSS verisini kontrol et
        for entry in feed.entries:
            listbox.insert(tk.END, entry.title)
            new_entries.append(entry.title)
        
        # Yeni veri geldi mi kontrol et
        new_data = [entry for entry in new_entries if entry not in previous_entries]
        
        if new_data:
            # Yeni veri varsa sesli uyarı çaldır
            alert_sound.play()
            highlight_new_entry()
        
        # Önceki verileri güncelle
        previous_entries = new_entries

    else:
        messagebox.showerror("Hata", "Deprem veri beslemesi okunamadı.")
    
    # 60 saniye sonra fonksiyonu tekrar çalıştır (60000 ms)
    root.after(60000, fetch_rss)

def highlight_new_entry():
    # Listbox'taki son öğeyi seç ve vurgula
    listbox.itemconfig(tk.END, {'bg': 'yellow'})
    
    # Vurgulamayı 3 saniye sonra geri al
    root.after(highlight_duration, reset_highlight)

def reset_highlight():
    # Son öğenin rengini geri al
    listbox.itemconfig(tk.END, {'bg': 'white'})

def show_custom_details(title, message):
    custom_window = Toplevel(root)
    custom_window.title(title)
    custom_window.geometry("300x150")  # Sabit boyut
    custom_window.resizable(False, False)  # Boyutlandırılamaz yap

    label = Label(custom_window, text=message, wraplength=250)
    label.pack(pady=10)

    close_button = Button(custom_window, text="Tamam", command=custom_window.destroy)
    close_button.pack(pady=5)

def show_details(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_entry = feedparser.parse(rss_url).entries[selected_index[0]]
        show_custom_details("Detaylar", f"Bilgi: {selected_entry.title}")

# Linke tıklanınca çalışacak fonksiyon
def open_link(event):
    webbrowser.open("https://qrv73.com")

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Deprem Veri Okuyucu")
root.geometry("600x400")  # Sabit boyut
root.resizable(False, False)  # Boyutlandırılamaz yap

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=10)
listbox.bind('<<ListboxSelect>>', show_details)

fetch_button = tk.Button(root, text="Veriyi Al", command=fetch_rss)
fetch_button.pack()

# Alt yazıyı ekleyin
footer_label = Label(root, text="Programming By QRV73.com", fg="blue", cursor="hand2")
footer_label.pack(side="bottom", pady=5)
footer_label.bind("<Button-1>", open_link)  # Tıklanabilir yapmak için

# İlk çalıştırma
fetch_rss()

root.mainloop()


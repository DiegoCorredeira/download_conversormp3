import pytube
from pytube import exceptions
import os
import tkinter as tk
from tkinter import messagebox, filedialog


def download_audio():
    url = entry_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira uma URL")
        return

    pasta_destino = filedialog.askdirectory(title='Selecione a pasta de destino')
    if pasta_destino:
        try:
            youtube = pytube.YouTube(url)
            audio = youtube.streams.filter(only_audio=True).first()
            destino = audio.download(output_path=pasta_destino)
            nome_mp3 = f"{youtube.title}.mp3"
            artist = youtube.author
            nome_destino = os.path.join(pasta_destino, nome_mp3)
            os.rename(destino, nome_destino)
            messagebox.showinfo('Sucesso', f"Você baixou uma musica de {artist}")
            return nome_destino
        except pytube.exceptions.ExtractError:
            messagebox.showerror("Erro", "Erro ao extraír audio do vídeo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocorreu um erro ao baixar o áudio: {str(e)}")


root = tk.Tk()
root.title('Download audio do Youtube')
root.geometry("400x200")
root.resizable(False, False)
root.config(bg="#F0F0F0")

label_url = tk.Label(root, text='URL DO VIDEO AQUI')
label_url.pack()

entry_url = tk.Entry(root, width=60, font=("Arial, 12"))
entry_url.pack()

button_download = tk.Button(root, text='Baixar video', command=download_audio, font=("Arial, 12"), width=15)
button_download.pack(pady=10)

root.mainloop()

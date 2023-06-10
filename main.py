import pytube
from pytube import exceptions
import os
import tkinter as tk
from tkinter import messagebox, filedialog


def baixar_videos(url, pasta_destino):
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


def download_audio():
    url = entry_url.get()
    pasta_destino = filedialog.askdirectory(title='Selecione a pasta de destino')
    if pasta_destino:
        audio_file = baixar_videos(url, pasta_destino)
        if audio_file:
            messagebox.showinfo("Concluído", f'Download concluído com sucesso!')


root = tk.Tk()
root.title('Download audio do Youtube')

label_url = tk.Label(root, text='URL DO VIDEO AQUI')
label_url.pack()

entry_url = tk.Entry(root, width=50)
entry_url.pack()

button_download = tk.Button(root, text='Baixar video', command=download_audio)
button_download.pack()

root.mainloop()

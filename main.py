from googleapiclient.discovery import build
import pytube
from pytube import exceptions
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog

API_KEY = 'AIzaSyCWJT2WyA1MqdaaXv6kFVo_doBhbpDur8U'
# Criar a tabela - OK
# Inserir dados na tabela - OK
# Obter resposta da tabela - OK
# Search Integrado com a API do Youtube
# Historico Embutido no programa com output
historico = []

def create_table():
    connection = sqlite3.connect('historico.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS historico (id INTEGER PRIMARY KEY,url TEXT, titulo TEXT)')
    connection.commit()
    connection.close()

def insert_data(url, titulo):
    connection = sqlite3.connect('historico.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO historico (url, titulo) VALUES (?,?)', (url, titulo))
    connection.commit()
    connection.close()

def get_data():
    connection = sqlite3.connect('historico.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM historico')
    registros = cursor.fetchall()
    connection.close()
    return registros

def baixar_audio_yt(url, pasta_destino):
    try:
        youtube = pytube.YouTube(url)
        audio = youtube.streams.filter(only_audio=True).first()
        destino = audio.download(output_path=pasta_destino)
        nome_mp3 = f"{youtube.title}.mp3"
        artist = youtube.author
        nome_destino = os.path.join(pasta_destino, nome_mp3)
        historico.append(nome_mp3)
        os.rename(destino, nome_destino)
        messagebox.showinfo('Sucesso', f"Você baixou uma musica de {artist}")

        return nome_destino
    except pytube.exceptions.ExtractError:
        messagebox.showerror("Erro", "Erro ao extraír audio do vídeo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocorreu um erro ao baixar o áudio: {str(e)}")


def download_audio():
    url = entry_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira uma URL")
        return
    pasta_destino = filedialog.askdirectory(title='Selecione a pasta de destino')
    if pasta_destino:
        audio_file = baixar_audio_yt(url, pasta_destino)
        if audio_file:
            messagebox.showinfo("Concluído", f"Download concluído")



def open_folder():
    pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino. ")
    if pasta_destino:
        os.startfile(pasta_destino)

def exibir_historico():
    messagebox.showinfo("Histórico de Downloads", "\n".join(historico))
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

button_open_folder = tk.Button(root, text="Abrir Pasta", command=open_folder, font=("Arial, 12"), width=15)
button_open_folder.pack(pady=10)

button_historico = tk.Button(root, text="Exibir Histórico", command=exibir_historico, font=("Arial, 12"), width=15)
button_historico.pack(pady=10)

root.mainloop()

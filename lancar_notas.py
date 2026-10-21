import pandas as pd
import pyautogui, pyperclip, time, subprocess, os

pyautogui.PAUSE = 0.3

URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfNeTsN1u-fZJ0_n8O6JyoXUcJrzPB0-GhNMTXIcfZplTCOqg/viewform"
ARQUIVO_CSV = "notas_alunos.csv"
CAMPOS = ["RA", "Nome", "Nota", "Nota2", "TF1", "TF2"] 
LIMITE = None 
TABS_INICIAIS = 4  

df = pd.read_csv(ARQUIVO_CSV, sep=";", dtype=str)
df = df.rename(columns={"nota01": "Nota", "nota02": "Nota2", "TF01": "TF1", "TF02": "TF2"})
df["RA"] = df["RA"].str.strip().str.split("-").str[0].str.lstrip("0")
df = df.dropna(subset=["RA"])
print(df.head(2))

feitos = set()
if os.path.exists("progresso.txt"):
    with open("progresso.txt") as f:
        feitos = set(f.read().split())

def colar():
    subprocess.run([
        "osascript", "-e",
        'tell application "System Events" to keystroke "v" using command down'
    ])


def digitar(valor):
    pyperclip.copy(str(valor))
    time.sleep(0.3)
    colar()
    time.sleep(0.3)

def abrir_formulario():
    pyautogui.keyDown("command")
    pyautogui.press("l")
    pyautogui.keyUp("command")
    time.sleep(0.5)
    digitar(URL_FORM)
    pyautogui.press("enter")
    time.sleep(4)

def lancar(aluno):
    abrir_formulario()
    for _ in range(TABS_INICIAIS):
        pyautogui.press("tab")
        time.sleep(0.3)
    for campo in CAMPOS:
        digitar(aluno[campo])
        pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(3)

pendentes = df[~df["RA"].isin(feitos)]
if LIMITE:
    pendentes = pendentes.head(LIMITE)

print(f"{len(pendentes)} alunos para lançar. Deixe o navegador em primeiro plano. Começo em 5 segundos...")
time.sleep(5)

for n, (i, aluno) in enumerate(pendentes.iterrows(), start=1):
    lancar(aluno)
    with open("progresso.txt", "a") as f:
        f.write(aluno["RA"] + "\n")
    print(f"{n}/{len(pendentes)} - {aluno['Nome']}")
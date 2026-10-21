import pandas as pd
import re

LINK = "https://docs.google.com/spreadsheets/d/1sIoY1nNJIxhYacwB6pmeGgPrHpcNc9pkPOJlIpvRE5E/edit?resourcekey=&gid=1614962099#gid=1614962099"

COL_RA = "ra"
COL_NOME = "nome"
PESOS = {"nota": 7, "nota2": 7, "TF1": 2, "TF2": 2}

def link_para_csv(link):
    id_planilha = re.search(r"/d/([a-zA-Z0-9-_]+)", link).group(1)
    achou_gid = re.search(r"gid=(\d+)", link)
    gid = achou_gid.group(1) if achou_gid else "0"
    return f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid={gid}"

def carregar():
    return pd.read_csv(link_para_csv(LINK), dtype=str)

def para_numero(texto):
    return float(str(texto).replace(",", "."))

def calcular_media(aluno):
    soma = 0
    soma_pesos = 0
    for coluna, peso in PESOS.items():
        soma += para_numero(aluno[coluna]) * peso
        soma_pesos += peso
    return soma / soma_pesos

df = carregar()
print("Colunas encontradas:", list(df.columns))
print(f"{len(df)} linhas carregadas.")

while True:
    ra = input("\nDigite o RA (ou 'sair'): ").strip()
    if ra.lower() == "sair":
        break

    df = carregar()  
    resultado = df[df[COL_RA].str.strip() == ra]
    if resultado.empty:
        print("RA não encontrado.")
        continue

    aluno = resultado.iloc[-1] 
    if len(resultado) > 1:
        print(f"(Atenção: esse RA aparece {len(resultado)} vezes, usei o último lançamento.)")

    print(f"\nNome: {aluno[COL_NOME]}")
    for coluna, peso in PESOS.items():
        print(f"{coluna} (peso {peso}): {aluno[coluna]}")
    print(f"Média: {calcular_media(aluno):.2f}")
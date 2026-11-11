from pathlib import Path

import pandas as pd

dados = pd.read_csv(Path(__file__).parent / "resultados.csv")
if dados.empty:
    raise SystemExit("resultados.csv ainda está vazio. Faça os testes e preencha a planilha.")

print(f"Participantes: {len(dados)}\n")
print("Tempo para encontrar a informação (segundos):")
for t in ["t1", "t2", "t3"]:
    tempos = dados[f"{t}_tempo_s"]
    print(f"  {t.upper()}: média {tempos.mean():.0f}  mediana {tempos.median():.0f}  "
          f"mín {tempos.min():.0f}  máx {tempos.max():.0f}  acerto {dados[f'{t}_acertou'].mean():.0%}")

notas = dados[["q1", "q2", "q3", "q4", "q5"]]
print("\nFacilidade de uso (1 a 5):")
for coluna in notas:
    print(f"  {coluna}: {notas[coluna].mean():.1f}")
print(f"  Média geral: {notas.values.mean():.2f}  ({notas.values.mean() / 5:.0%} da nota máxima)")

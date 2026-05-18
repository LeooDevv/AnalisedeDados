"""
Gerador de Dados Sintéticos - Projeto Credit Risk Analytics
Faculdade Engenheiro Salvador Arena
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 5000

# --- Dimensão Cliente ---
ages = np.random.normal(38, 12, N).clip(18, 75).astype(int)
education_map = {1: "Pós-Graduação", 2: "Graduação", 3: "Ensino Médio", 4: "Outros"}
educations = np.random.choice([1, 2, 3, 4], N, p=[0.20, 0.45, 0.25, 0.10])
genders = np.random.choice(["Masculino", "Feminino"], N, p=[0.52, 0.48])
marriage_map = {1: "Casado", 2: "Solteiro", 3: "Outros"}
marriages = np.random.choice([1, 2, 3], N, p=[0.45, 0.42, 0.13])

dim_cliente = pd.DataFrame({
    "id_cliente": range(1, N + 1),
    "idade": ages,
    "faixa_etaria": pd.cut(ages, bins=[17,25,35,45,55,75],
                           labels=["18-25","26-35","36-45","46-55","56+"]),
    "escolaridade": [education_map[e] for e in educations],
    "genero": genders,
    "estado_civil": [marriage_map[m] for m in marriages],
})

# --- Dimensão Tempo ---
months = pd.date_range("2023-01-01", periods=24, freq="MS")
dim_tempo = pd.DataFrame({
    "id_tempo": range(1, 25),
    "mes_ano": months.strftime("%Y-%m"),
    "mes": months.month,
    "ano": months.year,
    "trimestre": months.quarter,
    "semestre": (months.month > 6).astype(int) + 1,
})

# --- Dimensão Produto/Limite ---
credit_limits = np.random.lognormal(mean=10.5, sigma=0.7, size=N).clip(1000, 500000)
credit_bins = [0, 10000, 30000, 60000, 100000, 500001]
credit_labels = ["< 10k", "10k-30k", "30k-60k", "60k-100k", "> 100k"]
dim_produto = pd.DataFrame({
    "id_produto": range(1, N + 1),
    "limite_credito": credit_limits.astype(int),
    "faixa_limite": pd.cut(credit_limits, bins=credit_bins, labels=credit_labels),
    "tipo_cartao": np.random.choice(["Standard", "Gold", "Platinum"],
                                    N, p=[0.60, 0.30, 0.10]),
})

# --- Fato Default (Inadimplência) ---
# Regra de negócio: inadimplência influenciada por idade, limite, escolaridade
prob_default = (
    0.25
    - 0.003 * (ages - 18)
    - 0.00000015 * credit_limits
    + 0.05 * (educations == 3).astype(float)
    + 0.03 * (marriages == 2).astype(float)
)
prob_default = prob_default.clip(0.05, 0.65)
default = (np.random.rand(N) < prob_default).astype(int)

# Distribuir clientes ao longo dos meses
id_tempo_assign = np.random.choice(range(1, 25), N)

# Valores de fatura e pagamento
bill_amt = (credit_limits * np.random.uniform(0.1, 0.95, N)).astype(int)
pay_amt = np.where(default == 0,
                   (bill_amt * np.random.uniform(0.3, 1.2, N)).astype(int),
                   (bill_amt * np.random.uniform(0.0, 0.2, N)).astype(int))

# Score de risco (simulado, 300-850)
risk_score = (
    850
    - default * 200
    - np.random.normal(0, 30, N)
    - (educations == 3) * 40
    + (ages > 35) * 20
).clip(300, 850).astype(int)

fato_default = pd.DataFrame({
    "id_fato": range(1, N + 1),
    "id_cliente": range(1, N + 1),
    "id_produto": range(1, N + 1),
    "id_tempo": id_tempo_assign,
    "valor_fatura": bill_amt,
    "valor_pago": pay_amt,
    "inadimplente": default,
    "score_risco": risk_score,
    "prob_default_real": prob_default.round(4),
})

# --- Salvar ---
os.makedirs("processed", exist_ok=True)
dim_cliente.to_csv("processed/dim_cliente.csv", index=False)
dim_tempo.to_csv("processed/dim_tempo.csv", index=False)
dim_produto.to_csv("processed/dim_produto.csv", index=False)
fato_default.to_csv("processed/fato_default.csv", index=False)

print("✅ Dados gerados com sucesso!")
print(f"   - {N} clientes | Taxa de inadimplência: {default.mean():.1%}")

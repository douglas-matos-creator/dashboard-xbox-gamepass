import pandas as pd
import numpy as np

# Configuração para reprodutibilidade
np.random.seed(42)

n_utilizadores = 1000

# Dados simulados de utilizadores do Xbox Game Pass
ids = [f"XBOX-{1000 + i}" for i in range(n_utilizadores)]
planos = np.random.choice(['PC Game Pass', 'Console Game Pass', 'Ultimate'], size=n_utilizadores, p=[0.3, 0.3, 0.4])
precos_plano = {'PC Game Pass': 9.99, 'Console Game Pass': 10.99, 'Ultimate': 14.99}

# Horas jogadas no último mês
horas_jogadas = np.random.normal(loc=25, scale=15, size=n_utilizadores).round(1)
horas_jogadas = np.clip(horas_jogadas, 0, 120)

# Dispositivo principal
dispositivos = np.random.choice(['PC', 'Xbox Series X/S', 'Cloud Gaming', 'Xbox One'], size=n_utilizadores)

# Estado da Subscrição (Ativo vs Churn/Cancelado)
# Utilizadores com poucas horas jogadas têm maior probabilidade de cancelar (Churn)
prob_churn = np.where(horas_jogadas < 10, 0.6, np.where(horas_jogadas < 25, 0.2, 0.05))
status_churn = [np.random.choice(['Ativo', 'Cancelado'], p=[1-p, p]) for p in prob_churn]

# Criar DataFrame
df_xbox = pd.DataFrame({
    'ID_Utilizador': ids,
    'Plano': planos,
    'Mensalidade': [precos_plano[p] for p in planos],
    'Horas_Jogadas_Mes': horas_jogadas,
    'Dispositivo_Principal': dispositivos,
    'Status': status_churn
})

# Salvar em CSV
df_xbox.to_csv('xbox_game_pass.csv', index=False)
print("Ficheiro 'xbox_game_pass.csv' criado com sucesso!")
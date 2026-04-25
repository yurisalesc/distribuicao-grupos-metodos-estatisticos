import pandas as pd
import pulp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

print("Executando Método 2: Otimização Linear Inteira Mista (MILP)\n")

file_path = "perfil_alunos.csv"
if not os.path.exists(file_path): file_path = "perfil_alunos"

df = pd.read_csv(file_path).dropna(subset=['Nome Completo']).copy().reset_index(drop=True)

N_ALUNOS = len(df)
N_GRUPOS = 3
CAPACIDADES = [6, 6, 6] 
features = ['Soft Skills - Comunicação', 'Soft Skills - Habilidade de escrita', 'Soft Skills - Liderança']

medias_globais = df[features].mean().values
prob = pulp.LpProblem("Equilibrio_de_Grupos", pulp.LpMinimize)
x = pulp.LpVariable.dicts("x", (range(N_ALUNOS), range(N_GRUPOS)), cat='Binary')

for i in range(N_ALUNOS): prob += pulp.lpSum([x[i][j] for j in range(N_GRUPOS)]) == 1
for j in range(N_GRUPOS): prob += pulp.lpSum([x[i][j] for i in range(N_ALUNOS)]) == CAPACIDADES[j]

dev_vars = []
for j in range(N_GRUPOS):
    for f_idx, feature in enumerate(features):
        d = pulp.LpVariable(f"desvio_g{j}_f{f_idx}", lowBound=0)
        soma_grupo = pulp.lpSum([x[i][j] * df.loc[i, feature] for i in range(N_ALUNOS)])
        soma_ideal = medias_globais[f_idx] * CAPACIDADES[j]
        prob += d >= soma_grupo - soma_ideal
        prob += d >= soma_ideal - soma_grupo
        dev_vars.append(d)

prob += pulp.lpSum(dev_vars)
status = prob.solve(pulp.PULP_CBC_CMD(msg=0))

df['Grupo_Final'] = -1
for i in range(N_ALUNOS):
    for j in range(N_GRUPOS):
        # pulp.value retorna 1 se a variável binaria acendeu!
        if pulp.value(x[i][j]) == 1:
            df.loc[i, 'Grupo_Final'] = j + 1

# Gráfico Estático Fixo
medias_por_grupos = df.groupby('Grupo_Final')[features].mean()
medias_por_grupos.columns = ['Comunicação', 'Escrita', 'Liderança']
ax_static = medias_por_grupos.plot(kind='bar', figsize=(10,6), colormap='viridis', edgecolor='black')
plt.axhline(y=medias_globais[0], color='blue', linestyle='--', linewidth=0.8, alpha=0.5, label='Média Global Com')
plt.title('Comparativo Absoluto de Habilidades (MILP Estático)')
plt.ylabel('Score Médio Alocado')
plt.xlabel('Grupos')
plt.xticks(rotation=0)
plt.savefig("grafico_metodo_2_milp.png", dpi=150)
plt.close()

# ==== ANIMAÇÃO DE DISTRIBUIÇÃO DAS PESSOAS (O Solver lendo a matriz binaria) ====
fig, ax = plt.subplots(figsize=(10, 6))

alunos = df[['Nome Completo', 'Grupo_Final']].to_dict('records')

def init():
    ax.clear()
    ax.set_ylim(0, 8)
    return ax,

def update(frame):
    ax.clear()
    ax.set_ylim(0, 8)
    ax.set_title(f'Lendo a Matriz Binária do Solver (Alocados: {frame}/18)')
    
    contagem = {1: 0, 2: 0, 3: 0}
    for i in range(frame):
        contagem[alunos[i]['Grupo_Final']] += 1
        
    ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], 
            [contagem[1], contagem[2], contagem[3]], 
            color=['silver', 'gray', 'black'])
            
    # Escreve o aluno que a matriz binária resolveu nesse frame
    if frame > 0:
        ultimo = alunos[frame-1]
        nome = ultimo['Nome Completo'].split()[0]
        g_id = ultimo['Grupo_Final']
        ax.text(g_id - 1, contagem[g_id] + 0.2, f"+ {nome}\n(x[{frame-1},{g_id-1}] = 1)", 
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkred')

    return ax,

anim = FuncAnimation(fig, update, frames=18+1, init_func=init, interval=400, blit=False)
anim.save("anim_m2.gif", writer='pillow', dpi=80)
print("Animação de pessoas caindo na matriz binaria salva em: anim_m2.gif")

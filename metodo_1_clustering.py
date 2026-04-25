import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

print("Executando Método 1: Clustering K-Means e Amostragem Estratificada\n")

file_path = "perfil_alunos.csv"
if not os.path.exists(file_path): file_path = "perfil_alunos"

df_alunos = pd.read_csv(file_path).dropna(subset=['Nome Completo']).copy()
features = ['Soft Skills - Comunicação', 'Soft Skills - Habilidade de escrita', 'Soft Skills - Liderança']

scaler = StandardScaler()
X = scaler.fit_transform(df_alunos[features])

k = 6 
kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
df_alunos['Cluster'] = kmeans.fit_predict(X)

# --- Grafico Estático 3D ---
fig3d = plt.figure(figsize=(10, 8))
ax3d = fig3d.add_subplot(111, projection='3d')
ax3d.scatter(
    df_alunos[features[0]], df_alunos[features[1]], df_alunos[features[2]], 
    c=df_alunos['Cluster'], cmap='rainbow', s=100, label='Membros Regulares'
)
ax3d.set_xlabel('Comunicação')
ax3d.set_ylabel('Escrita')
ax3d.set_zlabel('Liderança')
ax3d.set_title('Método 1: Clusters de Soft Skills (18 Alunos)')
plt.savefig("grafico_metodo_1_clusters.png", dpi=150)
plt.close(fig3d)


grupos = {1: [], 2: [], 3: []}
capacidades = {1: 6, 2: 6, 3: 6}
grupo_atual = 1

# Historico para animação (qual aluno foi pra qual grupo passo a passo)
historico_alocacao = []

for cluster_id in range(k):
    alunos_no_cluster = df_alunos[df_alunos['Cluster'] == cluster_id].to_dict('records')
    for aluno in alunos_no_cluster:
        while len(grupos[grupo_atual]) >= capacidades[grupo_atual]:
            grupo_atual = 1 if grupo_atual == 3 else grupo_atual + 1
        grupos[grupo_atual].append(aluno)
        
        # Salva o estado para animar
        historico_alocacao.append({
            'nome': aluno['Nome Completo'],
            'cluster_color': cluster_id,
            'grupo_destino': grupo_atual
        })
        
        grupo_atual = 1 if grupo_atual == 3 else grupo_atual + 1

# === ANIMAÇÃO DE PREENCHIMENTO DOS GRUPOS ===
fig, ax = plt.subplots(figsize=(10, 6))

def init():
    ax.clear()
    ax.set_ylim(0, 8)
    ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], [0, 0, 0])
    return ax,

def update(frame):
    ax.clear()
    ax.set_ylim(0, 8)
    ax.set_title(f'Sorteando 1 aluno por Cluster -> Alocando: {frame}/18')
    ax.set_ylabel('Vagas Preenchidas')
    
    contagem = {1: 0, 2: 0, 3: 0}
    
    # Desenha apenas os alunos que ja cairam ate o frame atual
    for i in range(frame):
        g_dest = historico_alocacao[i]['grupo_destino']
        contagem[g_dest] += 1
    
    # Plota barras agregadas
    barras = ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], 
                    [contagem[1], contagem[2], contagem[3]], 
                    color=['#1f77b4', '#ff7f0e', '#2ca02c'])
                    
    # Escreve o nome do ULTIMO aluno caindo em cima da barra pra dar efeito dinamico
    if frame > 0:
        ultimo = historico_alocacao[frame-1]
        nome = ultimo['nome'].split()[0] # Pega só o primeiro nome
        g_id = ultimo['grupo_destino']
        altura = contagem[g_id]
        ax.text(g_id - 1, altura + 0.2, f"+ {nome}\n(Cluster {ultimo['cluster_color']})", 
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='purple')
        
    return barras,

anim = FuncAnimation(fig, update, frames=18+1, init_func=init, interval=400, blit=False)
anim.save("anim_m1.gif", writer='pillow', dpi=80)
print("Animação interativa de alocação estrita salva em: anim_m1.gif")

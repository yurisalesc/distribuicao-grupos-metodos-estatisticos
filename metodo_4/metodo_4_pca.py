import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import os

print("Executando Método 4: PCA e Draft\n")

file_path = "perfil_alunos.csv"
if not os.path.exists(file_path): file_path = "perfil_alunos"

df = pd.read_csv(file_path).dropna(subset=['Nome Completo']).copy().reset_index(drop=True)
features = ['Soft Skills - Comunicação', 'Soft Skills - Habilidade de escrita', 'Soft Skills - Liderança']

X = df[features]
pca = PCA(n_components=1)
df['Escore_PCA'] = pca.fit_transform(X)

# Apenas re-ordenar baseando-se nas notas para fazer o snake draft
df = df.sort_values(by='Escore_PCA', ascending=False).reset_index(drop=True)

# === ANIMAÇÃO DO SNAKE DRAFT EM BARRAS ===
fig, ax = plt.subplots(figsize=(10, 6))

snake_pattern = [1, 2, 3, 3, 2, 1] 
alunos_names = [n.split()[0] for n in df['Nome Completo']] # Primeiro nome pra nao estourar a tela

# Simulador de historico limpo
historico_draft = []
capacidades = {1: 6, 2: 6, 3: 6}
tmp_grupos = {1: 0, 2: 0, 3: 0}
step = 0

for i in range(18):
    ideal_grupo = snake_pattern[step % len(snake_pattern)]
    while tmp_grupos[ideal_grupo] >= capacidades[ideal_grupo]:
        ideal_grupo = 1 if ideal_grupo == 3 else ideal_grupo + 1
        
    tmp_grupos[ideal_grupo] += 1
    step += 1
    historico_draft.append({'aluno': alunos_names[i], 'dest': ideal_grupo})

def init():
    ax.clear()
    ax.set_ylim(0, 8)
    ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], [0, 0, 0])
    return ax,

def update(frame):
    ax.clear()
    ax.set_ylim(0, 8)
    
    # Contagem no frame
    contagem = {1: 0, 2: 0, 3: 0}
    for i in range(frame): contagem[historico_draft[i]['dest']] += 1
        
    barras = ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], 
                     [contagem[1], contagem[2], contagem[3]], 
                     color=['teal', 'coral', 'indigo'])
                     
    ax.set_title(f'Sorteio Snake Draft | Alunos alocados: {frame}/18')
    ax.set_ylabel('Vagas Preenchidas')
    
    # Adicionar nome do ultimo listado
    if frame > 0:
        ultimo = historico_draft[frame-1]
        ax.text(ultimo['dest'] - 1, contagem[ultimo['dest']] + 0.2, 
                f"+ {ultimo['aluno']}", 
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkred')
                
    return barras,

anim = FuncAnimation(fig, update, frames=18+1, init_func=init, interval=400, blit=False)
anim.save("anim_m4.gif", writer='pillow', dpi=80)
print("Animação PCA Draft c/ nomes salva em: anim_m4.gif")

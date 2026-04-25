import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import random
from deap import base, creator, tools, algorithms

print("Executando Método 3: Otimização Genética\n")

file_path = "perfil_alunos.csv"
if not os.path.exists(file_path): file_path = "perfil_alunos"

df = pd.read_csv(file_path).dropna(subset=['Nome Completo']).copy().reset_index(drop=True)

N = len(df) # 18
CAPACIDADES = {1: 6, 2: 6, 3: 6}
features = ['Soft Skills - Comunicação', 'Soft Skills - Habilidade de escrita', 'Soft Skills - Liderança']
dados_matrix = df[features].values
medias_globais = dados_matrix.mean(axis=0)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()

def generate_individual():
    grupos = [1]*6 + [2]*6 + [3]*6
    random.shuffle(grupos)
    return grupos

toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalDistrib(individual):
    error, contagem, somas = 0, {1: 0, 2: 0, 3: 0}, {1: np.zeros(3), 2: np.zeros(3), 3: np.zeros(3)}
    for i, g in enumerate(individual):
        contagem[g] += 1
        somas[g] += dados_matrix[i]
        
    for g in [1, 2, 3]:
        if contagem[g] != CAPACIDADES[g]: error += 1000 * abs(contagem[g] - CAPACIDADES[g])

    mse = 0
    for g in [1, 2, 3]:
        if contagem[g] > 0:
            mse += np.sum((somas[g] / contagem[g] - medias_globais)**2)
            
    return (error + mse,)


toolbox.register("evaluate", evalDistrib)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=3, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

random.seed(42)
pop = toolbox.population(n=300)
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("min", np.min)
stats.register("avg", np.mean)

# === TREINAMENTO GENÉTICO SALVANDO O ESTADO ===
historico_genetico_bests = []
linhas_log = {'gen': [], 'min': [], 'avg': []}

for gen in range(80):
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=1, stats=stats, verbose=False)
    
    # Salva metricas pra plotagem estática de linha depois
    linhas_log['gen'].append(gen)
    linhas_log['min'].append(log[0]['min'])
    linhas_log['avg'].append(log[0]['avg'])
    
    best_ind = tools.selBest(pop, 1)[0]
    historico_genetico_bests.append(list(best_ind))

# Salvamos de vez o resultado do loop 80
df['Grupo_Final'] = historico_genetico_bests[-1]

ancoras = pd.DataFrame({'Nome Completo': ['Yuri', 'Gilbran', 'Eduardo'], 'Grupo_Final': [1, 2, 3]})
df_absoluto = pd.concat([df, ancoras], ignore_index=True)

print("\nGrupos formados (com cabeças):")
for g in [1, 2, 3]: print(f"Grupo {g}:", df_absoluto[df_absoluto['Grupo_Final'] == g]['Nome Completo'].tolist())

# Gráfico da curva estática
plt.figure(figsize=(10,5))
plt.plot(linhas_log['gen'], linhas_log['min'], label="Menor Erro", color='green', linewidth=2)
plt.plot(linhas_log['gen'], linhas_log['avg'], label="Erro Médio", color='red', linestyle='--')
plt.title("Convergência do DEAP (18 Estudantes avaliados)")
plt.legend()
plt.savefig("grafico_metodo_3_genetico.png", dpi=150)
plt.close()

# === ANIMAÇÃO DE PESSOAS PULANDO NAS BARRAS ===
fig, ax = plt.subplots(figsize=(12, 7))
nomes_curtos = [n.split()[0] for n in df['Nome Completo']] # So primeiro nome pra caber na tela

def update(frame):
    ax.clear()
    ax.set_ylim(0, 10)
    
    ind_atual = historico_genetico_bests[frame]
    
    contagem = {1: 0, 2: 0, 3: 0}
    nomes_nos_grupos = {1: [], 2: [], 3: []}
    
    for i, g_id in enumerate(ind_atual):
        contagem[g_id] += 1
        nomes_nos_grupos[g_id].append(nomes_curtos[i])
        
    ax.bar(['Grupo 1', 'Grupo 2', 'Grupo 3'], 
            [contagem[1], contagem[2], contagem[3]], 
            color=['#ff9999','#66b3ff','#99ff99'])
            
    ax.set_title(f'Competição Genética de Mutação\nApurando Melhor Cromossomo da Geração: {frame}/80', fontsize=14)
    ax.set_ylabel('Vagas Ocupadas por Mutação')
    
    # Escreve a arvore da lista de nomes DENTRO da barra!
    for g_id in [1, 2, 3]:
        texto_nomes = "\n".join(nomes_nos_grupos[g_id])
        ax.text(g_id - 1, contagem[g_id]/2, texto_nomes, 
                ha='center', va='center', fontsize=9, fontweight='bold', color='black')

    # Plota a meta de vagas (y=6)
    ax.axhline(y=6, color='red', linestyle='--', label="Alvo Ideal de Vagas")

    return ax,

# Animamos ate a geracao 80 com FPS bem rápido
anim = FuncAnimation(fig, update, frames=80, interval=100, blit=False)
anim.save("anim_m3.gif", writer='pillow', dpi=80)
print("Animação genética das pessoas pulando de grupos salva em: anim_m3.gif")

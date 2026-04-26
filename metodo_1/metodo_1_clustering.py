import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib.animation import FuncAnimation


def encontrar_arquivo_csv():
    """Retorna o caminho para o arquivo CSV de perfil de alunos."""
    return "../perfil_alunos.csv"


def carregar_dados(file_path):
    """Carrega os dados dos alunos do CSV."""
    df_alunos = pd.read_csv(file_path).dropna(subset=["Nome Completo"]).copy()
    
    features = [
        "Soft Skills - Comunicação",
        "Soft Skills - Habilidade de escrita",
        "Soft Skills - Liderança",
    ]
    
    return df_alunos, features


def definir_cabecas_chave():
    """Define os cabeças-de-chave dos grupos."""
    return [
        {"Nome Completo": "Yuri", "is_cabeca_chave": True},
        {"Nome Completo": "Gilbran", "is_cabeca_chave": True},
        {"Nome Completo": "Eduardo", "is_cabeca_chave": True},
    ]


def exibir_info_inicial(df_alunos, cabecas_chave):
    """Exibe informações iniciais sobre os dados."""
    num_grupos = 3
    total_alunos = len(df_alunos) + len(cabecas_chave)
    
    print("Executando Método 1: Clustering K-Means e Amostragem Estratificada\n")
    print(f"Cabeças-de-chave (hardcoded): {len(cabecas_chave)}")
    print(f"Alunos no CSV: {len(df_alunos)}")
    print(f"Total: {total_alunos}\n")
    
    return num_grupos, total_alunos


def aplicar_kmeans(df_alunos, features, num_grupos):
    """Aplica o algoritmo K-Means aos dados dos alunos.
    
    Esta função executa o clustering K-Means para agrupar alunos com base em
    suas soft skills. Os dados são normalizados (StandardScaler) antes do clustering
    para garantir que todas as features tenham o mesmo peso.
    
    Processo:
    ---------
    1. Normaliza os dados usando StandardScaler (média=0, desvio padrão=1)
    2. Aplica K-Means com k clusters
    3. Atribui cada aluno ao cluster mais próximo
    4. Calcula os centróides na escala original para interpretação
    
    Retorna:
    --------
    tuple[pd.DataFrame, StandardScaler, KMeans, np.ndarray]
        - df_alunos: DataFrame atualizado com nova coluna "Cluster" (valores: 0, 1, 2)
        - scaler: objeto StandardScaler treinado (para possível uso futuro)
        - kmeans: objeto KMeans treinado com os parâmetros do modelo
        - centroides_original: array numpy (shape: [n_clusters, n_features]) com
          centróides na escala original (1-4). Exemplo:
          [[2.5, 3.0, 2.8],   # Centróide do Cluster 0
           [3.2, 2.5, 3.5],   # Centróide do Cluster 1
           [1.8, 2.0, 2.2]]   # Centróide do Cluster 2
    
    Detalhes do K-Means:
    -------------------
    - O algoritmo minimiza a distância euclidiana entre pontos e centróides
    
    Exemplo de uso:
    --------------
    df_alunos, scaler, kmeans, centroides = aplicar_kmeans(df, features, 3)
    print(df_alunos["Cluster"].value_counts())  # Contagem de alunos por cluster
    print(centroides)  # Ver posição dos centróides
    """
    scaler = StandardScaler()
    X = scaler.fit_transform(df_alunos[features])
    
    kmeans = KMeans(n_clusters=num_grupos, random_state=42, n_init="auto")
    df_alunos["Cluster"] = kmeans.fit_predict(X)
    
    centroides = kmeans.cluster_centers_
    centroides_original = scaler.inverse_transform(centroides)
    
    return df_alunos, scaler, kmeans, centroides_original


def analisar_duplicatas(df_alunos, features):
    """Analisa e conta coordenadas duplicadas nos dados."""
    coordenadas = [
        tuple(df_alunos.loc[i, features].values) for i in df_alunos.index
    ]
    contador_coords = Counter(coordenadas)
    
    return contador_coords

def exibir_analise_duplicatas(df_alunos, contador_coords, features):
    """Exibe análise detalhada de duplicatas e clustering."""
    print("\nAnálise de duplicatas e Clustering:")
    print(f"Total de alunos: {len(df_alunos)}")
    print(f"Coordenadas únicas: {len(contador_coords)}")
    print("\nPontos com múltiplos alunos:")
    
    for coord, count in sorted(contador_coords.items(), key=lambda x: x[1], reverse=True):
        if count > 1:
            alunos_nessa_coord = df_alunos[
                (df_alunos[features[0]] == coord[0]) &
                (df_alunos[features[1]] == coord[1]) &
                (df_alunos[features[2]] == coord[2])
            ]
            nomes = alunos_nessa_coord["Nome Completo"].tolist()
            clusters_desses_alunos = alunos_nessa_coord["Cluster"].tolist()
            
            clusters_unicos = set(clusters_desses_alunos)
            
            print(f"  {coord}: {count} alunos - {', '.join([n.split()[0] for n in nomes])}")
            if len(clusters_unicos) == 1:
                print(f"    OK: Todos no Cluster {list(clusters_unicos)[0]} (como esperado!)")
            else:
                print(f"    ATENCAO: Distribuídos em clusters diferentes: {clusters_unicos}")
                
    print("\nIMPORTANTE: Alunos com coordenadas idênticas SEMPRE vão para o mesmo cluster!")
    print("   O K-Means calcula distâncias - se as coordenadas são iguais, a distância")
    print("   para os centróides é a mesma, logo o cluster atribuído é o mesmo.")


def exibir_analise_distancias(df_alunos, centroides_original, features):
    """Exibe análise detalhada de distâncias até os centróides."""
    print(f"\n\n{'='*80}")
    print("ANALISE DETALHADA: DISTANCIA DE CADA ALUNO ATE OS CENTROIDES")
    print(f"{'='*80}\n")

    print("Centróides (escala original):")
    for i, centroide in enumerate(centroides_original):
        print(f"  Centróide {i}: Comunicação={centroide[0]:.2f}, Escrita={centroide[1]:.2f}, Liderança={centroide[2]:.2f}")

    print(f"\n{'─'*80}")

    for idx, aluno in df_alunos.iterrows():
        nome = aluno["Nome Completo"]
        coord = (aluno[features[0]], aluno[features[1]], aluno[features[2]])
        cluster_atribuido = aluno["Cluster"]
        
        distancias = []
        for i, centroide in enumerate(centroides_original):
            dist = euclidean(coord, centroide)
            distancias.append((i, dist))
        
        distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
        
        print(f"\nAluno: {nome}")
        print(f"   Coordenadas: Comunicação={coord[0]}, Escrita={coord[1]}, Liderança={coord[2]}")
        print("   Distâncias até os centróides:")
        
        for cluster_id, dist in distancias_ordenadas:
            marcador = "OK - ESCOLHIDO" if cluster_id == cluster_atribuido else ""
            print(f"      -> Centróide {cluster_id}: {dist:.4f} {marcador}")
        
        dist_mais_proximo = distancias_ordenadas[0][1]
        print(f"   -> Atribuído ao Cluster {cluster_atribuido} (menor distância = {dist_mais_proximo:.4f})")

    print(f"\n{'='*80}")
    print("IMPORTANTE: O K-Means escolhe SEMPRE o centróide mais próximo (menor distância euclidiana)")
    print(f"{'='*80}\n")


def adicionar_jitter(df_alunos, features, seed=42, jitter_amount=0.08):
    """Adiciona jitter (ruído aleatório) para melhorar visualização."""
    np.random.seed(seed)
    
    df_alunos["Comunicação_jitter"] = df_alunos[features[0]] + np.random.uniform(-jitter_amount, jitter_amount, len(df_alunos))
    df_alunos["Escrita_jitter"] = df_alunos[features[1]] + np.random.uniform(-jitter_amount, jitter_amount, len(df_alunos))
    df_alunos["Liderança_jitter"] = df_alunos[features[2]] + np.random.uniform(-jitter_amount, jitter_amount, len(df_alunos))
    
    return df_alunos


def criar_grafico_3d(df_alunos, centroides_original, contador_coords, num_grupos):
    """Cria e salva gráfico 3D dos clusters."""
    cores_clusters = ["#e74c3c", "#3498db", "#2ecc71"]
    
    fig3d = plt.figure(figsize=(14, 10))
    ax3d = fig3d.add_subplot(111, projection="3d")

    for cluster_id in range(num_grupos):
        cluster_data = df_alunos[df_alunos["Cluster"] == cluster_id]
        
        ax3d.scatter(
            cluster_data["Comunicação_jitter"],
            cluster_data["Escrita_jitter"],
            cluster_data["Liderança_jitter"],
            c=cores_clusters[cluster_id],
            s=150,
            alpha=0.8,
            edgecolors="black",
            linewidths=1.5,
            label=f"Cluster {cluster_id} ({len(cluster_data)} alunos)",
        )

    for i, centroide in enumerate(centroides_original):
        ax3d.scatter(
            centroide[0],
            centroide[1],
            centroide[2],
            c=cores_clusters[i],
            marker="X",
            s=600,
            edgecolors="black",
            linewidths=3,
            label=f"Centróide {i}",
            zorder=10,
        )
        ax3d.plot(
            [centroide[0], centroide[0]],
            [centroide[1], centroide[1]],
            [0, centroide[2]],
            color=cores_clusters[i],
            linestyle="--",
            alpha=0.3,
            linewidth=2,
        )

    ax3d.set_xlabel("Comunicação (1-4)", fontsize=12, fontweight="bold")
    ax3d.set_ylabel("Habilidade de Escrita (1-4)", fontsize=12, fontweight="bold")
    ax3d.set_zlabel("Liderança (1-4)", fontsize=12, fontweight="bold")
    ax3d.set_title(
        f"Método 1: K-Means Clustering (k={num_grupos})\n"
        f"{len(df_alunos)} Alunos agrupados por Soft Skills\n"
        f"Centróides marcados com X | Jitter aplicado para visualização",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    ax3d.grid(True, alpha=0.3)
    ax3d.legend(loc="upper left", fontsize=10, framealpha=0.9)

    info_text = (
        f"NOTA: {len(contador_coords)} coordenadas únicas de {len(df_alunos)} alunos\n"
        f"Pequeno ruído (jitter) adicionado para separar pontos sobrepostos visualmente\n"
        f"Muitos alunos têm respostas idênticas nas 3 dimensões"
    )
    fig3d.text(
        0.5,
        0.02,
        info_text,
        ha="center",
        fontsize=10,
        style="italic",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    ax3d.view_init(elev=20, azim=45)

    plt.tight_layout()
    plt.savefig("grafico_metodo_1_clusters.png", dpi=150, bbox_inches="tight")
    plt.close(fig3d)


def criar_graficos_2d(df_alunos, centroides_original, contador_coords, num_grupos):
    """Cria e salva gráficos 2D (projeções) dos clusters."""
    cores_clusters = ["#e74c3c", "#3498db", "#2ecc71"]
    
    fig2d, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Comunicação vs Escrita
    for cluster_id in range(num_grupos):
        cluster_data = df_alunos[df_alunos["Cluster"] == cluster_id]
        axes[0].scatter(
            cluster_data["Comunicação_jitter"],
            cluster_data["Escrita_jitter"],
            c=cores_clusters[cluster_id],
            s=120,
            alpha=0.7,
            edgecolors="black",
            linewidths=1.5,
            label=f"Cluster {cluster_id}",
        )
        axes[0].scatter(
            centroides_original[cluster_id, 0],
            centroides_original[cluster_id, 1],
            c=cores_clusters[cluster_id],
            marker="X",
            s=400,
            edgecolors="black",
            linewidths=2,
        )
    axes[0].set_xlabel("Comunicação", fontweight="bold")
    axes[0].set_ylabel("Habilidade de Escrita", fontweight="bold")
    axes[0].set_title("Comunicação vs Escrita", fontweight="bold")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Comunicação vs Liderança
    for cluster_id in range(num_grupos):
        cluster_data = df_alunos[df_alunos["Cluster"] == cluster_id]
        axes[1].scatter(
            cluster_data["Comunicação_jitter"],
            cluster_data["Liderança_jitter"],
            c=cores_clusters[cluster_id],
            s=120,
            alpha=0.7,
            edgecolors="black",
            linewidths=1.5,
            label=f"Cluster {cluster_id}",
        )
        axes[1].scatter(
            centroides_original[cluster_id, 0],
            centroides_original[cluster_id, 2],
            c=cores_clusters[cluster_id],
            marker="X",
            s=400,
            edgecolors="black",
            linewidths=2,
        )
    axes[1].set_xlabel("Comunicação", fontweight="bold")
    axes[1].set_ylabel("Liderança", fontweight="bold")
    axes[1].set_title("Comunicação vs Liderança", fontweight="bold")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Escrita vs Liderança
    for cluster_id in range(num_grupos):
        cluster_data = df_alunos[df_alunos["Cluster"] == cluster_id]
        axes[2].scatter(
            cluster_data["Escrita_jitter"],
            cluster_data["Liderança_jitter"],
            c=cores_clusters[cluster_id],
            s=120,
            alpha=0.7,
            edgecolors="black",
            linewidths=1.5,
            label=f"Cluster {cluster_id}",
        )
        axes[2].scatter(
            centroides_original[cluster_id, 1],
            centroides_original[cluster_id, 2],
            c=cores_clusters[cluster_id],
            marker="X",
            s=400,
            edgecolors="black",
            linewidths=2,
        )
    axes[2].set_xlabel("Habilidade de Escrita", fontweight="bold")
    axes[2].set_ylabel("Liderança", fontweight="bold")
    axes[2].set_title("Escrita vs Liderança", fontweight="bold")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    fig2d.suptitle(
        f"Método 1: Projeções 2D dos Clusters K-Means (X = Centróide)\n"
        f"{len(contador_coords)} coordenadas únicas | Jitter aplicado para visualização",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig("grafico_metodo_1_clusters_2d.png", dpi=150, bbox_inches="tight")
    plt.close(fig2d)


def calcular_capacidades(total_alunos, num_grupos):
    """Calcula dinamicamente a capacidade de cada grupo."""
    capacidade_base = total_alunos // num_grupos
    extras = total_alunos % num_grupos
    
    capacidades = {}
    for i in range(1, num_grupos + 1):
        capacidades[i] = capacidade_base + (1 if i <= extras else 0)
    
    print(f"Capacidades dos grupos: {capacidades}\n")
    return capacidades


def alocar_cabecas_chave(cabecas_chave, num_grupos):
    """Aloca cabeças-de-chave aleatoriamente aos grupos."""
    grupos = {i: [] for i in range(1, num_grupos + 1)}
    grupos_disponiveis = list(range(1, num_grupos + 1))
    random.shuffle(grupos_disponiveis)
    
    historico_alocacao = []
    
    for idx, cabeca in enumerate(cabecas_chave):
        grupo_destino = grupos_disponiveis[idx]
        grupos[grupo_destino].append(cabeca)
        
        historico_alocacao.append({
            "nome": cabeca["Nome Completo"],
            "cluster_color": -1,
            "grupo_destino": grupo_destino,
            "is_cabeca": True,
        })
        print(f"OK: {cabeca['Nome Completo']} -> Grupo {grupo_destino} (cabeça-de-chave)")
    
    print()
    return grupos, historico_alocacao


def distribuir_alunos(df_alunos, grupos, capacidades, num_grupos, historico_alocacao):
    """Distribui alunos do CSV maximizando diversidade entre os grupos.
    
    Esta função implementa uma estratégia de distribuição round-robin que maximiza
    a diversidade, distribuindo cada cluster proporcionalmente entre todos os grupos.
    
    IMPORTANTE: Não garante que todos os grupos tenham alunos de todos os clusters,
    pois isso depende do tamanho de cada cluster. Se um cluster tem menos alunos
    que o número de grupos, alguns grupos não receberão alunos daquele cluster.
    
    Algoritmo:
    - Para cada cluster (0, 1, 2), processa seus alunos sequencialmente
    - Distribui os alunos de cada cluster de forma circular entre todos os grupos
    - Começa sempre do grupo 1 e avança em round-robin (1 -> 2 -> 3 -> 1 -> ...)
    - Respeita a capacidade máxima de cada grupo
    - Se um grupo está cheio, pula para o próximo automaticamente
    
    Exemplo:
    - Cluster com 6 alunos e 3 grupos: cada grupo recebe 2 alunos
    - Cluster com 1 aluno e 3 grupos: apenas 1 grupo recebe, outros 2 ficam sem 
    """
    num_clusters = df_alunos["Cluster"].nunique()
    
    for cluster_id in range(num_clusters):
        alunos_no_cluster = df_alunos[df_alunos["Cluster"] == cluster_id].to_dict("records")
        
        grupo_atual = 1
        
        for aluno in alunos_no_cluster:
            tentativas = 0
            while len(grupos[grupo_atual]) >= capacidades[grupo_atual]:
                grupo_atual = grupo_atual % num_grupos + 1
                tentativas += 1
                if tentativas > num_grupos:
                    break
            
            if tentativas <= num_grupos:
                grupos[grupo_atual].append(aluno)

                historico_alocacao.append({
                    "nome": aluno["Nome Completo"],
                    "cluster_color": cluster_id,
                    "grupo_destino": grupo_atual,
                    "is_cabeca": False,
                })

                grupo_atual = grupo_atual % num_grupos + 1
    
    return grupos, historico_alocacao


def exibir_composicao_grupos(grupos):
    """Exibe a composição final dos grupos."""
    print("\n=== COMPOSICAO FINAL DOS GRUPOS ===")
    for g_id, membros in grupos.items():
        print(f"\nGrupo {g_id} ({len(membros)} alunos):")
        for membro in membros:
            marcador = "CABECA" if membro.get("is_cabeca_chave", False) else "-"
            print(f"  {marcador} {membro['Nome Completo']}")


def criar_animacao_alocacao(historico_alocacao, capacidades, total_alunos):
    """Cria animação de alocação dos alunos aos grupos."""
    fig, ax = plt.subplots(figsize=(10, 6))

    def init():
        ax.clear()
        ax.set_ylim(0, max(capacidades.values()) + 2)
        ax.bar(["Grupo 1", "Grupo 2", "Grupo 3"], [0, 0, 0])
        return (ax,)

    def update(frame):
        ax.clear()
        ax.set_ylim(0, max(capacidades.values()) + 2)
        ax.set_title(f"Alocando alunos nos grupos: {frame}/{total_alunos}")
        ax.set_ylabel("Vagas Preenchidas")

        contagem = {1: 0, 2: 0, 3: 0}

        for i in range(frame):
            g_dest = historico_alocacao[i]["grupo_destino"]
            contagem[g_dest] += 1

        barras = ax.bar(
            ["Grupo 1", "Grupo 2", "Grupo 3"],
            [contagem[1], contagem[2], contagem[3]],
            color=["#1f77b4", "#ff7f0e", "#2ca02c"],
        )

        for i, cap in capacidades.items():
            ax.axhline(y=cap, color="red", linestyle="--", alpha=0.3, linewidth=1)

        if frame > 0:
            ultimo = historico_alocacao[frame - 1]
            nome = ultimo["nome"].split()[0]
            g_id = ultimo["grupo_destino"]
            altura = contagem[g_id]
            
            if ultimo["is_cabeca"]:
                label = f"CABECA: {nome}\n(Cabeça-de-chave)"
                cor = "darkred"
            else:
                label = f"+ {nome}\n(Cluster {ultimo['cluster_color']})"
                cor = "purple"
            
            ax.text(
                g_id - 1,
                altura + 0.2,
                label,
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=cor,
            )

        return (barras,)

    anim = FuncAnimation(
        fig, update, frames=total_alunos + 1, init_func=init, interval=400, blit=False
    )
    anim.save("anim_m1.gif", writer="pillow", dpi=80)
    plt.close(fig)


def main():
    """Função principal que executa todo o pipeline."""
    # Carregar dados
    file_path = encontrar_arquivo_csv()
    df_alunos, features = carregar_dados(file_path)
    
    # Definir cabeças-de-chave
    cabecas_chave = definir_cabecas_chave()
    
    # Exibir informações iniciais
    num_grupos, total_alunos = exibir_info_inicial(df_alunos, cabecas_chave)
    
    # Aplicar K-Means
    df_alunos, scaler, kmeans, centroides_original = aplicar_kmeans(df_alunos, features, num_grupos)
    
    # Analisar duplicatas
    contador_coords = analisar_duplicatas(df_alunos, features)
    
    # Exibir análises
    exibir_analise_duplicatas(df_alunos, contador_coords, features)
    exibir_analise_distancias(df_alunos, centroides_original, features)
    
    # Adicionar jitter para visualização
    df_alunos = adicionar_jitter(df_alunos, features)
    
    # Criar gráficos
    criar_grafico_3d(df_alunos, centroides_original, contador_coords, num_grupos)
    criar_graficos_2d(df_alunos, centroides_original, contador_coords, num_grupos)
    
    # Calcular capacidades dos grupos
    capacidades = calcular_capacidades(total_alunos, num_grupos)
    
    # Alocar cabeças-de-chave
    grupos, historico_alocacao = alocar_cabecas_chave(cabecas_chave, num_grupos)
    
    # Distribuir alunos
    grupos, historico_alocacao = distribuir_alunos(df_alunos, grupos, capacidades, num_grupos, historico_alocacao)
    
    # Exibir composição final
    exibir_composicao_grupos(grupos)
    
    # Criar animação
    criar_animacao_alocacao(historico_alocacao, capacidades, total_alunos)
    
    print("\nOK: Animação interativa de alocação salva em: anim_m1.gif")
    print("OK: Gráfico 3D salvo em: grafico_metodo_1_clusters.png")
    print("OK: Gráfico 2D (projeções) salvo em: grafico_metodo_1_clusters_2d.png")


if __name__ == "__main__":
    main()


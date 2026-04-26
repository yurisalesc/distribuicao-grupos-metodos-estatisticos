# Método 1: Clustering K-Means com Amostragem Estratificada

## Índice
1. [Visão Geral](#visão-geral)
2. [Conceitos Fundamentais](#conceitos-fundamentais)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Fluxo de Execução](#fluxo-de-execução)
5. [Detalhamento Técnico](#detalhamento-técnico)
6. [Questões Frequentes](#questões-frequentes)
7. [Limitações e Considerações](#limitações-e-considerações)

---

## Visão Geral

### Objetivo
Distribuir alunos em **3 grupos balanceados** com base em suas **soft skills** (Comunicação, Escrita, Liderança), garantindo que:
- Cada grupo tenha número igual ou quase igual de membros
- Cada grupo tenha um **cabeça-de-chave** pré-definido (Yuri, Gilbran ou Eduardo)
- Os grupos sejam **heterogêneos**, com **máxima diversidade de perfis**
- **Maximizar** a representação de todos os clusters em cada grupo (limitado pela distribuição natural dos dados)

### Abordagem em Duas Fases
1. **Fase 1 - Clustering (Identificação de Estratos)**: Agrupar alunos com perfis similares usando K-Means
2. **Fase 2 - Amostragem Estratificada (Distribuição com Diversidade)**: Distribuir proporcionalmente cada cluster entre todos os grupos, garantindo representação balanceada

---

## Conceitos Fundamentais

### 1. K-Means Clustering

#### O Que É
K-Means é um algoritmo de **aprendizado não supervisionado** que divide um conjunto de dados em **k clusters** (grupos), onde cada ponto pertence ao cluster cujo centróide está mais próximo.

#### Como Funciona

**Algoritmo de Lloyd (EM - Expectation-Maximization):**

```
1. INICIALIZAÇÃO
   - Escolhe k pontos aleatórios como centróides iniciais
   - Usa K-Means++ (padrão do scikit-learn) para melhor distribuição

2. REPETIR ATÉ CONVERGÊNCIA:
   
   a) E-step (Expectation/Atribuição):
      Para cada aluno:
         - Calcula distância euclidiana até cada centróide
         - Atribui ao cluster do centróide mais próximo
   
   b) M-step (Maximization/Atualização):
      Para cada cluster:
         - Recalcula centróide como média de todos os pontos do cluster
   
3. CRITÉRIO DE PARADA:
   - Centróides param de se mover (diferença < threshold)
   - OU atinge número máximo de iterações (padrão: 300)
```

**Fórmula da Distância Euclidiana:**
```
d(aluno, centróide) = √[(x₁-c₁)² + (x₂-c₂)² + (x₃-c₃)²]

Onde:
  (x₁, x₂, x₃) = coordenadas do aluno (Comunicação, Escrita, Liderança)
  (c₁, c₂, c₃) = coordenadas do centróide
```

#### Por Que k=3?
No código atual, **k = número de grupos finais = 3**. Usar k=3 significa que o K-Means já cria os 3 perfis de alunos que depois serão distribuídos nos grupos.

### 2. Padronização (StandardScaler)

#### Por Que É Necessário?

Mesmo que todas as features estejam na mesma escala Likert (1-4), a padronização é importante porque:

1. **Médias diferentes**: Se todos avaliaram alto em "Comunicação" (média 3.5) mas variaram em "Liderança" (média 2.0), sem padronização a feature com maior variância dominaria o clustering.

2. **Variâncias diferentes**: Uma feature com maior espalhamento teria peso maior no cálculo de distâncias.

3. **K-Means usa distância euclidiana**: O algoritmo é sensível a escalas, mesmo que nominalmente iguais.

#### O Que Faz

**Fórmula:**
```
z = (x - μ) / σ

Onde:
  x = valor original
  μ = média da feature
  σ = desvio padrão da feature
```

**Resultado**: Todas as features ficam com média = 0 e desvio padrão = 1.

**Exemplo:**
```
Comunicação original: [2, 3, 3, 4]
Média = 3.0, Desvio = 0.816

Padronizado: [-1.22, 0, 0, 1.22]
```

#### fit_transform vs transform

- **fit_transform()**: Calcula estatísticas (média, desvio) E aplica transformação
  - Use apenas nos dados de treino (nosso caso: todos os alunos do CSV)

- **transform()**: Apenas aplica transformação usando estatísticas já calculadas
  - Use em dados novos (ex: se chegarem alunos adicionais depois)

**IMPORTANTE**: Sempre use as mesmas estatísticas para garantir comparabilidade!

### 3. Centróides

#### Definição
Um **centróide** é o ponto central de um cluster, calculado como a **média aritmética** de todos os pontos (alunos) que pertencem àquele cluster.

**Fórmula:**
```
Para cluster com n alunos:

centróide = (
    (x₁ + x₂ + ... + xₙ) / n,
    (y₁ + y₂ + ... + yₙ) / n,
    (z₁ + z₂ + ... + zₙ) / n
)
```

**Exemplo Real do Dataset:**
```
Centróide 0: (2.83, 2.00, 2.83)
  → Perfil "Comunicativo-Prático": Boa comunicação, escrita mais baixa

Centróide 1: (3.00, 3.27, 3.00)
  → Perfil "Equilibrado": Pontuações médias-altas em todas

Centróide 2: (3.00, 4.00, 1.00)
  → Perfil "Escritor-Técnico": Excelente escrita, liderança baixa
```

#### Interpretação
- Centróides representam o "aluno médio" de cada perfil
- Quanto mais próximo um aluno está de um centróide, mais típico ele é daquele perfil
- Centróides são recalculados a cada iteração do K-Means

### 4. Problema das Coordenadas Duplicadas

#### O Fenômeno
Com escalas Likert de apenas 4 valores (1-4) e 3 dimensões, o número de combinações únicas possíveis é:
```
4 × 4 × 4 = 64 combinações possíveis
```

No dataset real de 18 alunos, temos apenas **11 coordenadas únicas**, ou seja:
- **7 alunos (39%)** têm coordenadas duplicadas
- O ponto (3,2,3) contém **5 alunos** (28% do total!)

#### Implicação para K-Means

**Regra Fundamental:**
> Alunos com coordenadas idênticas SEMPRE vão para o mesmo cluster, pois:
> - Mesmas coordenadas → Mesmas distâncias a todos centróides
> - Mesmas distâncias → Mesmo centróide mais próximo
> - Mesmo centróide → Mesmo cluster atribuído

**Exemplo:**
```
Tobias:   (3, 2, 3) → dist. Centróide 0: 0.2357 ✓
Ana:      (3, 2, 3) → dist. Centróide 0: 0.2357 ✓
Luiz:     (3, 2, 3) → dist. Centróide 0: 0.2357 ✓
Bruno:    (3, 2, 3) → dist. Centróide 0: 0.2357 ✓
Nalberth: (3, 2, 3) → dist. Centróide 0: 0.2357 ✓

Todos no Cluster 0!
```

#### Por Que Clusters Ficam Desbalanceados?

O K-Means "vê" apenas **11 posições únicas** no espaço, mas algumas têm "peso" (número de alunos) diferente:
- 7 posições com 1 aluno cada
- 3 posições com 2 alunos cada
- 1 posição com 5 alunos

Resultado: **Clusters com 6, 11 e 1 alunos** (desbalanceado por natureza dos dados)

#### Solução: Jitter para Visualização

Para tornar visíveis todos os 18 pontos no gráfico (não apenas 11), aplicamos **jitter** (ruído aleatório pequeno):

```python
jitter_amount = 0.08
coord_visualização = coord_real + random.uniform(-0.08, +0.08)
```

**IMPORTANTE**: Jitter é aplicado **APÓS** o clustering, apenas para visualização. Não afeta o algoritmo.

### 5. Amostragem Estratificada: Maximização da Diversidade

#### Conceito Estatístico

**Amostragem Estratificada** é uma técnica estatística onde a população é dividida em **estratos** (subgrupos homogêneos) e cada estrato é **representado proporcionalmente** em cada amostra final.

**IMPORTANTE - Garantia vs. Maximização:**
- ✅ **GARANTE:** Distribuição proporcional de cada cluster entre os grupos
- ✅ **GARANTE:** Se cluster tem n ≥ k alunos, todos os grupos receberão alunos daquele cluster
- ⚠️ **NÃO GARANTE:** Que todos os grupos terão alunos de todos os clusters (depende do tamanho dos clusters)
- ✅ **MAXIMIZA:** A diversidade dentro das restrições matemáticas dos dados

**Aplicação no Método:**
- **Estratos** = Clusters K-Means (perfis comportamentais)
- **Amostras** = Grupos finais de trabalho
- **Objetivo** = Maximizar a diversidade distribuindo cada estrato proporcionalmente entre os grupos

#### Fundamentação Matemática

**Índice de Diversidade (Shannon):**
```
H = -Σ pᵢ × log(pᵢ)

Onde:
  pᵢ = proporção de alunos do cluster i no grupo
  H = máximo quando todos os clusters têm proporção similar
```

**Variância Inter-Grupos vs Intra-Grupos:**
```
Objetivo: Maximizar heterogeneidade entre membros de um grupo
         Minimizar similaridade dentro de cada grupo final

SST = SSB + SSW
  SST = Soma total dos quadrados
  SSB = Between-group (queremos minimizar)
  SSW = Within-group (queremos maximizar)
```

#### Implementação: Distribuição Balanceada por Cluster

**Estratégia:**
```
Para cada cluster C (0, 1, 2):
    grupo_atual = 1  # Reinicia para cada cluster!
    
    Para cada aluno A em C:
        Enquanto grupo_atual está cheio:
            grupo_atual = (grupo_atual % num_grupos) + 1
        
        Adiciona A ao grupo_atual
        grupo_atual = (grupo_atual % num_grupos) + 1
```

**Diferença Crítica da Abordagem Antiga:**
```
❌ ABORDAGEM ANTIGA (Round-Robin Global):
   grupo_atual = 1
   Para todos os alunos em sequência:
       Aloca no grupo_atual
   
   Problema: Clusters grandes podem se concentrar em poucos grupos

✅ ABORDAGEM NOVA (Round-Robin Por Cluster):
   Para cada cluster:
       grupo_atual = 1  # REINICIA!
       Distribui alunos desse cluster entre TODOS os grupos
   
   Garantia: Cada cluster é espalhado proporcionalmente
```

#### Exemplo Numérico

**Cenário:**
- Cluster 0: 6 alunos
- Cluster 1: 11 alunos  
- Cluster 2: 1 aluno
- 3 grupos finais

**Distribuição Garantida:**
```
Cluster 0 (6 alunos):
  Aluno 1 → Grupo 1
  Aluno 2 → Grupo 2
  Aluno 3 → Grupo 3
  Aluno 4 → Grupo 1  ← Volta!
  Aluno 5 → Grupo 2
  Aluno 6 → Grupo 3
  Resultado: 2 em cada grupo ✅

Cluster 1 (11 alunos):
  Alunos 1-3 → Grupos 1, 2, 3
  Alunos 4-6 → Grupos 1, 2, 3
  Alunos 7-9 → Grupos 1, 2, 3
  Alunos 10-11 → Grupos 1, 2
  Resultado: 4, 4, 3 (máximo balanceamento!) ✅

Cluster 2 (1 aluno):
  Aluno 1 → Grupo 1
  Resultado: 1, 0, 0 (impossível dividir 1 em 3!) ⚠️
```

**Matriz de Diversidade Resultante:**
```
           Grupo 1  Grupo 2  Grupo 3  Total
Cluster 0      2        2        2       6
Cluster 1      4        4        3      11  
Cluster 2      1        0        0       1
─────────────────────────────────────────────
Total          7        6        5      18

Índice de Diversidade (clusters representados / total de clusters):
  Grupo 1: 3/3 clusters (100%) ✅
  Grupo 2: 2/3 clusters (67%)  ⚠️
  Grupo 3: 2/3 clusters (67%)  ⚠️

CONCLUSÃO: Cluster 2 tem apenas 1 aluno - matematicamente impossível
distribuir entre 3 grupos. Algoritmo maximiza diversidade dentro das
restrições naturais dos dados.
```

#### Por Que Não Zig-Zag?

**Zig-Zag (Snake Draft):**
```
1 → 2 → 3 → 3 → 2 → 1 → 1 → 2 → 3 ...
```

Útil quando há **ordem de prioridade/força**, como em drafts esportivos.

**No nosso caso:**
- Não há hierarquia entre perfis
- Queremos **dispersão uniforme** de cada estrato
- Round-robin por cluster é estatisticamente superior para diversidade

---

## Fluxo de Execução

### 1. Inicialização

```python
# Carregar dados
df_alunos = pd.read_csv("perfil_alunos")  # 18 alunos

# Definir cabeças-de-chave (hardcoded)
cabecas_chave = [
    {"Nome Completo": "Yuri", "is_cabeca_chave": True},
    {"Nome Completo": "Gilbran", "is_cabeca_chave": True},
    {"Nome Completo": "Eduardo", "is_cabeca_chave": True}
]

# Features para clustering
features = [
    "Soft Skills - Comunicação",
    "Soft Skills - Habilidade de escrita",
    "Soft Skills - Liderança"
]
```

### 2. Clustering (Fase 1)

```python
distribuidor = ClusteringDistribuidor(df_alunos, features, num_grupos=3)

# Passo 1: Padronizar features
X = StandardScaler().fit_transform(df_alunos[features])

# Passo 2: Aplicar K-Means (k=3)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Passo 3: Obter centróides na escala original
centroides_padronizados = kmeans.cluster_centers_
centroides_original = scaler.inverse_transform(centroides_padronizados)
```

**Resultado:** Cada aluno recebe um label de cluster (0, 1 ou 2)

### 3. Cálculo de Capacidades

```python
total_alunos = 18 (CSV) + 3 (cabeças) = 21

capacidade_base = 21 // 3 = 7
extras = 21 % 3 = 0

capacidades = {1: 7, 2: 7, 3: 7}
```

**Lógica Geral:**
```python
# Para qualquer número de alunos
capacidade_base = total_alunos // num_grupos
extras = total_alunos % num_grupos

# Distribui os "extras" nos primeiros grupos
for i in range(1, num_grupos + 1):
    capacidades[i] = capacidade_base + (1 if i <= extras else 0)
```

**Exemplos:**
- 20 alunos → {1: 7, 2: 7, 3: 6}
- 22 alunos → {1: 8, 2: 7, 3: 7}
- 23 alunos → {1: 8, 2: 8, 3: 7}

### 4. Distribuição (Fase 2)

#### Passo 4.1: Alocar Cabeças-de-Chave

```python
grupos_disponiveis = [1, 2, 3]
random.shuffle(grupos_disponiveis)  # Ex: [3, 1, 2]

Yuri    → Grupo 3
Gilbran → Grupo 1
Eduardo → Grupo 2

# Estado após cabeças:
Grupo 1: [Gilbran]    # 1 aluno
Grupo 2: [Eduardo]    # 1 aluno
Grupo 3: [Yuri]       # 1 aluno
```

#### Passo 4.2: Distribuir Cluster 0 (6 alunos) com Round-Robin

**IMPORTANTE:** Round-robin **reinicia do Grupo 1** para cada cluster!

```
grupo_atual = 1 (REINICIA para Cluster 0)

Tobias   → Grupo 1 (2) → grupo_atual = 2
Ana      → Grupo 2 (2) → grupo_atual = 3
Luiz     → Grupo 3 (2) → grupo_atual = 1 (voltou!)
Bruno    → Grupo 1 (3) → grupo_atual = 2
Nalberth → Grupo 2 (3) → grupo_atual = 3
Aldo     → Grupo 3 (3) → grupo_atual = 1

Resultado: 2 alunos do Cluster 0 em cada grupo ✅
```

#### Passo 4.3: Distribuir Cluster 1 (11 alunos) com Round-Robin

```
grupo_atual = 1 (REINICIA para Cluster 1)

Rafael   → Grupo 1 (4) → grupo_atual = 2
Anne     → Grupo 2 (4) → grupo_atual = 3
Talita   → Grupo 3 (4) → grupo_atual = 1 (voltou!)
Pedro    → Grupo 1 (5) → grupo_atual = 2
Fermanda → Grupo 2 (5) → grupo_atual = 3
Ruth     → Grupo 3 (5) → grupo_atual = 1 (voltou!)
Thayze   → Grupo 1 (6) → grupo_atual = 2
Katarine → Grupo 2 (6) → grupo_atual = 3
Sara     → Grupo 3 (6) → grupo_atual = 1 (voltou!)
Davyson  → Grupo 1 (7) ✓ CHEIO → grupo_atual = 2
Ilany    → Grupo 2 (7) ✓ CHEIO

Resultado: 4, 4, 3 alunos do Cluster 1 (máximo balanceamento!) ✅
```

#### Passo 4.4: Distribuir Cluster 2 (1 aluno) com Round-Robin

```
grupo_atual = 1 (REINICIA para Cluster 2)

Ana Claudia → Grupo 3 (7) ✓ CHEIO

Resultado: Único aluno vai para primeiro grupo disponível
```

**Estado Final:**
```
Grupo 1: 7 alunos ✓
Grupo 2: 7 alunos ✓
Grupo 3: 7 alunos ✓
```

## Detalhamento Técnico

### Distância Euclidiana

**Fórmula 3D:**
```
d = √[(x₁-c₁)² + (x₂-c₂)² + (x₃-c₃)²]
```

**Exemplo Real:**
```
Aluno: (3, 2, 3)
Centróide 0: (2.83, 2.00, 2.83)

d = √[(3-2.83)² + (2-2.00)² + (3-2.83)²]
  = √[0.17² + 0² + 0.17²]
  = √[0.0289 + 0 + 0.0289]
  = √0.0578
  = 0.2357
```

**Propriedades:**
- Sempre ≥ 0
- d = 0 apenas se pontos são idênticos
- Satisfaz desigualdade triangular

### Convergência do K-Means

**Critérios de Parada:**

1. **Centróides não mudam:**
   ```python
   if max(|novo_centróide - centróide_anterior|) < tolerance:
       break
   ```
   Padrão: tolerance = 1e-4

2. **Número máximo de iterações:**
   ```python
   if iteracao >= max_iter:
       break
   ```
   Padrão: max_iter = 300

**Típico:** K-Means converge em 10-50 iterações para datasets pequenos/médios.

### Capacidades Dinâmicas

**Algoritmo:**
```python
def calcular_capacidades(total, num_grupos):
    base = total // num_grupos       # Divisão inteira
    extras = total % num_grupos       # Resto
    
    capacidades = {}
    for i in range(1, num_grupos + 1):
        if i <= extras:
            capacidades[i] = base + 1  # Primeiros grupos ficam com extra
        else:
            capacidades[i] = base
    
    return capacidades
```

**Exemplos:**
```
calcular_capacidades(21, 3) → {1: 7, 2: 7, 3: 7}
calcular_capacidades(20, 3) → {1: 7, 2: 7, 3: 6}
calcular_capacidades(22, 3) → {1: 8, 2: 7, 3: 7}
calcular_capacidades(25, 3) → {1: 9, 2: 8, 3: 8}
```

**Propriedade:**
```
Σ capacidades[i] = total  (sempre!)
```

---

## Questões Frequentes

### Q1: Por que padronizar se features já estão em escala Likert (1-4)?

**R:** Mesmo na mesma escala nominal, features podem ter:
- **Médias diferentes**: Todos marcaram alto em Comunicação mas baixo em Liderança
- **Variâncias diferentes**: Comunicação com respostas variadas (1-4), Escrita concentrada (2-3)

K-Means usa distância euclidiana, que é sensível a essas diferenças. Sem padronização, features com maior variância dominariam o clustering.

### Q2: Por que k=3 e não k=6?

**R:** Versões antigas usavam k=6 para "ter mais granularidade". Mas isso complica desnecessariamente:
- k=3 já cria os 3 perfis principais
- Round-robin já distribui balanceadamente
- k=6 + round-robin = layers de complexidade sem benefício claro

k = número de grupos finais é mais lógico e direto.

### Q3: Por que alguns clusters ficam muito desbalanceados (6, 11, 1)?

**R:** Com apenas 11 coordenadas únicas de 18 alunos:
- Muitos alunos têm respostas idênticas
- K-Means agrupa pela similaridade, não pelo número
- Um cluster pode ter 1 aluno único, outro pode ter vários idênticos

Isso é **natural** quando há baixa diversidade nos dados. Round-robin resolve o desbalanceamento nos grupos finais.

### Q4: Alunos com coordenadas idênticas sempre vão pro mesmo cluster?

**R:** **SIM, sempre!** Porque:
```
Mesmas coordenadas → Mesmas distâncias → Mesmo centróide mais próximo → Mesmo cluster
```

É matematicamente impossível que coordenadas idênticas sejam atribuídas a clusters diferentes.

### Q5: Jitter afeta o clustering?

**R:** **NÃO!** Jitter é aplicado **APÓS** o clustering, apenas para visualização. Sequência:
1. K-Means usa coordenadas originais → Gera clusters
2. Jitter é adicionado → Apenas para gráficos
3. Distribuição usa clusters originais → Não vê jitter

### Q6: Como a distribuição garante diversidade?

**R:** Através da **Amostragem Estratificada**:

1. **Estratificação:** K-Means divide alunos em estratos (clusters) por similaridade
2. **Distribuição Proporcional:** Cada cluster é distribuído entre **todos** os grupos usando round-robin
3. **Reinicialização por Estrato:** Round-robin reinicia do Grupo 1 para cada cluster

**IMPORTANTE:** Não é uma garantia absoluta de que todos os grupos terão alunos de todos os clusters - isso depende do tamanho dos clusters. Se um cluster tem menos alunos que o número de grupos, alguns grupos ficarão sem representantes daquele cluster.

**Garantia Matemática:**
```
Se cluster C tem n alunos e temos k grupos:
  Cada grupo recebe ⌊n/k⌋ ou ⌈n/k⌉ alunos do cluster C
  
  Se n < k: Alguns grupos não receberão alunos do cluster C
  Se n ≥ k: Todos os grupos receberão pelo menos 1 aluno do cluster C
```

**Exemplo Real:**
- Cluster 0 (6 alunos, 3 grupos): Cada grupo recebe 6/3 = **2 alunos** ✅
- Cluster 1 (11 alunos, 3 grupos): Grupos recebem **4, 4, 3** (balanceado!) ✅
- Cluster 2 (1 aluno, 3 grupos): Apenas 1 grupo recebe, outros 2 ficam sem ⚠️

### Q7: Como garantir reprodutibilidade?

**R:** Definindo seeds:
```python
# K-Means
kmeans = KMeans(random_state=42)

# Distribuição de cabeças
random.seed(42)

# Jitter
np.random.seed(42)
```

Com as mesmas seeds, mesmo input → mesmo output, sempre.

### Q8: O que acontece se chegarem mais alunos?

**R:** O sistema é **totalmente dinâmico**:
```python
# 25 alunos chegam
total = 25 + 3 = 28

capacidades = calcular_capacidades(28, 3)
# {1: 10, 2: 9, 3: 9}

# Sistema ajusta automaticamente!
```

Não há valores hardcoded (exceto cabeças-de-chave).

### Q9: Como interpretar os centróides?

**R:** Centróides são "alunos médios" de cada perfil:
```
Centróide 0: (2.83, 2.00, 2.83)
→ Perfil "Comunicativo-Prático"
  Boa comunicação e liderança, escrita mais técnica

Centróide 1: (3.00, 3.27, 3.00)
→ Perfil "Equilibrado"
  Pontuações altas e balanceadas em tudo

Centróide 2: (3.00, 4.00, 1.00)
→ Perfil "Escritor-Introspectivo"
  Excelente escrita, menos propenso a liderar
```

### Q10: Posso usar mais de 3 grupos?

**R:** SIM! Basta mudar `num_grupos`:
```python
distribuidor = ClusteringDistribuidor(df, features, num_grupos=4)
```

O sistema ajusta automaticamente:
- K-Means com k=4
- Distribuição round-robin entre 4 grupos
- Capacidades dinâmicas

**ATENÇÃO:** Precisará de 4 cabeças-de-chave!

---

## Limitações e Considerações

### 1. Baixa Diversidade de Dados

**Problema:**
Com escala Likert 1-4 e 3 dimensões:
- Apenas 64 combinações possíveis
- Dataset real: 11 coordenadas únicas de 18 alunos
- 39% de duplicatas

**Impacto:**
- Clusters naturalmente desbalanceados
- Alguns centróides representam poucos alunos
- Visualizações precisam de jitter

**Soluções:**
- Coletar mais features (aumentar dimensionalidade)
- Usar escalas mais granulares (1-10 em vez de 1-4)
- Aceitar que é limitação dos dados, não do método

### 2. K-Means é Sensível a Outliers

**Problema:**
Se um aluno tem (1, 1, 4) e todos outros têm ~(3, 3, 3):
- Esse outlier pode "puxar" um centróide
- Cluster inteiro fica distorcido

**Solução:**
- Detectar outliers antes (ex: Z-score > 3)
- Usar algoritmos robustos (DBSCAN, OPTICS)
- Para nosso caso: escala 1-4 limita outliers extremos

### 3. Número de Clusters (k) é Pré-Definido

**Problema:**
K-Means exige que você defina k antecipadamente.

**Como escolher k?**
- **Método do Cotovelo**: Plotar inércia vs k, procurar "joelho"
- **Silhouette Score**: Medir qualidade do clustering
- **Domínio**: No nosso caso, k = número de grupos desejados

### 4. Suposições do K-Means

**O algoritmo assume:**
- Clusters são **esféricos** (mesma variância em todas direções)
- Clusters têm **tamanhos similares**
- Clusters são **convexos**

**No mundo real:**
Dados nem sempre seguem essas suposições. Alternativas:
- **DBSCAN**: Encontra clusters de forma arbitrária
- **GMM (Gaussian Mixture)**: Clusters elipsoidais
- **Hierarchical**: Não assume forma

### 5. Cabeças-de-Chave Hardcoded

**Limitação:**
Os 3 cabeças são definidos no código, não estão no CSV.

**Implicação:**
- Não podemos analisar suas soft skills
- Eles não participam do clustering
- São alocados puramente aleatoriamente

**Alternativa:**
Se cabeças estivessem no CSV:
- Poderiam ser clusterizados também
- Alocação poderia considerar perfil deles
- Grupos teriam cabeças com perfis complementares

### 6. Diversidade Limitada por Tamanho de Clusters

**Limitação:**
Se um cluster tem apenas 1 aluno, é **matematicamente impossível** distribuí-lo entre 3 grupos.

**Exemplo do Dataset Real:**
```
Cluster 0: 6 alunos  → 2 por grupo ✅
Cluster 1: 11 alunos → 4, 4, 3 ✅  
Cluster 2: 1 aluno   → 1, 0, 0 ⚠️ (inevitável!)

Índice de Diversidade:
  Grupo 1: 2/3 clusters representados
  Grupo 2: 2/3 clusters representados
  Grupo 3: 3/3 clusters representados ✅
```

**Solução:**
A distribuição balanceada por cluster já **maximiza** a diversidade dentro das restrições matemáticas. Se todos os clusters tivessem ≥3 alunos, teríamos diversidade máxima em todos os grupos.

**Métrica de Qualidade:**
```python
# Índice de diversidade por grupo
diversidade[grupo] = len(set(cluster_ids no grupo)) / total_clusters

# Objetivo: diversidade ≈ 1.0 (100%)
```

### 7. Métricas de Qualidade

**O que NÃO medimos:**
- Silhouette Score (qualidade do clustering)
- Davies-Bouldin Index (separação entre clusters)
- Diversidade dentro de cada grupo final

**Recomendação:**
Adicionar métricas para avaliar se distribuição é realmente boa.

---

## Melhorias Futuras

### 1. Validação de Clustering
```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X, clusters)
# -1 a +1: quanto maior, melhor
```

### 2. Escolha Automática de k
```python
from sklearn.metrics import silhouette_score

scores = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(X)
    scores.append(silhouette_score(X, labels))

k_otimo = scores.index(max(scores)) + 2
```

### 3. Métricas de Diversidade Avançadas
```python
# Índice de Shannon por grupo
from scipy.stats import entropy

def calcular_diversidade_shannon(grupo):
    cluster_counts = contar_por_cluster(grupo)
    proporcoes = cluster_counts / sum(cluster_counts)
    return entropy(proporcoes, base=2)

# Chi-Quadrado de uniformidade
from scipy.stats import chisquare

def testar_uniformidade(grupo):
    observado = contar_por_cluster(grupo)
    esperado = [len(grupo) / num_clusters] * num_clusters
    chi2, p_value = chisquare(observado, esperado)
    return p_value  # p > 0.05 = distribuição uniforme
```

### 4. Análise de Soft Skills dos Cabeças
```python
# Incluir cabeças no CSV
# Clusterizar todos
# Alocar cabeças garantindo grupos heterogêneos
```

### 5. Visualização Interativa
```python
import plotly.express as px

# Gráfico 3D interativo (rotacionar, zoom)
fig = px.scatter_3d(df, x='Com', y='Escrita', z='Liderança', color='Cluster')
fig.show()
```

---

## Referências

### Científicas
- Arthur, D., & Vassilvitskii, S. (2007). "k-means++: The advantages of careful seeding"
- MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations"
- Lloyd, S. (1982). "Least squares quantization in PCM"

### Documentação
- [Scikit-learn K-Means](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

### Conceitos
- [K-Means Clustering (StatQuest)](https://www.youtube.com/watch?v=4b5d3muPQmA)
- [Elbow Method](https://en.wikipedia.org/wiki/Elbow_method_(clustering))

---

## Conclusão

O **Método 1** combina duas técnicas estatísticas complementares:

1. **K-Means Clustering (Estratificação)**
   - Identifica perfis comportamentais homogêneos (estratos)
   - Minimiza variância intra-cluster (SSW)
   - Maximiza variância inter-cluster (SSB)

2. **Amostragem Estratificada (Distribuição com Diversidade)**
   - Garante representação proporcional de cada estrato em cada grupo
   - Maximiza heterogeneidade dentro de grupos finais
   - Utiliza round-robin por cluster para balanceamento

### Fundamentação Estatística

**Objetivo Dual:**
```
Fase 1 (Clustering): Minimizar Σ ||xᵢ - μc||²  (homogeneidade intra-cluster)
Fase 2 (Distribuição): Maximizar H = -Σ pᵢlog(pᵢ)  (diversidade inter-grupo)
```

**Garantias Matemáticas:**
- ✅ Cada cluster C com n alunos distribui ⌊n/k⌋ ou ⌈n/k⌉ para cada grupo (distribuição proporcional)
- ✅ Variância do tamanho de grupos ≤ 1 (máximo balanceamento de tamanhos)
- ✅ Índice de diversidade maximizado dentro das restrições naturais (tamanho dos clusters)
- ⚠️ **Limitação:** Se cluster tem menos alunos que o número de grupos, não é possível distribuir para todos os grupos

### Vantagens
✅ **Estatisticamente fundamentado** (amostragem estratificada)
✅ **Totalmente dinâmico** (funciona com qualquer número de alunos)
✅ **Reprodutível** (mesmas seeds → mesmos resultados)
✅ **Código limpo** (SOLID, separação de responsabilidades)
✅ **Maximiza diversidade** (cada grupo tem representantes de todos os perfis)
✅ **Bem documentado** com conceitos estatísticos claros

### Limitações
⚠️ **K-Means sensível** a dados com baixa diversidade (escala Likert 1-4)
⚠️ **Diversidade limitada** por tamanho de clusters (cluster com 1 aluno não pode ser dividido)
⚠️ **Cabeças-de-chave** não participam do clustering (alocação aleatória)
⚠️ **Assume clusters esféricos** (limitação do K-Means)

### Aplicações

Este método é especialmente adequado para:
- 📚 **Trabalhos acadêmicos**: Base estatística sólida (K-Means + Amostragem Estratificada)
- 👥 **Formação de equipes**: Maximiza diversidade de perfis comportamentais
- 🎯 **Balanceamento**: Garante grupos de tamanhos iguais ou quase iguais
- 🔬 **Pesquisa**: Reprodutível e matematicamente fundamentado

A combinação de **Clustering + Amostragem Estratificada** oferece uma abordagem robusta, teoricamente embasada e empiricamente eficaz para distribuição de grupos com maximização de heterogeneidade.

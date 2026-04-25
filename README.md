# Implementação de Métodos Estatísticos para Distribuição de Grupos

## 1. Contexto Geral do Problema Estrutural (Para Todos os Grupos)

O escopo analítico propõe a alocação de uma população finita ($N = 22$ alunos) em três subamostras mutualmente exclusivas e exaustivas (Grupos de trabalho), de modo a gerar partições de tamanhos restritos ($n_1 = 7, n_2 = 7, n_3 = 8$). 

Para isto, todos os grupos devem observar e codificar as seguintes diretrizes metodológicas:

*   **Restrições Paramétricas Fixas:** A variável aleatória de alocação não possui graus de liberdade para 3 elementos específicos (Yuri, Gilbran e Eduardo). Estes constituem *outliers* na fluência em programação e atuarão como "âncoras", sendo obrigatoriamente designados como as restrições sementes dos 3 grupos.
*   **Amostragem Estratificada Diversificada:** A formulação dos blocos probabilísticos visa garantir homogeneidade **inter-grupos** (a média final das subamostras deve estar estatisticamente alinhada com a média populacional em todas as dimensões avaliadas) e elevada heterogeneidade **intra-grupo** (observar diversidade considerável nos perfis alocados).
*   **Matriz de Dados:** As covariáveis sob escrutínio representam construtos latentes de *Soft Skills* (Comunicação, Escrita, Liderança) quantificadas por meio de uma **escala Likert ordinal de 1 a 4**, parametrizadas no _dataset_ `perfil_alunos.csv`.

---

## 2. Abordagens de Análise e Modelagem Multivariada

Cada um dos quatro grupos responsáveis apresentará a formulação matemática e o respectivo escopo computacional para alcançar a solução analítica via metodologias distintas.

### Grupo 1: Análise de Agrupamentos (Clustering) e Amostragem Estratificada
*   **O Desafio:** Empregar técnicas de estatística não-supervisionada para mapear a associação espacial dos sujeitos, agrupando-os por similaridade de atributos, visando maximizar a variância entre *clusters* e garantir a representação de todos os nichos psicológicos em cada grupo final de alunos.
*   **Fundamentação Estatística:** Aplica-se a análise de _clustering_ (como *K-Means* ou método hierárquico de *Ward*) objetivando a minimização da Soma dos Quadrados dos Erros (SSE) intra-cluster no hiperespaço Euclidiano (ou utilizando a distância de *Mahalanobis* dadas as correlações potenciais das _skills_). Assim, extraem-se centróides demográficos dos perfis. A distribuição atua como uma Amostragem Estratificada Clássica sobre os nichos mapeados.
*   **Guia de Implementação Computacional:**
    1. Importar a matriz de dados e proceder, se julgar necessário na literatura, com a normalização ou padronização dos escores ordinais (*StandardScaler*).
    2. Filtrar e remover transitoriamente os 3 sujeitos âncoras para não enviesar o *clustering*.
    3. Aplicar a modelagem de _K-Means_ ($k \approx 6$ ou $7$) sobre a subamostra livre ($n=19$) para demarcar os subconjuntos estrato-dependentes intrínsecos.
    4. Distribuir sequencialmente, valendo-se dos princípios da aleatoriedade simples ponderada, representantes dos *clusters* obtidos para compor os agrupamentos finais 1, 2 e 3.
*   **Bibliotecas e Ferramentas:** `scikit-learn` (`KMeans`, `StandardScaler`), `pandas`.
*   **Entregável de Inferência:** Visualização paramétrica no $\mathbb{R}^3$ via _Scatterplot_ em 3 dimensões que delineiam os estratos estatísticos formados, junto às métricas de média e variância intra-grupo (pós-separação).

### Grupo 2: Otimização via Programação Linear Inteira Mista (MILP)
*   **O Desafio:** Expressar o contexto combinatório em um modelo estritamente determinístico cujas restrições direcionam o plano hipergeométrico para convergir ao estimador ótimo e isento de viés para as diferenças das médias das amostras.
*   **Fundamentação Estatística:** Trata-se da minimização direta do erro de predição (dispersão paramétrica). Equaciona-se uma Função Objetivo modelada via somatório de erros absolutos ou dos quadrados dos desvios entre a média de cada partição recém-criada e a verdadeira média populacional $(\bar{X}_{grupo} - \mu_{turma})^2$. As alocações operam sob vetores inteiros booleanos (indicadoras estruturais).
*   **Guia de Implementação Computacional:**
    1. Instanciar a matriz de coeficientes indicadoras binárias $X_{i,g}$, onde $i$ é o i-ésimo aluno e $g$ o j-ésimo grupo.
    2. Estabelecer as desigualdades lineares limitantes de espaço amostral ( $\sum X_{i,1} = 7$, $\sum X_{i,2} = 7$, $\sum X_{i,3} = 8$ ) e as equações canônicas dos âncoras ( $X_{Yuri, 1} = 1$, etc).
    3. Construir a Função Objetivo: Buscar o Mínimo de $\sum | \bar{Y}_{habilidade, g} - \mu_{habilidade} |$ para todas as combinações formadas.
    4. Acionar o algoritmo *Solver* (ex: Método Simplex ou *Branch and Bound*) iterando pelo escopo das variáveis reais em busca da solução estacionária.
*   **Bibliotecas e Ferramentas:** Módulos de pesquisa operacional e otimização **`PuLP`** ou **`Pyomo`** em Python.
*   **Entregável de Inferência:** A formulação algébrica da equação proposta e um sumário estatístico evidenciando a ínfima significância da variância (Análise ANOVA teórica) das médias entres os grupos gerados pelo modelo estrito.

### Grupo 3: Heurísticas de Otimização Estocástica (Algoritmos Genéticos)
*   **O Desafio:** Trabalhar sob a imobilidade de o espaço amostral de combinações ser da grandeza de um processo Fatorial astronômico. Para contornar, usa-se métodos pseudo-aleatórios e estocásticos baseados em iterativas gerações evolutivas da Função Adaptativa.
*   **Fundamentação Estatística:** Trata-se de uma meta-heurística baseada em população cuja meta é evadir-se de vales de falsos Mínimos Locais na superfície de erro, através da perturbação estocástica (Mutação Geométrica) e da convergência inter-gerações via Operadores de Recombinação, maximizando indiretamente uma ponderação das variâncias locais contra o balanço global.
*   **Guia de Implementação Computacional:**
    1. Instanciar cada amostra de divisão randômica da turma como um "cromossomo" — um vetor direcional determinando $\textbf{v}_i \in \{1,2,3\}$.
    2. Construir a Função de Avaliação Randômica (*Fitness Function*): Deve calcular o Erro Quadrático Médio (MSE - *Mean Squared Error*) da distribuição dos escores. Penalizações severas não-lineares devem ser taxadas sobre o *MSE* se a população da amostra estourar 8 indivíduos ou se dois âncoras caírem colineares.
    3. Roteirizar o *loop* de hiperparâmetros (Geração), realizando *Crossover* (transmissão de características populacionais bem-sucedidas) e Seleção por Torneio na simulação estocástica de Monte Carlo.
*   **Bibliotecas e Ferramentas:** Arcabouço **`DEAP`** para computação evolucional ou implementações puras dependentes das bibliotecas estatísticas nativas `random` e rotinas de vetores do `numpy`.
*   **Entregável de Inferência:** Acompanhamento da Curva de Convergência (plotagem cartesiana das funções de *Loss/Fitness* caindo assintoticamente) da convergência estocástica na otimização.

### Grupo 4: Redução de Dimensionalidade Ortogonal (PCA) com Alocação Sistemática 
*   **O Desafio:** Transformar as múltiplas variáveis ordinais (matriz de covariáveis densas) em um super-índice independente por meio de transformações lineares, reduzindo o esforço computacional e aplicando em seguida uma Amostragem Sistemática ordenacional em grade ("*Snake Draft*").
*   **Fundamentação Estatística:** O Princípio de Componentes Principais (PCA) atua através da matriz de Covariância/Correlação. Busca os *Eigenvalues* (Autovalores) e *Eigenvectors* (Autovetores). A projeção ortogonal na primeira componente (PC1) explicará a maior variância combinada da Liderança, Escrita e Comunicação num único _escore sintético latente_.
*   **Guia de Implementação Computacional:**
    1. Transmutar os dados contínuos/ordinais via `PCA(n_components=1)`, reduzindo o colapso do conjunto de alunos em uma projeção vetorial sintética $Z_1$. Extrair o Percentual de Variância Explicada.
    2. Classificar ($Rank$) o conjunto na distribuição do autovetor PC1.
    3. Posicionar os indivíduos nas subamostras utilizando de alocação cíclica inversa (*Snake Order*: Amostra $A \rightarrow B \rightarrow C \rightarrow C \rightarrow B \rightarrow A \dots$), expurgando os âncoras da ordem geral para integrá-los nas partições base.
*   **Bibliotecas e Ferramentas:** O Módulo `sklearn.decomposition` nativo para manipulação dos dados via álgebra linear e `pandas.DataFrame.sort_values` para as rodadas numéricas.
*   **Entregável de Inferência:** Relatar graficamente a matriz vetorial do PC1 e seu índice explicativo percentual das variâncias das colunas em estudo, consolidando os estratos em _boxplots_.

---

## 3. Consolidação e Conclusões da Amostragem (Checklist de Homologação)

Como baliza paramétrica de sucesso da disciplina, na etapa de resultados conclusivos, **todos os métodos quantitativos acima explorados** (do estritamente Otimizado ao Estocástico e ao Multivariado em Agrupamento) deverão corroborar rigor científico, submetendo suas respostas finais às descritivas triviais:
1.  **Medidas de Posição Diferenciais:** O Cômputo paramétrico final atestando as Médias $\bar{x}$, as Medianas, e as Variâncias Amostrais $S^2$ correspondentes a cada grupo ($g_{1}, g_{2}, g_{3}$) sobre o eixo individual original de Comunicação, de Escrita e de Liderança. 
2.  Avaliação Crítica sobre os desvios causados pelos vieses intrínsecos de cada um dos métodos escolhidos (o achatamento do PCA contra a excessiva restrição da modelagem linear estrita, por exemplo).

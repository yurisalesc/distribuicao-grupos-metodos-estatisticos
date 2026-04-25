# Resultados dos Métodos Estatísticos de Distribuição de Grupos

Este projeto calcula e avalia quatro rotas estatísticas para distribuir a turma em Grupos de Trabalho super balanceados mediante um questionário de *Soft Skills* (Comunicação, Escrita, Liderança) quantificadas numa escala Likert (1 a 4). 

Para cada método, os 18 alunos avaliados pelo questionário formam a base orgânica (para que as notas nulas das cabeças-de-chave não corrompam os coeficientes). Após a divisão de algoritmos fechada em 3 grupos exatos de 6 alunos, as âncoras (Yuri, Gilbran, Eduardo) assumem seu isolamento estrutural nas três equipes, finalizando as 21 vagas de lotação.

---

## 1. Agrupamento Espacial (K-Means Clustering) e Amostragem Estratificada

### Fundamentação Estatística e Modelagem
Aplica-se a técnica não-supervisionada de *Clustering* (K-Means) objetivando a minimização da Soma dos Quadrados dos Erros (SSE) intra-cluster no hiperespaço Euclidiano ortogonal. Extraem-se centróides locais correspondentes aos "nichos comportamentais" dos 18 alunos avaliados, limitando-o à fragmentação teórica local em amostras de K=6. Posteriormente, aplica-se os princípios de uma Amostragem Estratificada: a matriz recolhe e pulveriza componentes de cada estrato gerado sobre os três grupos base, garantindo a representação de nichos multivariados e homogeneidade populacional inter-grupos.

### Prós e Contras
*   **Prós:** Matematicamente desenhado para forçar a maior diversificação (heterogeneidade) paralela de equipes possível.
*   **Contras:** Restringe o poder do K-Means ao fixar rigidamente K=6 num universo limitadíssimo (N=18). Pode forçar agrupamentos espúrios e artificiais caso as variâncias não justifiquem mais que dois polos reais na sala pura.

### Como o Algoritmo Aloca as Pessoas (Dinâmica Explicativa)
A animação GIF abaixo demonstra exatamente o ato estratigráfico: Sorteia-se 1 aluno de cada Nicho formado pelo k-Means e o encaminha por vez a um Grupo, garantindo times diversos. Repare que as barras vão sendo preenchidas por um indivíduo diferente de cada vez! O script "puxa" uma cor psíquica diferente ciclicamente (clusterização), até cada calha lotar matematicamente as 6 vagas residuais em paralelo!

### Visualização dos Dados
![Gráfico Clustering M1 Estático](grafico_metodo_1_clusters.png)

![Animação Clustering M1](anim_m1.gif)

### Formação das Equipes Resultantes
- **Grupo 1:** Yuri (Âncora), Tobias Navarro, Bruno de Paiva, Thayze Mikelle, Ana Claudia Medeiros, Sara de Sousa, Aldo Nascimento.
- **Grupo 2:** Gilbran (Âncora), Ana Maria Fonseca, Nalberth Samuel, Davyson Silva, Pedro Afonso, Talita Samara, Anne Karolayne.
- **Grupo 3:** Eduardo (Âncora), Luiz Renato, Rafael Matos, Ilany Micaely, Katarine, Ruth de Lima, Fermanda Heloah.

---

## 2. Otimização combinatória Exata (Programação Linear - MILP)

### Fundamentação Estatística e Modelagem
O contexto da explosão combinatória pode ser solucionado via Programação Inteira Mista Estrita (MILP). O equacionamento instanciou uma matriz Booleana ($X_{ig}$) para representar a atribuição absoluta sem variância do i-ésimo aluno para a j-ésima turma, de forma mutuamente exclusiva ($N_{soma} = 1$). A Função Objetivo focava minimizar estritamente a magnitude modular (desvios absolutos ou resíduos mínimos) defrontando o Score Médio de Capacidade Local contra o Estimador Limite Global (Média Inteira Populacional para cada Likert individual). 

### Prós e Contras
*   **Prós:** Converge absoluta e determinísticamente para o arranjo supremo e isento de viés analítico. Entrega o grupo mais justo e balanceado com base num modelo matemático linear onde restrições são tratadas de forma blindada pelo *Solver* (Simplex/Branch and Bound).
*   **Contras:** A linearização de Funções Módulo (Erros) sob restrições estritas requer muitas variáveis lógicas e torna computação excessivamente custosa e inflexível para bases gigantescas caso incluíssemos múltiplas funções de otimização concorrentes.

### Como o Algoritmo Aloca as Pessoas (Dinâmica Explicativa)
O motor resolve milhões de matrizes lógicas ($zeros\ e\ uns$) até que o resíduo do somatório estatístico colapse para $0$ e chegue à aprovação. O GIF Animado ilustra a leitura em tempo real da Matriz Otimizada Vencedora: pessoas aparecem e cravam instantaneamente sua alocação na barra dos grupos a cada chave $X[i, j] = 1$ afirmativa validada pelo simulador estrito!

### Visualização dos Dados
![Gráfico MILP M2 Estático](grafico_metodo_2_milp.png)

![Animação MILP M2](anim_m2.gif)

### Formação das Equipes Resultantes
- **Grupo 1:** Yuri (Âncora), Ana Claudia Medeiros, Luiz Renato, Fermanda Heloah, Sara de Sousa, Ilany Micaely, Nalberth Samuel.
- **Grupo 2:** Gilbran (Âncora), Anne Karolayne, Pedro Afonso, Bruno de Paiva, Thayze Mikelle, Davyson Silva, Aldo Nascimento.
- **Grupo 3:** Eduardo (Âncora), Tobias Navarro, Rafael Matos, Ana Maria Fonseca, Talita Samara, Ruth de Lima, Katarine.

---

## 3. Algoritmos Heurísticos (Otimização Evolutiva Genética DEAP)

### Fundamentação Estatística e Modelagem
Para contornar o uso custoso do cálculo integral/combinatório, aplicam-se Meta-Heurísticas de Evolução Populacional. Assumimos um hiperespaço probabilístico de busca no qual a Função Estocástica emula Mutação e Herdabilidade. O algoritmo penaliza o indivíduo que descumpra a Função de Viabilidade ("*Fitness Objective*") — neste escopo, a minificação do Erro Quadrático Médio (*MSE*). Crossovers dinâmicos de monte-carlo trocam componentes estocasticamente tentando desviar dos *Mínimos Locais* e convergindo ao arranjo otimizado intra-estatístico gradativamente em cada milissegundo de simulação (Gerações).

### Prós e Contras
*   **Prós:** A heurística baseada em perturbação e fitness é absurdamente rápida e versátil pois não varre todas as infinitas combinações e equações, encontrando vetores subótimos de extrema eficiência global muito rapidamente.
*   **Contras:** Sorte e semente influenciam no resultado. Trata-se de uma amostragem estocástica que jamais garantirá que esmiuçou o limite matemático absoluto, e depende severamente da calibração das taxas de Recombinação vs Mutação.

### Como o Algoritmo Aloca as Pessoas (Dinâmica Explicativa)
O GIF animado exibe a lei gravitória biológica em tempo real numa amostragem visual em que os alunos mudam desenfreadamente de barras. No começo da vida (Geração 0) a randomização inicial comete erros cruéis onde blocos inteiros estouram a Linha Vermelha de limite ideal de vagas! Conforme as gerações progridem e herdam o DNA das modelagens que tiveram penalidade baixa, o modelo estabiliza perfeitamente e trava nas 6 vagas redondas e empata seus saldos.

### Visualização dos Dados
![Gráfico DEAP M3 Estático](grafico_metodo_3_genetico.png)

![Animação DEAP M3](anim_m3.gif)

### Formação das Equipes Resultantes
- **Grupo 1:** Yuri (Âncora), Rafael Matos, Talita Samara, Thayze Mikelle, Katarine, Ilany Micaely, Aldo Nascimento.
- **Grupo 2:** Gilbran (Âncora), Ana Claudia Medeiros, Luiz Renato, Bruno de Paiva, Fermanda Heloah, Sara de Sousa, Nalberth Samuel.
- **Grupo 3:** Eduardo (Âncora), Tobias Navarro, Ana Maria Fonseca, Anne Karolayne, Pedro Afonso, Ruth de Lima, Davyson Silva.

---

## 4. Redução de Dimensionalidade (PCA) e *Snake Draft*

### Fundamentação Estatística e Modelagem
Aplica-se o Princípio de Análise de Componentes Principais (PCA) para transformar as três variáveis ordinais e covariadas ($X_1, X_2, \dots, X_p$) em um "Índice Escore" colapsado através da Projeção Ortogonal da Matriz de Covariância. O autovetor do primeiro *Principal Component* (PC1) captura numericamente quase sessenta por cento de toda a variância da turma analisada, criando um indexador latente unificado. Estabelecido o arranjo ordinal, executa-se uma modelagem reversa de Amostragem Sistemática — o modelo popular em Draft Esportivo '*Snake Order*', visando dispersar as concentrações paramétricas no eixo reverso iterativamente.

### Prós e Contras
*   **Prós:** Prático de entender, e estupidamente rápido do ponto-de-vista computacional. Ele unifica um super-escore resumindo uma proficiência total da média harmônica do aluno perfeitamente, sendo indestrutível matematicamente usando *Eigenvalues*.
*   **Contras:** Causa o extermínio da percepção do eixo multivariado em favor da dimensionalidade comprimida linear: Um aluno que fosse espetacular em Liderança viraria matematicamente um peso morto igualado a um estudante que fosse ok em "Tudo". Falha terrivelmente em garantir complementaridade explícita intra-grupo na prática, pois perde a rastreabilidade da feature Liderança. 

### Como o Algoritmo Aloca as Pessoas (Dinâmica Explicativa)
O Escore linear unificado formou a Fila Ordenada de classificação rankeada. Na animação visual vemos porque o formato recebe o nome de _Sorteio Zigue-Zague_. Repare nas métricas caíndo de bar em bar intermitentemente: A quarta vaga não vai pro G1; ela volta para as mãos do G3 e depois pro G2 para manter equilíbrio e neutralizar a força bruta de quem pegou o Primeiro da fila!

### Visualização dos Dados
![Gráfico Heatmap M4 Estático](grafico_metodo_4_pca.png)

![Animação Heatmap M4](anim_m4.gif)

### Formação das Equipes Resultantes
- **Grupo 1:** Yuri (Âncora), Sara de Sousa, Ilany Micaely, Anne Karolayne, Tobias Navarro, Davyson Silva, Aldo Nascimento.
- **Grupo 2:** Gilbran (Âncora), Katarine, Rafael Matos, Nalberth Samuel, Bruno de Paiva, Ana Claudia Medeiros, Ruth de Lima.
- **Grupo 3:** Eduardo (Âncora), Pedro Afonso, Thayze Mikelle, Luiz Renato, Ana Maria Fonseca, Fermanda Heloah, Talita Samara.

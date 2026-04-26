# Guia de Execução: Implementação de Métodos Estatísticos

Este projeto agora conta com a modelagem prática em Python de 4 métodos avançados para realizar a partição de equipes através dos questionários de Likert baseados em _Soft Skills_.

## 1. Instalando Dependências 📦
Antes de começar, todos os 4 grupos precisam preparar o ambiente instalando as bibliotecas de processamento, machine learning e simulação algébrica.

Basta abrir o **Terminal** e garantir que estão no diretório atual do projeto (onde está o arquivo `requirements.txt`) para rodar:
```bash
pip install -r requirements.txt
```

## 2. Injetora de Vagas (Aviso Prévio) ⚠️
Seus códigos Python já estão configurados com inteligência para carregar seu arquivo local `perfil_alunos` e **inserir os dados artificiais de Yuri, Gilbran e Eduardo (os três âncoras na distribuição)** sob as colunas do seu sistema para completar a base de 22 vagas em memória, de forma a não estragar ou corromper o arquivo orginal! Você não precisa se preocupar com edição do CSV.

---

## 3. Rodando os Códigos de Demonstração Interativa 🚀

Cada grupo pode simular e demonstrar seu resultado na disciplina rodando apenas 1 comando e analisando as métricas plotadas que surgiriam.

### 🖥️ Grupo 1 (Clustering Espacial)
Abra o console e digite:
```bash
python metodo_1_clustering.py
```
> **Entregáveis:** Verifique sua tela de prompt para acompanhar o "banco de grupos" formados. Na sua pasta raiz aparecerá o novo arquivo `grafico_metodo_1_clusters.png` e ilustrando no hiperespaço a divisão de similares!

### 📊 Grupo 2 (Otimizacao MILP)
Abra e rode no console para acionar o motor algébrico:
```bash
python metodo_2_milp.py
```
> **Entregáveis:** O terminal exibirá matematicamente o *Solver Simplex* resolvendo as matrizes inteiras das combinações. Um gráfico comprovando minimização do balanço médio global da turma surgirá no arquivo `grafico_metodo_2_milp.png`.

### 🧬 Grupo 3 (Otimização Estocástica/Genético)
Ative a máquina de populações via framework DEAP:
```bash
python metodo_3_genetico.py
```
> **Entregáveis:** Diferente das contas diretas, este programa gera uma corrida intergeracional artificial. Um arquivo `grafico_metodo_3_genetico.png` mostrará a curva de aprendizado decrescendo seu erro até fechar no agrupamento listado terminal.

### 🐍 Grupo 4 (Redução Autovetorial e Draft)
Ative o gerador estatístico de dimensões minimizadas:
```bash
python metodo_4_pca.py
```
> **Entregáveis:** Além de gerar e provar percentualmente a "Variância Explicada" num componente linear, construirá um arquivo `grafico_metodo_4_pca.png`. Ele tem as formas de *Heatmap* de Cores listando os eleitos aos grupos por *Snake* via PCA.

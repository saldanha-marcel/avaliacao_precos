# Preços de Diesel e GNV - Pipeline Databricks

Guia funcional do projeto desenvolvido dentro de Databricks. O repositório organiza a ingestão, transformação e análise de preços de combustíveis da base pública da ANP.

## Visão geral

- O projeto consome arquivos CSV públicos da ANP sobre preços de diesel e GNV.
- Os dados brutos são armazenados em um volume do Databricks (`/Volumes/lakehouse/raw/prices_diesel`).
- O pipeline segue os estágios:
  1. **Raw / Ingestão**: download e leitura dos CSVs
  2. **Bronze**: ingestão em tabela Delta `lakehouse.bronze.precos_combustiveis`
  3. **Silver**: limpeza e normalização em `lakehouse.silver.precos_combustiveis`
  4. **Gold**: métricas e agregações em tabelas analíticas Delta

## Estrutura do projeto

- `notebooks/00_setup.ipynb` - criação de schemas, volumes e permissões no lakehouse.
- `notebooks/01_ingestion.ipynb` - download dos arquivos ANP e ingestão na camada bronze.
- `notebooks/02_transformation.ipynb` - conversão de tipos, normalização e criação da tabela silver.
- `notebooks/03_analytics.ipynb` - geração de tabelas gold com indicadores e agregados.
- `src/download.py` - script de exemplo para baixar os CSVs da ANP.
- `src/schema.py` - referência do cabeçalho esperado dos dados.

## Pré-requisitos

- Cluster Databricks com suporte a Spark e Delta Lake.
- Volume montado e acessível no cluster em `/Volumes/lakehouse/raw/prices_diesel`.
- Conexão à internet para baixar os arquivos CSV da ANP durante a ingestão.

## Como executar

### 1. Abra o workspace Databricks

Importe ou acesse os notebooks do repositório dentro do seu workspace Databricks.

### 2. Execute o notebook de setup

Abra `notebooks/00_setup.ipynb` e execute as células em sequência.

Objetivo:
- criar os schemas do lakehouse (`lakehouse.raw`, `lakehouse.bronze`, `lakehouse.silver`, `lakehouse.gold`)
- criar volumes e estruturas iniciais
- preparar permissões caso o ambiente exija controle de acesso

### 3. Execute o notebook de ingestão

Abra `notebooks/01_ingestion.ipynb` e execute todas as células.

Esse notebook:
- define o caminho raw: `/Volumes/lakehouse/raw/prices_diesel`
- baixa arquivos ANP por ano/mês
- lê os CSVs com Spark usando `sep=';'` e `header=True`
- renomeia colunas para formato snake_case
- grava o resultado em Delta como `lakehouse.bronze.precos_combustiveis`

### 4. Execute o notebook de transformação

Abra `notebooks/02_transformation.ipynb` e execute todas as células.

Esse notebook realiza:
- leitura de `lakehouse.bronze.precos_combustiveis`
- conversão de `valor_de_venda` para `Double`
- conversão de `data_da_coleta` para `Date`
- extração de `mes_da_coleta` e `ano_da_coleta`
- limpeza de `unidade_de_medida`
- gravação em `lakehouse.silver.precos_combustiveis`

### 5. Execute o notebook de analytics

Abra `notebooks/03_analytics.ipynb` e execute todas as células.

Esse notebook cria tabelas gold com análises como:
- preço médio mensal por bandeira e região
- média, máximo e mínimo por estado, ano e produto
- preços médios por estado, mês e produto
- variação percentual temporal e médias móveis
- índice de sazonalidade mensal

Tabelas gold geradas:
- `lakehouse.gold.preco_medio_mensais_por_bandeira`
- `lakehouse.gold.preco_medio_max_min_estado_ano_df`
- `lakehouse.gold.preco_medio_estado_mes`
- `lakehouse.gold.variacao_temporal`
- `lakehouse.gold.sazonalidade_mensal`

## Dados e esquema

Os principais campos usados no pipeline são:

- `regiao_sigla`
- `estado_sigla`
- `municipio`
- `revenda`
- `data_da_coleta`
- `produto`
- `valor_de_venda`
- `unidade_de_medida`
- `bandeira`

A fonte original é o portal de dados abertos da ANP para preços de combustíveis.

Fonte: https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp

# README - Teste de nivelamento v.250321

## Resumo do Projeto
Este projeto é uma solução para extração, transformação, armazenamento e consulta de dados do setor de saúde.
Ele combina web scraping, processamento e transformação de dados e uma API RESTful para disponibilizar informações estruturadas sobre operadoras de saúde.
## Componentes do Sistema
### 1. Web Scraping e Transformação de Dados
- **Extração de Dados**: Módulos para baixar anexos e documentos do site da ANS (Agência Nacional de Saúde Suplementar)
- **Processamento**: Transformação de PDFs e documentos em dados estruturados
- **Compactação**: Ferramentas para compactar arquivos extraídos e processados

### 2. Banco de Dados

- **Operadoras Ativas**: Módulo para gerenciar dados das operadoras de saúde em atividade
- **Demonstrações Contábeis**: Sistema para processar e armazenar dados financeiros das operadoras
- **Conexão com Banco de Dados**: Utiliza PostgreSQL para armazenamento persistente dos dados processados
- **Docker**: Arquivo Docker Compose disponível para configuração rápida do ambiente de banco de dados

## Configuração do Ambiente com Docker

O projeto inclui um arquivo Docker Compose para facilitar a configuração do ambiente de banco de dados:

1. **Iniciar o banco de dados**:
   ```
   docker-compose up -d
   ```

2. **Verificar status do container**:
   ```
   docker-compose ps
   ```

3. **Parar os serviços**:
   ```
   docker-compose down
   ```

O PostgreSQL será acessível na porta padrão 5432 com as credenciais definidas no arquivo de configuração.

### 3. API RESTful
- **Servidor Flask**: Interface para consulta dos dados processados
- **Paginação**: Sistema eficiente para consulta de grandes volumes de dados
- **Busca Textual**: Funcionalidade para localização rápida de informações específicas
- **CORS Habilitado**: Permite integração com aplicações front-end

## Como Usar
### Requisitos
- Python 3.6+
- Bibliotecas listadas em `requirements.txt`

### Executando os Módulos
1. **Web scraping e transformação de dados**:
```
   python web_scraping_transformacao_dados/main.py
```
1. **Processamento de Demonstrações Contábeis**:
```
   python banco_dados/demonstracoes_contabeis/main.py
```
1. **Processamento de Operadoras Ativas**:
```
   python banco_dados/operadoras_ativas/main.py
```
1. **Servidor API**:
```
   python api/servidor/servidor.py
```
### Endpoints da API
#### Consulta de Dados com Paginação
```
GET /data?page=1&per_page=10
```
#### Busca nos Dados
```
GET /search?query=termo&page=1&per_page=10
```
## Características Principais
- **Automação**: Coleta e processamento automático de dados do setor de saúde
- **Escalabilidade**: Estrutura modular que facilita a expansão do sistema
- **Performance**: Cache em memória para consultas rápidas
- **Flexibilidade**: Permite integração com diversas interfaces e sistemas

## Fluxo de Trabalho
1. Os módulos de web scraping extraem dados de fontes oficiais
2. Os dados são transformados em formatos estruturados (CSV)
3. Os módulos de banco de dados organizam e armazenam as informações
4. A API disponibiliza os dados processados para consulta



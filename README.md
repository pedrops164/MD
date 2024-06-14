
# Trabalho Prático da UC de Mineração de Dados 


## Sumário do Trabalho
Este trabalho baseia-se num LLM que serve como guia turístico para várias localizações no Norte de Portugal. O objetivo do grupo, desde o início, foi criar uma aplicação que oferecesse informações precisas e detalhadas sobre atrações turísticas, cultura e história do Norte de Portugal, utilizando técnicas avançadas de mineração de dados e processamento de linguagem natural.

## Elementos do Grupo

- Pedro Pereira Sousa PG54721
- Mateus Medeiros Pereira PG54089
- Nuno Miguel Leite da Costa PG54121
- Elione Culeca Cossengue PG51634

## Estrutura do Repositório

O repositório está estruturado da seguinte forma:

- **dbs** - Esta pasta contém as bases de dados das diferentes entidades e também o db.py, que gera a base de dados e realiza operações como inserir chunks, devolver a base respetiva, entre outras;

- **images** - Nesta pasta, guardamos as imagens para utilizar no README;

- **logs** - Aqui são armazenados os logs da aplicação;

- **pdfs** - Esta pasta contém os PDFs provenientes do VisitPortugal, utilizados para povoar as diferentes bases de dados;

- **presentations** - Esta pasta contém as duas apresentações do projeto prático;

- *requirements.txt* - Lista dos requisitos necessários para executar o trabalho;

- *queries.txt* - Alguns exemplos de queries;

- *templates.py* - Define as templates que são enviados para o system prompt do LLM;

- *scraper.py* - Utilizado para extrair os chunks dos PDFs e inseri-los nas bases de dados respetivas;

- *agent.py* - Define a classe responsável pela interação com o LLM;

- *gui.py* - Responsável por criar a interface utilizada no nosso trabalho;

- *main.py* - Encarregado de inicializar a interface, o agente e executar o loop principal da interface, que recebe o input do utilizador e passa o input para o agente processar a query;

- *report.pdf* - Relatório do nosso trabalho;

## Demonstração

![Demonstração do Projeto](./images/demo_projeto_1.gif)



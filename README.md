# Work at Olist

Esse repositório possui a estrutura básica de uma aplicação Django que deve
disponibilizar uma API para manipulação de uma árvore de categorias de
produtos.


## Como participar

1. Faça um fork desse repositório no Github
2. Siga as instruções desse `README.md`.
3. Faça o deploy do projeto no Heroku
4. Envie um [e-mail](olist-lst0966@applications.recruiterbox.com) contendo:
  - Link para o fork no Github.
  - Link para o projeto no Heroku.
  - Breve descrição do ambiente de trabalho usado para executar esse projeto
    (computador/sistema operacional, editor de textos/IDE, bibliotecas, etc).
  - Curriculum Vitae anexado ao e-mail.


## Especificação do problema

Olist é uma empresa que disponibiliza uma plataforma para integração entre
lojistas (*Sellers*) e canais (*Channels*) de vendas conhecidos como
marketplaces.

Um dos nossos serviços permite que os lojistas publiquem seus produtos nos
canais. Para que esses produtos sejam publicados é necessário informar a sua
categoria para o canal.

Todos os canais agrupam os produtos publicados em categorias que são
organizados como uma árvore de profundidades variáveis. Veja a versão
resumida da arvore de um dos canais:

- Livros
  - Direito
  - Literatura Nacional
    - Ficção Científica
    - Ficção Fantástica
  - Literatura Estrangeira
  - Informática
    - Aplicativos
    - Banco de Dados
    - Programação
- Games
  - XBOX 360
    - Console
    - Jogos
    - Acessórios
  - XBOX One
    - Console
    - Jogos
    - Acessórios
  - Playstation 4
- Informática
  - Notebooks
  - Tablets
  - Desktop
- Eletrodoméstico
  - Fogões
  - Fornos
  - Micro-ondas
- :

Cada canal envia um arquivo CSV onde uma das colunas (`Categoria`) tem o nome
completo de cada categoria usada:

```
Categoria
Livros
Livros/Direito
Livros/Literatura Nacional
Livros/Literatura Nacional/Ficção Científica
Livros/Literatura Nacional/Ficção Fantástica
Livros/Literatura Estrangeira
Livros/Informática
Livros/Informática/Aplicativos
Livros/Informática/Banco de Dados
Livros/Informática/Programação
Games
Games/XBOX 360
Games/XBOX 360/Console
Games/XBOX 360/Jogos
Games/XBOX 360/Acessórios
Games/XBOX One
Games/XBOX One/Console
Games/XBOX One/Jogos
Games/XBOX One/Acessórios
Games/Playstation 4
Informática
Informática/Notebooks
Informática/Tablets
Informática/Desktop
Eletrodoméstico
Eletrodoméstico/Fogões
Eletrodoméstico/Fornos
Eletrodoméstico/Micro-ondas
:
```


## Requisitos do projeto

O projeto a ser desenvolvido precisa implementar as seguintes funcionalidades:

- Utilizar Python >= 3.5 e Django >= 1.9.
- Os dados deverão ser armazenados em um banco de dados relacional.
- Criação de um *Django Management Command* para importar as categorias dos
  canais a partir de um CSV.
  - O comando de importação deve operar em em modo "*full update*", ou seja, deve
    sobrescrever todas as categorias de um canal pelas categorias do CSV.
  - O comando deve receber 2 parâmetros: nome do canal (cria o canal caso não
    exista) e o nome do arquivo `.csv`:

```
$ python manage.py importcategories walmart categorias.csv
```

- Cada canal tem um conjunto próprio de categorias.
- Cada canal precisa ter um identificador único e um campo com o nome do canal.
- Cada categoria precisa ter um identificador único e um campo com o nome da categoria.
- Criação de uma API HTTP REST que permita:
  - Listar canais existentes.
  - Listar as categorias e subcategorias de um canal.
  - Retornar uma categoria única com suas categorias-pai e suas subcategorias.

> Dica #1:
> As operações de atualização dessa árvore acontecem com uma frequência semanal
> e as consultas às categorias-pai e sub-categorias acontecem na escala de 
> milhares por minuto.

- A API precisa de documentação em inglês.
- Variáveis, código e strings devem estar todas em inglês.

> Dica #2:
> O projeto Django deste repositório tem vários pontos para melhoria.
> Encontre-os e implemente essas melhorias.


## Recomendações

- Escreva testes.
- Evite expor detalhes de implementação do banco de dados na API (ex. ID
  auto_increment dos models).
- Pratique os conceitos [12-Factor-App](http://12factor.net)
- Faça commits pequenos, atômicos, com mensagens claras e em inglês no Github.
- Utilize boas práticas de programação.

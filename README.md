# Work at Olist

Esse repositório possui a estrutura básica de uma aplicação Django que deve
disponibilizar uma API para manipulação de uma árvore de categorias de
produtos.


## Como participar

1. Faça um fork desse repositório no Github
2. Siga as instruções desse `README.md`.
3. Faça o deploy do projeto no Heroku
4. Envie o um [e-mail](olist-lst0966@applications.recruiterbox.com) contendo:
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

- Os dados deverão ser armazenados em um banco de dados relacional (ex. MySQL /
  PostgreSQL / SQLite).
- Criação de um *Django Management Command* para importar as categorias dos
  canais a partir de um CSV.
- O comando de importação deve operar em 2 modos: `full` e `update`.
  - Modo `full`: a importação deve sobrescrever todas as categorias de um canal
    específico.
  - Modo `update`: as categorias novas do CSV serão criadas e o restante será
    mantido intacto.
- O comando deve receber 3 parâmetros: modo de operação (`full` ou `update`),
  nome do canal (cria o canal caso não exista) e o nome do arquivo `.csv`:

```
$ python manage.py importcategories update walmart categorias.csv
```

- Cada canal tem um conjunto próprio de categorias.
- Cada canal precisa ter um identificador único.
- Cada categoria precisa ter um identificador único.
- Criação de uma API HTTP REST que permita:
  - Cadastrar novos canais.
  - Listar canais existentes.
  - Cadastrar novas categorias e sub-categorias.
  - Listar uma categoria com suas respectivas categorias-pai e sub-categorias.

> Dica #1:
> As operações de atualização dessa árvore acontecem com uma frequência semanal
> e as consultas às categorias-pai e sub-categorias acontecem às milhares por
> minuto.

- O acesso à API precisa ser autorizado através de um token associado à um
  usuário Django fornecido no Header HTTP apropriado (`Authorization`):

```
Authorization: token deadbeefdeadbeef...deadbeef
```

- Utilizar Python 3.5 ou mais recente e Django 1.9 ou mais recente.
- Variáveis, código e strings devem estar todas em inglês.

> Dica #2:
> O projeto Django deste repositório tem vários pontos para melhoria.
> Encontre-os e implemente essas melhorias.


## Recomendações

- Evite expor detalhes de implementação do banco de dados na API (ex. ID
  auto_increment dos models).
- Pratique os conceitos [12-Factor-App](http://12factor.net)
- Escreva testes.
- Documente a API.
- Faça commits pequenos, atômicos, com mensagens claras e em inglês no Github.
- Utilize boas práticas de programação.

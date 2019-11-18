## Contexto e dores

A minha primeira interação foi ler a especificação e em seguida buscar
referências a respeito de `candlesticks` e análise técnica (entender melhor a
aplicação).

Eu optei por usar uma estratégia altamente baseada no seguinte artigo:

```
https://medium.com/coinograph/storing-and-processing-billions-of-cryptocurrency-market-data-using-influxdb-f9f670b50bbd
```

Outras opções que me chamaram a atenção estão descritas nestes artigos:

```
https://towardsdatascience.com/how-to-store-financial-market-data-for-backtesting-84b95fc016fc
https://ericdraken.com/storing-stock-candle-data-efficiently/
```

A opção por usar o `influxdb` foi por (1) curiosidade em trabalhar com um tipo
de banco de dados que nunca havia trabalhado e (2) me pareceu ter um fit muito
grande com o deafio proposto.

Eu optei por fazer o código em python por ser uma das linguagens usadas na
empresa. Isso foi uma dor significativa pois gerou um acumulo de tecnologias
não conhecidas, a necessidade de dar um start no projeto e de consultar até
mesmo como faer um `split` em string, entender minimamente como módulos e
diretórios se relacionam e leitura de algumas das muitas `PEP`s.

Além disso, tive uma semana em que eu não consegui trabalhar com esse código.
Então foram dois sábados, um domingo e uma segunda parcialmente dedicados.

Gostaria de ter conseguido:

1. estruturar melhor o código, dentro de padrões do python
2. adicionar testes (isso acho bem negativo)
3. colocar o projeto no gitlab e testar o ci/cd do mesmo (que não conheço)
4. feito bons commits do git

Em que pese estes pontos, achei muito interessante o que aprendi de python e a
vontade que ficou de estudar e praticar um pouco mais. Ainda fica a sensação de
que algumas coisas são bem complicadas e/ou mal documentadas, mas com o meu
conhecimento bem limitado só fica mesmo a certeza que há muito ainda para
aprender da linguagem.

Outra coisa que valorizo muito foi ter chegado ao `influxdb` após esse teste.
Muito interessante e pretendo fazer alguns testes com histórico de eventos
usando o mesmo ou algum outro banco semelhante. Sem dúvida, valeu muito a pena
ter tido esse contato com ele.

Em relação aos commits do git e testes em aplicações, há aqui dois exemplos de
como eu acredito que eles devem ser feitos (descrição a cada alteração e specs
cobrindo o comportamento):

1. https://github.com/dleemoo/dns-app
2. https://github.com/dleemoo/bank-accounting

Em ambos os casos são testes em ruby, porém eles ilustram (muito melhor) como
acredito que commits devem ser feitos no git e como testes devem acompanhar os
mesmos.

## Descrição em alto nível

A solução apresentada está separada em quatro módulos:

1. lib.db
2. lib.aggregator
3. lib.websocket
4. lib.client

A ideia é obter os dados da API na maior frequencia possível (definido por
TICKER_FETCH_INTERVAL, que por padrão é 2 segundos). E atualizar o cliente o
mair rápido possível (definido por WEBSOCKET_UPDATE_INTERVAL e que padrão é 5
segundos).

Todas as queries de agregação executam a cada 10 segundos (definido em
`lib/aggregator/setup.py`).

A ideia desta configuração e permitir que os dados sejam exibidos em tempo real
(diferenças de até 15 segundos no pior caso). É um melhor esforço, uma vez que
não há precisão a respeito do momento de obteção dos dados da API.

A separação do código em módulos foi uma tentativa de separar as
responsabilidads. Há só um `requirements.txt` e nem todos os containers
precisariam das dependências. Isso foi só para simplificar o setup no contexto
deste teste.

### lib.db

A ideia foi agrupar aqui todas as funções relativas ao acesso ao `influxdb`.
Acesso a um dataset presente no banco também deveriam ser feitos aqui.

Esse módulo inclui o `lib.db.setup` que é um arquivo de configuração. Acredito
que isso não seja um padrão nada comum, porém eu não consegui fazer uma outra
forma reprodutível com facilidade.

### lib.aggregator

Esse modulo é o responsável por obter os dados de cotação da API e por
salvá-las no banco de dados.

Neste caso há também o `lib.aggregator.setup` que configura o `influxdb` para
fazer as queries de agregação dos candles.

### lib.websocket e lib.client

Estes dois módulos foram onde eu dediquei menos tempo e possuem uma
implementação muito pouco robusta. De toda forma, eles cumprem o papel mínimo
de exibir a informação e de obtê-la no client via um serviço.

No caso do client a ideia era usar `curses` para evitar a movimentação e
flicker ao renderizar novamente a tabela.

Há um bug que não consegui chegar a um código funcional para o momento em que o
cliente é fechado (usando-se control-c). Isso leva a um erro no servidor que
poderia ser evitado, porém tratar a interrupção do teclado e fechar
corretamente a conexão levou a uma depuração muito improdutiva no código.

## Configuração

Há um script em `bin/first-time-setup` que pode ser usado para configurar tudo
que é descrito nessa seção.

Esse repositório contém uma configuração para uso do código com o `docker`.
Todo o código desenvolvido utiliza a imagem
[python:3.8.0-slim-buster](https://github.com/docker-library/python/blob/0b1fb9529c79ea85b8c80ff3dd85a32a935b0346/3.8/buster/slim/Dockerfile).
Além disso a imagem
[influxdb:1.7.9](https://github.com/influxdata/influxdata-docker/blob/d80e739adbe01bb2f0cb3db77da3ded6c1556d15/influxdb/1.7/Dockerfile)
também é utilizada.

O arquivo `docker-compose.yml` define e conecta todos os serviços necessários.
Ele depende da configuração em um arquivo `.env` (que também é usado pelas
aplicações). O arquivo `.env.example` contém uma configuração funcional
completa, inicialmente fazemos uma cópia do mesmo:

```
cp .example.env .env
```

Para obter as imagens execute:

```
docker-compose pull
```

Para configurar os serviços (`aggregator` e `websocket`) execute:

```
docker-compose run --rm sb-websocket pip install --user -r requirements.txt
docker-compose run --rm sb-aggregator pip install --user -r requirements.txt
```

Há um sandbox no `docker-compose.yml`. A ideia é que ele seja o ambiente para
testes do cliente. Sendo assim, é necessário fazer:

```
docker-compose run --rm sb-sandbox pip install --user -r requirements.txt
```

Para configurar o `influxdb` e o `aggregator` é necessário executar alguns
comandos para configurar o banco de dados. Estes podem ser executados com os
seguintes comandos:

```
docker-compose run --rm sb-aggregator python -m lib.db.setup
docker-compose run --rm sb-aggregator python -m lib.aggregator.setup
```

:warning: :warning: :warning:
Estes comandos esperam que o **influxdb** já esteja em execução e aceitando
conexões. Eles podem falhar se o serviço **influx1** demorar mais tempo para
inicializar.

Isso pode ser contornado executando o serviço de forma independente (em um
segundo terminal) e esperando que o banco seja incializado (`docker-compose up
influxdb`).
:warning: :warning: :warning:

## Uso

Uma vez que todos os passos foram executados com sucesso os serviços já estão
prontos para o uso (pode-se inclusive terminar a execução anterior do
`influxdb`) com o seguinte comando:

```
docker-compose up
```

Ao executar este comando será inicializado:

1. `influx1` serviço que provê acesso ao `influxdb`
2. `sb-aggregator` serviço que provê a aggregação dos candles
3. `sb-websocket` serviço que provê acesso aos candles agregados

O serviço `sb-sandbox` é um serviço fake que permite a execução do cliente em
um ambiente facilmente reprodutível. Há um pequeno wrapper para executar o
cliente usando esse container em `bin/feed`. Ele pode ser usado das seguintes
maneiras:

```
./bin/feed 1m
./bin/feed 5m
./bin/feed 10m
```

O cliente aceita um segundo argumento que define quantos candles serão
exibidos.  Pode-se usar esse argumento entre 1 e 3. Assim, para exibir os
útlimos `2` para cada moeda de duração `5m`, pode-se utilizar:

```
./bin/feed 5m 2
```

Para testar o funcionamento fora do container `sb-sandbox` é necessário alterar
o `docker-compose.yml` e exportar as portas dos serviços para o localhost.

## Outros pontos relevantes

1. Avaliar melhor o uso do `influxdb` (comparação com as opções usando banco de
   dados relacionais, sqlite/arquivos).
2. No uso do influxdb não usar JSON e sim line protocol.
3. A solução usa uma opção do `influxdb` que será descontinuada na próxima
   versão. Então, há que se pensar a respeito do uso da versão 1 e *continuous
   queries* e uma eventual migração para a versão 2 com *tasks*.
4. O setup com o docker aqui apresentado é, talvez, viável para
   desenvolvimento. Para um ambiente de produção certamente ele não poderia ser
   utilizado.

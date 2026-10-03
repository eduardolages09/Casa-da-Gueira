# Casa da Gueira — site e dossiê

## Pastas

- `dossie/` — o dossiê da casa (skill al-dossier). Ponto de entrada: `dossie/resumo.md`. O que o site pode dizer: `dossie/site-pronto.md` (gerado de `contrato.json`).
- `site/` — o site estático, sem build. É a única pasta publicada (`netlify.toml`).
  - `index.html` — a página, só em português (versão base).
  - `styles.css`, `main.js`.
  - `assets/img/` — fotos em três tamanhos (original até 2400 px, 1400 e 800).
- `arquivo/` — versões anteriores do site, guardadas só para referência. Não são publicadas.
- `scripts/`
  - `imagens.py` — copia as fotos do dossiê para o site (`py scripts/imagens.py`).
  - `traduzir-en.py` — gera `site/en/index.html`. **Não se usa na versão base**: o inglês é um extra da versão completa. Os `PARES` estão desatualizados desde a versão 3 (a frase da casa, a piscina e os hóspedes mudaram); atualizá-los antes de voltar a gerar o inglês. O `main.js` já trata as duas línguas.

## O site (versão 10)

A landing page da versão base. Mantém a cara do site atual da casa (branco, verde-azeitona, taupe, o logótipo, letra fina) e corrige o que lhe falta, com poucas fotos e boas. Mostra a casa de leve: o visor abre poucas fotos por divisão (4 a 5 por divisão, 8 das três suites e 9 das casas de banho) e 4 de lá fora. A galeria inteira fica para a versão completa. Versões anteriores em `arquivo/` (`site-v1/`, `site-v3/` a `site-v10/`, `site-v11-hero-filme/`, `site-v12-hero-drone/`).

Secções, por ordem:
1. **Hero:** um "filme" com as fotos da casa e o nome e a frase por cima. São quatro planos: a piscina sobre o vale (afasta), o drone a pique sobre a casa (aproxima), a mesa do terraço (desliza para a direita) e o drone sobre a casa e a piscina (aproxima). A foto da água com a casa de pedra (piscina-05) saiu: só existe na versão ampliada e muito comprimida do Booking, e o mesmo ângulo já está em Reservar. Depois volta ao início. Os tempos foram escolhidos para a troca se notar. O primeiro plano troca 4,5 s depois de a página abrir e os outros duram 5,5 s. A troca é curta (0,8 s) e cada plano entra já em movimento e vai abrandando. Os dois drones estão separados e os movimentos alternam. Em baixo, à esquerda, quatro traços mostram o progresso: os já vistos ficam cheios, o atual vai enchendo, e cada traço salta para a sua fotografia. Cada foto só descarrega e é descodificada quando o plano anterior entra. O filme para quando o hero sai do ecrã e tem um botão de pausa. Com movimento reduzido fica só a primeira foto. **Qualidade:** as fotos do filme (`filme-*`) saem do original até 3000 px, com pouca compressão e com o tom do site já aplicado (`FILME` em `scripts/imagens.py`), sem filtro CSS. O CSS desenha cada foto a 112 % e a câmara só a reduz ou desliza, por isso nunca é ampliada. Num ecrã de 1920 px, cada plano usa a cópia de 2400 px. Os planos estão no HTML (`--mov`, `--pos`, `--pos-alto`) e o tempo está em `main.js`, "FILME".
   - **Alternativas guardadas:** o filme anterior, com fotos de 2000 px ampliadas, está em `arquivo/site-v11-hero-filme/`. O plano de drone com paralaxe (uma foto em dois planos) está em `arquivo/site-v12-hero-drone/`, com o `hero-camadas.py` e o `imagens.py` dessa versão.
2. **A casa:** a frase que se acende com o scroll, entre dois pormenores (a revista e a janela sobre os socalcos).
3. **A piscina:** a foto que cresce até ocupar o ecrã.
4. **Lá fora:** o terraço ao lado do texto; por baixo, a mesa posta e o relvado, da mesma altura.
5. **O coração da casa:** como a Casa da Vista Mágica no site da Quinta da Malhada. Abre com o aparador e a janela verde-azeitona a ecrã inteiro e o título (foto que não se repete no resto da página). Depois as divisões (a sala com a mesa, cozinha, suites, casas de banho) numa fila que, no computador, fica presa ao ecrã e desliza para o lado com o scroll, com contador e barra. No telemóvel desliza-se com o dedo. Cada divisão mostra quantas fotos tem, e um clique abre no visor só as fotos dela (séries `sala`, `cozinha`, `quartos` e `banhos` em `SERIES`; a sala junta a sala de estar e a mesa: 9 fotos). As suites (só os quartos) e as casas de banho aparecem legendadas por suite (Suite 1, 2 e 3), agrupadas a olho pelas fotos: confirmar com o dono. Na sala, a última foto é o canto do café (Nespresso, chávenas e vela). A foto da Nespresso das Comodidades só existe a 2560 px e pouco nítida (Airbnb): o `imagens.py` dá-lhe nitidez e menos compressão (`NITIDAS`); pedir o original ao dono.
6. **Comodidades:** dez ícones com poucas palavras, ao lado do pormenor da Nespresso.
7. **Hóspedes:** só o testemunho da Francisca.
8. **Experiências por perto:** no computador, a secção fica presa ao ecrã e a fila de fotos desliza na horizontal com o scroll. No telemóvel desliza-se com o dedo.
9. **Reservar:** a ficha da casa (casa inteira, 3 suites, até 8 pessoas, piscina), as condições da reserva direta, as regras da casa e a frase da Liliana e do Sérgio.

As fotos das experiências vêm do Wikimedia Commons, com licenças livres (CC BY e CC BY-SA), exceto a do restaurante, que é da casa (os petiscos com o cartão do Mira Freita; não dizer «take-away», que não está confirmado). Descarregam-se com `py scripts/experiencias.py`. As licenças obrigam a dar crédito: os créditos estão em `site/creditos.html`, ligada do rodapé («Créditos das fotografias»), e não na secção. O `imagens.py` não apaga as `exp-*`.

- **Telemóvel** (verificado a 360, 390 e 430 px ao alto e 844×390 deitado): sem scroll para os lados, letra de 13 px ou mais, alvos de toque de 40 px ou mais, LCP abaixo de 0,4 s e sem saltos (CLS 0). As filas deslizam com o dedo. Com o telemóvel deitado (altura até 520 px), as fotos medem-se pela altura do ecrã e as filas não ficam presas. Os `sizes` das imagens contam com o recorte (uma foto 3:2 num cartão 4:5 precisa de 1,9 vezes a largura). Só a piscina e o aparador, a ecrã inteiro ao alto, ficam abaixo da resolução ideal nos ecrãs @3x, porque os originais não são maiores.
- **Paleta**, a mesma do site da casa:

  | Tom | Hex | De onde vem |
  |---|---|---|
  | cal | #ffffff | o fundo branco do site da casa |
  | linho | #f4f0eb | taupe muito claro (a secção da citação) |
  | azeitona | #736f50 | o verde dos blocos do site, das portas e dos armários |
  | pinho (taupe) | #a9907f | o menu e os botões do site; as pedras do logótipo |
  | tinta | #1d1e1c | o quase-preto do site: texto e rodapé |

  O fundo da página muda de tom com a secção que está no meio do ecrã (`data-fundo` em cada secção; `main.js`, "TONS").
- **Letra**: Manrope fina (300) nos títulos, como a Helvetica Light do site da casa; Newsreader fina no título do hero ("Uma casa de granito sobre o vale") e, em itálico, nas citações.
- **Espaço**: secções bem separadas (`--secao` em `styles.css`), para a página respirar entre um bloco e o seguinte.
- **Hero** como o exemplo do Pátio da Gata: o nome enorme e translúcido sobre o céu, com cada letra em degradê (branca em cima, a fundir-se com a paisagem em baixo), letra a letra de desfocado para nítido; o título e uma frase ao centro, em baixo.
- **A casa**: uma frase só de texto (sem fotografias pelo meio, a pedido), que se acende palavra a palavra com o scroll; por baixo, os números da casa. A imagem do quadro ("janelas que parecem quadros") é a da própria casa e do testemunho que ela publica.
- **Movimento**:
  - scroll suave (Lenis, carregado do jsDelivr: se falhar, fica o scroll normal);
  - títulos que sobem ao entrar no ecrã;
  - a piscina que cresce, e só depois aparece o texto sobre a foto;
  - o acordeão "Por dentro" (no computador, a foto de cada painel tem a largura do painel aberto: abre-se sem mudar de zoom);
  - fotos que se revelam;
  - sobre as fotos que abrem o visor, só o cursor de lupa do sistema e uma aproximação lenta da foto.
- Com "movimento reduzido" no sistema, fica tudo no estado final e sem scroll suave.

O visor de fotografias usa o catálogo `SERIES` de `site/main.js`: só as fotos da página (7 por dentro, 4 lá fora). Para acrescentar uma foto: `scripts/imagens.py` e depois `SERIES`. As restantes fotos já estão em `site/assets/img/`, prontas para a galeria da versão completa.

Fotos deixadas de fora de propósito:
- as da MyConcierge (marca de água);
- as com pessoas e a bicicleta;
- as outras fotos da sala: só entra uma, de 2021, a pedido (a mobília pode ter mudado);
- a do terraço com a mobília antiga (refeicoes-05);
- as flores secas, que não acrescentavam nada.

Citações, todas em português ou inglês, com nome, plataforma e data:
- na piscina, Fabricio (Airbnb, junho de 2026);
- nos hóspedes, o testemunho de Francisca que a casa publica no seu site, e Mariana (Airbnb, junho de 2025), Monica (Airbnb, agosto de 2024) e Goomba (Airbnb, setembro de 2025);
- nas reservas, a frase da Liliana e do Sérgio no site da casa.

O site não mostra as notas das plataformas.

Depois de mexer no CSS ou no JS, subir o `?v=N` em `site/index.html`.

## Ver localmente

```
cd site
py -m http.server 8732
```
e abrir http://localhost:8732/.

## Antes de publicar o site definitivo (confirmar com o dono)

- Autorização para usar as fotos (são as do site atual, do Booking e do Airbnb, sessão de 2021).
- A mobília da sala: o site mostra a sala da sessão de 2021 (`sala`, de `interior/sala-05.jpg`), mas as fotos da MyConcierge têm outro sofá. Confirmar com o dono ou pedir uma foto atual.
- Condições da reserva direta (mínimo de 3 noites jun–set, cancelamento até 5 dias, pagamento): vêm do site de 2021 e o site mostra-as na secção Reservar.
- Época da piscina (abre em maio ou junho?). O site só diz que fecha no fim de outubro.
- Estacionamento: o site diz "gratuito na rua" (Airbnb); o Booking diz privado.
- Link do motor de reservas MyConcierge e o domínio final (o `canonical` e o `sitemap.xml` assumem https://casadagueira.pt/).
- Lista completa em `dossie/resumo.md` › "Por confirmar".

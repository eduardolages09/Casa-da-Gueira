"""Gera site/en/index.html a partir de site/index.html.

Cada par (português, inglês) tem de existir no HTML português: se uma frase
mudar lá e não aqui, o script pára e diz qual. Correr depois de qualquer
alteração ao texto português:  py scripts/traduzir-en.py
(A versão 1 do site e o seu tradutor estão em arquivo/.)"""
import os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pt = open(os.path.join(RAIZ, 'site', 'index.html'), encoding='utf-8').read()
s = pt

PARES = [
    # cabeça
    ('<html lang="pt-PT">', '<html lang="en">'),
    ('<title>Casa da Gueira — Casa de granito com piscina sobre o vale, em Felgueira</title>',
     '<title>Casa da Gueira — Granite house with a pool over the valley, in Felgueira, Portugal</title>'),
    ('content="Casa de granito para até 8 pessoas na aldeia de Felgueira, Vale de Cambra: três suites, piscina de água salgada virada ao vale e a Serra da Freita à porta. Alojamento Local 110255/AL."',
     'content="Granite house for up to 8 guests in the village of Felgueira, Vale de Cambra, Portugal: three en-suite bedrooms, a saltwater pool facing the valley and the Serra da Freita on the doorstep. Licence 110255/AL."'),
    ('content="Casa da Gueira — Casa de granito com piscina sobre o vale"', 'content="Casa da Gueira — Granite house with a pool over the valley"'),
    ('content="Três suites, até 8 pessoas, piscina de água salgada e a aldeia de Felgueira à volta. Vale de Cambra, a um passo da Serra da Freita."',
     'content="Three en-suite bedrooms, up to 8 guests, a saltwater pool and the village of Felgueira all around. Vale de Cambra, Portugal, close to the Serra da Freita."'),
    ('<meta property="og:locale" content="pt_PT">', '<meta property="og:locale" content="en_GB">'),
    ('<link rel="canonical" href="https://casadagueira.pt/">', '<link rel="canonical" href="https://casadagueira.pt/en/">'),
    ('"description": "Casa de granito para até 8 pessoas na aldeia de Felgueira, freguesia de Arões, Vale de Cambra, com três suites e piscina privada de água salgada."',
     '"description": "Granite house for up to 8 guests in the village of Felgueira, Arões, Vale de Cambra, Portugal, with three en-suite bedrooms and a private saltwater pool."'),
    ('"url": "https://casadagueira.pt/"', '"url": "https://casadagueira.pt/en/"'),
    ('"name": "Piscina privada exterior de água salgada"', '"name": "Private outdoor saltwater pool"'),
    ('"name": "Ar condicionado"', '"name": "Air conditioning"'),
    ('"name": "Wi-Fi gratuito"', '"name": "Free Wi-Fi"'),
    ('"name": "Cozinha equipada"', '"name": "Fully equipped kitchen"'),
    ('"name": "Churrasqueira"', '"name": "Barbecue"'),
    # topo
    ('<a class="salto" href="#main">Saltar para o conteúdo</a>', '<a class="salto" href="#main">Skip to content</a>'),
    ('aria-label="Casa da Gueira, início"', 'aria-label="Casa da Gueira, home"'),
    ('aria-label="Navegação principal"', 'aria-label="Main navigation"'),
    ('<li><a href="#casa">A casa</a></li>', '<li><a href="#casa">The house</a></li>'),
    ('<li><a href="#piscina">A piscina</a></li>', '<li><a href="#piscina">The pool</a></li>'),
    ('<li><a href="#dentro">Por dentro</a></li>', '<li><a href="#dentro">Inside</a></li>'),
    ('<li><a href="#fora">Lá fora</a></li>', '<li><a href="#fora">Outside</a></li>'),
    ('<li><a href="#aldeia">A aldeia</a></li>', '<li><a href="#aldeia">The village</a></li>'),
    ('<a href="en/" class="nav__lingua" lang="en" hreflang="en" aria-label="Read this page in English">EN</a>',
     '<a href="../" class="nav__lingua" lang="pt-PT" hreflang="pt-PT" aria-label="Ler esta página em português">PT</a>'),
    ('class="botao botao--pequeno nav__reservar">Reservar</a>', 'class="botao botao--pequeno nav__reservar">Book</a>'),
    ('aria-label="Abrir o menu"', 'aria-label="Open the menu"'),
    # hero
    ('alt="A piscina de água salgada da Casa da Gueira, com o relvado, a casa de granito e o vale ao fundo"',
     'alt="The saltwater pool at Casa da Gueira, with the lawn, the granite house and the valley beyond"'),
    # a casa
    ('<h2 class="invisivel" id="casa-titulo">A casa</h2>', '<h2 class="invisivel" id="casa-titulo">The house</h2>'),
    ('alt="Uma janela aberta da casa sobre a encosta em socalcos, com giestas em flor"', 'alt="An open window of the house onto the terraced hillside, with broom in flower"'),
    ('<span class="invisivel">Casa da Gueira: </span>Uma casa de granito sobre o vale</h1>', '<span class="invisivel">Casa da Gueira: </span>A granite house above the valley</h1>'),
    ('<p class="hero__sub">Três suites, uma piscina de água salgada e a aldeia de Felgueira à volta, a um passo da Serra da Freita.</p>',
     '<p class="hero__sub">Three en-suite bedrooms, a saltwater pool and the village of Felgueira all around, close to the Serra da Freita.</p>'),
    ('aria-label="Descer para a casa"', 'aria-label="Scroll down to the house"'),
    # a casa: a frase com fotografias, troço a troço
    ('<p class="acende" data-acende>Paredes de granito <span', '<p class="acende" data-acende>Granite walls <span'),
    ('</span>, madeira clara <span', '</span>, pale wood <span'),
    ('</span> e portas verde-azeitona <span', '</span> and olive-green doors <span'),
    ('</span>. Três suites, uma mesa comprida <span', '</span>. Three en-suite bedrooms, a long table <span'),
    ('</span> e, lá fora, uma piscina <span', '</span> and, outside, a pool <span'),
    ('</span> virada ao vale.</p>', '</span> facing the valley.</p>'),
    ('<li><b>3</b><span>suites, cada uma com a sua casa de banho</span></li>', '<li><b>3</b><span>bedrooms, each with its own bathroom</span></li>'),
    ('<li><b>8</b><span>pessoas, com a casa só para o seu grupo</span></li>', '<li><b>8</b><span>guests, with the house to your group alone</span></li>'),
    ('<li><b>100&nbsp;m²</b><span>de casa, na aldeia de Felgueira</span></li>', '<li><b>100&nbsp;m²</b><span>of house, in the village of Felgueira</span></li>'),
    ('<li><b>12&nbsp;m</b><span>de piscina de água salgada</span></li>', '<li><b>12&nbsp;m</b><span>of saltwater pool</span></li>'),
    # piscina
    ('alt="A água da piscina em primeiro plano e, logo a seguir, a encosta em socalcos com giestas em flor e casas da aldeia"',
     'alt="The pool water in the foreground and, just beyond, the terraced hillside with broom in flower and village houses"'),
    ('<h2 class="cresce__titulo" id="piscina-titulo"><span>A piscina</span> <span>sobre o vale</span></h2>',
     '<h2 class="cresce__titulo" id="piscina-titulo"><span>The pool</span> <span>over the valley</span></h2>'),
    ('aria-label="Ver a piscina em grande"', 'aria-label="See the pool full size"'),
    ('alt="A piscina comprida vista de uma ponta, com a escada de inox, o relvado e a casa de granito ao fundo"',
     'alt="The long pool seen from one end, with the steel ladder, the lawn and the granite house beyond"'),
    ('<p class="lead">Água salgada, 12 × 3,5 m, com relvado e espreguiçadeiras à volta. Aberta na época quente; fecha no fim de outubro.</p>',
     '<p class="lead">Saltwater, 12 × 3.5 m, with a lawn and loungers around it. Open in the warm months; it closes at the end of October.</p>'),
    ('<p class="voz__traducao">Uma piscina maravilhosa, com vista sobre uma zona sossegada.</p>', '<p class="voz__traducao">A wonderful pool with a view over a quiet area.</p>'),
    ('<footer>Iwona, no Airbnb, agosto de 2023</footer>', '<footer>Iwona, on Airbnb, August 2023</footer>'),
    ('aria-label="Ver o terraço em grande"', 'aria-label="See the terrace full size"'),
    ('alt="A mesa posta no terraço, à sombra do guarda-sol, com a piscina e os socalcos atrás"',
     'alt="The table laid on the terrace, in the shade of the parasol, with the pool and the terraces behind"'),
    # por dentro
    ('<h2 class="titulo" id="dentro-titulo">Por dentro</h2>', '<h2 class="titulo" id="dentro-titulo">Inside</h2>'),
    ('<p class="lead">Paredes de pedra, madeira clara e verde-azeitona nas portas e nos armários. Cada suite tem a sua casa de banho.</p>',
     '<p class="lead">Stone walls, pale wood and olive green on the doors and cupboards. Every bedroom has its own bathroom.</p>'),
    ('<span class="painel__nome">A mesa comprida</span>', '<span class="painel__nome">The long table</span>'),
    ('<span class="painel__nome">A cozinha</span>', '<span class="painel__nome">The kitchen</span>'),
    ('<span class="painel__nome">As suites</span>', '<span class="painel__nome">The bedrooms</span>'),
    ('<span class="painel__nome">As casas de banho</span>', '<span class="painel__nome">The bathrooms</span>'),
    ('<span class="painel__nome">O granito à vista</span>', '<span class="painel__nome">Bare granite</span>'),
    ('<span class="painel__nome">A escada</span>', '<span class="painel__nome">The stairs</span>'),
    ('<span class="painel__nome">Os pormenores</span>', '<span class="painel__nome">The details</span>'),
    ('<li>Ar condicionado e aquecimento</li>', '<li>Air conditioning and heating</li>'),
    ('<li>Cozinha Smeg e forno a lenha</li>', '<li>Smeg kitchen and wood-fired oven</li>'),
    ('<li>Máquinas de lavar loiça e roupa</li>', '<li>Dishwasher and washing machine</li>'),
    ('data-serie="dentro">Ver as <span id="dentroTotal">22</span> fotografias</button>', 'data-serie="dentro">See all <span id="dentroTotal">22</span> photos</button>'),
    # lá fora
    ('<h2 class="titulo" id="fora-titulo">Almoços ao pé da água</h2>', '<h2 class="titulo" id="fora-titulo">Lunch by the water</h2>'),
    ('<p class="lead">Um terraço de lajes de granito, com mesa comprida, guarda-sol e churrasqueira a carvão. Ao lado, o relvado e um chuveiro exterior.</p>',
     '<p class="lead">A granite-paved terrace with a long table, a parasol and a charcoal barbecue. Alongside, the lawn and an outdoor shower.</p>'),
    ('data-serie="fora">Ver as <span id="foraTotal">16</span> fotografias</button>', 'data-serie="fora">See all <span id="foraTotal">16</span> photos</button>'),
    ('aria-label="Ver a mesa do terraço em grande"', 'aria-label="See the terrace table full size"'),
    ('alt="A mesa de madeira posta no terraço, à sombra do guarda-sol, com a piscina e a encosta em socalcos atrás"',
     'alt="The wooden table laid on the terrace, in the shade of the parasol, with the pool and the terraced hillside behind"'),
    ('aria-label="Ver a mesa posta em grande"', 'aria-label="See the laid table full size"'),
    ('alt="Pratos e copos na mesa de madeira, com a água da piscina ao lado"', 'alt="Plates and glasses on the wooden table, with the pool water alongside"'),
    ('aria-label="Ver o relvado em grande"', 'aria-label="See the lawn full size"'),
    ('alt="O relvado entre o muro de granito e a piscina, com duas espreguiçadeiras e o vale ao fundo"', 'alt="The lawn between the granite wall and the pool, with two loungers and the valley beyond"'),
    # hóspedes: a tradução em grande, o original em português por baixo
    ('<h2 class="invisivel" id="hospedes-titulo">O que dizem os hóspedes</h2>', '<h2 class="invisivel" id="hospedes-titulo">What guests say</h2>'),
    ('<p>«Fomos recebidos com um delicioso bolo de laranja de boas-vindas, um gesto simples mas que demonstra o cuidado e carinho com que os hóspedes são recebidos.»</p>',
     '<p>“We were welcomed with a delicious orange cake, a simple gesture that shows the care and warmth with which guests are received.”</p>\n'
     '          <p class="destaque__original" lang="pt-PT">«Fomos recebidos com um delicioso bolo de laranja de boas-vindas, um gesto simples mas que demonstra o cuidado e carinho com que os hóspedes são recebidos.»</p>'),
    ('<figcaption>Fabricio, no Airbnb, junho de 2026</figcaption>', '<figcaption>Fabricio, on Airbnb, June 2026 (translated from Portuguese)</figcaption>'),
    ('<li><b>4,88</b><span>de 5 no Airbnb, em 33 avaliações</span></li>', '<li><b>4.88</b><span>out of 5 on Airbnb, from 33 reviews</span></li>'),
    ('<li><b>5,0</b><span>de 5 no Google, em 5 críticas</span></li>', '<li><b>5.0</b><span>out of 5 on Google, from 5 reviews</span></li>'),
    ('<li><b>8,6</b><span>de 10 no Booking, em 5 avaliações</span></li>', '<li><b>8.6</b><span>out of 10 on Booking.com, from 5 reviews</span></li>'),
    ('<p class="notas__data">Notas vistas nas plataformas em setembro de 2026. <a href="https://www.airbnb.pt/rooms/49923714/reviews" target="_blank" rel="noopener">Ler as avaliações no Airbnb</a></p>',
     '<p class="notas__data">Ratings as shown on each platform in September 2026. <a href="https://www.airbnb.com/rooms/49923714/reviews" target="_blank" rel="noopener">Read the reviews on Airbnb</a></p>'),
    # aldeia
    ('alt="A Casa da Gueira vista do ar, entre as casas de pedra da aldeia: o terraço, a piscina sobre o muro de granito e o relvado"',
     'alt="Casa da Gueira from the air, among the stone houses of the village: the terrace, the pool on its granite wall and the lawn"'),
    ('<h2 class="titulo" id="aldeia-titulo">A aldeia de Felgueira</h2>', '<h2 class="titulo" id="aldeia-titulo">The village of Felgueira</h2>'),
    ('<p class="lead">Casas de granito e hortas em socalcos, a um passo da Serra da Freita.</p>', '<p class="lead">Granite houses and terraced plots, close to the Serra da Freita.</p>'),
    ('<li><b>2 min a pé</b><span>Restaurante Mira Freita, na aldeia</span></li>', '<li><b>2 min walk</b><span>Mira Freita restaurant, in the village</span></li>'),
    ('<li><b>1 km</b><span>Casa das Pedras Parideiras</span></li>', '<li><b>1 km</b><span>Casa das Pedras Parideiras, the “birthing stones” centre</span></li>'),
    ('<li><b>1,5 km</b><span>Estação Meteorológica</span></li>', '<li><b>1.5 km</b><span>The weather station</span></li>'),
    ('<li><b>40 min</b><span>Aldeias da Pena e de Drave</span></li>', '<li><b>40 min</b><span>The villages of Pena and Drave</span></li>'),
    ('<li><b>50 min</b><span>Passadiços do Paiva</span></li>', '<li><b>50 min</b><span>Paiva Walkways (Passadiços do Paiva)</span></li>'),
    ('<p class="aldeia__nota"><span>Distâncias indicadas pela casa. Rua da Aldeia Antiga, 115, Felgueira, 3730-009 Arões, Vale de Cambra.</span>',
     '<p class="aldeia__nota"><span>Distances as given by the house. Rua da Aldeia Antiga, 115, Felgueira, 3730-009 Arões, Vale de Cambra, Portugal.</span>'),
    ('target="_blank" rel="noopener">Abrir o caminho no Google Maps</a>', 'target="_blank" rel="noopener">Get directions on Google Maps</a>'),
    # reservar
    ('alt="A mesa e o banco de madeira no terraço, à sombra do guarda-sol, com a piscina e a encosta em socalcos atrás"',
     'alt="The wooden table and bench on the terrace, in the shade of the parasol, with the pool and the terraced hillside behind"'),
    ('<h2 class="titulo" id="reservar-titulo">Reserve a casa inteira</h2>', '<h2 class="titulo" id="reservar-titulo">Book the whole house</h2>'),
    ('<p class="lead">Veja as datas livres e reserve diretamente, ou fale connosco.</p>', '<p class="lead">See which dates are free and book direct, or get in touch.</p>'),
    ('https://web.ynnovbooking.com/booking/?l=pt&amp;apikey', 'https://web.ynnovbooking.com/booking/?l=en&amp;apikey'),
    ('class="botao botao--pinho" target="_blank" rel="noopener">Ver datas e reservar', 'class="botao botao--pinho" target="_blank" rel="noopener">Check dates and book'),
    ('<a href="tel:+351927221952" class="botao botao--linha">Ligar 927 221 952</a>', '<a href="tel:+351927221952" class="botao botao--linha">Call +351 927 221 952</a>'),
    ('<a href="mailto:reservas@casadagueira.pt" class="botao botao--linha">Enviar email</a>', '<a href="mailto:reservas@casadagueira.pt" class="botao botao--linha">Send an email</a>'),
    ('<p class="reservar__outros">Também no <a href="https://www.airbnb.pt/rooms/49923714" target="_blank" rel="noopener">Airbnb</a> e no <a href="https://www.booking.com/hotel/pt/casa-da-gueira.pt-pt.html" target="_blank" rel="noopener">Booking</a>.</p>',
     '<p class="reservar__outros">Also on <a href="https://www.airbnb.com/rooms/49923714" target="_blank" rel="noopener">Airbnb</a> and <a href="https://www.booking.com/hotel/pt/casa-da-gueira.en-gb.html" target="_blank" rel="noopener">Booking.com</a>.</p>'),
    ('<h3>Na reserva direta</h3>', '<h3>When you book direct</h3>'),
    ('<li>Reembolso total se cancelar até 5 dias antes da chegada</li>', '<li>Full refund if you cancel up to 5 days before arrival</li>'),
    ('<li>Mínimo de 3 noites de junho a setembro</li>', '<li>Minimum stay of 3 nights from June to September</li>'),
    ('<li>Transferência bancária ou cartão de crédito</li>', '<li>Bank transfer or credit card</li>'),
    ('<h3>Na casa</h3>', '<h3>At the house</h3>'),
    ('<li>Entrada a partir das 16:00, saída até às 11:00</li>', '<li>Check-in from 4 pm, check-out by 11 am</li>'),
    ('<li>Sem animais, festas nem eventos</li>', '<li>No pets, parties or events</li>'),
    ('<li>Estacionamento gratuito na rua</li>', '<li>Free parking on the street</li>'),
    # perguntas
    ('<h2 class="titulo" id="perguntas-titulo">Antes de vir</h2>', '<h2 class="titulo" id="perguntas-titulo">Before you come</h2>'),
    ('<summary>Quantas pessoas cabem na casa?</summary>\n          <p>Até 8 pessoas: três suites com cama de casal e casa de banho privativa, e um sofá-cama na sala.</p>',
     '<summary>How many people does the house sleep?</summary>\n          <p>Up to 8: three bedrooms, each with a double bed and its own bathroom, plus a sofa bed in the living room.</p>'),
    ('<summary>A piscina está aberta todo o ano?</summary>\n          <p>Não. A piscina funciona na época quente e fecha no fim de outubro. Se vier no início ou no fim da época, confirme connosco as datas.</p>',
     '<summary>Is the pool open all year?</summary>\n          <p>No. The pool is open in the warm months and closes at the end of October. If you are coming at the start or end of the season, check the dates with us.</p>'),
    ('<summary>Posso ir com crianças?</summary>\n          <p>Sim. Há cadeira alta e, a pedido, berço. A piscina não tem vedação nem portão: as crianças pequenas precisam de estar sempre acompanhadas.</p>',
     '<summary>Can we bring children?</summary>\n          <p>Yes. There is a high chair and, on request, a cot. The pool has no fence or gate, so young children must be supervised at all times.</p>'),
    ('<summary>As refeições estão incluídas?</summary>\n          <p>Não. A casa tem cozinha completa, forno a lenha e churrasqueira, e o restaurante da aldeia fica a 2 minutos a pé.</p>',
     '<summary>Are meals included?</summary>\n          <p>No. The house has a full kitchen, a wood-fired oven and a barbecue, and the village restaurant is a 2-minute walk away.</p>'),
    ('<summary>Posso levar o meu cão?</summary>\n          <p>Não. A casa não aceita animais.</p>',
     '<summary>Can I bring my dog?</summary>\n          <p>No. Pets are not allowed.</p>'),
    ('<summary>A que horas posso chegar?</summary>\n          <p>A partir das 16:00; a saída é até às 11:00. Avise-nos da hora de chegada. À entrada da casa há uma câmara de segurança virada para o portão e para o cofre das chaves.</p>',
     '<summary>What time can we arrive?</summary>\n          <p>From 4 pm; check-out is by 11 am. Please let us know your arrival time. There is a security camera at the entrance, facing the gate and the key box.</p>'),
    # rodapé
    ('aria-label="Casa da Gueira, voltar ao início"', 'aria-label="Casa da Gueira, back to top"'),
    ('<span>Rua da Aldeia Antiga, 115, Felgueira<br>3730-009 Arões, Vale de Cambra</span>', '<span>Rua da Aldeia Antiga, 115, Felgueira<br>3730-009 Arões, Vale de Cambra, Portugal</span>'),
    ('<span><a href="tel:+351927221952">927 221 952</a> e <a href="tel:+351917106121">917 106 121</a><br>',
     '<span><a href="tel:+351927221952">+351 927 221 952</a> and <a href="tel:+351917106121">+351 917 106 121</a><br>'),
    ('<p>Alojamento Local n.º 110255/AL. &copy; <span id="ano">2026</span> Casa da Gueira.</p>',
     '<p>Alojamento Local (registered holiday let) no. 110255/AL. &copy; <span id="ano">2026</span> Casa da Gueira.</p>'),
    ('<p>Em caso de litígio, o consumidor pode recorrer ao CNIACC — Centro Nacional de Informação e Arbitragem de Conflitos de Consumo (253 619 107, <a href="mailto:geral@cniacc.pt">geral@cniacc.pt</a>).</p>',
     '<p>In case of dispute, consumers may turn to CNIACC, the Portuguese National Centre for Consumer Dispute Arbitration (+351 253 619 107, <a href="mailto:geral@cniacc.pt">geral@cniacc.pt</a>).</p>'),
    ('target="_blank" rel="noopener">Livro de Reclamações</a>', 'target="_blank" rel="noopener">Complaints book (Livro de Reclamações)</a>'),
    ('target="_blank" rel="noopener">Política de privacidade</a>', 'target="_blank" rel="noopener">Privacy policy</a>'),
    ('<a href="#reservar" class="cta-fixo" id="ctaFixo">Reservar</a>', '<a href="#reservar" class="cta-fixo" id="ctaFixo">Book</a>'),
    # visor
    ('aria-label="Fechar"><svg', 'aria-label="Close"><svg'),
    ('aria-label="Fotografia anterior"', 'aria-label="Previous photo"'),
    ('aria-label="Fotografia seguinte"', 'aria-label="Next photo"'),
]

falta = [a for a, b in PARES if a not in s]
if falta:
    print('Frases que já não existem no HTML português (atualizar PARES):')
    for a in falta:
        print('  ', a[:120])
    sys.exit(1)
for a, b in PARES:
    s = s.replace(a, b)

# caminhos: a página inglesa vive em /en/
s = s.replace('"assets/', '"../assets/').replace(', assets/', ', ../assets/')
s = s.replace('href="styles.css', 'href="../styles.css').replace('src="main.js', 'src="../main.js')
s = s.replace('content="assets/img/', 'content="../assets/img/')

# a abertura fica igual; o JS descobre a língua pelo <html lang>
os.makedirs(os.path.join(RAIZ, 'site', 'en'), exist_ok=True)
open(os.path.join(RAIZ, 'site', 'en', 'index.html'), 'w', encoding='utf-8', newline='\n').write(s)

# o que ficou em português (para rever à mão)
texto = re.sub(r'<script.*?</script>|<svg.*?</svg>|<style.*?</style>', ' ', s, flags=re.S)
texto = re.sub(r'<[^>]+>', '\n', texto)
suspeitas = [l.strip() for l in texto.split('\n') if re.search(r'[ãõçáéíóúâêô]', l) and l.strip()]
print(len(PARES), 'frases traduzidas. Linhas com acentos portugueses (rever):')
for l in suspeitas:
    print('  ', l[:140])

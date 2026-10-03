"""Copia as fotos escolhidas do dossiê para o site, com nome próprio e três
tamanhos (original até 2400 px, 1400 px e 800 px; o hero leva também 2000 px).
Os originais do dossiê nunca são tocados.

Para acrescentar uma foto: pôr a linha ('<pasta>/<ficheiro do dossiê>', '<nome>')
em FOTOS, correr `py scripts/imagens.py` e usar o nome no HTML ou no catálogo
SERIES de site/main.js. Grava scripts/tamanhos-imagens.json com as medidas.
As fotos que saírem de FOTOS são apagadas de site/assets/img."""
import os, json, re
import numpy as np
from PIL import Image, ImageOps, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, 'dossie', 'marketing', 'fotos') + '/'
DST = os.path.join(RAIZ, 'site', 'assets', 'img') + '/'
os.makedirs(DST, exist_ok=True)

# Só fotos da sessão de 2021 e do Airbnb: sem marca de água, sem pessoas e
# sem a bicicleta (as da MyConcierge têm marca de água — contrato: uso
# «restrito»; bicicletas: «não usar»). Sem a sala: a mobília pode ter mudado
# desde 2021 (dossiê, fontes.md › Mobília da sala). Sem refeicoes-05: mostra
# a mobília antiga do terraço (cadeiras e mesa de ripas, cobertura azul).
FOTOS = [
    # exterior
    ('exterior/piscina-01.jpg', 'piscina-borda'),
    ('exterior/piscina-08.jpg', 'piscina-comprida'),
    ('exterior/piscina-02.jpg', 'piscina-casa'),
    ('exterior/piscina-04.jpg', 'piscina-relvado'),
    ('exterior/piscina-07.jpg', 'piscina-muro'),
    ('exterior/piscina-06.jpg', 'piscina-solario'),
    ('exterior/refeicoes-02.jpg', 'terraco-mesa'),
    ('exterior/refeicoes-07.jpg', 'terraco-loica'),
    ('exterior/refeicoes-06.jpg', 'terraco-quadrado'),
    ('exterior/refeicoes-03.jpg', 'mesa-posta'),
    ('exterior/jardim-01.jpg', 'relvado'),
    ('exterior/detalhe-04.jpg', 'grelhador'),
    ('exterior/detalhe-03.jpg', 'revista'),
    ('exterior/refeicoes-04.jpg', 'mira-freita'),   # petiscos com o cartão do Mira Freita (não dizer take-away)
    ('exterior/vista-01.jpg', 'janela-socalcos'),
    ('exterior/vista-02.jpg', 'janela-piscina'),
    ('exterior/fachada-02.jpg', 'casa-aldeia'),
    ('exterior/fachada-01.jpg', 'casa-planta'),
    # interior
    ('interior/refeicoes-01.jpg', 'mesa-comprida'),
    ('interior/refeicoes-02.jpg', 'mesa-janelas'),
    ('interior/refeicoes-03.jpg', 'mesa-cima'),
    ('interior/refeicoes-05.jpg', 'aparador'),        # fundo da abertura "O coração da casa"
    ('interior/cozinha-01.jpg', 'cozinha'),
    ('interior/cozinha-03.jpg', 'fogao'),
    ('interior/cozinha-04.jpg', 'frigorifico'),
    ('interior/cozinha-05.jpg', 'bancada'),
    ('interior/quarto-01.jpg', 'suite-janelas'),
    ('interior/quarto-02.jpg', 'suite-cama'),
    ('interior/quarto-05.jpg', 'suite-janela-alta'),
    ('interior/quarto-08.jpg', 'suite-encosta'),
    ('interior/quarto-07.jpg', 'suite-roupeiros'),
    ('interior/quarto-04.jpg', 'suite-wc'),
    ('interior/casa-de-banho-04.jpg', 'wc-espelho'),
    ('interior/casa-de-banho-02.jpg', 'wc-lavatorio'),
    ('interior/casa-de-banho-05.jpg', 'wc-duche'),
    ('interior/casa-de-banho-01.jpg', 'wc'),
    ('interior/corredor-02.jpg', 'corredor-granito'),
    ('interior/escada-01.jpg', 'escada'),
    ('interior/detalhe-01.jpg', 'cafe'),
    ('interior/detalhe-02.jpg', 'armario-loica'),
    ('interior/detalhe-03.jpg', 'flores'),
    ('interior/detalhe-04.jpg', 'nespresso'),
    ('interior/sala-05.jpg', 'sala'),
    ('interior/sala-01.jpg', 'sala-tv'),
    ('interior/sala-03.jpg', 'sala-escada'),
    ('interior/sala-02.jpg', 'sala-mesa'),
    # as três suites, para o visor "quartos" (agrupadas a olho: confirmar com o dono)
    ('interior/casa-de-banho-08.jpg', 'suite1-wc'),
    ('interior/casa-de-banho-09.jpg', 'suite1-lavatorio'),
    ('interior/quarto-06.jpg', 'suite2-lavatorio'),
    ('interior/casa-de-banho-03.jpg', 'suite2-wc'),
    ('interior/quarto-12.jpg', 'suite3'),
    ('interior/quarto-11.jpg', 'suite3-cama'),
    ('interior/casa-de-banho-06.jpg', 'suite3-wc'),
    ('interior/casa-de-banho-07.jpg', 'suite3-duche'),        # pedida pelo utilizador; mobília de 2021 por confirmar
]

# cortes (frações: esquerda, cima, direita, baixo)
CORTES = {
    'casa-aldeia': (0, 0.36, 1, 1),        # tira os prédios vizinhos de cima
}
COM_2000 = {'piscina-borda'}
# fotos que só existem pouco nítidas (o Airbnb serve no máximo 2560 px):
# um pouco de nitidez em cada tamanho e menos compressão
NITIDAS = {'nespresso'}
# fundos a ecrã inteiro no telemóvel ao alto: guardam o original até 3000 px
MAXIMO = {'aparador': 3000}
QUALIDADE = {}

tam = {}
for src, nome in FOTOS:
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert('RGB')
    if nome in CORTES:
        e, c, d, b = CORTES[nome]
        im = im.crop((round(im.width * e), round(im.height * c), round(im.width * d), round(im.height * b)))
    lim = MAXIMO.get(nome, 2400)
    if max(im.size) > lim:
        im.thumbnail((lim, lim), Image.LANCZOS)
    q = QUALIDADE.get(nome, 90 if nome in NITIDAS else 80)
    afia = (lambda x: x.filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))) if nome in NITIDAS else (lambda x: x)
    afia(im).save(f'{DST}{nome}.jpg', quality=q, optimize=True, progressive=True)
    medidas = {'full': list(im.size)}
    larguras = (2000, 1400, 800) if nome in COM_2000 else (1400, 800)
    for s in larguras:
        if im.width > s:
            cp = im.copy()
            cp.thumbnail((s, 10000), Image.LANCZOS)
            afia(cp).save(f'{DST}{nome}-{s}.jpg', quality=q - 2, optimize=True, progressive=True)
            medidas[str(s)] = list(cp.size)
    tam[nome] = medidas
    print(nome, medidas)

# ---- o FILME do hero (main.js, "FILME"): quatro planos e o primeiro ao alto.
# Saem do original sem passar dos 3000 px, com pouca compressão e com o tom
# do site já aplicado (antes era um filtro CSS, que pesava no movimento e
# tirava nitidez). O CSS desenha-os a 112 % e só os reduz, nunca os amplia.
FILME = [
    ('exterior/piscina-03.jpg', 'filme-piscina', None),
    ('exterior/piscina-08.jpg', 'filme-alto', (0.25, 0, 0.75, 1)),   # o 1.º plano no telemóvel ao alto
    ('exterior/fachada-01.jpg', 'filme-planta', None),
    ('exterior/fachada-05.jpg', 'filme-drone', None),
    ('exterior/refeicoes-07.jpg', 'filme-terraco', None),
]
# o tom do site: saturate(0.88) e depois sepia(0.08), como no CSS (Filter Effects, em sRGB)
s_, a_ = 0.88, 0.08
SAT = np.array([[0.213 + 0.787 * s_, 0.715 - 0.715 * s_, 0.072 - 0.072 * s_],
                [0.213 - 0.213 * s_, 0.715 + 0.285 * s_, 0.072 - 0.072 * s_],
                [0.213 - 0.213 * s_, 0.715 - 0.715 * s_, 0.072 + 0.928 * s_]])
SEP = (1 - a_) * np.eye(3) + a_ * np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
TOM = SEP @ SAT
for src, nome, corte in FILME:
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert('RGB')
    if corte:
        e, c, d, b = corte
        im = im.crop((round(im.width * e), round(im.height * c), round(im.width * d), round(im.height * b)))
    if max(im.size) > 3000:
        im.thumbnail((3000, 3000), Image.LANCZOS)
    px = np.asarray(im).astype(np.float32) @ TOM.T
    im = Image.fromarray(np.clip(px + 0.5, 0, 255).astype(np.uint8))
    im.save(f'{DST}{nome}.jpg', quality=90, optimize=True, progressive=True, subsampling=0)
    medidas = {'full': list(im.size)}
    for s in (2400, 2000, 1400, 800):
        if im.width > s * 1.05:
            cp = im.copy(); cp.thumbnail((s, 10000), Image.LANCZOS)
            cp.save(f'{DST}{nome}-{s}.jpg', quality=88, optimize=True, progressive=True, subsampling=0 if s >= 2000 else 2)
            medidas[str(s)] = list(cp.size)
    tam[nome] = medidas
    print(nome, medidas)

# apaga o que já não está na lista (as exp-* vêm do Wikimedia Commons: scripts/experiencias.py)
nomes = {n for _, n in FOTOS} | {n for _, n, _ in FILME}
for f in os.listdir(DST):
    m = re.match(r'^(.*?)(-\d{3,4})?\.jpg$', f)
    if m and m.group(1) not in nomes and not f.startswith('exp-'):
        os.remove(DST + f)
        print('apagada', f)
json.dump(tam, open(os.path.join(RAIZ, 'scripts', 'tamanhos-imagens.json'), 'w'), indent=1)

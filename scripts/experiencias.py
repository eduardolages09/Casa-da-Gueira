"""Descarrega do Wikimedia Commons as fotografias das experiências (licenças
livres) para site/assets/img/exp-*.jpg, em três tamanhos, e grava os créditos
em scripts/experiencias-creditos.json. O site mostra os créditos por baixo
da secção (obrigatório nas licenças CC BY e CC BY-SA).

Uso: py scripts/experiencias.py"""
import os, json, urllib.request, urllib.parse
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(RAIZ, 'site', 'assets', 'img') + '/'
UA = {'User-Agent': 'CasaGueiraSite/1.0 (reservas@casadagueira.pt)'}

FOTOS = {
    'exp-paiva': ('Passadiços do Paiva Paiva walkways (39681956172).jpg', 'Luis Ascenso', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0'),
    'exp-drave': ('Drave 5.jpg', 'Paulo Manuel Monteiro Gomes', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0'),
    'exp-pedras': ('Pedras Parideiras da Serra da Freita 5.jpg', 'Cssantos', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0'),
    'exp-freita': ('Serra da Freita e Arada. GeoParque Arouca 143.jpg', 'Ricardo Oliveira', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0'),
    'exp-percursos': ('Blooming of flowers in Serra da Freita, April 2022.jpg', 'Gabi4754', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0'),
}

creditos = {}
for nome, (ficheiro, autor, licenca, url_licenca) in FOTOS.items():
    url = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(ficheiro) + '?width=2400'
    tmp = DST + nome + '-tmp.jpg'
    open(tmp, 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
    im = Image.open(tmp).convert('RGB'); os.remove(tmp)
    if max(im.size) > 2400: im.thumbnail((2400, 2400), Image.LANCZOS)
    im.save(DST + nome + '.jpg', quality=84, optimize=True, progressive=True)
    for t in (1400, 800):
        cp = im.resize((t, round(im.height * t / im.width)), Image.LANCZOS)
        cp.save(f'{DST}{nome}-{t}.jpg', quality=82, optimize=True, progressive=True)
    creditos[nome] = {'ficheiro': ficheiro, 'pagina': 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(ficheiro.replace(' ', '_')),
                      'autor': autor, 'licenca': licenca, 'licenca_url': url_licenca}
    print(nome, im.size)
json.dump(creditos, open(os.path.join(RAIZ, 'scripts', 'experiencias-creditos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

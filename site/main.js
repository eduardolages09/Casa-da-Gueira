/* Casa da Gueira — interações (versão 3)
   Um IIFE só, sem dependências. Cada bloco trata de uma parte da página.
   A abertura (as pedras do logótipo) e a entrada do nome são só CSS.
   Os efeitos de scroll escrevem variáveis CSS; o desenho está em styles.css. */
(function () {
  'use strict';

  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // a versão inglesa (extra da versão completa, scripts/traduzir-en.py) usa o mesmo ficheiro
  var EN = document.documentElement.lang === 'en';
  var T = EN
    ? { de: ' of ', abrir: 'Open the menu', fechar: 'Close the menu', foto: 'Photo ' }
    : { de: ' de ', abrir: 'Abrir o menu', fechar: 'Fechar o menu', foto: 'Fotografia ' };
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var limita = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* ------------------------------------------------------------
     CATÁLOGO DE FOTOGRAFIAS (o visor)
     { f: nome do ficheiro em assets/img (sem extensão), l: legenda, e: legenda em inglês }.
     Cada foto tem as cópias -800 e -1400 (scripts/imagens.py). Sem a sala:
     a mobília pode ter mudado desde 2021.
     ------------------------------------------------------------ */
  // Só as fotos que a página mostra: a galeria inteira fica para a versão
  // completa do site.
  var SERIES = {
    // a sala e a mesa num só espaço: uma série só
    sala: { nome: 'A sala', nomeEn: 'The living room', fotos: [
      { f: 'sala', l: 'A sala, com o sofá e a poltrona, e a mesa ao fundo', e: 'The living room, with the sofa and armchair, and the table beyond' },
      { f: 'sala-tv', l: 'A sala: sofá, poltrona e televisão, com a guarda da escada em madeira', e: 'The living room: sofa, armchair and TV, with the wooden stair rail' },
      { f: 'sala-escada', l: 'A sala e a escada, com as janelas verde-azeitona', e: 'The living room and the staircase, with the olive-green windows' },
      { f: 'sala-mesa', l: 'A sala e a mesa num só espaço', e: 'The living room and the table in one open space' },
      { f: 'mesa-janelas', l: 'A mesa de refeições, com as janelas verde-azeitona', e: 'The dining table, with the olive-green windows' },
      { f: 'mesa-comprida', l: 'A mesa comprida de madeira, com cadeiras de verga, e a cozinha ao fundo', e: 'The long wooden table with wicker chairs, and the kitchen beyond' },
      { f: 'mesa-cima', l: 'A mesa extensível, vista de cima', e: 'The extending table, seen from above' },
      { f: 'armario-loica', l: 'O armário da loiça', e: 'The crockery cabinet' },
      { f: 'cafe', l: 'O canto do café: máquina Nespresso, chávenas e uma vela', e: 'The coffee corner: Nespresso machine, cups and a candle' }
    ] },
    cozinha: { nome: 'A cozinha', nomeEn: 'The kitchen', fotos: [
      { f: 'cozinha', l: 'A cozinha: frigorífico e fogão Smeg, bancada de mármore', e: 'The kitchen: Smeg fridge and range cooker, marble worktop' },
      { f: 'fogao', l: 'O fogão de indução Smeg, com forno', e: 'The Smeg induction range cooker, with oven' },
      { f: 'frigorifico', l: 'O frigorífico Smeg', e: 'The Smeg fridge' },
      { f: 'bancada', l: 'A bancada, com os armários verde-azeitona', e: 'The worktop, with olive-green cupboards' }
    ] },
    // Casas de banho e suites agrupadas a olho pelas fotos (confirmar com o dono)
    banhos: { nome: 'As casas de banho', nomeEn: 'The bathrooms', fotos: [
      { f: 'suite1-wc', l: 'Suite 1: lavatório largo, espelho e duche', e: 'Suite 1: wide basin, mirror and shower' },
      { f: 'suite1-lavatorio', l: 'Suite 1: o lavatório comprido e o duche', e: 'Suite 1: the long basin and the shower' },
      { f: 'wc-lavatorio', l: 'Suite 1: o móvel do lavatório, verde-azeitona', e: 'Suite 1: the olive-green vanity unit' },
      { f: 'wc', l: 'Suite 1: o duche', e: 'Suite 1: the shower' },
      { f: 'wc-espelho', l: 'Suite 2: lavatório de pousar e espelho redondo', e: 'Suite 2: vessel basin and round mirror' },
      { f: 'suite2-wc', l: 'Suite 2: a casa de banho vista do quarto', e: 'Suite 2: the bathroom seen from the bedroom' },
      { f: 'wc-duche', l: 'Suite 2: o duche e o toalheiro de madeira', e: 'Suite 2: the shower and the wooden towel ladder' },
      { f: 'suite3-wc', l: 'Suite 3: lavatório, espelho redondo e duche', e: 'Suite 3: basin, round mirror and shower' },
      { f: 'suite3-duche', l: 'Suite 3: o duche', e: 'Suite 3: the shower' }
    ] },
    // As três suites: os quartos (as casas de banho estão em "banhos")
    quartos: { nome: 'As suites', nomeEn: 'The suites', fotos: [
      { f: 'suite-janelas', l: 'Suite 1: o quarto, com duas janelas sobre a encosta', e: 'Suite 1: the bedroom, with two windows onto the hillside' },
      { f: 'suite-cama', l: 'Suite 1: a cama de casal, com a cabeceira verde-azeitona', e: 'Suite 1: the double bed, with the olive-green headboard' },
      { f: 'suite-wc', l: 'Suite 1: o quarto visto da casa de banho', e: 'Suite 1: the bedroom seen from the bathroom' },
      { f: 'suite-janela-alta', l: 'Suite 2: o quarto, com a janela alta e o granito à vista', e: 'Suite 2: the bedroom, with the high window and bare granite' },
      { f: 'suite-roupeiros', l: 'Suite 2: os roupeiros embutidos', e: 'Suite 2: the built-in wardrobes' },
      { f: 'suite2-lavatorio', l: 'Suite 2: a cama e o lavatório, num nicho verde-azeitona', e: 'Suite 2: the bed and the basin, in an olive-green niche' },
      { f: 'suite3', l: 'Suite 3: o quarto, com a casa de banho à vista', e: 'Suite 3: the bedroom, with the bathroom beyond' },
      { f: 'suite3-cama', l: 'Suite 3: a cama de casal', e: 'Suite 3: the double bed' }
    ] },
    fora: { nome: 'Lá fora', nomeEn: 'Outside', fotos: [
      { f: 'terraco-mesa', l: 'O terraço: mesa comprida, guarda-sol e churrasqueira, com a piscina e os socalcos atrás', e: 'The terrace: long table, parasol and barbecue, with the pool and terraces beyond' },
      { f: 'relvado', l: 'O relvado e as espreguiçadeiras, entre o muro e a piscina', e: 'The lawn and loungers, between the wall and the pool' },
      { f: 'piscina-solario', l: 'As espreguiçadeiras na ponta da piscina, e a aldeia', e: 'The loungers at the end of the pool, and the village' },
      { f: 'piscina-casa', l: 'A piscina e a casa de granito, com os socalcos atrás', e: 'The pool and the granite house, with the terraced hillside behind' }
    ] }
  };

  var img = function (f, t) { return (EN ? '../' : '') + 'assets/img/' + f + (t ? '-' + t : '') + '.jpg'; };
  var legenda = function (x) { return EN ? x.e : x.l; };

  // quantas fotografias tem cada divisão (o selo em cima da foto)
  $$('[data-conta-serie]').forEach(function (el) {
    var s = SERIES[el.dataset.contaSerie]; if (s) el.textContent = s.fotos.length + (EN ? ' photos' : ' fotografias');
  });

  /* ------------------------------------------------------------
     SCROLL SUAVE (Lenis, carregado do jsDelivr antes deste ficheiro).
     Sem ele, ou com movimento reduzido, fica o scroll normal do browser.
     O menu e o visor param-no enquanto estão abertos.
     ------------------------------------------------------------ */
  var lenis = null;
  if (window.Lenis && !reduzido) {
    lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 1, anchors: { offset: 0 }, autoRaf: true });
  }
  function bloqueia(sim) {
    document.body.style.overflow = sim ? 'hidden' : '';
    if (lenis) { if (sim) lenis.stop(); else lenis.start(); }
  }

  /* ------------------------------------------------------------
     TOPO: fica sólido depois do hero, esconde-se ao descer e volta
     ao subir. Menu do telemóvel.
     ------------------------------------------------------------ */
  var topo = $('#topo'), hero = $('.hero'), menu = $('#menu');
  var ultimoY = window.scrollY;

  function atualizaTopo() {
    var y = window.scrollY;
    var limite = hero ? hero.offsetHeight - 90 : 200;
    topo.classList.toggle('is-solido', y > limite);
    if (!topo.classList.contains('menu-aberto')) topo.classList.toggle('is-escondido', y > ultimoY && y > limite + 200);
    ultimoY = y;
  }

  function fechaMenu() {
    topo.classList.remove('menu-aberto');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', T.abrir);
    bloqueia(false);
  }
  menu.addEventListener('click', function () {
    var aberto = topo.classList.toggle('menu-aberto');
    menu.setAttribute('aria-expanded', aberto);
    menu.setAttribute('aria-label', aberto ? T.fechar : T.abrir);
    bloqueia(aberto);
  });
  $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { if (topo.classList.contains('menu-aberto')) fechaMenu(); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && topo.classList.contains('menu-aberto')) { fechaMenu(); menu.focus(); } });

  // ligação ativa no menu
  var ligacoes = $$('.nav ul a');
  if ('IntersectionObserver' in window) {
    var ioNav = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        ligacoes.forEach(function (a) { a.classList.toggle('is-ativo', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['casa', 'piscina', 'fora', 'dentro', 'comodidades', 'hospedes', 'experiencias', 'reservar'].forEach(function (id) {
      var s = document.getElementById(id); if (s) ioNav.observe(s);
    });
  }

  /* ------------------------------------------------------------
     FOTOGRAFIAS QUE SE REVELAM ao entrar no ecrã ([data-revela]):
     a moldura abre de baixo para cima e a foto assenta (styles.css).
     ------------------------------------------------------------ */
  var revela = $$('[data-revela]');
  if (reduzido || !('IntersectionObserver' in window)) {
    revela.forEach(function (el) { el.classList.add('is-visivel'); });
  } else {
    var ioRevela = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-visivel');
        ioRevela.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    revela.forEach(function (el) { ioRevela.observe(el); });
  }

  /* ------------------------------------------------------------
     TONS: o fundo da página toma o tom da secção que está no meio do
     ecrã (data-fundo: cal, azeitona ou linho; styles.css faz a transição).
     ------------------------------------------------------------ */
  var comTom = $$('[data-fundo]');
  if (comTom.length && 'IntersectionObserver' in window) {
    var ioTom = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) document.documentElement.setAttribute('data-fundo', e.target.getAttribute('data-fundo')); });
    }, { rootMargin: '-50% 0px -50% 0px' });
    comTom.forEach(function (s) { ioTom.observe(s); });
  }

  /* ------------------------------------------------------------
     TÍTULOS que sobem de dentro de si próprios ao entrar no ecrã
     ------------------------------------------------------------ */
  var titulos = $$('.titulo');
  titulos.forEach(function (t) { t.innerHTML = '<span class="sobe">' + t.innerHTML + '</span>'; });
  if (reduzido || !('IntersectionObserver' in window)) {
    titulos.forEach(function (t) { t.classList.add('is-visivel'); });
  } else {
    var ioTitulo = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-visivel');
        ioTitulo.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    titulos.forEach(function (t) { ioTitulo.observe(t); });
  }

  /* ------------------------------------------------------------
     TEXTO QUE SE ACENDE ([data-acende], como o Scroll Reveal do
     React Bits): cada palavra passa de apagada a acesa à medida que a
     frase sobe no ecrã. O texto continua inteiro para leitores de ecrã.
     ------------------------------------------------------------ */
  function partePalavras(el) {
    Array.prototype.slice.call(el.childNodes).forEach(function (n) {
      if (n.nodeType !== 3) return;
      var frag = document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(function (bocado) {
        if (!bocado) return;
        if (/^\s+$/.test(bocado)) { frag.appendChild(document.createTextNode(bocado)); return; }
        var s = document.createElement('span');
        s.className = 'p'; s.textContent = bocado;
        frag.appendChild(s);
      });
      el.replaceChild(frag, n);
    });
  }
  var acende = reduzido ? [] : $$('[data-acende]').map(function (el) {
    partePalavras(el);
    return { el: el, ps: $$('.p', el) };
  });
  var MIN_ACESO = 0.16, JANELA = 4; // palavras que se acendem ao mesmo tempo
  function atualizaAcende(vh) {
    acende.forEach(function (a) {
      var r = a.el.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      // começa quando o topo da frase entra (90% do ecrã) e acaba quando o
      // fim da frase chega a meio do ecrã
      var p = limita((vh * 0.9 - r.top) / (vh * 0.4 + r.height), 0, 1);
      var n = a.ps.length, pos = p * (n + JANELA);
      a.ps.forEach(function (s, k) {
        var o = MIN_ACESO + (1 - MIN_ACESO) * limita((pos - k) / JANELA, 0, 1);
        s.style.setProperty('--o', o.toFixed(3));
      });
    });
  }

  /* ------------------------------------------------------------
     FOTO QUE CRESCE (#cresce, como o Scroll Expand do React Bits):
     a secção tem 250vh e o palco fica preso; --p vai de 0 a 1 nos
     primeiros 70% do percurso e a foto abre até ocupar o ecrã.
     ------------------------------------------------------------ */
  var cresce = $('#cresce');
  var suave = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  function atualizaCresce(vh) {
    if (!cresce || reduzido) return;
    var r = cresce.getBoundingClientRect();
    if (r.bottom < -50 || r.top > vh + 50) return;
    var percurso = Math.max(1, r.height - vh);
    var t = limita(-r.top / (percurso * 0.7), 0, 1);
    cresce.style.setProperty('--p', suave(t).toFixed(4));
  }

  /* ------------------------------------------------------------
     A ALDEIA: a fotografia de drone desliza devagar (parallax leve)
     ------------------------------------------------------------ */
  var aldeia = $('.aldeia__foto'), aldeiaImg = aldeia ? $('img', aldeia) : null;
  function atualizaAldeia(vh) {
    if (!aldeiaImg || reduzido) return;
    var r = aldeia.getBoundingClientRect();
    if (r.bottom < -100 || r.top > vh + 100) return;
    var p = limita((r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2), -1, 1);
    aldeiaImg.style.transform = 'translate3d(0,' + (-p * r.height * 0.07).toFixed(1) + 'px,0)';
  }

  var largo = window.matchMedia('(min-width: 901px) and (min-height: 521px)');  // telemóvel deitado: fila livre

  /* ------------------------------------------------------------
     FILAS QUE DESLIZAM ([data-pista]: as divisões da casa e as
     experiências) — no computador, a secção fica presa ao ecrã e a fila
     corre para o lado enquanto se faz scroll (a pista tem a altura que
     falta percorrer). No telemóvel, ou com movimento reduzido, é uma fila
     normal que desliza com o dedo. O contador e a barra seguem a fila.
     ------------------------------------------------------------ */
  var pistas = $$('[data-pista]').map(function (el) {
    var p = { el: el, fila: $('[data-pista-fila]', el), barra: $('[data-pista-barra]', el), conta: $('[data-pista-conta]', el), dist: 0 };
    p.n = $$('[data-pista-item]', el).length;
    var total = $('[data-pista-total]', el);
    if (total) total.textContent = String(p.n).padStart(2, '0');
    p.fila.addEventListener('scroll', function () { if (!p.dist) atualizaPistas(); }, { passive: true });
    return p;
  });
  function medePistas() {
    var presa = largo.matches && !reduzido;
    pistas.forEach(function (p) {
      p.el.classList.toggle('is-presa', presa);
      if (!presa) { p.el.style.height = ''; p.fila.style.transform = ''; p.dist = 0; return; }
      p.dist = Math.max(0, p.fila.scrollWidth - p.fila.clientWidth);
      p.el.style.height = (window.innerHeight + p.dist) + 'px';
    });
    atualizaPistas();
  }
  function atualizaPistas() {
    pistas.forEach(function (p) {
      var prog;
      if (p.dist) {
        var r = p.el.getBoundingClientRect();
        if (r.bottom < -50 || r.top > window.innerHeight + 50) return;
        prog = limita(-r.top / p.dist, 0, 1);
        p.fila.style.transform = 'translate3d(' + (-prog * p.dist).toFixed(1) + 'px,0,0)';
      } else {
        var max = p.fila.scrollWidth - p.fila.clientWidth;
        prog = max > 0 ? p.fila.scrollLeft / max : 0;
      }
      if (p.barra) p.barra.style.transform = 'scaleX(' + Math.max(0.04, prog).toFixed(3) + ')';
      if (p.conta && p.n) p.conta.textContent = String(Math.min(p.n, Math.round(prog * (p.n - 1)) + 1)).padStart(2, '0');
    });
  }
  medePistas();
  window.addEventListener('resize', medePistas);
  window.addEventListener('load', medePistas);

  /* ------------------------------------------------------------
     PARALLAX ([data-parallax]): a foto de abertura da casa sobe devagar
     ------------------------------------------------------------ */
  var parallax = reduzido ? [] : $$('[data-parallax]');
  function atualizaParallax(vh) {
    parallax.forEach(function (el) {
      var r = el.parentNode.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var p = limita((r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2), -1, 1);
      el.style.transform = 'translate3d(0,' + (-p * r.height * 0.07).toFixed(1) + 'px,0)';
    });
  }

  /* ------------------------------------------------------------
     RESERVAR fixo no telemóvel: aparece depois do hero e some de vez ao
     chegar à secção de reservas (não tapa o rodapé)
     ------------------------------------------------------------ */
  var cta = $('#ctaFixo'), reservar = $('#reservar');
  function atualizaCta(vh) {
    var r = reservar.getBoundingClientRect();
    cta.classList.toggle('is-visivel', window.scrollY > vh * 0.9 && r.top > vh * 0.7 && !topo.classList.contains('menu-aberto'));
  }

  var pedido = false;
  function quadro() {
    pedido = false;
    var vh = window.innerHeight;
    atualizaTopo();
    atualizaAcende(vh);
    atualizaCresce(vh);
    atualizaAldeia(vh);
    atualizaPistas();
    atualizaParallax(vh);
    atualizaCta(vh);
  }
  function pede() { if (!pedido) { pedido = true; requestAnimationFrame(quadro); } }
  window.addEventListener('scroll', pede, { passive: true });
  window.addEventListener('resize', pede);
  window.addEventListener('load', pede);
  quadro();

  /* ------------------------------------------------------------
     VISOR de fotografias
     ------------------------------------------------------------ */
  var visor = $('#visor');
  var vImg = $('#visorImg'), vLeg = $('#visorLegenda'), vConta = $('#visorConta'), vTit = $('#visorTitulo'), vMini = $('#visorMini');
  var serie = [], atual = 0, origem = null;
  var grande = function (f) { return window.innerWidth > 900 ? img(f) : img(f, 1400); };

  function mostra(i) {
    atual = (i + serie.length) % serie.length;
    var foto = serie[atual];
    vImg.classList.add('is-a-mudar');
    var nova = new Image();
    nova.onload = nova.onerror = function () { vImg.src = nova.src; vImg.alt = legenda(foto); vImg.classList.remove('is-a-mudar'); };
    nova.src = grande(foto.f);
    vLeg.textContent = legenda(foto);
    vConta.textContent = (atual + 1) + T.de + serie.length;
    $$('button', vMini).forEach(function (b, k) {
      b.classList.toggle('is-atual', k === atual);
      if (k === atual) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduzido ? 'auto' : 'smooth' });
    });
    (new Image()).src = grande(serie[(atual + 1) % serie.length].f);
  }
  function abre(id, f) {
    var c = SERIES[id];
    if (!c) return;
    origem = document.activeElement;
    serie = c.fotos;
    var i = 0;
    serie.forEach(function (x, k) { if (x.f === f) i = k; });
    vTit.textContent = EN ? c.nomeEn : c.nome;
    vMini.innerHTML = serie.map(function (x, k) {
      return '<button type="button" aria-label="' + T.foto + (k + 1) + '"><img src="' + img(x.f, 800) + '" alt="" loading="lazy"></button>';
    }).join('');
    $$('button', vMini).forEach(function (b, k) { b.addEventListener('click', function () { mostra(k); }); });
    visor.hidden = false;
    bloqueia(true);
    requestAnimationFrame(function () { visor.classList.add('is-aberto'); });
    mostra(i);
    $('#visorFechar').focus();
  }
  function fecha() {
    visor.classList.remove('is-aberto');
    bloqueia(false);
    setTimeout(function () { visor.hidden = true; vImg.removeAttribute('src'); }, reduzido ? 0 : 400);
    if (origem) origem.focus({ preventScroll: true });
  }
  $('#visorFechar').addEventListener('click', fecha);
  $('#visorAnt').addEventListener('click', function () { mostra(atual - 1); });
  $('#visorSeg').addEventListener('click', function () { mostra(atual + 1); });
  document.addEventListener('keydown', function (e) {
    if (visor.hidden) return;
    if (e.key === 'Escape') fecha();
    else if (e.key === 'ArrowLeft') mostra(atual - 1);
    else if (e.key === 'ArrowRight') mostra(atual + 1);
    else if (e.key === 'Tab') {
      var foc = $$('button', visor).filter(function (b) { return b.offsetParent !== null; });
      var primeiro = foc[0], ultimo = foc[foc.length - 1];
      if (e.shiftKey && document.activeElement === primeiro) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primeiro.focus(); }
    }
  });
  var toqueX = null;
  $('#visorPalco').addEventListener('touchstart', function (e) { toqueX = e.touches[0].clientX; }, { passive: true });
  $('#visorPalco').addEventListener('touchend', function (e) {
    if (toqueX === null) return;
    var dx = e.changedTouches[0].clientX - toqueX;
    if (Math.abs(dx) > 45) mostra(atual + (dx < 0 ? 1 : -1));
    toqueX = null;
  });
  $('#visorPalco').addEventListener('click', function (e) { if (e.target === e.currentTarget) fecha(); });

  // painéis do acordeão e fotos com data-foto abrem o visor na fotografia certa
  $$('[data-foto]').forEach(function (b) {
    b.addEventListener('click', function () { abre(b.dataset.serie || 'dentro', b.dataset.foto); });
  });

  /* ------------------------------------------------------------
     FILME do hero: quatro planos que trocam a cada 5,5 s (o primeiro 4,5 s
     depois da abertura), com uma troca curta e a câmara a entrar já em
     movimento (CSS: --mov em cada plano). Traços em baixo mostram o
     progresso e saltam para cada foto. Cada foto só descarrega quando o
     plano anterior entra. Para quando o hero sai do ecrã ou o separador
     fica escondido, e com o botão de pausa. Com movimento reduzido fica só
     a primeira foto.
     ------------------------------------------------------------ */
  var filme = $('[data-filme]');
  if (filme && !reduzido) {
    var planos = $$('.hero__plano', filme), botao = $('#heroPausa'), marcas = $('#heroMarcas');
    var tracos = marcas ? $$('.hero__marca', marcas) : [];
    // tempos: o 1.º plano troca 4,5 s depois da abertura; os outros duram 5,5 s;
    // a troca leva 0,8 s (styles.css, .hero__plano)
    var PRIMEIRO = 4500, DUR = 5500, FUNDE = 800, ia = 0, tempo = null, falta = 0, inicio = 0;
    var parado = false, noEcra = true, alvo = null;
    var carrega = function (k) {
      var im = $('img[data-srcset]', planos[k]);
      if (!im) return;
      im.sizes = im.dataset.sizes; im.srcset = im.dataset.srcset;
      im.removeAttribute('data-srcset');
      // descodifica antes de entrar, para a troca não engasgar o movimento
      var feito = function () { im.dataset.pronta = '1'; };
      if (im.decode) im.decode().then(feito, feito); else im.addEventListener('load', feito);
    };
    var pronta = function (k) {
      var im = $('img', planos[k]);
      return k === 0 || (im.dataset.pronta === '1' && im.naturalWidth > 0);
    };
    var corre = function () { return !parado && noEcra && !document.hidden; };
    // os tracos: os já vistos cheios, o atual a encher durante o plano
    function marca(dur) {
      tracos.forEach(function (t, k) {
        t.classList.remove('is-atual');
        t.classList.toggle('is-vista', k < ia);
        t.toggleAttribute('aria-current', k === ia);
      });
      if (!tracos[ia]) return;
      marcas.style.setProperty('--dur', dur + 'ms');
      void tracos[ia].offsetWidth;                                   // recomeça a animação
      tracos[ia].classList.add('is-atual');
    }
    function agenda(ms) {
      clearTimeout(tempo); tempo = null; falta = ms; inicio = Date.now();
      if (corre()) tempo = setTimeout(avanca, ms);
    }
    function avanca() {
      tempo = null;
      var seg = alvo !== null ? alvo : (ia + 1) % planos.length;
      if (!pronta(seg)) { carrega(seg); agenda(250); return; }       // espera pela foto
      alvo = null;
      var sai = planos[ia];
      sai.classList.remove('is-ativo'); sai.classList.add('is-saindo');
      setTimeout(function () { sai.classList.remove('is-saindo'); }, FUNDE + 150);
      planos[seg].classList.add('is-ativo');
      filme.classList.add('ja-correu');
      ia = seg;
      carrega((ia + 1) % planos.length);
      marca(DUR);
      agenda(DUR);
    }
    function atualiza() {
      var anda = corre();
      filme.classList.toggle('is-pausado', !anda);
      if (marcas) marcas.classList.toggle('is-pausado', !anda);
      if (anda) {
        if (!tempo) { inicio = Date.now(); tempo = setTimeout(avanca, falta); }
      } else if (tempo) {
        clearTimeout(tempo); tempo = null; falta = Math.max(0, falta - (Date.now() - inicio));
      }
    }
    var atraso = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--atraso')) || 0;
    window.addEventListener('load', function () { carrega(1); });
    agenda(atraso * 1000 + PRIMEIRO);
    if (marcas) {
      marcas.hidden = false;
      marca(atraso * 1000 + PRIMEIRO);
      tracos.forEach(function (t, k) {
        t.addEventListener('click', function () {
          if (k === ia) return;
          alvo = k; carrega(k);
          clearTimeout(tempo); tempo = null;
          if (corre()) avanca(); else { falta = 0; avanca(); }
        });
      });
    }
    if (botao) {
      botao.hidden = false;
      botao.addEventListener('click', function () {
        parado = !parado;
        botao.setAttribute('aria-pressed', String(parado));
        botao.setAttribute('aria-label', (parado ? (EN ? 'Play' : 'Continuar') : (EN ? 'Pause' : 'Pausar')) + (EN ? ' the film' : ' o filme'));
        atualiza();
      });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { noEcra = e[0].isIntersecting; atualiza(); }).observe(filme);
    }
    document.addEventListener('visibilitychange', atualiza);
  }

  var ano = $('#ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();

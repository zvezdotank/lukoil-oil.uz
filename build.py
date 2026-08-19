#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка статического сайта lukoil-oil.uz. Запуск: python3 build.py"""

import html
import json
import os
import re

from content import (SITE, NAV, STATS, ADVANTAGES, LOGISTICS, STEPS, DOCS,
                     FAQ, CATS, SHELF, CATALOG, INDUSTRIES)

ROOT = os.path.dirname(os.path.abspath(__file__))
V = "9"  # версия статики для кэша

TEL = SITE["phone_href"]
PHONE = SITE["phone"]
NOTE = SITE["phone_note"]
MAIL = SITE["mail"]
BASE = SITE["base"]


DRUM = '<svg class="drum" viewBox="0 0 64 104" aria-hidden="true" focusable="false"><path d="M4 12h56v80a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V12Z" fill="currentColor" opacity=".9"/><ellipse cx="32" cy="12" rx="28" ry="8" fill="currentColor"/><ellipse cx="32" cy="12" rx="20" ry="5.4" fill="#000" opacity=".16"/><rect x="4" y="28" width="56" height="6" fill="#000" opacity=".18"/><rect x="4" y="72" width="56" height="6" fill="#000" opacity=".18"/><rect x="4" y="44" width="56" height="18" fill="#fff" opacity=".92"/></svg>'


def e(s):
    return html.escape(s, quote=True)


def pic(name, alt, cls="", w=None, h=None, eager=False, sizes=None):
    """<picture> с webp и jpg-фолбэком."""
    attrs = ['src="img/%s.jpg?v=%s"' % (name, V), 'alt="%s"' % e(alt)]
    if cls:
        attrs.append('class="%s"' % cls)
    if w:
        attrs.append('width="%d"' % w)
    if h:
        attrs.append('height="%d"' % h)
    attrs.append('decoding="async"')
    attrs.append('fetchpriority="high"' if eager else 'loading="lazy"')
    return ('<picture><source srcset="img/%s.webp?v=%s" type="image/webp">'
            '<img %s></picture>' % (name, V, " ".join(attrs)))


def head(title, desc, path, extra_ld=None, og_img="hero-drums", lcp=None):
    canon = BASE + ("/" if path == "index.html" else "/" + path)
    ld = [{
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": BASE + "/#org",
        "name": "Смазочные материалы ЛУКОЙЛ — дистрибьютор в Узбекистане",
        "url": BASE + "/",
        "email": MAIL,
        "telephone": PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "UZ",
            "addressLocality": "Ташкент",
            "addressRegion": "Мирабадский район",
            "streetAddress": "ул. Нукус, 71",
        },
        "areaServed": {"@type": "Country", "name": "Узбекистан"},
    }]
    if extra_ld:
        ld.extend(extra_ld)

    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canon)s">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="geo.region" content="UZ-TK">
<meta name="geo.placename" content="Ташкент">
<meta name="theme-color" content="#ec3013">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Смазочные материалы ЛУКОЙЛ — Узбекистан">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canon)s">
<meta property="og:image" content="%(base)s/img/%(og)s.jpg">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="fonts/golos-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
%(lcp)s
<link rel="stylesheet" href="site.css?v=%(v)s">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<script type="application/ld+json">%(ld)s</script>
</head>
<body>
<a class="skip" href="#main">К основному содержанию</a>
""" % {
        "title": e(title), "desc": e(desc), "canon": canon, "base": BASE,
        "og": og_img, "v": V,
        "lcp": ('<link rel="preload" as="image" href="img/%s.webp?v=%s" '
                'type="image/webp" fetchpriority="high">' % (lcp, V)) if lcp else "",
        "ld": json.dumps(ld, ensure_ascii=False, separators=(",", ":")),
    }


def header(current):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else "", e(t))
        for h, t in NAV)
    return """<header class="hdr">
  <div class="hdr__in">
    <a class="brand" href="index.html">
      <b>Смазочные материалы ЛУКОЙЛ</b>
      <span>Официальный дистрибьютор в Узбекистане</span>
    </a>
    <nav class="nav" id="nav" aria-label="Основная навигация">%(links)s</nav>
    <div class="hdr__cta">
      <a class="hdr__tel" href="tel:%(tel)s">
        <b>%(phone)s</b>
        <span class="note">%(note)s</span>
      </a>
      <button class="btn btn-primary" type="button" data-callback>Обратный звонок</button>
      <button class="burger" type="button" id="burger" aria-label="Меню" aria-expanded="false"
              aria-controls="nav"><span></span></button>
    </div>
  </div>
</header>
<main id="main">
""" % {"links": links, "tel": TEL, "phone": e(PHONE), "note": e(NOTE)}


def form(idp, title, sub, note_label, note_ph, kinds=("Прайс", "Подбор", "Звонок")):
    opts = "".join(
        '<label class="seg-opt"><input type="radio" name="kind" value="%s"%s><span>%s</span></label>'
        % (e(k), " checked" if i == 0 else "", e(k)) for i, k in enumerate(kinds))
    return """<div>
  <form class="form" data-mailform>
    <div>
      <h3>%(title)s</h3>
      <p class="small muted" style="margin:0">%(sub)s</p>
    </div>
    <div class="field"><label for="%(id)s-name">Имя</label>
      <input class="input" id="%(id)s-name" name="name" autocomplete="name" placeholder="Как к вам обращаться" required></div>
    <div class="field"><label for="%(id)s-company">Организация</label>
      <input class="input" id="%(id)s-company" name="company" autocomplete="organization" placeholder="Название и сфера"></div>
    <div class="field"><label for="%(id)s-phone">Телефон</label>
      <input class="input" id="%(id)s-phone" name="phone" type="tel" autocomplete="tel" placeholder="+998 __ ___ __ __" required></div>
    <div class="field"><label for="%(id)s-note">%(nlabel)s</label>
      <textarea class="input" id="%(id)s-note" name="note" placeholder="%(nph)s"></textarea></div>
    <div class="field"><label>Тип обращения</label><div class="seg">%(opts)s</div></div>
    <button class="btn btn-primary btn-block" type="submit">Отправить заявку</button>
    <p class="fineprint" style="margin:0">Нажимая кнопку, вы соглашаетесь на обработку персональных
      данных. Заявка уходит письмом на %(mail)s.</p>
  </form>
  <div class="ok" data-sent hidden>
    <span class="tag tag-accent" style="align-self:flex-start">Заявка сформирована</span>
    <h3 style="margin:0">Спасибо<span data-sent-name></span></h3>
    <p class="small" style="margin:0">Письмо открылось в вашей почтовой программе — проверьте и отправьте.
      Если этого не произошло, напишите нам напрямую:
      <a href="mailto:%(mail)s" data-sent-link>%(mail)s</a> или позвоните
      <a href="tel:%(tel)s">%(phone)s</a>.</p>
    <button class="btn btn-secondary" type="button" data-again style="align-self:flex-start">Заполнить ещё раз</button>
  </div>
</div>""" % {"id": idp, "title": e(title), "sub": e(sub), "nlabel": e(note_label),
             "nph": e(note_ph), "opts": opts, "mail": MAIL, "tel": TEL, "phone": e(PHONE)}


def cta():
    return """<section class="cta">
  <div class="wrap"><div class="cta__in">
    <div class="cta__drum">%(drum)s</div>
    <h2>Пришлите список позиций — вернём прайс и сроки в тот же день</h2>
    <div class="cta__side">
      <div>
        <a class="cta__tel" href="tel:%(tel)s">%(phone)s</a>
        <span class="note" style="color:var(--bg);opacity:.75">%(note)s</span>
      </div>
      <a href="mailto:%(mail)s" style="font-size:15px">%(mail)s</a>
      <span style="font-size:14px;opacity:.9">Отдел продаж, пн–сб 9:00–18:00</span>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn btn-inv" href="contacts.html">Оставить заявку</a>
        <button class="btn btn-out-inv" type="button" data-callback>Обратный звонок</button>
      </div>
    </div>
  </div></div>
</section>""" % {"tel": TEL, "phone": e(PHONE), "note": e(NOTE), "mail": MAIL, "drum": DRUM}


def footer():
    cats = "".join('<a href="%s.html">%s</a>' % (c["slug"], e(c["nav"])) for c in CATS)
    return """</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div class="foot__col">
        <span class="foot__brand">Смазочные материалы ЛУКОЙЛ</span>
        <span class="muted">%(domain)s</span>
        <p class="muted" style="margin:6px 0 0;max-width:34ch">Официальный дистрибьютор смазочных
          материалов ЛУКОЙЛ в Республике Узбекистан. Поставки юридическим лицам по договору.</p>
      </div>
      <div class="foot__col">
        <span class="tiny">Продукция</span>
        %(cats)s
        <a href="products.html">Весь каталог и подбор</a>
      </div>
      <div class="foot__col">
        <span class="tiny">Связаться</span>
        <a href="tel:%(tel)s"><b>%(phone)s</b></a>
        <span class="note">%(note)s</span>
        <a href="mailto:%(mail)s">%(mail)s</a>
        <a href="mailto:%(mail2)s">%(mail2)s</a>
        <span class="muted">%(addr)s</span>
        <span class="muted">%(hours)s</span>
      </div>
    </div>
    <div class="foot__bar">
      ЛУКОЙЛ и названия продуктовых линеек — товарные знаки правообладателя.
      Сайт информационный, публичной офертой не является.
    </div>
  </div>
</footer>

<div class="modal" id="callback" hidden>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="cb-t">
    <form class="form" data-mailform>
      <div class="modal__title" id="cb-t">Обратный звонок</div>
      <p class="small muted" style="margin:0">Оставьте номер — перезвоним в рабочее время.
        Или позвоните сами: <a href="tel:%(tel)s">%(phone)s</a>.</p>
      <input type="hidden" name="kind" value="Обратный звонок">
      <div class="field"><label for="cb-name">Имя</label>
        <input class="input" id="cb-name" name="name" placeholder="Как к вам обращаться" required></div>
      <div class="field"><label for="cb-phone">Телефон</label>
        <input class="input" id="cb-phone" name="phone" type="tel" placeholder="+998 __ ___ __ __" required></div>
      <div class="modal__actions">
        <button class="btn btn-secondary" type="button" data-close>Отмена</button>
        <button class="btn btn-primary" type="submit">Жду звонка</button>
      </div>
    </form>
    <div class="ok" data-sent hidden>
      <span class="tag tag-accent" style="align-self:flex-start">Принято</span>
      <p class="small" style="margin:0">Письмо с вашим номером открылось в почтовой программе.
        Если нет — напишите на <a href="mailto:%(mail)s" data-sent-link>%(mail)s</a>.</p>
      <div class="modal__actions"><button class="btn btn-primary" type="button" data-close>Закрыть</button></div>
    </div>
  </div>
</div>

<nav class="mbar" aria-label="Быстрая связь">
  <a href="tel:%(tel)s">Позвонить</a>
  <a href="mailto:%(mail)s">Написать</a>
</nav>

<script src="site.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"domain": SITE["domain"], "cats": cats, "tel": TEL, "phone": e(PHONE),
       "note": e(NOTE), "mail": MAIL, "mail2": SITE["mail2"],
       "addr": e(SITE["addr"]), "hours": e(SITE["hours"]), "v": V}


def crumbs(items):
    """items: [(href|None, label)]"""
    parts = []
    for href, label in items:
        parts.append('<a href="%s">%s</a>' % (href, e(label)) if href else e(label))
    return '<nav class="crumbs" aria-label="Хлебные крошки">%s</nav>' % " → ".join(parts)


def ld_crumbs(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            dict({"@type": "ListItem", "position": i + 1, "name": label},
                 **({"item": BASE + "/" + href} if href else {}))
            for i, (href, label) in enumerate(items)
        ],
    }


def ld_faq(pairs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs],
    }


def faq_block(pairs, title="Частые вопросы"):
    items = "".join(
        '<details%s><summary><span class="n">%02d</span><span>%s</span>'
        '<span class="s">+</span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", i + 1, e(q), e(a)) for i, (q, a) in enumerate(pairs))
    return """<section class="sec"><div class="wrap sec-pad"
    style="display:grid;grid-template-columns:1fr 2fr;gap:44px" data-faqgrid>
    <h2 style="margin:0">%s</h2>
    <div class="faq">%s</div>
  </div></section>""" % (e(title), items)


# ───────────────────────── страницы ─────────────────────────

def page_index():
    stats = "".join('<div><b>%s</b><span>%s</span></div>' % (e(a), e(b)) for a, b in STATS)
    adv = "".join(
        '<div><div class="kicker" style="margin-bottom:10px">%s</div><h3 style="font-size:16px">%s</h3>'
        '<p class="small muted" style="margin:0">%s</p></div>' % (n, e(t), e(b))
        for n, t, b in ADVANTAGES)
    cats = "".join(
        '<a class="tile" href="%s.html"><div class="tile__ph grayscale">%s</div>'
        '<div class="tile__body"><div class="kicker">%s</div>'
        '<h3 style="font-size:20px;margin:0">%s</h3>'
        '<p class="small muted" style="margin:0">%s</p>'
        '<div class="tile__more">Подробнее и цены →</div></div></a>'
        % (c["slug"], pic(c["photo"] + "-t", c["alt"], w=560, h=315),
           e(c["kicker"]), e(c["title"]), e(c["short"])) for c in CATS)
    logi = "".join('<div><b>%s</b><span>%s</span></div>' % (e(a), e(b)) for a, b in LOGISTICS)
    who = "".join(
        '<a href="industries.html"><div class="who__ph grayscale">%s</div>'
        '<div class="who__body"><div class="kicker">%s</div>'
        '<h3 style="font-size:19px;margin:6px 0 6px">%s</h3>'
        '<p class="small muted" style="margin:0">%s</p></div></a>'
        % (pic(i["photo"] + "-t", i["alt"], w=560, h=315), i["num"], e(i["title"]),
           e(i["body"].split(":")[0] + ".")) for i in INDUSTRIES)

    ld = [ld_faq(FAQ), {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "@id": BASE + "/#business", "name": "Смазочные материалы ЛУКОЙЛ — Узбекистан",
        "image": BASE + "/img/hero-drums.jpg", "url": BASE + "/",
        "telephone": PHONE, "email": MAIL, "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressCountry": "UZ",
                    "addressLocality": "Ташкент", "streetAddress": "ул. Нукус, 71"},
        "openingHours": "Mo-Sa 09:00-18:00",
    }]

    return (head(
        "Масла ЛУКОЙЛ в Узбекистане — официальный дистрибьютор, Ташкент",
        "Индустриальные, гидравлические и моторные масла ЛУКОЙЛ в бочках 216,5 л со склада "
        "в Ташкенте. Складские цены, подбор по технике, отгрузка в день заявки.",
        "index.html", ld)
        + header("index.html") + """
<section class="sec"><div class="wrap"><div class="hero">
  <div class="hero__l">
    <span class="tag tag-outline">Поставки B2B по всей республике</span>
    <h1>Индустриальные масла ЛУКОЙЛ в бочках — со склада в Ташкенте</h1>
    <p class="lead hero__lead">Гидравлика, редукторные, компрессорные и турбинные масла бочками
      216,5 л и кубами. Прямые поставки заводам и автопаркам: складские цены, подбор по картам
      смазки, отгрузка в день заявки.</p>
    <div class="actions">
      <a class="btn btn-primary" href="#request">Получить прайс-лист</a>
      <a class="btn btn-secondary" href="products.html#finder">Подбор масла по технике</a>
      <a class="btn btn-ghost" href="tel:%(tel)s">%(phone)s</a>
    </div>
    <div class="stats">%(stats)s</div>
  </div>
  <div class="hero__r" id="request">%(form)s</div>
</div></div></section>

<section class="sec"><div class="wrap sec-pad">
  <h2>Что даёт статус официального дистрибьютора</h2>
  <div class="grid g4" style="margin-top:28px">%(adv)s</div>
</div></section>

<section class="sec"><div class="wrap sec-pad">
  <div style="display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:26px">
    <h2 style="margin:0">Продукция на складе</h2>
    <a class="btn btn-ghost" href="products.html">Все категории и подбор →</a>
  </div>
  <div class="grid g3">%(cats)s</div>
</div></section>

<section class="sec"><div class="wrap"><div class="split">
  <div class="split__media grayscale">%(photo)s</div>
  <div class="split__body">
    <h2>Склад, отгрузка, документы</h2>
    <p class="muted" style="max-width:46ch;font-size:15px">Собственный склад в Ташкенте и постоянный
      запас по ходовым позициям. Заявка до 14:00 — отгрузка в тот же день.</p>
    <div class="rows" style="margin-top:24px">%(logi)s</div>
    <div class="actions"><a class="btn btn-secondary" href="about.html">Как устроена работа</a></div>
  </div>
</div></div></section>

<section class="sec"><div class="wrap sec-pad">
  <div style="display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:26px">
    <h2 style="margin:0">Кому поставляем</h2>
    <a class="btn btn-ghost" href="industries.html">Подробно по отраслям →</a>
  </div>
  <div class="who">%(who)s</div>
</div></section>

%(faq)s
%(cta)s
""" % {"tel": TEL, "phone": e(PHONE), "stats": stats, "adv": adv, "cats": cats, "logi": logi,
       "who": who,
       "form": form("f", "Запрос прайс-листа",
                    "Ответим в течение рабочего часа с ценами под ваш объём.",
                    "Что нужно поставить",
                    "Например: 10W-40 для 40 грузовиков, бочки 216,5 л"),
       "photo": pic("bottling", "Линия розлива смазочных материалов", w=1400, h=760),
       "faq": faq_block(FAQ), "cta": cta()} + footer())


def page_products():
    cats = "".join(
        '<a class="tile" href="%s.html"><div class="tile__ph grayscale">%s</div>'
        '<div class="tile__body"><div class="kicker">%s</div>'
        '<h3 style="font-size:20px;margin:0">%s</h3>'
        '<p class="small muted" style="margin:0">%s</p>'
        '<div class="small muted" style="border-top:1px solid var(--hair);padding-top:10px">%s</div>'
        '<div class="tile__more">Смотреть марки и тару →</div></div></a>'
        % (c["slug"], pic(c["photo"] + "-t", c["alt"], w=560, h=315),
           e(c["kicker"]), e(c["title"]), e(c["short"]), e(c["packs"])) for c in CATS)

    shelf = "".join(
        '<a href="%s.html"><div class="ph">%s</div><b>%s</b><span>%s</span></a>'
        % (cat, pic(img, name, w=480, h=480), e(name), e(meta))
        for img, name, meta, cat in SHELF)

    segs = "".join(
        '<label class="seg-opt"><input type="radio" name="seg" value="%s"%s><span>%s</span></label>'
        % (e(k), " checked" if i == 0 else "", e(k)) for i, k in enumerate(CATALOG))

    cr = [("index.html", "Главная"), (None, "Продукция")]
    ld = [ld_crumbs(cr), {
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c["title"],
             "url": BASE + "/" + c["slug"] + ".html"} for i, c in enumerate(CATS)],
    }]

    return (head(
        "Каталог масел ЛУКОЙЛ — цены и подбор по технике, Ташкент",
        "Шесть товарных групп на складе в Ташкенте: индустриальные, гидравлические, компрессорные "
        "и моторные масла, СОЖ, смазки. Подбор по технике, прайс по запросу.",
        "products.html", ld, og_img="ind-gears")
        + header("products.html") + """
<section class="sec"><div class="wrap phead">
  %(cr)s
  <span class="tag tag-outline">Каталог</span>
  <h1>Продукция и подбор по технике</h1>
  <p class="lead" style="max-width:62ch">Шесть товарных групп на складе в Ташкенте. Полный прайс
    с ценами под ваш объём отправляем по запросу — в PDF и Excel. Точный продукт подбирает инженер
    по допускам производителя техники.</p>
  <div class="actions">
    <a class="btn btn-primary" href="#request">Запросить прайс-лист</a>
    <a class="btn btn-secondary" href="#finder">Подбор по технике</a>
  </div>
</div></section>

<section class="sec"><div class="wrap sec-pad">
  <h2>Товарные группы</h2>
  <div class="grid g3" style="margin-top:26px">%(cats)s</div>
</div></section>

<section class="sec"><div class="wrap sec-pad">
  <div style="display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:22px">
    <h2 style="margin:0">Мелкая тара под сервис и розницу</h2>
    <span class="small muted">Дополнение к основным поставкам в бочках</span>
  </div>
  <div class="prod">%(shelf)s</div>
</div></section>

<section class="sec" id="finder"><div class="wrap sec-pad">
  <div style="display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:20px">
    <h2 style="margin:0">Подбор масла по технике</h2>
    <span class="small muted">Выберите класс техники — покажем ходовые позиции и тару</span>
  </div>
  <div class="seg" style="margin-bottom:22px">%(segs)s</div>
  <div class="tablewrap"><table class="table">
    <thead><tr><th style="width:30%%">Техника и условия</th><th style="width:26%%">Продукт</th>
      <th style="width:16%%">Вязкость / класс</th><th style="width:16%%">Тара</th>
      <th style="width:12%%">Наличие</th></tr></thead>
    <tbody></tbody>
  </table></div>
  <p class="small muted" style="margin-top:14px;max-width:80ch">Таблица носит справочный характер.
    Точный продукт подбирается по допускам производителя техники — пришлите модель и наработку,
    инженер даст рекомендацию.</p>
  <div class="actions">
    <a class="btn btn-primary" href="#request">Отправить технику на подбор</a>
    <a class="btn btn-secondary" href="tel:%(tel)s">Позвонить %(phone)s</a>
  </div>
</div></section>

<section class="sec" id="request"><div class="wrap"><div class="split">
  <div class="split__body" style="padding-left:0;padding-right:48px;border-right:2px solid var(--divider)">
    <h2>Прайс-лист и подбор</h2>
    <p class="muted" style="max-width:48ch">Пришлите список позиций или модели техники — вернём цены
      под ваш объём, сроки и остаток на складе. Отвечаем в течение рабочего часа.</p>
    <div class="rows" style="margin-top:22px">
      <div><b>ПРАЙС</b><span>PDF и Excel с ценами под ваш объём</span></div>
      <div><b>ПОДБОР</b><span>Рекомендация инженера по допускам техники</span></div>
      <div><b>ОБРАЗЦЫ</b><span>Паспорт качества и сертификат на партию</span></div>
    </div>
  </div>
  <div class="split__body">%(form)s</div>
</div></div></section>
%(cta)s
""" % {"cr": crumbs(cr), "cats": cats, "shelf": shelf, "segs": segs, "tel": TEL,
       "phone": e(PHONE),
       "form": form("p", "Запрос прайс-листа", "Ответим в течение рабочего часа.",
                    "Что нужно поставить", "Например: HLP 46, 10 бочек, ежемесячно"),
       "cta": cta()}
        + "<script>window.CATALOG=%s;</script>\n" % json.dumps(CATALOG, ensure_ascii=False)
        + footer())


def page_cat(c):
    rows = "".join("<tr>%s</tr>" % "".join(
        "<td%s>%s</td>" % (' style="font-weight:600"' if i == 0 else "", e(v))
        for i, v in enumerate(r)) for r in c["table"])
    heads = "".join("<th>%s</th>" % e(h) for h in c["table_head"])
    uses = "".join('<div style="padding:14px 20px 14px 0;border-bottom:1px solid var(--hair);'
                   'font-size:14px">%s</div>' % e(u) for u in c["uses"])
    ask = "".join('<div><b class="num">%02d</b><span>%s</span></div>' % (i + 1, e(a))
                  for i, a in enumerate(c["ask"]))
    others = "".join(
        '<a href="%s.html" style="text-decoration:none;color:inherit;display:flex;'
        'flex-direction:column;gap:6px"><div class="kicker">%s</div>'
        '<h3 style="font-size:17px;margin:0">%s</h3>'
        '<p class="small muted" style="margin:0">%s</p></a>'
        % (o["slug"], e(o["kicker"]), e(o["title"]), e(o["packs"]))
        for o in CATS if o["slug"] != c["slug"])

    cr = [("index.html", "Главная"), ("products.html", "Продукция"), (None, c["title"])]
    ld = [ld_crumbs(cr), ld_faq(c["faq"]), {
        "@context": "https://schema.org", "@type": "Product",
        "name": c["title"] + " ЛУКОЙЛ",
        "description": c["seo_desc"],
        "brand": {"@type": "Brand", "name": "ЛУКОЙЛ"},
        "image": BASE + "/img/%s.jpg" % c["photo"],
        "offers": {"@type": "AggregateOffer", "priceCurrency": "UZS",
                   "availability": "https://schema.org/InStock",
                   "seller": {"@id": BASE + "/#org"}},
    }]

    return (head(c["seo_title"], c["seo_desc"], c["slug"] + ".html", ld,
                 og_img=c["photo"], lcp=c["photo"])
            + header("products.html") + """
<section class="sec"><div class="wrap"><div class="split split--narrow split--rev">
  <div class="split__media grayscale">%(photo)s</div>
  <div class="split__body" style="padding-left:0">
    %(cr)s
    <span class="tag tag-outline">%(kicker)s</span>
    <h1 style="margin:16px 0 14px">%(title)s</h1>
    <p class="lead" style="max-width:56ch">%(lead)s</p>
    <div class="rows" style="margin-top:22px">
      <div><b>ТАРА</b><span class="withdrum">%(drumi)s%(packs)s</span></div>
      <div><b>СКЛАД</b><span>Ходовые позиции — постоянный запас в Ташкенте</span></div>
      <div><b>ДОКУМЕНТЫ</b><span>Паспорт качества и сертификат на каждую партию</span></div>
    </div>
    <div class="actions">
      <a class="btn btn-primary" href="#request">Запросить цену</a>
      <a class="btn btn-secondary" href="tel:%(tel)s">%(phone)s</a>
    </div>
    <p class="fineprint" style="margin-top:10px">%(note)s — пишите на
      <a href="mailto:%(mail)s">%(mail)s</a> или оставьте заявку ниже.</p>
  </div>
</div></div></section>

<section class="sec"><div class="wrap sec-pad">
  <h2>Марки и характеристики</h2>
  <div class="tablewrap" style="margin-top:22px"><table class="table">
    <thead><tr>%(heads)s</tr></thead><tbody>%(rows)s</tbody>
  </table></div>
  <p class="small muted" style="margin-top:14px;max-width:80ch">Перечень справочный: наличие
    и точную марку под ваши допуски подтверждает менеджер при расчёте. Позиции не из списка
    привозим под заказ.</p>
</div></section>

<section class="sec"><div class="wrap sec-pad">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:44px" data-two>
    <div>
      <h2>Где применяется</h2>
      <div style="margin-top:18px;border-top:2px solid var(--divider)">%(uses)s</div>
      <div class="shots">%(shots)s</div>
    </div>
    <div>
      <h2>Что уточнить при заказе</h2>
      <div class="rows" style="margin-top:18px">%(ask)s</div>
    </div>
  </div>
</div></section>

%(faq)s

<section class="sec" id="request"><div class="wrap"><div class="split">
  <div class="split__body" style="padding-left:0;padding-right:48px;border-right:2px solid var(--divider)">
    <h2>Расчёт под ваш объём</h2>
    <p class="muted" style="max-width:48ch">Напишите марку, объём и периодичность — вернём цену,
      срок отгрузки и остаток на складе. Ответ в течение рабочего часа.</p>
    <div class="actions">
      <a class="btn btn-secondary" href="tel:%(tel)s">Позвонить %(phone)s</a>
      <a class="btn btn-secondary" href="mailto:%(mail)s">Написать на почту</a>
    </div>
  </div>
  <div class="split__body">%(form)s</div>
</div></div></section>

<section class="sec"><div class="wrap sec-pad">
  <h2>Другие товарные группы</h2>
  <div class="grid g3" style="margin-top:24px">%(others)s</div>
</div></section>
%(cta)s
""" % {"photo": pic(c["photo"], c["alt"], w=1120, h=628, eager=True),
       "cr": crumbs(cr), "kicker": e(c["kicker"]), "title": e(c["title"]),
       "lead": e(c["lead"]), "packs": e(c["packs"]), "drumi": DRUM,
       "tel": TEL, "phone": e(PHONE),
       "note": e(NOTE.capitalize()), "mail": MAIL,
       "heads": heads, "rows": rows, "uses": uses, "ask": ask,
       "shots": "".join('<div class="shots__i grayscale">%s</div>'
                        % pic(s + "-t", alt, w=560, h=315)
                        for s, alt in c["shots"]),
       "faq": faq_block(c["faq"], "Вопросы по группе"),
       "form": form("c", "Запрос цены", "Укажите марку, объём и периодичность поставки.",
                    "Что нужно поставить", "Например: %s, 6 бочек в квартал" % c["nav"]),
       "others": others, "cta": cta()} + footer())


def page_industries():
    blocks = []
    for i, ind in enumerate(INDUSTRIES):
        pts = "".join('<div style="padding:13px 20px 13px 0;border-bottom:1px solid var(--hair);'
                      'font-size:13px">%s</div>' % e(p) for p in ind["points"])
        rev = " split--rev" if i % 2 else ""
        blocks.append("""<section class="sec"><div class="wrap"><div class="split split--narrow%(rev)s">
  <div class="split__media grayscale">%(photo)s</div>
  <div class="split__body">
    <div class="kicker" style="font-size:15px;font-weight:800;margin-bottom:10px">%(num)s</div>
    <h2>%(title)s</h2>
    <p class="muted" style="max-width:58ch;font-size:15px">%(body)s</p>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);margin-top:20px;
                border-top:2px solid var(--divider)">%(pts)s</div>
    <div class="actions">
      <a class="btn btn-primary" href="%(cat)s.html">Подходящие масла</a>
      <a class="btn btn-secondary" href="contacts.html">Обсудить поставку</a>
    </div>
  </div>
</div></div></section>""" % {"rev": rev, "num": ind["num"], "title": e(ind["title"]),
                             "body": e(ind["body"]), "pts": pts, "cat": ind["cat"],
                             "photo": pic(ind["photo"], ind["alt"], w=1120, h=628,
                                          eager=(i == 0))})

    cr = [("index.html", "Главная"), (None, "Отрасли")]
    return (head(
        "Отрасли — масла ЛУКОЙЛ автопаркам, заводам и агрохозяйствам",
        "Три направления поставок: автопарки и логистика, промышленность, сельхозтехника. "
        "График отгрузок под цикл ТО, карта смазки, доставка по республике.",
        "industries.html", [ld_crumbs(cr)], og_img="ind-pumps")
        + header("industries.html") + """
<section class="sec"><div class="wrap phead">
  %(cr)s
  <span class="tag tag-outline">Отрасли</span>
  <h1>Три направления, под которые собран склад</h1>
  <p class="lead" style="max-width:62ch">Работаем с юридическими лицами по договору поставки:
    график отгрузок под ваш цикл обслуживания, отсрочка платежа для постоянных клиентов,
    единая точка входа по всей номенклатуре.</p>
  <div class="actions">
    <a class="btn btn-primary" href="contacts.html">Оставить заявку</a>
    <a class="btn btn-secondary" href="tel:%(tel)s">%(phone)s</a>
  </div>
</div></section>
%(blocks)s
%(cta)s
""" % {"cr": crumbs(cr), "tel": TEL, "phone": e(PHONE),
       "blocks": "\n".join(blocks), "cta": cta()} + footer())


def page_about():
    steps = "".join('<div><b class="num">%s</b><div><h3 style="font-size:16px;margin:0 0 3px">%s</h3>'
                    '<p class="small muted" style="margin:0">%s</p></div></div>'
                    % (n, e(t), e(b)) for n, t, b in STEPS)
    docs = "".join('<div class="card"><div class="kicker">%s</div>'
                   '<div class="card-title">%s</div><p class="card-body">%s</p></div>'
                   % (e(k), e(t), e(b)) for k, t, b in DOCS)
    logi = "".join('<div><b>%s</b><span>%s</span></div>' % (e(a), e(b)) for a, b in LOGISTICS)

    cr = [("index.html", "Главная"), (None, "О компании")]
    return (head(
        "О компании — дистрибьютор масел ЛУКОЙЛ в Узбекистане",
        "Поставки по дистрибьюторскому соглашению: продукция напрямую с завода, паспорт "
        "качества на партию, склад 3 000 м² в Ташкенте.",
        "about.html", [ld_crumbs(cr)], og_img="bottling")
        + header("about.html") + """
<section class="sec"><div class="wrap phead" style="display:grid;grid-template-columns:1.3fr 1fr;
    gap:44px;align-items:end" data-two>
  <div>
    %(cr)s
    <span class="tag tag-outline">О компании</span>
    <h1>Дистрибьютор, а не перепродажа</h1>
    <p class="lead" style="max-width:60ch">Поставляем смазочные материалы ЛУКОЙЛ в Узбекистане
      на основании дистрибьюторского соглашения: продукция приходит напрямую с завода-изготовителя,
      минуя посредников и параллельный импорт.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);border-top:2px solid var(--divider)">
    <div style="padding:16px 16px 0 0;border-right:1px solid var(--hair)">
      <div style="font-weight:800;font-size:30px">с 2011</div>
      <div class="small muted">поставок в республике</div></div>
    <div style="padding:16px 0 0 16px">
      <div style="font-weight:800;font-size:30px">1 200+</div>
      <div class="small muted">организаций-клиентов</div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="split">
  <div class="split__body" style="padding-left:0;padding-right:48px;border-right:2px solid var(--divider)">
    <h2>Как устроена работа</h2>
    <div class="rows" style="margin-top:18px">%(steps)s</div>
  </div>
  <div class="split__body">
    <h2>Документы на партию</h2>
    <div style="display:flex;flex-direction:column;gap:12px;margin-top:18px">%(docs)s</div>
    <div class="grayscale" style="margin-top:20px;aspect-ratio:16/9;overflow:hidden">%(plant)s</div>
    <p class="small muted" style="margin-top:14px">Копии дистрибьюторского соглашения и сертификатов
      предоставляем вместе с коммерческим предложением.</p>
  </div>
</div></div></section>

<section class="sec"><div class="wrap"><div class="split split--narrow split--rev">
  <div class="split__media grayscale">%(photo)s</div>
  <div class="split__body" style="padding-left:0">
    <h2>Склад и логистика</h2>
    <div class="rows" style="margin-top:18px">%(logi)s</div>
    <div class="actions">
      <a class="btn btn-primary" href="contacts.html">Запросить прайс</a>
      <a class="btn btn-secondary" href="products.html">Смотреть каталог</a>
    </div>
  </div>
</div></div></section>
%(cta)s
""" % {"cr": crumbs(cr), "steps": steps, "docs": docs, "logi": logi,
       "photo": pic("bottling", "Линия розлива смазочных материалов", w=1400, h=760),
       "plant": pic("plant-t", "Нефтеперерабатывающий завод ЛУКОЙЛ", w=560, h=315),
       "cta": cta()} + footer())


def page_contacts():
    cr = [("index.html", "Главная"), (None, "Контакты")]
    ld = [ld_crumbs(cr), {
        "@context": "https://schema.org", "@type": "ContactPage",
        "url": BASE + "/contacts.html",
        "mainEntity": {"@id": BASE + "/#org"},
    }]
    return (head(
        "Контакты — отдел продаж и склад в Ташкенте, lukoil-oil.uz",
        "Телефон, почта и адрес склада: г. Ташкент, Мирабадский район, ул. Нукус, 71. "
        "Пн–сб 9:00–18:00, отгрузка до 17:00. Заявка на прайс и подбор масла.",
        "contacts.html", ld, og_img="map")
        + header("contacts.html") + """
<section class="sec"><div class="wrap"><div class="split">
  <div class="split__body" style="padding-left:0;padding-right:48px;border-right:2px solid var(--divider)">
    %(cr)s
    <span class="tag tag-outline">Контакты</span>
    <h1 style="margin:16px 0 14px">Отдел продаж и склад</h1>
    <p class="muted" style="max-width:46ch">Быстрее всего — позвонить или написать на почту.
      Заявку с формы тоже получаем письмом.</p>
    <div class="rows" style="margin-top:22px">
      <div><b style="min-width:110px">ТЕЛЕФОН</b>
        <span><a href="tel:%(tel)s" style="font-weight:800;font-size:20px;color:inherit;
          text-decoration:none">%(phone)s</a><br><span class="note">%(note)s</span></span></div>
      <div><b style="min-width:110px">E-MAIL</b>
        <span><a href="mailto:%(mail)s" style="color:inherit;text-decoration:none">%(mail)s</a><br>
        <a href="mailto:%(mail2)s" style="color:inherit;text-decoration:none">%(mail2)s</a></span></div>
      <div><b style="min-width:110px">АДРЕС</b><span>%(addr)s — офис и склад</span></div>
      <div><b style="min-width:110px">ЧАСЫ</b><span>%(hours)s</span></div>
    </div>
    <div class="actions">
      <a class="btn btn-primary" href="mailto:%(mail)s">Написать на почту</a>
      <button class="btn btn-secondary" type="button" data-callback>Обратный звонок</button>
    </div>
    <div style="margin-top:28px;border:2px solid var(--divider)">
      <div class="grayscale">%(map)s</div>
    </div>
    <p class="fineprint" style="margin-top:8px">Сеть поставок ЛУКОЙЛ. Точку на карте Ташкента
      и схему проезда к складу пришлём вместе с коммерческим предложением.</p>
  </div>
  <div class="split__body">%(form)s</div>
</div></div></section>
%(cta)s
""" % {"cr": crumbs(cr), "tel": TEL, "phone": e(PHONE), "note": e(NOTE), "mail": MAIL,
       "mail2": SITE["mail2"], "addr": e(SITE["addr"]), "hours": e(SITE["hours"]),
       "map": pic("map", "Карта дистрибуции ЛУКОЙЛ", w=1320, h=1530),
       "form": form("k", "Заявка на прайс или подбор",
                    "Опишите технику и объём — вернём цены и сроки в тот же день.",
                    "Техника и объём",
                    "Модели техники, наработка, требуемые объёмы и тара"),
       "cta": cta()} + footer())


def page_404():
    return (head("Страница не найдена — Смазочные материалы ЛУКОЙЛ",
                 "Такой страницы нет. Перейдите в каталог продукции или свяжитесь с отделом продаж.",
                 "404.html")
            + header("") + """
<section class="sec"><div class="wrap sec-pad" style="min-height:44vh">
  <span class="tag tag-outline">Ошибка 404</span>
  <h1 style="margin:18px 0 14px">Такой страницы нет</h1>
  <p class="lead" style="max-width:52ch">Возможно, адрес изменился. Загляните в каталог продукции
    или позвоните — подскажем нужную позицию за минуту.</p>
  <div class="actions">
    <a class="btn btn-primary" href="products.html">В каталог</a>
    <a class="btn btn-secondary" href="tel:%(tel)s">%(phone)s</a>
    <a class="btn btn-ghost" href="index.html">На главную</a>
  </div>
</div></section>
%(cta)s
""" % {"tel": TEL, "phone": e(PHONE), "cta": cta()} + footer())


def sitemap(pages):
    urls = "".join(
        '<url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>'
        % (BASE + ("/" if p == "index.html" else "/" + p), pr) for p, pr in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)


def minify(s):
    """Аккуратная минификация: схлопываем отступы, но не трогаем содержимое тегов."""
    s = re.sub(r"\n\s*\n+", "\n", s)
    s = re.sub(r"\n\s{2,}", "\n", s)
    return s


def write(name, data):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(data)
    print("  %-32s %6.1f КБ" % (name, len(data.encode("utf-8")) / 1024))


def main():
    print("Сборка lukoil-oil.uz")
    write("index.html", minify(page_index()))
    write("products.html", minify(page_products()))
    for c in CATS:
        write(c["slug"] + ".html", minify(page_cat(c)))
    write("industries.html", minify(page_industries()))
    write("about.html", minify(page_about()))
    write("contacts.html", minify(page_contacts()))
    write("404.html", minify(page_404()))

    pages = ([("index.html", "1.0"), ("products.html", "0.9")]
             + [(c["slug"] + ".html", "0.8") for c in CATS]
             + [("industries.html", "0.7"), ("about.html", "0.6"), ("contacts.html", "0.8")])
    write("sitemap.xml", sitemap(pages))
    write("robots.txt", "User-agent: *\nAllow: /\n"
                     "Disallow: /README.md\nDisallow: /PHOTO.md\n"
                     "Disallow: /build.py\nDisallow: /content.py\n\n"
                     "Sitemap: %s/sitemap.xml\n" % BASE)
    write("CNAME", SITE["domain"] + "\n")
    print("Готово: %d страниц" % (len(pages) + 1))


if __name__ == "__main__":
    main()

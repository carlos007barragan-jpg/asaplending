#!/usr/bin/env python3
"""ASAP Lending site generator.
One template per page, both languages inline as [[English||Español]].
Every page gets the same header/footer, so the nav is identical everywhere.
Usage: python3 build.py <output_dir>
"""
import json, os, re, sys

OUT = sys.argv[1]
BASE = "https://asaplendinggroup.com/"
EMAIL = "funding@asaplendinggroup.com"
SHOW_EMAIL = False   # funding@ sends but has no inbox yet; show it once the alias exists
PHONE_D, PHONE_T = "(913) 513-2656", "+19135132656"
STREET, CITY = "7017 Oak Street", "Kansas City, MO"
LANG = "en"
LD = []


def tr(s):
    return re.sub(r"\[\[(.*?)\|\|(.*?)\]\]", lambda m: m.group(1 if LANG == "en" else 2), s, flags=re.S)


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


NAV = [
    ("fix-and-flip", "[[Fix &amp; Flip||Fix &amp; Flip]]"),
    ("dscr", "[[DSCR Rentals||Rentas DSCR]]"),
    ("construction", "[[Construction||Construcción]]"),
    ("hard-money-loans", "[[Hard Money||Dinero Privado]]"),
    ("calculator", "[[Calculator||Calculadora]]"),
    ("about", "[[About||Nosotros]]"),
    ("contact", "[[Contact||Contacto]]"),
]


def logo(light=False):
    return ('<a class="logo" href="index.html" aria-label="ASAP Lending"><img src="@@A@@logo-on-%s.svg" alt="ASAP Lending" width="%d" height="%d"></a>'
            % ("black" if light else "white", 114, 46) if not light else
            '<a class="logo" href="index.html" aria-label="ASAP Lending"><img src="@@A@@logo-on-black.svg" alt="ASAP Lending" width="133" height="54"></a>')


def header(slug):
    twin = ("es/" if LANG == "en" else "../") + slug + ".html"
    pill = ('<span class="on">EN</span><a href="%s" lang="es" hreflang="es">ES</a>' % twin if LANG == "en"
            else '<a href="%s" lang="en" hreflang="en">EN</a><span class="on">ES</span>' % twin)
    links = "".join('<a href="%s.html"%s>%s</a>' % (s, ' class="on" aria-current="page"' if s == slug else "", l) for s, l in NAV)
    return """
<div class="topbar"><div class="wrap">
  <span class="tb-states">MO · KS · FL · TX · AR · NE</span>
  <span class="sp">[[Call or text||Llame o envíe texto]] <a href="tel:%s">%s</a></span>
  <span class="langpill" aria-label="[[Language||Idioma]]">%s</span>
</div></div>
<header class="nav"><div class="wrap">
  %s
  <button class="burger" aria-label="[[Menu||Menú]]" aria-expanded="false"><span></span></button>
  <nav class="links" aria-label="[[Main||Principal]]">%s<a class="cta" href="apply.html">[[Apply Now||Aplicar]]</a></nav>
</div></header>
<div class="stripe" aria-hidden="true"></div>
""" % (PHONE_T, PHONE_D, pill, logo(), links)


def footer():
    return """
<footer><div class="wrap">
  <div class="cols">
    <div>%s
      <p style="margin-top:16px;max-width:34ch">[[Private financing for real estate investors. Underwritten on the deal, from an office you can walk into.||Financiamiento privado para inversionistas de bienes raíces. Evaluamos el proyecto, desde una oficina que usted puede visitar.]]</p>
    </div>
    <div><h4>[[Programs||Programas]]</h4><ul>
      <li><a href="fix-and-flip.html">[[Fix &amp; flip loans||Préstamos fix &amp; flip]]</a></li>
      <li><a href="dscr.html">[[DSCR rental loans||Préstamos DSCR para rentas]]</a></li>
      <li><a href="construction.html">[[Construction loans||Préstamos de construcción]]</a></li>
      <li><a href="hard-money-loans.html#transactional">[[Transactional funding||Fondeo transaccional]]</a></li>
    </ul></div>
    <div><h4>[[Company||Empresa]]</h4><ul>
      <li><a href="hard-money-loans.html">[[Hard money explained||Qué es el dinero privado]]</a></li>
      <li><a href="calculator.html">[[Deal calculators||Calculadoras]]</a></li>
      <li><a href="about.html">[[About us||Nosotros]]</a></li>
      <li><a href="about.html#partners">[[Referral partners||Socios de referidos]]</a></li>
      <li><a href="privacy.html">[[Privacy||Privacidad]]</a></li>
    </ul></div>
    <div><h4>[[Contact||Contacto]]</h4><ul>
      <li><a href="tel:%s">%s</a></li>
      <li><a href="mailto:funding@asaplending.com">funding@asaplending.com</a></li>
      <li>%s<br>%s</li>
      <li><a href="apply.html">[[Start an application||Iniciar una solicitud]]</a></li>
    </ul></div>
  </div>
  <div class="legal">
    <p>[[ASAP Lending provides and arranges business-purpose financing secured by non-owner-occupied investment real estate in Missouri, Kansas, Florida, Texas, Arkansas and Nebraska. We do not make consumer loans or loans on a home you live in. Loans may be funded by ASAP Lending or its capital partners.||ASAP Lending ofrece y gestiona financiamiento con fines comerciales, garantizado con propiedades de inversión no ocupadas por el dueño, en Missouri, Kansas, Florida, Texas, Arkansas y Nebraska. No hacemos préstamos de consumo ni préstamos sobre la casa donde usted vive. Los préstamos pueden ser fondeados por ASAP Lending o por sus socios de capital.]]</p>
    <p>[[Nothing on this site is a commitment to lend or a quote. All financing is subject to underwriting, valuation and title review. Calculator results are estimates from the numbers you enter.||Nada en este sitio es un compromiso de préstamo ni una cotización. Todo financiamiento está sujeto a evaluación, avalúo y revisión de título. Los resultados de las calculadoras son estimaciones basadas en los números que usted ingresa.]]</p>
    <p>© <span id="yr">2026</span> ASAP Lending · %s, %s</p>
  </div>
</div></footer>
<div class="mbar"><a href="tel:%s" aria-label="%s">[[Call||Llamar]]</a><a class="go" href="apply.html">[[Apply Now||Aplicar ahora]]</a></div>
""" % (logo(True), PHONE_T, PHONE_D, STREET, CITY, STREET, CITY, PHONE_T, PHONE_D)


STATES = [("MO", "Missouri", "Missouri"), ("KS", "Kansas", "Kansas"), ("FL", "Florida", "Florida"),
          ("TX", "Texas", "Texas"), ("AR", "Arkansas", "Arkansas"), ("NE", "Nebraska", "Nebraska")]
STATE_OPTS = "".join('<option value="%s">%s</option>' % (a, n) for a, n, _ in STATES)


def lead_form(src, fid, title, tagtxt, button, interest=None):
    opts = [("Investor lending — Fix & Flip", "[[Fix &amp; flip||Fix &amp; flip]]"),
            ("Investor lending — DSCR", "[[DSCR rental loan||Préstamo DSCR para renta]]"),
            ("Investor lending — Construction", "[[Construction or heavy rehab||Construcción o remodelación mayor]]"),
            ("Investor lending — Transactional", "[[Transactional funding||Fondeo transaccional]]"),
            ("Investor lending — Other", "[[Something else||Otro]]")]
    if interest:
        sel = '<input type="hidden" name="interest" value="%s">' % interest
    else:
        sel = ('<label for="%s-int">[[Loan type||Tipo de préstamo]]<select id="%s-int" name="interest">%s</select></label>'
               % (fid, fid, "".join('<option value="%s">%s</option>' % o for o in opts)))
    st = ('<label for="%s-state">[[Property state||Estado de la propiedad]]<select id="%s-state" name="state"><option value="">[[Choose||Elija]]</option>%s</select></label>'
          % (fid, fid, STATE_OPTS))
    selrow = (sel + st) if interest else '<div class="row">%s%s</div>' % (sel, st)
    return """
<div class="fcard" id="%(f)s-card">
  <div class="ftop"><h2>%(title)s</h2><span class="tag">%(tag)s</span></div>
  <form data-lead="%(src)s" id="%(f)s" novalidate-off>
    <div class="row">
      <label for="%(f)s-name">[[Your name||Su nombre]]<input id="%(f)s-name" name="name" autocomplete="name" required></label>
      <label for="%(f)s-phone">[[Cell phone||Celular]]<input id="%(f)s-phone" name="phone" type="tel" autocomplete="tel" required></label>
    </div>
    <label for="%(f)s-email">[[Email||Correo electrónico]] <span class="opt">([[optional||opcional]])</span><input id="%(f)s-email" name="email" type="email" autocomplete="email"></label>
    %(selrow)s
    <label for="%(f)s-msg">[[The deal||El proyecto]] <span class="opt">([[address, price, rehab budget, exit||dirección, precio, presupuesto, salida]])</span><textarea id="%(f)s-msg" name="msg" rows="3"></textarea></label>
    <input class="hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn wide arrow" type="submit">%(button)s</button>
    <div class="fmsg" role="status"></div>
    <p class="fine">[[By sending this you agree we may call or text the number you gave about your request. Message and data rates may apply. Reply STOP to opt out.||Al enviar acepta que le llamemos o enviemos textos al número indicado sobre su solicitud. Pueden aplicar cargos de mensajes y datos. Responda STOP para cancelar.]]</p>
  </form>
</div>""".replace(" novalidate-off", "") % dict(f=fid, title=title, tag=tagtxt, src=src, selrow=selrow, button=button)


def faq(items):
    out = ['<div class="faq">']
    ents = []
    for q, a in items:
        out.append("<details><summary>%s</summary><p>%s</p></details>" % (q, a))
        ents.append({"@type": "Question", "name": strip(tr(q)), "acceptedAnswer": {"@type": "Answer", "text": strip(tr(a))}})
    out.append("</div>")
    LD.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents})
    return "\n".join(out)


def band(h="[[Have a deal under contract? Send it today.||¿Tiene una propiedad bajo contrato? Envíela hoy.]]",
         p="[[Complete submissions get an answer the same business day, with a free review of your ARV.||Las solicitudes completas reciben respuesta el mismo día hábil, con una revisión gratuita de su ARV.]]"):
    return """
<div class="stripe" aria-hidden="true"></div>
<section class="band" style="padding:64px 0"><div class="wrap">
  <div><h2>%s</h2><p>%s</p></div>
  <div class="acts"><a class="btn yellow arrow" href="apply.html">[[Start my application||Iniciar mi solicitud]]</a><a class="btn ghost" href="tel:%s">[[Call||Llamar]] %s</a></div>
</div></section>""" % (h, p, PHONE_T, PHONE_D)


def subhero(crumb, eyebrow, h1, lead, acts=""):
    return """
<section class="hero sub-hero"><div class="wrap">
  <div class="crumbs"><a href="index.html">[[Home||Inicio]]</a><span>/</span><span>%s</span></div>
  <h1>%s</h1>
  <p class="lead">%s</p>
  %s
</div></section>""" % (crumb, h1, lead, ('<div class="acts">%s</div>' % acts) if acts else "")


APPLY_BTN = '<a class="btn arrow" href="apply.html">[[Apply now||Aplicar ahora]]</a>'
CALC_BTN = '<a class="btn ghost" href="calculator.html">[[Run the numbers||Haga los números]]</a>'

STATES_HTML = '<div class="states">' + "".join(
    '<div class="state%s"><b>%s</b><span>[[%s||%s]]</span>%s</div>' % (
        " hq" if a == "MO" else "", a, en, es, "<em>[[HEADQUARTERS||SEDE]]</em>" if a == "MO" else "")
    for a, en, es in STATES) + "</div>"

ICON = {
    "flip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>',
    "rent": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="8" cy="15" r="4"/><path d="m11 12 9-9"/><path d="m16 7 3 3"/></svg>',
    "build": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 21V4h10"/><path d="M4 8h14l2 3"/><path d="M14 8v6"/><rect x="11" y="14" width="6" height="4"/><path d="M2 21h20"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 8h15l-4-4"/><path d="M20 16H5l4 4"/></svg>',
}

# ───────────────────────── pages ─────────────────────────

def p_index():
    form = lead_form("Homepage quick request", "q", "[[Get my terms||Obtener mis términos]]", "[[Same-day answer||Respuesta el mismo día]]", "[[Send my deal||Enviar mi proyecto]]")
    fq = faq([
        ("[[What kinds of financing do you offer?||¿Qué tipos de financiamiento ofrecen?]]",
         "[[Fix and flip loans that cover purchase and rehab, DSCR loans for rentals, construction and heavy-rehab loans funded in stages (new builds depend on borrower and state), and transactional funding for double closings. If your deal does not fit one of those, send it anyway and we will tell you what we can structure.||Préstamos fix &amp; flip que cubren compra y remodelación, préstamos DSCR para rentas, préstamos de construcción y remodelación mayor por etapas (la obra nueva depende del prestatario y del estado), y fondeo transaccional para cierres dobles. Si su proyecto no encaja en uno de esos, envíelo de todos modos y le diremos qué podemos estructurar.]]"),
        ("[[Why don't you post rates?||¿Por qué no publican tasas?]]",
         "[[Because a posted rate is rarely the rate you get. Each loan is priced on its own numbers: the property, the scope of work, your experience and your exit. Send the deal and you get written terms for that deal.||Porque la tasa publicada casi nunca es la que usted recibe. Cada préstamo se cotiza con sus propios números: la propiedad, el alcance de obra, su experiencia y su salida. Envíe el proyecto y recibirá términos por escrito para ese proyecto.]]"),
        ("[[Do you check credit or income?||¿Revisan crédito o ingresos?]]",
         "[[The deal carries the weight. Our asset-based loans have no credit requirement, and we do not ask for W-2s or tax returns on them. Some other loan types do need a credit check. Applying never pulls your credit: we walk you through the programs first, and credit is only pulled if the program needs it or you choose one that does, before your term sheet is written.||El proyecto es lo que más pesa. Nuestros préstamos basados en el activo no tienen requisito de crédito, y en ellos no pedimos W-2 ni declaraciones de impuestos. Otros tipos de préstamo sí requieren revisar el crédito. Aplicar nunca consulta su crédito: primero le explicamos los programas, y el crédito solo se consulta si el programa lo requiere o si usted elige uno que lo requiera, antes de preparar su hoja de términos.]]"),
        ("[[I have never done a flip. Will you look at my deal?||Nunca he hecho un flip. ¿Revisan mi proyecto?]]",
         "[[Yes. We fund first-time investors when the deal's underwriting is sound.||Sí. Financiamos a inversionistas nuevos cuando la evaluación del proyecto es sólida.]]"),
        ("[[How fast can you close?||¿Qué tan rápido pueden cerrar?]]",
         "[[Days on a clean deal, not weeks. Timing depends on title work and valuation, and we tell you the realistic date up front.||Días en un proyecto limpio, no semanas. El tiempo depende del trabajo de título y del avalúo, y le decimos la fecha realista desde el principio.]]"),
        ("[[Where do you lend?||¿Dónde prestan?]]",
         "[[Missouri, Kansas, Florida, Texas, Arkansas and Nebraska. Our office is in Kansas City.||Missouri, Kansas, Florida, Texas, Arkansas y Nebraska. Nuestra oficina está en Kansas City.]]"),
        ("[[Do you lend on a home I plan to live in?||¿Prestan para una casa donde voy a vivir?]]",
         "[[No. We finance investment property for business purposes only.||No. Solo financiamos propiedades de inversión con fines comerciales.]]"),
    ])
    return """
<section class="hero"><div class="wrap split">
  <div>
    <span class="eyebrow">[[Hard money · Fix &amp; flip · DSCR · Construction||Dinero privado · Fix &amp; flip · DSCR · Construcción]]</span>
    <h1>[[Send us the address. We'll tell you what the deal can <span class="hl">borrow</span>.||Mándenos la dirección. Le decimos cuánto puede <span class="hl">financiar</span>.]]</h1>
    <p class="lead">[[ASAP Lending finances investment property in six states from our office in Kansas City. We underwrite the property and the plan, fund the rehab in draws, and answer complete submissions the same business day.||ASAP Lending financia propiedades de inversión en seis estados desde nuestra oficina en Kansas City. Evaluamos la propiedad y el plan, fondeamos la remodelación por etapas y respondemos las solicitudes completas el mismo día hábil.]]</p>
    <ul class="ticks">
      <li>[[No W-2s or tax returns||Sin W-2 ni declaraciones]]</li>
      <li>[[LLC friendly||Aceptamos LLC]]</li>
      <li>[[First-time flippers welcome||Inversionistas nuevos bienvenidos]]</li>
    </ul>
    <div class="acts">
      <a class="btn arrow" href="apply.html">[[Start the full application||Iniciar la solicitud completa]]</a>
      <a class="btn ghost" href="calculator.html">[[Check my deal first||Revisar mi proyecto primero]]</a>
    </div>
  </div>
  %(form)s
</div></section>

<div class="facts"><div class="wrap">
  <div class="fact"><b>[[Same day||Mismo día]]</b><span>[[answers on complete submissions||respuesta a solicitudes completas]]</span></div>
  <div class="fact"><b>[[6 states||6 estados]]</b><span>[[one phone call, one office in Kansas City||una llamada, una oficina en Kansas City]]</span></div>
  <div class="fact"><b>[[1st position||1.ª posición]]</b><span>[[closed at a title company, title insured||cierre en compañía de títulos, con seguro de título]]</span></div>
  <div class="fact"><b>$30M+</b><span>[[in real estate closed by our principals' companies||en bienes raíces cerrados por las empresas de nuestros socios]]</span></div>
</div></div>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Loan programs||Programas de préstamo]]</span>
    <h2>[[Four ways we put capital into a deal||Cuatro formas de poner capital en un proyecto]]</h2>
    <p class="lead">[[Pick the one that matches your exit. If you are not sure, apply and we will match it for you.||Elija el que corresponde a su salida. Si no está seguro, aplique y nosotros lo ubicamos.]]</p></div>
  <div class="grid g4">
    <article class="card feature"><div class="ico">%(i_flip)s</div><h3>[[Fix &amp; flip||Fix &amp; flip]]</h3>
      <p>[[Purchase and rehab in one loan.||Compra y remodelación en un solo préstamo.]]</p>
      <ul><li>[[Underwritten on the asset||Evaluado sobre el activo]]</li><li>[[Rehab funded on draws||Remodelación por desembolsos]]</li><li>[[Interest-only during the project||Solo intereses durante la obra]]</li></ul>
      <div class="more"><a class="tlink" href="fix-and-flip.html">[[How flip loans work||Cómo funcionan]] →</a></div></article>
    <article class="card"><div class="ico">%(i_rent)s</div><h3>[[DSCR rental||DSCR para rentas]]</h3>
      <p>[[The rent qualifies the loan.||La renta califica el préstamo.]]</p>
      <ul><li>[[No personal income verification||Sin verificación de ingresos personales]]</li><li>[[Lend to your LLC||Préstamo a su LLC]]</li><li>[[Refinance a finished flip and hold it||Refinancie un flip terminado y consérvelo]]</li></ul>
      <div class="more"><a class="tlink" href="dscr.html">[[How DSCR works||Cómo funciona DSCR]] →</a></div></article>
    <article class="card"><div class="ico">%(i_build)s</div><h3>[[Construction||Construcción]]</h3>
      <p>[[Ground-up builds and heavy rehab.||Obra nueva y remodelación mayor.]]</p>
      <ul><li>[[Funded in stages as work is verified||Fondeado por etapas al verificar avances]]</li><li>[[Reviewed deal by deal||Revisado caso por caso]]</li><li>[[Ground-up depends on borrower and state||Obra nueva depende del prestatario y del estado]]</li></ul>
      <div class="more"><a class="tlink" href="construction.html">[[How draws work||Cómo funcionan los desembolsos]] →</a></div></article>
    <article class="card"><div class="ico">%(i_swap)s</div><h3>[[Transactional||Transaccional]]</h3>
      <p>[[Short capital for a double close.||Capital corto para un cierre doble.]]</p>
      <ul><li>[[Built for wholesalers||Hecho para mayoristas]]</li><li>[[A-to-B funded, B-to-C repays||A-B se fondea, B-C lo paga]]</li><li>[[Acquisition only, no rehab||Solo adquisición, sin remodelación]]</li></ul>
      <div class="more"><a class="tlink" href="hard-money-loans.html#transactional">[[When to use it||Cuándo usarlo]] →</a></div></article>
  </div>
</div></section>

<section class="paper"><div class="wrap split">
  <div>
    <div class="shead" style="margin-bottom:26px"><span class="eyebrow">[[What we underwrite||Qué evaluamos]]</span>
      <h2>[[Three numbers drive every flip loan||Tres números mueven cada préstamo fix &amp; flip]]</h2>
      <p class="lead">[[Purchase price, rehab budget and after-repair value. Bring those and a plan to get out, and we can size the loan.||Precio de compra, presupuesto de remodelación y valor después de reparaciones (ARV). Traiga eso y un plan de salida, y podemos dimensionar el préstamo.]]</p></div>
    <ul class="check">
      <li><b>[[Purchase contract||Contrato de compra]]</b><span>[[Signed, or the offer you are about to make.||Firmado, o la oferta que está por hacer.]]</span></li>
      <li><b>[[Scope of work||Alcance de obra]]</b><span>[[Line items with costs. A clear scope supports a stronger ARV.||Partidas con costos. Un alcance claro respalda un mejor ARV.]]</span></li>
      <li><b>[[Your ARV estimate||Su estimado de ARV]]</b><span>[[We check it against renovated comps near the property at no charge.||Lo comparamos sin costo con ventas remodeladas cerca de la propiedad.]]</span></li>
      <li><b>[[Entity documents and insurance||Documentos de la entidad y seguro]]</b><span>[[We lend to your LLC.||Prestamos a su LLC.]]</span></li>
    </ul>
  </div>
  <div class="ticket" aria-label="[[Example deal file||Ejemplo de expediente]]">
    <div class="th"><span>[[Deal file · example||Expediente · ejemplo]]</span><b>[[Terms issued||Términos emitidos]]</b></div>
    <dl>
      <div><dt>[[Property||Propiedad]]</dt><dd>4418 Example Ave, KCMO</dd></div>
      <div><dt>[[Purchase price||Precio de compra]]</dt><dd>$118,000</dd></div>
      <div><dt>[[Rehab budget||Presupuesto de obra]]</dt><dd>$46,500</dd></div>
      <div><dt>[[ARV, checked against comps||ARV, verificado con comparables]]</dt><dd>$242,000</dd></div>
      <div><dt>[[Exit||Salida]]</dt><dd>[[Sell, list in month 5||Venta, listar en mes 5]]</dd></div>
      <div><dt>[[Rehab funding||Fondos de obra]]</dt><dd>[[4 draws||4 desembolsos]]</dd></div>
    </dl>
    <div class="tf">[[Illustration only. Your terms are written for your deal.||Solo ilustrativo. Sus términos se escriben para su proyecto.]]</div>
  </div>
</div></section>

<section class="ink"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[From submission to payoff||De la solicitud al pago final]]</span>
    <h2>[[How a deal moves through ASAP||Cómo avanza un proyecto en ASAP]]</h2></div>
  <div class="steps">
    <div class="step"><span class="num">01</span><h3>[[Submit||Envíe]]</h3><p>[[Address, numbers and exit. Five minutes online.||Dirección, números y salida. Cinco minutos en línea.]]</p></div>
    <div class="step"><span class="num">02</span><h3>[[Review||Revisión]]</h3><p>[[A decision-maker reads it the same business day.||Una persona que decide lo lee el mismo día hábil.]]</p></div>
    <div class="step"><span class="num">03</span><h3>[[Written terms||Términos por escrito]]</h3><p>[[A term sheet for this deal, not a rate card.||Una hoja de términos para este proyecto, no una tabla genérica.]]</p></div>
    <div class="step"><span class="num">04</span><h3>[[Value and title||Valor y título]]</h3><p>[[We confirm value; the title company clears the file.||Confirmamos el valor; la compañía de títulos limpia el expediente.]]</p></div>
    <div class="step"><span class="num">05</span><h3>[[Close||Cierre]]</h3><p>[[Sign at title. Purchase funds go out.||Firma en títulos. Sale el dinero de la compra.]]</p></div>
    <div class="step"><span class="num">06</span><h3>[[Draws, then payoff||Desembolsos y pago final]]</h3><p>[[Rehab money releases as work is verified. Sell or refinance to pay off.||El dinero de obra se libera al verificar avances. Venda o refinancie para liquidar.]]</p></div>
  </div>
</div></section>

<section><div class="wrap split even">
  <div>
    <span class="eyebrow">[[Why ASAP||Por qué ASAP]]</span>
    <h2 style="margin:14px 0 18px">[[We flip and build the same kind of houses we finance||Remodelamos y construimos el mismo tipo de casas que financiamos]]</h2>
    <p class="lead">[[Our principals buy, renovate and sell property across the Kansas City metro. That is why our questions sound like a contractor's and our answers come fast.||Nuestros socios compran, remodelan y venden propiedades en el área de Kansas City. Por eso nuestras preguntas suenan a las de un contratista y nuestras respuestas llegan rápido.]]</p>
    <p style="margin-top:22px"><a class="tlink" href="about.html">[[Meet the company||Conozca la empresa]] →</a></p>
  </div>
  <ul class="check">
    <li><b>[[Structure||Estructura]]</b><span>[[First-position loans, clear documents, closings at a title company.||Préstamos en primera posición, documentos claros, cierres en compañía de títulos.]]</span></li>
    <li><b>[[Transparency||Transparencia]]</b><span>[[Your costs are on the term sheet before you commit.||Sus costos están en la hoja de términos antes de comprometerse.]]</span></li>
    <li><b>[[Execution||Ejecución]]</b><span>[[We do what the term sheet says, on the date it says.||Hacemos lo que dice la hoja de términos, en la fecha que dice.]]</span></li>
    <li><b>[[A real office||Una oficina real]]</b><span>%(street)s, %(city)s.</span></li>
  </ul>
</div></section>

<section class="paper"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Free tools||Herramientas gratis]]</span>
    <h2>[[Run the deal before you send it||Haga los números antes de enviarlo]]</h2></div>
  <div class="grid g3">
    <a class="card" href="calculator.html#flip" style="text-decoration:none;color:inherit"><span class="num">A</span><h3>[[Flip deal analyzer||Analizador de flip]]</h3><p>[[Cash in, cost of capital and projected profit.||Efectivo necesario, costo del capital y ganancia proyectada.]]</p><div class="more"><span class="tlink">[[Open||Abrir]] →</span></div></a>
    <a class="card" href="calculator.html#offer" style="text-decoration:none;color:inherit"><span class="num">B</span><h3>[[Maximum offer||Oferta máxima]]</h3><p>[[Work back from ARV to the most you should pay.||Parta del ARV para saber lo máximo que debe pagar.]]</p><div class="more"><span class="tlink">[[Open||Abrir]] →</span></div></a>
    <a class="card" href="calculator.html#dscr" style="text-decoration:none;color:inherit"><span class="num">C</span><h3>[[DSCR check||Revisión DSCR]]</h3><p>[[See whether the rent covers the payment.||Vea si la renta cubre el pago.]]</p><div class="more"><span class="tlink">[[Open||Abrir]] →</span></div></a>
  </div>
</div></section>

<section data-gallery hidden><div class="wrap">
  <div class="shead"><span class="eyebrow">[[The work||El trabajo]]</span><h2>[[The kind of projects we fund||El tipo de proyectos que financiamos]]</h2></div>
  <div class="gallery">
    <figure class="wide"><img src="@@A@@photos/exterior.jpg" alt="[[Renovated ranch house with new siding, cedar accents and black windows||Casa remodelada con revestimiento nuevo, detalles de cedro y ventanas negras]]" loading="lazy"><figcaption>[[Finished exterior||Exterior terminado]]</figcaption></figure>
    <figure><img src="@@A@@photos/rehab.jpg" alt="[[Interior taken down to the studs with new floor framing||Interior hasta la estructura con piso nuevo en proceso]]" loading="lazy"><figcaption>[[Mid-rehab||En plena obra]]</figcaption></figure>
    <figure><img src="@@A@@photos/kitchen.jpg" alt="[[Finished white kitchen with a gas range||Cocina blanca terminada con estufa de gas]]" loading="lazy"><figcaption>[[Finished kitchen||Cocina terminada]]</figcaption></figure>
  </div>
</div></section>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Where we lend||Dónde prestamos]]</span>
    <h2>[[Six states, underwritten from Kansas City||Seis estados, evaluados desde Kansas City]]</h2></div>
  %(states)s
</div></section>

<section class="paper"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Questions||Preguntas]]</span><h2>[[What investors ask us first||Lo que los inversionistas preguntan primero]]</h2></div>
  %(faq)s
</div></section>
%(band)s
""" % dict(form=form, i_flip=ICON["flip"], i_rent=ICON["rent"], i_build=ICON["build"], i_swap=ICON["swap"],
           street=STREET, city=CITY, states=STATES_HTML, faq=fq, band=band())


def p_flip():
    form = lead_form("Fix & flip page", "ff", "[[Send a flip||Envíe un flip]]", "[[Free ARV review||Revisión de ARV gratis]]", "[[Get my terms||Obtener mis términos]]", "Investor lending — Fix & Flip")
    fq = faq([
        ("[[How much can I borrow?||¿Cuánto puedo pedir prestado?]]", "[[Loan size comes from three numbers: purchase price, rehab budget and ARV. We size it on your deal and put it in writing before you commit to anything.||El monto sale de tres números: precio de compra, presupuesto de remodelación y ARV. Lo calculamos para su proyecto y se lo damos por escrito antes de que se comprometa.]]"),
        ("[[How do rehab draws work?||¿Cómo funcionan los desembolsos de obra?]]", "[[Your rehab budget is set aside at closing. Finish a phase, a quick inspection verifies it, and that phase's money is released. You never front the whole rehab.||Su presupuesto de obra se aparta al cierre. Termine una etapa, una inspección rápida la verifica y se libera el dinero de esa etapa. Usted nunca adelanta toda la remodelación.]]"),
        ("[[Can I close in my LLC?||¿Puedo cerrar con mi LLC?]]", "[[Yes. We lend to LLCs and other business entities.||Sí. Prestamos a LLC y otras entidades de negocio.]]"),
        ("[[What if I decide to keep the house?||¿Y si decido quedarme con la casa?]]", "[[Finish the rehab on the flip loan, then refinance into a DSCR rental loan and hold it.||Termine la remodelación con el préstamo de flip y luego refinancie a un préstamo DSCR para rentarla.]]"),
        ("[[What happens if the rehab runs long?||¿Qué pasa si la obra se alarga?]]", "[[Tell us early. Your written terms spell out the loan term and what your options are if you need more time.||Avísenos pronto. Sus términos por escrito indican el plazo del préstamo y sus opciones si necesita más tiempo.]]"),
    ])
    return subhero("[[Fix &amp; flip loans||Préstamos fix &amp; flip]]", "", "[[Fix and flip loans built around the deal||Préstamos fix &amp; flip hechos alrededor del proyecto]]",
                   "[[One loan for the purchase and the rehab. We underwrite the property and your plan, fund the work in draws and stay out of your tax returns.||Un préstamo para la compra y la remodelación. Evaluamos la propiedad y su plan, fondeamos la obra por etapas y no le pedimos declaraciones de impuestos.]]",
                   APPLY_BTN + CALC_BTN) + """
<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[How it works||Cómo funciona]]</span><h2>[[Four parts to every flip loan||Cuatro partes de cada préstamo de flip]]</h2></div>
  <div class="steps">
    <div class="step"><span class="num">01 · [[THE DEAL||EL PROYECTO]]</span><h3>[[We underwrite the asset||Evaluamos el activo]]</h3><p>[[Purchase price, rehab budget and ARV, set by what renovated homes near yours actually sold for.||Precio de compra, presupuesto de obra y ARV, según lo que realmente se vendieron casas remodeladas cerca de la suya.]]</p></div>
    <div class="step"><span class="num">02 · [[THE SCOPE||EL ALCANCE]]</span><h3>[[Your scope sets your ARV||Su alcance define su ARV]]</h3><p>[[A line-item plan lets us comp your house against homes finished to the same standard.||Un plan por partidas nos permite comparar su casa con otras terminadas al mismo nivel.]]</p></div>
    <div class="step"><span class="num">03 · [[THE DRAWS||LOS DESEMBOLSOS]]</span><h3>[[Rehab funded in stages||Obra fondeada por etapas]]</h3><p>[[Finish a phase, pass a quick inspection, get the next draw. Crews keep moving.||Termine una etapa, pase una inspección rápida y reciba el siguiente desembolso. La cuadrilla no se detiene.]]</p></div>
    <div class="step"><span class="num">04 · [[THE EXIT||LA SALIDA]]</span><h3>[[Sell it or hold it||Véndala o consérvela]]</h3><p>[[Interest-only during the project. Pay off by selling, or roll into a DSCR rental loan.||Solo intereses durante la obra. Liquide al vender, o pase a un préstamo DSCR para renta.]]</p></div>
  </div>
</div></section>

<section class="paper"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Three borrower paths||Tres perfiles de prestatario]]</span><h2>[[Where you fit||Dónde encaja usted]]</h2>
  <p class="lead">[[Every path uses the same structure. What changes is how much weight the property carries.||Todos los perfiles usan la misma estructura. Lo que cambia es cuánto pesa la propiedad.]]</p></div>
  <div class="grid g3">
    <article class="card"><span class="num">[[PATH A||PERFIL A]]</span><h3>[[Strong credit, clear exit||Buen crédito, salida clara]]</h3><p>[[Experienced investors with established credit. Our most competitive pricing. This path uses a credit check, which we tell you about before it happens.||Inversionistas con experiencia y crédito establecido. Nuestros mejores precios. Este perfil usa una consulta de crédito, y le avisamos antes de hacerla.]]</p></article>
    <article class="card"><span class="num">[[PATH B||PERFIL B]]</span><h3>[[Flexible credit||Crédito flexible]]</h3><p>[[You know how to run a flip but your credit is thin or bruised. Same structure, more room on credit.||Usted sabe manejar un flip pero su crédito es corto o tiene golpes. Misma estructura, más flexibilidad.]]</p></article>
    <article class="card feature"><span class="num" style="color:#fff">[[PATH C||PERFIL C]]</span><h3>[[Asset-based||Basado en el activo]]</h3><p>[[The deal carries the loan. No credit requirement; we look at the property, the numbers and your cash in the project.||El proyecto sostiene el préstamo. Sin requisito de crédito; vemos la propiedad, los números y su efectivo en el proyecto.]]</p></article>
  </div>
</div></section>

<section><div class="wrap split">
  <div>
    <span class="eyebrow">[[What to send||Qué enviar]]</span>
    <h2 style="margin:14px 0 24px">[[A complete file gets a same-day answer||Un expediente completo recibe respuesta el mismo día]]</h2>
    <ul class="check">
      <li><b>[[Purchase contract||Contrato de compra]]</b><span>[[Or the address and your offer price.||O la dirección y su precio de oferta.]]</span></li>
      <li><b>[[Scope of work with costs||Alcance de obra con costos]]</b><span>[[Line items, not one lump number.||Por partidas, no un solo número.]]</span></li>
      <li><b>[[Your ARV and the comps behind it||Su ARV y los comparables]]</b><span>[[We verify it free.||Lo verificamos gratis.]]</span></li>
      <li><b>[[Entity documents and insurance||Documentos de la entidad y seguro]]</b><span>[[Articles, operating agreement, EIN, builder's risk or hazard policy.||Acta constitutiva, acuerdo operativo, EIN, póliza de riesgo de obra.]]</span></li>
      <li><b>[[Your exit||Su salida]]</b><span>[[Sell or refinance, and roughly when.||Venta o refinanciamiento, y más o menos cuándo.]]</span></li>
    </ul>
    <p class="muted" style="margin-top:22px">[[No W-2s. No tax returns. Investment property only.||Sin W-2. Sin declaraciones de impuestos. Solo propiedades de inversión.]]</p>
  </div>
  %(form)s
</div></section>

<section class="paper"><div class="wrap"><div class="shead"><span class="eyebrow">[[Questions||Preguntas]]</span><h2>[[Fix and flip loan questions||Preguntas sobre préstamos fix &amp; flip]]</h2></div>%(faq)s</div></section>
%(band)s""" % dict(form=form, faq=fq, band=band())


DSCR_CALC = """
<div class="calc" id="dscr">
  <div class="in">
    <h3>[[DSCR check||Revisión DSCR]]</h3>
    <div class="note">[[The rates in the table are examples for the math, not a quote.||Las tasas de la tabla son ejemplos para el cálculo, no una cotización.]]</div>
    <label for="dr-loan">[[Loan amount ($)||Monto del préstamo ($)]]<input id="dr-loan" inputmode="numeric" value="160000"></label>
    <label for="dr-rent">[[Monthly rent ($)||Renta mensual ($)]]<input id="dr-rent" inputmode="numeric" value="1750"></label>
    <label for="dr-ti">[[Taxes + insurance per month ($)||Impuestos + seguro al mes ($)]]<input id="dr-ti" inputmode="numeric" value="290"></label>
    <p class="fine">[[30-year amortization. DSCR = rent ÷ (principal, interest, taxes, insurance).||Amortización a 30 años. DSCR = renta ÷ (capital, interés, impuestos, seguro).]]</p>
  </div>
  <div class="out">
    <div class="tablewrap"><table style="min-width:420px"><thead><tr><th>[[Rate||Tasa]]</th><th>P&amp;I</th><th>PITI</th><th>DSCR</th><th></th></tr></thead><tbody id="dr-body"></tbody></table></div>
  </div>
</div>"""


def p_dscr():
    form = lead_form("DSCR page", "ds", "[[Send a rental||Envíe una renta]]", "DSCR", "[[Get my terms||Obtener mis términos]]", "Investor lending — DSCR")
    fq = faq([
        ("[[What DSCR do I need?||¿Qué DSCR necesito?]]", "[[At 1.0 the rent covers the full payment. Stronger coverage earns better terms. We look at each property on its own numbers.||En 1.0 la renta cubre el pago completo. Una mejor cobertura obtiene mejores términos. Vemos cada propiedad con sus propios números.]]"),
        ("[[Do you verify my personal income?||¿Verifican mis ingresos personales?]]", "[[No. The property's rent qualifies the loan, which is why DSCR works for self-employed and full-time investors.||No. La renta de la propiedad califica el préstamo, por eso DSCR funciona para inversionistas independientes y de tiempo completo.]]"),
        ("[[Can my LLC be the borrower?||¿Mi LLC puede ser el prestatario?]]", "[[Yes. We lend directly to your LLC.||Sí. Prestamos directamente a su LLC.]]"),
        ("[[Is this for purchases or refinances?||¿Es para compras o refinanciamientos?]]", "[[Both. Buy a rental, or refinance a flip you finished and want to keep.||Ambos. Compre una renta, o refinancie un flip que terminó y quiere conservar.]]"),
        ("[[The house is vacant. How do you count rent?||La casa está vacía. ¿Cómo cuentan la renta?]]", "[[With market-rent support for the property in place of a lease.||Con un sustento de renta de mercado para la propiedad en lugar de un contrato.]]"),
    ])
    return subhero("[[DSCR rental loans||Préstamos DSCR para rentas]]", "", "[[DSCR rental loans: the property qualifies, not your W-2||Préstamos DSCR: califica la propiedad, no su W-2]]",
                   "[[Long-term financing for rentals, approved on whether the rent covers the payment. Built for buy-and-hold and BRRRR investors.||Financiamiento a largo plazo para rentas, aprobado según si la renta cubre el pago. Hecho para inversionistas de compra y retención y BRRRR.]]",
                   APPLY_BTN + '<a class="btn ghost" href="#dscr">[[Check my DSCR||Revisar mi DSCR]]</a>') + """
<section><div class="wrap split even">
  <div>
    <span class="eyebrow">[[The one ratio||La única razón]]</span>
    <h2 style="margin:14px 0 18px">[[Rent divided by payment||Renta dividida entre el pago]]</h2>
    <p class="lead">[[DSCR stands for debt service coverage ratio. Divide the monthly rent by the full monthly payment. At or above 1.0 the property pays for itself, and that is what we lend on.||DSCR significa razón de cobertura del servicio de deuda. Divida la renta mensual entre el pago mensual completo. En 1.0 o más la propiedad se paga sola, y sobre eso prestamos.]]</p>
  </div>
  <div class="formula">
    <div class="frac"><span>[[Monthly rent||Renta mensual]]</span><span>[[Principal + interest + taxes + insurance||Capital + interés + impuestos + seguro]]</span></div>
    <div class="eq">$1,750 ÷ $1,390 = <b>1.26</b> · [[example||ejemplo]]</div>
  </div>
</div></section>

<section class="paper"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Try it||Pruébelo]]</span><h2>[[Does your rental cover its payment?||¿Su renta cubre el pago?]]</h2></div>
  %(calc)s
</div></section>

<section><div class="wrap">
  <div class="grid g3">
    <article class="card"><span class="num">[[WHO IT'S FOR||PARA QUIÉN]]</span><h3>[[Portfolio builders||Quien construye portafolio]]</h3><p>[[Buy-and-hold and BRRRR investors, self-employed borrowers and full-time investors whose tax returns do not tell the story.||Inversionistas de compra y retención y BRRRR, independientes e inversionistas de tiempo completo cuyas declaraciones no cuentan la historia.]]</p></article>
    <article class="card feature"><span class="num" style="color:#fff">[[THE PAIRING||LA COMBINACIÓN]]</span><h3>[[Flip loan in, DSCR loan out||Entra con flip, sale con DSCR]]</h3><p>[[Buy and renovate on our short-term capital, then refinance into a DSCR loan and keep the house. One lender for the whole cycle.||Compre y remodele con nuestro capital de corto plazo, luego refinancie a DSCR y conserve la casa. Un solo prestamista para todo el ciclo.]]</p></article>
    <article class="card"><span class="num">[[DOCUMENTS||DOCUMENTOS]]</span><h3>[[A short list||Una lista corta]]</h3><ul><li>[[Lease or market-rent support||Contrato o sustento de renta de mercado]]</li><li>[[Entity documents||Documentos de la entidad]]</li><li>[[Insurance||Seguro]]</li></ul></article>
  </div>
</div></section>

<section class="paper"><div class="wrap split">
  <div><div class="shead"><span class="eyebrow">[[Questions||Preguntas]]</span><h2>[[DSCR loan questions||Preguntas sobre DSCR]]</h2></div>%(faq)s</div>
  %(form)s
</div></section>
%(band)s""" % dict(calc=DSCR_CALC, faq=fq, form=form, band=band())


def p_construction():
    form = lead_form("Construction page", "cn", "[[Fund a build||Financie una obra]]", "[[Draw-funded||Por etapas]]", "[[Get my terms||Obtener mis términos]]", "Investor lending — Construction")
    fq = faq([
        ("[[How is the budget released?||¿Cómo se libera el presupuesto?]]", "[[In stages. Money is released as completed work is verified. The schedule for your project is written into your terms.||Por etapas. El dinero se libera al verificar el trabajo terminado. El calendario de su proyecto queda escrito en sus términos.]]"),
        ("[[Do you fund ground-up construction in every state?||¿Financian obra nueva en todos los estados?]]", "[[New construction depends on the borrower and the state. Send an application with the property and borrower information and we will tell you where it stands.||La obra nueva depende del prestatario y del estado. Envíe una solicitud con los datos de la propiedad y del prestatario y le diremos en qué situación está.]]"),
        ("[[Do you finance the lot?||¿Financian el terreno?]]", "[[We are open to looking at it. Include the lot in your application and we will tell you what we can do.||Estamos abiertos a revisarlo. Incluya el terreno en su solicitud y le diremos qué podemos hacer.]]"),
        ("[[What counts as heavy rehab?||¿Qué es una remodelación mayor?]]", "[[Projects that go past cosmetics: structural work, additions, full mechanical replacement or a gut renovation.||Proyectos que van más allá de lo cosmético: trabajo estructural, ampliaciones, reemplazo completo de instalaciones o una renovación total.]]"),
        ("[[Do I need building experience?||¿Necesito experiencia construyendo?]]", "[[It depends on the borrower and the project. Tell us about your experience and who is building, and we will tell you where the deal stands.||Depende del prestatario y del proyecto. Cuéntenos su experiencia y quién construye, y le diremos en qué situación está el proyecto.]]"),
    ])
    rows = [("[[Foundation||Cimentación]]", 100, "[[Released||Liberado]]", "done"), ("[[Framing + roof||Estructura + techo]]", 100, "[[Released||Liberado]]", "done"),
            ("[[Mechanicals||Instalaciones]]", 70, "[[Inspection booked||Inspección agendada]]", ""), ("[[Drywall + finishes||Tablaroca + acabados]]", 0, "[[Next||Siguiente]]", ""),
            ("[[Final + CO||Final + ocupación]]", 0, "[[Pending||Pendiente]]", "")]
    draws = "".join('<div class="draw"><span>%s</span><span class="bar"><i style="width:%d%%"></i></span><span class="st %s">%s</span></div>' % r for r in [(a, b, d, c) for a, b, c, d in rows])
    return subhero("[[Construction loans||Préstamos de construcción]]", "", "[[Construction and heavy-rehab loans, reviewed deal by deal||Préstamos de construcción y remodelación mayor, revisados caso por caso]]",
                   "[[Heavy rehab and ground-up builds, funded in stages against completed work. Whether we can fund a new build depends on the borrower and the state, so the first step is a short application with the property and borrower information.||Remodelación mayor y obra nueva, fondeadas por etapas contra trabajo terminado. Que podamos financiar una obra nueva depende del prestatario y del estado, así que el primer paso es una solicitud corta con los datos de la propiedad y del prestatario.]]",
                   APPLY_BTN + CALC_BTN) + """
<section class="ink"><div class="wrap split even">
  <div>
    <span class="eyebrow">[[How stage funding works||Cómo funciona el fondeo por etapas]]</span>
    <h2 style="margin:14px 0 18px">[[Money is released as the work is verified||El dinero se libera al verificar el avance]]</h2>
    <p class="lead">[[Construction and rehab budgets are paid out in stages, not all at once. The schedule for your project is set with you and written into your terms. The chart is an illustration, not a fixed schedule.||Los presupuestos de construcción y remodelación se pagan por etapas, no de una sola vez. El calendario de su proyecto se define con usted y queda escrito en sus términos. La gráfica es ilustrativa, no un calendario fijo.]]</p>
  </div>
  <div><p class="mono muted" style="font-size:12px;letter-spacing:.08em;margin-bottom:14px">[[EXAMPLE PROJECT · WEEK 11||PROYECTO DE EJEMPLO · SEMANA 11]]</p><div class="draws">%(draws)s</div></div>
</div></section>

<section><div class="wrap split">
  <div>
    <span class="eyebrow">[[What to send||Qué enviar]]</span>
    <h2 style="margin:14px 0 24px">[[Start with the property and the borrower||Empiece con la propiedad y el prestatario]]</h2>
    <p class="lead" style="margin-bottom:24px">[[The application is all we need to begin. If you have any of these, they help us answer faster.||La solicitud es todo lo que necesitamos para empezar. Si tiene algo de esto, nos ayuda a responder más rápido.]]</p>
    <ul class="check">
      <li><b>[[Plans and permit status||Planos y estado del permiso]]</b><span>[[Drawings, plus where the permit stands.||Planos, y en qué va el permiso.]]</span></li>
      <li><b>[[Line-item budget||Presupuesto por partidas]]</b><span>[[By phase, with contractor bids where you have them.||Por etapa, con cotizaciones de contratistas si las tiene.]]</span></li>
      <li><b>[[Who is building||Quién construye]]</b><span>[[Builder or general contractor, license and recent projects.||Constructor o contratista general, licencia y proyectos recientes.]]</span></li>
      <li><b>[[Lot||Terreno]]</b><span>[[Owned, under contract or part of this loan.||Propio, bajo contrato o parte de este préstamo.]]</span></li>
      <li><b>[[Finished value and exit||Valor terminado y salida]]</b><span>[[Sell on completion or refinance and hold.||Vender al terminar o refinanciar y conservar.]]</span></li>
    </ul>
  </div>
  %(form)s
</div></section>

<section class="paper"><div class="wrap"><div class="shead"><span class="eyebrow">[[Questions||Preguntas]]</span><h2>[[Construction loan questions||Preguntas sobre préstamos de construcción]]</h2></div>%(faq)s</div></section>
%(band)s""" % dict(draws=draws, form=form, faq=fq, band=band())


def p_hard():
    fq = faq([
        ("[[Is hard money a last resort?||¿El dinero privado es un último recurso?]]", "[[No. Experienced investors choose it because speed and certainty win deals. A seller will often take a lower price from a buyer who can close in days.||No. Los inversionistas con experiencia lo eligen porque la rapidez y la certeza ganan negocios. Un vendedor muchas veces acepta un precio menor de quien puede cerrar en días.]]"),
        ("[[Why do you always ask about my exit?||¿Por qué siempre preguntan por mi salida?]]", "[[Because the exit is how the loan gets repaid. If you cannot say whether you will sell or refinance, and roughly when, the deal is not ready to fund.||Porque la salida es como se paga el préstamo. Si no puede decir si va a vender o refinanciar, y más o menos cuándo, el proyecto no está listo para fondearse.]]"),
        ("[[How do you decide the ARV?||¿Cómo determinan el ARV?]]", "[[From recent sales of renovated homes near the property, finished to the standard your scope of work describes.||Con ventas recientes de casas remodeladas cerca de la propiedad, terminadas al nivel que describe su alcance de obra.]]"),
        ("[[What property types do you finance?||¿Qué tipos de propiedad financian?]]", "[[Non-owner-occupied investment property: single-family homes, two-to-four unit buildings and light commercial.||Propiedades de inversión no ocupadas por el dueño: casas unifamiliares, edificios de dos a cuatro unidades y comercial ligero.]]"),
        ("[[Is hard money more expensive than a bank loan?||¿El dinero privado es más caro que un banco?]]", "[[Per month, yes. You are paying for speed, flexibility and a loan on a house a bank would not touch in its current condition. The question is what the deal earns after the cost of capital, which is what our calculator shows.||Por mes, sí. Usted paga por rapidez, flexibilidad y un préstamo sobre una casa que un banco no tocaría en su condición actual. La pregunta es cuánto gana el proyecto después del costo del capital, y eso muestra nuestra calculadora.]]"),
    ])
    return subhero("[[Hard money loans||Préstamos de dinero privado]]", "", "[[Hard money loans, explained by people who use them||Dinero privado (hard money), explicado por quienes lo usan]]",
                   "[[Hard money is a short-term loan secured by real estate and approved on the property and the plan. The name comes from the hard asset behind it. It has nothing to do with being hard to get.||El dinero privado, o hard money, es un préstamo de corto plazo garantizado con bienes raíces y aprobado según la propiedad y el plan. El nombre viene del activo tangible que lo respalda, no de que sea difícil de obtener.]]",
                   APPLY_BTN + CALC_BTN) + """
<section><div class="wrap">
  <div class="grid g4">
    <article class="card"><span class="num">01</span><h3>[[Asset-based||Basado en el activo]]</h3><p>[[The property is the collateral and the main reason for the approval.||La propiedad es la garantía y la razón principal de la aprobación.]]</p></article>
    <article class="card"><span class="num">02</span><h3>[[Short-term||Corto plazo]]</h3><p>[[Months, sized to the project. Not a 30-year mortgage.||Meses, según el proyecto. No es una hipoteca a 30 años.]]</p></article>
    <article class="card"><span class="num">03</span><h3>[[Fast||Rápido]]</h3><p>[[No bank underwriting queue. Clean deals close in days.||Sin fila de evaluación bancaria. Los proyectos limpios cierran en días.]]</p></article>
    <article class="card"><span class="num">04</span><h3>[[Built for investors||Para inversionistas]]</h3><p>[[LLC borrowers, houses that need work, no owner-occupancy rules.||Prestatarios LLC, casas que necesitan obra, sin reglas de ocupación.]]</p></article>
  </div>
</div></section>

<section class="paper"><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Side by side||Lado a lado]]</span><h2>[[Hard money and a bank loan do different jobs||El dinero privado y el banco hacen trabajos distintos]]</h2></div>
  <div class="tablewrap"><table>
    <thead><tr><th></th><th class="us">[[Hard money||Dinero privado]]</th><th>[[Conventional bank loan||Préstamo bancario convencional]]</th></tr></thead>
    <tbody>
      <tr><th>[[Approved on||Se aprueba por]]</th><td>[[The property, the plan and the exit||La propiedad, el plan y la salida]]</td><td>[[Your income, tax returns and debt ratios||Sus ingresos, declaraciones y razones de deuda]]</td></tr>
      <tr><th>[[Timeline||Tiempo]]</th><td>[[Days||Días]]</td><td>[[Often 30 to 60 days||A menudo 30 a 60 días]]</td></tr>
      <tr><th>[[Property condition||Condición de la propiedad]]</th><td>[[Needs work is fine. That is the point.||Que necesite obra está bien. De eso se trata.]]</td><td>[[Usually must be livable||Normalmente debe ser habitable]]</td></tr>
      <tr><th>[[Rehab money||Dinero de obra]]</th><td>[[Included, released in draws||Incluido, por desembolsos]]</td><td>[[Usually not included||Normalmente no incluido]]</td></tr>
      <tr><th>[[Borrower||Prestatario]]</th><td>[[Your LLC||Su LLC]]</td><td>[[Usually you personally||Normalmente usted en lo personal]]</td></tr>
      <tr><th>[[Best for||Ideal para]]</th><td>[[Buying, fixing and getting out or refinancing||Comprar, arreglar y salir o refinanciar]]</td><td>[[Long-term holds on finished property||Retención a largo plazo de propiedad terminada]]</td></tr>
    </tbody></table></div>
</div></section>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Who uses it||Quién lo usa]]</span><h2>[[Five kinds of investors we fund||Cinco tipos de inversionistas que financiamos]]</h2></div>
  <div class="grid g3">
    <article class="card"><h3>[[Fix-and-flippers||Flippers]]</h3><p>[[Buy below value, renovate, sell.||Compran por debajo del valor, remodelan y venden.]]</p><div class="more"><a class="tlink" href="fix-and-flip.html">[[Fix &amp; flip loans||Préstamos fix &amp; flip]] →</a></div></article>
    <article class="card"><h3>[[BRRRR and landlords||BRRRR y arrendadores]]</h3><p>[[Buy, rehab, rent, refinance, repeat.||Comprar, remodelar, rentar, refinanciar, repetir.]]</p><div class="more"><a class="tlink" href="dscr.html">[[DSCR loans||Préstamos DSCR]] →</a></div></article>
    <article class="card"><h3>[[Builders||Constructores]]</h3><p>[[Ground-up and gut renovations.||Obra nueva y renovaciones totales.]]</p><div class="more"><a class="tlink" href="construction.html">[[Construction loans||Préstamos de construcción]] →</a></div></article>
  </div>
</div></section>

<section class="ink" id="transactional"><div class="wrap split even">
  <div>
    <span class="eyebrow">[[For wholesalers||Para mayoristas]]</span>
    <h2 style="margin:14px 0 18px">[[Transactional funding for double closings||Fondeo transaccional para cierres dobles]]</h2>
    <p class="lead">[[When you are buying from a seller and reselling to your end buyer back to back, transactional funding covers the first closing until the second one pays it off.||Cuando usted compra a un vendedor y revende a su comprador final uno tras otro, el fondeo transaccional cubre el primer cierre hasta que el segundo lo liquida.]]</p>
    <p style="margin-top:24px"><a class="btn yellow arrow" href="apply.html">[[Submit a double close||Enviar un cierre doble]]</a></p>
  </div>
  <ul class="check">
    <li><b>[[A to B||A a B]]</b><span>[[We fund your purchase from the seller.||Fondeamos su compra al vendedor.]]</span></li>
    <li><b>[[B to C||B a C]]</b><span>[[Your end buyer closes and our capital is repaid from those proceeds.||Su comprador final cierra y nuestro capital se paga con esos fondos.]]</span></li>
    <li><b>[[Clean and documented||Limpio y documentado]]</b><span>[[Both closings run through the title company.||Ambos cierres pasan por la compañía de títulos.]]</span></li>
    <li><b>[[Acquisition only||Solo adquisición]]</b><span>[[There is no rehab money in this product.||Este producto no incluye dinero de obra.]]</span></li>
  </ul>
</div></section>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Glossary||Glosario]]</span><h2>[[The terms on your term sheet||Los términos de su hoja de términos]]</h2></div>
  <dl class="gloss">
    <div><dt>ARV</dt><dd>[[After-repair value. What the property should be worth once the work is done.||Valor después de reparaciones. Lo que debería valer la propiedad al terminar la obra.]]</dd></div>
    <div><dt>LTV / LTC</dt><dd>[[Loan-to-value and loan-to-cost. The ratios that cap how large the loan can be.||Préstamo a valor y préstamo a costo. Las razones que limitan el tamaño del préstamo.]]</dd></div>
    <div><dt>[[Rehab holdback||Retención de obra]]</dt><dd>[[Renovation money set aside at closing and released as work is completed.||Dinero de remodelación apartado al cierre y liberado conforme se termina el trabajo.]]</dd></div>
    <div><dt>[[Draw||Desembolso]]</dt><dd>[[A release of holdback funds after an inspection confirms the work.||Una liberación de fondos retenidos después de que una inspección confirma el trabajo.]]</dd></div>
    <div><dt>[[Points||Puntos]]</dt><dd>[[A fee stated as a percentage of the loan. One point is one percent.||Una comisión expresada como porcentaje del préstamo. Un punto es uno por ciento.]]</dd></div>
    <div><dt>[[Interest-only||Solo intereses]]</dt><dd>[[You pay interest during the loan and the principal at payoff.||Usted paga intereses durante el préstamo y el capital al liquidar.]]</dd></div>
    <div><dt>[[Exit strategy||Estrategia de salida]]</dt><dd>[[How the loan gets repaid: sale or refinance.||Cómo se paga el préstamo: venta o refinanciamiento.]]</dd></div>
    <div><dt>BPO</dt><dd>[[Broker price opinion. A value estimate that can stand in for a full appraisal.||Opinión de valor de un corredor. Un estimado que puede sustituir un avalúo completo.]]</dd></div>
  </dl>
</div></section>

<section class="paper"><div class="wrap"><div class="shead"><span class="eyebrow">[[Questions||Preguntas]]</span><h2>[[Hard money questions||Preguntas sobre dinero privado]]</h2></div>%(faq)s</div></section>
%(band)s""" % dict(faq=fq, band=band())


def p_calc():
    return subhero("[[Calculators||Calculadoras]]", "", "[[Deal calculators for flips and rentals||Calculadoras para flips y rentas]]",
                   "[[Three quick tools. Put in your own numbers, including the rate and points from any term sheet you are comparing.||Tres herramientas rápidas. Use sus propios números, incluidas la tasa y los puntos de cualquier hoja de términos que esté comparando.]]") + """
<section id="flip"><div class="wrap">
  <div class="shead"><span class="eyebrow">A · [[Flip deal analyzer||Analizador de flip]]</span><h2>[[Is there enough profit in this flip?||¿Hay suficiente ganancia en este flip?]]</h2></div>
  <div class="calc">
    <div class="in">
      <h3>[[Your deal||Su proyecto]]</h3>
      <div class="note">[[The rate, points and down payment below are placeholders, not our pricing. Replace them with the numbers on your term sheet.||La tasa, los puntos y el enganche de abajo son valores de ejemplo, no nuestros precios. Cámbielos por los números de su hoja de términos.]]</div>
      <div class="row">
        <label for="fc-buy">[[Purchase price ($)||Precio de compra ($)]]<input id="fc-buy" inputmode="numeric" value="118000"></label>
        <label for="fc-rehab">[[Rehab budget ($)||Presupuesto de obra ($)]]<input id="fc-rehab" inputmode="numeric" value="46500"></label>
      </div>
      <div class="row">
        <label for="fc-arv">[[After-repair value ($)||Valor después de reparaciones ($)]]<input id="fc-arv" inputmode="numeric" value="242000"></label>
        <label for="fc-mo">[[Months held||Meses de tenencia]]<input id="fc-mo" inputmode="numeric" value="6"></label>
      </div>
      <div class="row">
        <label for="fc-rate">[[Annual rate (%%)||Tasa anual (%%)]]<input id="fc-rate" inputmode="decimal" value="12"></label>
        <label for="fc-pts">[[Points and fees (%% of loan)||Puntos y comisiones (%% del préstamo)]]<input id="fc-pts" inputmode="decimal" value="3"></label>
      </div>
      <div class="row">
        <label for="fc-down">[[Your cash in (%% of total cost)||Su efectivo (%% del costo total)]]<input id="fc-down" inputmode="decimal" value="15"></label>
        <label for="fc-sell">[[Selling costs (%% of ARV)||Costos de venta (%% del ARV)]]<input id="fc-sell" inputmode="decimal" value="7"></label>
      </div>
    </div>
    <div class="out">
      <h3>[[The result||El resultado]]</h3>
      <div class="outgrid">
        <div class="o big" id="fc-netbox"><small>[[Projected profit||Ganancia proyectada]]</small><b id="fc-net">$0</b></div>
        <div class="o"><small>[[Loan amount||Monto del préstamo]]</small><b id="fc-loan">$0</b></div>
        <div class="o"><small>[[Your cash in||Su efectivo]]</small><b id="fc-cash">$0</b></div>
        <div class="o"><small>[[Points and fees||Puntos y comisiones]]</small><b id="fc-fee">$0</b></div>
        <div class="o"><small>[[Interest carry||Intereses]]</small><b id="fc-carry">$0</b></div>
        <div class="o"><small>[[Selling costs||Costos de venta]]</small><b id="fc-sc">$0</b></div>
        <div class="o"><small>[[Return on cash||Retorno sobre efectivo]]</small><b id="fc-roi">0%%</b></div>
      </div>
      <p style="margin-top:18px"><a class="btn wide arrow" href="apply.html">[[Get real terms for this deal||Obtener términos reales para este proyecto]]</a></p>
    </div>
  </div>
</div></section>

<section class="paper" id="offer"><div class="wrap">
  <div class="shead"><span class="eyebrow">B · [[Maximum offer||Oferta máxima]]</span><h2>[[What is the most you should pay?||¿Cuánto es lo máximo que debe pagar?]]</h2>
  <p class="lead">[[A common investor rule of thumb: a share of ARV, minus repairs. Many flippers start at 70 percent and adjust for the market.||Una regla común entre inversionistas: un porcentaje del ARV, menos reparaciones. Muchos flippers empiezan en 70 por ciento y ajustan según el mercado.]]</p></div>
  <div class="calc">
    <div class="in">
      <div class="row">
        <label for="mo-arv">[[After-repair value ($)||Valor después de reparaciones ($)]]<input id="mo-arv" inputmode="numeric" value="242000"></label>
        <label for="mo-rep">[[Repairs ($)||Reparaciones ($)]]<input id="mo-rep" inputmode="numeric" value="46500"></label>
      </div>
      <div class="row">
        <label for="mo-pct">[[Rule (%% of ARV)||Regla (%% del ARV)]]<input id="mo-pct" inputmode="decimal" value="70"></label>
        <label for="mo-fee">[[Wholesale fee, if any ($)||Comisión de mayorista, si hay ($)]]<input id="mo-fee" inputmode="numeric" value="0"></label>
      </div>
    </div>
    <div class="out"><div class="outgrid"><div class="o big"><small>[[Maximum offer||Oferta máxima]]</small><b id="mo-out">$0</b></div></div>
      <p class="mono muted" id="mo-line" style="margin-top:14px;font-size:14px"></p>
      <p class="fine">[[A rule of thumb for screening deals. It is not a loan limit.||Una regla general para filtrar proyectos. No es un límite de préstamo.]]</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">C · DSCR</span><h2>[[Does the rent cover the payment?||¿La renta cubre el pago?]]</h2></div>
  %(calc)s
</div></section>
%(band)s""" % dict(calc=DSCR_CALC, band=band("[[Numbers work? Put the deal in front of us.||¿Los números funcionan? Preséntenos el proyecto.]]"))


def p_about():
    form = lead_form("Referral partner", "rp", "[[Become a referral partner||Sea socio de referidos]]", "[[Partners||Socios]]", "[[Talk to us||Hablemos]]", "Referral partner")
    return subhero("[[About||Nosotros]]", "", "[[Operators first. Lenders because investors needed one.||Primero operadores. Prestamistas porque los inversionistas lo necesitaban.]]",
                   "[[ASAP Lending was founded in Kansas City by Carlos Barragan, an investor and builder who buys, renovates and builds homes in the metro. The company finances the kind of projects its own principals take on.||ASAP Lending fue fundada en Kansas City por Carlos Barragan, inversionista y constructor que compra, remodela y construye casas en el área. La empresa financia el tipo de proyectos que sus propios socios realizan.]]") + """
<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[How we lend||Cómo prestamos]]</span><h2>[[Structure. Transparency. Execution.||Estructura. Transparencia. Ejecución.]]</h2></div>
  <div class="grid g3">
    <article class="card"><span class="num">01</span><h3>[[Structure||Estructura]]</h3><p>[[First-position loans on investment property, documented clearly and closed at a title company with title insurance.||Préstamos en primera posición sobre propiedades de inversión, documentados con claridad y cerrados en compañía de títulos con seguro de título.]]</p></article>
    <article class="card"><span class="num">02</span><h3>[[Transparency||Transparencia]]</h3><p>[[You see your costs in writing before you commit. We tell you who we are and what our role is in your loan.||Usted ve sus costos por escrito antes de comprometerse. Le decimos quiénes somos y cuál es nuestro papel en su préstamo.]]</p></article>
    <article class="card"><span class="num">03</span><h3>[[Execution||Ejecución]]</h3><p>[[We do not promise approvals before underwriting, and we do what the term sheet says once it is issued.||No prometemos aprobaciones antes de evaluar, y cumplimos lo que dice la hoja de términos una vez emitida.]]</p></article>
  </div>
</div></section>

<section class="paper"><div class="wrap split even">
  <div>
    <span class="eyebrow">[[What we finance||Qué financiamos]]</span>
    <h2 style="margin:14px 0 22px">[[Investment property, for business purposes||Propiedades de inversión, con fines comerciales]]</h2>
    <ul class="check">
      <li><b>[[Fix and flip||Fix &amp; flip]]</b><span>[[Purchase plus rehab.||Compra más remodelación.]]</span></li>
      <li><b>[[Rentals||Rentas]]</b><span>[[DSCR loans for purchase or refinance.||Préstamos DSCR para compra o refinanciamiento.]]</span></li>
      <li><b>[[Construction||Construcción]]</b><span>[[Heavy rehab, and ground-up builds depending on borrower and state.||Remodelación mayor, y obra nueva según el prestatario y el estado.]]</span></li>
      <li><b>[[Double closings||Cierres dobles]]</b><span>[[Transactional funding for wholesalers.||Fondeo transaccional para mayoristas.]]</span></li>
    </ul>
  </div>
  <div>
    <span class="eyebrow">[[What we do not finance||Qué no financiamos]]</span>
    <h2 style="margin:14px 0 22px">[[Being clear saves everyone time||Ser claros ahorra tiempo a todos]]</h2>
    <div class="prose">
      <p>[[We do not lend on a home you live in or plan to live in. We do not make personal or consumer loans.||No prestamos sobre una casa donde usted vive o piensa vivir. No hacemos préstamos personales ni de consumo.]]</p>
      <p>[[Every loan is underwritten before it is approved. Nothing on this site is a commitment to lend.||Cada préstamo se evalúa antes de aprobarse. Nada en este sitio es un compromiso de préstamo.]]</p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="shead"><span class="eyebrow">[[Where we lend||Dónde prestamos]]</span><h2>[[Six states, one office||Seis estados, una oficina]]</h2>
  <p class="lead">[[Visit or mail us at %(street)s, %(city)s.||Visítenos o escríbanos a %(street)s, %(city)s.]]</p></div>
  %(states)s
</div></section>

<section class="paper" id="partners"><div class="wrap split">
  <div>
    <span class="eyebrow">[[Referral partners||Socios de referidos]]</span>
    <h2 style="margin:14px 0 18px">[[Know an investor who needs funding?||¿Conoce a un inversionista que necesita capital?]]</h2>
    <p class="lead">[[Real estate agents, wholesalers, contractors and title professionals send us investors who need to close. ASAP Lending runs a referral program for the people who bring us good deals.||Agentes de bienes raíces, mayoristas, contratistas y profesionales de títulos nos envían inversionistas que necesitan cerrar. ASAP Lending tiene un programa de referidos para quienes nos traen buenos proyectos.]]</p>
    <ul class="check" style="margin-top:24px">
      <li><b>[[Your buyer closes||Su comprador cierra]]</b><span>[[A funded investor is a closed transaction for you.||Un inversionista fondeado es una transacción cerrada para usted.]]</span></li>
      <li><b>[[You stay informed||Usted se mantiene informado]]</b><span>[[We tell you where the file stands.||Le decimos en qué va el expediente.]]</span></li>
    </ul>
  </div>
  %(form)s
</div></section>
%(band)s""" % dict(street=STREET, city=CITY, states=STATES_HTML, form=form, band=band())


def p_apply():
    return subhero("[[Apply||Aplicar]]", "", "[[Loan application||Solicitud de préstamo]]",
                   "[[About five minutes. Applying does not pull your credit, and this form does not ask for a Social Security number.||Unos cinco minutos. Aplicar no consulta su crédito, y este formulario no pide número de Seguro Social.]]") + """
<section style="padding-top:8px"><div class="wrap split">
  <div class="fcard">
    <div class="wiz-prog" aria-hidden="true"><div>1 · [[Loan||Préstamo]]</div><div>2 · [[Property||Propiedad]]</div><div>3 · [[You||Usted]]</div><div>4 · [[Review||Revisar]]</div></div>
    <form id="apply-form">
      <fieldset>
        <legend>[[What do you need funded?||¿Qué necesita financiar?]]</legend>
        <div class="choices">
          <label class="choice"><input type="radio" name="loan_type" value="Fix & Flip" data-label="[[Loan type||Tipo de préstamo]]" required checked><span>[[Fix &amp; flip||Fix &amp; flip]]<small>[[Purchase + rehab||Compra + remodelación]]</small></span></label>
          <label class="choice"><input type="radio" name="loan_type" value="DSCR" data-label="[[Loan type||Tipo de préstamo]]"><span>[[DSCR rental||DSCR para renta]]<small>[[Buy or refinance a rental||Compra o refinanciamiento]]</small></span></label>
          <label class="choice"><input type="radio" name="loan_type" value="Construction" data-label="[[Loan type||Tipo de préstamo]]"><span>[[Construction||Construcción]]<small>[[Ground-up or heavy rehab||Obra nueva o remodelación mayor]]</small></span></label>
          <label class="choice"><input type="radio" name="loan_type" value="Transactional" data-label="[[Loan type||Tipo de préstamo]]"><span>[[Transactional||Transaccional]]<small>[[Double close||Cierre doble]]</small></span></label>
        </div>
        <div class="row">
          <label for="ap-state">[[Property state||Estado de la propiedad]]<select id="ap-state" name="state" data-label="[[State||Estado]]" required><option value="">[[Choose||Elija]]</option>%(states)s</select></label>
          <label for="ap-stage">[[Where is the deal?||¿En qué va el proyecto?]]<select id="ap-stage" name="stage" data-label="[[Stage||Etapa]]">
            <option>[[Under contract||Bajo contrato]]</option><option>[[Making an offer||Haciendo oferta]]</option><option>[[I own it already||Ya es mía]]</option><option>[[Still looking||Todavía buscando]]</option></select></label>
        </div>
        <div class="wiz-nav"><span></span><button class="btn arrow" type="button" data-next>[[Continue||Continuar]]</button></div>
      </fieldset>
      <fieldset>
        <legend>[[The property and the numbers||La propiedad y los números]]</legend>
        <label for="ap-addr">[[Property address||Dirección de la propiedad]]<input id="ap-addr" name="address" data-label="[[Address||Dirección]]" autocomplete="off" required></label>
        <div class="row">
          <label for="ap-buy">[[Purchase price ($)||Precio de compra ($)]]<input id="ap-buy" name="purchase_price" data-label="[[Purchase price||Precio de compra]]" inputmode="numeric" required></label>
          <label for="ap-rehab">[[Rehab or build budget ($)||Presupuesto de obra ($)]]<input id="ap-rehab" name="rehab_budget" data-label="[[Rehab budget||Presupuesto de obra]]" inputmode="numeric"></label>
        </div>
        <div class="row">
          <label for="ap-arv">[[After-repair value ($)||Valor después de reparaciones ($)]]<input id="ap-arv" name="arv" data-label="ARV" inputmode="numeric"></label>
          <label for="ap-rent">[[Monthly rent, if a rental ($)||Renta mensual, si es renta ($)]] <input id="ap-rent" name="rent" data-label="[[Monthly rent||Renta mensual]]" inputmode="numeric"></label>
        </div>
        <div class="row">
          <label for="ap-close">[[Target closing date||Fecha de cierre deseada]]<input id="ap-close" name="closing_date" data-label="[[Closing date||Fecha de cierre]]" type="date"></label>
          <label for="ap-exit">[[Exit plan||Plan de salida]]<select id="ap-exit" name="exit" data-label="[[Exit||Salida]]"><option>[[Sell||Vender]]</option><option>[[Refinance and hold||Refinanciar y conservar]]</option><option>[[Not sure yet||Aún no sé]]</option></select></label>
        </div>
        <div class="wiz-nav"><button class="btn ghost" type="button" data-back>[[Back||Atrás]]</button><button class="btn arrow" type="button" data-next>[[Continue||Continuar]]</button></div>
      </fieldset>
      <fieldset>
        <legend>[[You and your company||Usted y su empresa]]</legend>
        <div class="row">
          <label for="ap-name">[[Full name||Nombre completo]]<input id="ap-name" name="name" autocomplete="name" data-label="[[Name||Nombre]]" required></label>
          <label for="ap-phone">[[Cell phone||Celular]]<input id="ap-phone" name="phone" type="tel" autocomplete="tel" data-label="[[Phone||Teléfono]]" required></label>
        </div>
        <label for="ap-email">[[Email||Correo electrónico]]<input id="ap-email" name="email" type="email" autocomplete="email" data-label="Email" required></label>
        <div class="row">
          <label for="ap-ent">[[LLC or entity name||Nombre de la LLC o entidad]] <span class="opt">([[optional||opcional]])</span><input id="ap-ent" name="entity" data-label="[[Entity||Entidad]]" autocomplete="organization"></label>
          <label for="ap-exp">[[Deals completed, last 2 years||Proyectos terminados, últimos 2 años]]<select id="ap-exp" name="experience" data-label="[[Experience||Experiencia]]"><option>[[This is my first||Este es el primero]]</option><option>1–2</option><option>3–5</option><option>6–10</option><option>[[More than 10||Más de 10]]</option></select></label>
        </div>
        <div class="row">
          <label for="ap-cash">[[Cash available for this deal ($)||Efectivo disponible para este proyecto ($)]] <span class="opt">([[optional||opcional]])</span><input id="ap-cash" name="cash_available" data-label="[[Cash available||Efectivo disponible]]" inputmode="numeric"></label>
          <label for="ap-ref">[[Who referred you?||¿Quién lo refirió?]] <span class="opt">([[optional||opcional]])</span><input id="ap-ref" name="referred_by" data-label="[[Referred by||Referido por]]"></label>
        </div>
        <label for="ap-notes">[[Anything else we should know?||¿Algo más que debamos saber?]] <span class="opt">([[optional||opcional]])</span><textarea id="ap-notes" name="notes" data-label="[[Notes||Notas]]" rows="3"></textarea></label>
        <div class="wiz-nav"><button class="btn ghost" type="button" data-back>[[Back||Atrás]]</button><button class="btn arrow" type="button" data-next>[[Review||Revisar]]</button></div>
      </fieldset>
      <fieldset>
        <legend>[[Review and send||Revise y envíe]]</legend>
        <div class="review" id="apply-review">[[Your answers appear here before you send.||Sus respuestas aparecen aquí antes de enviar.]]</div>
        <label class="agree" for="ap-biz"><input id="ap-biz" name="agree" type="checkbox" required><span>[[This financing is for business or investment purposes. I will not live in the property.||Este financiamiento es para fines de negocio o inversión. No voy a vivir en la propiedad.]]</span></label>
        <label class="agree" for="ap-tcpa"><input id="ap-tcpa" name="agree" type="checkbox" required><span>[[ASAP Lending may call or text me at the number above about this request. Message and data rates may apply. Reply STOP to opt out.||ASAP Lending puede llamarme o enviarme textos al número indicado sobre esta solicitud. Pueden aplicar cargos de mensajes y datos. Responda STOP para cancelar.]]</span></label>
        <input class="hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="wiz-nav"><button class="btn ghost" type="button" data-back>[[Back||Atrás]]</button><button class="btn arrow" type="submit">[[Send my application||Enviar mi solicitud]]</button></div>
      </fieldset>
      <div class="fmsg" role="status"></div>
    </form>
  </div>
  <aside>
    <span class="eyebrow">[[What happens next||Qué sigue]]</span>
    <h2 style="margin:14px 0 22px;font-size:30px">[[A person reads it today||Una persona lo lee hoy]]</h2>
    <ul class="check">
      <li><b>[[Same business day||Mismo día hábil]]</b><span>[[A decision-maker reviews complete applications and calls you.||Una persona que decide revisa las solicitudes completas y le llama.]]</span></li>
      <li><b>[[Programs first, then credit if needed||Primero los programas, luego crédito si hace falta]]</b><span>[[We explain which programs fit. Credit is pulled only if that program needs it or you choose it.||Le explicamos qué programas encajan. El crédito se consulta solo si ese programa lo requiere o usted lo elige.]]</span></li>
      <li><b>[[Written terms||Términos por escrito]]</b><span>[[If the deal works, you get a term sheet for it.||Si el proyecto funciona, recibe una hoja de términos.]]</span></li>
      <li><b>[[Then documents||Luego documentos]]</b><span>[[Contract, scope of work, entity documents and insurance.||Contrato, alcance de obra, documentos de la entidad y seguro.]]</span></li>
    </ul>
    <div class="ticket" style="margin-top:30px">
      <div class="th"><span>[[Prefer to talk?||¿Prefiere hablar?]]</span><b>[[Call or text||Llame o texto]]</b></div>
      <dl><div><dt>[[Phone||Teléfono]]</dt><dd><a href="tel:%(pt)s">%(pd)s</a></dd></div><div><dt>Email</dt><dd><a href="mailto:funding@asaplending.com">funding@asaplending.com</a></dd></div><div><dt>[[Office||Oficina]]</dt><dd>%(street)s<br>%(city)s</dd></div></dl>
    </div>
    <p class="fine" style="margin-top:18px">[[Sending an application does not obligate you to anything and is not a commitment to lend.||Enviar una solicitud no lo obliga a nada y no es un compromiso de préstamo.]]</p>
  </aside>
</div></section>""" % dict(states=STATE_OPTS, pt=PHONE_T, pd=PHONE_D, street=STREET, city=CITY)


def p_contact():
    form = lead_form("Contact page", "ct", "[[Send a message||Envíe un mensaje]]", "[[We reply fast||Respondemos rápido]]", "[[Send||Enviar]]")
    maps = "https://www.google.com/maps/search/?api=1&query=7017+Oak+Street+Kansas+City+MO"
    return subhero("[[Contact||Contacto]]", "", "[[Talk to a decision-maker||Hable con quien decide]]",
                   "[[Call, text or send the deal. If you already have a property under contract, the application is the fastest route.||Llame, envíe un texto o mande el proyecto. Si ya tiene una propiedad bajo contrato, la solicitud es el camino más rápido.]]",
                   APPLY_BTN) + """
<section style="padding-top:8px"><div class="wrap split even">
  <div>
    <ul class="contact-list">
      <li><small>[[Call or text||Llame o envíe texto]]</small><a href="tel:%(pt)s">%(pd)s</a></li>
      <li><small>[[Email||Correo electrónico]]</small><a href="mailto:funding@asaplending.com" style="font-size:22px">funding@asaplending.com</a></li>
      <li><small>[[Office||Oficina]]</small><b>%(street)s</b><br><b>%(city)s</b><br><a class="tlink" style="font-size:16px" href="%(maps)s" rel="noopener">[[Open in Google Maps||Abrir en Google Maps]] →</a></li>
      <li><small>[[We lend in||Prestamos en]]</small><b class="mono" style="font-size:20px">MO · KS · FL · TX · AR · NE</b></li>
    </ul>
  </div>
  %(form)s
</div></section>
%(band)s""" % dict(pt=PHONE_T, pd=PHONE_D, street=STREET, city=CITY, maps=maps, form=form, band=band())


def p_privacy():
    return subhero("[[Privacy||Privacidad]]", "", "[[Privacy policy||Política de privacidad]]", "[[What we collect when you contact ASAP Lending and how we use it.||Qué recopilamos cuando usted contacta a ASAP Lending y cómo lo usamos.]]") + """
<section style="padding-top:8px"><div class="wrap"><div class="prose">
  <h2>[[What we collect||Qué recopilamos]]</h2>
  <p>[[When you send a form or an application we collect what you enter: your name, phone number, email, and the details of the property and project you describe.||Cuando usted envía un formulario o una solicitud recopilamos lo que escribe: su nombre, teléfono, correo y los datos de la propiedad y el proyecto que describe.]]</p>
  <h2>[[How we use it||Cómo lo usamos]]</h2>
  <p>[[We use it to review your request, contact you about it and, if you move forward, arrange your financing. We do not sell your personal information.||Lo usamos para revisar su solicitud, contactarlo al respecto y, si usted avanza, gestionar su financiamiento. No vendemos su información personal.]]</p>
  <h2>[[Calls and text messages||Llamadas y mensajes de texto]]</h2>
  <p>[[By sending a form with your phone number you agree that we may call or text you about your request. Message and data rates may apply. Reply STOP to opt out of texts at any time.||Al enviar un formulario con su teléfono usted acepta que le llamemos o enviemos textos sobre su solicitud. Pueden aplicar cargos de mensajes y datos. Responda STOP para dejar de recibir textos en cualquier momento.]]</p>
  <h2>[[Contact||Contacto]]</h2>
  <p>[[Questions or removal requests: email funding@asaplending.com, call or text %(pd)s, or visit %(street)s, %(city)s.||Preguntas o solicitudes de eliminación: escriba a funding@asaplending.com, llame o envíe un texto al %(pd)s, o visite %(street)s, %(city)s.]]</p>
</div></div></section>""" % dict(pd=PHONE_D, street=STREET, city=CITY)


PAGES = [
    ("index", p_index, "[[ASAP Lending | Hard Money Loans for Real Estate Investors||ASAP Lending | Préstamos de Dinero Privado para Inversionistas]]",
     "[[Kansas City hard money lender for fix and flip, DSCR rental and construction loans in MO, KS, FL, TX, AR and NE. Same-day answers on complete submissions.||Préstamos de dinero privado desde Kansas City para fix &amp; flip, rentas DSCR y construcción en MO, KS, FL, TX, AR y NE. Respuesta el mismo día en solicitudes completas.]]"),
    ("fix-and-flip", p_flip, "[[Fix and Flip Loans | ASAP Lending||Préstamos Fix &amp; Flip | ASAP Lending]]",
     "[[Fix and flip loans that cover purchase and rehab, underwritten on the deal and funded in draws. No W-2s or tax returns.||Préstamos fix &amp; flip que cubren compra y remodelación, evaluados sobre el proyecto y fondeados por etapas. Sin W-2 ni declaraciones.]]"),
    ("dscr", p_dscr, "[[DSCR Rental Loans | ASAP Lending||Préstamos DSCR para Rentas | ASAP Lending]]",
     "[[DSCR loans for rental property: qualify on the rent, lend to your LLC, purchase or refinance. Free DSCR calculator.||Préstamos DSCR para propiedades de renta: califique con la renta, a nombre de su LLC, compra o refinanciamiento. Calculadora DSCR gratis.]]"),
    ("construction", p_construction, "[[Construction Loans for Investors | ASAP Lending||Préstamos de Construcción | ASAP Lending]]",
     "[[Heavy rehab and ground-up construction loans funded in stages against completed work. New construction depends on borrower and state.||Préstamos para remodelación mayor y obra nueva fondeados por etapas contra trabajo terminado. La obra nueva depende del prestatario y del estado.]]"),
    ("hard-money-loans", p_hard, "[[Hard Money Loans Explained | ASAP Lending||Qué es el Dinero Privado (Hard Money) | ASAP Lending]]",
     "[[What hard money is, who uses it, how it compares to a bank loan, and how transactional funding works for wholesalers.||Qué es el dinero privado, quién lo usa, cómo se compara con un banco y cómo funciona el fondeo transaccional.]]"),
    ("calculator", p_calc, "[[Flip and DSCR Calculators | ASAP Lending||Calculadoras de Flip y DSCR | ASAP Lending]]",
     "[[Free calculators for real estate investors: flip profit, maximum offer and DSCR.||Calculadoras gratis para inversionistas: ganancia de flip, oferta máxima y DSCR.]]"),
    ("about", p_about, "[[About ASAP Lending | Kansas City||Sobre ASAP Lending | Kansas City]]",
     "[[ASAP Lending is a Kansas City company that finances investment real estate in six states, founded by an investor and builder.||ASAP Lending es una empresa de Kansas City que financia bienes raíces de inversión en seis estados, fundada por un inversionista y constructor.]]"),
    ("contact", p_contact, "[[Contact ASAP Lending||Contacto | ASAP Lending]]",
     "[[Email funding@asaplending.com, call or text (913) 513-2656, or visit 7017 Oak Street, Kansas City, MO.||Escriba a funding@asaplending.com, llame o envíe un texto al (913) 513-2656, o visite 7017 Oak Street, Kansas City, MO.]]"),
    ("apply", p_apply, "[[Apply for a Loan | ASAP Lending||Solicitud de Préstamo | ASAP Lending]]",
     "[[Five-minute online loan application for fix and flip, DSCR, construction and transactional funding. No Social Security number on the form.||Solicitud en línea de cinco minutos para fix &amp; flip, DSCR, construcción y fondeo transaccional. El formulario no pide Seguro Social.]]"),
    ("privacy", p_privacy, "[[Privacy Policy | ASAP Lending||Política de Privacidad | ASAP Lending]]",
     "[[How ASAP Lending collects and uses the information you send.||Cómo ASAP Lending recopila y usa la información que usted envía.]]"),
]

ORG = {"@context": "https://schema.org", "@type": "FinancialService", "name": "ASAP Lending", "url": BASE,
       "telephone": PHONE_T, "email": EMAIL, "logo": BASE + "assets/icon-512.png",
       "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Kansas City", "addressRegion": "MO", "addressCountry": "US"},
       "areaServed": [s[1] for s in STATES],
       "description": "Business-purpose real estate financing for investors: fix and flip, DSCR rental, construction and transactional funding."}


def render(slug, fn, title, desc):
    global LD
    LD = [ORG]
    A = "assets/" if LANG == "en" else "../assets/"
    body = fn()
    en_url, es_url = BASE + (slug + ".html" if slug != "index" else ""), BASE + "es/" + slug + ".html"
    me = en_url if LANG == "en" else es_url
    ld = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in LD)
    page = """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(me)s">
<link rel="alternate" hreflang="en" href="%(en)s">
<link rel="alternate" hreflang="es" href="%(es)s">
<link rel="alternate" hreflang="x-default" href="%(en)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ASAP Lending">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(me)s">
<meta property="og:image" content="%(base)sassets/og.png">
<meta name="theme-color" content="#0B0B0C">
<link rel="icon" href="%(A)sfavicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@500;600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(A)ssite.css">
%(ld)s
</head>
<body>
%(header)s
<main>%(body)s</main>
%(footer)s
<script src="%(A)ssite.js"></script>
</body>
</html>
""" % dict(lang=LANG, title=title, desc=desc, me=me, en=en_url, es=es_url, base=BASE, A=A, ld=ld,
           header=header(slug), body=body, footer=footer())
    out = tr(page).replace("@@A@@", A)
    if not SHOW_EMAIL:
        out = re.sub(r'\s*<li><a href="mailto:[^"]*">[^<]*</a></li>', '', out)
        out = re.sub(r'\s*<li><small>(?:Email|Correo electrónico)</small><a href="mailto:[^<]*</a></li>', '', out)
        out = re.sub(r'<div><dt>Email</dt><dd><a href="mailto:[^<]*</a></dd></div>', '', out)
        out = out.replace("email %s, call or text" % EMAIL, "call or text").replace("escriba a %s, llame" % EMAIL, "llame")
        out = out.replace("Email %s, call or text" % EMAIL, "Call or text").replace("Escriba a %s, llame" % EMAIL, "Llame")
        out = out.replace('"email": "%s", ' % EMAIL, "")
        assert EMAIL not in out, slug
    return out


def main():
    global LANG
    urls = []
    for LANG in ("en", "es"):
        d = OUT if LANG == "en" else os.path.join(OUT, "es")
        os.makedirs(d, exist_ok=True)
        for slug, fn, title, desc in PAGES:
            with open(os.path.join(d, slug + ".html"), "w", encoding="utf-8") as f:
                f.write(render(slug, fn, title, desc))
            urls.append((slug, LANG))
    LANG = "en"
    nf = render("404", lambda: subhero("404", "", "[[That page is not here||Esa página no está aquí]]", "[[The link may be old. Start from the homepage or go straight to the application.||El enlace puede ser viejo. Empiece en el inicio o vaya directo a la solicitud.]]", '<a class="btn arrow" href="index.html">[[Home||Inicio]]</a>'), "Page not found | ASAP Lending", "Page not found.")
    nf = nf.replace('href="assets/', 'href="%sassets/' % BASE).replace('src="assets/', 'src="%sassets/' % BASE)
    nf = re.sub(r'href="((?!https?:|tel:|#)[^"]+\.html[^"]*)"', lambda m: 'href="%s%s"' % (BASE, m.group(1)), nf)
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(nf)

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug, lg in urls:
        en, es = BASE + (slug + ".html" if slug != "index" else ""), BASE + "es/" + slug + ".html"
        sm.append('<url><loc>%s</loc><xhtml:link rel="alternate" hreflang="en" href="%s"/><xhtml:link rel="alternate" hreflang="es" href="%s"/></url>' % (en if lg == "en" else es, en, es))
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % BASE)
    print("built", len(urls) + 1, "pages")


main()

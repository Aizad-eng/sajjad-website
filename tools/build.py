#!/usr/bin/env python3
"""Build the SurgiSource static site.

Usage: python3 tools/build.py
Reads category content below and guides from content/guides/*.json, writes the site to the repo root:
index.html, <category>/index.html, guides/index.html, guides/<slug>/index.html, quote/, about/,
404.html, sitemap.xml, robots.txt, llms.txt. Change SITE when a custom domain is attached.
"""
import os, re, json, glob, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://surgisource.dxuxama.workers.dev"
NAME = "SurgiSource"
TALLY = "zEjKDE"
TODAY = datetime.date.today()
e = html.escape

# ---------------------------------------------------------------- categories
# Each item: (name, what it is, what to tell us when you ask for a price)
CATS = [
 {"slug": "surgical-disposables", "name": "Surgical disposables",
  "h1": "Surgical disposables in Pakistan",
  "seo": "Surgical Disposables in Pakistan: Gloves, Masks, Syringes",
  "desc": "Gloves, masks, gowns, syringes, IV cannulas, catheters and other surgical disposables, imported on order and supplied across Pakistan.",
  "intro": "Single-use items for clinics, operation theatres, wards and labs. Tell us the item, size and quantity, and we price it in rupees and source it on order.",
  "items": [
   ("Examination gloves", "Non-sterile gloves for routine examinations, in nitrile, latex or vinyl, usually sold in boxes of 100.", "Material, powder-free or powdered, size (XS to XL) and number of boxes."),
   ("Surgical gloves", "Sterile gloves packed in pairs for surgery and sterile procedures, sized by hand size.", "Latex or latex-free, size (for example 6.5, 7, 7.5, 8) and number of pairs or boxes."),
   ("Face masks and respirators", "Medical face masks for clinical use, and respirators such as N95, KN95 and FFP2 for airborne protection.", "Mask type or standard (for example Type IIR, N95), ear-loop or tie-on, and quantity."),
   ("Gowns, drapes and caps", "Disposable isolation gowns, sterile surgical gowns, surgical drapes, bouffant caps and shoe covers.", "Sterile or non-sterile, size, fabric weight if you know it, and quantity."),
   ("Syringes and needles", "Disposable syringes from 1 ml to 50 ml, insulin syringes and hypodermic needles in standard gauges.", "Syringe volume, needle gauge and length, Luer lock or Luer slip, and quantity."),
   ("IV cannulas and giving sets", "Peripheral IV cannulas in colour-coded gauges, infusion giving sets and extension lines.", "Gauge (for example 18G, 20G, 22G), with or without injection port, and quantity."),
   ("Catheters and urine bags", "Foley catheters, suction catheters, feeding tubes and urine drainage bags.", "Type, size in French (Fr), balloon size for Foley catheters, and quantity."),
   ("Gauze, swabs and dressings", "Gauze swabs, gauze rolls, cotton, crepe bandages, adhesive dressings and tapes.", "Sterile or non-sterile, size, ply and quantity."),
   ("Specimen and blood collection", "Urine and stool containers, sample tubes, blood collection tubes and needles, and swabs.", "Container or tube type, volume, additive (for blood tubes) and quantity."),
  ],
  "faqs": [
   ("Can I order surgical disposables in small quantities?", "Yes. Tell us the quantity you need, whether that is one box or a larger order for a clinic, and we price that quantity."),
   ("Do I need to know the exact standard or size?", "It helps, but it is not required. Describe what you use now, or send a photo of the box, and we will match the item."),
   ("Are surgical disposables regulated in Pakistan?", "Many are medical devices under DRAP's Medical Devices Rules 2017. Ask about a specific item and we will tell you what documentation the supplier provides. See our DRAP guide for the basics."),
   ("Do you deliver outside Islamabad?", "Yes. Items are imported on order and supplied across Pakistan. Tell us your city when you request a quote."),
  ]},
 {"slug": "audiology-equipment", "name": "Audiology equipment",
  "h1": "Audiology equipment in Pakistan",
  "seo": "Audiology Equipment in Pakistan: Audiometers, Headphones",
  "desc": "Audiometers, TDH39, DD45 and DD65 audiometric headphones, B71 and B81 bone conductors and audiology accessories, imported on order across Pakistan.",
  "intro": "Audiology equipment is hard to find in Pakistan, and replacement transducers are harder still. We have sourced an audiometric headset as a single piece from a verified supplier and delivered it in Pakistan, and we can source other audiology items on order.",
  "items": [
   ("Audiometers", "Screening and diagnostic audiometers for clinics, ENT practices and hearing centres.", "Screening or diagnostic, the tests you need (air, bone, speech) and any brand or model you prefer."),
   ("Audiometric headphones", "Supra-aural headphones used with audiometers, such as the TDH39, DD45 and DD65 types.", "The headphone model your audiometer uses, and your audiometer's make and model."),
   ("Bone conductors", "Bone conduction transducers such as the B71 and B81 types, with headbands.", "The model your audiometer supports and whether you need a headband or cable."),
   ("Insert earphones", "Insert earphones with foam ear tips for audiometry.", "Your audiometer model and the ear tip sizes you need."),
   ("Tympanometers and OAE screeners", "Middle-ear analysers and otoacoustic emission screeners used in hearing assessment.", "The tests you need and whether the unit is for screening or diagnostic use."),
   ("Accessories and spares", "Patient response buttons, headbands, cables, ear tips and probe tips.", "The part name or number, and the equipment it is for."),
  ],
  "faqs": [
   ("Can you find a replacement headphone for my audiometer?", "Usually. Send us your audiometer's make and model and the headphone type it uses, such as TDH39 or DD45, and we will source a compatible one."),
   ("Will a new headphone need calibration?", "Audiometer transducers are calibrated together with the audiometer, so plan for calibration after a replacement. We source the equipment but do not provide calibration."),
   ("Do you sell single units?", "Yes. One of our orders was a single audiometric headset, sourced from a verified supplier and delivered in Pakistan."),
   ("Can you source a complete audiometer?", "Yes. Tell us whether you need a screening or diagnostic audiometer and the tests you run, and we will come back with options and a price in rupees."),
  ]},
 {"slug": "diagnostic-equipment", "name": "Diagnostic equipment",
  "h1": "Diagnostic equipment in Pakistan",
  "seo": "Diagnostic Equipment in Pakistan: BP Monitors, Oximeters",
  "desc": "Blood pressure monitors, pulse oximeters, stethoscopes, thermometers, otoscopes, ECG machines and glucometers, imported on order across Pakistan.",
  "intro": "Everyday diagnostic devices for clinics, pharmacies and home use. Tell us the model or the features you need and we price it in rupees.",
  "items": [
   ("Blood pressure monitors", "Digital upper-arm and wrist monitors, and aneroid sphygmomanometers with cuffs.", "Digital or aneroid, cuff size, and whether you need a clinically validated model."),
   ("Pulse oximeters", "Fingertip and handheld pulse oximeters, with adult and paediatric probes.", "Fingertip or handheld, adult or paediatric, and any brand or model you prefer."),
   ("Stethoscopes", "Single and dual-head stethoscopes for adult and paediatric use.", "Type, adult or paediatric, and any model you prefer."),
   ("Thermometers", "Digital and infrared thermometers for clinical and home use.", "Contact or non-contact, and quantity."),
   ("Otoscopes and ophthalmoscopes", "Pocket and wall-mounted diagnostic sets, specula and spare bulbs.", "Pocket or full size, light type, and any spares you need."),
   ("ECG machines and electrodes", "Single and multi-channel ECG machines, disposable electrodes and ECG paper.", "Number of channels, paper size, and electrode type."),
   ("Glucometers and test strips", "Blood glucose meters with matching test strips and lancets.", "The meter model, so the strips match, and quantity."),
  ],
  "faqs": [
   ("What is a validated blood pressure monitor?", "One that has passed a clinical accuracy test against a recognised protocol. Our guide explains how to check a model before you buy."),
   ("Can I order one device for home use?", "Yes. We supply clinics, hospitals, labs and individuals, and you can order a single device."),
   ("Do test strips have to match the meter?", "Yes. Glucometer strips are made for specific meters, so tell us your meter model when you ask for strips."),
  ]},
 {"slug": "hospital-equipment", "name": "Hospital equipment",
  "h1": "Hospital and ward equipment in Pakistan",
  "seo": "Hospital Equipment in Pakistan: Monitors, Suction, Pumps",
  "desc": "Patient monitors, suction machines, nebulisers, infusion and syringe pumps, mobility aids and ward equipment, imported on order across Pakistan.",
  "intro": "Equipment for wards, emergency rooms and clinics. Larger items are priced with freight in mind, so tell us the size and quantity early.",
  "items": [
   ("Patient monitors", "Bedside monitors for parameters such as ECG, SpO2, blood pressure and temperature.", "The parameters you need, screen size, and accessories such as cuffs and probes."),
   ("Suction machines", "Portable and ward suction units for airway and surgical suction.", "Portable or ward use, flow rate needs, and spare jars or tubing."),
   ("Nebulisers", "Compressor and mesh nebulisers with adult and child masks.", "Compressor or mesh, and the masks and kits you need."),
   ("Infusion and syringe pumps", "Volumetric infusion pumps and syringe pumps for controlled drug delivery.", "Pump type, compatible syringe sizes or sets, and quantity."),
   ("Mobility aids", "Wheelchairs, walkers, crutches and commode chairs.", "Type, size, folding or fixed, and weight capacity."),
   ("Oxygen accessories", "Flow meters, humidifier bottles, nasal cannulas and oxygen masks.", "Connector type, adult or paediatric, and quantity."),
  ],
  "faqs": [
   ("Can you supply large items like beds or couches?", "We can price them, but freight from China is charged by size and weight, so large items cost more to bring in. Tell us the item and your city and we will give you the full price."),
   ("Do you provide installation or servicing?", "No. We source and supply the equipment. Plan installation, servicing and maintenance with a local biomedical engineer."),
   ("Can I order spare parts and accessories?", "Yes. Send the part name or number and the equipment it is for."),
  ]},
 {"slug": "laboratory-equipment", "name": "Laboratory equipment",
  "h1": "Laboratory equipment in Pakistan",
  "seo": "Laboratory Equipment in Pakistan: Microscopes, Centrifuges",
  "desc": "Microscopes, centrifuges, micropipettes, tips, test tubes, slides and lab glassware for clinical and teaching labs, imported on order across Pakistan.",
  "intro": "Equipment and consumables for clinical, research and teaching laboratories. Send us the specification you need and we price it in rupees.",
  "items": [
   ("Microscopes", "Biological microscopes for clinical and teaching labs, with objectives and accessories.", "Monocular, binocular or trinocular, objectives needed, and light source."),
   ("Centrifuges", "Benchtop centrifuges for blood and sample tubes, and microcentrifuges.", "Tube sizes and number, maximum speed, and quantity."),
   ("Micropipettes and tips", "Fixed and adjustable volume micropipettes with matching tips.", "Volume range, single or multichannel, and tip type."),
   ("Tubes, slides and plasticware", "Test tubes, centrifuge tubes, microscope slides, cover slips and Petri dishes.", "Type, size, material and quantity."),
   ("Lab glassware", "Beakers, flasks, measuring cylinders and bottles.", "Item, volume, glass type and quantity."),
   ("Incubators and water baths", "Incubators, water baths and dry bath heaters for sample work.", "Capacity, temperature range and power supply (220V)."),
  ],
  "faqs": [
   ("Do you supply teaching labs and colleges?", "Yes. We supply clinics, hospitals, labs and individuals. Send the list of items and quantities you need."),
   ("Will the equipment work on Pakistan's power supply?", "Pakistan uses 220 to 240V at 50Hz. Tell us when you request a quote and we will source a 220V version."),
   ("Can I order consumables only?", "Yes. Tips, tubes, slides and other consumables can be ordered on their own."),
  ]},
]

# ---------------------------------------------------------------- page shell
CSS = """
:root{--ink:#14211f;--ink-2:#3a4745;--ink-3:#66716f;--bg:#f7f6f2;--paper:#fff;--line:#e2dfd6;--teal:#0e6b63;--teal-dark:#0a4f49;--teal-soft:#e4f1ef;--warm:#fbf4e4;--warm-line:#efdcae}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 "Source Sans 3",system-ui,-apple-system,sans-serif}
h1,h2,h3{font-family:"Fraunces",Georgia,serif;font-weight:600;line-height:1.15;letter-spacing:-.01em;margin:0}
a{color:var(--teal)}img{max-width:100%;display:block}
.wrap{width:min(1080px,100% - 32px);margin-inline:auto}
header{background:var(--paper);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:68px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font:600 21px "Fraunces",Georgia,serif}
.brand svg{width:30px;height:30px;flex:none}
.links{display:flex;gap:22px;font-size:15.5px}.links a{color:var(--ink-2);text-decoration:none}.links a:hover{color:var(--teal)}
.btn{display:inline-block;background:var(--teal);color:#fff;text-decoration:none;font-weight:600;padding:11px 20px;border-radius:10px;font-size:16px;white-space:nowrap}
.btn:hover{background:var(--teal-dark)}
.btn.ghost{background:transparent;color:var(--teal);border:1.5px solid var(--teal)}
.crumbs{font-size:14px;color:var(--ink-3);padding-top:22px}.crumbs a{color:var(--ink-3)}
.hero{padding:34px 0 18px;max-width:760px}
.hero h1{font-size:clamp(32px,5vw,50px)}
.lead{font-size:19px;color:var(--ink-2);margin:14px 0 0}
.meta{font-size:14.5px;color:var(--ink-3);margin-top:12px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
section{padding:34px 0;border-top:1px solid var(--line)}
section h2{font-size:clamp(24px,3.2vw,31px);margin-bottom:10px}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.cols h3{font-size:19px;margin-bottom:6px}.cols p{margin:0;color:var(--ink-2)}
.num{font:600 15px "Source Sans 3",sans-serif;color:var(--teal);display:block;margin-bottom:4px}
.catlist{list-style:none;padding:0;margin:0;columns:2;column-gap:40px}
.catlist li{break-inside:avoid;padding:14px 0;border-bottom:1px solid var(--line)}
.catlist a{font:600 20px "Fraunces",Georgia,serif;text-decoration:none;color:var(--ink)}.catlist a:hover{color:var(--teal)}
.catlist p{margin:4px 0 0;color:var(--ink-2);font-size:16px}
.items{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px}
.item{padding:18px 0;border-bottom:1px solid var(--line)}
.item h3{font-size:20px;margin-bottom:6px}.item p{margin:0;color:var(--ink-2)}
.item .ask{font-size:15px;color:var(--ink-3);margin-top:8px}.item .ask b{color:var(--ink-2)}
.note{background:var(--warm);border:1px solid var(--warm-line);border-radius:12px;padding:18px 20px;margin:8px 0}
.note p{margin:0}
.story{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:32px;align-items:start}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{cursor:pointer;font-weight:600;font-size:17.5px;list-style:none}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--teal);font-weight:600}.faq details[open] summary::after{content:"\\2212"}
.faq p{margin:8px 0 0;color:var(--ink-2)}
.guides{list-style:none;padding:0;margin:0}
.guides li{padding:16px 0;border-bottom:1px solid var(--line)}
.guides a{font:600 19px "Fraunces",Georgia,serif;color:var(--ink);text-decoration:none}.guides a:hover{color:var(--teal)}
.guides p{margin:4px 0 0;color:var(--ink-2);font-size:16px}.guides small{color:var(--ink-3);font-size:14px}
.article{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:48px;padding-bottom:40px}
.answer{background:var(--teal-soft);border-left:4px solid var(--teal);border-radius:0 12px 12px 0;padding:16px 20px;margin:6px 0 26px}
.answer b{display:block;font-size:14px;color:var(--teal-dark);margin-bottom:2px}.answer p{margin:0}
.prose h2{font-size:26px;margin:34px 0 10px}.prose p,.prose li{color:#24302e}
.prose table{width:100%;border-collapse:collapse;font-size:15.5px;margin:12px 0 22px;display:block;overflow-x:auto}
.prose th,.prose td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.prose th{background:var(--paper);font-weight:600}
aside .box{position:sticky;top:20px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:18px}
aside h3{font-size:18px;margin-bottom:8px}aside p{font-size:15.5px;color:var(--ink-2);margin:0 0 12px}
.formwrap{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:8px 18px;max-width:720px}
footer{background:var(--ink);color:#c9d3d1;padding:36px 0;margin-top:20px;font-size:15px}
footer a{color:#e6efed}footer .row{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
footer .cols4{display:flex;gap:32px;flex-wrap:wrap}footer ul{list-style:none;padding:0;margin:6px 0 0}footer li{margin:4px 0}
footer .small{margin-top:22px;color:#9fb0ad;font-size:13.5px}
@media(max-width:820px){.cols{grid-template-columns:1fr}.catlist{columns:1}.items{grid-template-columns:1fr}.story{grid-template-columns:1fr}.article{grid-template-columns:1fr}aside .box{position:static}.links{display:none}}
"""

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0e6b63"/><path d="M13 7h6v6h6v6h-6v6h-6v-6H7v-6h6z" fill="#fff"/></svg>'

def shell(path, title, desc, body, ld=None, og_type="website"):
    url = SITE + path
    lds = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (ld or []))
    nav = "".join(f'<a href="/{c["slug"]}/">{e(c["name"].split()[0])}</a>' for c in CATS) + '<a href="/guides/">Guides</a>'
    foot_cats = "".join(f'<li><a href="/{c["slug"]}/">{e(c["name"])}</a></li>' for c in CATS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{NAME}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{lds}</head>
<body>
<header><div class="wrap nav"><a class="brand" href="/">{LOGO}{NAME}</a><nav class="links" aria-label="Main">{nav}</nav><a class="btn" href="/quote/">Request a quote</a></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">
<div class="row"><div><a class="brand" href="/" style="color:#fff">{LOGO}{NAME}</a><p style="max-width:360px">Medical equipment and surgical disposables, imported on order and supplied across Pakistan.</p></div>
<div class="cols4"><div><b style="color:#fff">Categories</b><ul>{foot_cats}</ul></div>
<div><b style="color:#fff">Company</b><ul><li><a href="/about/">About</a></li><li><a href="/guides/">Buying guides</a></li><li><a href="/quote/">Request a quote</a></li></ul></div></div></div>
<p class="small">© {TODAY.year} {NAME}. Based in Islamabad. Product names and model numbers belong to their manufacturers and are used only to identify items.</p>
</div></footer>
</body>
</html>
"""

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div>"

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
       "logo": SITE + "/favicon.svg", "areaServed": {"@type": "Country", "name": "Pakistan"},
       "description": "Medical equipment and surgical disposables, imported on order and supplied across Pakistan.",
       "address": {"@type": "PostalAddress", "addressLocality": "Islamabad", "addressCountry": "PK"}}

def write(path, text):
    full = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(text)

def load_guides():
    gs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "guides", "*.json"))):
        g = json.load(open(f)); g.setdefault("updated", TODAY.isoformat()); gs.append(g)
    return gs

def main():
    guides = load_guides()
    open(os.path.join(ROOT, "style.css"), "w").write(CSS.strip() + "\n")
    open(os.path.join(ROOT, "favicon.svg"), "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    urls = []

    # ---- home
    cat_list = "".join(f'<li><a href="/{c["slug"]}/">{e(c["name"])}</a><p>{e(c["desc"].split(", imported")[0])}.</p></li>' for c in CATS)
    g_list = "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a><p>{e(g["description"])}</p></li>' for g in guides[:6])
    home_faqs = [
        ("Do you keep stock?", "No. Items are imported on order. You tell us what you need, we price it in rupees, and once you confirm we source it and deliver it to you."),
        ("Who do you supply?", "Clinics, hospitals, laboratories and individuals across Pakistan. You can order a single item or a larger quantity for a clinic."),
        ("Where are you based?", "Islamabad. We supply customers across Pakistan."),
        ("How do I get a price?", "Fill in the quote form with the item name, model or a link, the quantity and your city. We reply on WhatsApp with a price in rupees."),
        ("Are the products DRAP registered?", "Many medical devices in Pakistan fall under DRAP's Medical Devices Rules 2017. Ask about a specific item and we will tell you what documentation the supplier provides."),
        ("Do you install, calibrate or service equipment?", "No. We source and supply equipment. Arrange installation, calibration and servicing with a local biomedical engineer."),
    ]
    body = f"""<div class="hero">
<h1>Medical equipment and surgical disposables in Pakistan</h1>
<p class="lead">Audiology equipment, diagnostic devices, hospital equipment, lab equipment and surgical disposables. Imported on order and supplied across Pakistan to clinics, hospitals, labs and individuals.</p>
<div class="cta-row"><a class="btn" href="/quote/">Request a quote</a><a class="btn ghost" href="#categories">Browse categories</a></div>
</div>
<section><h2>How ordering works</h2><div class="cols">
<div><span class="num">1</span><h3>Tell us the item</h3><p>Send the product name, model number or a link, the quantity and your city through the quote form.</p></div>
<div><span class="num">2</span><h3>Get a price in rupees</h3><p>We find the item from manufacturers and verified suppliers and reply on WhatsApp with a price.</p></div>
<div><span class="num">3</span><h3>Confirm and receive</h3><p>Once you confirm, we import the item and deliver it to you anywhere in Pakistan.</p></div>
</div></section>
<section id="categories"><h2>What we supply</h2><ul class="catlist">{cat_list}</ul></section>
<section><div class="story"><div><h2>A recent order</h2><p>A customer needed a replacement audiometric headset, the TDH39 and DD45 type used with audiometers. No shop in Pakistan stocked it. We found it from a verified supplier, bought it as a single piece and delivered it in Pakistan.</p><p>Audiology parts, specialist instruments and other items that are hard to find locally are what we are set up for.</p></div>
<div class="note"><p><b>Looking for something specific?</b> Send the model number or a photo of the old part. We will match it and price it.</p><p style="margin-top:12px"><a class="btn" href="/quote/">Request a quote</a></p></div></div></section>
{'<section><h2>Buying guides</h2><ul class="guides">' + g_list + '</ul><p><a href="/guides/">All buying guides</a></p></section>' if guides else ''}
<section><h2>Questions</h2>{faq_html(home_faqs)}</section>"""
    ws = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/"}
    write("/", shell("/", "Medical Equipment & Surgical Disposables in Pakistan | " + NAME,
                     "Audiology, diagnostic, hospital and lab equipment and surgical disposables, imported on order and supplied across Pakistan. Request a quote.",
                     body, [ORG, ws, faq_ld(home_faqs)])); urls.append("/")

    # ---- categories
    for c in CATS:
        rel = [g for g in guides if g.get("category", "").lower().startswith(c["name"].split()[0].lower()[:6])]
        items = "".join(f'<div class="item"><h3>{e(n)}</h3><p>{e(d)}</p><p class="ask"><b>When you ask for a price, tell us:</b> {e(a)}</p></div>' for n, d, a in c["items"])
        others = "".join(f'<li><a href="/{o["slug"]}/">{e(o["name"])}</a></li>' for o in CATS if o is not c)
        rel_html = ('<section><h2>Buying guides</h2><ul class="guides">' + "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a><p>{e(g["description"])}</p></li>' for g in rel) + "</ul></section>") if rel else ""
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › {e(c["name"])}</nav>
<div class="hero"><h1>{e(c["h1"])}</h1><p class="lead">{e(c["intro"])}</p>
<div class="cta-row"><a class="btn" href="/quote/">Request a quote</a></div></div>
<section><h2>Items we source</h2><div class="items">{items}</div>
<p class="meta">Don't see your item? We source most medical equipment and consumables on order. <a href="/quote/">Ask us</a>.</p></section>
{rel_html}
<section><h2>Questions</h2>{faq_html(c["faqs"])}</section>
<section><h2>Other categories</h2><ul>{others}</ul></section>"""
        il = {"@context": "https://schema.org", "@type": "ItemList", "name": c["name"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n} for i, (n, d, a) in enumerate(c["items"])]}
        write(f'/{c["slug"]}/', shell(f'/{c["slug"]}/', c["seo"] + " | " + NAME, c["desc"], body,
              [crumbs_ld([("Home", "/"), (c["name"], f'/{c["slug"]}/')]), il, faq_ld(c["faqs"])]))
        urls.append(f'/{c["slug"]}/')

    # ---- guides
    for g in guides:
        p = f'/guides/{g["slug"]}/'
        body_html = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener">', g["body"])
        upd = datetime.date.fromisoformat(g["updated"])
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/guides/">Guides</a> › {e(g.get("category", ""))}</nav>
<div class="hero"><h1>{e(g["title"])}</h1><p class="meta">Updated {upd.strftime("%B %-d, %Y")} · {g.get("minutes", 8)} min read</p></div>
<div class="article"><article class="prose">
<div class="answer"><b>Quick answer</b><p>{e(g["answer"])}</p></div>
{body_html}
<h2 id="faq">Frequently asked questions</h2>{faq_html(g["faqs"])}
</article>
<aside><div class="box"><h3>Need this item?</h3><p>We source medical equipment and disposables on order and supply them across Pakistan.</p><a class="btn" href="/quote/">Request a quote</a></div></aside></div>"""
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["description"],
               "datePublished": g.get("published", g["updated"]), "dateModified": g["updated"], "mainEntityOfPage": SITE + p,
               "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}}
        write(p, shell(p, g.get("seo_title", g["title"]) + " | " + NAME, g["description"], body,
              [ORG, art, faq_ld(g["faqs"]), crumbs_ld([("Home", "/"), ("Guides", "/guides/"), (g["title"], p)])], "article"))
        urls.append(p)
    gl = "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a><p>{e(g["description"])}</p><small>{e(g.get("category", ""))} · {g.get("minutes", 8)} min read</small></li>' for g in guides)
    write("/guides/", shell("/guides/", "Medical Equipment Buying Guides for Pakistan | " + NAME,
          "Buying guides for medical equipment and surgical disposables in Pakistan: audiology, gloves, masks, BP monitors, DRAP rules and importing.",
          f'<nav class="crumbs"><a href="/">Home</a> › Guides</nav><div class="hero"><h1>Buying guides</h1><p class="lead">What to check before you buy medical equipment and disposables in Pakistan.</p></div><section><ul class="guides">{gl}</ul></section>',
          [crumbs_ld([("Home", "/"), ("Guides", "/guides/")])])); urls.append("/guides/")

    # ---- quote
    qbody = f"""<nav class="crumbs"><a href="/">Home</a> › Request a quote</nav>
<div class="hero"><h1>Request a quote</h1><p class="lead">Tell us what you need. We reply on WhatsApp with a price in rupees, delivered anywhere in Pakistan.</p></div>
<div class="formwrap"><iframe data-tally-src="https://tally.so/embed/{TALLY}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="900" frameborder="0" marginheight="0" marginwidth="0" title="Request a quote"></iframe></div>
<script>(function(){{var s="https://tally.so/widgets/embed.js";function l(){{if(typeof Tally!=="undefined")Tally.loadEmbeds();else document.querySelectorAll("iframe[data-tally-src]:not([src])").forEach(function(f){{f.src=f.dataset.tallySrc}})}}if(typeof Tally!=="undefined")l();else if(!document.querySelector('script[src="'+s+'"]')){{var t=document.createElement("script");t.src=s;t.onload=l;t.onerror=l;document.body.appendChild(t)}}}})();</script>
<section><h2>What helps us price it quickly</h2><ul><li>The product name and model number, or a link to the product.</li><li>The size, variant or specification, if the item comes in more than one.</li><li>The quantity you need.</li><li>Your city, so we can include delivery.</li></ul></section>"""
    write("/quote/", shell("/quote/", "Request a Quote for Medical Equipment | " + NAME,
          "Request a price in rupees for medical equipment or surgical disposables, imported on order and supplied across Pakistan.", qbody,
          [crumbs_ld([("Home", "/"), ("Request a quote", "/quote/")])])); urls.append("/quote/")

    # ---- about
    abody = f"""<nav class="crumbs"><a href="/">Home</a> › About</nav>
<div class="hero"><h1>About {NAME}</h1><p class="lead">{NAME} sources medical equipment and surgical disposables for clinics, hospitals, laboratories and individuals in Pakistan.</p></div>
<section><h2>What we do</h2><p>We find the item you need from manufacturers and verified suppliers, price it in rupees, import it on order and deliver it anywhere in Pakistan. We are based in Islamabad.</p>
<p>One example: a customer needed a replacement audiometric headset that no shop in Pakistan stocked. We found it from a verified supplier, bought it as a single piece and delivered it in Pakistan.</p></section>
<section><h2>What we don't do</h2><ul><li>We don't keep stock. Items are imported on order.</li><li>We don't install, calibrate or service equipment. Arrange that with a local biomedical engineer.</li><li>We don't give medical advice. Our guides are about buying equipment, not about treatment.</li></ul></section>
<section><h2>Contact</h2><p>Every enquiry goes through our <a href="/quote/">quote form</a>. We reply on WhatsApp.</p></section>"""
    write("/about/", shell("/about/", "About " + NAME + " | Medical Equipment Supplier, Islamabad",
          NAME + " sources medical equipment and surgical disposables on order for clinics, hospitals, labs and individuals across Pakistan.", abody,
          [ORG, crumbs_ld([("Home", "/"), ("About", "/about/")])])); urls.append("/about/")

    # ---- 404
    open(os.path.join(ROOT, "404.html"), "w").write(shell("/404", "Page not found | " + NAME, "Page not found.",
         '<div class="hero"><h1>Page not found</h1><p class="lead">The page you are looking for does not exist.</p><div class="cta-row"><a class="btn" href="/">Go to the homepage</a><a class="btn ghost" href="/quote/">Request a quote</a></div></div>'))

    # ---- sitemap, robots, llms
    sm = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for u in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sm + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    L = [f"# {NAME}", "", f"> {NAME} sources medical equipment and surgical disposables for clinics, hospitals, laboratories and individuals in Pakistan. Items are imported on order and supplied across Pakistan. Based in Islamabad. Buyers request a price through the quote form at {SITE}/quote/ and get a reply on WhatsApp with a price in rupees.", "",
         "Key facts:", "- Stock: none kept; everything is imported on order.", "- Buyers: clinics, hospitals, labs and individuals; single items or larger quantities.",
         "- Not offered: installation, calibration, servicing, medical advice.", "", "## Categories"]
    L += [f"- [{c['name']}]({SITE}/{c['slug']}/): {c['desc']}" for c in CATS]
    if guides:
        L += ["", "## Buying guides"] + [f"- [{g['title']}]({SITE}/guides/{g['slug']}/): {g['description']}" for g in guides]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(L) + "\n")
    print(f"built {len(urls)} pages, {len(guides)} guides")

if __name__ == "__main__":
    main()

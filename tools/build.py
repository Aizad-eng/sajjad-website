#!/usr/bin/env python3
"""Build the SurgiSource static site.

Usage: python3 tools/build.py
Reads category content below and guides from content/guides/*.json, writes the site to the repo root:
index.html, <category>/index.html, guides/index.html, guides/<slug>/index.html, quote/, about/,
404.html, sitemap.xml, robots.txt, llms.txt. Change SITE when a custom domain is attached.
"""
import os, re, json, glob, html, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from products import PRODUCTS

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
 {"slug": "surgical-instruments", "name": "Surgical instruments",
  "h1": "Surgical instruments in Pakistan",
  "seo": "Surgical Instruments in Pakistan: Scissors, Forceps, Sets",
  "desc": "Surgical scissors, forceps, needle holders, scalpel handles and blades, retractors and instrument sets, sourced on order and supplied across Pakistan.",
  "intro": "Reusable stainless steel instruments for clinics, operation theatres and dental and veterinary practices. Pakistan's surgical instrument industry is centred in Sialkot, and we source instruments on order from makers in Pakistan or abroad.",
  "items": [
   ("Surgical scissors", "Operating, dissecting (Metzenbaum, Mayo), bandage and suture scissors in straight and curved patterns.", "Pattern, length, straight or curved, and quantity."),
   ("Forceps", "Dissecting and tissue forceps, artery forceps (haemostats) and sponge-holding forceps.", "Type and pattern, length, toothed or non-toothed, and quantity."),
   ("Needle holders", "Mayo-Hegar and other needle holders, with or without tungsten carbide inserts.", "Pattern, length and insert type."),
   ("Scalpel handles and blades", "Reusable scalpel handles and sterile disposable blades in standard numbers.", "Handle number and blade numbers (for example 10, 11, 15, 22), and quantity."),
   ("Retractors and clamps", "Hand-held and self-retaining retractors, towel clips and clamps.", "Type, size and quantity."),
   ("Instrument sets", "Minor surgery, dressing, suturing and delivery sets, in a tray or pouch.", "The procedure the set is for, the instruments you need in it, and quantity."),
  ],
  "faqs": [
   ("Are surgical instruments made in Pakistan?", "Yes. Sialkot is the main centre of Pakistan's surgical instrument industry. Tell us the pattern and quantity and we will source it."),
   ("Can I order a single instrument?", "Yes. You can order one instrument or a full set."),
   ("Do you sterilise instruments?", "No. Reusable instruments must be cleaned and sterilised by your clinic before use, following your infection control procedure."),
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
:root{--ink:#0f2a2c;--ink-2:#3b5254;--ink-3:#6b7f80;--bg:#f6f9f9;--paper:#fff;--line:#e1e9e9;--teal:#0b7a70;--teal-dark:#075c55;--mint:#dff3ef;--mint-2:#c7ebe4;--sand:#f7f1e6;--sky:#e8f1fb;--rose:#fbecec;--shadow:0 1px 2px rgba(15,42,44,.05),0 18px 40px -22px rgba(15,42,44,.28);--r:20px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16.5px/1.65 "Plus Jakarta Sans",system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-weight:800;line-height:1.1;letter-spacing:-.025em;margin:0}
a{color:var(--teal)}img{max-width:100%;display:block}
.wrap{width:min(1160px,100% - 32px);margin-inline:auto}
/* nav */
header{position:sticky;top:12px;z-index:50;padding:0 16px}
.nav{width:min(1160px,100%);margin:12px auto 0;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 10px 10px 18px;background:rgba(255,255,255,.82);backdrop-filter:saturate(170%) blur(14px);-webkit-backdrop-filter:saturate(170%) blur(14px);border:1px solid var(--line);border-radius:18px;box-shadow:0 10px 30px -20px rgba(15,42,44,.35)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:800;font-size:19px;letter-spacing:-.02em}
.brand svg{width:32px;height:32px;flex:none}
.links{display:flex;gap:4px}.links a{color:var(--ink-2);text-decoration:none;font-weight:600;font-size:15px;padding:8px 12px;border-radius:10px}.links a:hover{background:var(--mint);color:var(--teal-dark)}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:12px;font-size:15.5px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit;transition:transform .15s,background .15s}
.btn:hover{background:var(--teal-dark);transform:translateY(-1px)}
.btn.ghost{background:var(--paper);color:var(--ink);border:1px solid var(--line)}.btn.ghost:hover{background:var(--mint)}
/* hero */
.home-hero{position:relative;margin-top:-74px;padding:130px 0 70px;background:radial-gradient(900px 500px at 85% 10%,var(--mint-2),transparent 60%),radial-gradient(700px 420px at 0% 100%,#eaf4ff,transparent 60%),linear-gradient(180deg,#f2faf8,var(--bg));overflow:hidden}
.home-hero::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(11,122,112,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(11,122,112,.06) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 70% 30%,#000 20%,transparent 70%);-webkit-mask-image:radial-gradient(ellipse at 70% 30%,#000 20%,transparent 70%)}
.hero-grid{position:relative;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:56px;align-items:center}
.home-hero h1{font-size:clamp(38px,5.6vw,66px);letter-spacing:-.035em}
.home-hero .lead{font-size:19px;color:var(--ink-2);margin:20px 0 0;max-width:560px}
.search{margin-top:28px;display:flex;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:8px;box-shadow:var(--shadow);max-width:560px}
.search input{flex:1;min-width:0;border:0;outline:0;font:500 16.5px "Plus Jakarta Sans",sans-serif;padding:10px 12px;color:var(--ink);background:transparent}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;align-items:center}
.chips span{font-size:14px;color:var(--ink-3);margin-right:2px}
.chip{display:inline-block;font-size:14px;font-weight:600;color:var(--ink-2);background:rgba(255,255,255,.75);border:1px solid var(--line);border-radius:999px;padding:6px 12px;text-decoration:none}.chip:hover{border-color:var(--teal);color:var(--teal-dark)}
.photos{position:relative;height:520px}
.photos img{position:absolute;border-radius:22px;object-fit:cover;box-shadow:0 30px 60px -28px rgba(15,42,44,.5);border:6px solid #fff}
.photos .p1{width:58%;height:78%;right:0;top:0;transform:rotate(2deg)}
.photos .p2{width:50%;height:62%;left:0;bottom:0;transform:rotate(-3deg)}
.photos .tag{position:absolute;left:8%;top:6%;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px 16px;max-width:250px;box-shadow:var(--shadow);font-size:14px;line-height:1.45;color:var(--ink-2)}
.photos .tag b{display:block;color:var(--ink);font-size:15px;margin-bottom:2px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#1aa37a;box-shadow:0 0 0 4px rgba(26,163,122,.18);margin-right:8px;vertical-align:middle}
/* sections */
.sec{padding:84px 0}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:30px;flex-wrap:wrap}
.sec-head h2,.sec h2{font-size:clamp(28px,3.6vw,42px)}
.sec-head p{margin:10px 0 0;color:var(--ink-2);max-width:560px;font-size:17.5px}
/* bento categories */
.bento{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));grid-auto-rows:minmax(210px,auto);gap:16px}
.tile{position:relative;border-radius:var(--r);padding:26px;text-decoration:none;color:var(--ink);border:1px solid var(--line);background:var(--paper);display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s;overflow:hidden}
.tile:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.tile .ic{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:var(--mint);color:var(--teal-dark);margin-bottom:auto}
.tile .ic svg{width:28px;height:28px}
.tile h3{font-size:22px;margin-top:22px}.tile p{margin:8px 0 0;color:var(--ink-2);font-size:15px}
.tile .go{margin-top:14px;font-weight:700;color:var(--teal);font-size:14.5px}
.t1{grid-column:span 3;grid-row:span 2;background:linear-gradient(160deg,var(--mint),#fff 70%)}.t1 h3{font-size:30px}
.t1 ul{list-style:none;padding:0;margin:16px 0 0;display:flex;flex-wrap:wrap;gap:8px}.t1 li{background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:14px;font-weight:600;color:var(--ink-2)}
.t2{grid-column:span 3;background:var(--sand)}.t2 .ic{background:#fff}
.t3{grid-column:span 3;background:var(--sky)}.t3 .ic{background:#fff;color:#2860a8}
.t4,.t5,.t6{grid-column:span 2}
/* product rail */
.rail{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.pr{display:flex;align-items:center;gap:14px;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px 16px;text-decoration:none;color:var(--ink);font-weight:700;transition:border-color .15s,transform .15s}
.pr:hover{border-color:var(--teal);transform:translateY(-2px)}
.pr .ic{width:42px;height:42px;border-radius:12px;background:var(--mint);display:grid;place-items:center;color:var(--teal-dark);flex:none}.pr .ic svg{width:22px;height:22px}
.pr small{display:block;font-weight:500;color:var(--ink-3);font-size:13px}
/* how */
.how{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center}
.steps{margin:24px 0 0;padding:0;list-style:none;position:relative}
.steps li{position:relative;padding:0 0 26px 56px}
.steps li::before{content:attr(data-n);position:absolute;left:0;top:0;width:38px;height:38px;border-radius:50%;background:var(--teal);color:#fff;font-weight:800;display:grid;place-items:center;font-size:15px}
.steps li::after{content:"";position:absolute;left:18px;top:42px;bottom:4px;width:2px;background:var(--mint-2)}
.steps li:last-child::after{display:none}
.steps b{display:block;font-size:18px;margin-bottom:2px}.steps span{color:var(--ink-2)}
.req{background:var(--paper);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:24px;max-width:460px;margin-left:auto}
.req h3{font-size:18px;margin-bottom:14px}
.req .row{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-top:1px solid var(--line);font-size:15px}.req .row span{color:var(--ink-3)}.req .row b{text-align:right}
.req .wa{margin-top:16px;background:#e7f6ee;border-radius:14px;padding:12px 14px;font-size:14.5px;color:#14532d}
/* who */
.who{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.who div{flex:1 1 200px;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:16px 18px;font-weight:700}.who small{display:block;font-weight:500;color:var(--ink-3);margin-top:2px;font-size:14px}
/* faq two-column */
.qa{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 48px}
.qa h3{font-size:18px;letter-spacing:-.01em}.qa p{margin:8px 0 0;color:var(--ink-2)}
.final{border-radius:28px;padding:48px;background:radial-gradient(600px 300px at 90% 0%,var(--mint-2),transparent 60%),var(--mint);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;align-items:center}
.final h2{font-size:clamp(28px,3.4vw,40px)}.final p{color:var(--ink-2);margin:10px 0 0}
.final .search{margin-top:0;max-width:none}
/* inner pages */
main.inner{padding-top:24px}
.crumbs{font-size:14px;color:var(--ink-3);padding-top:22px}.crumbs a{color:var(--ink-3)}
.hero{padding:26px 0 26px;max-width:800px}
.hero h1{font-size:clamp(32px,4.8vw,52px);letter-spacing:-.03em}
.lead{font-size:18.5px;color:var(--ink-2);margin:14px 0 0}
.meta{font-size:14.5px;color:var(--ink-3);margin-top:12px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
section{padding:36px 0;border-top:1px solid var(--line)}
section h2{font-size:clamp(24px,3vw,32px);margin-bottom:12px}
.items{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.item{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:20px 22px}
.item h3{font-size:19px;margin-bottom:6px}.item p{margin:0;color:var(--ink-2);font-size:15.5px}
.item .ask{font-size:14.5px;color:var(--ink-3);margin-top:10px;padding-top:10px;border-top:1px dashed var(--line)}.item .ask b{color:var(--ink-2)}
.note{background:var(--sand);border:1px solid #eadfc8;border-radius:16px;padding:18px 20px;margin:8px 0}.note p{margin:0}
.faq details{border-bottom:1px solid var(--line);padding:15px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:17px;list-style:none}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--teal);font-weight:800}.faq details[open] summary::after{content:"\\2212"}
.faq p{margin:8px 0 0;color:var(--ink-2)}
.guides{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.guides li{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:16px 18px}
.guides a{font-weight:800;font-size:17px;color:var(--ink);text-decoration:none;letter-spacing:-.01em}.guides a:hover{color:var(--teal)}
.guides p{margin:6px 0 0;color:var(--ink-2);font-size:15px}.guides small{color:var(--ink-3);font-size:13.5px}
.catlist{list-style:none;padding:0;margin:0}
.article{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:48px;padding-bottom:40px}
.answer{background:var(--mint);border:1px solid var(--mint-2);border-radius:16px;padding:18px 20px;margin:6px 0 26px}
.answer b{display:block;font-size:14px;color:var(--teal-dark);margin-bottom:4px}.answer p{margin:0}
.prose{max-width:740px}.prose h2{font-size:26px;margin:38px 0 10px}.prose p,.prose li{color:#23393b}.prose li{margin:6px 0}
.prose table{width:100%;border-collapse:collapse;font-size:15px;margin:14px 0 24px;display:block;overflow-x:auto;background:var(--paper);border-radius:14px;border:1px solid var(--line)}
.prose th,.prose td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}.prose th{background:#f1f6f6;font-weight:700}
aside .box{position:sticky;top:100px;background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:var(--shadow)}
aside h3{font-size:19px;margin-bottom:8px}aside p{font-size:15px;color:var(--ink-2);margin:0 0 14px}
.formwrap{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:8px 20px;max-width:760px;box-shadow:var(--shadow)}
.asked{background:var(--mint);border:1px solid var(--mint-2);border-radius:14px;padding:12px 16px;margin:0 0 16px;max-width:760px}
footer{background:var(--paper);border-top:1px solid var(--line);padding:48px 0 28px;margin-top:40px;font-size:15px;color:var(--ink-2)}
footer a{color:var(--ink-2);text-decoration:none}footer a:hover{color:var(--teal)}
footer .row{display:flex;justify-content:space-between;gap:32px;flex-wrap:wrap}
footer .cols4{display:flex;gap:48px;flex-wrap:wrap}footer b{color:var(--ink)}footer ul{list-style:none;padding:0;margin:8px 0 0}footer li{margin:6px 0}
footer .small{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);color:var(--ink-3);font-size:13.5px}
.reveal{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}}
@media(max-width:960px){.hero-grid,.how,.final{grid-template-columns:1fr}.photos{height:420px;max-width:520px}.req{margin-left:0}.rail{grid-template-columns:repeat(2,minmax(0,1fr))}.bento{grid-template-columns:repeat(2,minmax(0,1fr))}.t1,.t2,.t3,.t4,.t5,.t6{grid-column:span 2;grid-row:auto}.article{grid-template-columns:1fr}aside .box{position:static}}
@media(max-width:1040px){.links a{padding:8px 8px;font-size:14.5px}}
@media(max-width:900px){.links{display:none}}
@media(max-width:720px){.qa,.items,.guides{grid-template-columns:1fr}.rail{grid-template-columns:1fr}.sec{padding:60px 0}.final{padding:28px}.home-hero{padding-top:110px}.photos{height:360px}.photos .tag{left:0;top:auto;bottom:-6px;max-width:220px}.nav .btn{padding:10px 14px;font-size:14.5px}}
"""

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0e6b63"/><path d="M13 7h6v6h6v6h-6v6h-6v-6H7v-6h6z" fill="#fff"/></svg>'

ICON = {
 "surgical-disposables": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 11V5.5a1.5 1.5 0 0 1 3 0V10"/><path d="M10 9.5V4.5a1.5 1.5 0 0 1 3 0V10"/><path d="M13 9.5V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M16 9.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1.5a6 6 0 0 1-4.6-2.2L4 15.2a1.6 1.6 0 0 1 2.4-2.1L7 14"/></svg>',
 "surgical-instruments": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/></svg>',
 "audiology-equipment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14v-2a9 9 0 0 1 18 0v2"/><rect x="2.5" y="13" width="5" height="8" rx="2"/><rect x="16.5" y="13" width="5" height="8" rx="2"/></svg>',
 "diagnostic-equipment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3v6a5 5 0 0 0 10 0V3"/><path d="M10 14v2a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="12" r="2"/><path d="M4 3h2M14 3h2"/></svg>',
 "hospital-equipment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6v14M3 14h18v6M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/></svg>',
 "laboratory-equipment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5.5 9.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7.5 15h9"/></svg>',
}

def shell(path, title, desc, body, ld=None, og_type="website", full=False):
    url = SITE + path
    lds = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (ld or []))
    nav = '<a href="/products/">Products</a><a href="/surgical-disposables/">Disposables</a><a href="/surgical-instruments/">Instruments</a><a href="/audiology-equipment/">Audiology</a><a href="/guides/">Guides</a>'
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
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{lds}</head>
<body>
<header><div class="nav"><a class="brand" href="/">{LOGO}{NAME}</a><nav class="links" aria-label="Main">{nav}</nav><a class="btn" href="/quote/">Get a price</a></div></header>
<main{'' if full else ' class="wrap inner"'}>
{body}
</main>
<footer><div class="wrap">
<div class="row"><div><a class="brand" href="/">{LOGO}{NAME}</a><p style="max-width:360px">Medical equipment and surgical disposables, imported on order and supplied across Pakistan.</p></div>
<div class="cols4"><div><b>Categories</b><ul>{foot_cats}</ul></div>
<div><b>Popular</b><ul><li><a href="/products/nebulizer/">Nebulizer</a></li><li><a href="/products/bp-apparatus/">BP apparatus</a></li><li><a href="/products/glucometer/">Glucometer</a></li><li><a href="/products/pulse-oximeter/">Pulse oximeter</a></li><li><a href="/products/">All products</a></li></ul></div>
<div><b>Company</b><ul><li><a href="/about/">About</a></li><li><a href="/guides/">Buying guides</a></li><li><a href="/quote/">Request a quote</a></li></ul></div></div></div>
<p class="small">© {TODAY.year} {NAME}. Based in Islamabad. Product names and model numbers belong to their manufacturers and are used only to identify items.</p>
</div></footer>
<script src="/site.js" defer></script>
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
    cls = {"surgical-disposables": "t1", "audiology-equipment": "t2", "diagnostic-equipment": "t3", "surgical-instruments": "t4", "hospital-equipment": "t5", "laboratory-equipment": "t6"}
    order = ["surgical-disposables", "audiology-equipment", "diagnostic-equipment", "surgical-instruments", "hospital-equipment", "laboratory-equipment"]
    cmap = {c["slug"]: c for c in CATS}
    tiles = ""
    for sl in order:
        c = cmap[sl]; short = re.split(r", (?:imported|sourced) on order", c["desc"])[0]
        extra = ('<ul>' + "".join(f"<li>{e(n)}</li>" for n, d, a in c["items"]) + '</ul>') if sl == "surgical-disposables" else ""
        tiles += f'<a class="tile {cls[sl]} reveal" href="/{sl}/"><span class="ic">{ICON[sl]}</span><h3>{e(c["name"])}</h3><p>{e(short)}.</p>{extra}<span class="go">See items →</span></a>'
    rail = "".join(f'<a class="pr reveal" href="/products/{pr["slug"]}/"><span class="ic">{ICON[pr["cat"]]}</span><span>{e(pr["name"])}<small>Price in Pakistan</small></span></a>' for pr in PRODUCTS[:12])
    chips = "".join(f'<a class="chip" href="/products/{x}/">{e(n)}</a>' for x, n in [("nebulizer", "Nebulizer"), ("bp-apparatus", "BP apparatus"), ("glucometer", "Glucometer"), ("pulse-oximeter", "Pulse oximeter"), ("audiometer", "Audiometer"), ("iv-cannula", "IV cannula")])
    g_list = "".join(f'<li class="reveal"><a href="/guides/{g["slug"]}/">{e(g["title"])}</a><p>{e(g["description"])}</p></li>' for g in guides[:6])
    home_faqs = [
        ("Do you keep stock?", "No. Items are imported on order. You tell us what you need, we price it in rupees, and once you confirm we source it and deliver it to you."),
        ("Who do you supply?", "Clinics, hospitals, laboratories and individuals across Pakistan. You can order a single item or a larger quantity for a clinic."),
        ("Where are you based?", "Islamabad. We supply customers across Pakistan."),
        ("How do I get a price?", "Fill in the quote form with the item name, model or a link, the quantity and your city. We reply on WhatsApp with a price in rupees."),
        ("Are the products DRAP registered?", "Many medical devices in Pakistan fall under DRAP's Medical Devices Rules 2017. Ask about a specific item and we will tell you what documentation the supplier provides."),
        ("Do you install, calibrate or service equipment?", "No. We source and supply equipment. Arrange installation, calibration and servicing with a local biomedical engineer."),
    ]
    qa = "".join(f"<div class=\"reveal\"><h3>{e(q)}</h3><p>{e(a)}</p></div>" for q, a in home_faqs)
    search = '<form class="search" action="/quote/" method="get" data-search><input name="item" placeholder="What do you need? e.g. TDH39 headphones, nitrile gloves" aria-label="What do you need?" autocomplete="off"><button class="btn" type="submit">Get a price</button></form>'
    body = f"""<section class="home-hero"><div class="wrap hero-grid">
<div>
<h1>Medical equipment and surgical supplies, sourced for you</h1>
<p class="lead">Tell us the item. We find it, price it in rupees and deliver it anywhere in Pakistan. For clinics, hospitals, labs and home use.</p>
{search}
<div class="chips"><span>Popular:</span>{chips}</div>
</div>
<div class="photos">
<img class="p1" src="/assets/order-headset-hand.jpg" alt="Audiometric headset from one of our orders" width="480" height="640" fetchpriority="high">
<img class="p2" src="/assets/order-headset-box.jpg" alt="The audiometric headset in its shipping box" width="480" height="640" loading="lazy">
<div class="tag"><b><span class="dot"></span>A recent order</b>An audiometric headset of the TDH39 and DD45 type. No shop in Pakistan stocked it, so we sourced one and delivered it.</div>
</div>
</div></section>
<div class="wrap">
<section class="sec" id="categories" style="border:0"><div class="sec-head"><div><h2>What we supply</h2><p>Six areas, from everyday disposables to specialist audiology equipment. If it is a medical item, ask us.</p></div><a class="btn ghost" href="/quote/">Ask for something else</a></div>
<div class="bento">{tiles}</div></section>
<section class="sec"><div class="sec-head"><div><h2>Prices people search for</h2><p>Each page explains the types, what changes the price and what to check. Ask for today's price in rupees.</p></div><a class="btn ghost" href="/products/">All products</a></div>
<div class="rail">{rail}</div></section>
<section class="sec"><div class="how">
<div class="reveal"><h2>How ordering works</h2><p class="lead" style="font-size:17.5px">There is nothing to sign up for. You send a request, we come back with a price.</p>
<ol class="steps"><li data-n="1"><b>Tell us the item</b><span>Name, model number or a link, the quantity and your city.</span></li>
<li data-n="2"><b>Get a price in rupees</b><span>We find it from manufacturers and verified suppliers and reply on WhatsApp.</span></li>
<li data-n="3"><b>Confirm and receive</b><span>We import it on order and deliver it anywhere in Pakistan.</span></li></ol>
<a class="btn" href="/quote/">Start a request</a></div>
<div class="req reveal"><h3>Example request</h3>
<div class="row"><span>Item</span><b>TDH39 audiometric headphones</b></div>
<div class="row"><span>Quantity</span><b>1</b></div>
<div class="row"><span>Buying for</span><b>Clinic</b></div>
<div class="row"><span>City</span><b>Lahore</b></div>
<div class="wa">We reply on WhatsApp with the price in rupees.</div></div>
</div></section>
<section class="sec"><h2>Who we supply</h2>
<div class="who"><div class="reveal">Clinics<small>GP, ENT, dental and specialist practices</small></div><div class="reveal">Hospitals<small>Wards, theatres and emergency rooms</small></div><div class="reveal">Laboratories<small>Clinical, research and teaching labs</small></div><div class="reveal">Home use<small>Patients and families buying for home care</small></div></div></section>
{'<section class="sec"><div class="sec-head"><div><h2>Buying guides</h2><p>What to check before you buy.</p></div><a class="btn ghost" href="/guides/">All guides</a></div><ul class="guides">' + g_list + '</ul></section>' if guides else ''}
<section class="sec"><h2 style="margin-bottom:28px">Questions</h2><div class="qa">{qa}</div></section>
<div class="final reveal"><div><h2>What do you need?</h2><p>Type the item and we'll take you to the right page or the quote form.</p></div>{search}</div>
</div>"""
    ws = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/"}
    write("/", shell("/", "Medical Equipment & Surgical Disposables in Pakistan | " + NAME,
                     "Audiology, diagnostic, hospital and lab equipment and surgical disposables, imported on order and supplied across Pakistan. Get a price in rupees.",
                     body, [ORG, ws, faq_ld(home_faqs)], full=True)); urls.append("/")

    # ---- site.js: scroll reveal + search routing
    keys = {pr["slug"]: [pr["name"].lower()] for pr in PRODUCTS}
    keys["bp-apparatus"] += ["bp", "blood pressure", "sphygmomanometer"]; keys["pulse-oximeter"] += ["oximeter", "spo2"]
    keys["nebulizer"] += ["nebuliser"]; keys["glucometer"] += ["glucose", "sugar"]; keys["iv-cannula"] += ["cannula", "branula"]
    keys["surgical-gloves"] += ["gloves", "glove"]; keys["syringes"] += ["syringe"]; keys["oxygen-concentrator"] += ["oxygen"]
    keys["audiometer"] += ["audiometry"]; keys["hearing-aid"] += ["hearing"]
    js = """(function(){
var R=%s;
document.querySelectorAll("form[data-search]").forEach(function(f){f.addEventListener("submit",function(ev){var q=(f.item.value||"").toLowerCase().trim();if(!q)return;for(var k in R){for(var i=0;i<R[k].length;i++){if(q.indexOf(R[k][i])>-1&&q.length<=R[k][i].length+12){ev.preventDefault();location.href="/products/"+k+"/";return}}}});});
var els=document.querySelectorAll(".reveal");
if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches){els.forEach(function(x){x.classList.add("in")});return}
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}})},{rootMargin:"0px 0px -8%% 0px"});
els.forEach(function(x){io.observe(x)});
})();
""" % json.dumps(keys)
    open(os.path.join(ROOT, "site.js"), "w").write(js)

    # ---- categories
    for c in CATS:
        rel = [g for g in guides if g.get("category", "").lower().startswith(c["name"].split()[0].lower()[:6])]
        items = "".join(f'<div class="item"><h3>{e(n)}</h3><p>{e(d)}</p><p class="ask"><b>When you ask for a price, tell us:</b> {e(a)}</p></div>' for n, d, a in c["items"])
        others = "".join(f'<li><a href="/{o["slug"]}/">{e(o["name"])}</a></li>' for o in CATS if o is not c)
        rel_html = ('<section><h2>Buying guides</h2><ul class="guides">' + "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a><p>{e(g["description"])}</p></li>' for g in rel) + "</ul></section>") if rel else ""
        cprods = [pr for pr in PRODUCTS if pr["cat"] == c["slug"]]
        if cprods:
            rel_html = '<section><h2>Prices in Pakistan</h2><ul class="guides">' + "".join(f'<li><a href="/products/{pr["slug"]}/">{e(pr["name"])} price in Pakistan</a></li>' for pr in cprods) + "</ul></section>" + rel_html
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

    # ---- products ("<product> price in Pakistan")
    catname = {c["slug"]: c["name"] for c in CATS}
    for pr in PRODUCTS:
        p = f'/products/{pr["slug"]}/'
        n, nl = pr["name"], pr["name"].lower()
        answer = (f"We don't publish fixed {nl} prices because they change with the model, the features and the exchange rate. "
                  f"Send us the {nl} model you want, or the features you need, and we reply on WhatsApp with today's price in rupees. "
                  "Items are imported on order and supplied across Pakistan.")
        types = "".join(f"<li><strong>{e(a)}.</strong> {e(b)}</li>" for a, b in pr["types"])
        fac = "".join(f"<li>{e(x)}</li>" for x in pr["factors"])
        chk = "".join(f"<li>{e(x)}</li>" for x in pr["checks"])
        faqs = [(f"What is the {nl} price in Pakistan?", f"It depends on the type, brand and model, and on the exchange rate, so we quote each request. Send the model or the features you need through our quote form and we reply with today's price in rupees.")] + pr["faqs"]
        rel = [g for g in guides if any(w in (g["title"] + " " + g["slug"]).lower() for w in nl.replace("bp apparatus", "blood pressure").split()[:1])]
        rel_html = "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></li>' for g in rel[:3])
        sib = [o for o in PRODUCTS if o["cat"] == pr["cat"] and o is not pr]
        sib_html = "".join(f'<li><a href="/products/{o["slug"]}/">{e(o["name"])} price in Pakistan</a></li>' for o in sib)
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/products/">Products</a> › {e(n)}</nav>
<div class="hero"><h1>{e(n)} price in Pakistan</h1><p class="lead">{e(pr["lead"])}</p></div>
<div class="article"><article class="prose">
<div class="answer"><b>Quick answer</b><p>{e(answer)}</p></div>
<h2>What types of {e(nl)} are there?</h2><ul>{types}</ul>
<h2>What changes the {e(nl)} price?</h2><ul>{fac}</ul>
<h2>What should you check before you buy?</h2><ul>{chk}</ul>
<h2>Which brands and models can we source?</h2><p>{e(pr["brands"])}</p>
<h2>How do you get today's price?</h2><p>Fill in the <a href="/quote/">quote form</a> with the {e(nl)} model or the features you need, the quantity and your city. We reply on WhatsApp with a price in rupees. Items are imported on order and supplied across Pakistan to clinics, hospitals, labs and individuals.</p>
{'<h2>Related guides</h2><ul>' + rel_html + '</ul>' if rel_html else ''}
<h2 id="faq">Frequently asked questions</h2>{faq_html(faqs)}
{'<h2>Related products</h2><ul>' + sib_html + '</ul>' if sib_html else ''}
<p class="meta">Category: <a href="/{pr["cat"]}/">{e(catname[pr["cat"]])}</a></p>
</article>
<aside><div class="box"><h3>Get today's {e(nl)} price</h3><p>Send the model or features you need. We reply on WhatsApp with a price in rupees.</p><a class="btn" href="/quote/">Request a quote</a></div></aside></div>"""
        prod = {"@context": "https://schema.org", "@type": "WebPage", "name": f"{n} price in Pakistan", "url": SITE + p,
                "about": {"@type": "Thing", "name": n}, "publisher": {"@id": SITE + "/#org"}}
        write(p, shell(p, f"{n} Price in Pakistan: Types and What to Check | {NAME}",
              f"{n} price in Pakistan: types, what changes the price and what to check before you buy. Get today's price in rupees, supplied across Pakistan."[:158],
              body, [ORG, prod, faq_ld(faqs), crumbs_ld([("Home", "/"), ("Products", "/products/"), (n, p)])]))
        urls.append(p)
    plist = "".join(f'<li><a href="/products/{pr["slug"]}/">{e(pr["name"])} price in Pakistan</a><p>{e(pr["lead"].split(". ")[0])}.</p></li>' for pr in PRODUCTS)
    write("/products/", shell("/products/", "Medical Equipment Prices in Pakistan: Popular Products | " + NAME,
          "Prices in Pakistan for nebulizers, thermometers, BP apparatus, glucometers, pulse oximeters, stethoscopes, wheelchairs and more. Get today's price.",
          f'<nav class="crumbs"><a href="/">Home</a> › Products</nav><div class="hero"><h1>Popular medical products</h1><p class="lead">The items people in Pakistan search for most. Each page explains the types, what changes the price and what to check, and you can get today\'s price in rupees.</p></div><section><ul class="guides">{plist}</ul></section>',
          [crumbs_ld([("Home", "/"), ("Products", "/products/")])])); urls.append("/products/")

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
<div class="asked" id="asked" hidden></div>
<div class="formwrap"><iframe data-tally-src="https://tally.so/embed/{TALLY}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="900" frameborder="0" marginheight="0" marginwidth="0" title="Request a quote"></iframe></div>
<script>(function(){{var s="https://tally.so/widgets/embed.js";function l(){{if(typeof Tally!=="undefined")Tally.loadEmbeds();else document.querySelectorAll("iframe[data-tally-src]:not([src])").forEach(function(f){{f.src=f.dataset.tallySrc}})}}if(typeof Tally!=="undefined")l();else if(!document.querySelector('script[src="'+s+'"]')){{var t=document.createElement("script");t.src=s;t.onload=l;t.onerror=l;document.body.appendChild(t)}}}})();</script>
<script>(function(){{var q=new URLSearchParams(location.search).get("item");if(!q)return;var a=document.getElementById("asked");a.textContent="You searched for \u201c"+q.slice(0,120)+"\u201d. Type it into the first question below and add the quantity and your city.";a.hidden=false}})();</script>
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
    L += ["", "## Product price pages"] + [f"- [{pr['name']} price in Pakistan]({SITE}/products/{pr['slug']}/): types, price factors and how to get today's price" for pr in PRODUCTS]
    if guides:
        L += ["", "## Buying guides"] + [f"- [{g['title']}]({SITE}/guides/{g['slug']}/): {g['description']}" for g in guides]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(L) + "\n")
    print(f"built {len(urls)} pages, {len(guides)} guides")

if __name__ == "__main__":
    main()

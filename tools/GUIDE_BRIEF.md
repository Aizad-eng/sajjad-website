# Guide brief: SurgiSource (medical equipment and surgical disposables, Pakistan)

SurgiSource sources medical equipment and surgical disposables for clinics, hospitals, laboratories and individuals in Pakistan. Items are imported on order and supplied across Pakistan. Buyers send a request through the quote form at /quote/ and get a price in rupees on WhatsApp.

## Hard rules
1. Never invent facts, prices, customers, orders, certifications, stock or delivery times. The only real past order you may mention: a TDH39/DD45-type audiometric headset sourced from a verified Alibaba supplier and delivered in Pakistan. SurgiSource supplies any quantity, from one unit to clinic or hospital volumes; never describe it as single-item only.
2. Never claim SurgiSource holds a DRAP licence, registration or any certification. Never claim we inspect, test, calibrate or service equipment.
3. Never state a price, tax rate or fee unless you verified it today from an official source (DRAP, FBR, the manufacturer) and cite it. Never quote product prices.
4. Every factual claim about a product, standard, law or process must come from a page you actually opened (WebFetch/WebSearch). Prefer official sources: DRAP (dra.gov.pk), manufacturers (RadioEar, Interacoustics, Masimo, Omron...), standards bodies (ISO, IEC, ASTM, EN summaries), WHO, FDA. If you cannot verify, leave it out or hedge with "check the current rule".
5. No medical advice or diagnosis. These are buying guides for equipment, not treatment guides.
6. Plain English, short sentences, Pakistani reader, no em dashes, no exclamation marks, no hype words (ultimate, seamless, game-changer, unlock, elevate, dive into).
7. Contact is only the quote form at /quote/. Never print a phone number.

## Format (one JSON file per guide, in content/guides/<slug>.json)
{
 "slug": "kebab-case",
 "title": "H1 title, question or keyword first",
 "seo_title": "Google title, 60 chars max, keyword first",
 "description": "Meta description, 140-155 chars",
 "category": "exactly the category given for your slug in tools/GUIDE_TOPICS.md",
 "minutes": 8,
 "answer": "Quick answer, 40-60 words, first sentence answers the title directly",
 "body": "HTML using only <h2>, <p>, <ul>, <ol>, <li>, <strong>, <table><thead><tr><th></th></tr></thead><tbody><tr><td></td></tr></tbody></table>, <a href>. 1,000-1,600 words, 7-10 question-style H2s, at least one table, end with <h2>Sources</h2><ul><li><a href=\"https://...\">Name</a></li></ul> of pages you opened. External links only in Sources. Internal links (3 to 6 per guide): /quote/, category pages /audiology-equipment/, /surgical-disposables/, /surgical-instruments/, /diagnostic-equipment/, /hospital-equipment/, /laboratory-equipment/, product price pages /products/<slug>/ (nebulizer, thermometer, bp-apparatus, glucometer, pulse-oximeter, stethoscope, wheelchair, hospital-bed, oxygen-concentrator, syringes, iv-cannula, surgical-gloves, audiometer, hearing-aid), and any /guides/<slug>/ listed in tools/GUIDE_TOPICS.md. Never link to a slug that is not in those lists.",
 "faqs": [["Question?", "Answer, 1-3 sentences."]]   // exactly 5
}
End each guide with one short paragraph saying SurgiSource can source the item on order, with a link to /quote/.
Validate before replying: python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('content/guides/*.json')];print('ok')"
Self-audit: grep your files for "licen", "certif", "inspect", "calibrat", "Rs ", "PKR", "—", "!" and fix anything that breaks the rules (describing what a standard or DRAP requires is fine; claiming we have it is not).
Reply with slugs, word counts, sources used and anything you could not verify.


## SEO, AEO and GEO (so Google and AI assistants pick the page up)
- Title and H1 lead with the exact phrase people search (for example "Mesh nebulizer price in Pakistan", "IV cannula sizes and colour codes"). seo_title keyword first, 60 characters max.
- The quick answer is a self-contained 40 to 60 word answer an AI assistant could quote word for word. First sentence answers the title. Name the entity in full (for example "the Drug Regulatory Authority of Pakistan (DRAP)").
- Every H2 is a real question people ask. The first sentence under each H2 answers it directly in one sentence, then explain.
- Include at least one table (comparison, size chart, checklist or spec table) with clear column headers and units.
- Use specific, checkable facts with numbers and standards (ISO, IEC, ASTM, EN numbers, manufacturer model names) from sources you opened. Put "at the time of writing (November 2026)" next to anything that can change.
- 1,000 to 1,600 words of body. Exactly 5 FAQs phrased as natural questions, answers 1 to 3 sentences that stand alone.
- "Price in Pakistan" pages never state a price. Explain what changes the price (type, brand, features, exchange rate, quantity) and that SurgiSource quotes today's price in rupees through /quote/.
- No medication dosing, no diagnosis, no treatment advice: write "follow your doctor's advice" where relevant. Equipment only.
- Use clear, unique wording. Do not copy sentences from sources.

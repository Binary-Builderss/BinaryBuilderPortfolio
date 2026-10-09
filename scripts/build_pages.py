"""Writes every HTML page and the sitemap in public/, in English and Italian.

The site has no build step: run `python3 scripts/build_pages.py` after editing copy here, then commit the output.
English lives at /, /services/<slug> and /privacy; Italian at /it/, /it/servizi/<slug> and /it/privacy.
Each language also gets a 404.html, which Cloudflare serves for unknown paths.
"""
import json
import math
import pathlib
import random

PUBLIC = pathlib.Path(__file__).resolve().parent.parent / "public"
BASE = "https://binarybuilders.dev"
EMAIL = "contactus@binarybuilders.dev"  # forwarded by Cloudflare Email Routing
BOOKING = "https://calendar.app.google/YGhmBX6z3w4fvo8m6"  # Google Calendar appointment schedule on giuseppe@
LASTMOD = "2026-10-09"

UI = {
    "en": {
        "home": "/", "services": "/services/", "locale": "en_US", "other": "it", "switch": "Italiano",
        "home_title": "BinaryBuilders | Java, Salesforce and API Development",
        "home_desc": "BinaryBuilders is an independent software engineering team: Java and Spring Boot backends, Salesforce development, React and Next.js apps, and the integrations between them.",
        "home_og": "Backend, web, Salesforce and integration work from an independent two-engineer team.",
        "studio": "Software engineering studio", "nav": "Services", "book": "Book a call",
        "links": ["Salesforce", "Java and APIs", "Web apps", "Maintenance"],
        "contact_h": "Tell us about your project",
        "contact_p": "Send us the scope and the systems involved. We will tell you honestly whether we are the right fit.",
        "more": "Other services", "privacy": "/privacy",
        "nf_title": "Page not found | BinaryBuilders", "nf_h1": "Page not found",
        "nf_p": "This address does not exist, or the page has moved. Everything we do is listed below.",
        "nf_home": "Go to the home page",
    },
    "it": {
        "home": "/it/", "services": "/it/servizi/", "locale": "it_IT", "other": "en", "switch": "English",
        "home_title": "BinaryBuilders | Sviluppo Java, Salesforce e API",
        "home_desc": "BinaryBuilders è un team indipendente di ingegneria del software: backend Java e Spring Boot, sviluppo Salesforce, app React e Next.js e integrazioni tra sistemi.",
        "home_og": "Backend, web, Salesforce e integrazioni da un team indipendente di due ingegneri.",
        "studio": "Studio di ingegneria del software", "nav": "Servizi", "book": "Prenota una call",
        "links": ["Salesforce", "Java e API", "Web app", "Manutenzione"],
        "contact_h": "Raccontateci il vostro progetto",
        "contact_p": "Inviateci il perimetro e i sistemi coinvolti. Vi diremo onestamente se siamo le persone giuste.",
        "more": "Altri servizi", "privacy": "/it/privacy",
        "nf_title": "Pagina non trovata | BinaryBuilders", "nf_h1": "Pagina non trovata",
        "nf_p": "Questo indirizzo non esiste, oppure la pagina è stata spostata. Qui sotto trovate tutto quello che facciamo.",
        "nf_home": "Torna alla home",
    },
}

# Plain, factual policy: the site has no analytics, no tracking cookies and no forms (checked 2026-10-09).
PRIVACY = {
    "en": {
        "title": "Privacy Policy | BinaryBuilders",
        "desc": "How binarybuilders.dev handles personal data: no analytics and no tracking cookies, only email and call bookings.",
        "h1": "Privacy policy",
        "lede": "This site does not use analytics, advertising or tracking cookies. This page explains the little personal data involved when you visit it, write to us or book a call.",
        "body": f"""
      <h2>Who is responsible</h2>
      <p>BinaryBuilders, the software engineering team of Giuseppe Scappaticci and Michele Sabatino, is the data controller. You can reach us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h2>Visiting the site</h2>
      <p>The site is hosted on Cloudflare. To deliver pages and protect the site from abuse, Cloudflare processes technical data such as your IP address, browser type and the pages requested. We do not use this data to identify you. Fonts and all other files are served from our own domain, so browsing the site loads nothing from third parties.</p>
      <h2>Cookies</h2>
      <p>The site sets one technical cookie, <code>lang</code>, and only if you switch language. It remembers your choice for one year and contains nothing else. It needs no consent, and no other cookies are set.</p>
      <h2>Writing to us</h2>
      <p>Messages sent to {EMAIL} are forwarded by Cloudflare Email Routing to our mailbox. We use your address and your message only to reply and, if we work together, to run the project. We keep the correspondence for as long as that requires, or as long as the law requires.</p>
      <h2>Booking a call</h2>
      <p>The "Book a call" button opens a booking page run by Google Calendar. The name, email and notes you enter there are processed by Google and shared with us to schedule the call and send you the video link. Google's own <a href="https://policies.google.com/privacy">privacy policy</a> applies to that page.</p>
      <h2>Legal basis and transfers</h2>
      <p>We process this data to answer requests you start (Article 6(1)(b) GDPR) and for our legitimate interest in running a secure website (Article 6(1)(f) GDPR). Cloudflare and Google are based in the United States and transfer data under the EU-U.S. Data Privacy Framework.</p>
      <h2>Your rights</h2>
      <p>You can ask us to access, correct or delete your data, to restrict or object to its processing, or to receive it in a portable format, by writing to {EMAIL}. You can also lodge a complaint with your data protection authority: in Italy, the Garante per la protezione dei dati personali.</p>
      <p class="updated">Last updated: 9 October 2026.</p>""",
    },
    "it": {
        "title": "Privacy | BinaryBuilders",
        "desc": "Come binarybuilders.dev tratta i dati personali: nessuna statistica e nessun cookie di tracciamento, solo email e prenotazioni di call.",
        "h1": "Informativa privacy",
        "lede": "Questo sito non usa statistiche, pubblicità o cookie di tracciamento. Questa pagina spiega i pochi dati personali coinvolti quando lo visitate, ci scrivete o prenotate una call.",
        "body": f"""
      <h2>Chi è il titolare</h2>
      <p>Il titolare del trattamento è BinaryBuilders, il team di ingegneria del software di Giuseppe Scappaticci e Michele Sabatino. Potete contattarci a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h2>Navigazione</h2>
      <p>Il sito è ospitato su Cloudflare. Per servire le pagine e proteggere il sito dagli abusi, Cloudflare tratta dati tecnici come l'indirizzo IP, il tipo di browser e le pagine richieste. Non usiamo questi dati per identificarvi. I font e tutti gli altri file sono serviti dal nostro dominio, quindi navigando non viene caricato nulla da terze parti.</p>
      <h2>Cookie</h2>
      <p>Il sito imposta un solo cookie tecnico, <code>lang</code>, e solo se cambiate lingua. Ricorda la scelta per un anno e non contiene altro. Non richiede consenso e non vengono impostati altri cookie.</p>
      <h2>Se ci scrivete</h2>
      <p>I messaggi inviati a {EMAIL} vengono inoltrati da Cloudflare Email Routing alla nostra casella. Usiamo il vostro indirizzo e il messaggio solo per rispondere e, se lavoriamo insieme, per gestire il progetto. Conserviamo la corrispondenza per il tempo necessario a questo scopo o per quello richiesto dalla legge.</p>
      <h2>Prenotazione di una call</h2>
      <p>Il pulsante "Prenota una call" apre una pagina di prenotazione gestita da Google Calendar. Il nome, l'email e le note che inserite sono trattati da Google e condivisi con noi per fissare la call e inviarvi il link della videochiamata. Per quella pagina vale l'<a href="https://policies.google.com/privacy?hl=it">informativa privacy di Google</a>.</p>
      <h2>Base giuridica e trasferimenti</h2>
      <p>Trattiamo questi dati per rispondere a richieste che avviate voi (art. 6, par. 1, lett. b GDPR) e per il nostro legittimo interesse a gestire un sito sicuro (art. 6, par. 1, lett. f GDPR). Cloudflare e Google hanno sede negli Stati Uniti e trasferiscono i dati nell'ambito dell'EU-U.S. Data Privacy Framework.</p>
      <h2>I vostri diritti</h2>
      <p>Potete chiederci l'accesso, la rettifica o la cancellazione dei vostri dati, la limitazione o l'opposizione al trattamento, o di riceverli in un formato portabile, scrivendo a {EMAIL}. Potete anche presentare reclamo al Garante per la protezione dei dati personali.</p>
      <p class="updated">Ultimo aggiornamento: 9 ottobre 2026.</p>""",
    },
}

SERVICES = [
    {
        "en": {
            "slug": "salesforce-development",
            "title": "Salesforce Development: Apex, Flow and LWC | BinaryBuilders",
            "desc": "Apex classes and triggers, Salesforce Flow, Lightning Web Components and REST integrations, built and maintained by an independent two-engineer team.",
            "h1": "Salesforce development and automation",
            "service": "Salesforce development",
            "lede": "We customize Salesforce, implement business logic, automate workflows, connect external services and maintain existing orgs. We work directly with companies and as development capacity for Salesforce consulting partners.",
            "body": """
      <h2>What we build</h2>
      <ul>
        <li><strong>Apex classes and triggers</strong> for business logic that declarative tools cannot cover.</li>
        <li><strong>Salesforce Flow</strong> automation for approvals, record updates and multi-step processes.</li>
        <li><strong>Lightning Web Components</strong> for custom UI inside Lightning pages and apps.</li>
        <li><strong>REST API integrations</strong> between Salesforce and the other systems you run.</li>
        <li><strong>Troubleshooting and performance work</strong> on existing implementations: governor limits, slow queries, failing automations.</li>
      </ul>
      <h2>Who it is for</h2>
      <p>Businesses that run Salesforce and need custom development or automation, and Salesforce consulting companies that need specialized development or integration capacity on a defined scope. We are open to direct engagements and to B2B subcontracting.</p>
      <h2>How we work</h2>
      <p>We start from the business process, agree on realistic requirements and deliverables, and write Apex that is covered by tests and easy for your team to maintain. We prefer to reuse what your org already does well instead of rebuilding it.</p>""",
        },
        "it": {
            "slug": "sviluppo-salesforce",
            "title": "Sviluppo Salesforce: Apex, Flow e LWC | BinaryBuilders",
            "desc": "Classi e trigger Apex, Salesforce Flow, Lightning Web Components e integrazioni REST, sviluppati e mantenuti da un team indipendente di due ingegneri.",
            "h1": "Sviluppo e automazione Salesforce",
            "service": "Sviluppo Salesforce",
            "lede": "Personalizziamo Salesforce, implementiamo la logica di business, automatizziamo i processi, colleghiamo servizi esterni e manteniamo org esistenti. Lavoriamo direttamente con le aziende e come capacità di sviluppo per i partner di consulenza Salesforce.",
            "body": """
      <h2>Cosa sviluppiamo</h2>
      <ul>
        <li><strong>Classi e trigger Apex</strong> per la logica di business che gli strumenti dichiarativi non coprono.</li>
        <li><strong>Salesforce Flow</strong> per approvazioni, aggiornamenti dei record e processi in più passaggi.</li>
        <li><strong>Lightning Web Components</strong> per interfacce personalizzate in pagine e app Lightning.</li>
        <li><strong>Integrazioni REST API</strong> tra Salesforce e gli altri sistemi che usate.</li>
        <li><strong>Troubleshooting e prestazioni</strong> su implementazioni esistenti: governor limit, query lente, automazioni che falliscono.</li>
      </ul>
      <h2>Per chi è</h2>
      <p>Aziende che usano Salesforce e hanno bisogno di sviluppo personalizzato o di automazione, e società di consulenza Salesforce che cercano capacità di sviluppo o di integrazione su un perimetro definito. Siamo aperti sia a incarichi diretti sia al subappalto B2B.</p>
      <h2>Come lavoriamo</h2>
      <p>Partiamo dal processo di business, concordiamo requisiti e deliverable realistici e scriviamo Apex coperto da test e facile da mantenere per il vostro team. Preferiamo riusare ciò che la vostra org fa già bene invece di ricostruirlo.</p>""",
        },
    },
    {
        "en": {
            "slug": "backend-api-integration",
            "title": "Java, Spring Boot and API Integration | BinaryBuilders",
            "desc": "Backend services and integrations in Java, Spring Boot, Go and C#: REST APIs, microservices, databases and connections between enterprise systems.",
            "h1": "Backend development and API integrations",
            "service": "Backend development and API integration",
            "lede": "We build reliable backend services and connect applications, external APIs, databases and enterprise systems, so data moves where it needs to without manual work.",
            "body": """
      <h2>What we build</h2>
      <ul>
        <li><strong>REST APIs</strong> designed around clear contracts and versioning.</li>
        <li><strong>Java and Spring Boot services</strong>, from single services to microservices and distributed systems.</li>
        <li><strong>Go and C# services</strong> when they fit the project or the existing stack better.</li>
        <li><strong>Business logic and database integration</strong> for the rules your applications depend on.</li>
        <li><strong>Third-party and enterprise integrations</strong>, including connections between Salesforce and other platforms.</li>
        <li><strong>Process automation</strong> that replaces repetitive manual steps between systems.</li>
      </ul>
      <h2>Who it is for</h2>
      <p>Startups and companies that need a backend built or extended, teams with systems that do not talk to each other, and agencies or development teams that need extra backend capacity for a specific project.</p>
      <h2>How we work</h2>
      <p>We map the systems and data involved first, define the integration points and failure cases, then deliver clean, maintainable and testable code. Where an existing system already does the job, we connect to it instead of replacing it.</p>""",
        },
        "it": {
            "slug": "backend-integrazione-api",
            "title": "Java, Spring Boot e integrazione API | BinaryBuilders",
            "desc": "Servizi backend e integrazioni in Java, Spring Boot, Go e C#: REST API, microservizi, database e collegamenti tra sistemi aziendali.",
            "h1": "Sviluppo backend e integrazioni API",
            "service": "Sviluppo backend e integrazione API",
            "lede": "Costruiamo servizi backend affidabili e colleghiamo applicazioni, API esterne, database e sistemi aziendali, così i dati arrivano dove servono senza lavoro manuale.",
            "body": """
      <h2>Cosa sviluppiamo</h2>
      <ul>
        <li><strong>REST API</strong> progettate attorno a contratti chiari e al versioning.</li>
        <li><strong>Servizi Java e Spring Boot</strong>, dal singolo servizio ai microservizi e ai sistemi distribuiti.</li>
        <li><strong>Servizi in Go e C#</strong> quando si adattano meglio al progetto o allo stack esistente.</li>
        <li><strong>Logica di business e integrazione con i database</strong> per le regole da cui dipendono le vostre applicazioni.</li>
        <li><strong>Integrazioni con terze parti e sistemi aziendali</strong>, compresi i collegamenti tra Salesforce e altre piattaforme.</li>
        <li><strong>Automazione dei processi</strong> che sostituisce i passaggi manuali ripetitivi tra sistemi.</li>
      </ul>
      <h2>Per chi è</h2>
      <p>Startup e aziende che devono costruire o estendere un backend, team con sistemi che non comunicano tra loro, e agenzie o team di sviluppo che cercano capacità backend aggiuntiva per un progetto specifico.</p>
      <h2>Come lavoriamo</h2>
      <p>Prima mappiamo i sistemi e i dati coinvolti, definiamo i punti di integrazione e i casi di errore, poi consegniamo codice pulito, manutenibile e testabile. Se un sistema esistente fa già il suo lavoro, ci colleghiamo a quello invece di sostituirlo.</p>""",
        },
    },
    {
        "en": {
            "slug": "custom-software",
            "title": "Custom Software, React and Next.js Apps | BinaryBuilders",
            "desc": "Custom web applications, dashboards and internal tools in React, Next.js and TypeScript, connected to your backend services. From focused features to MVPs.",
            "h1": "Custom software and web applications",
            "service": "Custom software development",
            "lede": "We build applications and features tailored to specific business requirements, from focused improvements to larger application components and MVPs.",
            "body": """
      <h2>What we build</h2>
      <ul>
        <li><strong>Web applications</strong> in React, Next.js and TypeScript that work on any screen size.</li>
        <li><strong>Dashboards and internal tools</strong> that put the data your team needs in one place.</li>
        <li><strong>MVPs and custom features</strong> for startups that need to ship and learn.</li>
        <li><strong>Frontend and backend together</strong>, so the interface and the services behind it are designed as one system.</li>
        <li><strong>Components in C# or C++</strong> when a project calls for them.</li>
      </ul>
      <h2>Who it is for</h2>
      <p>Startups that need technical support or an MVP, small and medium businesses that need software shaped around their processes, and digital agencies that need dependable external development.</p>
      <h2>How we work</h2>
      <p>We start by understanding the problem, then agree on a clear scope and deliverables. We favour practical, maintainable solutions over unnecessary complexity, and keep you updated throughout development.</p>""",
        },
        "it": {
            "slug": "software-su-misura",
            "title": "Software su misura, app React e Next.js | BinaryBuilders",
            "desc": "Web app, dashboard e strumenti interni su misura in React, Next.js e TypeScript, collegati ai vostri servizi backend. Dalle singole funzionalità agli MVP.",
            "h1": "Software su misura e applicazioni web",
            "service": "Sviluppo software su misura",
            "lede": "Sviluppiamo applicazioni e funzionalità costruite su requisiti di business specifici, dai miglioramenti mirati a componenti applicativi più ampi e MVP.",
            "body": """
      <h2>Cosa sviluppiamo</h2>
      <ul>
        <li><strong>Applicazioni web</strong> in React, Next.js e TypeScript che funzionano su qualsiasi schermo.</li>
        <li><strong>Dashboard e strumenti interni</strong> che riuniscono in un solo posto i dati di cui il vostro team ha bisogno.</li>
        <li><strong>MVP e funzionalità su misura</strong> per startup che devono rilasciare e imparare in fretta.</li>
        <li><strong>Frontend e backend insieme</strong>, così l'interfaccia e i servizi che la alimentano sono progettati come un unico sistema.</li>
        <li><strong>Componenti in C# o C++</strong> quando il progetto li richiede.</li>
      </ul>
      <h2>Per chi è</h2>
      <p>Startup che hanno bisogno di supporto tecnico o di un MVP, piccole e medie imprese che cercano software costruito sui propri processi, e agenzie digitali che cercano uno sviluppo esterno affidabile.</p>
      <h2>Come lavoriamo</h2>
      <p>Partiamo dal capire il problema, poi concordiamo un perimetro e dei deliverable chiari. Preferiamo soluzioni pratiche e manutenibili alla complessità inutile, e vi teniamo aggiornati per tutto lo sviluppo.</p>""",
        },
    },
    {
        "en": {
            "slug": "software-maintenance",
            "title": "Software Maintenance and Debugging | BinaryBuilders",
            "desc": "We analyze, troubleshoot, refactor, optimize and extend existing software, and take ownership of clearly defined technical tasks within larger projects.",
            "h1": "Software maintenance and technical problem solving",
            "service": "Software maintenance",
            "lede": "We analyze, troubleshoot, refactor, optimize and extend software you already run, and take ownership of clearly defined technical tasks within larger projects.",
            "body": """
      <h2>What we do</h2>
      <ul>
        <li><strong>Troubleshooting and debugging</strong> of bugs, failing jobs and integrations that stopped working.</li>
        <li><strong>Refactoring</strong> that makes existing code easier to change without rewriting it from scratch.</li>
        <li><strong>Performance improvements</strong> in backend services, databases and Salesforce orgs.</li>
        <li><strong>New features on existing codebases</strong>, following the conventions already in place.</li>
        <li><strong>Ongoing maintenance agreements</strong> for systems that need regular care.</li>
      </ul>
      <h2>Who it is for</h2>
      <p>Companies with software that works but needs attention, and development teams or agencies that need additional engineering capacity for a defined piece of work.</p>
      <h2>How we work</h2>
      <p>We read the existing code before proposing changes, agree on what done means, and leave the codebase easier to work with than we found it.</p>""",
        },
        "it": {
            "slug": "manutenzione-software",
            "title": "Manutenzione e debugging del software | BinaryBuilders",
            "desc": "Analisi, debugging, refactoring, ottimizzazione ed estensione di software esistente, più attività tecniche ben definite all'interno di progetti più ampi.",
            "h1": "Manutenzione software e risoluzione di problemi tecnici",
            "service": "Manutenzione software",
            "lede": "Analizziamo, correggiamo, rifattorizziamo, ottimizziamo ed estendiamo il software che già usate, e prendiamo in carico attività tecniche ben definite all'interno di progetti più ampi.",
            "body": """
      <h2>Cosa facciamo</h2>
      <ul>
        <li><strong>Troubleshooting e debugging</strong> di bug, job che falliscono e integrazioni che hanno smesso di funzionare.</li>
        <li><strong>Refactoring</strong> che rende il codice esistente più facile da modificare senza riscriverlo da zero.</li>
        <li><strong>Miglioramenti delle prestazioni</strong> in servizi backend, database e org Salesforce.</li>
        <li><strong>Nuove funzionalità su codebase esistenti</strong>, seguendo le convenzioni già in uso.</li>
        <li><strong>Contratti di manutenzione continuativa</strong> per i sistemi che richiedono cura regolare.</li>
      </ul>
      <h2>Per chi è</h2>
      <p>Aziende con software che funziona ma ha bisogno di attenzione, e team di sviluppo o agenzie che cercano capacità di ingegneria aggiuntiva per un lavoro ben definito.</p>
      <h2>Come lavoriamo</h2>
      <p>Leggiamo il codice esistente prima di proporre modifiche, concordiamo cosa significa "finito" e lasciamo la codebase più facile da gestire di come l'abbiamo trovata.</p>""",
        },
    },
]

ORG_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": f"{BASE}/#org",
            "name": "BinaryBuilders",
            "alternateName": "Binary Builders",
            "url": f"{BASE}/",
            "logo": f"{BASE}/assets/apple-touch-icon.png",
            "email": EMAIL,
            "description": "Independent software engineering team building Java and Spring Boot backends, Salesforce solutions, React and Next.js applications, and system integrations.",
            "founder": [{"@type": "Person", "name": "Giuseppe Scappaticci"}, {"@type": "Person", "name": "Michele Sabatino"}],
            "knowsAbout": ["Java", "Spring Boot", "REST API design", "Microservices", "Go", "C#", "C++", "React", "Next.js", "TypeScript",
                           "Salesforce", "Apex", "Salesforce Flow", "Lightning Web Components", "System integration", "Business process automation"],
        },
        {
            "@type": "WebSite",
            "@id": f"{BASE}/#website",
            "name": "BinaryBuilders",
            "alternateName": "Binary Builders",
            "url": f"{BASE}/",
            "inLanguage": ["en", "it"],
            "publisher": {"@id": f"{BASE}/#org"},
        },
    ],
}


def head(lang, title, desc, path, preloads, og_desc=None, alternates=None, ld=None, index=True):
    """alternates: {"en": path, "it": path}; the English page doubles as x-default. index=False for the 404 pages."""
    meta = []
    if index:
        meta.append(f'  <link rel="canonical" href="{BASE}{path}">')
        meta += [f'  <link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in alternates.items()]
        meta.append(f'  <link rel="alternate" hreflang="x-default" href="{BASE}{alternates["en"]}">')
    else:
        meta.append('  <meta name="robots" content="noindex">')
    if ld:
        meta.append(f'  <script type="application/ld+json">\n{json.dumps(ld, indent=2, ensure_ascii=False)}\n  </script>')
    if index:
        meta.append(f"""  <meta property="og:site_name" content="BinaryBuilders">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc or desc}">
  <meta property="og:url" content="{BASE}{path}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{UI[lang]["locale"]}">
  <meta property="og:image" content="{BASE}/assets/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">""")
    nl = "\n"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="color-scheme" content="light dark">
{nl.join(meta)}
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{nl.join(preloads)}
  <link rel="stylesheet" href="/styles.css">"""


def header(lang, switch_href):
    other = UI[lang]["other"]
    return f"""  <header class="top wrap">
    <a class="brand" href="{UI[lang]["home"]}">
      <picture>
        <source srcset="/assets/logo-white.png" media="(prefers-color-scheme: dark)">
        <img src="/assets/logo-black.png" alt="BinaryBuilders" width="480" height="109">
      </picture>
    </a>
    <a class="lang" href="{switch_href}" hreflang="{other}" lang="{other}">{UI[lang]["switch"]}</a>
  </header>"""


def ctas(lang, cls="btn-lg"):
    return f"""<div class="ctas">
      <a class="btn btn-primary {cls}" href="{BOOKING}" target="_blank" rel="noopener">{UI[lang]["book"]}</a>
      <a class="btn btn-ghost {cls}" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>"""


def footer(lang):
    ui = UI[lang]
    links = " ".join(f'<a href="{ui["services"]}{s[lang]["slug"]}">{label}</a>' for s, label in zip(SERVICES, ui["links"]))
    return f"""  <footer class="footer wrap">
    <nav aria-label="{ui["nav"]}">
      <p>{ui["studio"]}</p>
      <p class="links">{links}</p>
    </nav>
    <p>binarybuilders.dev &middot; <a href="{ui["privacy"]}">Privacy</a><br>&copy; 2026 BinaryBuilders</p>
  </footer>"""


def services_list(lang, skip=None):
    items = "\n".join(f'          <li><a href="{UI[lang]["services"]}{s[lang]["slug"]}">{s[lang]["h1"]}</a></li>'
                      for s in SERVICES if s is not skip)
    return f'<ul class="more-list">\n{items}\n        </ul>'


def field(x, y, t=0.9):
    # Same three sine waves as main.js, frozen at one moment.
    return (math.sin(x * 0.11 + t) + math.sin(y * 0.17 - t * 0.8) + math.sin((x + y) * 0.07 + t * 0.5)) / 3


def band():
    """A frozen slice of the home page bit field as plain text: content pages get the texture with no JS."""
    rnd = random.Random(7)  # fixed seed: regenerating the pages does not churn the diff
    rows = ("".join(rnd.choice("01") if field(c, r) > 0.2 else " " for c in range(110)).rstrip() for r in range(14))
    return '  <pre class="band" aria-hidden="true">' + "\n".join(rows) + "</pre>"


JB = '  <link rel="preload" href="/fonts/jetbrains-mono.woff2" as="font" type="font/woff2" crossorigin>'
MARTIAN = '  <link rel="preload" href="/fonts/martian-mono.woff2" as="font" type="font/woff2" crossorigin media="(min-width: 768px)">'


def home(lang):
    ui = UI[lang]
    # On the home page the switch goes through the Worker (?lang=), which remembers the choice in a cookie.
    return f"""{head(lang, ui["home_title"], ui["home_desc"], ui["home"], [JB, MARTIAN], ui["home_og"], {"en": "/", "it": "/it/"}, ORG_LD)}
  <script type="module" src="/main.js"></script>
</head>
<body>
  <canvas class="bits" aria-hidden="true"></canvas>

{header(lang, "/?lang=" + ui["other"])}

  <main class="hero wrap">
    <h1 class="decode">Build. Automate. Scale.</h1>
    {ctas(lang)}
  </main>

{footer(lang)}
</body>
</html>
"""


def doc_page(lang, head_html, switch_href, content):
    """Shared shell of the reading pages: services, privacy, 404."""
    return f"""{head_html}
</head>
<body>
{band()}
{header(lang, switch_href)}

  <main class="doc wrap">
    <article>
{content}
    </article>
  </main>

{footer(lang)}
</body>
</html>
"""


def service(lang, s):
    ui, p = UI[lang], s[lang]
    path = ui["services"] + p["slug"]
    alternates = {l: UI[l]["services"] + s[l]["slug"] for l in UI}
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "name": p["h1"], "serviceType": p["service"], "description": p["desc"],
             "url": BASE + path, "areaServed": "Worldwide", "inLanguage": lang,
             "provider": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "BinaryBuilders", "url": f"{BASE}/"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "BinaryBuilders", "item": BASE + ui["home"]},
                {"@type": "ListItem", "position": 2, "name": p["h1"], "item": BASE + path}]},
        ],
    }
    content = f"""      <p class="crumb"><a href="{ui["home"]}">BinaryBuilders</a> / {ui["nav"]}</p>
      <h1>{p["h1"]}</h1>
      <p class="lede">{p["lede"]}</p>
{p["body"]}
      <nav class="more" aria-labelledby="more-title">
        <h2 id="more-title">{ui["more"]}</h2>
        {services_list(lang, s)}
      </nav>
      <section class="contact" aria-labelledby="contact-title">
        <h2 id="contact-title">{ui["contact_h"]}</h2>
        <p>{ui["contact_p"]}</p>
        {ctas(lang)}
      </section>"""
    return doc_page(lang, head(lang, p["title"], p["desc"], path, [JB, MARTIAN], None, alternates, ld),
                    alternates[ui["other"]], content)


def privacy(lang):
    ui, p = UI[lang], PRIVACY[lang]
    alternates = {l: UI[l]["privacy"] for l in UI}
    content = f"""      <h1>{p["h1"]}</h1>
      <p class="lede">{p["lede"]}</p>
{p["body"]}"""
    return doc_page(lang, head(lang, p["title"], p["desc"], ui["privacy"], [JB, MARTIAN], None, alternates),
                    alternates[ui["other"]], content)


def not_found(lang):
    ui = UI[lang]
    content = f"""      <h1>{ui["nf_h1"]}</h1>
      <p class="lede">{ui["nf_p"]}</p>
      {services_list(lang)}
      <div class="ctas">
        <a class="btn btn-ghost btn-lg" href="{ui["home"]}">{ui["nf_home"]}</a>
      </div>"""
    return doc_page(lang, head(lang, ui["nf_title"], ui["nf_p"], None, [JB, MARTIAN], index=False),
                    "/?lang=" + ui["other"], content)


def write(path, html):
    file = PUBLIC / (path.strip("/") + ("/index.html" if path.endswith("/") else ".html")).lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(html)
    return path


urls = []
for lang in UI:
    ui = UI[lang]
    urls.append(write(ui["home"], home(lang)))
    for s in SERVICES:
        p = s[lang]
        assert len(p["title"]) <= 60 and len(p["desc"]) <= 160, (p["slug"], len(p["title"]), len(p["desc"]))
        urls.append(write(ui["services"] + p["slug"], service(lang, s)))
    urls.append(write(ui["privacy"], privacy(lang)))
    write(ui["home"] + "404", not_found(lang))  # served by Cloudflare for unknown paths, not listed in the sitemap

(PUBLIC / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls)
    + "</urlset>\n"
)
print("\n".join(urls))

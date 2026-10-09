"""Writes every HTML page and the sitemap in public/, in English and Italian.

The site has no build step: run `python3 scripts/build_pages.py` after editing copy here, then commit the output.
English lives at /, /services/<slug>, /about, /privacy and one page per founder; Italian under /it/ with the same pages (/it/servizi/<slug>, /it/chi-siamo).
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
        "more": "Other services", "privacy": "/privacy", "about": "/about", "about_label": "About",
        "nf_title": "Page not found | BinaryBuilders", "nf_h1": "Page not found",
        "nf_p": "This address does not exist, or the page has moved. Everything we do is listed below.",
        "nf_home": "Go to the home page",
    },
    "it": {
        "home": "/it/", "services": "/it/servizi/", "locale": "it_IT", "other": "en", "switch": "English",
        "home_title": "BinaryBuilders | Sviluppo software Java, Salesforce e API",
        "home_desc": "Siamo un piccolo studio indipendente di sviluppo software: backend Java e Spring Boot, Salesforce, applicazioni React e Next.js e integrazioni tra sistemi.",
        "home_og": "Backend, web, Salesforce e integrazioni: uno studio indipendente di sviluppo software.",
        "studio": "Studio di sviluppo software", "nav": "Servizi", "book": "Prenota una call",
        "links": ["Salesforce", "Java e API", "Web app", "Manutenzione"],
        "contact_h": "Parlaci del tuo progetto",
        "contact_p": "Scrivici cosa ti serve e quali sistemi sono coinvolti. Ti diremo con franchezza se siamo le persone giuste.",
        "more": "Altri servizi", "privacy": "/it/privacy", "about": "/it/chi-siamo", "about_label": "Chi siamo",
        "nf_title": "Pagina non trovata | BinaryBuilders", "nf_h1": "Pagina non trovata",
        "nf_p": "Questa pagina non esiste o è stata spostata. Qui sotto trovi tutti i nostri servizi.",
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
        "desc": "Come binarybuilders.dev tratta i dati personali: niente statistiche, niente cookie di tracciamento, solo email e prenotazioni delle call.",
        "h1": "Informativa sulla privacy",
        "lede": "Questo sito non usa statistiche, pubblicità né cookie di tracciamento. Qui spieghiamo quali dati personali entrano in gioco quando visiti il sito, ci scrivi o prenoti una call.",
        "body": f"""
      <h2>Chi è il titolare</h2>
      <p>Il titolare del trattamento è BinaryBuilders, lo studio di sviluppo software di Giuseppe Scappaticci e Michele Sabatino. Puoi contattarci a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h2>Navigazione</h2>
      <p>Il sito è ospitato su Cloudflare. Per mostrare le pagine e proteggere il sito da abusi, Cloudflare tratta alcuni dati tecnici, come indirizzo IP, tipo di browser e pagine richieste. Non li usiamo per identificarti. Font e file sono tutti sul nostro dominio: mentre navighi non viene caricato nulla da siti di terze parti.</p>
      <h2>Cookie</h2>
      <p>Il sito usa un solo cookie tecnico, <code>lang</code>, e solo se cambi lingua: ricorda la tua scelta per un anno e non contiene altro. Non richiede consenso e non ci sono altri cookie.</p>
      <h2>Se ci scrivi</h2>
      <p>Le email inviate a {EMAIL} arrivano nella nostra casella tramite Cloudflare Email Routing. Usiamo il tuo indirizzo e il messaggio solo per risponderti e, se lavoriamo insieme, per gestire il progetto. Conserviamo la corrispondenza per il tempo necessario a questi scopi o per quello previsto dalla legge.</p>
      <h2>Se prenoti una call</h2>
      <p>Il pulsante «Prenota una call» apre una pagina di prenotazione di Google Calendar. Nome, email ed eventuali note che inserisci vengono trattati da Google e condivisi con noi per fissare la call e mandarti il link della videochiamata. Per quella pagina vale l'<a href="https://policies.google.com/privacy?hl=it">informativa privacy di Google</a>.</p>
      <h2>Base giuridica e trasferimenti</h2>
      <p>Trattiamo questi dati per rispondere alle richieste che ci invii (art. 6, par. 1, lett. b del GDPR) e per il nostro legittimo interesse a mantenere il sito sicuro (art. 6, par. 1, lett. f). Cloudflare e Google hanno sede negli Stati Uniti e trasferiscono i dati in base all'EU-U.S. Data Privacy Framework.</p>
      <h2>I tuoi diritti</h2>
      <p>Puoi chiederci in qualsiasi momento di vedere i tuoi dati, correggerli o cancellarli, di limitarne o contestarne il trattamento, o di riceverli in un formato portabile: basta scrivere a {EMAIL}. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>
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
            "desc": "Sviluppo Apex, automazioni con Flow, Lightning Web Components e integrazioni REST su Salesforce, da uno studio indipendente di due sviluppatori.",
            "h1": "Sviluppo e automazione su Salesforce",
            "service": "Sviluppo Salesforce",
            "lede": "Personalizziamo Salesforce, scriviamo la logica di business, automatizziamo i processi, lo colleghiamo agli altri sistemi e ci occupiamo delle org già in uso. Lavoriamo sia direttamente con le aziende sia come supporto allo sviluppo per i partner Salesforce.",
            "body": """
      <h2>Cosa facciamo</h2>
      <ul>
        <li><strong>Classi e trigger Apex</strong> per la logica che gli strumenti dichiarativi non riescono a gestire.</li>
        <li><strong>Automazioni con Salesforce Flow</strong> per approvazioni, aggiornamento dei record e processi a più passaggi.</li>
        <li><strong>Lightning Web Components</strong> per interfacce su misura nelle pagine e nelle app Lightning.</li>
        <li><strong>Integrazioni via REST API</strong> tra Salesforce e gli altri sistemi che usi.</li>
        <li><strong>Analisi e ottimizzazione</strong> di implementazioni esistenti: governor limit, query lente, automazioni che si bloccano.</li>
      </ul>
      <h2>A chi ci rivolgiamo</h2>
      <p>Alle aziende che usano Salesforce e hanno bisogno di sviluppo su misura o di automatizzare i processi, e alle società di consulenza Salesforce che cercano sviluppatori per un progetto ben definito. Lavoriamo sia con incarichi diretti sia in subappalto.</p>
      <h2>Come lavoriamo</h2>
      <p>Partiamo dal processo di business, fissiamo insieme obiettivi e consegne realistici e scriviamo codice Apex coperto da test, che il tuo team possa mantenere senza difficoltà. Se la tua org fa già bene qualcosa, la riusiamo invece di rifarla da capo.</p>""",
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
      <h3>Services and APIs</h3>
      <ul>
        <li><strong>REST APIs</strong> designed around clear contracts and versioning.</li>
        <li><strong>Java and Spring Boot services</strong>, from single services to microservices and distributed systems.</li>
        <li><strong>Go and C# services</strong> when they fit the project or the existing stack better.</li>
        <li><strong>Business logic and database integration</strong> for the rules your applications depend on.</li>
      </ul>
      <h3>Integrations and automation</h3>
      <ul>
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
            "title": "Sviluppo backend Java e integrazioni API | BinaryBuilders",
            "desc": "Servizi backend e integrazioni in Java, Spring Boot, Go e C#: REST API, microservizi, database e collegamenti tra i sistemi aziendali.",
            "h1": "Sviluppo backend e integrazioni API",
            "service": "Sviluppo backend e integrazione API",
            "lede": "Sviluppiamo servizi backend affidabili e colleghiamo applicazioni, API esterne, database e sistemi aziendali, così i dati arrivano dove servono senza passaggi manuali.",
            "body": """
      <h2>Cosa sviluppiamo</h2>
      <h3>Servizi e API</h3>
      <ul>
        <li><strong>REST API</strong> con contratti chiari e versionamento.</li>
        <li><strong>Servizi Java e Spring Boot</strong>, dal singolo servizio fino ai microservizi e ai sistemi distribuiti.</li>
        <li><strong>Servizi in Go e C#</strong>, quando sono la scelta migliore per il progetto o per lo stack che hai già.</li>
        <li><strong>Logica di business e accesso ai dati</strong>, cioè le regole su cui si reggono le tue applicazioni.</li>
      </ul>
      <h3>Integrazioni e automazione</h3>
      <ul>
        <li><strong>Integrazioni con servizi esterni e sistemi aziendali</strong>, compreso il collegamento tra Salesforce e altre piattaforme.</li>
        <li><strong>Automazione dei processi</strong>, per eliminare i passaggi manuali ripetitivi tra un sistema e l'altro.</li>
      </ul>
      <h2>A chi ci rivolgiamo</h2>
      <p>Alle startup e alle aziende che devono costruire o estendere un backend, a chi ha sistemi che non si parlano tra loro, e ad agenzie e team di sviluppo che cercano rinforzi sul backend per un progetto specifico.</p>
      <h2>Come lavoriamo</h2>
      <p>Prima mappiamo i sistemi e i dati coinvolti, poi definiamo i punti di integrazione e cosa succede quando qualcosa va storto. Solo allora scriviamo il codice: pulito, manutenibile e testabile. Se un sistema esistente fa già il suo lavoro, ci colleghiamo a quello invece di sostituirlo.</p>""",
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
            "desc": "Web app, dashboard e strumenti interni su misura in React, Next.js e TypeScript, collegati ai tuoi servizi backend. Dalla singola funzione all'MVP.",
            "h1": "Software su misura e applicazioni web",
            "service": "Sviluppo software su misura",
            "lede": "Sviluppiamo applicazioni e funzionalità costruite sulle esigenze della tua azienda, dal singolo miglioramento a componenti più complessi, fino all'MVP.",
            "body": """
      <h2>Cosa sviluppiamo</h2>
      <ul>
        <li><strong>Applicazioni web</strong> in React, Next.js e TypeScript, che funzionano bene su qualsiasi schermo.</li>
        <li><strong>Dashboard e strumenti interni</strong> che raccolgono in un unico posto i dati che servono al tuo team.</li>
        <li><strong>MVP e funzionalità su misura</strong> per startup che devono arrivare sul mercato e imparare in fretta.</li>
        <li><strong>Frontend e backend insieme</strong>, così interfaccia e servizi nascono come un unico sistema.</li>
        <li><strong>Componenti in C# o C++</strong>, quando il progetto li richiede.</li>
      </ul>
      <h2>A chi ci rivolgiamo</h2>
      <p>Alle startup che cercano supporto tecnico o devono costruire un MVP, alle piccole e medie imprese che vogliono software adatto ai propri processi e alle agenzie digitali che cercano sviluppatori esterni affidabili.</p>
      <h2>Come lavoriamo</h2>
      <p>Prima capiamo bene il problema, poi concordiamo cosa realizzare e cosa consegnare. Preferiamo soluzioni pratiche e facili da mantenere alla complessità fine a se stessa, e ti aggiorniamo per tutta la durata dello sviluppo.</p>""",
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
            "title": "Manutenzione software e debugging | BinaryBuilders",
            "desc": "Debugging, refactoring, ottimizzazione e nuove funzionalità su software esistente, più attività tecniche mirate all'interno di progetti più grandi.",
            "h1": "Manutenzione software e risoluzione dei problemi",
            "service": "Manutenzione software",
            "lede": "Mettiamo mano al software che già usi: lo analizziamo, lo correggiamo, lo riorganizziamo, lo rendiamo più veloce e lo estendiamo. Possiamo anche prendere in carico attività tecniche precise all'interno di progetti più grandi.",
            "body": """
      <h2>Cosa facciamo</h2>
      <ul>
        <li><strong>Debugging</strong> di bug, job che falliscono e integrazioni che hanno smesso di funzionare.</li>
        <li><strong>Refactoring</strong> per rendere il codice più facile da modificare, senza riscriverlo da zero.</li>
        <li><strong>Ottimizzazione delle prestazioni</strong> di servizi backend, database e org Salesforce.</li>
        <li><strong>Nuove funzionalità su codice esistente</strong>, rispettando le convenzioni già in uso.</li>
        <li><strong>Contratti di manutenzione</strong> per i sistemi che hanno bisogno di cure regolari.</li>
      </ul>
      <h2>A chi ci rivolgiamo</h2>
      <p>Alle aziende con software che funziona ma ha bisogno di attenzioni, e ai team di sviluppo o alle agenzie che cercano rinforzi per un lavoro ben definito.</p>
      <h2>Come lavoriamo</h2>
      <p>Prima di proporre modifiche leggiamo il codice che c'è, concordiamo cosa vuol dire "finito" e lasciamo il progetto più semplice da gestire di come l'abbiamo trovato.</p>""",
        },
    },
]

# Only facts from the company context: no clients, numbers or claims it does not state.
ABOUT = {
    "en": {
        "title": "About BinaryBuilders | Independent software team",
        "desc": "BinaryBuilders is an independent two-developer team combining enterprise engineering, modern web development, systems integration and business automation.",
        "h1": "About BinaryBuilders",
        "lede": "We are an independent software engineering team founded by two developers with professional experience in enterprise software, backend systems, frontend applications and business process automation.",
        "body": """
      <h2>Why we started</h2>
      <p>We created BinaryBuilders with one objective: help organizations solve real technical problems with reliable, maintainable and scalable software. We favour practical engineering, clear requirements and long-term maintainability over unnecessary complexity.</p>
      <h2>What we combine</h2>
      <p>Enterprise engineering, modern web development, systems integration and business automation. In practice that means Java and Spring Boot backends, React and Next.js applications, Salesforce development, and the integrations that connect them.</p>
      <h2>How we work</h2>
      <ul>
        <li><strong>Problem first.</strong> We understand the problem before proposing a solution.</li>
        <li><strong>Realistic scope.</strong> We agree on requirements and deliverables we can actually meet.</li>
        <li><strong>Maintainable code.</strong> Clean, tested and easy for your team to take over.</li>
        <li><strong>Reuse before rebuild.</strong> If an existing system does the job, we connect to it.</li>
        <li><strong>Clear communication</strong> throughout development, on new projects and existing codebases alike.</li>
      </ul>
      <h2>A small team, on purpose</h2>
      <p>We are two engineers, not a large consultancy. You talk directly with the people writing the code, ownership is clear and delivery stays focused. We work best on clearly scoped projects, technical integrations, targeted development tasks and ongoing maintenance, either directly with companies or as subcontractors for agencies and consulting partners.</p>
      <h2>The team</h2>
      <ul class="more-list">
        <li><a href="/giuseppe-scappaticci">Giuseppe Scappaticci</a></li>
        <li><a href="/michele-sabatino">Michele Sabatino</a></li>
      </ul>""",
    },
    "it": {
        "title": "Chi siamo | BinaryBuilders",
        "desc": "BinaryBuilders è uno studio indipendente di due sviluppatori: software enterprise, sviluppo web, integrazione tra sistemi e automazione dei processi.",
        "h1": "Chi siamo",
        "lede": "Siamo uno studio indipendente di sviluppo software, fondato da due sviluppatori con esperienza professionale su software enterprise, backend, frontend e automazione dei processi aziendali.",
        "body": """
      <h2>Perché esistiamo</h2>
      <p>Abbiamo fondato BinaryBuilders con un obiettivo semplice: aiutare le aziende a risolvere problemi tecnici concreti con software affidabile, facile da mantenere e pronto a crescere. Preferiamo soluzioni pratiche e requisiti chiari alla complessità inutile.</p>
      <h2>Cosa sappiamo fare</h2>
      <p>Mettiamo insieme sviluppo enterprise, web moderno, integrazione tra sistemi e automazione. In concreto: backend Java e Spring Boot, applicazioni React e Next.js, sviluppo Salesforce e tutto quello che serve per farli dialogare.</p>
      <h2>Come lavoriamo</h2>
      <ul>
        <li><strong>Prima il problema.</strong> Lo capiamo a fondo prima di proporre una soluzione.</li>
        <li><strong>Obiettivi realistici.</strong> Concordiamo requisiti e consegne che possiamo davvero rispettare.</li>
        <li><strong>Codice manutenibile.</strong> Pulito, testato e facile da prendere in mano per il tuo team.</li>
        <li><strong>Riusare prima di rifare.</strong> Se un sistema esistente funziona, ci colleghiamo a quello.</li>
        <li><strong>Comunicazione chiara</strong> per tutto il progetto, che si parta da zero o da codice già esistente.</li>
      </ul>
      <h2>Piccoli per scelta</h2>
      <p>Siamo due sviluppatori, non una grande società di consulenza. Parli direttamente con chi scrive il codice, sai sempre chi si occupa di cosa e il lavoro resta concentrato. Diamo il meglio su progetti ben definiti, integrazioni, sviluppi mirati e manutenzione continuativa, sia direttamente con le aziende sia in subappalto per agenzie e società di consulenza.</p>
      <h2>Il team</h2>
      <ul class="more-list">
        <li><a href="/it/giuseppe-scappaticci">Giuseppe Scappaticci</a></li>
        <li><a href="/it/michele-sabatino">Michele Sabatino</a></li>
      </ul>""",
    },
}

# Facts given by Giuseppe and Michele (2026-10-09). Written in the first person: each page is that person's own.
PEOPLE = [
    {
        "slug": "giuseppe-scappaticci", "name": "Giuseppe Scappaticci", "first": "Giuseppe",
        "github": "https://github.com/Leixien",
        "en": {
            "title": "Giuseppe Scappaticci | Software engineer, BinaryBuilders",
            "desc": "Giuseppe Scappaticci, co-founder of BinaryBuilders. Software engineer since 2021, previously a Salesforce and backend consultant at Accenture.",
            "lede": "I founded BinaryBuilders with Michele Sabatino. I have worked as a software engineer since 2021.",
            "background": "I worked as a consultant at Accenture, developing Salesforce solutions and backend services on enterprise projects. I bring that experience with CRM processes and the systems around them to BinaryBuilders.",
        },
        "it": {
            "title": "Giuseppe Scappaticci | Software engineer, BinaryBuilders",
            "desc": "Giuseppe Scappaticci ha fondato BinaryBuilders con Michele Sabatino. Nel software dal 2021, prima come consulente Salesforce e backend in Accenture.",
            "lede": "Ho fondato BinaryBuilders con Michele Sabatino. Lavoro nello sviluppo software dal 2021.",
            "background": "Ho lavorato in Accenture come consulente, sviluppando soluzioni Salesforce e servizi backend per progetti enterprise. In BinaryBuilders porto questa esperienza: i processi CRM e tutti i sistemi che ci girano intorno.",
        },
    },
    {
        "slug": "michele-sabatino", "name": "Michele Sabatino", "first": "Michele",
        "github": "https://github.com/mennenne",
        "en": {
            "title": "Michele Sabatino | Software engineer, BinaryBuilders",
            "desc": "Michele Sabatino, co-founder of BinaryBuilders. Working in software since 2021, from cybersecurity to Java development for companies in Campania.",
            "lede": "I founded BinaryBuilders with Giuseppe Scappaticci. I have worked in software since 2021.",
            "background": "I started my career in cybersecurity, then moved to Java development, working for two companies in Campania.",
        },
        "it": {
            "title": "Michele Sabatino | Software engineer, BinaryBuilders",
            "desc": "Michele Sabatino ha fondato BinaryBuilders con Giuseppe Scappaticci. Nel software dal 2021: prima la cybersecurity, poi lo sviluppo Java per aziende campane.",
            "lede": "Ho fondato BinaryBuilders con Giuseppe Scappaticci. Lavoro nel software dal 2021.",
            "background": "Ho iniziato nella cybersecurity, poi ho cambiato strada e ho cominciato a sviluppare in Java, lavorando per due aziende campane.",
        },
    },
]

PEOPLE_UI = {
    "en": {"background": "Background", "work": "At BinaryBuilders", "work_p": "{other} and I both work across every service we offer:",
           "langs": "Languages and location", "langs_p": "Italian (native) and English (C1). I am from Naples, Italy.",
           "links": "Profiles", "team": "The team"},
    "it": {"background": "Percorso", "work": "In BinaryBuilders", "work_p": "Con {other} ci occupiamo di tutti i servizi dello studio:",
           "langs": "Lingue e città", "langs_p": "Italiano madrelingua e inglese a livello C1. Sono di Napoli.",
           "links": "Profili", "team": "Il team"},
}


def person_path(lang, p):
    return UI[lang]["home"] + p["slug"]


def person_id(p):
    return f"{BASE}/{p['slug']}#person"

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
            "founder": [{"@type": "Person", "@id": person_id(p), "name": p["name"], "url": f"{BASE}/{p['slug']}", "sameAs": [p["github"]]}
                        for p in PEOPLE],
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
    <div class="meta">
      <p class="links"><a href="{ui["about"]}">{ui["about_label"]}</a> <a href="{ui["privacy"]}">Privacy</a></p>
      <p>&copy; 2026 BinaryBuilders</p>
    </div>
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


def about(lang):
    ui, p = UI[lang], ABOUT[lang]
    alternates = {l: UI[l]["about"] for l in UI}
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "url": BASE + ui["about"], "inLanguage": lang,
          "mainEntity": {"@id": f"{BASE}/#org"}}
    content = f"""      <h1>{p["h1"]}</h1>
      <p class="lede">{p["lede"]}</p>
{p["body"]}
      <section class="contact" aria-labelledby="contact-title">
        <h2 id="contact-title">{ui["contact_h"]}</h2>
        <p>{ui["contact_p"]}</p>
        {ctas(lang)}
      </section>"""
    return doc_page(lang, head(lang, p["title"], p["desc"], ui["about"], [JB, MARTIAN], None, alternates, ld),
                    alternates[ui["other"]], content)


def person(lang, p):
    ui, t, pu = UI[lang], p[lang], PEOPLE_UI[lang]
    path = person_path(lang, p)
    alternates = {l: person_path(l, p) for l in UI}
    other = next(q["first"] for q in PEOPLE if q is not p)
    ld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": BASE + path, "inLanguage": lang,
          "mainEntity": {"@type": "Person", "@id": person_id(p), "name": p["name"], "jobTitle": "Software engineer",
                         "worksFor": {"@id": f"{BASE}/#org"}, "sameAs": [p["github"]], "knowsLanguage": ["it", "en"]}}
    content = f"""      <p class="crumb"><a href="{ui["home"]}">BinaryBuilders</a> / <a href="{ui["about"]}">{ui["about_label"]}</a></p>
      <h1>{p["name"]}</h1>
      <p class="lede">{t["lede"]}</p>
      <h2>{pu["background"]}</h2>
      <p>{t["background"]}</p>
      <h2>{pu["work"]}</h2>
      <p>{pu["work_p"].format(other=other)}</p>
      {services_list(lang)}
      <h2>{pu["langs"]}</h2>
      <p>{pu["langs_p"]}</p>
      <h2>{pu["links"]}</h2>
      <ul class="more-list">
          <li><a href="{p["github"]}" rel="me">GitHub</a></li>
        </ul>
      <section class="contact" aria-labelledby="contact-title">
        <h2 id="contact-title">{ui["contact_h"]}</h2>
        <p>{ui["contact_p"]}</p>
        {ctas(lang)}
      </section>"""
    return doc_page(lang, head(lang, t["title"], t["desc"], path, [JB, MARTIAN], None, alternates, ld),
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
    urls.append(write(ui["about"], about(lang)))
    for p in PEOPLE:
        assert len(p[lang]["title"]) <= 60 and len(p[lang]["desc"]) <= 160, (p["slug"], lang, len(p[lang]["title"]), len(p[lang]["desc"]))
        urls.append(write(person_path(lang, p), person(lang, p)))
    urls.append(write(ui["privacy"], privacy(lang)))
    write(ui["home"] + "404", not_found(lang))  # served by Cloudflare for unknown paths, not listed in the sitemap

(PUBLIC / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls)
    + "</urlset>\n"
)
print("\n".join(urls))

# WBSO AI Agent Architectuur

Dit document beschrijft de architectuur van de WBSO AI Agent, een tool ontworpen om te assisteren bij het invullen van WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) aanvraagformulieren voor software ontwikkelingsprojecten.

## 1. Architecturale Doelen

De primaire architecturale doelen voor dit project zijn:

- **Modulariteit:** Ontwerp componenten met duidelijke verantwoordelijkheden en interfaces om onafhankelijke ontwikkeling, testen en onderhoud mogelijk te maken.
- **Uitbreidbaarheid:** Maak toekomstige verbeteringen mogelijk, zoals het ondersteunen van verschillende formuliertypen of integratie met andere LLM's.
- **Nauwkeurigheid:** Zorg voor hoge precisie bij PDF-parsing, veldmatching en informatie-extractie.
- **Efficiëntie:** Optimaliseer voor redelijke verwerkingstijden, vooral voor PDF-parsing en LLM-interacties.
- **Onderhoudbaarheid:** Volg duidelijke codeerstandaarden en zorg voor uitgebreide documentatie.

## 2. Kerncomponenten

Gebaseerd op het projectoverzicht en de structuur zoals beschreven in `README.md`, zal het systeem bestaan uit de volgende kerncomponenten:

### 2.1. PDF Verwerking (`src/pdf/`)

Dit component is verantwoordelijk voor het verwerken van PDF-documenten.

- **`parser.py` (PDF Parser):**
  - **Verantwoordelijkheid:** PDF-bestanden laden, invulbare formuliervelden identificeren en hun eigenschappen extraheren (bijv. naam, type, locatie). Het kan ook nodig zijn om nabijgelegen tekst te extraheren die dient als de vraag of het label voor een veld.
  - **Keuzes:** Gebruik gevestigde Python-bibliotheken voor PDF-manipulatie (bijv. `PyPDF2`, `pdfminer.six`, of mogelijk meer gespecialiseerde bibliotheken voor formulierextractie zoals `pdfforms`). De keuze hangt af van de complexiteit van de WBSO-formulieren en het vereiste detailniveau.
- **`matcher.py` (Veldmatcher):**
  - **Verantwoordelijkheid:** Geïdentificeerde PDF-formuliervelden intelligent matchen met hun overeenkomstige semantische betekenis of vraagcontext. Dit kan regelgebaseerde logica, heuristieken gebaseerd op nabijheid en trefwoorden, of zelfs een lichtgewicht ML-model omvatten als eenvoudige matching onvoldoende is. Het zal ook invoergegevenstypen en beperkingen bepalen.
  - **Keuzes:** Begin met heuristische matching. Als de nauwkeurigheid onvoldoende is, onderzoek dan fuzzy string matching of eenvoudige NLP-technieken.

### 2.2. LLM Integratie (`src/llm/`)

Dit component beheert alle interacties met het Large Language Model.

- **`client.py` (LLM Client):**
  - **Verantwoordelijkheid:** Een gestandaardiseerde interface bieden voor communicatie met de gekozen LLM (aanvankelijk een lokale LLM). Dit omvat het verzenden van prompts en het ontvangen van gestructureerde antwoorden. Het moet API-aanroepen, nieuwe pogingen en foutafhandeling beheren.
  - **Keuzes:** Ontwerp een generieke clientinterface die kan worden aangepast als de onderliggende LLM verandert. Zorg voor robuuste foutafhandeling en mogelijk configureerbare parameters (bijv. temperatuur, max tokens).
- **`prompts.py` (Prompt Templates):**
  - **Verantwoordelijkheid:** Templates opslaan en beheren voor het genereren van specifieke prompts voor de LLM. Deze prompts zullen de LLM begeleiden bij het extraheren van gestructureerde informatie uit de context van formuliervelden en het genereren van passende antwoorden.
  - **Keuzes:** Gebruik een templating engine (bijv. Jinja2) als prompts complex worden. Prompts moeten versiebeheerd en gemakkelijk bij te werken zijn.

### 2.3. Hulpprogramma's (`src/utils/`)

Dit component zal gedeelde functionaliteiten bevatten die door andere modules worden gebruikt.

- **`validators.py` (Invoervalidatie):**
  - **Verantwoordelijkheid:** De door de LLM geëxtraheerde of door een gebruiker ingevoerde gegevens (indien van toepassing in toekomstige versies) valideren aan de hand van verwachte gegevenstypen en beperkingen die door `matcher.py` zijn geïdentificeerd.
  - **Keuzes:** Implementeer een flexibel validatieraamwerk dat verschillende gegevenstypen en regels aankan.

## 3. Gegevensstroom

De algemene gegevensstroom zal als volgt zijn:

1.  **Invoer:** Een WBSO PDF-formulier wordt aan het systeem aangeboden.
2.  **PDF Parsing (`parser.py`):** De PDF wordt geparst om formuliervelden en bijbehorende tekst te identificeren.
3.  **Veldmatching (`matcher.py`):** Ruwe veldinformatie wordt verwerkt om de semantische betekenis, het gegevenstype en de beperkingen voor elk relevant veld te begrijpen.
4.  **Promptgeneratie (`prompts.py` & `llm/client.py`):** Voor elk veld (of groep gerelateerde velden) wordt een specifieke prompt gegenereerd met behulp van templates en de context afgeleid van de PDF.
5.  **LLM Interactie (`llm/client.py`):** De gegenereerde prompt wordt naar de LLM gestuurd.
6.  **Informatie-extractie & Structurering:** De LLM verwerkt de prompt en retourneert een gestructureerde uitvoer (bijv. JSON) die de informatie bevat die nodig is om het formulierveld in te vullen.
7.  **Validatie (`validators.py`):** De geëxtraheerde informatie wordt gevalideerd.
8.  **Uitvoer:** De gevalideerde, gestructureerde informatie wordt beschikbaar gesteld (bijv. om het formulier vooraf in te vullen of voor beoordeling).

## 4. Architecturale Keuzes & Overwegingen

- **Programmeertaal:** Python, zoals aangegeven door de projectstructuur en `pyproject.toml`.
- **Lokale LLM Integratie:** De initiële focus ligt op integratie met een lokale LLM. Dit impliceert dat de mogelijkheden en API van de LLM een belangrijke factor zullen zijn in het ontwerp van `llm/client.py` en `llm/prompts.py`.
- **Modulariteit:** De gekozen projectstructuur (scheiding van `pdf`, `llm`, `utils`) ondersteunt modulariteit. Duidelijke interfaces tussen deze modules zullen cruciaal zijn.
- **Testen:** Een uitgebreide testsuite (`tests/`) is gepland, wat essentieel is voor het waarborgen van de betrouwbaarheid van elk component, met name `parser.py`, `matcher.py`, en de LLM-interactielogica.
- **Configuratie:** Overweeg hoe LLM-eindpunten, API-sleutels (indien aanwezig voor lokale LLM's), en andere configureerbare parameters zullen worden beheerd (bijv. omgevingsvariabelen, configuratiebestanden).
- **Foutafhandeling:** Robuuste foutafhandeling is nodig bij elke stap, vooral bij PDF-parsing (beschadigde bestanden, ongebruikelijke formaten) en LLM-interacties (API-fouten, onverwachte antwoorden).

## 5. Implementatieplan (Hoog-niveau Stappen)

Om tot een efficiënte en effectieve implementatie te komen, wordt de volgende gefaseerde aanpak aanbevolen:

1.  **Fase 1: Kern PDF Parsing & Basis Matching**

    - Implementeer `pdf/parser.py`: Focus op het betrouwbaar extraheren van velden en hun directe tekstlabels uit voorbeeld WBSO PDF-formulieren.
    - Implementeer basis `pdf/matcher.py`: Begin met eenvoudige regelgebaseerde of trefwoordgebaseerde matching voor veelvoorkomende velden.
    - Ontwikkel initiële unit tests voor parsing en basis matching.

2.  **Fase 2: LLM Integratie & Basis Prompting**

    - Zet de lokale LLM-omgeving op.
    - Implementeer `llm/client.py`: Breng communicatie tot stand met de lokale LLM.
    - Ontwikkel initiële `llm/prompts.py`: Creëer eenvoudige prompts om informatie te extraheren voor enkele kernvelden op basis van de output van Fase 1.
    - Integreer de PDF-verwerkingsoutput met de LLM-client om een end-to-end flow te bereiken voor een kleine subset van velden.
    - Ontwikkel initiële integratietests.

3.  **Fase 3: Geavanceerde Matching & Prompt Engineering**

    - Verbeter `pdf/matcher.py`: Verhoog de matchingnauwkeurigheid met behulp van meer geavanceerde heuristieken of technieken indien nodig. Adresseer identificatie van gegevenstypen en beperkingen.
    - Verfijn `llm/prompts.py`: Ontwikkel meer geavanceerde en robuuste prompt templates voor een breder scala aan velden en vraagtypen. Focus op het verkrijgen van gestructureerde output.
    - Implementeer `utils/validators.py` en integreer validatie in de workflow.

4.  **Fase 4: Iteratie, Testen & Verfijning**

    - Test grondig met een verscheidenheid aan WBSO-formulieren.
    - Itereer op alle componenten op basis van testresultaten en feedback.
    - Breid testdekking uit, inclusief edge cases.
    - Focus op het verbeteren van nauwkeurigheid, efficiëntie en robuustheid.

5.  **Fase 5: Documentatie & Packaging**
    - Finaliseer alle documentatie, inclusief `README.md`, `architecture.md`, en `api.md` (indien van toepassing).
    - Zorg ervoor dat code-level documentatie (docstrings) compleet is en voldoet aan de standaarden.
    - Bereid het project voor op eenvoudiger gebruik of implementatie indien nodig.

Dit plan benadrukt een incrementele aanpak, wat vroege feedback en continue verbetering gedurende de ontwikkelingslevenscyclus mogelijk maakt, in lijn met de AI-ondersteunde codeeraanpak vermeld in de `README.md`.

# WBSO AI Agent

Dit project implementeert een AI Agent om te assisteren bij het invullen van WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) aanvraagformulieren voor software ontwikkelingsprojecten.

## 1. Projectoverzicht

De WBSO AI Agent is ontworpen om:

- PDF-formulieren te parsen om invoervelden te identificeren
- Invoervelden te matchen met vraagtekstblokken en context
- Invoergegevenstypen en beperkingen te bepalen
- Gestructureerde output te extraheren met behulp van een LLM
- Specifieke prompts te genereren voor formuliervragen
- Te integreren met een lokale LLM

## 2. Projectstructuur

```
WBSO/
├── README.md                 # Dit bestand
├── pyproject.toml           # Projectconfiguratie en afhankelijkheden
├── LICENSE                  # Licentiebestand
├── .pre-commit-config.yaml  # Configuratie pre-commit hooks
├── src/                      # Broncode
│   ├── __init__.py
│   ├── pdf/                  # PDF-verwerkingsmodules
│   │   ├── __init__.py
│   │   ├── parser.py        # PDF-parsefunctionaliteit
│   │   └── matcher.py       # Logica voor veldmatching
│   ├── llm/                  # LLM-integratie
│   │   ├── __init__.py
│   │   ├── client.py        # LLM-clientimplementatie
│   │   └── prompts.py       # Prompt templates
│   └── utils/               # Hulpfuncties
│       ├── __init__.py
│       └── validators.py    # Invoervalidatie
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_matcher.py
│   └── test_llm.py
└── docs/                    # Documentatie
    ├── architecture.md      # Systeemarchitectuur
    └── api.md              # API-documentatie
```

## 3. Ontwikkelingsaanpak

Dit project volgt de AI-ondersteunde codeeraanpak zoals uiteengezet in [Full Process for Coding with AI Coding Assistants](https://docs.google.com/document/d/12ATcyjCEKh8T-MPDZ-VMiQ1XMa9FUvvk2QazrsKoiR8/edit?usp=sharing).

Kernaspecten van het ontwikkelingsproces:

1. Duidelijke probleemdefinitie en verzamelen van vereisten
2. Incrementele ontwikkeling met AI-assistentie
3. Regelmatig testen en valideren
4. Documentatiegestuurde ontwikkeling
5. Continue integratie en implementatie

## 4. Aan de slag

1. Kloon de repository
2. Installeer de uv package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Creëer een virtuele omgeving en installeer afhankelijkheden:
   ```bash
   uv venv
   source .venv/bin/activate  # Op Windows: .venv\Scripts\activate
   uv sync  # voor initiële setup
   uv pip install -e ".[dev]"  # Installeer package in bewerkbare modus met dev-afhankelijkheden
   ```
4. Stel pre-commit hooks in:
   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

## 5. Bijdragen

TODO: Richtlijnen voor bijdragen zullen worden toegevoegd in CONTRIBUTING.md. Neem voorlopig contact op met de projectbeheerder voor bijdragerichtlijnen.

## 6. Licentie

Dit project is gelicentieerd onder de MIT-licentie met beperkingen voor commercieel gebruik. Zie het [LICENSE](LICENSE) bestand voor details.

Commercieel gebruik van deze software vereist expliciete toestemming van de auteur. Neem voor commerciële licentievragen contact op met de projectbeheerder.

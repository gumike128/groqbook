![Licencia](https://img.shields.io/badge/license-MIT-green)

# Groqbook: Generuj celé knihy v sekundách pomocou Groq a Llama3

Groqbook je aplikácia streamlit, ktorá umožňuje generovať knihy na jeden riadok promptu pomocou Llama3 na Groq. Skvele funguje na literatúre faktu a každú kapitolu generuje v priebehu sekúnd. Aplikácia kombinuje rýchlosť Llama3-8b a kvalitu Llama3-70b.

[Demo Groqbooku](https://github.com/Bklieger/groqbook/assets/62450410/3adb11cd-8264-4289-a28a-49dc5b3cf453)
> Ukážka rýchlej generácie obsahu knihy pomocou Groqbooku

---

[Demo stiahnutia markdown knihy](https://github.com/Bklieger/groqbook/assets/62450410/5b0147fb-90f3-4584-8572-fa452545d833)
> Ukážka stiahnutia knihy vo formáte markdown

---

### Funkcie

- 📖 Strategické prepínanie medzi Llama3-70b a Llama3-8b pre rovnováhu medzi rýchlosťou a kvalitou
- 🖊️ Markdown štýlovanie pre estetickú prezentáciu knihy, tabuľky a kód
- 📂 Možnosť stiahnuť celú knihu ako textový súbor

### Príklady vygenerovaných kníh:

| Príklad                               | Prompt                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| [Základy LLM](Example_1.md)           |  Základy veľkých jazykových modelov                                                         |
| [Dátové štruktúry a algoritmy](Example_2.md) | Dátové štruktúry a algoritmy v Jave                                               |

---

## Rýchly štart

> [!DÔLEŽITÉ]
> Groqbook môžeš spustiť priamo na [groqbook.streamlit.app](https://groqbook.streamlit.app)  
> Prípadne aplikáciu spustíš aj lokálne podľa návodu nižšie.

### Webová verzia:

Použi [groqbook.streamlit.app](https://groqbook.streamlit.app)

### Lokálne spustenie:

#### Krok 1
Nastav si Groq API kľúč v premenných prostredia:

```
export GROQ_API_KEY=gsk_yA...
```

Tento krok je voliteľný, kľúč môžeš zadať aj neskôr v aplikácii.

#### Krok 2
Vytvor virtuálne prostredie a nainštaluj závislosti.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Krok 3
Spusti aplikáciu streamlit:

```
python3 -m streamlit run main.py
```

## Detaily

### Použité technológie

- Streamlit
- Llama3 na Groq Cloud

### Obmedzenia

Groqbook môže generovať nepresné informácie alebo dočasný obsah. Používaj na zábavné účely.

## Prispievanie

Vylepšenia cez pull requesty sú vítané!

# Markdown notatie

In verschillende invoervelden binnen de applicatie is het mogelijk om **Markdown** te gebruiken.
Met Markdown kun je tekst eenvoudig opmaken, zoals koppen, lijsten, links en codeblokken.

Onderstaand vind je een aantal **veelgebruikte voorbeelden** van wat er mogelijk is met Markdown.
Deze *cheat sheet* is bedoeld als snelle referentie.

Voor een volledige en uitgebreide uitleg van alle Markdown-functionaliteit, zie:
[Markdown guide](https://www.markdownguide.org/basic-syntax/)

---

## 1. Koppen

Gebruik `#` voor titels en secties:

```md
# Titel (h1)

## Subtitel (h2)

### Sub-subtitel (h3)
```

---

## 2. Nieuwe regels en regeleindes

In Markdown is een **nieuwe regel niet automatisch een nieuwe alinea**.

### Nieuwe alinea

Laat een **lege regel** tussen twee tekstblokken:

```md
Dit is de eerste alinea.

Dit is de tweede alinea.
```

### Regelafbreking binnen dezelfde alinea

Gebruik een backslash (`\`) aan het einde van de regel om expliciet een nieuwe regel af te dwingen:

```md
Dit is regel één\
Dit is regel twee
```

Dit kan handig zijn bij:

- adressen
- korte opsommingen
- vaste regelindelingen

Zonder backslash of lege regel worden regels vaak samengevoegd.

**Let op:** een backslash (`\`) is geen standaard Markdown-syntax.
Op veel plekken binnen Atlas werkt dit wel, maar dit is niet overal gegarandeerd.

Als dit niet werkt, kun je altijd **twee spaties aan het einde van de regel** gebruiken

```md
Dit is regel één␠␠
Dit is regel twee
```

---

## 3. Vet en cursief

```md
**Dit is vet**
*Dit is cursief*
```

---

## 4. Lijsten

Ongeordend:

```md
- Item 1
- Item 2
- Item 3
```

Geordend:

```md
1. Eerste
2. Tweede
3. Derde
```

---

## 5. Links

```md
[Linktekst](https://example.com)
```

---

## 6. Tabellen

```md
| Kolom 1 | Kolom 2 |
|--------|--------|
| Waarde | Waarde |
| Waarde | Waarde |
```

---

## 7. Horizontale lijn

```md
---
```
# AMZ-Scraper
Webscraping for Amazon

LEGGERE ATTENTAMENTE IL FILE README.md

Questo è uno script Python che utilizza la libreria BeautifulSoup per effettuare il web scraping dei risultati di ricerca sul sito Amazon.it in base ad una specifica parola chiave, e quindi inviare i dati dei prodotti (nome, prezzo, link di acquisto) al canale Telegram specificato, oltre che salvare i dati in un file CSV.

Il codice utilizza anche la libreria pyshorteners per accorciare i link dei prodotti, e prevede una ritardata di 30 secondi tra le richieste, per evitare il blocco dell'IP da parte di Amazon.

Inoltre, è possibile personalizzare il codice inserendo il token del proprio bot Telegram e l'ID del proprio canale, oltre al codice Amazon Affiliate, per guadagnare commissioni sulle vendite effettuate tramite i link di affiliazione.

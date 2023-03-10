# Introducció


Antecedents:

* A finals de 2022 es publica [un article de recerca](https://zakird.com/papers/toplists.pdf) on es conclou, que la manera més fiable per a determinar quins són els webs més populars al món, és usar la llista que publica Google dels llocs web que els usuaris tenen en memòria la cau del navegador Chrome. 
* El projecte https://github.com/zakird/crux-top-lists publica les dades compartides per Google en format CSV perquè siguin fàcils de consumir.

# Dades originals usades

Algunes característiques de les dades originals:

* Usem les [dades de desembre 2022](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv).
* Tingueu en compte que això no és una llista de webs, sinó de URLs. Per això algunes web, com gencat, apareixen diversos cops amb diferents subdominis (www.gencat.cat, salut.gencat, ruralcat.gencat.cat, etc).
* Inclouen només el primer 1 milió de llocs web més populars al món.
* No es proporciona un rànquing de posicions (1,2,3), sinó que els URL es classifiquen en grups dels primers 1000, 5000, etc. Dins d'aquests blocs, els URL no estan ordenats.

# Com volem usar aquestes dades?

Tenim dos objectius:

1) Ens agradaria contestar la pregunta: quins són els llocs web més populars del món existents en català?

2) Ens és útil disposar d'una llista de webs en català per poder baixar-les i obtenir en el futur tots els textos en català a Internet.

Qualsevol dada addicional és útil si ens ajuda a aportar noves perspectives d'on som com a comunitat de parlants, malgrat que no sigui 100% acurada.

# Què hem fet 

Filtrar la llista original perquè inclogui només els llocs que ofereixen el català. 

Per fer això ha calgut:
* Baixar els URLs (usant un [crawler](crawler.py)) i classificar-les segons la seva llengua

Cal considerar que:
* Al demanar els URL ens identifiquem com a parlants de català, així els llocs web multilingües ens ofereixen la versió en català.
* Per determinar la llengua visitem tots aquests llocs. Alguns URL no es poden consultar: alguns en el moment de visitar-los donen errors, altres tenen mecanismes per evitar els crawlers, etc. 
* Els mecanismes de detecció de llengua no són perfectes. Usem dos mecanismes diferents i només concloem una URL és en català si els dos coincideixen en aquesta predicció.

# Fitxers que compartim

## Llista de webs més populars del món en català

Recordeu que aquestes són les webs disponibles en català més populars del món (que és diferent que les webs en català més populars entre els catalanoparlants).

El fitxer [llocs_en_catala.txt](llocs_en_catala.txt) (feu clic per veure la llista completa). Aspecte que té (mostra parcial):

```
Primers 1000 llocs
 https://www.booking.com
 https://www.google.com
 https://www.facebook.com
 https://outlook.live.com
 https://twitter.com
 https://lichess.org
Primers 5000 llocs
 https://www.fcf.cat
 https://www.elnacional.cat
 https://www.blogger.com
... 
... 
... 

Nombre d'adreçes per domini de primer nivell: com: 178, cat: 141, es: 40, org: 38, net: 21, edu: 8, ad: 6, eu: 6, info: 4, io: 3, barcelona: 3, jp: 2, coop: 2, is: 1, fr: 1, store: 1, fi: 1, bar: 1, cz: 1, cloud: 1, social: 1, download: 1, film: 1, 
Nota: s'han analitzat les primeres 500000 URL de les 1000000 disponibles
```

Aquesta llista es genera amb l'aplicació [stats.py](stats.py).  Apliquem algunes regles d'ordenació que podeu revisar al codi. Per resumir-les:
* Es descarten els URL llistat al fitxer [falsos_positius.txt](falsos_positius.txt)
* Es descarten totes les URL que redirigeixen a un altre domini (per exemple, a google.com).
* Dins d'un mateix grup les adreces estan desordenades. Llavors donem preferència a les que comencen en www., són .cat, etc per mostrar primer les més comunes.
* Cada domini es mostra només un cop. Això vol dir que si hi ha https://www.google.com no mostrarem https://www.google.fi ja que són equivalents (i les dues contesten en català) o bé si tens https://www.facebook.com i https://mobile.facebook.com. Per això la regla anterior és important perquè és prioritizen més comunes dins del mateix grup.


## Fitxers de depuració

Si us pregunteu per què un lloc no s'ha identificat en català o no està inclòs en aquest llistat aquests fitxers els compartim per transparència:

Fitxer original de els URL:

* [202211.csv](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv) conté el milió d'URLs més populars al món.

La llista de URLs com a resultat del procés de *crawling* amb l'idioma identificat per URL:

* [urls.txt](crawling/urls.txt) conté tots els URLs que hem baixat amb la predicció de la llengua en què estan

I també el fitxer d'errors del *crawler* (pàgines que no ha pogut baixar, etc):

* [crawler_info.log.gz](crawling/crawler_info.log.gz) els errors produïts durant el procés de baixada de les pàgines

*Com a referència final, la gent del [Wiccac](http://wiccac.cat/) manté una llista de webs en català de forma manual.*



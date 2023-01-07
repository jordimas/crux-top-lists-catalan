# Introducció


Antecedents:

* A finals de 2022 es publica [un article de recerca](https://zakird.com/papers/toplists.pdf) on es conclou, que la manera més fiable per a determinar quins són els webs més populars al món, és usar la llista que publica Google dels llocs web que els usuaris tenen en memòria la cau del navegador Chrome. 
* El projecte https://github.com/zakird/crux-top-lists pública les dades compartides per Google en format CSV perquè siguin fàcils de consumir.

# Dades originals usades

Algunes característiques de les dades:

* Usem les [dades de desembre 2022](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv)
* Tingueu en compte que això no és una llista de webs, sinó de URLs. Per això algunes web, com gencat, apareixen diversos cops amb diferents subdominis (www.gencat.cat, salut.gentcat, ruralcat.gencat.cat, etc)
* Inclouen només el primer 1 milió de llocs web més populars al món
* No es proporciona un rànquing de posicions (1,2,3), sinó que els URL es classifiquen en grups dels primers 1000, 5000, etc. Dins d'aquests blocs, els URL no estan ordenats.

# Com volem usar aquestes dades?

Tenim dos objectius:

1) Ens agradaria contestar la pregunta:
* Quins són els llocs web més populars del món existents en català?

2) Ens és útil disposar d'una llista de webs en català per poder baixar-les i obtenir en el futur tots els textos en català a Internet.

Qualsevol dada addicional, malgrat que no sigui 100% acurada, és útil si ens ajuda a aportar noves perspectives d'on som com a comunitat de parlants. 

# Què hem fet 

Filtrar la llista original perquè inclogui només els llocs que ofereixen el català. 

Per fer això ha calgut:
* Baixar les URLs i classificar-les segons la seva llengua

Cal considerar que:
* Al demanar els URL ens identifiquem com a parlants de català, així els llocs multilingües ens ofereixen la versió en català.
* Per determinar la llengua visitem tots aquests llocs. Alguns URL no es poden consultar: alguns en el moment de visitar-los donen errors, altres tenen mecanismes per evitar els crawlers, etc. 
* Els mecanismes de detecció de llengua no són perfectes. Usem dos mecanismes diferents i només determinem que és en català si els dos donen aquesta predicció

# Fitxers que compartim

## Llista de webs més populars del món en català

El fitxer [llocs_en_catala.txt](llocs_en_catala.txt) conté el llistat de webs en català (creat amb l'aplicació [stats.py](stats.py)). Aquesta aplicació aplica algunes regles d'ordenació que podeu revisar al codi. Però bàsicament:
* Descartem els URL llistat al fitxer [falsos_positius.txt](falsos_positius.txt)
* Es descarten totes les URL que redirigeixen a un altre domini (per exemple, a google.com).
* Dins d'un mateix grup les adreces estan desordenades. Llavors donem preferència a les que comencen en wwww., són .cat, etc per mostrar primer les més comunes 
* Cada domini es mostra només un cop. Això vol dir que si hi ha https://www.google.com no mostrarem https://www.google.fi ja que són equivalent (i les dues contesten en català) o bé si tens https://www.facebook.com i https://mobile.facebook.com. Per això la regla anterior és important perquè és prioritizen més comunes dins del mateix grup.


## Fitxers de depuració

Si us pregunteu per què un lloc no s'ha identificat en català o no està inclòs en aquest llistat aquests fitxers els compartim per transparència:

Fitxer original de les URL:

* [202211.csv](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv) conté el milió d'URLs més populars al món.

La llista de URLs com a resulat del procés de *crawling* amb l'idioma identificat per URL:

* [urls.txt](crawling/urls.txt) conté tots els URLs que hem baixat amb la predicció de la llengua en què estan

I també el fitxer d'errors del *crawler* (pàgines que no ha pogut baixar, etc):

* [crawler_info.log.gz](crawling/crawler_info.log.gz) els errors produïts durant el procés de baixada de les pàgines

*Com a referència final, la gent del [Wiccac](http://wiccac.cat/) manté una llista de webs en català.*



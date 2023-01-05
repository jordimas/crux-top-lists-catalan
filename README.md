

# Introducció


Antecedents:

* A finals de 2022 es pubica [un article de recerca](https://zakird.com/papers/toplists.pdf) on es conclou, que la manera més fiable per a determinar quins són els webs més populars al món, és usar la llista que publica Google dels llocs web que els usuaris tenen en memòria la cau del navegador Chrome. 
* El projecte https://github.com/zakird/crux-top-lists pública les dades compartides per Google en format CSV perquè siguin fàcils de consumir.

# Dades originals usades

Algunes característiques de les dades:

* Usem les [dades de desembre 2022](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv)
* Tingueu en compte que això no és una llista de webs, sinó de URLs. Per això algunes web, com gencat, apareix diversos cops amb diferents subdominis (www.gencat.cat, salut.gentcat, ruralcat.gencat.cat, etc)
* Inclouen només el primer 1 milió de llocs web més populars al món
* No es propociona un ranking rànquing (1,2,3) sinó que els URL es classifiquen en grups dels primers 1000, 5000, etc. Dins d'aquests blocs, els URL no estan ordenats

# Com volem usar aquestes dades?

Tenim dos objectius:

1) Ens agradaria contestar les següents preguntes:
* Quins són els llocs web més populars en català?
* Quin percentatge usen domini .cat?

2) Ens és útil disposar d'una llista de webs en català per poder baixar-les i obtenir en el futur tots els textos en català a Internet.

Qualsevol dada addicional, malgrat que no sigui 100% acurada, és útil si ens ajuda a aportar noves perspectives d'on som com a comunitat de parlants. 

# Què hem fet 

Filtrar la llista original perquè inclogui només els llocs que ofereixen el català. 

Per fer això ha calgut:
* Baixar 1 milió d'URLs i classificar-les segons la seva llengua

Cal considerar que:
* Al demanar els URL ens identifiquem com a parlants de català, el que fa que molts llocs multingües ens ofereixen la versió en català
* Per determinar la llengua visiten tots aquests llocs. Alguns en el moment de visitar-los donen errors, altres no són amables amb els automatismes de baixada, etc. Alguns URL no es poden consultar.
* Els mecanismes de detecció de llengua no són perfectes. Usem dos mecanismes diferents i només determinem que és en català si el dos donen aquesta predicció

# Fitxers que compartim

El fitxer [llocs_en_catala.txt](llocs_en_catala.txt) conté el llistat de webs en català (creat amb l'aplicació [stats.py](stats.py))

Si us pregunteu perquè un lloc no s'ha identificat en català o no està inclòs aquí teniu els fitxers amb l'idioma identificat a cada pàgina:

* [urls.txt](crawling/urls.txt) conté tots els URLs que hem baixat amb la predicció de la llengua en què estan

I també el fitxer d'errors del crawler (pàgines que no ha pogut baixar, etc)

* [crawler-error.log](crawling/crawler-error.log) els errors produïts durant el procés de baixada de les pàgines

*Com a referència final, la gent del [Wiccac](http://wiccac.cat/) manté una llista de webs en català.*







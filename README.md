

# Introducció


Antecedents:

* Basant-se en [recerca recent](https://zakird.com/papers/toplists.pdf) es determina que la llista del navegador Chrome de llocs web en memòria cau és la manera més sòlida per a entendre quins són els web més populars al món
* El projecte https://github.com/zakird/crux-top-lists pública les dades compartides per Google en format CSV perquè siguin fàcils de consumir

# Les dades

* Aquestes són les [dades de desembre 2022](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv)
* No és propociona un ranking acurat (1,2,3) sinó que els llocs web es classifiquen en primers 1000, 5000, etc. Dins d'aquests blocs, els URL no estan ordenats
* Tingueu en compte que això no és una llista de webs, sinó de URLs. Per això algunes web com gencat apareix diversos cops amb diferents subdominis. 

# Objectiu

Ens agradaria contestar dues preguntes:
* Quin són els llocs web més populars en català?
* Quin percentatge usen domini .cat? 

# Què hem fet 

Crear una llista filtrada (de moment primers 50.000 llocs) que inclogui els llocs que ofereixen el català per entendre com s'aplica aquesta popularitat en la nostra realitat.

Cal considerar que:
* Per determinar la llengua visiten tots aquests llocs. Alguns en el moment de visitar-los donen errors, altres no són amables amb els automatismes de baixada, etc. Alguns no es poden consultar. Veure el log d'errors
* Els mecanismes de detecció de llengua no són perfectes. Usen dos mecanismes diferents i només determinem que és en català si el dos donen aquesta predicció
* Addicionalment alguns lloc webs cal demanar explícitament el català o seleccionar-ho, aquests no els considerem de moment.

# Reflexions

* Les dades originals tenen alguns resultats sorprenents, com ara veure https://www.xapes.net o https://www.basquetcatala.cat al mateix nivell que els diaris digitals. 
* Qualsevol dada addicional, malgrat que no sigui 100% acurada, és útil si ens ajuda a aportar noves perspectives d'on som com a comunitat de parlants

# Fitxers

El fitxer [llocs_en_catala.txt](llocs_en_catala.txt) conté el llistat de webs en català (creat amb [stats.py](stats.py))

Si us pregunteu perquè un lloc no s'identificat en català o no està inclòs aquí teniu els fitxers amb l'idioma identificat a cada pàgina:

* [urls.txt](crawling/urls.txt) conté tots els URLs que hem baixat amb la predicció de la llengua en que estan

I també el fitxer d'errors del crawler (pàgines que no ha pogut baixar, etc)

* [crawler-error.log](crawling/crawler-error.log) els errors produïts durant el procés de baixada de les pàgines

*Com a referència final, la gent del [Wiccac](http://wiccac.cat/) manté una llista de webs en català.*


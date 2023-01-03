

# Introduccció


Antecents:

* Basant-se en [recerca recent](https://zakird.com/papers/toplists.pdf) es determina que la llista del navegador Chrome de llocs en memòria cau és la manera més sòlida per a entendre quins són les web més populars al món
* El projecte https://github.com/zakird/crux-top-lists pública les dades compartides per Google en format CSV perquè siguin fàcils de consumir


# Les dades

* Aquestes són les [dades de desembre 2022](https://raw.githubusercontent.com/jordimas/crux-top-lists-catalan/main/data/202211.csv)
* No és propociona un ranking acurat (1,2,3) sinó que els llocs web es classifiquen en primers 1000, 5000, etc. Dins d'aquests blocs, les URL no estan ordenats

# Objectiu

Ens agradaria contestar dues preguntes:
* Quin són els llocs web més populars en català?
* Quin percentatge usen domini .cat? 

# Què hem fet 

Crear una llista filtrada (de moment primers 50.000 llocs) que inclogui els llocs que ofereixen el català per entendre com s'aplica aquesta popularitat en la nostra realitat.

Cal considerar que:
* Per determinar la llengua visiten tots aquests llocs. Alguns en el moment de visitar-los donen errors, altres no són amables amb els automatimes de baixada, etc. Alguns no es poden consultar. Veure el log d'errors
* El mecanisme de detecció de llengua no és perfecte. En alguns casos dóna falsos positius (que filtrem) i alguns falsos negatius que ignorem
* Addicionalment alguns lloc webs cal demanar explícitament el català o seleccionar-ho, aquests no els considerem de moment.

# Fitxer

* [llocs_en_catala.txt](llocs_en_catala.txt) conté el filtrat de llistats en català







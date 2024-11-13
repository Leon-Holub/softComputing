## Analýza clusteringu pro segmentaci uživatelů kreditních karet

Cílem tohoto projektu bylo využít dvou populárních algoritmů clusteringu, K-MEANS a DBSCAN, k segmentaci uživatelů kreditních karet. Dataset obsahoval různé parametry o uživatelích, jako jsou zůstatky na účtech, počty nákupů, částky čerpané přes cash advance a frekvenci nákupů. Analýza se zaměřila na rozpoznání a charakterizaci různých skupin uživatelů na základě těchto dat.

## K-MEANS Clustering

Prvním krokem bylo určení optimálního počtu clusterů pro algoritmus K-MEANS. Pro tento účel jsme použili Silhouette Score, který ukázal, že nejlepší počet clusterů je dva. Na následujícím obrázku je vidět průběh hodnot Silhouette Score pro různé počty clusterů, přičemž hodnota pro dva clustery dosahuje nejvyšší hodnoty (0.48).

![Silhouette Score](silhouetteScore.png)

Po aplikaci algoritmu K-MEANS jsme rozdělili uživatele do dvou skupin. První skupina zahrnuje uživatele označené jako "Balanced Spenders & Savers", kteří mají vyvážené finanční návyky, a druhá skupina představuje "Cash Advance Users", tedy uživatele s vysokým využíváním cash advance. Následující obrázek zobrazuje rozložení těchto dvou clusterů.

![K-MEANS Clustering](kMeans.png)

Charakteristika clusterů:

**Cluster 0 (Cash Advance Users - 1):**

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 1364.000   | 1364.000     | 1364.000            |
| mean        | 5258.039   | 1571.999     | 4154.463            |
| std         | 2626.613   | 4104.559     | 3701.171            |
| min         | 78.115     | 0.000        | 0.000               |
| 25%         | 3381.587   | 0.000        | 1942.024            |
| 50%         | 4981.819   | 228.400      | 3510.742            |
| 75%         | 6600.153   | 1394.248     | 5409.624            |
| max         | 19043.139  | 49039.570    | 47137.212           |

**Cluster 1 (Balanced Spenders & Savers - 1):**

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 7586.000   | 7586.000     | 7586.000            |
| mean        | 900.354    | 900.933      | 407.884             |
| std         | 988.826    | 1513.307     | 766.723             |
| min         | 0.000      | 0.000        | 0.000               |
| 25%         | 87.196     | 64.820       | 0.000               |
| 50%         | 551.378    | 379.660      | 0.000               |
| 75%         | 1393.028   | 1084.843     | 462.266             |
| max         | 5315.946   | 22746.810    | 5291.769            |

## DBSCAN Clustering

Pro algoritmus DBSCAN jsme nemuseli předem stanovovat počet clusterů. Namísto toho jsme využili vzdálenost k pátému nejbližšímu sousedovi a pomocí tzv. "elbow rule" jsme určili vhodnou hodnotu parametru ϵ (eps). Optimální hodnota eps byla určena jako 0.3747, jak je vidět na následujícím grafu.

![Optimal Value for Eps](elbow.png)

Výsledky DBSCAN clusteringu ukázaly, že algoritmus nalezl sedm clusterů a také odhalil šum (outliers). Na obrázku níže jsou jednotlivé clustery vizualizovány a popsány, například "Balanced Spenders & Savers", "Heavy Spenders" nebo "Cash Advance Users".

![DBSCAN Clustering](dbscan_0.37469118099227106.png)

Charakteristika DBSCAN clusterů:

**Cluster 0 (Balanced Spenders & Savers - 1):**

Tento cluster zahrnuje uživatele s vyváženým chováním při používání kreditních karet. Mají relativně nízký průměrný zůstatek (1141.25), menší průměrný objem nákupů (738.90), a také průměrnou hodnotu cash advance (611.35). Frekvence nákupů se liší, ale průměrná hodnota ukazuje spíše průměrnou aktivitu (611.35). Většina těchto uživatelů se jeví jako pečliví při správě svých financí a nevyužívají nadměrné úvěrové zatížení.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 8013.000   | 8013.000     | 8013.000            |
| mean        | 1141.245   | 738.897      | 611.353             |
| std         | 1410.746   | 1126.380     | 1150.281            |
| min         | 0.000      | 0.000        | 0.000               |
| 25%         | 97.300     | 19.910       | 0.083               |
| 50%         | 669.974    | 313.360      | 0.417               |
| 75%         | 1601.393   | 947.720      | 0.917               |
| max         | 9629.809   | 9751.900     | 8422.555            |

**Cluster 1 (Cash Advance Users - 1):**

Tento cluster zahrnuje uživatele, kteří velmi často využívají cash advance (průměr 9469.32), což naznačuje, že mohou mít vyšší potřebu hotovosti. Mají vysoký průměrný zůstatek (4505.39), ale jejich aktivita v nákupech je minimální (průměr 8.30). Tento profil může odrážet finanční potíže nebo preferenci pro přístup k hotovosti.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 10.000     | 10.000       | 10.000              |
| mean        | 4505.394   | 8.300        | 9469.319            |
| std         | 570.375    | 26.247       | 366.553             |
| min         | 3495.736   | 0.000        | 9003.085            |
| 25%         | 4193.478   | 0.000        | 9132.034            |
| 50%         | 4472.905   | 0.000        | 9496.438            |
| 75%         | 4844.177   | 0.000        | 9766.460            |
| max         | 5347.377   | 83.000       | 9968.185            |

**Cluster 2 (Heavy Spenders - 1):**

Tento cluster zahrnuje uživatele, kteří velmi často utrácejí velké částky (průměr nákupů 10977.96). Průměrný zůstatek je nižší (1034.59), ale uživatelé mají vysokou frekvenci nákupů (0.99), což značí, že tito uživatelé často používají svou kreditní kartu pro běžné výdaje a rádi maximalizují své výhody z nákupů.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 10.000     | 10.000       | 10.000              |
| mean        | 1034.593   | 10977.961    | 0.992               |
| std         | 179.484    | 442.537      | 0.026               |
| min         | 776.920    | 10243.480    | 0.917               |
| 25%         | 920.785    | 10702.765    | 1.000               |
| 50%         | 978.695    | 10909.295    | 1.000               |
| 75%         | 1192.707   | 11389.303    | 1.000               |
| max         | 1311.732   | 11522.900    | 1.000               |

**Cluster 3 (Cash Advance Users - 3):**

Tento cluster se skládá z uživatelů s vysokým průměrným zůstatkem (5751.28), kteří také hojně využívají cash advance (průměr 10093.27). V jejich nákupní aktivitě je vidět značná variabilita, ale obecně mají tendenci využívat své prostředky ve formě hotovosti namísto běžných nákupů.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 5.000      | 5.000        | 5.000               |
| mean        | 5751.283   | 12.942       | 10093.273           |
| std         | 209.128    | 28.939       | 437.876             |
| min         | 5422.456   | 0.000        | 9596.317            |
| 25%         | 5665.803   | 0.000        | 9799.530            |
| 50%         | 5861.101   | 0.000        | 9972.235            |
| 75%         | 5880.219   | 0.000        | 10507.873           |
| max         | 5926.838   | 64.710       | 10590.411           |

**Cluster 4 (Rich Savers - 1):**

Tento cluster obsahuje uživatele s vysokými zůstatky (průměr 3744.65) a nízkými nákupy (357.49). Tito uživatelé mají mírně vyšší aktivitu v cash advance (1539.55), ale spíše se jedná o spořivější jedince, kteří preferují uchovávání finančních prostředků namísto jejich častého utrácení.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 5.000      | 5.000        | 5.000               |
| mean        | 3744.647   | 357.486      | 1539.550            |
| std         | 279.190    | 124.340      | 169.202             |
| min         | 3347.230   | 207.000      | 1328.658            |
| 25%         | 3626.197   | 256.630      | 1428.188            |
| 50%         | 3743.771   | 368.440      | 1546.728            |
| 75%         | 3946.877   | 475.360      | 1634.030            |
| max         | 4059.160   | 480.000      | 1760.146            |

**Cluster 5 (Cash Advance Users - 2):**

Tento cluster zahrnuje uživatele s průměrně vysokým zůstatkem (3434.56) a vyšší průměrnou částkou cash advance (4589.81). Tito uživatelé se zdají být aktivní jak v oblasti nákupů (860.48), tak v čerpání hotovosti, což naznačuje vyvážený přístup mezi nákupy a potřebou přímého přístupu k hotovosti.

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 16.000     | 16.000       | 16.000              |
| mean        | 3434.560   | 860.475      | 4589.809            |
| std         | 297.649    | 315.831      | 503.383             |
| min         | 3086.120   | 230.000      | 3585.835            |
| 25%         | 3234.805   | 690.053      | 4303.917            |
| 50%         | 3334.820   | 910.345      | 4583.682            |
| 75%         | 3593.630   | 1123.265     | 5024.834            |
| max         | 4070.501   | 1307.160     | 5338.547            |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 8013.000   | 8013.000     | 8013.000            |
| mean        | 1141.245   | 738.897      | 611.353             |
| std         | 1410.746   | 1126.380     | 1150.281            |
| min         | 0.000      | 0.000        | 0.000               |
| 25%         | 97.300     | 19.910       | 0.083               |
| 50%         | 669.974    | 313.360      | 0.417               |
| 75%         | 1601.393   | 947.720      | 0.917               |
| max         | 9629.809   | 9751.900     | 8422.555            |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 10.000     | 10.000       | 10.000              |
| mean        | 4505.394   | 8.300        | 9469.319            |
| std         | 570.375    | 26.247       | 366.553             |
| min         | 3495.736   | 0.000        | 9003.085            |
| 25%         | 4193.478   | 0.000        | 9132.034            |
| 50%         | 4472.905   | 0.000        | 9496.438            |
| 75%         | 4844.177   | 0.000        | 9766.460            |
| max         | 5347.377   | 83.000       | 9968.185            |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 16.000     | 16.000       | 16.000              |
| mean        | 3434.560   | 860.475      | 4589.809            |
| std         | 297.649    | 315.831      | 503.383             |
| min         | 3086.120   | 230.000      | 3585.835            |
| 25%         | 3234.805   | 690.053      | 4303.917            |
| 50%         | 3334.820   | 910.345      | 4583.682            |
| 75%         | 3593.630   | 1123.265     | 5024.834            |
| max         | 4070.501   | 1307.160     | 5338.547            |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 10.000     | 10.000       | 10.000              |
| mean        | 1034.593   | 10977.961    | 0.992               |
| std         | 179.484    | 442.537      | 0.026               |
| min         | 776.920    | 10243.480    | 0.917               |
| 25%         | 920.785    | 10702.765    | 1.000               |
| 50%         | 978.695    | 10909.295    | 1.000               |
| 75%         | 1192.707   | 11389.303    | 1.000               |
| max         | 1311.732   | 11522.900    | 1.000               |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 5.000      | 5.000        | 5.000               |
| mean        | 3744.647   | 357.486      | 1539.550            |
| std         | 279.190    | 124.340      | 169.202             |
| min         | 3347.230   | 207.000      | 1328.658            |
| 25%         | 3626.197   | 256.630      | 1428.188            |
| 50%         | 3743.771   | 368.440      | 1546.728            |
| 75%         | 3946.877   | 475.360      | 1634.030            |
| max         | 4059.160   | 480.000      | 1760.146            |

| BALANCE     | PURCHASES  | CASH_ADVANCE | PURCHASES_FREQUENCY |
|-------------|------------|--------------|---------------------|
| count       | 5.000      | 5.000        | 5.000               |
| mean        | 5751.283   | 12.942       | 10093.273           |
| std         | 209.128    | 28.939       | 437.876             |
| min         | 5422.456   | 0.000        | 9596.317            |
| 25%         | 5665.803   | 0.000        | 9799.530            |
| 50%         | 5861.101   | 0.000        | 9972.235            |
| 75%         | 5880.219   | 0.000        | 10507.873           |
| max         | 5926.838   | 64.710       | 10590.411           |

## Shrnutí

Použití dvou algoritmů clusteringu, K-MEANS a DBSCAN, nám umožnilo rozdělit uživatele kreditních karet do různých segmentů na základě jejich nákupního chování a finančních návyků. Každý z algoritmů poskytl unikátní pohled na segmentaci – K-MEANS umožnil rozdělení uživatelů na předem daný počet kategorií, zatímco DBSCAN rozpoznal složitější a necentrické clustery a identifikoval i šum. Tato analýza poskytuje užitečné informace pro lepší porozumění potřebám jednotlivých skupin uživatelů a pro zacílení vhodných finančních produktů.


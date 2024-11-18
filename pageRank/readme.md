# PageRank algoritmus pro leonholub.cz

## Cíl
Cílem tohoto projektu bylo naimplementovat vlastní PageRank algoritmus, který Google používá pro řazení relevantních stránek, a otestovat jej na datasetu, který jsem vytvořil. Použil jsem k tomu stránku [leonholub.cz](https://leonholub.cz/), odkud jsem extrahoval odkazy a provedl jejich analýzu.

## Vstupní data
Vstupní data pocházejí ze stránky [leonholub.cz](https://leonholub.cz/). Následuje seznam odkazů, které byly z této stránky získány:

| URL |
|-----|
| https://www.linkedin.com/in/leon-holub-8a9b991b6/ |
| https://www.instagram.com/leonholub/ |
| https://www.facebook.com/leon.holub.5 |
| https://leonholub.cz/Prispevek/system-pro-spravu-autobazaru |
| https://leonholub.cz/Prispevek/doctus |
| https://leonholub.cz/Prispevek/ballgame |
| https://leonholub.cz/Prispevky |
| https://leonholub.cz/ |

## Postup
Nejprve jsem implementoval webcrawler, který extrahoval všechny odkazy z výchozí stránky `leonholub.cz` a následně provedl zanoření do hloubky 2, aby získal i odkazy z propojených stránek. Použil jsem knihovny `requests` a `BeautifulSoup` pro extrakci odkazů a `pandas` pro ukládání dat. Výsledná data jsem použil k vytvoření orientovaného grafu pomocí knihovny `networkx`, který reprezentuje vztahy mezi jednotlivými stránkami.

Na tento graf jsem aplikoval PageRank algoritmus, který iterativně vypočítal relativní důležitost každé stránky v síti. K výpočtu jsem použil 50 iterací.

## Zpracovaný dataset
Následující tabulka obsahuje 10 stránek s nejvyššími hodnotami PageRank. Každá hodnota PageRank určuje relativní důležitost stránky v rámci celé sítě stránek propojených s `leonholub.cz`.

| URL                                                         | PageRank |
|-------------------------------------------------------------|----------|
| https://www.linkedin.com/in/leon-holub-8a9b991b6/           | 0.040746 |
| https://www.instagram.com/leonholub/                        | 0.040746 |
| https://www.facebook.com/leon.holub.5                       | 0.040746 |
| https://leonholub.cz/Prispevky                              | 0.037823 |
| https://leonholub.cz/                                       | 0.019474 |
| https://leonholub.cz/Prispevek/system-pro-spravu-autobazaru | 0.019474 |
| https://leonholub.cz/Prispevek/doctus                       | 0.019474 |
| https://leonholub.cz/Prispevek/ballgame                     | 0.019474 |
| https://www.autobazardrabek.cz/                             | 0.018507 |
| https://ballgame.leonholub.cz/#stazeni                      | 0.018262 |

Zbytek datasetu je k dispozici v souboru [`pagerank_results.csv`](pagerank_results.csv).

## Závěr
Výstup byl vytvořen po 50 iteracích algoritmu PageRank, což mi poskytlo relativní hodnocení všech odkazovaných stránek. Výsledky jsem následně seřadil podle důležitosti. Nejvyšší hodnoty PageRank dosáhly stránky s významným množstvím externích odkazů a propojení s dalšími relevantními zdroji.
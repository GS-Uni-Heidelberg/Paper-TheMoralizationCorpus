# Statistics

## Annotation Data
- download from: [https://corpora.ids-mannheim.de/repo/moralization-corpus/](https://corpora.ids-mannheim.de/repo/moralization-corpus/)
- `testset_LREC2026.json` contains 1734 instances

## Split

- train(valid) : dev(valid) : test(valid) = 7816 : 1953 : 1734 = 0.7 : 0.15 : 0.15
  - because of re-annotation, this ratio is no more held!
- gerne and binary label (moralization / thematization) balanced

## Statistics

> Note:  
> `test` = test set w/o test-150

### contains moralization

|    |Moralization|Thematization|total|
|:--:|--:|--:|--:|
|train|1182|6634|7816|
|dev|294|1659|1953|
|test|489|1095|1584|
|test-150|49|101|150|
|all|2014|9489|11503|

### genre

|    |Leserbriefe|Sachbücher|Kommentare|Wikipedia_Diskussionen|Interviews|Plenarprotokolle|Gerichtsurteile|total|
|:--:|--:|--:|--:|--:|--:|--:|--:|--:|
|train|1057|1161|1229|1126|1261|1077|905|7816|
|dev|263|291|307|283|315|266|228|1953|
|test|203|241|249|224|259|214|194|1584|
|test-150|30|16|22|26|20|26|10|150|
|all|1553|1709|1807|1659|1855|1583|1337|11503|

### kat1_type

|    |Keine Moralisierung|Moralisierung explizit|Moralisierung interpretativ|Moralisierung Kontext|Moralisierung Weltwissen|Moralisierung fremde Stimme|Doppelung|total|
|:--:|--:|--:|--:|--:|--:|--:|--:|--:|
|train|6634|741|125|197|113|4|2|7816|
|dev|1659|177|39|47|31|0|0|1953|
|test|1095|209|105|92|74|9|0|1584|
|test-150|101|28|3|6|12|0|0|150|
|all|9489|1155|272|342|230|13|2|11503|

### kat2_moral_value

|    |Care|Harm|Fairness|Cheating|Loyality|Betrayal|Authority|Subversion|Purity|Degradation|Liberty|Opression|total|
|:--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|train|378|575|316|240|72|66|58|28|90|56|185|107|2171|
|dev|110|144|64|62|22|7|16|15|27|13|39|24|543|
|test|181|316|165|142|39|20|19|19|50|53|68|52|1124|
|test-150|24|46|23|11|5|13|3|1|6|9|5|3|149|
|all|693|1081|568|455|138|106|96|63|173|131|297|186|3987|

### kat3_protagonist role

|    |Forderer:in|Adressat:in|Benefizient:in|Malefizient:in|Bezug-unklar|total|
|:--:|--:|--:|--:|--:|--:|--:|
|train|495|717|718|19|234|2183|
|dev|129|176|178|6|58|547|
|test|189|366|380|127|129|1191|
|test-150|24|35|37|8|2|106|
|all|837|1294|1313|160|423|4027|

### kat3_protagonist group

|    |Individuum|Menschen|Institution|Soziale-Gruppe|OTHER|total|
|:--:|--:|--:|--:|--:|--:|--:|
|train|413|301|731|687|51|2183|
|dev|103|63|170|192|19|547|
|test|279|209|328|324|51|1191|
|test-150|19|14|49|19|5|106|
|all|814|587|1278|1222|126|4027|

### kat4_communicative_function

|    |Appell|Appell+Darstellung|Appell+Expression|Appell+Beziehung|total|
|:--:|--:|--:|--:|--:|--:|
|train|302|691|274|35|1302|
|dev|77|178|63|11|329|
|test|126|268|93|24|511|
|test-150|11|30|9|3|53|
|all|516|1167|439|73|2195|

### kat5_demand

|    |explicit|implicit|total|
|:--:|--:|--:|--:|
|train|648|534|1182|
|dev|158|136|294|
|test|235|254|489|
|test-150|28|21|49|
|all|1069|945|2014|

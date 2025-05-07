# Substancje lecznicze - baza danych

## Streszczenie

Skrypt instalacyjny tutułowej bazy. Jest to projekt końcowy z przedmiotu *Bazy danych*. Ściślej, jego tłumaczenie do *Pythona*, bo oryginał został napisany z myślą o TSQL.

## Spis spraw

1. [Instalacja bazy](#instalacja-bazy)
2. [Model E/R](#model-er)
3. [Model relacyjny](#model-relacyjny)
4. [Co dalej?](#co-dalej)
5. [Literatura](#literatura)

## Instalacja bazy

W celu powołania bazy do życia należy:
1. zainstalować ten pakiet;
2. zaimportować moduł `substances.database` w środowisku lub w powłoce Pythona;
3. wywołać funkcję `initialize`, np. `substances.database.initialize()`.

Następnie, w bieżącym katalogu pojawi się plik `substances.db`. Zapytania do bazy można wykonać z użyciem pakietu [sqlite3](https://docs.python.org/3/library/sqlite3.html) (swoją drogą ninejszy pakiet opiera się na tym linkowanym).

> ### Uwaga.
> SQLite nie wymusza zachowania więzów klucza obcego. Można to zmienić po nawiązaniu połączenia z bazą danych, np. w następujący sposób:
> 
> 1. import sqlite3 as sql
> 2. import substances.database as db
> 3. db.initialize()
> 4. con = sql.connect("substances.db")
> 5. con.execute("PRAGMA foreign_keys=1")
> 
> Zobacz [https://sqlite.org/pragma.html#pragma_foreign_keys](#https://sqlite.org/pragma.html#pragma_foreign_keys).

## Model E/R

Analiza została przeprowadzona z użyciem [[1]](#widom).

1. Atrybuty zbioru encji *Leki*
+ <u>bloz</u> - unikatowy kod nadawany każdej substancji leczniczej
+ <u>nazwaHandlowa</u>
+ <u>substancjaAktywna</u>
+ <u>postać</u> - postać leku (np. tabletki, syrop, itp.)
+ <u>dawka</u> - ilość substancji aktywnej w jednostce leku
+ OTC - lek wydawany bez recepty (*over the counter*)
+ zastosowanie
+ producent

2. Atrybuty zbioru encji *Producenci*
+ <u>nazwa</u>
+ <u>siedziba</u>
+ prezes
+ rokZałożenia

Atrybuty podkreślone stanowią elementy klucza lub kluczy.

<figure>
    <img src="diagram.png">
    <figcaption>Rys. 1 Diagram związków encji dla bazy danych substancji leczniczych wykonany przy pomocy <a href="draw.io">draw.io</a></figcaption>
</figure>

Na rysunku 1 są przedstawione dwa zbiory encji **Leki** oraz **Producenci** połączone związkiem binarnym **produkuje** typu *wiele-do-jeden*. Strzałka z zaokrąglonym grotem skierowana w stronę zbioru **Producenci** oznacza, że dla ustalonej encji ze zbioru **Leki** istnieje dokładnie jedna encja ze zbioru **Producenci**.

## Model relacyjny

Związek **produkuje** z modelu E/R jest *wiele-do-jeden* z **Leków** do **Producentów**, więc oba zbiory encji zostaną połączone w jedną relację, nazwijmy ją $R$, o schemacie:

$R(\mathrm{bloz,\ nazwaHandlowa,\ substancjaAktywna,\ postać,\ dawka,\ OTC,} \\[1ex] \mathrm{zastosowanie,\ producent,\ siedziba,\ prezes,\ rokZałożenia}).$

Wprowadźmy następujące oznaczenia:

$A \mapsto \mathrm{bloz}, \quad B \mapsto \mathrm{nazwaHandlowa}, \quad C \mapsto \mathrm{substancjaAktywna}, \\[2ex] D \mapsto \mathrm{postać}, \quad E \mapsto \mathrm{dawka}, \quad F \mapsto \mathrm{OTC}, \quad G \mapsto \mathrm{zastosowanie}, \\[2ex] H \mapsto \mathrm{producent}, \quad X \mapsto \mathrm{siedziba}, \quad Y \mapsto \mathrm{prezes}, \quad Z \mapsto \mathrm{rokZałożenia}.$

Zachodzą następujące zależności funkcyjne:

$A \to BC\dots HX\dots Z, \quad B \to ACD\dots HX\dots Z, \quad CDE \to ABFGHXYZ, \quad HX \to YZ.$

W relacji $R$ możemy wyróżnić trzy klucze:

$\{A\}, \quad \{B\}, \quad \{C, D, E\}.$

Zauważmy, że:

$\{H, X\}^+ = \{H, X, Y, Z\},$

co oznacza, że zależność funkcyjna $HX \to YZ$ narusza warunek BCNF. Relację $R$ rozbijamy na dwie relacje $R'$ oraz $R''$ o schematach:

$R'(A, B, C, D, E, F, G, H, X), \quad R''(H, X, Y, Z).$

Obie relację są teraz w BCNF.

## Co dalej?

+ Utworzenie funkcjonalności do instalowania bazy z poziomu terminala.

## Literatura
<a name="widom">[1]</a> H. Garcia-Molina, J.D. Ullman, J. Widom, *Systemy baz danych. Pełny wykład*, WNT, Warszawa, 2006.
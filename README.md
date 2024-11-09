# KUVAKE - kuvien arkistointityökalu

Kuvake on ohjelma, jolla voi siirtää kuvat esimerkiksi ulkoiselta muistikortilta haluttuun kansioon.
Se luo automaattisesti kansiorakenteen vuosille ja kuukausille.

Kuvake ei poista tai korvaa jo olemassa olevia kansioita tai kuvia kohdekansiosta. 

### Esimerkki:


```
Lähdekansio:
- 20230101.jpg
- 20230102.jpg
- 20230103.jpg
- 20230410.jpg
- 20240201.jpg
- 20240202.jpg 
```

```
(Tyhjä) kohdekansio tiedostosiirron jälkeen:

2023 (kansio)
    - 01 (kansio)
        - 20230101.jpg
        - 20230102.jpg
        - 20230103.jpg
    - 04 (kansio)
        - 20230410.jpg

2024 (kansio)
    - 02 (kansio)
        - 20240201.jpg
        - 20240202.jpg 
```
**HUOMIO!** 

- Kuvake ei (toistaiseksi) etsi tiedostoja alakansioista, 
eli siirrettävien tiedostojen on oltava kaikkien samassa kansiossa kuten esim. kameran muistikortilla. 
- Kuvakkeen toiminta perustuu (toistaiseksi) päivämäärälla alkaviin tiedostonimiin.




## Sisältö
- [Asennusohje](#asennusohje)
- [Käyttöohje](#käyttöohje)

---
## Asennusohje 
0. TBA

---

## Käyttöohje 
1. käynnistä Kuvake
2. tarkista lähde- ja kohdekansioiden sijainti
   - lähdekansio on oletusarvona tietokoneen D-levy, joka läppäreitä käyttäessä on yleensä muistikortti
   - kohdekansio on oletusarvoisesti käyttäjän oma Kuvat-kansio
3. valitse, poistetaanko kuvat lähdekansiosta (tekstiä voi klikata hiirellä valinnan muuttamiseksi)
4. paina OK
5. valmis!


### Näppäimistökäyttöohje

Kuvaketta voi myös käyttää melkein kokonaan ilman hiirtä. Tällöin Kuvake käynnistetään tavalliseen tapaan 
hiirellä, mutta ohjelmassa voi siirtyä napista toiseen Tab-näppäintä käyttämällä. 
Nappia painetaan välilyöntiä painamalla. Tämä toimii myös valittaessa, poistetaanko lähdekansion kuvat.


---
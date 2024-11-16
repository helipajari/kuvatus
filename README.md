# Kuvatus - kuvien arkistointityökalu

Kuvatus on ohjelma, jolla voi siirtää kuvat esimerkiksi ulkoiselta muistikortilta haluttuun kansioon.
Se luo automaattisesti kansiorakenteen vuosille ja kuukausille.

Kuvatus ei poista tai korvaa jo olemassa olevia kansioita tai kuvia kohdekansiosta. 

---

## Sisältö
- [Käyttöesimerkki](#Käyttöesimerkki)
- [Asennusohje](#Asennusohje)
- [Käyttöohje](#Käyttöohje)
  - [Näppäimistökäyttöohje](#Näppäimistökäyttöohje)
- [Asetukset](#Asetukset)
  - [Kuvatukset perusasetukset](#Kuvatukset perusasetukset) 
  - [Edistyneet asetukset](#Edistyneet asetukset)

---

### Käyttöesimerkki


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

- Kuvatus ei (toistaiseksi) etsi tiedostoja alakansioista, 
eli siirrettävien tiedostojen on oltava kaikkien samassa kansiossa kuten esim. kameran muistikortilla. 
- Kuvatuksen toiminta perustuu (toistaiseksi) päivämäärällä alkaviin tiedostonimiin.

---
## Asennusohje 
0. TBA

---

## Käyttöohje 
1. käynnistä Kuvatus
2. tarkista lähde- ja kohdekansioiden sijainti, etsi tai muuta niitä tarvittaessa
   - lähdekansio on oletusarvona tietokoneen `D`-levy, joka läppäreitä käyttäessä on yleensä muistikortti
   - kohdekansio on oletusarvoisesti käyttäjän oma `Kuvat`-kansio
     - katso [Asetukset](#Asetukset) näiden muokkaamiseksi
   2. **HUOM** kansiota etsiessä tai muutettaessa on valittava `Valitse kansio`, muuten muutos ei tule voimaan.
3. valitse, poistetaanko kuvat lähdekansiosta (tekstiä `Poistetaanko kuvat lähdekansiosta?` voi klikata hiirellä valinnan muuttamiseksi)
4. paina `OK`
5. siirto on valmis, kun ruutuun ilmestyy `Valmis!`-ikkuna. 
6. paina `OK`.

### Näppäimistökäyttöohje

Kuvatusta voi käyttää melkein kokonaan ilman hiirtä. Tällöin Kuvatus käynnistetään tavalliseen tapaan 
hiirellä. Hiirtä tarvitaan vain, jos kansiosijainteja pitää muuttaa.

- `Tab` : Siirry eteenpäin
- `Shift` ja `Tab` : Siirry taaksepäin
- `Välilyönti` : Valitse

---
## Asetukset
Kuvatuksen asetuksia voi muuttaa muokkaamalla asetustiedostoa `config.ini` 
tekstieditorissa (esim. Muistio) ja tallentamalla muutokset. Tiedostopäätettä ei saa muuttaa.

### Kuvatuksen perusasetukset
- `source` sisältää siirrettävien kuvien sijainnin.
  - oletusarvoisesti `D`, joka kannettavilla tietokoneilla vastaa usein muistikorttia
- `destination` sisältää siirrettävien kuvien kohdekansion 
  - oletusarvoisesti käyttäjän oma `Kuvat`-kansio
- `remove` on `1`, jos tiedostot halutaan poistaa lähdekansiosta siirron yhteydessä, muutoin `0`.
  - oletusarvoisesti `1` 
- `month_names` on `1`, jos luotavissa kuukausikansioissa halutaan käyttää myös kuukausien nimiä, muutoin `0`.
  - oletusarvoisesti `1` 

### Edistyneet asetukset
- `store_under_user` on `1`, jos tiedostot tallennetaan 
tietokoneelle kirjautuneen käyttäjän omiin tiedostoihin, muutoin `0`
  - oletusarvoisesti `1`


---




---
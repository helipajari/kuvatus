# <img src="src/img/kuvatus logo.png" width="50" alt-text="kuvatus logo"> Kuvatus - kuvien arkistointityökalu
Kuvatus on ohjelma, jolla voi siirtää kuvatiedostoja.
Se luo kohdekansiooon kansiorakenteen vuosille ja kuukausille 
siirrettävien kuvien tiedostonimien perusteella.

Kuvatus ei poista jo olemassa olevia kansioita tai kohdekansiossa olevia kuvia. 

Kuvatus toimii toistaiseksi vain tiedostonimillä, jotka alkavat päivämäärällä:
- 20230101... toimii
- IMG_20230101... ei toimi

---

## Sisältö
- [Käyttöesimerkki](#Käyttöesimerkki)
- [Asennusohje](#Asennusohje)
- [Käyttöohje](#Käyttöohje)
  - [Näppäimistökäyttöohje](#Näppäimistökäyttöohje)
- [Asetukset](#Asetukset)

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

2023
    - 01 tammi
        - 20230101.jpg
        - 20230102.jpg
        - 20230103.jpg
    - 04 huhti
        - 20230410.jpg

2024
    - 02 helmi
        - 20240201.jpg
        - 20240202.jpg 
```
**HUOMIO!** 

- Kuvatus ei etsi tiedostoja alakansioista, eli siirrettävien tiedostojen on oltava kaikkien samassa kansiossa kuten esim. kameran muistikortilla. 
- Kuvatuksen toiminta perustuu (toistaiseksi) päivämäärällä alkaviin tiedostonimiin.

---
## Asennusohje käyttäjälle
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
4. valitse, käytetäänkö kansioiden nimissä myös kuukausien nimiä numeroiden lisäksi (tekstiä `Käytä kuukausien nimiä kansiossa?` voi klikata hiirellä valinnan muuttamiseksi)
5. paina `OK`
6. siirto on valmis, kun ruutuun ilmestyy `Valmis!`-ikkuna. 
7. paina `Ok, sulje ohjelma`.

### Näppäimistökäyttöohje

Kuvatusta voi käyttää melkein kokonaan ilman hiirtä. Tällöin Kuvatus käynnistetään tavalliseen tapaan 
hiirellä. Hiirtä tarvitaan vain, jos kansiosijainteja pitää muuttaa.

- `Tab` : Siirry eteenpäin
- `Shift` ja `Tab` : Siirry taaksepäin
- `Välilyönti` : Valitse

---
## Asetukset
Kuvatus tallentaa valitut tiedostopolut ja käyttöasetukset automaattisesti asetustiedostoon `config.ini`, kun tiedostoja siirretään.

Jos `config.ini`-tiedostoa ei löydy, Kuvatus luo sellaisen oletusasetuksilla. 
Oletusasetuksina kuvien lähdekansio on D-levy, kohde käyttäjän Kuvat-kansio, 
kuvat poistetaan lähdekansiosta siirron jälkeen ja kansioissa käytetään kuukausien nimiä.


### Kuukausien nimet
Kuukausien nimiä voi vaihtaa muokkaamalla asetustiedostoa tekstieditorissa (esim. Muistio)
ja tallentamalla muutokset.

Tiedostopäätettä `ini` ei saa muuttaa.

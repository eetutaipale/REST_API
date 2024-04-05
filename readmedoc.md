Tehtävät:

REST API sovellus, joka tarjoaa CRUD eli Create Read Update ja Delete -toiminnallisuudet.
Aihepiiri: Yrityslistaus, jossa tilinpäätöstiedot useammalta vuodelta. 

Yhdellä yrityksellä on useampia tilinpäätöksiä. Yritykset tunnistetaan Y-tunnuksella, jotka ovat uniikit. 
Tilinpäätökseen liittyy vain yksi yritys ja tilinpäätöksiä on yksi vuodessa. 

Yritys 1 - N Tilinpäätöstä.
---------
class Yritys:
    id: int
    y-tunnus: string
    nimi: string
    osoitetiedot: string

class Tilinpäätös:
    id: int
    yritys-id: int
    vuosi: int
    tuloslakselma: object
    tase: object
    liitteet: int

Toiminnot:
    CREATE 
    READ 
    UPDATE 
    DELETE 
    https://www.youtube.com/watch?v=4Zy90rd0bkU

Lisätoiminto:
    Yhdistäminen Microsoft PowerBI 
    web-server nginx tai korvaava?
    ASGI async server gateway Interface -> uvicorn
    yksinkertainen käyttöliittymä
    Palvelinvaihtoehdot -> local, vmachine tai vuokrapalvelin

Kirjastoista:
    sqlAlchemy - sessionmaker ja session toiminnot
    pydantic -kirjasto tarjoaa datamallilnnusta


Huomioita:
    Dokumentointi siten, että sovelluksen käyttöönotto on helppoa myös myöhemmin (esim. 1 vuosi)
    Jos riittää aika, niin vaihtoehdot konfigurointiohjeet paikallisesti ja etäserverille
    Millainen käyttöliittymä? 
    Mallit/skeemat omaan tiedostoon
    main joka ohjaa palvelinta ja lisää API komennot
    database.py joka alustaa tietokannan
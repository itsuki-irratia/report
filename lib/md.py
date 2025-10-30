import json
import re

from datetime import datetime
from .common  import Common
from .device  import Device
from .app     import App
from .geo     import Geo

class Md:

    def intro():
        caddy_log = r'{"level":"info","ts":1756367208.0590785,"logger":"http.log.access.log0","msg":"handled request","request":{"remote_ip":"1.2.3.4","remote_port":"6743","proto":"HTTP/2.0","method":"GET","host":"irratia.itsuki.freemyip.com","uri":"/itsuki.ogg","headers":{"User-Agent":["Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0"],"Accept":["text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"],"Accept-Language":["en-US,en;q=0.5"],"Accept-Encoding":["gzip, deflate, br, zstd"],"Sec-Gpc":["1"],"Upgrade-Insecure-Requests":["1"],"Sec-Fetch-Dest":["document"],"Sec-Fetch-Mode":["navigate"],"Sec-Fetch-Site":["none"],"Sec-Fetch-User":["?1"],"Priority":["u=0, i"],"Te":["trailers"]},"tls":{"resumed":false,"version":772,"cipher_suite":4865,"proto":"h2","server_name":"irratia.itsuki.freemyip.com"}},"user_id":"","duration":3.510691638,"size":113299,"status":200,"resp_headers":{"Server":["Caddy","Icecast 2.4.4"],"Alt-Svc":["h3=\":443\"; ma=2592000"],"Content-Type":["audio/ogg"],"Access-Control-Allow-Origin":["*"],"Date":["Thu, 28 Aug 2025 07:46:44 GMT"],"Expires":["Mon, 26 Jul 1997 05:00:00 GMT"],"Pragma":["no-cache"],"Cache-Control":["no-cache, no-store"],"Icy-Pub":["0"],"Icy-Metadata":["1"]}}'

        md = f"""
---
mainfont: "Liberation Mono"
fontsize: 14pt
---
# ITSUKI IRRATIAKO<br>ERREPORTE SISTEMA  

## NOLA DABIL?  
Itsuki irratian zerbitzu nagusi bi ditugu:  

1. Web zerbitzaria  
2. Streaming zerbitzaria

<div style="page-break-after: always;"></div>
### WEB ZERBITZARIA

Web zerbitzari bezala **caddy** erabiltzen dugu, eta web bidez datozen eskaerak kudeatzen ditu, zerbitzu honek uzten dituen **log**-ekin (datuekin) lortzen dugu grafikoak sortzeko ahalmena.

Log adibidea:
```
{caddy_log}
```
Log-ak **json** formatuan agertzen dira, eta datu hauek hartzen ditugu:

- **ts**: timestamp formatuan dator data. Bisitariaren data kalkulatzeko erabiliko dugu.  
- **remote_ip**: bisitariaren IP helbidea. Bisitari bakarrak kalkulatzeko erabiliko dugu.  
- **uri**: web helbidea, streaming ezberdinak aztertzeko erabiliko dugu.  
- **user-agent**: bisitariak erabili duen gailua kalkulatzeko erabiliko dugu.  
- **duration**: bisitaria irratia online entzuten ibili den denbora adierazten digu.  
<div style="page-break-after: always;"></div>
### STREAMING ZERBITZARIA

Streaming zerbitzari bezala **icecast** erabiltzen dugu, eta bertatik seinailea internetean gaur egun **OPUS**, eta **AAC** formatuetan eskaintzen dugu.
Hasieran **OGG** eta **MP3** formatuetan jarri bagenuen ere, gaur egun **OPUS** eta **AAC** formatu berriagotan eskaintzen dugu.

**icecast** zerbitzariaren **log**-ekin erabiltzaileak zenbat denporaz irratia entzuten ibili diren kalkulatu dezakegu:

Log adibidea:
```
127.0.0.1 - - [20/Oct/2025:16:58:11 +0200] "GET /itsuki.opus HTTP/1.1" 200 417 "-" "Go-http-client/2.0" 0
```

Ikusten dugun moduan **200** zenbakia **http status** motako zenbakia da eta balio horrek konexioa ondo joan dela esan nahi du, bere eskumako zenbakia ordea bisitaria zenbat denboraz irratia entzuten ibili den da, kasu honetan: **417** segunduz entzuten ibili da.
<div style="page-break-after: always;"></div>

### GARRANTZITSUA

Bisitari bakarren kalkulua **OHARRAK** atalean dago.
<div style="page-break-after: always;"></div>
    """
        return md

    @staticmethod
    def visistsMonth(since_d, mont_data, duration_data, month_image, width):
        md = f"""
## {since_d}

Hilabetean kontsumitutako denbora:  
**{mont_data['duration']}** segundo, hau da:  
**{duration_data['hours']}** ordu, **{duration_data['minutes']}** minutu, **{duration_data['seconds']}** segundo.

Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{mont_data['connections']}**  
Bisitari bakarrak: **{mont_data['unique']}** 
![]({month_image}){width}
<div style="page-break-after: always;"></div>
        """
        return md

    @staticmethod
    def visistsDay(since_d, day_data, day_image, width):
        md = f"""
## {since_d}

Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{day_data['connections']}**  
Bisitari bakarrak: **{day_data['unique']}** 
![]({day_image}){width}
<div style="page-break-after: always;"></div>
        """
        return md

    @staticmethod
    def notes(month_visite_uniques, mont_data, rest_month_visit):
        md = f"""
## OHARRAK

### BISITARI BAKARREN KALKULUA

Hilabetearen bisitari bakarren kalkulua ez dator bat eguneko bisitari bakarren batuketarekin.
Ezta eguneko orduetako bisitati bakarren batura eta egun osoko bisitari bakarren batura ere.

**Zergatik?**

Egun ezberdinetan, zein eguneko ordu ezberdinetan bisitari berberak irratia entzutera bueltatu direlako.

Beraz, honako formula hau erabiliko dugu, bueltan etorri diren bisitari kopurua kalkulatzeko:

Hilabetean eguneko bisita bakarren batura: **{month_visite_uniques}**  
Hilabeteko bisitak bakarrak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{mont_data['unique']}**  
{month_visite_uniques} - {mont_data['unique']} = **{rest_month_visit}**

Beraz, kenduketa eginda esan genezake bisitari bakar guztietatik (**{mont_data['unique']}**), **{rest_month_visit}** berriz bueltatu direla **itsuki irratia** entzutera.

Formula berbera erabil genezake egunekoak kalkulatzeko, baina uste dugu hilabatekoarekin nahikoa dela.
        """
        return md

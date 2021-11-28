# PMKit

PMKit



## Handig

### Als je ooit de wachtwoord wil resetten van een PI

edit op de sdcard deel ROOTFS

gebruik: `cd rootfs/etc/shadow` en dan `sudo nano shadow`

verander de line die begint met pi naar dit:

`pi:$6$aL9tKoN4$CYpHIPALpfAbOn.vSCR6ZqeK41LZ4eYCTItmiX6gJUUjYFV7entBJdEiX7f5geL.FNZzJ1EArLeneCyaN.ahx/:16878:0:99999:7:::`

dit reset de wachtwoord naar de standaard:

```
usr: pi
```
```
pswd: raspberry
```

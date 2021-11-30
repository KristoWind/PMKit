# PMKit

Working with a SIM7600X-4G-HAT and a Sense-HAT stacked on each other

### Links to both HAT's:

* [SIM7600X-4G-HAT](https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT)

* [Sense-HAT](https://www.raspberrypi.com/products/sense-hat/)


## Code stuff:

For this program I'm using python. The GPS is working with the example file from Waveshare + some extra code to have LED's of the Sense HAT working as a Status of the GPS


## Usefull:

### Converting the ~~fucking~~ .h264 files to mp4

```text
ffmpeg -f lavfi -i aevalsrc=0 -r 30 -i test.h264 -shortest -c:v copy -c:a aac -strict experimental testo.mp4
```

### Resetting the pi user password back to raspberry:

Edit on the ROOTFS part of the SD card:

First go to this directory:
```
cd rootfs/etc/shadow
```
then open shadow with your favorite editor (I'm using nano):
```
sudo nano shadow
```

change the line that starts with `pi` to this:

```
pi:$6$aL9tKoN4$CYpHIPALpfAbOn.vSCR6ZqeK41LZ4eYCTItmiX6gJUUjYFV7entBJdEiX7f5geL.FNZzJ1EArLeneCyaN.ahx/:16878:0:99999:7:::
```

this will reset the password to: 
```
usr: pi
```
```
pswd: raspberry
```

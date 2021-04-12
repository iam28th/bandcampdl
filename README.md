# bandcampdl

Parses Bandcamp HTML to download free 128-kbps MP3 files streaming there. Written in pure Python. Uses `concurrent.futures` module from standard library to download up to 10 tracks simultaneously.

### Install:
```bash
git clone https://github.com/iam28th/bandcampdl 
# or just download a single raw file...
```
### Usage examples:
```bash
python bandcampdl.py https://fief.bandcamp.com/album/v

# or:
chmod +x bandcampdl.py
./bandcampdl.py https://fief.bandcamp.com/album/v
```

Can also pass multiple album links:
```bash
python bandcampdl.py https://sequesteredkeep.bandcamp.com/album/wandering-far \
    https://iamdim.bandcamp.com/album/compendium-ii \
    https://erang.bandcamp.com/album/tome-i
```
Or a text file containing links separeted with Newline:
```
python bandcampdl.py -i urls.txt
```

### Requirements

- Python (written in 3.8.5, probably should work in other versions). Nothing else is requiered.

Currently works only with "album" links, e.g. https://fief.bandcamp.com/album/v

(Support for others might be added in the future).

P.S. Highly recommend checking albums from examples!

# bandcampdl

Parses Bandcamp HTML to download free 128-kbps MP3 files streaming there.

Install:
```bash
git clone https://github.com/iam28th/bandcampdl
```
Usage examples:
```bash
python bandcampdl.py https://fief.bandcamp.com/album/v

# or:
chmod +x bandcampdl.py
./bandcampdl.py https://fief.bandcamp.com/album/v
```

Can also download multiple albums:
```bash
python bandcampdl.py https://sequesteredkeep.bandcamp.com/album/wandering-far \
    https://iamdim.bandcamp.com/album/compendium-ii \
    https://erang.bandcamp.com/album/tome-i
```

Currently works only with "album" links, e.g. https://fief.bandcamp.com/album/v
(Support for others might be added in the future).

#!/usr/bin/env python


import sys
import argparse
import json
import os 
import pathlib
import logging
from urllib import request
from html.parser import HTMLParser
from collections import namedtuple
from concurrent import futures

# parsing command line arguments...
class MyArgParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.stderr.write('error: %s\n' % message)
        sys.exit(1)

parser = MyArgParser(description='A script to download albums from bandcamp')

parser.add_argument('links', metavar='URL', type=str, nargs='*', help='Album links to download') 
parser.add_argument('-i', '--infile', type=str, help='a file with links separeted by Newline')
 
TrackRecord = namedtuple('Track', 'name link')

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOGGER = logging.getLogger()


class AlbumParser(HTMLParser):
    
    def __init__(self):
        super().__init__()

        self.artist = ""
        self.album_title = ""
        self.year = None   # year published

        self.cover_link = ""
        self.tracklist = []

    def full_album_name(self):
        """ Artist - Title (Year) """
        return self.artist + " - " + self.album_title + r' (%s)/' % self.year

    def handle_starttag(self, tag, attrs):
        # might add option to download cover someday
        if tag == 'link':
            rel = attrs[0]
            if rel[1] == 'image_src':
                for attr in attrs:
                    if attr[0] == 'href':
                        self.cover_link = attrs[1]

    def handle_data(self, data):
        data = data.strip()
        if data.startswith('{'):

            data = json.loads(data)
            self.artist = data['byArtist']['name']
            self.year= data['datePublished'].split()[2]
            self.album_title = data['albumRelease'][0]['name']

            for track in data['track']['itemListElement']:
                item = track['item']
                name = item['name']
                additionalProperty = item['additionalProperty']
                for prop in additionalProperty:
                    if prop['name'] == 'file_mp3-128':
                        mp3_url = prop['value']
                        track_record = TrackRecord(self.artist + ' - ' + name + '.mp3', mp3_url)
                        self.tracklist.append(track_record)


def download_tracks(folder, artist, tracklist, n_workers):
    with futures.ThreadPoolExecutor(n_workers) as executor:
        
        jobs = {
             executor.submit(request.urlretrieve, track.link, folder + track.name): track.name for track in tracklist
         }

        for future in futures.as_completed(jobs):
            LOGGER.info('Downloaded track: ' + jobs[future])


if __name__ == '__main__':

    if len(sys.argv) < 2:
        parser.error('No URLs provided, exiting...')
    
    args = parser.parse_args()
    links = []
    if args.infile:
        with open(args.infile, 'r') as f:
            links.extend([line.strip() for line in f])  
    links.extend(args.links)
     
    for link in links:
        LOGGER.info('Opening url: ' + link)
        with request.urlopen(link) as req:
            parser = AlbumParser()
            LOGGER.info('Parsing  HTML...')
            parser.feed(req.read().decode('utf-8'))
        
        
        dirname = parser.full_album_name()
        try:
            LOGGER.info('Creating directory: ' + dirname)
            os.mkdir(dirname)
        except FileExistsError:
            LOGGER.info('...already exists')
        
        n_workers = min(10, len(parser.tracklist))
        LOGGER.info(f'Download start ({n_workers} threads)')
        download_tracks(dirname, parser.artist, parser.tracklist, n_workers) 
    
    print('Download finised. Thank you and come again.')

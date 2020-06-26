import azapi
import pprint
import os
import sys
import getopt

proxy_ip = '34.91.135.38'
proxy_port = 80

proxy  = "http://{}:{}".format(proxy_ip, str(proxy_port))
proxyDict = { 
              "http"  : proxy,
              "https" : proxy
            }

def download_lyrics(artist=str):
    api = azapi.AZlyrics(proxies=proxyDict)
    api.artist = artist

    all_songs = api.getSongs()
    print('Found {} total songs'.format(len(all_songs)))
    for song in all_songs:
        # check if lyric file exists already
        file_name = '{} - {}.txt'.format(str(song).strip(), api.artist)
        if not os.path.isfile(file_name):
            print('Getting lyrics for {}...'.format(str(song)))
            api.getLyrics(url=all_songs[song]["url"], save=True, sleep=30.0)
        else:
            print('Lyric file exists already for {}'.format(str(song)))

def print_help():
    print('lyric-downloader.py -a <artist name>')

def main(argv):
    artist = ''
    try:
        opts, args = getopt.getopt(argv, "ha:", ['artist='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)    
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-a", "-artist"):
            if len(arg) > 0:
                artist = arg
                download_lyrics(artist)
            else:
                print('You must set the artist name')
                sys.exit(1)
        else:
            print('Ignoring unknown option {}'.format(opt))

if __name__ == "__main__":
    main(sys.argv[1:])
    pass
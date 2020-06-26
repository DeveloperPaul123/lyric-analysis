import os
import glob
import pprint
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import getopt
import sys
import csv

def remove_characters(value=str, deletechars=str) -> str:
    """
    Removes the given characters from the given string.

    Parameters:
    -----------
    value: str
        String to modify
    deletechars: str
        The characters to remove
    """
    for c in deletechars:
        value = value.replace(c,'')
    return value

def print_help():
    print("lyric-analysis.py -a <artist name>")

def analyze_lyrics(artist=str):
    text_files = glob.glob('*{}.txt'.format(artist))

    word_dict = dict()
    print('Analyzing lyric files...')
    for file_path in text_files:
        with open(file_path, 'r') as file:
            text_content = file.read()
            # process the content
            for line in text_content.splitlines():
                if '[' in line.strip()[0:3]:
                    print('Ignoring line: {}'.format(line))
                    # skip line
                    continue
                # remove punctuation
                cleaned_up_line = remove_characters(line, ';:,.?*!()&%@#$-_/\\')
                cleaned_up_line = cleaned_up_line.lower()
                # split by whitespace
                words = cleaned_up_line.split()
                for word in words:
                    word_dict[word] = word_dict.get(word, 0) + 1
    
    print('Found {} total words'.format(len(word_dict.keys())))
    
    stopwords = set(STOPWORDS)
    stopwords.update(['to', "the", 'and', 'in', 'for', 'a', 'of', 'my', 'our', 'we', "we\'re", 'i', "i\'m"])

    print('Removing stopwords...')
    for word in stopwords:
        word_dict.pop(word, None)

    sorted_words = dict(sorted(word_dict.items(), key= lambda item : item[1], reverse=True))

    print('Creating bar plot...')

    word_count = 40
    names = list(sorted_words.keys())
    values = list(sorted_words.values())

    plt.bar(range(word_count), values[0:word_count], tick_label=names[0:word_count])
    plt.title('Top {} Words of {} Lyrics'.format(word_count, artist))
    plt.tick_params(axis='x', which='major', labelsize=7)
    plt.xticks(rotation=90)
    plt.savefig('{}-word-hist.png'.format(artist.lower()), dpi=300, bbox_inches='tight')

    print('Creating word cloud...')

    wordcloud = WordCloud(width = 3840, height=2160, background_color = 'white', stopwords = stopwords, max_words=300).generate_from_frequencies(word_dict)
    wordcloud.to_file('{}-analysis.png'.format(artist.lower()))

    print('Saving word list...')
    with open('{}-words.csv'.format(artist.lower()), 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(sorted_words.items())
    

def main(argv):
    artist = ''
    try:
        opts, args = getopt.getopt(argv, "ha:", ['artist='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)   
    if len(opts) == 0:
        print_help()
        sys.exit(2) 
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-a", "-artist"):
            if len(arg) > 0:
                artist = arg
                analyze_lyrics(artist)
            else:
                print('You must set the artist name')
                sys.exit(1)
        else:
            print('Ignoring unknown option {}'.format(opt))


if __name__ == "__main__":
    main(sys.argv[1:])

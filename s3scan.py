import requests
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser


def parseXml(result, link):

    # TO-DO: add unicode support
    try:
        root = ET.fromstring(result)
        for c in root.iter('{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
            print link + "/" + c.text

    # TO-DO: add better parse error handling
    except:
        pass


def main():
    wordlist = ""

    parser = ArgumentParser()
    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="Wordlist to use for bucket names (default: wordlist.txt)", default="wordlist.txt",
                        metavar="wordlist")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    with open(args.wordlist, 'r') as f:
        bucketNames = [line.strip() for line in f]

    for bucket in bucketNames:
        link = "http://" + bucket + ".s3.amazonaws.com"
        try:
            r = requests.head(link)
            if r.status_code != 404:
                r = requests.get(link)
                parseXml(r.text, link)
        except requests.exceptions.RequestException as e:
            print e
            pass


if __name__ == "__main__":
    main()

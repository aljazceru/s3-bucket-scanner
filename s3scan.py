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


def s3Scan(silent,bucket):
    if not silent:
        print "scanning bucket: " + bucket
    link = "http://" + bucket + ".s3.amazonaws.com"
    try:
        r = requests.head(link)
        if r.status_code != 404:
            r = requests.get(link)
            parseXml(r.text, link)
    except requests.exceptions.RequestException as e:
        print e
        pass


def main():
    wordlist = ""
    keyword = ""
    silent = 0
    parser = ArgumentParser()
    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="Wordlist to use for bucket names (default: wordlist.txt)", default="wordlist.txt",
                        metavar="wordlist")
    parser.add_argument("-k", "--keyword", dest="keyword",
                        help="Keyword to use with the wordlist in three different combinations: <keyword>-<wordlist>,<keyword>_<wordlist> and <keyword><wordlist>"
                        , default="", metavar="keyword")
    parser.add_argument("-s", "--silent", dest="silent",
                        help="Silent mode - only prints out the findings without all the combinations and words it scanned for", action="store_true")



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.silent:
        silent = 1

    with open(args.wordlist, 'r') as f:
        bucketNames = [line.strip() for line in f]

    for bucket in bucketNames:
        if args.keyword != "":
            target = args.keyword + "-" + bucket
            s3Scan(silent,target)
            target = args.keyword + "_" + bucket
            s3Scan(silent,target)
            target = args.keyword + bucket
            s3Scan(silent,target)

        else:
            s3Scan(silent,bucket)


if __name__ == "__main__":
    main()

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


def wordlistScan(bucket):
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

def keywordScan(bucket):
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
    parser = ArgumentParser()
    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="Wordlist to use for bucket names (default: wordlist.txt)", default="wordlist.txt",
                        metavar="wordlist")

    parser.add_argument("-k", "--keyword", dest="keyword",
                        help="Keyword to use with the wordlist in the form of <keyword>-<wordlist>", default="",
                        metavar="keyword")



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    with open(args.wordlist, 'r') as f:
        bucketNames = [line.strip() for line in f]

    for bucket in bucketNames:
        if args.keyword != "":
            target = args.keyword + "-" + bucket
            keywordScan(target)
        else:
            wordlistScan(bucket)


if __name__ == "__main__":
    main()

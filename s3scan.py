""" Scans open AWS's S3 buckets using wordlists without aws cli (boto)"""
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
import requests


def parse_xml(result, link):
    """ Parse XML results """
    # TO-DO: add unicode support
    try:
        root = ET.fromstring(result)
        for _ in root.iter('{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
            target = link + "/" + _.text
            _ = requests.head(target)
            if _.status_code == 200:
                print target

    # TO-DO: add better parse error handling
    # If there is a known exception it would be better to catch that exception
    except:
        pass


def s3_scan(silent, bucket):
    """ Checks for open S3 buckets and returns content """
    if not silent:
        print "scanning bucket: " + bucket
    link = "https://" + bucket + ".s3.amazonaws.com"
    try:
        _ = requests.head(link)
        if _.status_code != 404:
            _ = requests.get(link)
            parse_xml(_.text, link)
    except requests.exceptions.RequestException as _:
        print _


def main():
    """ Main program entry with help options and flow logic """
    silent = 0
    parser = ArgumentParser()
    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="Wordlist to use for bucket names (default: wordlist.txt)",
                        default="wordlist.txt",
                        metavar="wordlist")

    parser.add_argument("-k", "--keyword", dest="keyword",
                        help="""Keyword to use with the wordlist in three
                        different combinations:
                        <keyword>-<wordlist>,<keyword>_<wordlist> or
                        <keyword><wordlist>""",
                        default="",
                        metavar="keyword")

    parser.add_argument("-s", "--silent", dest="silent",
                        help="""Silent mode - only prints out the findings
                        without all the combinations and words it scanned
                        for""",
                        action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.silent:
        silent = 1

    with open(args.wordlist, 'r') as _:
        bucket_names = [line.strip() for line in _]

    for bucket in bucket_names:
        if args.keyword != "":
            target = args.keyword + "-" + bucket
            s3_scan(silent, target)
            target = args.keyword + "_" + bucket
            s3_scan(silent, target)
            target = args.keyword + bucket
            s3_scan(silent, target)

        else:
            s3_scan(silent, bucket)


if __name__ == "__main__":
    main()

# S3 bucket scanner

Simple public s3 bucket scanner written in python


### How it works

This script is a public s3 bucket scanner. It uses wordlist to test for existence of publicly open s3 buckets and lists their contents. Wordlist provided with it is just a PoC wordlist I've gathered from various subdomain enumeration lists.

Scanner supports two different modes: 
- simple wordlist scan where it check if there is a publicly accessible s3 bucket for every word in the wordlist
- keyword scan where it uses the keyword in combination with the wordlist. Is uses the wordlist in three different combinations: {keyword}-{wordlist},{keyword}_{wordlist} and {keyword}{wordlist}

For example if we use the keyword nsa and the wordlist contains the word "backup" the script will test for:

```
nsa-backup
nsa_backup
nsabackup
```

### Requirements 

The only requirements for this to run is python's requests lib . 

```
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


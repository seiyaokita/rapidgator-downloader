# Rapidgator-Downloader
Download file from rapidgator with premium user


### How to run
```sh
Usage: rapidgator/cli.py [COMMAND] [OPTIONS]

Command:
  status
  download-single
  download-batch
```

## status
Download by read list of URL in text file (Example : dl.txt)

### Example
```sh
$ python rapidgator/cli.py status ./dl.txt

$ python rapidgator/cli.py status ./dlwithrename.txt

```


## download batch.
Download by read list of URL in text file (Example : dl.txt)
### Example
```sh
$ python rapidgator/cli.py download-batch ./dl.txt

$ python rapidgator/cli.py download-batch ./dlwithrename.txt

```

## download url
Download by URL in argument

### Example
```sh
$ python rapidgator/cli.py download-single [URL]

```

###

---


### Reference

 - [Rapidgator API](https://rapidgator.net/article/api/index).



# available file format.
```
https://rapidgator.net/file/...
https://rapidgator.net/file/...
https://rapidgator.net/file/...
```

or
```
https://rapidgator.net/file/a.rar | alarm.rar
https://rapidgator.net/file/b.part1.rar | book.part1.rar
https://rapidgator.net/file/b.part2.rar | book.part2.rar
https://rapidgator.net/file/8cbb5f521b6d67dad63ab2379a2ed8bb | this_is_a_book.zip 
```
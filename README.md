# Rapidgator-Downloader

This project is a fork of the original [rapidgator-downloader](https://github.com/goodgodth/rapidgator-downloader), which is now inactive. It allows you to download files from Rapidgator using a premium user account.

## Features
- Download files from Rapidgator with a premium account.
- Supports batch downloads from a list of URLs.
- Rename downloaded files based on input.
- Automatic token management for session persistence.

## Requirements
- Python 3.x
- A premium Rapidgator account

## Installation
Before running the downloader, ensure you have the required dependencies installed:
```
pip install -r requirements.txt
```

## How to Run
To run the downloader, use the `cli.py` script. The basic usage is:

Usage: python rapidgator/cli.py [COMMAND] [OPTIONS]

Commands:
  status            Check the status of URLs listed in a text file.
  download-single   Download a single file from Rapidgator.
  download-batch    Download multiple files from a list.


### 1. Check Status of Links (`status`)
Check the status of Rapidgator links by reading from a file. Each line in the file should contain a URL.

#### Example:
```
$ python rapidgator/cli.py status ./dl.txt
```
This will read the file `dl.txt`, check the status of the URLs, and print whether the links are alive or dead.

### 2. Batch Download (`download-batch`)
Download multiple files from Rapidgator by reading a list of URLs from a text file.

#### Example:
```
$ python rapidgator/cli.py download-batch ./dl.txt
```
This command will download all the files listed in `dl.txt`. Optionally, you can rename the files by using the following format in the list:
```
https://rapidgator.net/file/b.part1.rar | book.part1.rar
```

### 3. Single File Download (`download-single`)
Download a single file from Rapidgator by providing the URL directly as a command argument.

#### Example:
```
$ python rapidgator/cli.py download-single https://rapidgator.net/file/12345/example.rar
```

This will download the specified file.

## File Format for Input
You can use two formats in your input files:

1. **Basic Format:**
```
https://rapidgator.net/file/...
https://rapidgator.net/file/...
```

2. **Rename Format:**
```
https://rapidgator.net/file/a.rar | alarm.rar
https://rapidgator.net/file/b.part1.rar | book.part1.rar
https://rapidgator.net/file/b.part2.rar | book.part2.rar
https://rapidgator.net/file/8cbb5f521b6d67dad63ab2379a2ed8bb | this_is_a_book.zip 
```

In the rename format, the file will be saved with the name after the pipe (`|`).

## Token Management
- After successful login, an access token is stored locally to avoid re-authentication on every request.
- If the token expires or becomes invalid, the tool will automatically log in again and refresh the token.

## Reference
- [Rapidgator API Documentation](https://rapidgator.net/article/api/index)

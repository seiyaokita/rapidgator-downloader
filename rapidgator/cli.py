# rapidgator/cli.py

import click
import os
import sys
import logging
import configparser
from rapidgator import RapidgatorAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up ConfigParser to read config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Read username, password, and download folder from config file
USERNAME = config['rapidgator'].get('username')
PASSWORD = config['rapidgator'].get('password')
DOWNLOAD_FOLDER = config['rapidgator'].get('download_folder')

@click.group()
def cli():
    """Rapidgator Downloader Command-Line Interface"""
    pass

@cli.command()
@click.argument('filelist')
def status(filelist):
    """Check the status of Rapidgator links using config for username and password"""
    try:
        api = RapidgatorAPI(USERNAME, PASSWORD)
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        sys.exit(1)

    with open(filelist, 'r') as f:
        for cnt, line in enumerate(f, 1):
            url = line.strip()
            if not url:
                continue
            try:
                file_id = url.split("/")[4]
                data = api.get_file_info(file_id)
                status_msg = "Link is Alive" if data["status"] == 200 else "Link is dead/wrong"
                logger.info(f"File {cnt}: {url} -> {status_msg}")
            except Exception as e:
                logger.error(f"Error processing URL {url}: {e}")

@cli.command()
@click.argument('rapid_url')  # Use a positional argument for the URL
def download_single(rapid_url):
    """Download a single file from Rapidgator using config for username, password, and download folder"""
    try:
        api = RapidgatorAPI(USERNAME, PASSWORD)
        file_id = rapid_url.split("/")[4]
        file_name = api.get_file_name(rapid_url)
        download_url = api.get_download_link(file_id)

        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        download_cmd = f"wget -O '{file_path}' '{download_url}'"
        logger.info(f"Downloading to {file_path}")
        os.system(download_cmd)
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        sys.exit(1)

@cli.command()
@click.argument('filelist')
def download_batch(filelist):
    """Download multiple files from Rapidgator using config for username, password, and download folder"""
    try:
        api = RapidgatorAPI(USERNAME, PASSWORD)
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        sys.exit(1)

    with open(filelist, 'r') as f:
        for cnt, line in enumerate(f, 1):
            try:
                parts = line.strip().split("|")
                url = parts[0].strip()
                file_name_alt = parts[1].strip() if len(parts) > 1 else None

                if not url:
                    continue

                file_id = url.split("/")[4]
                file_name = api.get_file_name(url, default_name=file_name_alt)
                download_url = api.get_download_link(file_id)

                file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
                download_cmd = f"wget -nc -O '{file_path}' '{download_url}'"
                logger.info(f"Downloading file {cnt}: {file_name}")
                os.system(download_cmd)
            except Exception as e:
                logger.error(f"Error processing file {cnt}: {e}")

if __name__ == '__main__':
    cli()
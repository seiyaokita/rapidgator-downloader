# rapidgator/rapidgator.py

import requests
from lxml import html
import logging
import os
import json

logger = logging.getLogger(__name__)

class RapidgatorAPI:
    LOGIN_URL = "https://rapidgator.net/api/v2/user/login"
    FILE_INFO_URL = "https://rapidgator.net/api/v2/file/info/"
    FILE_DOWNLOAD_URL = "https://rapidgator.net/api/v2/file/download/"
    XPATH_FILENAME = "//div[@class='text-block file-descr']//p//a//text()"
    TOKEN_FILE = "rapidgator_token.json"  # File to store the token

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.load_token()

        # If no token is available, login and save the new token
        if not self.token:
            self.token = self.login(username, password)
            self.save_token(self.token)

    def login(self, username, password):
        """Login to Rapidgator and retrieve a new token"""
        params = {"login": username, "password": password}
        response = requests.get(url=self.LOGIN_URL, params=params)
        data = response.json()

        if data["status"] != 200:
            logger.error(f"Failed to authenticate with Rapidgator API. Response: {data['response']}")
            raise Exception("Failed to authenticate with Rapidgator API")

        # Log the full response and save the token
        logger.info(f"Successfully authenticated with Rapidgator API. Response: {data['response']}")
        return data["response"]["token"]

    def load_token(self):
        """Load the token from the file, if it exists"""
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'r') as f:
                data = json.load(f)
                logger.info(f"Token loaded from file: {self.TOKEN_FILE}")
                return data.get('token')
        return None

    def save_token(self, token):
        """Save the token to a file"""
        with open(self.TOKEN_FILE, 'w') as f:
            json.dump({'token': token}, f)
            logger.info(f"Token saved to file: {self.TOKEN_FILE}")

    def delete_token(self):
        """Delete the token file if it exists"""
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)
            logger.info("Token file deleted due to 401 Unauthorized")

    def get_file_info(self, file_id):
        """Get file information, retry login if token expired (401)"""
        params = {"file_id": file_id, "token": self.token}
        response = requests.get(url=self.FILE_INFO_URL, params=params)

        if response.status_code == 401:
            logger.warning("Received 401 Unauthorized. Refreshing token...")
            self.token = self.login(self.username, self.password)
            self.save_token(self.token)

            # Retry the request with the new token
            params["token"] = self.token
            response = requests.get(url=self.FILE_INFO_URL, params=params)

        return response.json()

    def get_download_link(self, file_id):
        """Get the download link, retry login if token expired (401)"""
        params = {"file_id": file_id, "token": self.token}
        response = requests.get(url=self.FILE_DOWNLOAD_URL, params=params)

        if response.status_code == 401:
            logger.warning("Received 401 Unauthorized. Refreshing token...")
            self.token = self.login(self.username, self.password)
            self.save_token(self.token)

            # Retry the request with the new token
            params["token"] = self.token
            response = requests.get(url=self.FILE_DOWNLOAD_URL, params=params)

        data = response.json()
        if data["status"] != 200:
            logger.error(f"Failed to get download link for file_id {file_id}")
            raise Exception("Failed to get download link")
        return data["response"]["download_url"]

    def get_file_name(self, url, default_name=None):
        """Get the file name from the page source or use a default"""
        page = requests.get(url)
        if page.status_code >= 400:
            logger.warning(f"Failed to retrieve page for URL {url}. Using default name.")
            return default_name or url.split('/')[-1]
        root = html.fromstring(page.text)
        result = root.xpath(self.XPATH_FILENAME)
        file_name = ''.join([word.strip() for word in result])
        if not file_name:
            logger.warning(f"Could not extract file name from URL {url}. Using default name.")
        else:
            logger.debug(f"Extracted file name: {file_name}")
        return file_name or default_name or url.split('/')[-1]
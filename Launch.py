import traceback
import requests
import json
import time

from datetime import datetime
from colorama import Fore

from DDNS import load as DDNSLoad
from DDNS import request_url


# Instantiate Config.json
config = DDNSLoad.Load().get_json()
ReqUrl = request_url.RequestUrl()


class Program:
    def __init__(self):
        self.mydomain       =config["mydomain"]
        self.dns_record     =config["dns_record"]
        self.gdapikey       =config["gdapikey"]
        self.refresh        =config["refresh_rate"]

        self.get_response = ""
        self.put_response = ""

        self.engine = True

        self.gdip = ""
        self.myip = ""
        self.error_occured = False

        self.request_url = ReqUrl.get_url()

    def get(self):
        r=requests.get(f"{self.request_url}", headers={"Authorization" : f"sso-key {self.gdapikey}"})

        # Log failure in the console
        if not r.ok:
            print(Fore.RED + "Failed to get rest_api, Error Code: " + str(r.status_code))
            print(f"Response:\n {r.text}", end=Fore.RESET)
            print()

            return False

        try:
            # Log response to get_response
            self.get_response = json.loads(r.content.decode("utf-8"))[0]

            # Save current gdip from response
            self.gdip = self.get_response["data"]
        except Exception:
            print(Fore.RED + "Failed to get rest_api, unable to decode JSON !")
            traceback.print_exc()
            print(Fore.RESET)

            return False

        return True

    def get_public_ip(self):
        r = requests.get("https://api.ipify.org")

        if not r.ok:
            print("Failed to get public_ip, Error Code: " + str(r.status_code))
            print(f"Response:\n {r.text}")
            print()

            return False

        try:
            self.myip = r.content.decode("utf-8")
        except Exception:
            print(Fore.RED + "Failed to get public_ip, unable to decode content !")
            traceback.print_exc()
            print(Fore.RESET)

            return False

        return True

    def put(self):
        payload = [{"data": f"{(self.myip)}"}]

        r=requests.put(
            self.request_url, headers={

            "Authorization" : f"sso-key {self.gdapikey}",
            "Content-Type" : "application/json"},
            json=payload)

        # Log response to put_response
        if r.ok:
            self.put_response = "OK, Looks Good!"
        else:
            self.put_response = json.loads(r.content.decode("utf-8"))[0]

    def runEngine(self):
        while self.engine:
            # Get current datetime
            now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

            # Get Current IP from API
            if not self.get():
                # Check every <seconds>
                time.sleep(self.refresh)
                continue

            # Get Current Public IP
            if not self.get_public_ip():
                # Check every <seconds>
                time.sleep(self.refresh)
                continue

            if self.gdip != self.myip and self.myip != "":
                print("\n")
                print(Fore.RED + "IP Has Changed : Updating on GoDaddy" + Fore.RESET)

                # Update new ip
                self.put()
                # Return new response
                self.get()

                # Print Updated IP
                print(Fore.GREEN + f"IP Successfully Updated : {self.gdip}" + Fore.RESET)

                # Create Log Files
                with open("Response.log", "a") as log:
                    log.write(
                        f"[{now}]" +
                        "\n\n" +
                        "GET Response:\n" +
                        str(self.get_response) +
                        "\n\n" +
                        "PUT Response:\n" +
                        str(self.put_response) +
                        "\n\n\n\n\n\n"
                    )

            # Display Text
            print("\n")
            print(Fore.CYAN + f"[{now}]" + Fore.RESET)
            print(f"GD IP: {self.gdip}")
            print(f"My IP: {self.myip}")

            # Check every <seconds>
            time.sleep(self.refresh)


if __name__ == "__main__":
    # Instantiate Program
    program = Program()

    # Background Process
    program.runEngine()
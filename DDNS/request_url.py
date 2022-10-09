from DDNS import load as DDNSLoad


# Instantiate Config.json
config = DDNSLoad.Load().get_json()


class RequestUrl:
    def __init__(self):
        self.mydomain       =config["mydomain"]
        self.dns_record     =config["dns_record"]

        # -------- Set your request url here --------
        self.request_url = f"https://api.godaddy.com/v1/domains/{self.mydomain}/records/A/{self.dns_record}"


    def get_url(self):
        return self.request_url
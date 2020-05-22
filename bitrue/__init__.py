from hashlib import sha256
import hmac
import requests # try with aiohttp?
import time

from constants import URI, URIS, URLS

class Bitrue:
    FF_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"

    @classmethod
    def get_url(cls, uri):
        return URLS["BASE_URL"] + "/" + URLS["API_VERSION"] + "/" + uri.path

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self._init_session()

    def _init_session(self):
        """Initiate the user session
        """
        session = requests.session()
        session.headers.update({
            "Accept": "application/json",
            "User-Agent": self.FF_USER_AGENT,
            "X-MBX-APIKEY": self.api_key,
        })
        return session

    def _generate_signature(self, data):
        data_params = self._sort_data_params(data)
        data_params = [f"{var}={val}" for var, val in data_params.items()]

        query = "&".join(data_params).encode("utf-8")
        m = hmac.new(self.api_secret.encode("utf-8"), query, sha256)
        return m.hexdigest()

    def _sort_data_params(self, data):
        signature = None
        params = []
        for key, val in data.items():
            if key == "signature":
                signature = val
            else:
                params.append((key, val))

        params.sort(lambda x: x[0])
        if signature is not None:
            params.append(("signature", signature))
        return params

    def _get(self, path, **kwargs):
        return self._api_request("get", path, **kwargs)

    def _post(self, path, **kwargs):
        return self._api_request("post", path, **kwargs)

    def _delete(self, path, **kwargs):
        return self._api_request("delete", path, **kwargs)

    def _put(self, path, **kwargs):
        return self._api_request("put", path, **kwargs)

    def _get_uri(self, method, path):
        uri = URIS.get(path, None)
        if uri is None:
            raise Exception(f"Invalid API path: {path}")

        if isinstance(uri, URI):
            return uri

        # `order` is a list of GET, POST, DELETE uris.
        for u in uri:
            if u.method == method:
                return u
        else:
            raise Exception(f"Invalid method for {uri.path}")


    def _api_request(self, method, path, **kwargs):
        uri = self._get_uri(method, path)
        return self._request(uri, **kwargs)

    def _request(self, uri, **kwargs):
        kwargs["timeout"] = 10

        data = kwargs.get("data")
        if data and isinstance(data, dict):
            kwargs["data"] = data

        if uri.signed:
            ts = int(time.time() * 1000)
            kwargs["data"]["timestamp"] = ts
            kwargs["data"]["signature"] = self._generate_signature(kwargs["data"])

        # need to sort again incase we added ts and signature above ^
        if data:
            kwargs["data"] = self._sort_data_params(kwargs["data"])

            # if get request assign data list to `params`
            if uri.method == "get":
                kwargs["params"] = kwargs["data"]
                del kwargs["data"]

        resp = None
        url = self.get_url(uri)
        if uri.method == "get":
            resp = self.session.get(url, **kwargs)
        else:
            resp = self.session.post(url, **kwargs)

        return self._parse_response(resp)

    def _parse_response(self, resp):
        if str(resp.status_code)[0] != "2":
            raise Exception(f"Bitrue Error: {response}")

        try:
            return resp.json()
        except ValueError:
            raise Exception(f"Error parsing response: {resp.text}")

    def exchange_info(self):
        return self._get("exchangeInfo")


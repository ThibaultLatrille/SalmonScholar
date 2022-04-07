import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urlencode, quote_plus


class ScraperAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get(self,
            url,
            headers={},
            country_code=None,
            premium=None,
            render=None,
            session_number=None,
            autoparse=None,
            retry=3,
            timeout=60):
        return makeRequestWithMethod(url, self.api_key, "GET", headers, country_code, premium, render, session_number,
                                     autoparse, retry, timeout, None)

    def scrapyGet(self,
                  url,
                  headers={},
                  country_code=None,
                  premium=None,
                  render=None,
                  session_number=None,
                  autoparse=None,
                  retry=3,
                  timeout=60):
        query = {
            'url': url,
            'api_key': self.api_key,
            'keep_headers': 'true' if len(headers) > 0 else None,
            'country_code': country_code,
            'premium': 'true' if premium else None,
            'render': 'true' if render else None,
            'session_number': session_number,
            'autoparse': 'true' if autoparse else None,
            'scraper_sdk': 'python'
        }
        query_filtered = {k: v for k, v in query.items() if v is not None}
        result = urlencode(query_filtered, quote_via=quote_plus)
        url = ('https://api.scraperapi.com/?' + result)
        return url

    def post(self,
             url,
             headers={},
             country_code=None,
             premium=None,
             render=None,
             session_number=None,
             autoparse=None,
             retry=3,
             timeout=60,
             body=None):
        return makeRequestWithMethod(url, self.api_key, "POST", headers, country_code, premium, render, session_number,
                                     autoparse, retry, timeout, body)

    def put(self,
            url,
            headers={},
            country_code=None,
            premium=None,
            render=None,
            session_number=None,
            autoparse=None,
            retry=3,
            timeout=60,
            body=None):
        return makeRequestWithMethod(url, self.api_key, "PUT", headers, country_code, premium, render, session_number,
                                     autoparse, retry, timeout, body)

    def account(self):
        return requests.get('https://api.scraperapi.com/account', params={'api_key': self.api_key}).json()


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def makeRequestWithMethod(url,
                          api_key,
                          method,
                          headers={},
                          country_code=None,
                          premium=None,
                          render=None,
                          session_number=None,
                          autoparse=None,
                          retry=3,
                          timeout=60,
                          body=None):
    query = {
        'url': url,
        'api_key': api_key,
        'keep_headers': 'true' if len(headers) > 0 else None,
        'country_code': country_code,
        'premium': 'true' if premium else None,
        'render': 'true' if render else None,
        'session_number': session_number,
        'autoparse': 'true' if autoparse else None,
        'scraper_sdk': 'python'
    }
    query_filtered = {k: v for k, v in query.items() if v is not None}
    # @todo add headers
    r = requests_retry_session(retries=retry).request(method, 'https://api.scraperapi.com/', params=query_filtered,
                                                      timeout=timeout, data=body, headers=headers)
    return r

# print(ScraperAPIClient("b2b93816137cae0f4679b5253c3dcfd8").get("https://postman-echo.com").text)
# ScraperAPIClient("b2b93816137cae0f4679b5253c3dcfd8").account()

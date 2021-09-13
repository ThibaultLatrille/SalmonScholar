import pandas as pd
from scraper_api import ScraperAPIClient
from scholarly import scholarly, ProxyGenerator
import argparse


class ScraperAPI(ProxyGenerator):
    def __init__(self, api_key):
        self._api_key = api_key
        self._client = ScraperAPIClient(api_key)

        assert api_key is not None

        super(ScraperAPI, self).__init__()

        self._TIMEOUT = 120
        self._session = self._client
        self._session.proxies = {}

    def _new_session(self):
        self.got_403 = False
        return self._session

    def _close_session(self):
        pass  # no need to close the ScraperAPI client


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--search', required=True, type=str, dest="search")
    parser.add_argument('-n', '--name', required=True, type=str, dest="name")
    parser.add_argument('-k', '--api_key', required=True, type=str, dest="api_key")
    args = parser.parse_args()

    pg = ScraperAPI(args.api_key)
    scholarly.use_proxy(pg)
    scholarly.set_timeout(120)
    search_query = scholarly.search_pubs(args.search)
    publi = next(search_query)
    cites = scholarly.citedby(publi)
    df = pd.DataFrame([p["bib"] for p in cites])
    df.to_csv(args.name, index=False)

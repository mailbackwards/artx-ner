from urllib2 import urlopen, Request
from urllib import urlencode
import json


class DbpediaAPI(object):
    """
    Interacts with DBpedia API endpoints. No API key required.
    """

    DBPEDIA_ENDPOINT = "http://lookup.dbpedia.org/api/search.asmx/"
    SPOTLIGHT_ENDPOINT = "http://spotlight.dbpedia.org/rest/"

    def get_json(self, url, params):
        r = Request(url+'?'+urlencode(params))
        r.add_header('accept', 'application/json')
        resp = urlopen(r)
        return json.loads(resp.read())

    def spotlight_annotate(self, payload):
        """
        Queries DBpedia's `Spotlight API <https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki>`_.

        :param payload: Fulltext natural language payload.
        :type payload: string
        :return: Dictionary of JSON response from DBpedia
        """
        url = self.SPOTLIGHT_ENDPOINT + "annotate"
        params = {
            "text": payload,
            "confidence": 0.3
        }
        return self.get_json(url, params)

    def extract_entities(self, payload):
        """
        Queries DBpedia's `Spotlight API <https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki>`_
        and processes the results to return only useful resources.

        :param payload: Fulltext natural language payload.
        :type payload: string
        :return: List of JSON entities returned by DBpedia
        """
        results = self.spotlight_annotate(payload)
        return [resource['@URI'] for resource in results['Resources']]

    def keyword_search(self, keyword):
        """
        Queries DBpedia's keyword search API to get a list of matching entities
        to the provided keyword.

        :param keyword: Keyword to use in query.
        :type keyword: string
        """
        url = self.DBPEDIA_ENDPOINT + "KeywordSearch"
        params = {
            "QueryClass": "",
            "QueryString": keyword
        }
        return self.get_json(url, params)

    def prefix_search(self, prefix):
        """
        Search by prefix, used for autocomplete.

        :param prefix: Text prefix.
        :type prefix: string
        """
        url = self.DBPEDIA_ENDPOINT + "PrefixSearch"
        params = {
            "QueryClass": "",
            "QueryString": prefix,
            "MaxHits": 5
        }
        return self.get_json(url, params)

    def wikify_stanford(self, stanford_results):
        """
        Take a set of unlinked entities from the Stanford module and link them
        to DBpedia resources.

        :param stanford_results: Formatted Stanford entities as returned by
            :py:meth:`parserbot.stanford.StanfordNER.extract_entities`.
        :type stanford_results: dict
        """
        dbp_results = []
        for entity_type, entity_list in stanford_results.items():
            for keyword in entity_list:
                dbp_response = self.keyword_search(keyword)['results']
                dbp_resource = dbp_response[0] if dbp_response else {}
                response = {
                    'uri': None,
                    'stanford_type': entity_type.lower(),
                    'stanford_name': keyword
                }
                response.update(dbp_resource)
                dbp_results.append(response)
        return dbp_results

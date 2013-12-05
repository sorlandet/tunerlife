import requests


class YahooAuctionAPI():
    url = ''
    query = {}
    headers = {'User-Agent': 'auction-api-developer'}
    method = 'GET'
    timeout = 30.0
    error_code = ''

    def set_query(self, key, value):
        self.query.setdefault(key, value)

    def execute(self):
        if self.method == 'GET':
            r = requests.get(self.url, params=self.query,
                             headers=self.headers, timeout=self.timeout)
        elif self.method == 'POST':
            r = requests.post(self.url, data=self.query,
                              headers=self.headers, timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            return r.json()

        self.error_code = r.status_code

        return False

    def get_error_code(self):
        return self.error_code

    def set_url(self, value):
        self.url = value

    def set_method(self, method):
        self.method = method

    def set_timeout(self, timeout):
        self.timeout = timeout


class APIAccessBase():
    API_OPTION_APPID = "appid"
    API_OPTION_URL = "url"
    API_OPTION_PAGE = "page"
    API_OPTION_AUCTIONID = "auctionID"
    #  for listing
    API_OPTION_ESCROW = "escrow"
    API_OPTION_EASYPAYMENT = "easypayment"
    API_OPTION_THUMBNAIL = "thumbnail"

    LISTINGS_PER_PAGE = 50

    def __init__(self, application_id):
        self.api = YahooAuctionAPI()
        self.api.set_query(self.API_OPTION_APPID, application_id)

    def action(self):
        obj = self.api.execute()
        if not obj:
            obj = self.api.get_error_code()

        return obj

    def set_option(self, key, value):
        if key == self.API_OPTION_URL:
            self.api.set_url(value)
        else:
            self.api.set_query(key, value)


class Search(APIAccessBase):
    AUCTION_API_URL = 'http://auctions.yahooapis.jp/AuctionWebService/'
    API_NAME = 'search'

    version = None

    def __init__(self, application_id, version):
        APIAccessBase.__init__(self, application_id)
        self.version = version

    def action(self):
        url = '%s%s/%s' % (self.AUCTION_API_URL, self.version, self.API_NAME)
        self.set_option(self.API_OPTION_URL, url)
        return APIAccessBase.action(self)

    def set_option(self, key, value):
        APIAccessBase.set_option(self, key, value)








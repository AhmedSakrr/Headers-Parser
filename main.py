from re import search
from requests import get
from bs4 import BeautifulSoup


class AgentParser:
    '''
        browser - str, chrome/opera/firefox\n
        pages - int, pages for parse. 50 entries in one page.\n
        full - bool, save full UA string or by versions and devices\n
            If full -> use .ua_list\n
            Elif -> use .versions and .devices\n
        min_ver - int, minimum browser version.\n
        os - str, Windows/Linux\n
        platform - str, Mobile/Computer
    '''

    __slots__ = (
        'browser', 'min_ver', 'os', 'platform',
        'ua_list', 'versions', 'devices', 'full',
        'pages', '__parse_re'
    )

    def __init__(self, browser, pages=1, full=True,
                 min_ver=40, os='Any', platform='Any'):
        self.browser = browser.lower()
        self.full = full
        self.min_ver = min_ver
        self.os = os.lower()
        self.platform = platform.lower()
        self.pages = pages

        if self.full:
            self.ua_list = []
        else:
            self.versions = []
            self.devices = []

        self.__parse_re = {
            'chrome': {
                'r_dev': r'(?:Mozilla\/5.0..)(.*)..Apple',
                'r_ver': r'(?:Chrome\/)(\d{2}\W\d\W\d{1,4}\W\d{1,4})'
            },
            'opera': {
                'r_dev': r'(?:Mozilla\/5.0..)(.*)..Apple',
                'r_ver': r'(?:OPR\/)(.*)'
            },
            'firefox': {
                'r_dev': r'(?:Mozilla\/5.0..)(.*)..Ge',
                'r_ver': r'(?:Firefox\/)(.*)'
            }
        }

        self.__receive()

    def __url(self, page):
        return 'https://developers.whatismybrowser.com/useragents/explore' + \
            f'/software_name/{self.browser}/{page}?order_by=-software_version'

    def __add(self, v, d):
        if v not in self.versions:
            self.versions.append(v)
        if d not in self.devices:
            self.devices.append(d)

    def __parse2(self, td):
        txt = td[0].find('a').text
        ver = int(td[1].text)
        os = (td[2].text).lower()
        platform = (td[3].text).lower()

        v = search(self.__parse_re[self.browser]['r_ver'], txt)[1]
        d = search(self.__parse_re[self.browser]['r_dev'], txt)[1]

        if ver >= self.min_ver:
            if (self.os == 'any' or os in self.os) and \
               (self.platform == 'any' or platform in self.platform):
                if self.full:
                    if txt not in self.ua_list:
                        self.ua_list.append(txt)
                else:
                    self.__add(v, d)

    def __parse(self, text):
        bs = BeautifulSoup(text, 'html5lib')
        a = bs.find('table', {'class': 'table-useragents'})
        b = a.find('tbody')
        rows = b.findAll('tr')

        for row in rows:
            try:
                self.__parse2(row.findAll('td'))
            except Exception:
                pass

    def __receive(self):
        for i in range(self.pages):
            i += 1
            self.__parse(get(self.__url(i)).text)

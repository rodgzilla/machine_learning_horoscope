import requests
import bs4
import pandas as pd
import time

class HoroscopePage():
    def __init__(self, zodiac_sign, date):
        self.url = 'http://www.beliefnet.com/inspiration/astrology/{}.aspx?d={}'.format(zodiac_sign, date)

    def _download_page(self):
        """
        Download the page containing the horoscope.
        """
        request           = requests.get(self.url)
        self.page_content = request.text

    def get_horoscope(self):
        """
        Extract the horoscope from the page content.
        """
        self._download_page()
        soup      = bs4.BeautifulSoup(self.page_content, 'html.parser')
        date_tag  = soup.find('time', {'class' : 'todays-horoscope'})
        horoscope = date_tag.next_sibling.strip()

        return horoscope

class Requester():
    def __init__(self, date_start, date_end, zodiac_signs = None):
        self.date_start = date_start
        self.date_end   = date_end

        if not zodiac_signs:
            zodiac_signs = [
                'aries',
                'taurus',
                'gemini',
                'cancer',
                'leo',
                'virgo',
                'libra',
                'scorpio',
                'sagittarius',
                'capricorn',
                'aquarius',
                'pisces'
            ]

        self.zodiac_signs = zodiac_signs

    def make_requests(self, delay, verbose = False):
        def format_date(date):
            return str(date.date()).replace('-', '')

        result = []
        for date in pd.date_range(self.date_start, self.date_end):
            for zodiac_sign in self.zodiac_signs:
                if verbose:
                    print('Requesting horoscope for {:11} on date {}'.format(zodiac_sign, date.date()))
                url_date  = format_date(date)
                page      = HoroscopePage(zodiac_sign, url_date)
                horoscope = page.get_horoscope()
                result.append((zodiac_sign, date.date(), horoscope))
                time.sleep(delay)
        return result

def result_to_dataframe(results):
    return pd.DataFrame.from_records(results, columns = ['SIGN', 'DATE', 'TEXT'])

def request_everything(start_year, end_year, delay):
    for year in range(start_year, end_year + 1):
        print('####################### {} #######################'.format(year))
        start_date = '{}-01-01'.format(year)
        end_date   = '{}-12-31'.format(year) if year != 2017 else '2012-12-20'
        requester  = Requester(start_date, end_date)
        results    = requester.make_requests(delay, True)
        df         = result_to_dataframe(results)
        df.to_csv('data/horoscope_{}.csv'.format(year), index = False)

if __name__ == '__main__':
    request_everything(2010, 2017, 0)

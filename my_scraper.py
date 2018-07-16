from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
import lxml
import numpy as np

__author__ = "Mike Zhong"


# 'http://www.footballdb.com/fantasy-football/index.html?pos=QB%2CRB%2CWR%2CTE&yr=2016&wk=1&rules=2'
class Scraper:

    def __init__(self, base_url):
        """
        Constructor, takes a base_url to associate with. Once a URL has been parsed, the soup attribute will hold a
        BeautifulSoup object used for further parsing. The weeks attribute is used to loop over all 16 weeks of the
        NFL season. The dfs dictionary holds all tables as dataframes, with the week number as the key, they will be
        stacked on top of one another to generate a big compiled data frame
        :param base_url: URL to scrape from
        """
        self.url_base = base_url
        self.soup = None
        self.url_options = {}
        self.wd = os.getcwd()
        self.weeks = np.arange(1, 17)
        self.dfs = {}

    def build_url(self, week, rules):
        """
        Returns URL based on the week and rules
        :param week: string (1-16)
        :param rules: string (1 or 2)
        :return: full URL for parsing
        """
        return self.url_base + '&wk=' + str(week) + '&rules=' + rules

    def mod_header(self, header):
        """
        Modifies header to fit the needs of my dataframe
        :param header: starting header
        :return: None
        """
        assert(isinstance(header, list))
        if 'Game' in header:
            header.remove('Game')
        header.insert(1, 'Team')
        header.insert(2, 'Opponent')
        header.insert(3, 'Location')
        header.append('Week')

    def parse_url(self, url):
        """
        parses the url passed and creates a BeautifulSoup instance stored in the soup attribute
        :param url: full URL to parse
        :return: None
        """
        response = requests.get(url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'lxml')
        else:
            raise BaseException('Response returned status code:', response.status_code)

    def parse_html_table(self, week):
        """
        heavily lifting method, see the 'bs4_and_requests.ipynb' notebook for the development of this method
        :param week: the week corresponding to the table
        :return: None
        """
        all_tables = self.soup.find_all('table')
        table = all_tables[0]
        trs = table.find_all('tr')

        header = trs[1].text.strip().split('\n')
        self.mod_header(header)

        rows = []
        for tr in trs[2:]:
            row = []

            for td in tr.find_all('td'):
                if len(td) > 0:
                    text = td.text.replace("\xa0", " ").replace('.', '')

                    # get team of player and opposing team, and home/away
                    bold = td.find('b')
                    if bold:
                        row.append(bold.text)
                        m = re.match(r"^(.+)@(.+)$", text)
                        if m and text.startswith(bold.text):
                            row.append(m.groups()[1])
                            row.append('home')
                        else:
                            row.append('@' + m.groups()[0])
                            row.append('away')
                        continue

                    # parse player name from awful text
                    m = re.match(r"^(.+) (.+)", text)
                    if m:
                        name = m.groups()[0][:-1]
                        row.append(name)
                        continue

                    row.append(text)

            row.append(week)
            rows.append(row)

        my_table = pd.DataFrame(rows, columns=header)
        my_table.loc[:, 'Pts*'] = my_table.loc[:, 'Pts*'].astype(float) / 100.0
        self.dfs[week] = my_table

    def concat_tables(self):
        """
        Concatenates all the tables in the self.df attribute vertically. Saves the resulting dataframe to disk.
        :return: None
        """
        dfs = [df for df in self.dfs.values()]
        print(type(dfs))
        new_df = pd.concat(dfs, axis=0, ignore_index=True)
        new_df.to_csv(self.wd + '/data/merged.csv', index=False)

    def write_tables(self):
        """
        Helper function to write each individual data frame to disk. Not necessary but helpful for debugging
        :return: None
        """
        for i, table in self.dfs.items():
            table.to_csv(self.wd + '/data/week' + str(i) + '.csv', index=False)


if __name__ == "__main__":

    # Driver
    base_url = 'http://www.footballdb.com/fantasy-football/index.html?pos=QB%2CRB%2CWR%2CTE&yr=2016'
    rules = '2'  # 2=PPR, 1=standard

    scraper = Scraper(base_url)

    # iterate over all 16 weeks
    for week in scraper.weeks:
        # build the URL
        url = scraper.build_url(week, rules)
        # parse the URL, the scraper.soup should now hold the BeautifulSoup object
        scraper.parse_url(url)

        # parse the table and store in scraper.dfs
        if scraper.soup:
            scraper.parse_html_table(week)

    scraper.concat_tables()

    # scraper.write_tables()

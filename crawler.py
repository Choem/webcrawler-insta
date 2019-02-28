import time
import json
import io

from urllib.parse import urlparse, urlencode, quote_plus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class InstagramCrawler():
    data = list()

    def __init__(self, email, password):
        self.browser = webdriver.Chrome('/usr/bin/chromedriver')
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://instagram.com/accounts/login')

        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        

    def crawl(self, url, cb):
        print('Crawling %s' % (url))
        self.browser.get(url)
        bodyWebElement = self.browser.find_element_by_tag_name('body')
        if bodyWebElement and len(bodyWebElement.text) > 0:
            bodyWebElementJson = json.loads(bodyWebElement.text)

            print('Status %s' % (bodyWebElementJson['status']))
            if bodyWebElementJson['status'] == 'fail':
                print('Retrying in 10 seconds...')
                time.sleep(10)
                self.crawl(url, cb)
                return

            total = bodyWebElementJson['data']['location']['edge_location_to_media']['count']
            edges = bodyWebElementJson['data']['location']['edge_location_to_media']['edges']
            self.data += [edge['node'] for edge in edges]
            print('Added %d items' % (len(edges)))

            if bodyWebElementJson['data']['location']['edge_location_to_media']['page_info']['has_next_page'] == True:
                end_cursor = bodyWebElementJson['data']['location']['edge_location_to_media']['page_info']['end_cursor']
                amount_to_get = total - len(self.data)
                print('Progress (%d/%d) - %f' % (len(self.data), total, (len(self.data)/int(total)*100)))
                self.crawl(self._createUrl(amount_to_get, end_cursor), cb)
            else:
                print('Done crawling')
                cb()


    def _createUrl(self, max, next):
        variables = '{"id":"224081233","first":'+ str(max) +',"after":'+ next +'}'
        return 'https://www.instagram.com/graphql/query/?query_hash=1b84447a4d8b6d6d0426fefb34514485&variables=%s' % quote_plus(variables)


    def shutdown(self):
        self.browser.quit()

    @property
    def get_data(self):
        return self.data
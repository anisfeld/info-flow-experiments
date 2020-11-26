import time
# time.sleep, re.split
import re
# some prints
import sys
# for running the driver on websites
from selenium import webdriver
# for tagging log with datetime
from datetime import datetime
# to press keys on a webpage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
# interacting with Google Search
import google_search
import random
# strip html

from HTMLParser import HTMLParser


class MLStripper():
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class GoogleAdsUnit(google_search.GoogleSearchUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_search.GoogleSearchUnit.__init__(
            self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#         browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

    def collect_ads(self, reloads, delay, site, file_name=None, search_terms=None):
        if file_name == None:
            file_name = self.log_file
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
            try:
                s = datetime.now()
                if(site == 'toi'):
                    self.save_ads_toi(file_name)
                elif(site == 'bbc'):
                    self.save_ads_bbc(file_name)
                elif(site == 'monster'):
                    self.save_ads_monster(file_name)
                elif(site == 'google'):
                    self.save_ads_google(file_name, search_terms=search_terms)
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
            except:
                self.log('error', 'collecting ads', 'Error')
            rel = rel + 1

    def save_ads_toi(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://timesofindia.indiatimes.com/international-home")
        time.sleep(10)
        driver.execute_script('window.stop()')
        tim = str(datetime.now())
        frame = driver.find_element_by_xpath(
            ".//iframe[@id='ad-left-timeswidget']")

        def scroll_element_into_view(driver, element):
            """Scroll element into view"""
            y = element.location['y']
            driver.execute_script('window.scrollTo(0, {0})'.format(y))

        scroll_element_into_view(driver, frame)
        driver.switch_to.frame(frame)
        ads = driver.find_elements_by_css_selector(
            "html body table tbody tr td table")
        for ad in ads:
            aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
            bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
            t = aa[0].get_attribute('innerHTML')
            l = aa[1].get_attribute('innerHTML')
            b = bb[0].get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()

    def save_ads_bbc(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.bbc.com/news/")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector(
            "div.bbccom_adsense_container ul li")
        for el in els:
            t = el.find_element_by_css_selector(
                "h4 a").get_attribute('innerHTML')
            ps = el.find_elements_by_css_selector("p")
            b = ps[0].get_attribute('innerHTML')
            l = ps[1].find_element_by_css_selector(
                "a").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)

    def save_ads_monster(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://jobsearch.monster.com/")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector("section.card-content")
        for i, el in enumerate(els):
            try:
                title = el.find_element_by_class_name('title').text
                company = el.find_element_by_class_name('company').text
                location = el.find_element_by_class_name('location').text
                ad = tim+"@|"+title+"@|"+company+"@|"+location
                ad = ad.encode("utf8")
                self.log('measurement', 'ad', ad)

            except:
                try:
                    if el.text:
                        title = el.find_element_by_class_name('title-ad').text
                        company = el.find_element_by_class_name(
                            'job-ad-description').text
                        location = el.find_element_by_class_name(
                            'entry-ad').text
                        ad = tim+"@|"+title+"@|"+company+"@|"+location
                        ad = ad.encode("utf8")
                        self.log('measurement', 'ad', ad)

                except:
                    ad = tim+"@|Failed@|NA@|NA"
                    self.log('measurement', 'ad', ad)

    def save_ads_google(self, file, search_terms, n_pages=5):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        random.shuffle(search_terms)
        driver.set_page_load_timeout(60)
        driver.get("http://www.google.com/")

        def process_ads(ads, term, tim):
            for i in range(len(ads)):
                parsed_ad = [x for x in ads[i].text.split(
                    "\n") if x not in ["Ads", "", 'Ad·']]
                # some will be blank
                if parsed_ad:
                    title = parsed_ad[0]
                    url = parsed_ad[1]
                    body = "\n".join(parsed_ad[2:])
                    out_ad = tim+"@|ad - "+term+"@|"+title+"@|"+url+"@|"+body
                    out_ad = out_ad.encode("utf8")
                    # print(out_ad)
                    self.log('measurement', 'ad', out_ad)

        def process_search(res, term, tim):
            for i in range(len(res)):
                title = res[i].find_element_by_css_selector("h3 span").text
                url = res[i].find_element_by_css_selector(
                    "a cite").text.split()[0]
                body = res[i].find_element_by_xpath(
                    "div[@class = 'IsZvec']").text
                out_res = tim+"@|search - "+term+"@|"+title+"@|"+url+"@|"+body
                out_res = out_res.encode("utf8")
                # print(out_res)
                self.log('measurement', 'ad', out_res)

        tim = str(datetime.now())

        for term in search_terms:
            q = driver.find_element_by_name("q")
            q.clear()
            q.send_keys(term)
            q.submit()
            page = 1
            while page <= n_pages:

                # text ads at the top of the page are in a
                #   div with id 'tads' (inside 'tvcap')
                # text ads at the bottom of the page are in a
                #   div with id 'tadsb' (inside 'bottomads')
                ads = WebDriverWait(driver, timeout=60).until(lambda d: d.find_elements_by_xpath(
                    ".//div[contains(@id, 'tvcap') or contains(@id, 'bottomads')]"))

                # ads = driver.find_elements_by_xpath(".//div[contains(@id, 'tvcap') or contains(@id, 'bottomads')]")
                ads = [ad for ad in ads if ad.text != ""]

                # collect first page of ads
                if page == 1:
                    # this WebDriverWait seemed to fail: got a stale element error
                    time.sleep(5)
                    res = WebDriverWait(driver, timeout=60).until(
                        lambda d: d.find_elements_by_xpath(".//div[@class = 'rc']"))
                    res = [r for r in res if r.text != ""]

                    try:
                        process_search(res, term, tim)
                    except:
                        pass

                if ads:
                    process_ads(ads, term, tim)
                    page += 1
                    # see if there are ads on the next page
                else:
                    if page > 1:
                        break
                    page += 1

                # try next page
                driver.find_element_by_xpath(
                    "//span[contains(text(), 'Next')]").click()

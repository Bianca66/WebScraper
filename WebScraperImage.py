from      PIL import Image
from selenium import webdriver
import hashlib
import io
import os
import time
import requests
from selenium.webdriver.chrome.options import Options


class scrape_imag:
    CHROME_PATH = '/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/home/palade/Documents/proiecte/Sisteme de Operare/WebScraper/chromedriver'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #chrome_options.binary_location = CHROME_PATH

    def fetch_image_urls(query: str, tbs, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
        def scroll_to_end(wd):
             wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             time.sleep(sleep_between_interactions)

        ### Build the google query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gsl=img&tbs=ic:specific,{tbs}"
        query_ = query.split()
        query_ = '+'.join(query_)
        ### Load the page
        wd.get(search_url.format(q=query_, tbs=tbs))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            ### Get images
            thumbnail_results = wd.find_elements_by_css_selector("img.rg_ic")
            number_results = len(thumbnail_results)

            print("Found: {} search results. Extracting links from {}:{}".format(number_results,results_start,number_results))

            for img in thumbnail_results[results_start:number_results]:
                ### Try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                ### Extract image urls
                actual_images = wd.find_elements_by_css_selector('img.irc_mi')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print("Found: {} image links, done!".format(len(image_urls)))
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(1)
                load_more_button = wd.find_element_by_css_selector(".ksb")
                if load_more_button:
                    wd.execute_script("document.querySelector('.ksb').click();")

            ### Move the result startpoint further down
            results_start = len(thumbnail_results)
        return image_urls


    def persist_image(folder_path: str, url: str):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print("ERROR - Could not download {} - {}".format(url,e))

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print("SUCCESS - saved {} - as {}".format(url,file_path))
            #scrape_imag.progress += scrape_imag.progress_iterator
            print(scrape_imag.progress)
        except Exception as e:
            print("ERROR - Could not save {} - {}".format(url,e))


    def search_and_download(search_term, tbs, driver_path: str, target_path='./images', number_images=10):
        target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
        #scrape_imag.progress_iterator = 100/number_images
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        with webdriver.Chrome(executable_path=driver_path, chrome_options=scrape_imag.chrome_options) as wd:
            wd.minimize_window()
            res = scrape_imag.fetch_image_urls(search_term, tbs, number_images, wd=wd, sleep_between_interactions=1)

        for elem in res:
            scrape_imag.persist_image(target_folder, elem)

#nr_imag = 10
#scrape_imag.search_and_download(search_term='pandas', tbs="isc:red", driver_path=scrape_imag.CHROMEDRIVER_PATH,target_path='/home/palade/Documents/proiecte/Sisteme de Operare/Scraped Image', number_images=5)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/home/palade/Documents/proiecte/Sisteme de Operare/WebScraper/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )
search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gsl=img&tbs=ic:specific,{tbs}"
query = "cute python"
query_ = query.split()
query_ = '+'.join(query_)
### Load the page
driver.get(search_url.format(q=query_, tbs=""))
driver.get_screenshot_as_file("capture.png")
driver.close()
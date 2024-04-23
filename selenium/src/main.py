import sys
sys.path.append('C:/Users/chand/Documents/Workspace/vcode/python-snippets-1/selenium/src') 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Specify the path to the WebDriver executable (e.g., chromedriver.exe)
driver_path = 'C:/Users/chand/Documents/Workspace/vcode/python-snippets-1/selenium/tools/chromedriver.exe'

# Create ChromeOptions object
chrome_options = webdriver.ChromeOptions()

# Pass the executable path to the ChromeOptions
chrome_options.add_argument(f'--webdriver={driver_path}')

# Create a new instance of the Chrome driver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Open a website
driver.get("https://www.example.com")

time.sleep(10)

# Find an element by its name attribute
search_box = driver.find_element("name", "q")

# Type something into the search box
search_box.send_keys("Hello, Selenium!")

# Submit the form (e.g., pressing Enter)
search_box.send_keys(Keys.RETURN)

# Wait for a few seconds to see the results
driver.implicitly_wait(5)

# Close the browser
driver.quit()

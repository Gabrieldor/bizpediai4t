from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from selenium.webdriver.chrome.options import Options
from asyncio import run

api = FastAPI()

@api.post("/api/v1/bizapedia/quote")
def quote(request: Request):
    return get_quote(request.json())

def get_state_code(state_name):
    state_codes = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 
        'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 
        'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 
        'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 
        'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    
    return state_codes.get(state_name, "Invalid state name")

def get_quote(_j):
    company_name = _j["company_name"]
    state_name = get_state_code(_j["state_code"])

    # Configure options to use a real browser
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open browser in full-screen
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid Selenium detection

    # Initialize WebDriver with random user-agent and headers
    driver = webdriver.Chrome(options=chrome_options)

    # Set random delays
    def random_sleep(min_time=2, max_time=5):
        time.sleep(random.uniform(min_time, max_time))

    # Function to type characters one by one (human-like)
    def human_type(element, text):
        for char in text:
            element.send_keys(char)
            random_sleep(0.1, 0.3)  # Simulate typing speed

    # Function to log in
    def login():
        driver.get("https://www.bizapedia.com/login.aspx")
        
        # Wait for the username field to be present (timeout after 10 seconds)
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtUid"))  # Updated to correct ID
            )
        except Exception as e:
            print("Username field not found:", e)
            driver.quit()
            return

        # Wait for the password field
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtPwd"))  # Corrected ID for password field
            )
        except Exception as e:
            print("Password field not found:", e)
            driver.quit()
            return

        # Type in username and password character by character
        human_type(username_field, "steve@insurance4truck.com")
        random_sleep()
        human_type(password_field, "Trucking@2024#")
        
        # After entering the password, hit the "Enter" key to submit the form
        password_field.send_keys(u'\ue007')  # Unicode for the Enter key (U+E007)
        random_sleep()

    # Search by company and state
    def perform_search():
        driver.get("https://www.bizapedia.com/advanced-search.aspx")
        random_sleep()

        # Enter company name
        company_input = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td[2]/input')
        human_type(company_input, company_name)
        random_sleep()

        # Select the state from the dropdown
        state_dropdown = Select(driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td[2]/select'))
        state_value = get_state_value(state_name)
        state_dropdown.select_by_value(state_value)
        random_sleep()

        # Click search button
        search_button = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[11]/td/table/tbody/tr/td[1]/div')
        ActionChains(driver).move_to_element(search_button).click().perform()
        random_sleep()

        company = driver.find_element(By.XPATH, f'//tr[@class="listview_item_out"]')
        ActionChains(driver).move_to_element(company).click().perform()
        random_sleep()


        #WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[@class='groupbox_large_darkblue_link']")))  # Corrected ID for password field)
        links = driver.find_elements(By.XPATH, "//a[@class='groupbox_large_darkblue_link']")
        output = []
        for name in links:
            if name.text.isupper():
                output.append(name.text)
        
        return output

    # Get state value from provided state name
    def get_state_value(state_name):
        state_mapping = {
            "Alaska": "2",
            "Alabama": "1",
            "Arkansas": "4",
            "Arizona": "3",
            "California": "5",
            "Canada": "52",
            "Colorado": "6",
            "Connecticut": "7",
            "District of Columbia": "9",
            "Delaware": "8",
            "Florida": "10",
            "Georgia": "12",
            "Hawaii": "13",
            "Iowa": "19",
            "Idaho": "16",
            "Illinois": "17",
            "Indiana": "18",
            "Kansas": "20",
            "Kentucky": "21",
            "Louisiana": "22",
            "Massachusetts": "26",
            "Maryland": "25",
            "Maine": "24",
            "Michigan": "28",
            "Minnesota": "14",
            "Missouri": "30",
            "Mississippi": "29",
            "Montana": "11",
            "North Carolina": "36",
            "North Dakota": "37",
            "Nebraska": "32",
            "New Hampshire": "33",
            "New Jersey": "34",
            "New Mexico": "31",
            "Nevada": "15",
            "New York": "35",
            "Ohio": "38",
            "Oklahoma": "39",
            "Oregon": "40",
            "Pennsylvania": "41",
            "Puerto Rico": "55",
            "Rhode Island": "42",
            "South Carolina": "43",
            "South Dakota": "44",
            "Tennessee": "45",
            "Texas": "46",
            "Utah": "47",
            "Virginia": "49",
            "Virgin Islands": "56",
            "Vermont": "48",
            "Washington": "50",
            "Wisconsin": "27",
            "West Virginia": "51",
            "Wyoming": "23",
            # Continue mapping all states similarly...
        }
        return state_mapping.get(state_name, "0")  # Default to empty value if not found

    login()
    driver.quit()
    return perform_search()
    

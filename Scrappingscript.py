from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from datetime import datetime

# List of URLs and corresponding league names to scrape
url_league_mapping = [
    ("https://www.flashscore.in/football/norway/eliteserien/fixtures/","eliteserien"),  # URL and League Name
    ("https://www.flashscore.in/football/norway/obos-ligaen/fixtures/","obos-ligaen"),
    ("https://www.flashscore.in/football/usa/mls/fixtures/","mls") # Add more URLs and League Names as needed
]

# Get the current year
current_year = datetime.now().year

# Initialize the Selenium WebDriver without specifying the executable path
driver = webdriver.Chrome()  # Ensure that ChromeDriver is in your system's PATH

# Create the CSV file and write the header row
with open('fixtures.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['League', 'Date', 'Time', 'Home Team', 'Away Team'])  # Separate League, Date, Time, Home Team, and Away Team columns

    for url_and_league in url_league_mapping:
        url, league_name = url_and_league  # Unpack URL and League Name within the loop

        # Open the website
        driver.get(url)

        # Wait for a few seconds to ensure the page is loaded
        driver.implicitly_wait(10)  # You may need to adjust the time as needed

        # Find the fixture data on the page using Selenium
        fixtures = driver.find_elements(By.CSS_SELECTOR, '.event__match')

        # Iterate through the fixture data and write it to the CSV file
        for fixture in fixtures:
            date_time_element = fixture.find_element(By.CSS_SELECTOR, '.event__time')
            date_time = date_time_element.text.split()  # Split the Date and Time
            date = f"{date_time[0]} {current_year}"  # Add the current year to the Date
            time = date_time[1]  # Second part is the Time
            home_team = fixture.find_element(By.CSS_SELECTOR, '.event__participant--home').text
            away_team = fixture.find_element(By.CSS_SELECTOR, '.event__participant--away').text

            # Write data to the CSV file, including the League Name
            writer.writerow([league_name, date, time, home_team, away_team])

# Close the browser
driver.quit()

print("Fixture data from multiple URLs has been scraped and saved to fixtures.csv with separate League Name and other columns.")

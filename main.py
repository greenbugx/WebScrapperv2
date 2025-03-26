from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import re
import time
import random
from urllib.parse import urljoin, urlparse
import logging

# Colors for UI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def show_ascii_art():
    art = f"""
    {GREEN}                                                                                                                                         
@@@  @@@  @@@  @@@@@@@@  @@@@@@@      @@@@@@    @@@@@@@  @@@@@@@    @@@@@@   @@@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@     @@@  @@@   @@@@@@   
@@@  @@@  @@@  @@@@@@@@  @@@@@@@@    @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@    @@@  @@@  @@@@@@@@  
@@!  @@!  @@!  @@!       @@!  @@@    !@@       !@@       @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!       @@!  @@@    @@!  @@@       @@@  
!@!  !@!  !@!  !@!       !@   @!@    !@!       !@!       !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!  @!@    !@!  @!@      @!@   
@!!  !!@  @!@  @!!!:!    @!@!@!@     !!@@!!    !@!       @!@!!@!   @!@!@!@!  @!@@!@!   @!@@!@!   @!!!:!    @!@!!@!     @!@  !@!     !!@    
!@!  !!!  !@!  !!!!!:    !!!@!!!!     !!@!!!   !!!       !!@!@!    !!!@!!!!  !!@!!!    !!@!!!    !!!!!:    !!@!@!      !@!  !!!    !!:     
!!:  !!:  !!:  !!:       !!:  !!!         !:!  :!!       !!: :!!   !!:  !!!  !!:       !!:       !!:       !!: :!!     :!:  !!:   !:!      
:!:  :!:  :!:  :!:       :!:  !:!        !:!   :!:       :!:  !:!  :!:  !:!  :!:       :!:       :!:       :!:  !:!     ::!!:!   :!:       
 :::: :: :::    :: ::::   :: ::::    :::: ::    ::: :::  ::   :::  ::   :::   ::        ::        :: ::::  ::   :::      ::::    :: :::::  
  :: :  : :    : :: ::   :: : ::     :: : :     :: :: :   :   : :   :   : :   :         :        : :: ::    :   : :       :      :: : :::  
                                                                                                                                           
{RESET}
    """
    print(art)
    print(f"{GREEN}GreenBugX{RESET}\n")


def load_user_agents():
    try:
        with open("UserAgent.txt", "r") as file:
            user_agents = [line.strip() for line in file if line.strip()]
            if user_agents:
                return user_agents
    except FileNotFoundError:
        print(f"{RED}UserAgent.txt not found. Falling back to default User-Agent.{RESET}")
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ]


def configure_driver():
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def create_folder(base_path, folder_name):
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_file(url, folder, user_agent):
    try:
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "index.html"
            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"{GREEN}Downloaded:{RESET} {filepath}")
            logging.info(f"Downloaded: {filepath}")
        else:
            print(f"{RED}Failed to download:{RESET} {url} (Status Code: {response.status_code})")
            logging.error(f"Failed to download {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"{RED}Error downloading {url}: {e}{RESET}")
        logging.error(f"Error downloading {url}: {e}")


def extract_assets(driver, url, folder, depth, visited, user_agents):
    if url in visited or depth < 0:
        return
    visited.add(url)

    print(f"{YELLOW}Scraping:{RESET} {url}")
    logging.info(f"Scraping: {url}")

    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Save main HTML
    user_agent = random.choice(user_agents)
    save_file(url, folder, user_agent)

    asset_types = {
        "css": [link.get("href") for link in soup.find_all("link", href=True) if ".css" in link.get("href")],
        "js": [script.get("src") for script in soup.find_all("script", src=True)],
        "images": [img.get("src") for img in soup.find_all("img", src=True)],
        "videos": [video.get("src") for video in soup.find_all("video", src=True)],
        "audios": [audio.get("src") for audio in soup.find_all("audio", src=True)],
        "fonts": [font.get("href") for font in soup.find_all("link", href=True) if "font" in font.get("href")]
    }

    # Download assets
    for asset_type, urls in asset_types.items():
        asset_folder = create_folder(folder, asset_type)

        for asset_url in urls:
            full_url = urljoin(url, asset_url)
            save_file(full_url, asset_folder, user_agent)

    # Recursively scrape links
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    for link in links:
        full_url = urljoin(url, link)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            extract_assets(driver, full_url, folder, depth - 1, visited, user_agents)


def scrape_website():
    user_agents = load_user_agents()
    url = input("Enter the URL to scrape: ").strip()
    folder_name = input("Enter the folder name to save the website: ").strip()
    depth = int(input("Enter the depth for recursive crawling (0 for single page): "))

    base_folder = create_folder("scraped_sites", folder_name)
    driver = configure_driver()

    try:
        visited = set()
        extract_assets(driver, url, base_folder, depth, visited, user_agents)
    except Exception as e:
        print(f"{RED}Error during scraping: {e}{RESET}")
        logging.error(f"Error during scraping: {e}")
    finally:
        driver.quit()

    print(f"\n{GREEN}Scraping completed! Files saved in: {base_folder}{RESET}")


def main():
    show_ascii_art()

    while True:
        print("\n1. Start Scraping")
        print("2. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            scrape_website()
        elif choice == "2":
            print("Exiting... Goodbye!")
            break
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")


if __name__ == "__main__":
    main()

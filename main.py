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

def generate_user_agents(num_agents=10):
    """Generate random modern browser User-Agents"""
    browsers = {
        'chrome': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36'
        ],
        'firefox': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{}.0) Gecko/20100101 Firefox/{}.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{}.0) Gecko/20100101 Firefox/{}.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:{}.0) Gecko/20100101 Firefox/{}.0'
        ],
        'edge': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36 Edg/{}.0.{}.{}'
        ]
    }
    
    user_agents = []
    for _ in range(num_agents):
        browser = random.choice(list(browsers.keys()))
        template = random.choice(browsers[browser])
        
        if browser == 'chrome':
            major = random.randint(90, 120)  # Recent Chrome versions
            minor = random.randint(0, 9999)
            patch = random.randint(0, 999)
            user_agents.append(template.format(major, minor, patch))
        elif browser == 'firefox':
            version = random.randint(90, 120)  # Recent Firefox versions
            user_agents.append(template.format(version, version))
        elif browser == 'edge':
            major = random.randint(90, 120)
            minor = random.randint(0, 9999)
            patch = random.randint(0, 999)
            edge_major = random.randint(90, 120)
            edge_minor = random.randint(0, 9999)
            edge_patch = random.randint(0, 999)
            user_agents.append(template.format(major, minor, patch, edge_major, edge_minor, edge_patch))
    
    return list(set(user_agents))  # Remove any duplicates

def load_or_generate_user_agents():
    print(f"\n{GREEN}User-Agent Configuration:{RESET}")
    print("1. Load from UserAgent.txt")
    print("2. Generate random User-Agents")
    choice = input("Choose an option (1/2): ").strip()
    
    if choice == "1":
        try:
            with open("UserAgent.txt", "r") as file:
                user_agents = [line.strip() for line in file if line.strip()]
                if user_agents:
                    print(f"{GREEN}Successfully loaded {len(user_agents)} User-Agents from file{RESET}")
                    return user_agents
                else:
                    print(f"{YELLOW}UserAgent.txt is empty, falling back to generation...{RESET}")
        except FileNotFoundError:
            print(f"{YELLOW}UserAgent.txt not found, falling back to generation...{RESET}")
    elif choice == "2":
        num_agents = int(input("How many User-Agents to generate? (default 10): ") or 10)
        user_agents = generate_user_agents(num_agents)
        print(f"{GREEN}Generated {len(user_agents)} unique User-Agents{RESET}")
        
        # Option to save generated User-Agents
        save_choice = input("Would you like to save these User-Agents to UserAgent.txt? (y/n): ").strip().lower()
        if save_choice == 'y':
            try:
                with open("UserAgent.txt", "w") as file:
                    for ua in user_agents:
                        file.write(ua + "\n")
                print(f"{GREEN}User-Agents saved to UserAgent.txt{RESET}")
            except Exception as e:
                print(f"{RED}Error saving User-Agents to file: {e}{RESET}")
        
        return user_agents
    else:
        print(f"{YELLOW}Invalid choice, falling back to generation...{RESET}")
    
    # Default fallback
    user_agents = generate_user_agents(10)
    print(f"{GREEN}Generated {len(user_agents)} default User-Agents{RESET}")
    return user_agents

def format_proxy(proxy_string):
    """Format proxy string to proper URL format with authentication if present"""
    try:
        # Check if proxy contains authentication credentials
        if ':' in proxy_string:
            parts = proxy_string.split(':')
            if len(parts) == 4:  # Format: ip:port:username:password
                ip, port, username, password = parts
                return f"http://{username}:{password}@{ip}:{port}"
            elif len(parts) == 2:  # Format: ip:port
                return f"http://{proxy_string}"
        return f"http://{proxy_string}"
    except Exception as e:
        print(f"{RED}Error formatting proxy {proxy_string}: {e}{RESET}")
        return None

def load_proxies():
    try:
        with open("proxies.txt", "r") as file:
            proxies = []
            for line in file:
                proxy = line.strip()
                if proxy:
                    formatted_proxy = format_proxy(proxy)
                    if formatted_proxy:
                        proxies.append(formatted_proxy)
            
            if proxies:
                print(f"{GREEN}Loaded {len(proxies)} proxies{RESET}")
                return proxies
    except FileNotFoundError:
        print(f"{RED}proxies.txt not found. Falling back to direct connection.{RESET}")
    return []

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


def save_file(url, folder, user_agent, proxy=None, timeout=10):
    try:
        headers = {"User-Agent": user_agent}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        if proxy:
            # Only show the proxy host:port in the UI, not the credentials
            display_proxy = proxy.split('@')[-1] if '@' in proxy else proxy
            print(f"{YELLOW}Using proxy {display_proxy} to scrape: {url}{RESET}")
        else:
            print(f"{YELLOW}Using direct connection to scrape: {url}{RESET}")
            
        response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)

        if response.status_code == 200:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "index.html"
            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"{GREEN}Successfully downloaded:{RESET} {filepath}")
            logging.info(f"Downloaded: {filepath}")
            return True
        else:
            print(f"{RED}Failed to download:{RESET} {url} (Status Code: {response.status_code})")
            logging.error(f"Failed to download {url} (Status Code: {response.status_code})")
            return False
    except requests.Timeout:
        print(f"{RED}Proxy {proxy} timed out while scraping: {url}{RESET}")
        logging.error(f"Proxy timeout: {proxy}")
        return False
    except Exception as e:
        print(f"{RED}Error downloading {url}: {e}{RESET}")
        logging.error(f"Error downloading {url}: {e}")
        return False


def try_with_proxies(url, folder, user_agent, proxies, max_attempts=5):
    if not proxies:
        return save_file(url, folder, user_agent)
        
    attempts = 0
    tried_proxies = set()
    
    while attempts < max_attempts and len(tried_proxies) < len(proxies):
        proxy = random.choice([p for p in proxies if p not in tried_proxies])
        tried_proxies.add(proxy)
        
        if save_file(url, folder, user_agent, proxy):
            return True
        attempts += 1
        if attempts < max_attempts and len(tried_proxies) < len(proxies):
            print(f"{YELLOW}Switching to different proxy...{RESET}")
    
    if attempts == max_attempts:
        print(f"{YELLOW}Max proxy attempts reached, trying without proxy...{RESET}")
        return save_file(url, folder, user_agent)
    return False

def extract_assets(driver, url, folder, depth, visited, user_agents, proxies):
    if url in visited or depth < 0:
        return
    visited.add(url)

    print(f"\n{YELLOW}Scraping:{RESET} {url}")
    logging.info(f"Scraping: {url}")

    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Save main HTML
    user_agent = random.choice(user_agents)
    try_with_proxies(url, folder, user_agent, proxies)

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
        if urls:
            print(f"\n{GREEN}Processing {len(urls)} {asset_type} files...{RESET}")
            asset_folder = create_folder(folder, asset_type)

            for asset_url in urls:
                full_url = urljoin(url, asset_url)
                try_with_proxies(full_url, asset_folder, user_agent, proxies)

    # Recursively scrape links
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    if links:
        print(f"\n{GREEN}Found {len(links)} links to process...{RESET}")
        for link in links:
            full_url = urljoin(url, link)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                extract_assets(driver, full_url, folder, depth - 1, visited, user_agents, proxies)


def scrape_website():
    print(f"\n{GREEN}Loading configurations...{RESET}")
    user_agents = load_or_generate_user_agents()
    proxies = load_proxies()
    
    # Display configuration summary
    print(f"\n{GREEN}Configuration Summary:{RESET}")
    print(f"User-Agents: {len(user_agents)} available")
    print(f"Proxies: {len(proxies)} available")
    
    print(f"\n{GREEN}Please enter the following details:{RESET}")
    url = input("Enter the URL to scrape: ").strip()
    folder_name = input("Enter the folder name to save the website: ").strip()
    depth = int(input("Enter the depth for recursive crawling (0 for single page): "))

    base_folder = create_folder("scraped_sites", folder_name)
    print(f"\n{GREEN}Initializing Chrome driver...{RESET}")
    driver = configure_driver()

    try:
        visited = set()
        extract_assets(driver, url, base_folder, depth, visited, user_agents, proxies)
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
            print(f"{RED}Exiting... Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")


if __name__ == "__main__":
    main()

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Web_Scrapper_v2.1-GreenBugX-8A2BE2?style=for-the-badge&logo=insects&logoColor=white&labelColor=darkgreen&color=green&labelWidth=400&logoWidth=40" alt="Scrape!" style="transform: scale(1.5); margin: 10px 0;" />
  </a>
</p>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,py,vscode,selenium" />
  </a>
</p>

## 📜 Introduction
The **Web Scrapper v2.1** is a Python-based tool and the successor of [Web Scrapper v1](https://github.com/greenbugx/WebScrapper) designed to scrape and download entire websites, including all associated assets like HTML, CSS, JavaScript, images, videos, audios, and fonts. It leverages both **requests** and **Selenium** to handle dynamic content and provides advanced features for recursive crawling, user-agent spoofing, and error handling.

---

## 🚀 What's the Use?
- Archiving complete websites for offline use.
- Extracting all assets (images, videos, audio, font's) from a webpage.
- Analyzing website structure for research or SEO purposes.
- Learning how websites serve dynamic content through JavaScript.

---

## ✨ Features
- [x] **Dynamic Content Handling:** Uses Selenium to render JavaScript-heavy pages.
- [x] **Download All Assets:** HTML, CSS, JS, images, videos, audio, and fonts.
- [x] **User-Agent Spoofing:** Randomized User-Agent from a `UserAgent.txt` file.
- [x] **Recursive Crawling:** Scrape all internal links up to a specified depth.
- [x] **Save as Complete Website:** Adjusts paths to work offline.
- [x] **Error Handling & Logging:** Comprehensive error management and logging.
- [x] **Improved User Interface:** Interactive menu with ASCII art for enhanced terminal experience.
- [X] **Proxies:** Rotating proxy from `proxies.txt` feature for Anonymity.
- [ ] **Custom Header Requests:** Coming in next update.
---

## 🛠️ Installation
1. **Clone the Repository:**
```bash
git clone https://github.com/greenbugx/
cd advanced-web-scraper
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
Ensure **Google Chrome** is installed.

3. **Set Up User-Agent File:**
Create a `UserAgent.txt` file in the same directory and add User-Agent strings like:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```
Or
Simple Run the script and it will prompt you to generate Random UserAgents and save it in `UserAgent.txt`.
---

4. **Set Up Proxies File:**
Create a `proxies.txt` file in the same directory and add your proxies like:
```
ip:port:username:password
ip2:port2:username2:password2
```
If Proxies are not available then it will fall back to default IP(Your IP)!

## 🔧 How to Run
```bash
python main.py
```
- Choose **Option 1** to start scraping.
- Choose **Option 1** to Load UserAgents from `UserAgents.txt` Or **Option 2** to generate Random UserAgents.
- Provide the URL, folder name, and recursive depth.
- The scraped content will be saved inside the `scraped_sites` folder.

---

## ⚠️ Warning
- Scraping websites without permission may violate **legal and ethical guidelines**. Always check the site's `robots.txt` file and **terms of service**.
- This tool is intended for **educational purposes** only. The authors are not responsible for any misuse.

---

## 📢 Disclaimer
This tool is provided **as-is** without any warranty. Use it responsibly and respect website policies. The developers are not liable for any damages resulting from its usage.

---

## 📬 Contact
If you have questions, suggestions, or issues, feel free to open an issue on the GitHub repository!

**Happy Scraping!** 🕸️🚀
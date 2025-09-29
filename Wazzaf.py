from bs4 import BeautifulSoup as bs           # For parsing HTML pages
from urllib.request import urlopen            # For opening URLs
import csv                                    # For writing data to CSV files
import pandas as pd                           # For previewing the scraped data
import math                                   # For ceiling calculation of total pages

# ============================================================
# 🌐 INITIAL URL (page 1) — Last week jobs for "Data Analyst"
# ============================================================
base_url = 'https://wuzzuf.net/search/jobs/?a=navbg&filters%5Bpost_date%5D%5B0%5D=within_1_week&q=data%20analyst&start=0'

#function to get info from the website
def getinfo(container, tagName, attributeName, attributeValue):
    info = container.findAll(tagName, {attributeName: attributeValue})
    return info[0].text.strip() if info else ""

#get the number of total pages
def getPages(soup):
    pages = soup.findAll("li", {"class": "css-18k4nsw"})
    text = pages[0].text.strip()
    parts = text.split()
    page_size = int(parts[3])
    total_num = int(parts[5])
    total_pages = math.ceil(total_num / page_size)
    return total_num, total_pages

#function to return the soup
def htmlparser(url):
    client = urlopen(url)                   # Open URL connection
    html = client.read()                         # Read the HTML content
    soup = bs(html, "html.parser")               # Parse it with BeautifulSoup
    return soup

soup = htmlparser(base_url)
# ==================================================
# 🔢 STEP 2: Find total number of jobs & pages # e.g. "Showing 1 - 15 of 395"
# ==================================================
total_num, total_pages = getPages(soup)
print(f"Total pages found: {total_pages}, with: {total_num} Job")

# ==========================================
# 📄 STEP 3: Create a CSV file for output
# ==========================================
filename = "Wazzaf.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Write header row
    writer.writerow(["Job_title", "Company_name", "Job_type", "Job_Location", "Listing_Time", "job_link"])
    # =======================================================
    # 🌀 STEP 4: Loop through all pages and scrape each one
    # =======================================================
    for pagenum in range(total_pages):
        # Build URL for each page (0, 1, 2, ...)
        url = f'https://wuzzuf.net/search/jobs/?a=navbg&filters%5Bpost_date%5D%5B0%5D=within_1_week&q=data%20analyst&start={pagenum}'
        print(f"Scraping page {pagenum+1}: {url}")

        try:
            # -------------------------------
            # 🌐 Fetch and parse each page
            # -------------------------------
            soup = htmlparser(url)

            # ======================================
            # 📌 Find all job cards on the page
            # ======================================
            containers = soup.findAll("div", {"class": "css-ghe2tq e1v1l3u10"})
            if not containers:
                print(f"No job cards found on page {pagenum+1}")
                continue

            # ======================================================
            # 📥 STEP 5: Extract information from each job container
            # ======================================================
            for container in containers:
                jobtitle = getinfo(container , "h2" , "class" , "css-193uk2c")

                # 🏢 Company Name
                # Some jobs use a different class name for the link
                # ---------------------
                cname = container.findAll("a", {"class": "css-17s97q8"})
                if not cname:
                    # older class alternative
                    cname = container.findAll("a", {"class": "css-ipsyv7"})
                company_name = cname[0].text.strip('-') if cname else ""

                job_type = getinfo(container, "span", "class", "css-uc9rga eoyjyou0")
                Ltime = container.findAll("div", {"class": "css-1jldrig"})
                if not Ltime:
                    # alternative class
                    Ltime = container.findAll("div", {"class": "css-eg55jf"})
                listing_time = Ltime[0].text.strip() if Ltime else ""
                job_location = getinfo(container, "span", "class", "css-16x61xq")
                job_link = getinfo(container, "a", "class", "css-o171kl")

                # ✍️ Write the scraped data to CSV file
                # ------------------------------------
                writer.writerow([jobtitle, company_name, job_type, job_location, listing_time, job_link])

        except Exception as e:
            # Handle any error during page scraping
            print(f"Error on page {pagenum+1}: {e}")

# ============================================
# ✅ STEP 6: Scraping finished — Preview data
# ============================================
print(f"\n✅ Scraping finished. All data saved to {filename}")

# Read the CSV file to check the first few rows
df = pd.read_csv(filename)
print(df.head())

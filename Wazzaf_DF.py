# =============================
# 📌 IMPORT REQUIRED LIBRARIES
# =============================
from bs4 import BeautifulSoup as bs           # For parsing HTML pages
from urllib.request import urlopen            # For opening URLs
import pandas as pd                           # For working with data as DataFrames
import math                                   # For ceiling calculation of total pages

# ============================================================
# 🌐 INITIAL URL (page 1) — Last week jobs for "Data Analyst"
# ============================================================
base_url = 'https://wuzzuf.net/search/jobs/?a=navbg&filters%5Bpost_date%5D%5B0%5D=within_1_week&q=data%20analyst&start=0'

# ====================================
# 🌟 STEP 1: Open the first page to
# determine total number of pages
# ====================================
def htmlparser(url):
    client = urlopen(url)                   # Open URL connection
    html = client.read()                         # Read the HTML content
    soup = bs(html, "html.parser")               # Parse it with BeautifulSoup
    return soup

soup = htmlparser(base_url)
# ==================================================
# 🔢 STEP 2: Find total number of jobs & pages
# e.g. "Showing 1 - 15 of 395"
# ==================================================
pages = soup.findAll("li", {"class": "css-18k4nsw"})  # Find the text containing pagination info
text = pages[0].text                                # Extract the text
parts = text.split()                                # Split into words
page_size = int(parts[3])                           # "15" in "Showing 1 - 15 of 395"
total_num = int(parts[5])                           # "395" in "Showing 1 - 15 of 395"
total_pages = math.ceil(total_num / page_size)      # Calculate total pages

print(f"Total pages found: {total_pages} with {total_num} Job")

# ======================================================
# 📄 STEP 3: Create an empty list to store scraped data
# ======================================================
jobs_data = []  # Will hold dictionaries for each job row

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

            # 🧠 Job Title
            jtitle = container.findAll("h2", {"class": "css-193uk2c"})
            jobtitle = jtitle[0].text.strip() if jtitle else ""

            # 🏢 Company Name
            cname = container.findAll("a", {"class": "css-17s97q8"})
            if not cname:
                cname = container.findAll("a", {"class": "css-ipsyv7"})
            company_name = cname[0].text.strip('-') if cname else ""

            # 📋 Job Type
            jtype = container.findAll("span", {"class": "css-uc9rga eoyjyou0"})
            job_type = jtype[0].text.strip() if jtype else ""

            # 🕒 Listing Time
            Ltime = container.findAll("div", {"class": "css-1jldrig"})
            if not Ltime:
                Ltime = container.findAll("div", {"class": "css-eg55jf"})
            listing_time = Ltime[0].text.strip() if Ltime else ""

            # 📍 Location
            location = container.findAll("span", {"class": "css-16x61xq"})
            job_location = location[0].text.strip() if jtype else ""

            # 🔗 Job Link
            jlink = container.findAll("a", {"class": "css-o171kl"})
            job_link = jlink[0].get("href")

            # ➕ Add the job as a dictionary to the list
            jobs_data.append({
                "Job_title": jobtitle,
                "Company_name": company_name,
                "Job_type": job_type,
                "Job_Location": job_location,
                "Listing_Time": listing_time,
                "job_link": job_link
            })

    except Exception as e:
        # Handle any error during page scraping
        print(f"Error on page {pagenum+1}: {e}")

# =========================================================
# ✅ STEP 5: Convert collected data into a Pandas DataFrame
# =========================================================
df = pd.DataFrame(jobs_data)
print("\n✅ Scraping finished. DataFrame created successfully!")
print(df.head())

# Optional: Show basic DataFrame info
print("\nDataFrame Info:")
print(df.info())

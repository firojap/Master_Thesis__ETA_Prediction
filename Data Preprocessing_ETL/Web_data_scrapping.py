from bs4 import BeautifulSoup
import requests
import schedule
import time
import os
from datetime import datetime, timedelta
import concurrent.futures


os.chdir('C:\\Users\\firoj\\OneDrive\\Desktop\\Thesis')

BASE_URL = "https://www.pegelonline.wsv.de"


waterway_url_map = {
    "WESER": "WESER",
    "MITTELLANDKANAL": "MITTELLANDKANAL"
}

data_url_map = {
    "Water temperature": "Wassertemperatur+Rohdaten",
    "Water level": "Wasserstand+Rohdaten",
    "Wind direction": "WINDRICHTUNG",
    "Wind speed": "WINDGESCHWINDIGKEIT",
    "Wave period": "Wellenperiode",
    "Turbidity": "Trübung",
    "Significant wave height": "SignifikanteWellenhöhe",
    "Raw Oxygen Data": "SignifikanteWellenhöhe",
    "Maximum wave height": "MAXIMALEWELLENHÖHE",
    "Electrical conductivity raw data": "ELEKTRISCHE_LEITFÄHIGKEIT_ROHDATEN",
    "Air temperature raw data": "Lufttemperatur+Rohdaten",
    "Chloride": "CHLORID"
}

data_categories_by_waterway = {
    "WESER": [
        "Water temperature",
        "Water level",
        "Wind direction",
        "Wind speed",
        "Wave period",
        "Turbidity",
        "Significant wave height",
        "Raw Oxygen Data",
        "Maximum wave height",
        "Electrical conductivity raw data",
    ],
    "MITTELLANDKANAL": [
        "Water temperature",
        "Water level",
        "Wind direction",
        "Wind speed",
        "Air temperature raw data",
        "Chloride",
    ],
}

downloaded_csv_count = 0


def get_create_folder_name(parent_folder, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code != 200:
        print(
            f"Failed to get response from {url}. Status code: {response.status_code}")
        return

    p_elements = soup.find_all("p")

    for p_element in p_elements:
        a_element = p_element.find(
            "a", href="/webservices/files/", string="Root")
        if a_element:
            break

    a_elements = p_element.find_all("a")
    last_a_text = a_elements[-1].text

    subfolder_path = os.path.join(parent_folder, last_a_text)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"Created subfolder {subfolder_path}.")
    return subfolder_path


def download_data(waterway_names, data_categories, folder_date=None):

    data_categories_folder_name = data_categories
    if not os.path.exists(data_categories_folder_name):
        os.makedirs(data_categories_folder_name)
        print(f"Created folder {data_categories_folder_name}.")

    waterway_folder_name = os.path.join(
        data_categories_folder_name, waterway_names)
    if not os.path.exists(waterway_folder_name):
        os.makedirs(waterway_folder_name)
        print(f"Created folder {waterway_folder_name}.")

    data_url = data_url_map.get(data_categories)
    waterway_url = waterway_url_map.get(waterway_names)

    WESER_url = f"{BASE_URL}/webservices/files/{data_url}/{waterway_url}"
    print(WESER_url)
    response = requests.get(WESER_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # print(data_url)
        # print(waterway_url)
        table = soup.find("table", class_="filelisting")
        folder_links = [link["href"]
                        for link in table.find_all("a", href=True)]
        print(folder_links)

        def process_folder_link(folder_link):
            global downloaded_csv_count
            WESER_folder_url = f"{BASE_URL}/{folder_link}"
            # print(f"{WESER_folder_url} for folder link")
            sub_folder_name = get_create_folder_name(
                waterway_folder_name, WESER_folder_url)

            WESER_folder_date_url = f"{WESER_folder_url}/{folder_date}"
            # print(f"{WESER_folder_date_url} for folder date url")
            sub_folder_name = get_create_folder_name(
                sub_folder_name, WESER_folder_date_url)

            csv_file_url = f"{WESER_folder_date_url}/down.csv"
            response = requests.get(csv_file_url)
            if response.status_code == 200:
                save_file_name = csv_file_url.split("/")[-1]
                full_save_path = os.path.join(sub_folder_name, save_file_name)
                print(f"Downloading data from {csv_file_url}...")
                print(f"Saving data as {save_file_name}...")
                with open(full_save_path, "wb") as f:
                    f.write(response.content)
                print(
                    f"Data downloaded successfully and saved as {save_file_name}. \n\n")
                downloaded_csv_count += 1
            else:
                print("==============================================================================================================================")
                print(
                    f"2. Failed to download data. Status code: {response.status_code}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_folder_link, folder_links)
    else:
        print("==============================================================================================================================")

        print(
            f"1. Failed to download data. Status code: {response.status_code} and url: {WESER_url}")


def download_historical_data(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        for waterway_name, data_categories in data_categories_by_waterway.items():
            for data_category in data_categories:
                download_data(waterway_name, data_category,
                              current_date.strftime("%d.%m.%Y"))
        current_date += timedelta(days=1)


# Download historical data from last 4 days
start_date = datetime.now() - timedelta(days=3)
end_date = datetime.now()

start_time = time.time()  # Record the start time

download_historical_data(start_date, end_date)
# download_data("WESER", "Turbidity", "05.05.2023")
# download_data("WESER", "Water temperature", "05.05.2023")
# download_data("MITTELLANDKANAL", "Water temperature", "05.05.2023")
# download_data("MITTELLANDKANAL", "Chloride", "05.05.2023")

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time

print(f"Total downloaded CSV files: {downloaded_csv_count}")
print(f"Time elapsed: {elapsed_time:.2f} seconds")


def job():
    print("Starting the download process...")
    current_date = datetime.now().strftime("%d.%m.%Y")
    download_data(current_date)


# Schedule the script to run every day
schedule.every().day.at("00:00").do(job)

# Keep the script running
while True:
    print(
        f"Checking for scheduled tasks at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    schedule.run_pending()
    time.sleep(60)
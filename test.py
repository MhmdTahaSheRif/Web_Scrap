import statistics
import re
import pyodbc
import undetected_chromedriver as uc
import streamlit as st
import pandas as pd
import io
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from io import BytesIO
from datetime import date, datetime


arabic_names = {
    "Alexandria": "محافظه الاسكندريه",
    "sidi-gaber": "سيدي جابر",
    "manshiyya": "قسم المنشيه",
    "moharam-bik": "قسم محرم بك",
    "dekheila": "قسم الدخيله",
    "Aswan": "محافظة أسوان",
    "Cairo": "محافظه القاهره",
    "badr-city": "قسم بدر",
    "Sharqia": "محافظه الشرقيه",
    "abu-talat": "أبو تلات",
    "agami": "العجمي",
    "al-hadrah": "الحضرة",
    "abu-qir": "أبو قير",
    "abou-al-reish": "أبو الريش",
    "abou-simbel": "أبو سمبل",
    "aswan-city": "مدينة أسوان",
    "basiliah": "بصيلية",
    "15-may-city": "مايو",
    "abasiya": "العباسية",
    "ain-shams": "عين شمس",
    "hadayek-al-kobba": "حدائق القبه",
    "zagazig": "مركز الزقازيق",
    "10th-of-ramadan": "اول العاشر من رمضان",
    "deyerb-negm": "مركز ديرب نجم",
    "hihya": "مركز ههيا",
    "kafr-saqr": "مركز كفر صقر",
    "alqnayat": "القنايات",
    "Properties": "عقارات",
    "Lands": "أراضي",
    "monufia": "محافظه المنوفيه",
    "menouf": "مركز منوف",
    "shebin-al-koum": "مركز شبين الكوم",
    "berket-al-sabaa": "مركز بركه السبع",
    "faqous": "مركز فاقوس",
    "bilbeis": "مركز بلبيس",
    "Buildings and Lands": "أراضي",
    "Commercial Properties": "عقارات",
    "Residential Properties": "عقارات",
    "Residential Apartments": "عقارات",
    "Nasr City":"قسم مدينه نصر ",
    "new-administrative-capital":"قسم بدر",
"Residential":"عقارات",
"Commercial":"عقارات",
}

filter_mapping = {
    "apartments-duplex-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7"
    },
    "buildings-lands-other": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

ASSET_SUB_TYPE_MAPPING = {
    "apartments-duplex-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "buildings-lands-other": ["مبني سكني", "مبني"]
}

# ------------------ SMSARKO-SPECIFIC MAPPINGS ------------------

smsarko_property_types = {
    "Residential Apartments": "apartments-for-sale",
    "Commercial Properties": "commercial-for-sale",
    "Lands": "lands-for-sale"
}


filter_mapping_smsarko = {
    "apartments-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7",
    },
    "lands-for-sale": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

smsarko_asset_sub_mapping = {
    "apartments-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "lands-for-sale": ["مبني سكني", "مبني"]
}

smsarko_governorates = {
    "Alexandria": ["qesm-el-manshia", "el-sahel-el-shamaly-1"],
    "Cairo": ["nasr-city", "new-administrative-capital"]  # Add more if needed
}

smsarko_location_dict = {
    "qesm-el-manshia": "قسم المنشية",
    "el-sahel-el-shamaly-1": "الساحل الشمالي 1",
    "nasr-city": "مدينة نصر",
    "new-administrative-capital": "قسم بدر",
    "helwan": "حلوان"
}


# ------------------ AQARMAP-SPECIFIC MAPPINGS ------------------
aqarmap_property_types = {
    "Commercial": "commercial",
    "Apartment": "apartment",
    "Land or Farm": "land-or-farm"
}
filter_mapping_smsarko = {
    "apartments-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7"
    },
    "lands-for-sale": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

aqarmap_ASSET_SUB_TYPE_MAPPING = {
    "apartments-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "lands-for-sale": ["مبني سكني", "مبني"]
}

aqarmap_governorates = {
    "Alexandria": ["moharram-bey"],
    "Cairo": ["cairo"],
    "Sharqia": ["zagazig"],
    "monufia": ["monufia"],
}

# ------------------ DRIVER SETUP & UTILITY FUNCTIONS ------------------




def setup_driver():
    chrome_path = r'C:\Users\edge-t\appdata\roaming\undetected_chromedriver\undetected_chromedriver.exe'

    # Attempt to remove the driver file if it exists.
    if os.path.exists(chrome_path):
        try:
            os.remove(chrome_path)
        except Exception as e:
            # Log the exception so you know why removal failed.
            print(f"Could not remove file at {chrome_path}: {e}")
            # Depending on your needs, you might want to either:
            # - exit the function early, or
            # - continue without removal.
            # For now, we continue.


    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/132.0.0.0 Safari/537.36')

    try:
        driver = uc.Chrome(options=options, version_main=132, use_subprocess=True)
    except FileExistsError as fee:
        # If a FileExistsError occurs, attempt removal again.
        print(f"FileExistsError encountered: {fee}. Trying to remove the file again.")
        if os.path.exists(chrome_path):
            try:
                os.remove(chrome_path)
            except Exception as e:
                print(f"Second attempt to remove {chrome_path} failed: {e}")
        driver = uc.Chrome(options=options, version_main=132, use_subprocess=True)

    return driver


def extract_number(text, min_val, max_val):
    cleaned = re.sub(r"[^\d.]", "", text)
    cleaned = cleaned.replace('²', '')
    if cleaned:
        try:
            number = float(cleaned)
            if min_val <= number <= max_val:
                return number
        except ValueError:
            return None
    return None

# ------------------ SCRAPING FUNCTIONS ------------------

def get_listing_elements(driver):
    candidate_xpaths = [
        "//div[contains(@class, '_357a9937')]",
        "//div[contains(@class, 'listing-item')]",
        "//div[contains(@class, '_948d9e0a')]",
        "//article[.//span[contains(text(), 'EGP')]]",
        "//div[contains(@class, 'sc-') and .//span[contains(text(), 'EGP')]]"
    ]
    for xpath in candidate_xpaths:
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            valid_elements = [el for el in elements if "EGP" in el.text and any(unit in el.text for unit in ['m²', 'SQM', 'متر'])]
            if valid_elements:
                return valid_elements
    return []

def scrape_property_data(url, is_land=False, selected_sub_type=None, use_client_filter=False, url_type=None):
    driver = setup_driver()
    property_data = []
    try:
        driver.get(url)
        time.sleep(5)
        price_selectors = [
            ".//span[contains(@class, '_95eae7db')]",
            ".//span[contains(text(), 'EGP')]",
            ".//*[contains(@class, 'price')]"
        ]
        area_selectors = [
            ".//span[contains(text(), 'SQM')]",
            ".//span[contains(text(), 'm²')]",
            ".//span[contains(@class, '_3e1113f0')]"
        ]
        listings = get_listing_elements(driver)
        for listing in listings:
            price = None
            area = None
            for selector in price_selectors:
                try:
                    price_el = listing.find_element(By.XPATH, selector)
                    price = extract_number(price_el.text, 100000, 100000000)
                    if price:
                        break
                except Exception:
                    continue
            for selector in area_selectors:
                try:
                    area_el = listing.find_element(By.XPATH, selector)
                    area = extract_number(area_el.text, 20, 1000)
                    if area:
                        break
                except Exception:
                    continue
            if price:
                if not area and is_land:
                    area = 100.0
                    st.warning("Area not found; using default value for a Buildings and Lands listing.")
                if area:
                    property_data.append((price, area))
        return property_data
    finally:
        driver.quit()

def scrape_smsarko_data(url):
    driver = setup_driver()
    property_data = []
    try:
        driver.get(url)
        time.sleep(5)
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                price_el = article.find_element(By.CSS_SELECTOR, "div.badge.text-bg-success.fs-6.fw-light")
                area_el = article.find_element(By.CSS_SELECTOR, "div.badge.text-bg-dark.fs-6.fw-light")
                price = extract_number(price_el.text, 100000, 100000000)
                area = extract_number(area_el.text, 20, 1000)
                if price and area:
                    property_data.append((price, area))
            except Exception:
                continue
        return property_data
    finally:
        driver.quit()




def scrape_aqarmap_data(url):
    """
    Scrape Aqarmap listings from the given URL.

    This function:
      - Waits for listing cards to load.
      - Scrolls down to trigger lazy-loading.
      - For each listing card, attempts to locate the details link,
        then extracts the price and area information.
    Returns:
      A list of (price, area) tuples.
    """
    driver = setup_driver()  # Ensure your driver is correctly set up.
    property_data = []
    try:
        driver.get(url)

        # Wait until at least one listing card is present.
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'listing-card')]")))

        # Scroll down to load any lazy-loaded content.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Find all listing cards.
        cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'listing-card')]")
        for index, card in enumerate(cards, start=1):
            try:
                # Look for the details anchor that should contain the text details.
                details_links = card.find_elements(
                    By.XPATH, ".//a[contains(@class, 'p-2x') and starts-with(@href, '/en/listing/')]"
                )
                if not details_links:
                    print(f"Card {index}: No details link found in this card.")
                    continue
                details_link = details_links[0]

                # Locate the price element.
                price_elems = details_link.find_elements(
                    By.XPATH, ".//span[contains(@class, 'text-title_4')]"
                )
                if not price_elems:
                    print(f"Card {index}: No price element found in card details.")
                    continue
                price_elem = price_elems[0]
                price_text = price_elem.text.strip()
                price = extract_number(price_text, 100000, 1000000000)

                # Locate the area element using a more flexible XPath.
                area_elems = details_link.find_elements(
                    By.XPATH, ".//p[contains(., 'm²')]"
                )
                if not area_elems:
                    print(f"Card {index}: No area element found in card details.")
                    continue
                area_elem = area_elems[0]
                area_text = area_elem.text.strip()
                area = extract_number(area_text, 20, 10000)

                if price is not None and area is not None:
                    property_data.append((price, area))
            except Exception as e:
                print(f"Card {index}: Error processing a card:", e)
                continue

        return property_data
    except Exception as general_e:
        print("General error during scraping:", general_e)
        return property_data
    finally:
        driver.quit()


def calculate_metrics(data):
    if not data:
        return None
    prices, areas = zip(*data)
    avg_price = statistics.mean(prices)
    avg_area = statistics.mean(areas)
    return {
        'avg_price': avg_price,
        'avg_area': avg_area,
        'avg_price_per_m2': avg_price / avg_area,
        'median_price': statistics.median(prices),
        'sample_size': len(data)
    }

# ------------------ REPORT FUNCTIONS ------------------

def save_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    governorate_arabic = arabic_names.get(governorate, governorate)
    city_arabic = arabic_names.get(city, city)
    property_type_arabic = arabic_names.get(property_type, property_type)
    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics['avg_price_per_m2']],
        'Rent per m²': [metrics['avg_price_per_m2'] / (12 * 20)],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }
    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "dubizzle_report.xlsx")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save report: {e}")
        return None, None
    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df

def save_smsarko_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    governorate_arabic = arabic_names.get(governorate, governorate)
    city_arabic = smsarko_location_dict.get(city, city)
    property_type_arabic = arabic_names.get(property_type, property_type)
    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics['avg_price_per_m2']],
        'Rent per m²': [metrics['avg_price_per_m2'] / (12 * 20)],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }
    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "smsarko_report.xlsx")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save SMSARKO report: {e}")
        return None, None
    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df





aqarmap_property_types = {
    "Residential": "apartment",
    "Commercial": "commercial",
    "Lands": "land-or-farm"
}

aqarmap_asset_sub_mapping = {
    "apartment": ["غرفة", "وحدة سكنية"],
    "commercial": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "land-or-farm": ["مبني سكني", "مبني"]
}

aqarmap_governorates = {
    "Cairo": ["Nasr City", "Heliopolis","new-administrative-capital"],
    "Alexandria": ["Smouha", "Stanley"]
}

# Dummy Arabic names mapping (for demonstration)



# --- Dummy implementation of save_aqarmap_report_excel ---
def save_aqarmap_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    # Convert names to Arabic using our helper function:
    property_type_arabic = convert_to_arabic(property_type)
    governorate_arabic = convert_to_arabic(governorate)
    city_arabic = convert_to_arabic(city)

    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics.get('avg_price_per_m2', 0)],
        'Rent per m²': [metrics.get('avg_price_per_m2', 0) / (12 * 20) if metrics.get('avg_price_per_m2', 0) else 0],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }

    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "aqarmap_report.xlsx")

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save Aqarmap report: {e}")
        return None, None

    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df


# ------------------ DATABASE FUNCTIONS ------------------

def get_db_connection():
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=omar-pc;'
        'DATABASE=EAMS_R2_01_copy;'
        'UID=sa;'
        'PWD=P@ssw0rd;'
        'TrustServerCertificate=yes;'
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        st.error(f"Failed to connect to SQL Server: {e}")
        return None

def fetch_all_matching_assets_by_keys(asset_type_desc, asset_sub_type_desc, governorate_name, section_name):
    conn = get_db_connection()
    if not conn:
        return None
    query = """
    SELECT a.asset_id, a.final_area_m2, a.ASSET_TYPE_DESC, 
           a.ASSET_SUB_TYPE_DESC, a.GOVERNORATE_NAME, a.SECTION_NAME
    FROM dbo.v_assets_aream2 a
    WHERE LOWER(LTRIM(RTRIM(a.ASSET_TYPE_DESC))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.ASSET_SUB_TYPE_DESC))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.GOVERNORATE_NAME))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.SECTION_NAME))) = LOWER(?)
    """
    try:
        cursor = conn.cursor()
        st.write("Fetching assets with keys:")
        st.write("Asset Type:", asset_type_desc)
        st.write("Asset Sub-Type:", asset_sub_type_desc)
        st.write("Governorate:", governorate_name)
        st.write("Section:", section_name)
        cursor.execute(query, (asset_type_desc, asset_sub_type_desc, governorate_name, section_name))
        results = cursor.fetchall()
        st.write("Found", len(results), "matching assets in view.")
        return results
    except Exception as e:
        st.error(f"Error fetching assets by keys: {e}")
        return None
    finally:
        conn.close()

def process_assets_batch(assets, price_per_m2, rent_per_m2):
    conn = get_db_connection()
    if not conn:
        return None
    current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    processed_count = {'updated': 0}
    try:
        cursor = conn.cursor()
        update_query = """
            UPDATE [EVAL].[ASSETS_EVALUATE]
            SET SITE_MONTHLY_VALUE_EGP = ?,
                SITE_MARKTING_VALUE_EGP = ?,
                SITE_EVAL_DATE = ?,
                DATE_MODIFIED = GETDATE()
            WHERE ASSET_ID = ?
        """
        batch_size = 50
        total_assets = len(assets)
        st_progress_container = st.empty()
        for i in range(0, total_assets, batch_size):
            batch = assets[i:i + batch_size]
            params = []
            for asset in batch:
                asset_id = asset[0]
                final_area_m2 = float(asset[1]) if asset[1] is not None else 100.0
                site_marketing_value = final_area_m2 * float(price_per_m2)
                site_monthly_value = final_area_m2 * float(rent_per_m2)
                params.append((site_monthly_value, site_marketing_value, current_date, asset_id))
                processed_count['updated'] += 1
            cursor.executemany(update_query, params)
            conn.commit()
            progress = (i + len(batch)) / total_assets
            st_progress_container.progress(progress)
            st_progress_container.write(f"Updated {i + len(batch)} of {total_assets} assets")
            time.sleep(0.05)
        st.success(f"Successfully updated {processed_count['updated']} assets")
        return processed_count
    except Exception as e:
        st.error(f"Database operation failed: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def convert_to_arabic(name, lowercase_lookup=False):
    """
    Converts the provided name to Arabic using the arabic_names dictionary.
    If `lowercase_lookup` is True, the lookup key is forced to lowercase.
    """
    key = name.lower() if lowercase_lookup else name
    return arabic_names.get(key, name)


# -------------------------------------------------------


def main():
    st.set_page_config(page_title="Property Market Analysis", layout="wide")
    st.title("🏡 Property Market Analysis")
    st.markdown("### Analyze property prices and land rates in Egypt")
    source_options = ["Dubizzle", "SMSARKO", "Aqarmap"]
    selected_source = st.radio("Select Data Source:", source_options)

    if selected_source == "Dubizzle":
        property_types = {
            "Residential Properties": "apartments-duplex-for-sale",
            "Commercial Properties": "commercial-for-sale",
            "Buildings and Lands": "buildings-lands-other"
        }
        governorates_list = {
            "Alexandria": ["moharam-bik", "dekheila", "sidi-gaber", "manshiyya"],
            "Cairo": ["badr-city", "hadayek-al-kobba", "15-may-city"],
            "Sharqia": ["zagazig", "10th-of-ramadan", "deyerb-negm", "faqous", "bilbeis", "hihya", "kafr-saqr"],
            "monufia": ["menouf", "shebin-al-koum", "berket-al-sabaa"],
        }
        property_type = st.selectbox("🏠 Select property type:", list(property_types.keys()), index=0)
        url_type = property_types[property_type]
        asset_sub_options = ASSET_SUB_TYPE_MAPPING.get(url_type, [])
        selected_sub_type = st.selectbox("🔎 Select asset sub-type filter:", asset_sub_options) if asset_sub_options else ""
        default_sub_type = selected_sub_type if selected_sub_type.strip() != "" else "غير محدد"
        selected_governorate = st.selectbox("🌍 Select a governorate:", list(governorates_list.keys()), index=0)
        selected_city = st.selectbox("🏙️ Select a city:", governorates_list[selected_governorate], index=0)
        city_slug = selected_city.lower().replace(" ", "-")
        base_url = f"https://www.dubizzle.com.eg/en/properties/{url_type}/{city_slug}/"
        url = base_url
        if default_sub_type != "غير محدد" and selected_sub_type in filter_mapping.get(url_type, {}):
            filter_code = filter_mapping[url_type][selected_sub_type]
            url = f"{base_url}?filter={filter_code}"
        st.write("Using URL:", url)
        if st.button("📊 Analyze Market Prices (Dubizzle)"):
            with st.spinner("Scraping Dubizzle market data..."):
                data = scrape_property_data(url,
                                            is_land=(url_type == "buildings-lands-other"),
                                            selected_sub_type=selected_sub_type,
                                            use_client_filter=True,
                                            url_type=url_type)
                if not data:
                    st.error("❌ No listings found matching the filter! Check your search criteria or website structure.")
                    return
                metrics = calculate_metrics(data)
                if metrics:
                    st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                    st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                    df_prices = pd.DataFrame(data, columns=['Price', 'Area'])
                    st.subheader("Market Price Distribution")
                    st.line_chart(df_prices['Price'])

                    # Convert the names to Arabic using the helper function (or directly via the dictionary)
                    arabic_property_type = convert_to_arabic(property_type)
                    arabic_governorate = convert_to_arabic(selected_governorate)
                    arabic_city = convert_to_arabic(selected_city)

                    buffer, report_df = save_report_excel(
                        arabic_property_type,
                        arabic_governorate,
                        arabic_city,
                        metrics,
                        default_sub_type
                    )

                    if buffer is not None:
                        st.download_button(
                            label=f"📥 Download {property_type} Report",
                            data=buffer,
                            file_name="dubizzle_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                        st.write("### Current Dubizzle Data (Saved in dubizzle_report.xlsx)")
                        st.dataframe(report_df)
                        st.session_state["dubizzle_report_df"] = report_df
                        st.session_state["dubizzle_metrics"] = metrics
                        st.session_state["dubizzle_governorate"] = selected_governorate
                        st.session_state["dubizzle_city"] = selected_city
                        st.session_state["dubizzle_asset_sub"] = default_sub_type
        if "dubizzle_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (Dubizzle)"):
                with st.spinner("Updating Dubizzle assets in database..."):
                    metrics = st.session_state["dubizzle_metrics"]
                    selected_governorate = st.session_state["dubizzle_governorate"]
                    selected_city = st.session_state["dubizzle_city"]
                    excel_data = {
                        'asset_type_desc': convert_to_arabic(
                            'أراضي' if url_type == "buildings-lands-other" else 'عقارات'),
                        'asset_sub_type': default_sub_type,
                        'governorate_name': convert_to_arabic(selected_governorate),  # uses key as is
                        'section_name': convert_to_arabic(selected_city, lowercase_lookup=True),
                        # forces lowercase lookup
                        'price_per_m2': metrics.get('avg_price_per_m2', 0),
                        'rent_per_m2': metrics.get('avg_price_per_m2', 0) / (12 * 20)
                    }

                    matching_assets = fetch_all_matching_assets_by_keys(
                        excel_data['asset_type_desc'],
                        excel_data['asset_sub_type'],
                        excel_data['governorate_name'],
                        excel_data['section_name']
                    )
                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"Found {len(matching_assets)} matching Dubizzle assets to update")
                        result = process_assets_batch(matching_assets,
                                                      excel_data['price_per_m2'],
                                                      excel_data['rent_per_m2'])
                        if result:
                            st.success(f"✅ Updated {result['updated']} Dubizzle assets in database")
                        else:
                            st.error("❌ Failed to update Dubizzle assets")
                    else:
                        st.warning("No Dubizzle assets found for the selected criteria.")

    elif selected_source == "SMSARKO":
        # ------------------ SMSARKO SECTION ------------------
        st.subheader("SMSARKO Scraping Settings")
        smsarko_property = st.selectbox("🏠 Select SMSARKO property type:", list(smsarko_property_types.keys()))
        smsarko_property_value = smsarko_property_types[smsarko_property]
        smsarko_asset_sub_options = smsarko_asset_sub_mapping.get(smsarko_property_value, [])
        smsarko_selected_asset_sub = st.selectbox("🔎 Select SMSARKO asset sub-type filter:", smsarko_asset_sub_options) if smsarko_asset_sub_options else ""
        smsarko_default_sub = smsarko_selected_asset_sub if smsarko_selected_asset_sub.strip() != "" else "غير محدد"
        smsarko_selected_governorate = st.selectbox("🌍 Select SMSARKO governorate:", list(smsarko_governorates.keys()))
        smsarko_selected_city = st.selectbox("🏙️ Select SMSARKO city:", smsarko_governorates[smsarko_selected_governorate])
        smsarko_city_slug = smsarko_selected_city
        url = f"https://www.smsarko.com/search/{smsarko_property_value}/{smsarko_city_slug}"
        st.write("Using URL:", url)
        if st.button("📊 Analyze Market Prices (SMSARKO)"):
            with st.spinner("Scraping SMSARKO market data..."):
                data = scrape_smsarko_data(url)
                if not data:
                    st.error("❌ No SMSARKO listings found!")
                    return
                metrics = calculate_metrics(data)
                if metrics:
                    st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                    st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                    df_prices = pd.DataFrame(data, columns=['Price', 'Area'])
                    st.subheader("SMSARKO Market Price Distribution")
                    st.line_chart(df_prices['Price'])
                    buffer, report_df = save_smsarko_report_excel(smsarko_property, smsarko_selected_governorate, smsarko_selected_city,
                                                                  metrics, smsarko_default_sub)
                    if buffer is not None:
                        st.download_button(
                            label=f"📥 Download SMSARKO {smsarko_property} Report",
                            data=buffer,
                            file_name="smsarko_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                        st.write("### Current SMSARKO Data (Saved in smsarko_report.xlsx)")
                        st.dataframe(report_df)
                        st.session_state["smsarko_report_df"] = report_df
                        st.session_state["smsarko_metrics"] = metrics
                        st.session_state["smsarko_governorate"] = smsarko_selected_governorate
                        st.session_state["smsarko_city"] = smsarko_selected_city
                        st.session_state["smsarko_asset_sub"] = smsarko_default_sub
        if "smsarko_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (SMSARKO)"):
                with st.spinner("Updating SMSARKO assets in database..."):
                    metrics = st.session_state["smsarko_metrics"]
                    selected_governorate = st.session_state["smsarko_governorate"]
                    selected_city = st.session_state["smsarko_city"]
                    excel_data = {
                        'asset_type_desc': 'أراضي' if smsarko_property_value == "lands-for-sale" else 'عقارات',
                        'asset_sub_type': smsarko_default_sub,
                        'governorate_name': arabic_names.get(selected_governorate, selected_governorate),
                        'section_name': convert_to_arabic(selected_city, lowercase_lookup=True),
                        'price_per_m2': metrics.get('avg_price_per_m2', 0),
                        'rent_per_m2': metrics.get('avg_price_per_m2', 0) / (12 * 20)
                    }
                    matching_assets = fetch_all_matching_assets_by_keys(
                        excel_data['asset_type_desc'],
                        excel_data['asset_sub_type'],
                        excel_data['governorate_name'],
                        excel_data['section_name']
                    )
                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"Found {len(matching_assets)} matching SMSARKO assets to update")
                        result = process_assets_batch(matching_assets,
                                                      excel_data['price_per_m2'],
                                                      excel_data['rent_per_m2'])
                        if result:
                            st.success(f"✅ Updated {result['updated']} SMSARKO assets in database")
                        else:
                            st.error("❌ Failed to update SMSARKO assets")
                    else:
                        st.warning("No SMSARKO assets found for the selected criteria.")

    elif selected_source == "Aqarmap":
        st.subheader("Aqarmap Scraping Settings")

        aqarmap_property = st.selectbox("🏠 Select Aqarmap property type:", list(aqarmap_property_types.keys()))
        aqarmap_property_value = aqarmap_property_types[aqarmap_property]

        aqarmap_asset_sub_options = aqarmap_asset_sub_mapping.get(aqarmap_property_value, [])
        if aqarmap_asset_sub_options:
            aqarmap_selected_asset_sub = st.selectbox("🔎 Select Aqarmap asset sub-type filter:", aqarmap_asset_sub_options)
        else:
            aqarmap_selected_asset_sub = "غير محدد"
        aqarmap_default_sub = aqarmap_selected_asset_sub if aqarmap_selected_asset_sub.strip() != "" else "غير محدد"

        aqarmap_selected_governorate = st.selectbox("🌍 Select Aqarmap governorate:", list(aqarmap_governorates.keys()))

        aqarmap_selected_city = st.selectbox("🏙️ Select Aqarmap city:", aqarmap_governorates[aqarmap_selected_governorate])
#https://aqarmap.com.eg/en/for-sale/land-or-farm/cairo/el-marg/
        aqarmap_governorate_slug = aqarmap_selected_governorate.lower().replace(" ", "-")
        aqarmap_city_slug = aqarmap_selected_city.lower().replace(" ", "-")
        base_url = f"https://aqarmap.com.eg/en/for-sale/{aqarmap_property_value}/{aqarmap_governorate_slug}/{aqarmap_city_slug}/"


        st.write("Using URL:", base_url)

        if st.button("📊 Analyze Market Prices (Aqarmap)"):
            with st.spinner("Scraping Aqarmap market data..."):
                data = scrape_aqarmap_data(base_url)
                if not data:
                    st.error("❌ No Aqarmap listings found!")
                    return
                metrics = calculate_metrics(data)
                if metrics:
                    st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                    st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                    df_prices = pd.DataFrame(data, columns=['Price', 'Area'])
                    st.subheader("Aqarmap Market Price Distribution")
                    st.line_chart(df_prices['Price'])
                    buffer, report_df = save_aqarmap_report_excel(
                        aqarmap_property,
                        aqarmap_selected_governorate,
                        aqarmap_selected_city,
                        metrics,
                        aqarmap_default_sub
                    )
                    if buffer is not None:
                        st.download_button(
                            label="📥 Download Aqarmap Report",
                            data=buffer,
                            file_name="aqarmap_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                        st.write("### Current Aqarmap Data")
                        st.dataframe(report_df)
                        st.session_state["aqarmap_report_df"] = report_df
                        st.session_state["aqarmap_metrics"] = metrics
                        st.session_state["aqarmap_governorate"] = aqarmap_selected_governorate
                        st.session_state["aqarmap_city"] = aqarmap_selected_city
                        st.session_state["aqarmap_asset_sub"] = aqarmap_default_sub
                        st.session_state["aqarmap_property_value"] = aqarmap_property_value

        if "aqarmap_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (Aqarmap)"):
                with st.spinner("Updating Aqarmap assets in database..."):
                    metrics = st.session_state["aqarmap_metrics"]
                    selected_governorate = st.session_state["aqarmap_governorate"]
                    selected_city = st.session_state["aqarmap_city"]
                    aqarmap_property_value = st.session_state["aqarmap_property_value"]
                    aqarmap_asset_sub = st.session_state["aqarmap_asset_sub"]
                    asset_type_desc = 'أراضي' if aqarmap_property_value == "lands-for-sale" else 'عقارات'
                    matching_assets = fetch_all_matching_assets_by_keys(
                        asset_type_desc,
                        aqarmap_asset_sub,
                        arabic_names.get(selected_governorate, selected_governorate),
                        arabic_names.get(selected_city, selected_city)
                    )
                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"Found {len(matching_assets)} matching Aqarmap assets to update")
                        result = process_assets_batch(matching_assets,
                                                      metrics.get('avg_price_per_m2', 0),
                                                      metrics.get('avg_price_per_m2', 0) / (12 * 20))
                        if result:
                            st.success(f"✅ Updated {result['updated']} Aqarmap assets in database")
                        else:
                            st.error("❌ Failed to update Aqarmap assets")
                    else:
                        st.warning("No Aqarmap assets found for the selected criteria.")
# In your main() function (or wherever appropriate), add the button:

    # Set BASE_PATH to your desired directory
    BASE_PATH = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"

    st.markdown("---")
    st.subheader("Final Report Generation")

    if all(key in st.session_state for key in ["dubizzle_report_df", "smsarko_report_df", "aqarmap_report_df"]):
        if st.button("✨ Generate Final Report"):
            with st.spinner("Processing final report..."):
                # Retrieve dataframes from session state
                dubizzle_df = st.session_state["dubizzle_report_df"]
                smsarko_df = st.session_state["smsarko_report_df"]
                aqarmap_df = st.session_state["aqarmap_report_df"]

                # Define required columns
                required_columns = [
                    'ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME',
                    'SECTION_NAME', 'Price per m²', 'Rent per m²', 'Date'
                ]
                dfs = {'Dubizzle': dubizzle_df, 'SMSARKO': smsarko_df, 'Aqarmap': aqarmap_df}

                # Check for missing columns
                for name, df in dfs.items():
                    missing = [col for col in required_columns if col not in df.columns]
                    if missing:
                        st.error(f"❌ {name} report is missing columns: {', '.join(missing)}")
                        return

                # Helper function to extract unique grouping keys
                def get_groups(df):
                    return set(df[['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME']].apply(tuple, axis=1))

                # Get unique groups for each dataframe
                dubizzle_groups = get_groups(dubizzle_df)
                smsarko_groups = get_groups(smsarko_df)
                aqarmap_groups = get_groups(aqarmap_df)

                # Find common groups across all three reports
                common_groups = dubizzle_groups & smsarko_groups & aqarmap_groups

                if not common_groups:
                    st.error("❌ No common entries found across all three reports!")
                    return

                # Combine data from all three reports for common groups
                combined_dfs = []
                for df in [dubizzle_df, smsarko_df, aqarmap_df]:
                    # Create a temporary 'Group' column for filtering
                    df['Group'] = df[['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME']].apply(tuple,
                                                                                                           axis=1)
                    filtered = df[df['Group'].isin(common_groups)]
                    combined_dfs.append(filtered.drop(columns=['Group']))

                combined_df = pd.concat(combined_dfs, ignore_index=True)

                # Ensure numeric columns are correctly typed
                numeric_cols = ['Price per m²', 'Rent per m²']
                for col in numeric_cols:
                    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

                # Group by key columns and compute the averages
                grouped = combined_df.groupby(
                    ['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME', 'SECTION_NAME']
                ).agg({
                    'Price per m²': 'mean',
                    'Rent per m²': 'mean'
                }).reset_index()

                # Add current date and reorder columns
                grouped['Date'] = date.today().strftime('%Y-%m-%d')
                final_df = grouped[['ASSET_TYPE_DESC', 'GOVERNORATE_NAME', 'SECTION_NAME',
                                    'Price per m²', 'Rent per m²', 'Date', 'ASSET_SUB_TYPE_DESC']]

                # Save to Excel in a BytesIO buffer for the download button
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Final Report')
                buffer.seek(0)

                # Save the final report to the specified file path
                file_path = os.path.join(BASE_PATH, "final_report.xlsx")
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Final Report')

                st.success("✅ Final report generated and saved successfully!")

                st.download_button(
                    label="📥 Download Final Report",
                    data=buffer,
                    file_name="final_report.xlsx",
                    mime="application/vnd.ms-excel"
                )
                st.write("### Final Report Preview")
                st.dataframe(final_df)


if __name__ == "__main__":
    main()

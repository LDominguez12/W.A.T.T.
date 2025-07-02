from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page(accept_downloads=True)
    page.goto("https://power.larc.nasa.gov/data-access-viewer/")

    page.wait_for_timeout(5000)

    page.get_by_label('Community').select_option('RE')
    page.get_by_label('Temporal').select_option('Daily')
    page.get_by_label('Latitude').fill('35.1')
    page.get_by_label('Longitude').fill('-106.5')

    page.wait_for_selector('#time_daily')

    start_date = "06/23/2004"
    end_date = "06/24/2004"

    page.evaluate(f"""
        const datePicker = document.querySelector("#time_daily");
        datePicker.value = "{start_date},{end_date}";
        datePicker.dispatchEvent(new Event('calciteInputDatePickerChange'));""")
    
    page.get_by_label('Parameters').select_option('WS2M')
    page.get_by_label('Parameters').select_option('T2M')
    page.get_by_label('Parameters').select_option('RH2M')

    page.get_by_label('Format').select_option('CSV')

    with page.expect_download() as download_info:
        page.get_by_role('button', name = 'Submit').click()

    download = download_info.value

    download_path = Path("Code/test_data.csv")
    download.save_as(download_path)

    print(f"File downloaded to: {download_path}")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)

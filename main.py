from playwright.sync_api import sync_playwright, Playwright
import time
import os
from dotenv import load_dotenv
import pandas as pd 

load_dotenv()
USERNAME = os.getenv("USERNAME_HISQIS")
PASSWORD = os.getenv("PASSWORD_HISQIS")

df_hisqis = pd.DataFrame({
    "Prüfungsnr.": [],
    "Prüfungstext": [],
    "Semester": [],
    "Note": [],
    "Punkte": [],
    "Status": [],
    "SWS": [],
    "Bonus": [],
    "Vermerk": [],
    "Versuch": [],
    "Prüfungsdatum": [],
})

def run(playwright: Playwright):
    chromium = playwright.chromium 
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://qis.dez.tu-dresden.de/qisserver/servlet/de.his.servlet.RequestDispatcherServlet?state=user&type=0&category=menu.browse&startpage=portal.vm")
    page.locator("#asdf").fill(USERNAME)
    page.locator("#fdsa").fill(PASSWORD)
    page.locator("[type=submit]").click()
    page.get_by_text('Prüfungsbescheinigungen (HTML, PDF)').click()
    page.get_by_alt_text("Leistungen für Abschluss 11 Diplom anzeigen").click()
    
    stuff = page.locator("//body//table[2]//tbody//tr[3]//td[3]") 
    print(stuff.inner_text())
    
    # for row in range(3,10):
    #     for col in range(0,12):
    #         stuff = page.locator(f"xpath=//body//table[2]//tbody//tr[{row}]//td[{col}]") 
    #         print(stuff.inner_text())
    #time.sleep(5)
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
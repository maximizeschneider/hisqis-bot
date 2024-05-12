from playwright.sync_api import sync_playwright, Playwright
import time
import os
from dotenv import load_dotenv
import pandas as pd 

load_dotenv()
USERNAME = os.getenv("USERNAME_HISQIS")
PASSWORD = os.getenv("PASSWORD_HISQIS")


def get_grades():
    with sync_playwright() as playwright:
        chromium = playwright.chromium 
        browser = chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://qis.dez.tu-dresden.de/qisserver/servlet/de.his.servlet.RequestDispatcherServlet?state=user&type=0&category=menu.browse&startpage=portal.vm")
        page.locator("#asdf").fill(USERNAME)
        page.locator("#fdsa").fill(PASSWORD)
        page.locator("[type=submit]").click()
        page.get_by_text('Prüfungsbescheinigungen (HTML, PDF)').click()
        page.get_by_alt_text("Leistungen für Abschluss 11 Diplom anzeigen").click()
        
        # load table fully 
        page.wait_for_selector("//body//table[2]") 
        table = page.locator("//body//table[2]")
        
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
        
        rows = table.locator("tbody > tr").element_handles()
        for row_index, row in enumerate(rows[2:]): # first two are not data
            # fetch all cells within this row
            row_content = []
            cells = row.query_selector_all("td")
            for cell_index, cell in enumerate(cells):
                # Get the text from each cell
                text = cell.inner_text()
                row_content.append(text)
            
            df_hisqis.loc[len(df_hisqis)] = row_content    
        page.locator("//body//div[@id='visual-footer-wrapper']//a[5]").click() # logout
        browser.close()
        
        return df_hisqis

df_old = pd.read_csv('data.csv')
df_new = get_grades()
print(df_new.dtypes)
#df_new.dtypes()
#df = df[df["Prüfungsnr."].str[-2:].isin(["10", "20", "30", "40", "50", "60"])]



from playwright.sync_api import sync_playwright, Playwright
import time
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("USERNAME_HISQIS")
PASSWORD = os.getenv("PASSWORD_HISQIS")


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://qis.dez.tu-dresden.de/qisserver/servlet/de.his.servlet.RequestDispatcherServlet?state=user&type=0&category=menu.browse&startpage=portal.vm")
    page.locator("#asdf").fill(USERNAME)
    page.locator("#fdsa").fill(PASSWORD)
    page.locator("[type=submit]").click()
    page.locator(':has-text(""Prüfungsbescheinigungen (HTML, PDF)"').click()
    time.sleep(5)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
import asyncio
import datetime
from playwright.async_api import async_playwright
import smtplib
from email.mime.text import MIMEText


netid = ""  
password = ""
permit_category = "Garage Parking Permits"
permit_name = "2024-2025 Garage Specific"
permit_locations = ["(SEC) Second Street Garage : General"]
parking_url = "https://arizona.aimsparking.com/permits/?cmd=new"

smtp_server = ''
smtp_port = 587
smtp_username = ''
smtp_password = ''
from_address = ''
to_address = ''

async def login(page, use_duo=True):
    await page.fill('#username', netid)
    await page.fill('#password', password)
    await page.click('.btn.btn-primary.btn-block:has-text("Login")')

    if page.get_by_text("Remember me for 30 days"):
        print_red("Need two-factor authentication.")
        if use_duo:
            await page.click('button:has-text("Yes, this is my device")')
        else:
            # hardware key, not tested
            await page.select_option('select[name="device"]', 'Token')
            await page.click('fieldset[data-device-index="token"] button#passcode')

async def detect_garage_parking_permits(page):
    await page.click(f'label:has-text("{permit_category}")')
    await page.click(f'label:has-text("{permit_name}")')

    await page.wait_for_selector('div:has-text("Please Select a Location")')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for location in permit_locations:
        location_element = await page.query_selector(f'label:has-text("{location}")')
        parent_location_element = await location_element.evaluate_handle('(element) => element.parentElement')
        is_disabled = await parent_location_element.evaluate('(element) => element.className.includes("disable")')

        print(f"{timestamp}: ", end="")
        if is_disabled:
            print_red(location, addon=" is not available.")
        else:
            print_green(location, addon=" is available.")
            send_email(location)
            print("Email sent.")
            await page.click(f'label:has-text("{location}")')
            await page.wait_for_timeout(1000*60*15)

    filename = f"garage_{timestamp}.png"
    await page.screenshot(path="log/"+filename, full_page=True)
    await page.reload()

async def run(playwright, headless, reload_time=60):
    browser = await playwright.webkit.launch(headless=headless)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(parking_url)

    try:
        await page.wait_for_selector("#login_permit_type", timeout=5000)
        await page.click("#login_permit_type")
    except:
        print("Cannot go to the login page.")

    await page.click('.btn.btn-primary:has-text("Login")')

    if page.get_by_text("Log in with your NetID and Password"):
        print("Login in required.")
        await login(page)

    await page.wait_for_selector('div:has-text("Account #")')
    await page.click('.btn.btn-default:has-text("Get Permits")')

    while True:
        await detect_garage_parking_permits(page)
        await asyncio.sleep(reload_time)
        await page.reload()
        is_reload_success = await page.wait_for_selector('div:has-text("Permit Category")')
        if is_reload_success is None:
            print_red("Alert: Permit Category not found after refreshing page.")

async def main():
    async with async_playwright() as playwright:
        await run(playwright, headless=True)

def send_email(garage_type):
    message = MIMEText(f"{garage_type} is now available!")
    message['Subject'] = f"{garage_type} is available"
    message['From'] = from_address
    message['To'] = to_address

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, to_address.split(','), message.as_string())

def print_red(text, addon=""):
    print("\033[91m {}\033[00m".format(text) + addon)

def print_green(text, addon=""):
    print("\033[92m {}\033[00m".format(text) + addon)

if __name__ == "__main__":
    asyncio.run(main())
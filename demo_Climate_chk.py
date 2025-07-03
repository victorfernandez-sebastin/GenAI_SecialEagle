from playwright.sync_api import sync_playwright

CITY = "Chennai"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Step 1: Visit weather.com
    page.goto("https://weather.com", timeout=60000)

    # Step 2: Accept cookies (if shown)
    try:
        page.locator("button:has-text('Accept')").click(timeout=5000)
    except:
        pass  # Safe to ignore if not shown

    # Step 3: Click the search icon (top right)
    try:
        page.locator("#headerSearch_LocationSearch_input").click(timeout=8000)
    except:
        print("❌ Could not find search icon.")

    # Step 4: Search for city
    search_input = page.locator("#headerSearch_LocationSearch_input")
    search_input.wait_for(timeout=10000)
    search_input.fill(CITY)
    page.keyboard.press("Enter")

    # Step 5: Wait for weather data
    temp_locator = page.locator("#WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034 > div > section > div > div > div.CurrentConditions--body--r20G9 > div.CurrentConditions--primary--A\+Brf > div > div.CurrentConditions--tempIconContainer--mWt\+L > span.CurrentConditions--tempValue--zUBSz")
    desc_locator = page.locator("#WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034 > div > section > div > div > div.CurrentConditions--body--r20G9 > div.CurrentConditions--primary--A\+Brf > div > div.CurrentConditions--phraseValue---VS-k")

    temp_locator.wait_for(timeout=15000)
    temperature = temp_locator.inner_text()
    description = desc_locator.inner_text()

    # Step 6: Output result
    print(f"\n📍 Weather in {CITY}")
    print(f"🌡️ Temperature: {temperature}")
    print(f"🌤️ Condition: {description}\n")

    browser.close()

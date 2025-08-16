from re import A

import click
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.webdriver.common.appiumby import AppiumBy
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.extensions.android.nativekey import AndroidKey

def swipe(driver, start_x, start_y, end_x, end_y, duration=0):
    touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=touch_input)
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    if duration > 0:
        actions.w3c_actions = ActionBuilder(
            driver, mouse=touch_input, duration=duration
        )
    actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def tap(driver, x, y):
    touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=touch_input)
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pointer_up()
    actions.perform()


def send_keys_with_keycode(driver, text):
    """
    Send multiple keystrokes using `driver.press_keycode`.
    :param driver: Appium driver instance
    :param text: Text string to be typed
    """
    # Mapping from characters to Android keycodes
    keycode_map = {
        "a": AndroidKey.A,
        "b": AndroidKey.B,
        "c": AndroidKey.C,
        "d": AndroidKey.D,
        "e": AndroidKey.E,
        "f": AndroidKey.F,
        "g": AndroidKey.G,
        "h": AndroidKey.H,
        "i": AndroidKey.I,
        "j": AndroidKey.J,
        "k": AndroidKey.K,
        "l": AndroidKey.L,
        "m": AndroidKey.M,
        "n": AndroidKey.N,
        "o": AndroidKey.O,
        "p": AndroidKey.P,
        "q": AndroidKey.Q,
        "r": AndroidKey.R,
        "s": AndroidKey.S,
        "t": AndroidKey.T,
        "u": AndroidKey.U,
        "v": AndroidKey.V,
        "w": AndroidKey.W,
        "x": AndroidKey.X,
        "y": AndroidKey.Y,
        "z": AndroidKey.Z,
        " ": AndroidKey.SPACE,
    }

    for char in text.lower():
        if char in keycode_map:
            driver.press_keycode(keycode_map[char])
        else:
            print(f"Character '{char}' is not supported and will be skipped.")

def find_element_by_text(driver, text):
    """
    Find an element by text using UiAutomator2's `text` locator strategy.
    :param driver: Appium driver instance
    :param text: Text string to be matched
    :return: WebElement object
    """
    return driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'text("{text}")')


def click_donate_more_button(driver):
    """
    Click the 'Donate More' button if it exists and is clickable.
    """
    donate_more_button_id = "com.oceanwing.battery.cam:id/tv_donation_more"

    try:
        # Wait for the 'Donate More' button to be clickable
        donate_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, donate_more_button_id))
        )

        # Log details for debugging
        print(f"'Donate More' button found with properties:")
        print(f"Clickable: {donate_more_button.get_attribute('clickable')}")
        print(f"Displayed: {donate_more_button.get_attribute('displayed')}")

        # Click the button
        donate_more_button.click()
        print("Clicked on 'Donate More' button.")
        time.sleep(2)  # Small delay after the click
    except Exception as e:
        print(f"Error interacting with 'Donate More' button: {e}")


from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def donate_videos(driver):
    """
    Select 9 videos at a time, click the donate button, wait 2 minutes, and select Donate More.
    Repeat until no more videos are available. Navigate to the previous day if no videos are left.
    """
    # Locators
    base_xpath = '//android.widget.ImageView[@resource-id="com.oceanwing.battery.cam:id/item_history_select_icon"]'
    donate_button_id = "com.oceanwing.battery.cam:id/tv_start_donation"
    donate_more_button_id = "com.oceanwing.battery.cam:id/tv_donation_more"
    prev_day_button_id = "com.oceanwing.battery.cam:id/iv_pre_day"

    donated_videos = []  # Track indices of donated videos
    index = 1  # Initialize index for video selection

    def click_donate_more_button():
        """
        Click the 'Donate More' button if it exists and is clickable.
        """
        try:
            donate_more_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((AppiumBy.ID, donate_more_button_id))
            )
            donate_more_button.click()
            print("Clicked on 'Donate More' button.")
            time.sleep(2)  # Small delay after clicking
        except Exception as e:
            print(f"Error interacting with 'Donate More' button: {e}")
            raise

    def click_donate_button():
        """
        Click the 'Donate' button to start the donation process.
        """
        try:
            donate_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((AppiumBy.ID, donate_button_id))
            )
            donate_button.click()
            print("Clicked on 'Donate' button. Waiting for 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes after donating
        except Exception as e:
            print(f"Error interacting with 'Donate' button: {e}")
            raise

    def navigate_to_previous_day():
        """
        Navigate to the previous day's videos.
        """
        try:
            prev_day_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((AppiumBy.ID, prev_day_button_id))
            )
            prev_day_button.click()
            print("Navigated to the previous day.")
            time.sleep(2)  # Small delay after navigation
        except Exception as e:
            print(f"No previous day button found or not clickable: {e}")
            return False  # Indicate that no previous day is available
        return True

    while True:
        # Select up to 9 videos
        selected_videos = []
        for _ in range(9):
            xpath = f"({base_xpath})[{index}]"
            try:
                # Skip already donated videos
                if index in donated_videos:
                    index += 1
                    continue

                # Wait for the video element to appear
                video_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, xpath))
                )
                video_element.click()
                selected_videos.append(index)
                print(f"Selected video {index}")
                index += 1
                time.sleep(1)  # Delay to mimic human interaction
            except Exception as e:
                print(f"No more videos to select or interact with: {e}")
                break

        if not selected_videos:
            print("No videos left on the current page. Checking for previous day...")
            if not navigate_to_previous_day():
                print("No more previous days available. Exiting donation process.")
                break
            index = 1  # Reset index for the new day
            continue

        # Click the Donate button
        try:
            click_donate_button()
        except Exception:
            print("Unable to complete donation. Exiting.")
            break

        # Click the Donate More button
        try:
            click_donate_more_button()
            index = 1  # Reset index for the next batch
        except Exception:
            print("No 'Donate More' button found. Exiting donation process.")
            break

    print("Donation process completed.")
    return donated_videos


# Define capabilities
capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "Android",
    "language": "en",
    "locale": "US",
    "uiautomator2ServerInstallTimeout": 60000,
}

# Appium server URL
appium_server_url = "http://localhost:4723"

# Open session
driver = webdriver.Remote(
    command_executor=appium_server_url,
    options=UiAutomator2Options().load_capabilities(capabilities),
)

# Print session ID
print(f"Appium session started with ID: {driver.session_id}")

actions = ActionChains(driver)
# override as 'touch' pointer action
actions.w3c_actions = ActionBuilder(
    driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
)

# Swipe up from the bottom of the screen
swipe(driver, 100, 2200, 100, 1500)

time.sleep(2)

# Wait for the search bar element to be present and visible
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (AppiumBy.ID, "com.sec.android.app.launcher:id/app_search_edit_text")
    )
)

# Click on the search bar
search_bar.click()
time.sleep(2)

send_keys_with_keycode(driver, "eufy Security")
time.sleep(2)

# Find the Eufy Security app in the search results
eufy_app = find_element_by_text(driver, "eufy Security")
eufy_app.click()
time.sleep(5)

# Click on hamburger menu
hamburger_menu = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (AppiumBy.ID, "com.oceanwing.battery.cam:id/main_home_personal")
    )
)
hamburger_menu.click()
time.sleep(2)

# Click on 'Enhance My AI' option
enhance_my_ai = find_element_by_text(driver, "Enhance My AI")
enhance_my_ai.click()
time.sleep(5)

# Click on "Donate" button with index 0
donate_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (AppiumBy.XPATH, '(//android.widget.Button[@text="Donate"])[1]')
    )
)
donate_button.click()
time.sleep(2)

donate_video_list = donate_videos(driver)


# Keep the session open
input("Press Enter to quit the session...")

# Close session
driver.quit()

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os

BASE_URL = "http://localhost:3000"  # Update if needed


def wait_for_table(driver):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tbody"))
    )


def click_movie_row(driver, movie_title):
    links = driver.find_elements(By.CSS_SELECTOR, "tbody tr td a")
    for link in links:
        if movie_title in link.text:
            link.click()
            return
    raise Exception(f"Movie title '{movie_title}' not found in the list!")


def scroll_to_element(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element
    )


def save_screenshot(driver, prefix):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{prefix}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")


# Test 1: Sort by title
def test_sort_movies_by_title_and_last_is_phantom_menace(driver):
    driver.get(BASE_URL)
    wait_for_table(driver)
    driver.find_element(By.XPATH, "//th[contains(.,'Title')]").click()
    wait_for_table(driver)
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    last_row = rows[-1]
    last_movie_title = last_row.find_elements(By.TAG_NAME, "td")[0].text
    assert last_movie_title == "The Phantom Menace"


# Test 2: Species validation with logs
def test_species_for_empire_strikes_back_contains_wookie(driver):
    try:
        driver.get(BASE_URL)
        wait_for_table(driver)
        click_movie_row(driver, "The Empire Strikes Back")

        print("Navigated to 'The Empire Strikes Back' details page")

        species_header = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Species')]"))
        )

        scroll_to_element(driver, species_header)
        print("Scrolled to 'Species' section")

        species_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//h1[contains(text(),'Species')]/ancestor::div/following-sibling::ul/li")
            )
        )

        species = [e.text.strip() for e in species_elements]
        print("Species found:", species)

        wookie_found = any("Wookie" in s or "Wookiee" in s for s in species)

        if wookie_found:
            print("Wookie/Wookiee is present in species list!")
        else:
            print("Wookie/Wookiee not found in species list!")

        assert wookie_found, "Wookie or Wookiee not found in species list!"
        save_screenshot(driver, "species_passed")

    except Exception as e:
        save_screenshot(driver, "species_failed")
        raise


# Test 3: Negative validation for planets with logs
def test_camino_not_in_phantom_menace_planets(driver):
    try:
        driver.get(BASE_URL)
        wait_for_table(driver)
        click_movie_row(driver, "The Phantom Menace")

        print("Navigated to 'The Phantom Menace' details page")

        phontom_header = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Planets')]"))
        )
        scroll_to_element(driver, phontom_header)
        print("📜 Scrolled to 'Planets' section")

        phontom_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//h1[contains(text(),'Planets')]/ancestor::div/following-sibling::ul/li")
            )
        )

        planets = [e.text.strip() for e in phontom_elements]
        print("🔍 Planets found:", planets)

        camino_found = any("Camino" in p for p in planets)

        if camino_found:
            print("Camino is present in planets list!")
        else:
            print("Camino is NOT present in planets list!")

        assert not camino_found, "Camino should NOT be in The Phantom Menace planets list!"
        save_screenshot(driver, "planets_passed")

    except Exception as e:
        save_screenshot(driver, "planets_failed")
        raise

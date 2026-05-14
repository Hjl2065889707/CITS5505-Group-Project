import socket
import threading

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from werkzeug.serving import make_server

from app import create_app, db
from app.models import Post, User
from config import TestConfig


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("selenium-db") / "catchlog-selenium.db"
    upload_dir = tmp_path_factory.mktemp("selenium-uploads")

    class SeleniumTestConfig(TestConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        UPLOAD_FOLDER = str(upload_dir)

    test_app = create_app(SeleniumTestConfig)

    with test_app.app_context():
        db.create_all()
        user = User(username="selenium_user", email="selenium@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.flush()
        db.session.add_all([
            Post(
                user_id=user.id,
                content="Selenium trout catch",
                category="Catch Report",
                species="Trout",
                location_name="Swan River",
            ),
            Post(
                user_id=user.id,
                content="Selenium gear review",
                category="Gear Review",
                species=None,
                location_name="Fremantle",
            ),
        ])
        db.session.commit()

    port = _free_port()
    server = make_server("127.0.0.1", port, test_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def browser():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Selenium Chrome driver is not available: {exc}")

    yield driver
    driver.quit()


@pytest.fixture()
def driver(browser):
    browser.delete_all_cookies()
    return browser


def wait(driver, seconds=5):
    return WebDriverWait(driver, seconds)


def login(driver, base_url):
    driver.get(f"{base_url}/login")
    wait(driver).until(EC.presence_of_element_located((By.ID, "username_or_email")))
    driver.find_element(By.ID, "username_or_email").send_keys("selenium_user")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, ".auth-submit").click()
    wait(driver).until(EC.url_to_be(f"{base_url}/"))


def visible_feed_posts(driver):
    return [
        item for item in driver.find_elements(By.CSS_SELECTOR, ".feed-post-item")
        if item.is_displayed()
    ]


def test_feed_page_shows_create_search_and_category_controls(driver, live_server):
    driver.get(f"{live_server}/")

    assert driver.find_element(By.CSS_SELECTOR, ".create-post-btn").is_displayed()
    assert driver.find_element(By.ID, "searchInput").is_displayed()
    tag_labels = [tag.text for tag in driver.find_elements(By.CSS_SELECTOR, ".tag")]
    assert "Catch Report" in tag_labels
    assert "Gear Review" in tag_labels


def test_feed_search_filters_visible_posts(driver, live_server):
    driver.get(f"{live_server}/")
    search = driver.find_element(By.ID, "searchInput")
    search.clear()
    search.send_keys("trout")

    wait(driver).until(lambda current: len(visible_feed_posts(current)) == 1)
    assert "Selenium trout catch" in visible_feed_posts(driver)[0].text


def test_feed_category_filter_hides_other_categories(driver, live_server):
    driver.get(f"{live_server}/")
    gear_button = next(
        tag for tag in driver.find_elements(By.CSS_SELECTOR, ".tag")
        if tag.text == "Gear Review"
    )
    gear_button.click()

    wait(driver).until(lambda current: len(visible_feed_posts(current)) == 1)
    assert "Selenium gear review" in visible_feed_posts(driver)[0].text


def test_logged_out_create_post_redirects_to_login(driver, live_server):
    driver.get(f"{live_server}/create-post")

    wait(driver).until(EC.url_contains("/login"))
    assert "Log in" in driver.page_source


def test_logged_in_user_can_open_create_post_page(driver, live_server):
    login(driver, live_server)
    driver.get(f"{live_server}/create-post")

    wait(driver).until(EC.presence_of_element_located((By.ID, "postText")))
    assert driver.find_element(By.ID, "postCategory").is_displayed()
    assert driver.find_element(By.ID, "locationMap").is_displayed()


def test_logged_in_user_can_create_post_and_see_it_on_feed(driver, live_server):
    login(driver, live_server)
    driver.get(f"{live_server}/create-post")
    wait(driver).until(EC.presence_of_element_located((By.ID, "postText")))

    driver.find_element(By.ID, "postText").send_keys("Selenium created feed post")
    Select(driver.find_element(By.ID, "postCategory")).select_by_visible_text("General")
    driver.find_element(By.CSS_SELECTOR, ".catch-details summary").click()
    driver.find_element(By.ID, "postSpecies").send_keys("Bream")
    driver.find_element(By.ID, "postLocation").send_keys("Canning River")
    driver.find_element(By.CSS_SELECTOR, ".post-btn").click()

    wait(driver).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    wait(driver).until(EC.url_to_be(f"{live_server}/"))
    wait(driver).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#feedContainer"),
            "Selenium created feed post",
        )
    )

    assert "Bream" in driver.find_element(By.ID, "feedContainer").text
    assert "Canning River" in driver.find_element(By.ID, "feedContainer").text

"""Selenium (end-to-end) tests for Profile & Interaction features.

Owner: Hjl2065889707

Covers:
  1. Profile page shows user info
  2. Profile tab switching (My Posts ↔ Saved Posts)
  3. Post detail page shows content and comments
  4. Like button updates on click
  5. Add comment on post detail page
  6. Settings page saves profile changes
"""

import socket
import threading

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server

from app import create_app, db
from app.models import Comment, Post, SavedPost, User
from config import TestConfig


# ── Helpers ───────────────────────────────────────────────────────────


def _free_port():
    """Find an available port on localhost."""
    # Create a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Binding to port 0 tells the OS to randomly assign an unused port
        sock.bind(("127.0.0.1", 0))
        # Retrieve the assigned port number from the socket info tuple
        return sock.getsockname()[1]


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    """Start a real Flask server in a background thread with test data."""
    # tmp_path_factory is a built-in Pytest fixture that creates auto-cleaned temporary directories.
    db_path = tmp_path_factory.mktemp("selenium-db") / "test.db"
    upload_dir = tmp_path_factory.mktemp("selenium-uploads")

    class SeleniumTestConfig(TestConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        UPLOAD_FOLDER = str(upload_dir)

    test_app = create_app(SeleniumTestConfig)

    with test_app.app_context():
        db.create_all()

        # Create two users
        user = User(username="selenium_user", email="sel@example.com")
        user.set_password("password123")
        other = User(username="selenium_other", email="other@example.com")
        other.set_password("password123")
        db.session.add_all([user, other])
        # flush() sends the SQL to the database to generate IDs (like post2.id)
        db.session.flush()

        # Post by selenium_user (id=1)
        post1 = Post(
            user_id=user.id,
            content="My fishing trip to Swan River",
            category="Catch Report",
            species="Trout",
            location_name="Swan River",
        )
        # Post by selenium_other (id=2) — will be saved by selenium_user
        post2 = Post(
            user_id=other.id,
            content="Other user general post",
            category="General",
        )
        db.session.add_all([post1, post2])
        db.session.flush()

        # selenium_user saves other's post (for Saved Posts tab)
        db.session.add(SavedPost(user_id=user.id, post_id=post2.id))

        # A comment on post1 by other user
        db.session.add(
            Comment(user_id=other.id, post_id=post1.id, content="Nice catch!")
        )
        db.session.commit()

    port = _free_port()
    server = make_server("127.0.0.1", port, test_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    # Tell the server to stop accepting requests
    server.shutdown()
    # Wait up to 5 seconds for the background thread to finish shutting down cleanly
    thread.join(timeout=5)
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


# scope="module" tells Pytest to only launch the browser ONCE for this entire file.
# Starting Chrome is slow and resource-heavy, so sharing it across tests saves a lot of time.
@pytest.fixture(scope="module")
def browser():
    """Launch a headless Chrome browser (shared across all tests in this module)."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Chrome driver not available: {exc}")

    yield driver
    driver.quit()


@pytest.fixture()
def driver(browser):
    """Fresh session for each test (clears cookies)."""
    browser.delete_all_cookies()
    return browser


def wait(driver, seconds=5):
    """Shorthand for WebDriverWait."""
    return WebDriverWait(driver, seconds)


def login(driver, base_url):
    """Log in as selenium_user via the login page."""
    # Instruct the browser to navigate to the login URL
    driver.get(f"{base_url}/login")
    
    # Wait until the browser finishes rendering the page and the input field is actually in the DOM
    wait(driver).until(EC.presence_of_element_located((By.ID, "username_or_email")))
    
    # Simulate a user typing into the input fields
    driver.find_element(By.ID, "username_or_email").send_keys("selenium_user")
    driver.find_element(By.ID, "password").send_keys("password123")
    
    # Simulate clicking the submit button
    driver.find_element(By.CSS_SELECTOR, ".auth-submit").click()
    
    # Wait until the login is successful and the server redirects us to the home page ("/")
    wait(driver).until(EC.url_to_be(f"{base_url}/"))


# ── Test 1: Profile page shows user info ──────────────────────────────


def test_profile_page_shows_user_info(driver, live_server):
    """The profile page should display the user's name and follow stats."""
    login(driver, live_server)
    driver.get(f"{live_server}/profile")

    wait(driver).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".username")))
    assert "selenium_user" in driver.find_element(By.CSS_SELECTOR, ".username").text
    assert driver.find_element(By.CSS_SELECTOR, ".follow-stats").is_displayed()


# ── Test 2: Profile tab switching ─────────────────────────────────────


def test_profile_tabs_switch(driver, live_server):
    """Clicking 'Saved Posts' tab should show saved posts and hide My Posts."""
    login(driver, live_server)
    driver.get(f"{live_server}/profile")

    # Click "Saved Posts" tab
    saved_tab = wait(driver).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.nav-tab[data-target="saved-posts"]')
        )
    )
    saved_tab.click()

    # Saved posts content should become visible
    wait(driver).until(EC.visibility_of_element_located((By.ID, "saved-posts")))

    # My Posts should be hidden
    my_posts = driver.find_element(By.ID, "my-posts")
    assert not my_posts.is_displayed()


# ── Test 3: Post detail shows content and comments ────────────────────


def test_post_detail_shows_content_and_comments(driver, live_server):
    """The post detail page should display the post body and existing comments."""
    driver.get(f"{live_server}/posts/1")

    wait(driver).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".post-card__body"))
    )
    assert "My fishing trip" in driver.find_element(
        By.CSS_SELECTOR, ".post-card__body"
    ).text
    assert "Nice catch!" in driver.find_element(By.ID, "comment-list").text


# ── Test 4: Like button updates on click ──────────────────────────────


def test_like_button_updates_on_click(driver, live_server):
    """Clicking the like button should fill the heart icon and increment the count."""
    login(driver, live_server)
    driver.get(f"{live_server}/posts/1")

    like_btn = wait(driver).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".like-btn"))
    )
    old_count = int(like_btn.find_element(By.CSS_SELECTOR, ".like-count").text)

    like_btn.click()

    # Wait for the icon to change to solid (liked state)
    wait(driver).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".like-btn .fa-solid.fa-heart")
        )
    )
    new_count = int(like_btn.find_element(By.CSS_SELECTOR, ".like-count").text)
    assert new_count == old_count + 1


# ── Test 5: Add comment on post detail ────────────────────────────────


def test_add_comment_on_post_detail(driver, live_server):
    """Submitting a comment should dynamically add it to the comment list."""
    login(driver, live_server)
    driver.get(f"{live_server}/posts/1")

    comment_input = wait(driver).until(
        EC.presence_of_element_located((By.ID, "comment-text"))
    )
    comment_input.send_keys("Selenium test comment")
    driver.find_element(By.CSS_SELECTOR, ".comment-submit-btn").click()

    # Wait for the new comment to appear in the list
    wait(driver).until(
        EC.text_to_be_present_in_element(
            (By.ID, "comment-list"), "Selenium test comment"
        )
    )


# ── Test 6: Settings page saves profile changes ──────────────────────


def test_settings_page_saves_profile(driver, live_server):
    """Updating the bio on the settings page should show a success toast."""
    login(driver, live_server)
    driver.get(f"{live_server}/settings")

    bio_input = wait(driver).until(
        EC.presence_of_element_located((By.ID, "bio"))
    )
    bio_input.clear()
    bio_input.send_keys("Avid angler from Perth")

    driver.find_element(By.ID, "saveProfileBtn").click()

    # Wait for success toast notification
    wait(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast.show"))
    )
    toast_text = driver.find_element(By.ID, "toast").text
    assert "Profile updated" in toast_text

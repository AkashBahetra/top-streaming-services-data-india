import logging
import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ============================
# CONFIGURATION
# ============================
class Config:
    """Configuration management for the streaming services tracker."""

    def __init__(self):
        # Load environment variables for multiple Trakt.tv accounts

        # Account 1: Netflix
        self.NETFLIX_CLIENT_ID = os.getenv("NETFLIX_CLIENT_ID")
        self.NETFLIX_CLIENT_SECRET = os.getenv("NETFLIX_CLIENT_SECRET")
        self.NETFLIX_ACCESS_TOKEN = os.getenv("NETFLIX_ACCESS_TOKEN")
        self.NETFLIX_REFRESH_TOKEN = os.getenv("NETFLIX_REFRESH_TOKEN")

        # Account 2: Prime Video
        self.PRIME_CLIENT_ID = os.getenv("PRIME_CLIENT_ID")
        self.PRIME_CLIENT_SECRET = os.getenv("PRIME_CLIENT_SECRET")
        self.PRIME_ACCESS_TOKEN = os.getenv("PRIME_ACCESS_TOKEN")
        self.PRIME_REFRESH_TOKEN = os.getenv("PRIME_REFRESH_TOKEN")

        # Account 3: Hotstar & Zee5
        self.OTHERS_CLIENT_ID = os.getenv("OTHERS_CLIENT_ID")
        self.OTHERS_CLIENT_SECRET = os.getenv("OTHERS_CLIENT_SECRET")
        self.OTHERS_ACCESS_TOKEN = os.getenv("OTHERS_ACCESS_TOKEN")
        self.OTHERS_REFRESH_TOKEN = os.getenv("OTHERS_REFRESH_TOKEN")

        # Other configs
        self.KIDS_LIST = os.getenv("KIDS_LIST", "False").lower() in ("true", "True")
        self.PRINT_LISTS = os.getenv("PRINT_LISTS", "False").lower() in ("true", "True")

        # Request configuration
        self.REQUEST_TIMEOUT = 30  # seconds
        self.MAX_RETRIES = 10
        self.BACKOFF_FACTOR = 2

        # Dates
        self.yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # URLs
        self.urls = {
            "netflix": "https://flixpatrol.com/top10/netflix/india/",
            "hotstar": "https://flixpatrol.com/top10/hotstar/india/",
            "zee5": "https://flixpatrol.com/top10/zee5/india/",
            "prime": "https://flixpatrol.com/top10/amazon-prime/india/",
        }

        # Section names (used by all services: Netflix, HBO, Apple, Prime, Disney)
        self.sections = {
            "movies": "TOP 10 Movies",
            "shows": "TOP 10 TV Shows",
            "overall": "TOP 10 Overall",
            "overall_hotstar": "TOP 10 Overall (in Hindi)",
        }


# ============================
# GLOBAL VARIABLES (for backward compatibility)
# ============================
config = Config()

# Netflix account credentials
NETFLIX_CLIENT_ID = config.NETFLIX_CLIENT_ID
NETFLIX_ACCESS_TOKEN = config.NETFLIX_ACCESS_TOKEN

# Prime Video account credentials
PRIME_CLIENT_ID = config.PRIME_CLIENT_ID
PRIME_ACCESS_TOKEN = config.PRIME_ACCESS_TOKEN

# Hotstar & Zee5 account credentials
OTHERS_CLIENT_ID = config.OTHERS_CLIENT_ID
OTHERS_ACCESS_TOKEN = config.OTHERS_ACCESS_TOKEN

# Other configs
KIDS_LIST = config.KIDS_LIST
PRINT_LISTS = config.PRINT_LISTS
REQUEST_TIMEOUT = config.REQUEST_TIMEOUT
MAX_RETRIES = config.MAX_RETRIES
BACKOFF_FACTOR = config.BACKOFF_FACTOR

# Top kids only available on "yesterday" page so we need to get yesterday's date
yesterday_date = config.yesterday_date

# Flixpatrol URLs
top_netflix_url = config.urls["netflix"]
top_hotstar_url = config.urls["hotstar"]
top_zee5_url = config.urls["zee5"]
top_prime_url = config.urls["prime"]

# Sections Names
top_movies_section = config.sections["movies"]
top_shows_section = config.sections["shows"]
top_overrall_section = config.sections["overall"]

# Trakt Lists Data

# Lists for Netflix (Account 1)
trakt_netflix_movies_list_data = {
    "name": "Top India Netflix Movies",
    "description": "List that contains the top 10 movies on Netflix India right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

trakt_netflix_shows_list_data = {
    "name": "Top India Netflix Shows",
    "description": "List that contains the top 10 TV shows on Netflix India right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

# Lists for Zee5 and Hotstar (Account 3)
trakt_zee5_top_list_data = {
    "name": "Top India Zee5 Overall",
    "description": "List that contains the top 10 overall content on Zee5 India right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

trakt_hotstar_top_list_data = {
    "name": "Top India Hotstar Overall",
    "description": "List that contains the top 10 overall content on Hotstar India (in Hindi) right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

# Lists for Prime Video (Account 2)
trakt_prime_movies_list_data = {
    "name": "Top India Amazon Prime Video Movies",
    "description": "List that contains the top 10 movies on Amazon Prime Video India right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

trakt_prime_shows_list_data = {
    "name": "Top India Amazon Prime Video Shows",
    "description": "List that contains the top 10 TV shows on Amazon Prime Video India right now, updated daily",
    "privacy": "public",
    "display_numbers": True,
}

# # Hotstar
# trakt_hotstar_top_list_data = {
#     "name": "Top India Hotstar Overall",
#     "description": ("List that contains the top 10 overall content on Hotstar India "
#                    "(in Hindi) right now, updated daily"),
#     "privacy": "public",
#     "display_numbers": True,
# }

# # Amazon Prime
# trakt_prime_movies_list_data = {
#     "name": "Top India Amazon Prime Movies",
#     "description": "List that contains the top 10 movies on Amazon Prime Video India right now, updated daily",
#     "privacy": "public",
#     "display_numbers": True,
# }

# trakt_prime_shows_list_data = {
#     "name": "Top India Amazon Prime Shows",
#     "description": "List that contains the top 10 TV shows on Amazon Prime Video India right now, updated daily",
#     "privacy": "public",
#     "display_numbers": True,
# }


# Trakt List slugs
trakt_netflix_movies_list_slug = "top-india-netflix-movies"
trakt_netflix_shows_list_slug = "top-india-netflix-shows"

trakt_zee5_list_slug = "top-india-zee5-overall"
trakt_hotstar_list_slug = "top-india-hotstar-overall"
trakt_prime_movies_list_slug = "top-india-amazon-prime-video-movies"
trakt_prime_shows_list_slug = "top-india-amazon-prime-video-shows"

# ============================
# HELPER METHODS
# ============================


# Get headers
def get_headers(client_id: str = None, access_token: str = None) -> Dict[str, str]:
    """Returns headers with authorization for requests.

    Args:
        client_id: The Trakt.tv client ID for the appropriate account
        access_token: The access token for the appropriate account
    """
    # Default to Netflix account if no credentials provided
    client_id = client_id or NETFLIX_CLIENT_ID
    access_token = access_token or NETFLIX_ACCESS_TOKEN

    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )

    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": client_id,
        "User-Agent": user_agent,
    }


# Print the results
def print_top_list(title: str, top_list: List[Tuple[str, str, str]]) -> None:
    logging.info("=" * 30)
    logging.info(f"{title}")
    logging.info("=" * 30)
    for rank, item_title, title_tag in top_list:
        logging.info(f"{rank}: {item_title} | {title_tag}")


# Scrape movie or show data based in the section title
def scrape_top10(url: str, section_title: str) -> Optional[List[Tuple[str, str, str]]]:
    data = []

    # Define headers to mimic a real browser
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
    headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
        "Cookie": "_nss=1",
    }

    try:
        # Send the GET request
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        # Check for a successful response
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Locate the correct section - search in document order, not heading tag order
            # This ensures we find the first occurrence in the actual HTML structure
            section_header = None

            # Find all heading tags in document order
            all_headings = soup.find_all(["h2", "h3", "h4"])

            for heading in all_headings:
                heading_text = heading.get_text(strip=True)
                # Try exact match first
                if heading_text == section_title:
                    section_header = heading
                    logging.debug(f"Found section '{section_title}' with {heading.name} tag (exact match)")
                    break
                # Try case-insensitive match
                elif heading_text.lower() == section_title.lower():
                    section_header = heading
                    logging.debug(f"Found section '{section_title}' with {heading.name} tag (case-insensitive)")
                    break

            # Check if the section was found
            if section_header:
                # All services use the same HTML structure: heading is inside a card div
                section_div = None

                # Find parent card div (heading inside card)
                parent = section_header.parent
                while parent and section_div is None:
                    if parent.name == "div" and parent.get("class") and "card" in parent.get("class"):
                        section_div = parent
                        logging.debug(f"Found card div as parent of heading for {section_title}")
                        break
                    parent = parent.parent
                    # Don't go too far up
                    if parent and parent.name == "body":
                        break

                if not section_div:
                    logging.warning(f"Could not find card div containing section header for {section_title}")
                    return data

                tbody = section_div.find("tbody")  # Locate the table body within the div
                if not tbody:
                    logging.warning(f"Could not find tbody in card div for {section_title}")
                    return data

                rows = tbody.find_all("tr")
                logging.debug(f"Found {len(rows)} rows for {section_title}")

                for row in rows:
                    try:
                        # Try to find rank with specific class, fall back to first td if not found
                        rank_td = row.find(
                            "td",
                            class_="table-td w-12 font-semibold text-right text-gray-500 table-hover:text-gray-400",
                        )
                        if not rank_td:
                            # Fallback: try to find first td element
                            rank_td = row.find("td")

                        if not rank_td:
                            logging.warning(f"Could not find rank td in row for {section_title}")
                            continue

                        rank = rank_td.get_text(strip=True)

                        # Get the anchor tag containing the title
                        title_tag = row.find("a")
                        if not title_tag:
                            logging.warning(f"Could not find title link in row for {section_title}")
                            continue

                        title = title_tag.get_text(strip=True)  # Get the movie/show title
                        title_tag_href = title_tag.get("href", "")
                        if not title_tag_href:
                            logging.warning(f"Title link has no href for {section_title}: {title}")
                            continue

                        # Extract the title tag from the href
                        title_tag_slug = title_tag_href.split("/")[-2] if len(title_tag_href.split("/")) >= 2 else ""
                        if not title_tag_slug:
                            logging.warning(f"Could not extract slug from href: {title_tag_href}")
                            continue

                        rank = rank.rstrip(".")
                        data.append(
                            (rank, title, title_tag_slug)
                        )  # Append the rank, title, and title tag to the data list
                    except Exception as row_error:
                        logging.warning(f"Error processing row in {section_title}: {row_error}")
                        continue

                logging.info(f"Scraped {len(data)} items from {section_title}")
            else:
                logging.warning(f"Could not find section header for '{section_title}' in {url}")
            return data
        else:
            logging.error(f"Failed to retrieve page {url}, status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return None


# parse items from trakt list
def parse_items(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    movies = []
    shows = []
    for item in items:
        if item["type"] == "movie":
            movie_data = {"ids": {"trakt": item["movie"]["ids"]["trakt"]}}
            movies.append(movie_data)
        elif item["type"] == "show":
            show_data = {"ids": {"trakt": item["show"]["ids"]["trakt"]}}
            shows.append(show_data)
    payload = {"movies": movies, "shows": shows}
    return payload


# Decorator to retry requests
def retry_request(func):
    def wrapper(*args, **kwargs):
        attempts = MAX_RETRIES
        for attempt in range(attempts):
            response = func(*args, **kwargs)
            if (
                response
                and response == 304
                or (hasattr(response, "status_code") and response.status_code in [200, 201])
            ):
                return response
            logging.warning(
                f"Attempt {attempt + 1} failed with {getattr(response, 'status_code', 'unknown status')}. Retrying..."
            )
            time.sleep(BACKOFF_FACTOR**attempt)
        logging.error("All attempts to update the list failed.")
        return None

    return wrapper


# ============================
# TRAKT METHODS
# ============================


# Refresh Trakt.tv access token
def refresh_token(
    client_id: str,
    client_secret: str,
    refresh_token: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Refresh a Trakt.tv access token.

    Args:
        client_id: The Trakt.tv client ID
        client_secret: The Trakt.tv client secret
        refresh_token: The refresh token to use

    Returns:
        Tuple[Optional[str], Optional[str]]: New access token and refresh token, or None if refresh failed
    """
    url = "https://api.trakt.tv/oauth/token"
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
    }

    try:
        response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            return result["access_token"], result["refresh_token"]
        else:
            logging.error(f"Token refresh failed with status {response.status_code}")
            return None, None
    except Exception as e:
        logging.error(f"Error refreshing token: {e}")
        return None, None


# Check Trakt access token
def check_token(
    client_id: str = None,
    client_secret: str = None,
    access_token: str = None,
    refresh_token: str = None,
) -> Union[bool, Tuple[Optional[str], Optional[str]]]:
    """Check if a Trakt.tv access token is valid and refresh if needed.

    Args:
        client_id: The Trakt.tv client ID to check
        client_secret: The Trakt.tv client secret
        access_token: The access token to check
        refresh_token: The refresh token to use if access token is invalid

    Returns:
        Union[bool, Tuple[Optional[str], Optional[str]]]:
            - True if token is valid
            - Tuple of new tokens if refreshed
            - (None, None) if refresh failed
    """
    # Default to Netflix account if no credentials provided
    if not all([client_id, client_secret, access_token, refresh_token]):
        client_id = config.NETFLIX_CLIENT_ID
        client_secret = config.NETFLIX_CLIENT_SECRET
        access_token = config.NETFLIX_ACCESS_TOKEN
        refresh_token = config.NETFLIX_REFRESH_TOKEN

    response = requests.get(
        "https://api.trakt.tv/users/me", headers=get_headers(client_id, access_token), timeout=REQUEST_TIMEOUT
    )

    if response.status_code == 200:
        return True
    elif response.status_code == 401:  # Unauthorized - try refreshing token
        logging.info("Access token expired, attempting refresh...")
        return refresh_token(client_id, client_secret, refresh_token)
    else:
        logging.error(f"Token check failed with status {response.status_code}")
        return None, None


# Get Trakt user's lists
def get_lists(client_id: str = None, access_token: str = None) -> List[Dict[str, Any]]:
    """Get all lists for a Trakt.tv user.

    Args:
        client_id: The Trakt.tv client ID to use
        access_token: The access token to use
    Returns:
        List[Dict[str, Any]]: List of Trakt.tv lists
    """
    response = requests.get(
        "https://api.trakt.tv/users/me/lists", headers=get_headers(client_id, access_token), timeout=REQUEST_TIMEOUT
    )
    return response.json()


# Get a list by ID
def get_list(list_id: str, client_id: str = None, access_token: str = None) -> Dict[str, Any]:
    """Get a specific Trakt.tv list.

    Args:
        list_id: ID of the list to get
        client_id: The Trakt.tv client ID to use
        access_token: The access token to use
    Returns:
        Dict[str, Any]: List details
    """
    response = requests.get(
        f"https://api.trakt.tv/users/me/lists/{list_id}",
        headers=get_headers(client_id, access_token),
        timeout=REQUEST_TIMEOUT,
    )
    return response.json()


# Get list id by slug
def get_list_id(list_slug: str) -> Optional[int]:
    lists = get_lists()
    for list in lists:
        if list["ids"]["slug"] == list_slug:
            return list["ids"]["trakt"]
    return None


# Get a list items
def get_list_items(list_id: str, client_id: str = None, access_token: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """Get items from a Trakt.tv list.

    Args:
        list_id: The ID of the list to get items from
        client_id: The Trakt.tv client ID for the appropriate account
        access_token: The access token for the appropriate account
    """
    logging.info(f"Getting items from list ID: {list_id}")
    response = requests.get(
        f"https://api.trakt.tv/users/me/lists/{list_id}/items",
        headers=get_headers(client_id, access_token),
        timeout=REQUEST_TIMEOUT,
    )
    logging.info(f"Response status code: {response.status_code}")
    logging.debug(f"Response content: {response.json()}")
    parsed_items = parse_items(response.json())
    logging.info(f"Retrieved {len(parsed_items['movies'])} movies and {len(parsed_items['shows'])} shows from list.")
    return parsed_items


# Delete a list by ID
def delete_list(list_id: str, client_id: str = None, access_token: str = None) -> int:
    """Delete a Trakt.tv list.

    Args:
        list_id: The ID of the list to delete
        client_id: The Trakt.tv client ID for the appropriate account
        access_token: The access token for the appropriate account
    """
    response = requests.delete(
        f"https://api.trakt.tv/users/me/lists/{list_id}",
        headers=get_headers(client_id, access_token),
        timeout=REQUEST_TIMEOUT,
    )
    return response.status_code


@retry_request
def create_list(list_data: Dict[str, Any], client_id: str = None, access_token: str = None) -> requests.Response:
    """Create a new list in Trakt.tv.

    Args:
        list_data: The data for creating the list
        client_id: The Trakt.tv client ID for the appropriate account
        access_token: The access token for the appropriate account
    """
    response = requests.post(
        "https://api.trakt.tv/users/me/lists",
        headers=get_headers(client_id, access_token),
        json=list_data,
        timeout=REQUEST_TIMEOUT,
    )
    if response and response.status_code == 201:
        logging.info(f"List '{list_data['name']}' created successfully.")
    return response


# Empty a list
def empty_list(list_id: str, client_id: str, access_token: str) -> int:
    logging.info("Emptying list...")
    logging.info(f"List ID: {list_id}, Client ID: {client_id}, Access Token: {access_token}")
    list_items = get_list_items(list_id)
    response = requests.post(
        f"https://api.trakt.tv/users/me/lists/{list_id}/items/remove",
        headers=get_headers(client_id, access_token),
        json=list_items,
        timeout=REQUEST_TIMEOUT,
    )
    logging.info("List emptied")
    return response.status_code


# Check necessary lists
def check_lists(config: Config) -> bool:
    """Check if lists exist, create them if they don't.

    Args:
        config: The configuration object containing account credentials
    Returns:
        bool: True if any error occurred, False otherwise
    """
    error_create = False

    # Check Netflix lists
    netflix_lists = get_lists(config.NETFLIX_CLIENT_ID, config.NETFLIX_ACCESS_TOKEN)
    netflix_slugs = [list["ids"]["slug"] for list in netflix_lists]
    logging.debug(f"Netflix lists slugs: {netflix_slugs}")

    if trakt_netflix_movies_list_slug not in netflix_slugs:
        error_create = create_list(
            trakt_netflix_movies_list_data, config.NETFLIX_CLIENT_ID, config.NETFLIX_ACCESS_TOKEN
        )
    if trakt_netflix_shows_list_slug not in netflix_slugs:
        error_create = create_list(trakt_netflix_shows_list_data, config.NETFLIX_CLIENT_ID, config.NETFLIX_ACCESS_TOKEN)

    # Check Prime Video lists
    prime_lists = get_lists(config.PRIME_CLIENT_ID, config.PRIME_ACCESS_TOKEN)
    prime_slugs = [list["ids"]["slug"] for list in prime_lists]
    logging.debug(f"Prime Video lists slugs: {prime_slugs}")

    if trakt_prime_movies_list_slug not in prime_slugs:
        error_create = create_list(trakt_prime_movies_list_data, config.PRIME_CLIENT_ID, config.PRIME_ACCESS_TOKEN)
    if trakt_prime_shows_list_slug not in prime_slugs:
        error_create = create_list(trakt_prime_shows_list_data, config.PRIME_CLIENT_ID, config.PRIME_ACCESS_TOKEN)

    # Check Hotstar and Zee5 lists
    others_lists = get_lists(config.OTHERS_CLIENT_ID, config.OTHERS_ACCESS_TOKEN)
    others_slugs = [list["ids"]["slug"] for list in others_lists]
    logging.debug(f"Others lists slugs: {others_slugs}")

    if trakt_zee5_list_slug not in others_slugs:
        error_create = create_list(trakt_zee5_top_list_data, config.OTHERS_CLIENT_ID, config.OTHERS_ACCESS_TOKEN)
    if trakt_hotstar_list_slug not in others_slugs:
        error_create = create_list(trakt_hotstar_top_list_data, config.OTHERS_CLIENT_ID, config.OTHERS_ACCESS_TOKEN)
    # if trakt_prime_shows_list_slug not in lists_slugs:
    #     error_create = create_list(trakt_prime_shows_list_data)
    logging.debug("Lists checked!")
    return error_create


# Search movies or shows by title and type
def search_title_by_type(title_info: Tuple[str, str], type: str) -> List[int]:
    title = title_info[0].replace("&", "and")
    title_tag = title_info[1]

    response = requests.get(
        f"https://api.trakt.tv/search/{type}?query={title}&extended=full",
        headers=get_headers(),
        timeout=REQUEST_TIMEOUT,
    )
    trakt_ids = []
    if response.status_code == 200:
        results = response.json()
        logging.debug(f"Results: {results} for title: {title}")
        for result in results:
            logging.debug("Comparing " + title + " with: " + result[type]["title"].lower())
            normalized_slug = result[type]["ids"]["slug"].replace("-", "")
            normalized_title_tag = title_tag.replace("-", "")
            if (
                result["type"] == type
                and result[type]["title"].lower() == title.lower()
                and (normalized_title_tag in normalized_slug or normalized_title_tag.startswith(normalized_slug))
                or (
                    normalized_title_tag in normalized_slug
                    or normalized_title_tag.startswith(normalized_slug)
                    or normalized_slug.startswith(normalized_title_tag)
                )
            ):
                trakt_ids.append(result[type]["ids"]["trakt"])
                logging.debug(
                    f"Added trakt id: {result[type]['ids']['trakt']} with slug {normalized_slug} for title: {title}"
                )
                break
        if trakt_ids == []:
            logging.warning(f"Title not found: {title}, will add first result : {results[0][type]['title']}")
            trakt_ids.append(results[0][type]["ids"]["trakt"])
    else:
        logging.error(f"Error: {response.status_code}")
    return trakt_ids


# Search movies and shows by title
def search_title(title_info: Tuple[str, str, str]) -> List[Tuple[str, int, str]]:
    title = title_info[0].replace("&", "and")
    title_tag = title_info[1]
    rank = title_info[2]

    response = requests.get(
        f"https://api.trakt.tv/search/movie,show?query={title}&extended=full",
        headers=get_headers(),
        timeout=REQUEST_TIMEOUT,
    )
    trakt_info = []
    if response.status_code == 200:
        results = response.json()
        logging.debug(f"Results: {results} for title: {title}")
        for result in results:
            type = result["type"]
            normalized_slug = result[type]["ids"]["slug"].replace("-", "")
            normalized_title_tag = title_tag.replace("-", "")
            logging.debug(
                "Comparing "
                + title
                + " and tag "
                + normalized_title_tag
                + " with: "
                + result[type]["title"].lower()
                + " and slug "
                + normalized_slug
            )
            if (
                result[type]["title"].lower() == title.lower()
                and (normalized_title_tag in normalized_slug or normalized_title_tag.startswith(normalized_slug))
                or (normalized_title_tag in normalized_slug or normalized_title_tag.startswith(normalized_slug))
            ):
                trakt_info.append((type, result[type]["ids"]["trakt"], rank))
                logging.debug(
                    f"Added trakt id: {result[type]['ids']['trakt']} with slug {normalized_slug} for title: {title}"
                )
                break
        if trakt_info == []:
            type_0 = results[0]["type"]
            logging.warning(f"Title not found: {title}, will add first result : {results[0][type_0]['title']}")
            trakt_info.append((type_0, results[0][type_0]["ids"]["trakt"], rank))
    else:
        logging.error(f"Error: {response.status_code}")
    return trakt_info


# Create a Trakt list payload based on the top movies and shows list
def create_type_trakt_list_payload(top_list: List[Tuple[str, str, str]], type: str) -> Dict[str, List[Dict[str, Any]]]:
    # get titles from top_list
    titles_info = [(title, title_tag) for _, title, title_tag in top_list]

    # get trakt ids from titles
    trakt_ids = []
    for title_info in titles_info:
        trakt_id = search_title_by_type(title_info, type)
        if trakt_id:
            trakt_ids.append(trakt_id[0])

    # create the payload
    payload = {f"{type}s": []}
    for trakt_id in trakt_ids:
        payload[f"{type}s"].append({"ids": {"trakt": trakt_id}})

    logging.debug(f"Payload: {payload}")
    return payload


# Create a mixed Trakt list payload based on an overral top movies and shows list
def create_mixed_trakt_list_payload(top_list: List[Tuple[str, str, str]]) -> Dict[str, List[Dict[str, Any]]]:
    # get titles from top_list
    titles_info = [(title, title_tag, rank) for rank, title, title_tag in top_list]

    # get trakt ids from titles
    trakt_infos = []
    for title_info in titles_info:
        trakt_info = search_title(title_info)
        logging.debug(f"Trakt info: {trakt_info}")
        if trakt_info:
            trakt_infos.append(trakt_info[0])

    # create the payload
    payload = {"movies": [], "shows": []}
    for type, trakt_id, rank in trakt_infos:
        payload[f"{type}s"].append({"ids": {"trakt": trakt_id}})

    logging.debug(f"Payload: {payload}")
    return payload


# Update a trakt list
@retry_request
def update_list(
    list_slug: str,
    payload: Dict[str, List[Dict[str, Any]]],
    client_id: str = None,
    access_token: str = None,
) -> Union[requests.Response, int]:
    """Update a list in Trakt.tv with new content.

    Args:
        list_slug: The slug of the list to update
        payload: The content to update the list with
        client_id: The Trakt.tv client ID for the appropriate account
        access_token: The access token for the appropriate account
    """
    # Empty the list only if payload is not empty
    if payload.get("movies") or payload.get("shows"):
        empty_list(list_slug, client_id, access_token)
        logging.info(f"Updating list {list_slug} ...")
        response = requests.post(
            f"https://api.trakt.tv/users/me/lists/{list_slug}/items",
            headers=get_headers(client_id, access_token),
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code in [200, 201]:
            logging.info("List updated successfully")
        return response
    else:
        logging.warning("Payload is empty. No items to add on list " + list_slug)
        return 304


# ============================
# STREAMING SERVICE TRACKER CLASS
# ============================


class StreamingServiceTracker:
    """Main class for tracking streaming service data and updating Trakt lists."""

    def __init__(self, config_instance: Config = None):
        """Initialize the tracker with configuration."""
        self.config = config_instance or config

        # Initialize list data
        self._init_list_data()

        # Performance optimization: cache for repeated calls
        self._headers_cache = None
        self._failed_services = set()  # Track failed services to avoid retrying

    def _init_list_data(self) -> None:
        """Initialize Trakt list data configurations."""
        # Netflix lists
        self.netflix_movies_list_data = {
            "name": "Top India Netflix Movies",
            "description": "List that contains the top 10 movies on Netflix India right now, updated daily",
            "privacy": "public",
            "display_numbers": True,
        }

        self.netflix_shows_list_data = {
            "name": "Top India Netflix Shows",
            "description": "List that contains the top 10 TV shows on Netflix India right now, updated daily",
            "privacy": "public",
            "display_numbers": True,
        }

        # Additional list configurations would go here...
        # For now, keeping it minimal to not duplicate all the list data

    def get_headers_cached(self) -> Dict[str, str]:
        """Get headers with caching for performance."""
        if self._headers_cache is None:
            self._headers_cache = get_headers()
        return self._headers_cache

    def run(self) -> int:
        """Main execution method."""
        try:
            logging.info("Starting streaming service data update...")

            # Extract Movies and TV Shows
            scraped_data = self._scrape_all_services()

            if self.config.PRINT_LISTS:
                self._print_scraped_data(scraped_data)

            # Check Trakt token and lists
            if not self._validate_trakt_setup():
                return -1

            # Update all lists
            self._update_all_lists(scraped_data)

            # Report execution summary
            self._report_execution_summary(scraped_data)

            logging.info("Finished updating lists")
            return 0

        except Exception as e:
            logging.error(f"Error in main execution: {e}")
            return -1

    def _scrape_all_services(self) -> Dict[str, Any]:
        """Scrape data from all streaming services with improved error handling."""
        scraped_data = {}

        # Define scraping tasks
        scraping_tasks = [
            ("netflix_movies", self.config.urls["netflix"], self.config.sections["movies"]),
            ("netflix_shows", self.config.urls["netflix"], self.config.sections["shows"]),
            ("zee5_overall", self.config.urls["zee5"], self.config.sections["overall"]),
            ("hotstar_overall", self.config.urls["hotstar"], self.config.sections["overall_hotstar"]),
            ("prime_movies", self.config.urls["prime"], self.config.sections["movies"]),
            ("prime_shows", self.config.urls["prime"], self.config.sections["shows"]),
        ]

        # Execute scraping tasks with error handling
        for task_name, url, section in scraping_tasks:
            try:
                result = scrape_top10(url, section)
                scraped_data[task_name] = result or []  # Ensure we always have a list
                if result is None:
                    logging.warning(f"Failed to scrape {task_name}")
                    self._failed_services.add(task_name)
                else:
                    logging.debug(f"Successfully scraped {task_name}: {len(result)} items")
            except Exception as e:
                logging.error(f"Error scraping {task_name}: {e}")
                scraped_data[task_name] = []
                self._failed_services.add(task_name)

        return scraped_data

    def _print_scraped_data(self, data: Dict[str, Any]) -> None:
        """Print all scraped data for debugging."""
        print_top_list("TOP Netflix Movies", data["netflix_movies"])
        print_top_list("TOP Netflix Shows", data["netflix_shows"])
        print_top_list("TOP Zee5 Overall", data["zee5_overall"])
        print_top_list("TOP Hotstar Overall", data["hotstar_overall"])
        print_top_list("TOP Amazon Prime Video Movies", data["prime_movies"])
        print_top_list("TOP Amazon Prime Video Shows", data["prime_shows"])

    def _validate_trakt_setup(self) -> bool:
        """Validate Trakt tokens and create necessary lists for all accounts."""
        # Check Netflix account
        netflix_result = check_token(
            self.config.NETFLIX_CLIENT_ID,
            self.config.NETFLIX_CLIENT_SECRET,
            self.config.NETFLIX_ACCESS_TOKEN,
            self.config.NETFLIX_REFRESH_TOKEN,
        )
        if netflix_result is True:
            logging.info("Netflix Trakt token is valid")
        elif isinstance(netflix_result, tuple):
            new_access, new_refresh = netflix_result
            if new_access and new_refresh:
                logging.info("Netflix Trakt token refreshed successfully")
                self.config.NETFLIX_ACCESS_TOKEN = new_access
                self.config.NETFLIX_REFRESH_TOKEN = new_refresh
            else:
                logging.error("Failed to refresh Netflix Trakt token")
                return False
        else:
            logging.error("Failed to validate Netflix Trakt token")
            return False

        # Check Prime Video account
        prime_result = check_token(
            self.config.PRIME_CLIENT_ID,
            self.config.PRIME_CLIENT_SECRET,
            self.config.PRIME_ACCESS_TOKEN,
            self.config.PRIME_REFRESH_TOKEN,
        )
        if prime_result is True:
            logging.info("Prime Video Trakt token is valid")
        elif isinstance(prime_result, tuple):
            new_access, new_refresh = prime_result
            if new_access and new_refresh:
                logging.info("Prime Video Trakt token refreshed successfully")
                self.config.PRIME_ACCESS_TOKEN = new_access
                self.config.PRIME_REFRESH_TOKEN = new_refresh
            else:
                logging.error("Failed to refresh Prime Video Trakt token")
                return False
        else:
            logging.error("Failed to validate Prime Video Trakt token")
            return False

        # Check Hotstar & Zee5 account
        others_result = check_token(
            self.config.OTHERS_CLIENT_ID,
            self.config.OTHERS_CLIENT_SECRET,
            self.config.OTHERS_ACCESS_TOKEN,
            self.config.OTHERS_REFRESH_TOKEN,
        )
        if others_result is True:
            logging.info("Others Trakt token is valid")
        elif isinstance(others_result, tuple):
            new_access, new_refresh = others_result
            if new_access and new_refresh:
                logging.info("Others Trakt token refreshed successfully")
                self.config.OTHERS_ACCESS_TOKEN = new_access
                self.config.OTHERS_REFRESH_TOKEN = new_refresh
            else:
                logging.error("Failed to refresh Others Trakt token")
                return False
        else:
            logging.error("Failed to validate Others Trakt token")
            return False

        # Check and create necessary lists for all accounts
        if check_lists(self.config) is True:
            logging.error("Failed to create necessary lists")
            return False

        return True

    def _update_all_lists(self, data: Dict[str, Any]) -> None:
        """Update all Trakt lists with scraped data."""
        # Update Netflix lists using Netflix account
        logging.info("Updating Netflix lists...")
        movies_update = create_type_trakt_list_payload(data["netflix_movies"], "movie")
        shows_update = create_type_trakt_list_payload(data["netflix_shows"], "show")
        update_list(
            trakt_netflix_movies_list_slug,
            movies_update,
            self.config.NETFLIX_CLIENT_ID,
            self.config.NETFLIX_ACCESS_TOKEN,
        )
        update_list(
            trakt_netflix_shows_list_slug, shows_update, self.config.NETFLIX_CLIENT_ID, self.config.NETFLIX_ACCESS_TOKEN
        )

        # Update Prime Video lists using Prime account
        logging.info("Updating Prime Video lists...")
        prime_movies_update = create_type_trakt_list_payload(data["prime_movies"], "movie")
        prime_shows_update = create_type_trakt_list_payload(data["prime_shows"], "show")
        update_list(
            trakt_prime_movies_list_slug,
            prime_movies_update,
            self.config.PRIME_CLIENT_ID,
            self.config.PRIME_ACCESS_TOKEN,
        )
        update_list(
            trakt_prime_shows_list_slug, prime_shows_update, self.config.PRIME_CLIENT_ID, self.config.PRIME_ACCESS_TOKEN
        )

        # Update Hotstar and Zee5 lists using Others account
        logging.info("Updating Hotstar and Zee5 lists...")
        zee5_update = create_mixed_trakt_list_payload(data["zee5_overall"])
        hotstar_update = create_mixed_trakt_list_payload(data["hotstar_overall"])
        update_list(trakt_zee5_list_slug, zee5_update, self.config.OTHERS_CLIENT_ID, self.config.OTHERS_ACCESS_TOKEN)
        update_list(
            trakt_hotstar_list_slug, hotstar_update, self.config.OTHERS_CLIENT_ID, self.config.OTHERS_ACCESS_TOKEN
        )

    def _report_execution_summary(self, data: Dict[str, Any]) -> None:
        """Report summary of execution including successes and failures."""
        total_services = len(data)
        successful_services = sum(1 for v in data.values() if v and len(v) > 0)
        failed_services = len(self._failed_services)

        logging.info("Execution Summary:")
        logging.info(f"  Total services: {total_services}")
        logging.info(f"  Successful: {successful_services}")
        logging.info(f"  Failed: {failed_services}")

        if self._failed_services:
            logging.warning(f"  Failed services: {', '.join(self._failed_services)}")

        success_rate = (successful_services / total_services) * 100 if total_services > 0 else 0
        logging.info(f"  Success rate: {success_rate:.1f}%")


# ============================
# MAIN METHOD (backward compatibility)
# ============================


def main() -> int:
    """Main function for backward compatibility. Uses the StreamingServiceTracker class."""
    tracker = StreamingServiceTracker()
    return tracker.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())

import random
from typing import Sequence

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

SEARCH_URL_TEMPLATE = "https://market.yandex.ru/search?text={query}"
PRODUCT_LINKS_SELECTOR = "a[class='EQlfk Gqfzd']"
PARAMETERS_SELECTOR = "div[class='_2ZKgm']"
MIN_WAIT_SECONDS = 3
MAX_WAIT_SECONDS = 5


def _build_driver(user_agent: str) -> webdriver.Firefox:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)

    options = webdriver.FirefoxOptions()
    options.profile = profile
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Firefox(options)


def query_to_urls(query: str, user_agent: str, return_all: bool = False) -> list[str]:
    search_url = SEARCH_URL_TEMPLATE.format(query=query)
    driver = _build_driver(user_agent)

    try:
        driver.get(search_url)
        products = WebDriverWait(driver, random.randint(MIN_WAIT_SECONDS, MAX_WAIT_SECONDS)).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, PRODUCT_LINKS_SELECTOR))
        )
        links = [link for product in products if (link := product.get_attribute("href"))]
        return links if return_all else links[:1]
    except Exception as err:
        print(f"Search failed for query '{query}': {err}")
        return []
    finally:
        driver.quit()


def extract_params(query: str, user_agents: Sequence[str]) -> str | None:
    if not user_agents:
        print("No user agents provided.")
        return None

    user_agent = random.choice(user_agents)
    urls = query_to_urls(query=query, user_agent=user_agent)
    if not urls:
        print(f"No products found for query: {query}")
        return None

    driver = _build_driver(user_agent)
    try:
        for url in urls:
            driver.get(url)
            parameters = WebDriverWait(
                driver, random.randint(MIN_WAIT_SECONDS, MAX_WAIT_SECONDS)
            ).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, PARAMETERS_SELECTOR)))
            values = [
                parameter.find_element(By.TAG_NAME, "span").text.strip().lower()
                for parameter in parameters
            ]
            return "|".join(values)
    except Exception as err:
        print(f"Failed to parse product parameters for query '{query}': {err}")
        return None
    finally:
        driver.quit()

    return None


def main() -> None:
    with open("user-agents.txt", "r", encoding="utf-8") as file:
        user_agents = [ua for ua in file.read().splitlines() if ua]

    data_frame = pd.read_csv("itog_data_from_pars.csv")
    name_column = "Наименование"
    params_column = "Параметры"

    data_frame.loc[:, params_column] = [
        extract_params(query=str(name), user_agents=user_agents)
        for name in data_frame[name_column].tolist()
    ]
    print(data_frame)
    data_frame.to_csv("new.csv", index=False)


if __name__ == "__main__":
    main()

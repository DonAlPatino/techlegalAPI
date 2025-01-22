import requests


# Функция для выполнения запроса к API
def fetch_all_pages(base_url, token):
    # base_url = "https://tl96.techlegal.ru/api/getRequest/credit"
    data = {
        "token": token
    }
    all_results = []

    # Запрашиваем первую страницу
    response = requests.post(base_url, data=data)
    if response.status_code != 200:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        return None

    first_page_data = response.json()
    all_results.extend(first_page_data.get("result", []))

    # Проверяем количество страниц
    total_pages = first_page_data.get("pages", 1)

    # Если страниц больше одной, запрашиваем остальные
    if total_pages > 1:
        for page in range(2, total_pages + 1):
            url = f"{base_url}/{page}"
            response = requests.post(url, data=data)
            if response.status_code == 200:
                page_data = response.json()
                all_results.extend(page_data.get("result", []))
            else:
                print(f"Ошибка при выполнении запроса для страницы {page}: {response.status_code}")

    return all_results

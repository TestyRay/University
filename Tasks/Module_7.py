import re
import csv
from urllib.request import urlopen


URL = "https://msk.spravker.ru/avtoservisy-avtotehcentry"


def fetch_html(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_companies(html: str) -> list[dict]:
    html = re.sub(r"\s+", " ", html)

    pattern = re.compile(
        r'<div class="org-widget-header__title"><.*?a[^>]*>(?P<name>.*?)</a>.*?'
        r'org-widget-header__meta--location">\s*(?P<address>.*?)\s*</span>.*?'
        r'<span class="spec__index-inner">Телефон</span></dt>\s*'
        r'<dd class="spec__value">\s*(?P<phone>.*?)\s*</dd>.*?'
        r'<span class="spec__index-inner">Часы работы</span></dt>\s*'
        r'<dd class="spec__value">\s*(?P<hours>.*?)\s*</dd>',
        re.S
    )

    matches = list(pattern.finditer(html))
    data: list[dict[str, str]] = []

    for match in matches:
        data.append({
            "name": match.group("name").strip(),
            "address": match.group("address").strip(),
            "phone": match.group("phone").strip(),
            "hours": match.group("hours").strip(),
        })

    return data


def save_csv(data: list, filename="companies.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Название", "Адрес", "Телефоны", "Часы работы"])

        for item in data:
            writer.writerow([
                item["name"],
                item["address"],
                item["phone"],
                item["hours"],
            ])

    print(f"CSV файл '{filename}' успешно создан.")


def main():
    print("Скачиваю HTML-страницу...")
    html = fetch_html(URL)

    print("Извлекаю данные...")
    companies = parse_companies(html)

    print(f"Найдено организаций: {len(companies)}")
    save_csv(companies)


if __name__ == "__main__":
    main()

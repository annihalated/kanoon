from bs4 import BeautifulSoup

class TableProcessor:
    def __init__(self, html):
        self.table = BeautifulSoup(html, features="html.parser").find("table")


    def to_list_of_dicts(self) -> list:
        results = []
        heading_items = self.table.find_all("th")
        rows = self.table.find_all("tr")
        keys = [heading_item.text.strip().lower().replace(" ", "_") for heading_item in heading_items]

        for row in rows:
            values = [item.text if not item.a else item.a["href"] for item in row.find_all("td")]
            table_row  = dict(zip(keys,values))
            results.append(table_row)
        results = list(filter(None, results))

        return results


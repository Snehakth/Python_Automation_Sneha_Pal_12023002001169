"""Create an Excel copy of the default purchase scenario."""

from openpyxl import Workbook

from test_data.data_loader import load_purchase_data


def main():
    scenario = load_purchase_data()
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Purchase"
    headers = ["base_url", "product_name", "quantity"]
    sheet.append(headers)
    sheet.append([scenario[header] for header in headers])
    workbook.save("test_data/purchase.xlsx")


if __name__ == "__main__":
    main()
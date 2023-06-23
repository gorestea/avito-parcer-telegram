import openpyxl
import json

def to_excel():
    with open("news_dict.json", encoding="utf-8") as file:
        data = json.load(file)

        # print(id, title, url, price, comment, date)

    book = openpyxl.Workbook()
    sheet = book.active

    sheet['B1'] = "TITLE"
    sheet['C1'].hyperlink = "URL"
    sheet['D1'] = "PRICE (₽)"
    sheet['E1'] = "COMMENT"
    sheet['F1'] = "DATE"
    sheet['G1'] = "APPEND_DATE"

    row = 2
    for tovar in data["tovary"]:
        sheet[row][1].value = tovar['title']
        sheet[row][2].hyperlink = tovar['url']
        sheet[row][3].value = tovar['price']
        sheet[row][4].value = tovar['comment']
        sheet[row][5].value = tovar['date']
        sheet[row][6].value = tovar['date_append']
        row += 1

    book.save("my_book.xlsx")
    book.close()
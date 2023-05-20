import pandas as pd
from fpdf import FPDF

""" Your App should use the articles in articles csv and do stock management.
USE OOP framework 
Finally, a receipt needs to be outputed as per the item chosen!, should include:

Receipt No.: with Id of item
Article: with name of item
Price: with price of the item


Bonus: Once an item is booked for stock, its in stock quantity should go down """

stock_df = pd.read_csv("008 articles.csv", dtype={"id": str})


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

    def book_item(self):
        stock_df.loc[stock_df["id"] == self.item_id,"in stock"] -= 1
        stock_df.to_csv("008 articles.csv", index=False)


class Receipt:
    def __init__(self, item_receipt):
        self.item_receipt = item_receipt

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Receipt No.: {self.item_receipt.item_id}", ln=1)
        receipt_name = stock_df.loc[stock_df["id"] == self.item_receipt.item_id, "name"].squeeze()
        pdf.cell(w=50, h=8, txt=f"Article: {receipt_name.title()}", ln=1)
        receipt_price = stock_df.loc[stock_df["id"] == self.item_receipt.item_id, "price"].squeeze()
        pdf.cell(w=50, h=8, txt=f"Price: {receipt_price}", ln=1)
        output = pdf.output("receipt.pdf")
        return output



"""How App Operation"""
print(stock_df)
item_chosen = input("Enter id of the item: ")
item = Item(item_chosen)
item.book_item()
receipt = Receipt(item)
receipt.generate()


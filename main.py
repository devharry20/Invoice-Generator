from invoice import Invoice
import os

if __name__ == "__main__":
    invoice = Invoice(
        rec_addr_name="My Business Name", 
        rec_addr_addr="104 Business Lane",
        rec_addr_city="Manchester", 
        rec_addr_postal="M5 4DG", 
        rec_addr_country="United Kingdom",
        sndr_addr_name="Google London",
        sndr_addr_addr="6 Pancras Sq",
        sndr_addr_city="London",
        sndr_addr_postal="N1C 4AG",
        sndr_addr_country="United Kingdom",
        invoice_ref="Google Ads Spend Oct-Nov",
        invoice_num="INV-0001",
        items=[
            ["Promoted Campaign", 1, 29.00],
            ["Promoted Campaign", 1, 55.60],
            ["Sponsored Post", 1, 22.10],
        ]
    )

    invoice.create(
        filename="output.pdf",
        image_path=os.getcwd() + r"\static\images\logo.png",
        image_size=(150, 51)   
    )
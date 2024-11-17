from invoice import Invoice

if __name__ == "__main__":
    invoice = Invoice(
        rec_addr_name="Google London", 
        rec_addr_addr="6 Pancras Sq",
        rec_addr_city="London", 
        rec_addr_postal="N1C 4AG", 
        rec_addr_country="United Kingdom",
        sndr_addr_name="My Business",
        sndr_addr_addr="My Business Address",
        sndr_addr_city="My Business City",
        sndr_addr_postal="My Business Postal",
        sndr_addr_country="United Kingdom",
        invoice_ref="REF-0001",
        invoice_num=1,
        items=[
            ["Web hosting", 1, 30, 20],
            ["Social media management", 1, 60, 20],
            ["Logo graphic redesigns", 3, 15, 20]
        ]
    )

    invoice.create(
        filename="output.pdf",
        image_path=r"C:\Users\Athon\Desktop\Programming Projects\Invoice Generator\static\images\logo.png" ,
        image_size=(100, 100)   
    )

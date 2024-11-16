from invoice import Invoice


if __name__ == "__main__":
    invoice = Invoice(
        addr_name="Google London", 
        addr_addr="6 Pancras Sq, London", 
        addr_postal="N1C 4AG", 
        addr_country="United Kingdom",
        invoice_ref="REF-0001",
        invoice_num=1
    )

    invoice.create()
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer, PageBreak
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import inspect
from datetime import datetime

class Invoice:
    def __init__(self,
                 filename: str = "output.pdf", 
        addr_name: str = None, 
        addr_addr: str = None, 
        addr_postal: str = None, 
        addr_country: str = None,
        invoice_date: datetime = datetime.now(),
        invoice_ref: str = None,
        invoice_num: str = None
    ):
        self.filename = filename
        self.addr_name = addr_name
        self.addr_addr = addr_addr
        self.addr_postal = addr_postal
        self.addr_country = addr_country
        self.invoice_date = invoice_date
        self.invoice_ref = invoice_ref
        self.invoice_num = invoice_num

        self.styles = getSampleStyleSheet()

    def conv_to_paragraph(self, text: str, _styles = None) -> Paragraph:
        if _styles == None:
            _styles = self.styles["Normal"]

        return Paragraph(text, _styles)

    def create(self, filename: str = "output.pdf"):
        # Checking that all arguements have values other than None
        frame = inspect.currentframe()
        args = frame.f_locals
        function_args = {key: value for key, value in args.items() if key not in ['frame']}

        for key, value in function_args.items():
            if value == None:
                raise Exception(f"Argument {key} must have a supplied value")

        document = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        invoice_date = self.invoice_date.strftime("%d/%m/%Y %H:%M %p")
        BOLD_STYLE = ParagraphStyle(name="Bold", parent=self.styles["Normal"], fontName="Helvetica-Bold")

        invoice_title = Paragraph("SALES INVOICE", self.styles["Heading2"])

        invoice_data_table_data = [
            [self.conv_to_paragraph("Invoice Date", BOLD_STYLE), invoice_date], 
            [self.conv_to_paragraph("Invoice Reference", BOLD_STYLE), self.invoice_ref], 
            [self.conv_to_paragraph("Invoice Number", BOLD_STYLE), self.invoice_num]
        ]
        invoice_data_table = Table(invoice_data_table_data)
        invoice_data_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        table_data = [[
            [
                invoice_title, 
                self.conv_to_paragraph(self.addr_name), 
                self.conv_to_paragraph(self.addr_addr), 
                self.conv_to_paragraph(self.addr_postal), 
                self.conv_to_paragraph(self.addr_country)
            ], 
            invoice_data_table
        ]]

        table = Table(table_data, colWidths=["*", "*"])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),  # Align both cells to the top
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Reduce extra padding
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))

        elements.append(table)

        document.build(elements)
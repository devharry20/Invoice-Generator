from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer, HRFlowable
from reportlab.platypus import Image as RLImage
from reportlab.lib.colors import Color, black, grey, whitesmoke, beige
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage

import inspect
from datetime import datetime
from io import BytesIO
from typing import Union

class Invoice:
    def __init__(self,
        filename: str = "output.pdf", 
        company_addr_name: str = None,
        company_addr_addr: str = None,
        company_addr_city: str = None,
        company_addr_postal: str = None,
        company_addr_country: str = None,
        client_addr_name: str = None, 
        client_addr_addr: str = None, 
        client_addr_city: str = None,
        client_addr_postal: str = None, 
        client_addr_country: str = None,
        invoice_date: datetime = datetime.now(),
        invoice_ref: str = None,
        invoice_num: str = None,
        items: list = []
    ):
        self.filename = filename
        self.company_addr_name = company_addr_name
        self.company_addr_addr = company_addr_addr
        self.company_addr_city = company_addr_city
        self.company_addr_postal = company_addr_postal
        self.company_addr_country = company_addr_country
        self.client_addr_name = client_addr_name
        self.client_addr_addr = client_addr_addr
        self.client_addr_city = client_addr_city
        self.client_addr_postal = client_addr_postal
        self.client_addr_country = client_addr_country
        self.invoice_date = invoice_date
        self.invoice_ref = invoice_ref
        self.invoice_num = invoice_num
        self.items = items

        self.styles = getSampleStyleSheet()

    def _get_image_buffer(self, img_location: str) -> tuple:
        """Returns an image buffer and PIL image object"""
        buffer = BytesIO()
        image = PILImage.open(img_location)
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return (buffer, image)

    def _conv_to_paragraph(self, text: str, _styles = None) -> Paragraph:
        """Converts a string to a reportlab Paragraph"""
        if _styles == None:
            _styles = self.styles["Normal"]

        return Paragraph(text, _styles)

    def _create_horizontal_line_break(self, width: str = "100%", thickness: int = 1, colour: Color = black, h_align: str = "CENTER", v_align: str = "BOTTOM") -> HRFlowable:
        """Returns a HRFlowable which serves as a horizontal line break"""
        return HRFlowable(width, thickness=thickness, lineCap="round", color=colour, spaceBefore=1, spaceAfter=1, hAlign=h_align, vAlign=v_align, dash=None)

    def create(self, filename: str = "output.pdf", image_path: str = None, image_size: tuple = (200, 50)):
        """Creates the invoice as a PDF"""
        frame = inspect.currentframe()
        args = frame.f_locals
        function_args = {key: value for key, value in args.items() if key not in ["frame"]}

        # Checking that all arguements have values other than None
        for key, value in function_args.items():
            if value == None:
                raise Exception(f"Argument {key} must have a supplied value")

        document = SimpleDocTemplate(filename, pagesize=A4, leftMargin=30, rightMargin=30)
        elements = []

        invoice_date = self.invoice_date.strftime("%d/%m/%Y %H:%M %p")
        BOLD_STYLE = ParagraphStyle(name="Bold", parent=self.styles["Normal"], fontName="Helvetica-Bold")

        image_buffer, _ = self._get_image_buffer(image_path)
        logo_image = RLImage(image_buffer, image_size[0], image_size[1])
        logo_image.hAlign = "RIGHT"
        elements.append(logo_image)

        elements.append(Spacer(0, 25))

        invoice_title = Paragraph("SALES INVOICE", self.styles["Heading2"])

        right_hand_info_data = [
            [self._conv_to_paragraph("Invoice Date", BOLD_STYLE), invoice_date], 
            [self._conv_to_paragraph("Invoice Reference", BOLD_STYLE), self.invoice_ref], 
            [self._conv_to_paragraph("Invoice Number", BOLD_STYLE), self.invoice_num],
            [self._conv_to_paragraph("Sender", BOLD_STYLE), self.company_addr_name],
            [self._conv_to_paragraph("", BOLD_STYLE), self.company_addr_addr],
            [self._conv_to_paragraph("", BOLD_STYLE), self.company_addr_city],
            [self._conv_to_paragraph("", BOLD_STYLE), self.company_addr_postal],
            [self._conv_to_paragraph("", BOLD_STYLE), self.company_addr_country]
        ]
        right_hand_info_table = Table(right_hand_info_data)
        right_hand_info_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        table_data = [[
            [
                invoice_title, 
                self._conv_to_paragraph(self.client_addr_name), 
                self._conv_to_paragraph(self.client_addr_addr), 
                self._conv_to_paragraph(self.client_addr_city), 
                self._conv_to_paragraph(self.client_addr_postal), 
                self._conv_to_paragraph(self.client_addr_country)
            ], 
            right_hand_info_table
        ]]

        table = Table(table_data, colWidths=["*", "*"])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),  # Align both cells to the top
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Reduce extra padding
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(table)

        elements.append(Spacer(0, 40))
        elements.append(self._create_horizontal_line_break())
        elements.append(Spacer(0, 40))

        # INVOICE DATA / ITEMS TABLE

        page_width, _ = A4
        page_left_margin = document.leftMargin
        page_right_margin = document.rightMargin
        container_width = page_width - page_left_margin - page_right_margin

        invoice_data = [["Description", "Quantity", "Unit Price", "Amount"]]

        for i in self.items:
            i = [i[0], i[1], f"£{i[2]}", f"£{i[1] * i[2]}"]
            invoice_data.append(i)

        col_widths = [container_width * 0.4]  # 40% of available width for Description
        remaining_width = container_width * 0.6  # 60% of available width for the other columns
        col_widths += [remaining_width / 4] * (len(invoice_data[0]) - 1)  # Divide remaining width among 4 columns

        invoice_table = Table(invoice_data, colWidths=col_widths)
        invoice_table_style = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12)
        ])
        invoice_table.setStyle(invoice_table_style)

        elements.append(invoice_table)

        elements.append(Spacer(0, 40))
        elements.append(self._create_horizontal_line_break())
        elements.append(Spacer(0, 40))

        total_sum = sum([i[2] for i in self.items])
        totals_table = Table([["Items", "VAT", "Total"], [len(invoice_data)-1, "20%", f"£{round(total_sum + total_sum * 0.20, 2)}"]], colWidths=col_widths)
        totals_table_style = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12)
        ])
        totals_table.setStyle(totals_table_style)

        elements.append(totals_table)

        document.build(elements)
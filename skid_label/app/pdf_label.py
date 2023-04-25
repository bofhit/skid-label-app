"""
Accept input from user and create a skid label as a PDF doc.
"""

from fpdf import FPDF
import os
import time

#TODO: Handle long product names. Using multicell is not satifactory, 
# because alignment is not maintained.

DEBUG = 1

TEXT_BOH = 'Blessings of Hope'
TEXT_SORT = 'Sort Date'
TEXT_PACK = 'Pack Date'

class SkidLabelPDF():
    def __init__(self):
        pass

    def main(self):
        self.validate_params()
        self.generate_labels()
        return self.write_label()

    def validate_params(self):
        # Overwrite in child class.
        pass

    def generate_labels(self):
        # Overwrite in child class.
        pass

    def write_label(self):
        # Write to file.
        pdf_path = os.path.join(self.out_file, str(time.time()) + '.pdf')
        self.pdf.output(pdf_path)
        if DEBUG:
            print(f'{self.__str__()} wrote to file.')
        return pdf_path

    def format_date(self, date):
        splt = date.split('-')
        mo = splt[1].lstrip('0')
        day = splt[2].lstrip('0')
        date = f'{mo}/{day}'
        return date

class SortLabelPDF(SkidLabelPDF):
    def __init__(self, **kwargs):
        super().__init__()

        # Unpack parameters.
        self.product = kwargs['product']
        self.date = kwargs['date']
        self.label_count = kwargs['label_count']
        self.out_file = kwargs['out_file']

        # Initialize pdf object.
        self.pdf = FPDF()

    def __str__(self):
        return 'Sort Label'

    def validate_params(self):
        assert type(self.product) == str, 'Unexpected type for variable "product".'
        assert type(self.date) == str, 'Unexpected type for variable "date".'
        assert int(self.label_count), 'Number of copies needs to be convertible to integer.'
        assert type(self.out_file) == str, 'Unexpected type for variable "file".'

    def generate_labels(self):

        for page in range(int(self.label_count)):
            Y = 0           # Vertical position.
            # Units are mm.
            # 81.6 = 101.6 - <10mm margins>
            X = 195.9        # Page width.

            self.pdf.add_page()
            self.pdf.set_font('Arial')

            # Add header.
            self.pdf.set_font_size(72)
            self.pdf.cell(X, 45, TEXT_BOH, 0, 1, 'C')
            Y += 5
            
            self.pdf.set_font_size(72)
            self.pdf.cell(X, 50, TEXT_SORT, 0, 1, 'C')
            Y += 5

            # Add date.
            print(self.date)
            self.pdf.set_font_size(216)
            self.pdf.cell(X, 85, self.format_date(self.date), 0, 1, 'C')
            Y += 5

            # Add product.
            self.pdf.set_font_size(72)
            self.pdf.cell(X, 30, self.product, 0, 1, 'C')
            Y += 5

            if DEBUG:
                print(f'{self.__str__()} finished generating label.')

class HOHLabelPDF(SkidLabelPDF):
    def __init__(self, **kwargs):
        super().__init__()

        # Unpack parameters.
        self.num_box = kwargs['num_box']
        self.shift = kwargs['shift']
        self.date = kwargs['date']
        self.label_count = kwargs['label_count']
        self.out_file = kwargs['out_file']

        # Initialize pdf object.
        self.pdf = FPDF()

    def __str__(self):
        return 'Sort Label'

    def validate_params(self):
        assert int(self.num_box), 'Number of copies needs to be convertible to integer.'
        assert self.shift in ['A', 'B', 'C'], 'Unexpected value for shift parameter'
        assert type(self.date) == str, 'Unexpected type for variable "date".'
        assert int(self.label_count), 'Number of copies needs to be convertible to integer.'
        assert type(self.out_file) == str, 'Unexpected type for variable "file".'

    def generate_labels(self):

        for page in range(int(self.label_count)):
            Y = 0           # Vertical position.
            # Units are mm.
            # 81.6 = 101.6 - <10mm margins>
            X = 195.9        # Page width.

            self.pdf.add_page()
            self.pdf.set_font('Arial')

            # Add header.
            self.pdf.set_font_size(72)
            self.pdf.cell(X, 30, TEXT_BOH, 0, 1, 'C')
            Y += 5
            
            self.pdf.set_font_size(72)
            self.pdf.cell(X, 30, TEXT_PACK, 0, 1, 'C')
            Y += 5

            # Add date.
            self.pdf.set_font_size(216)
            self.pdf.cell(X, 85, self.format_date(self.date), 0, 1, 'C')
            Y += 5

            # Add box number.
            self.pdf.set_font_size(250)
            self.pdf.cell(X, 85, self.shift + str(self.num_box), 0, 1, 'C')

            if DEBUG:
                print(f'{self.__str__()} finished generating label.')


if __name__ == '__main__':
    hoh = HOHLabelPDF(shift='A', num_box=2, date='2021-9-20', label_count=1, out_file='C:/io/labels')
    sort = SortLabelPDF(product='CABBAGE', date='2021-4-18', label_count=1, out_file='C:/io/labels')
    print(hoh.main())
    print(sort.main())
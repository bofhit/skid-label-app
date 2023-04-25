__doc__  = """Generate ZPL skid labels."""

"""
Accepts input from user and generates zpl as a text file.
"""
import os
import time

import yaml

from logger import LoggerWrapper

"""
ZPL Notes

^XA- Marks the start of the file.
^XZ- Marks the end of the file.

^FO- Field origin- params: X origin, Y origin
^A- Font- params: font, height, width (optional, scasles to height by default)
^FB- Field block- params: 
                            width of block, 
                            max number of lines,
                            add or delete space between lines,
                            justification:
                                L = left,
                                C = center,
                                R = right,
                                J = justified
                                ,
                            hanging indent
^FS- Field seperator
"""
CONFIG_PATH = 'app/config.yaml'

def load_config(path):
    """
    Load configuration data.
    """
    open(path, 'r')
    try:
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return config_dict
    except:
        return None

config_data = load_config(CONFIG_PATH)

LOGGING_CONFIG = config_data['LOGGING_CONFIG']
LOG_FILE = config_data['LOG_FILE']
LOGGER_NAME = config_data['LOGGER_NAME']

lw = LoggerWrapper(
    LOGGER_NAME,
    LOGGING_CONFIG,
    LOG_FILE
)


class SkidLabelZPL():
    def __init__(self):
        pass

    def main(self):
        self.validate_params()
        self.zpl = self.generate_label()
        return self.write_label()

    def validate_params(self):
        # Overwrite in child class.
        pass

    def generate_label(self):
        # Overwrite in child class.
        pass

    def write_label(self):
        # Write to file.
        zpl_path = os.path.join(self.out_file, str(time.time()) + '.zpl')
        with open(zpl_path, 'w') as f:
            f.write('\n'.join(self.zpl))
        return zpl_path

    def format_date(self, date):
        splt = date.split('-')
        mo = splt[1].lstrip('0')
        day = splt[2].lstrip('0')
        date = f'{mo}/{day}'
        return date
    
    def sanitize_text(self, string):
        """
        Sanitize text for Zebra printers.
        """
        sanitized = []

        for char in string:
            if char not in ['$', '\\', '^']:
                sanitized.append(char)
        return ''.join(sanitized)
    
class SortLabelZPL(SkidLabelZPL):
    def __init__(self, **kwargs):
        super().__init__()

        # Unpack parameters.
        self.product = self.sanitize_text(kwargs['product'])
        self.date = kwargs['date']
        self.num_pages = kwargs['num_pages']
        self.out_file = kwargs['out_file']

    def __str__(self):
        return 'Sort Label'

    def validate_params(self):
        assert type(self.product) == str, 'Unexpected type for variable "product".'
        assert type(self.date) == str, 'Unexpected type for variable "date".'
        assert int(self.num_pages), 'Number of copies needs to be convertible to integer.'
        assert type(self.out_file) == str, 'Unexpected type for variable "file".'

    def generate_label(self):
        # Start of file.
        zpl = ['^XA']

        # Add header.
        zpl.append(f'^FO50,60^A0,150^FB1200,5,25,C^FDBlessings of Hope\&Sort Date^FS')

        # Add date.
        fmtdate = self.format_date(self.date)
        zpl.append(f'^FO50,600^A0,500^FB1200,5,25,C^FD{fmtdate}^FS')

        # Add product.
        zpl.append(f'^FO50,1200^A0,150^FB1200,5,25,C,^FD{self.product}^FS')

        # Need these so text file will be executed as zpl.
        zpl.append('^XZ')

        return zpl * int(self.num_pages)

class HOHLabelZPL(SkidLabelZPL):
    def __init__(self, **kwargs):
        super().__init__()

        # Unpack parameters.
        self.num_box = kwargs['num_box']
        self.shift = kwargs['shift']
        self.date = kwargs['date']
        self.num_pages = kwargs['num_pages']
        self.out_file = kwargs['out_file']

    def __str__(self):
        return 'Sort Label'

    def validate_params(self):
        assert int(self.num_box), 'Number of copies needs to be convertible to integer.'
        assert self.shift in ['A', 'B', 'C'], 'Unexpected value for shift parameter'
        assert type(self.date) == str, 'Unexpected type for variable "date".'
        assert int(self.num_pages), 'Number of copies needs to be convertible to integer.'
        assert type(self.out_file) == str, 'Unexpected type for variable "file".'

    def generate_label(self):
        # Start of file.
        zpl = ['^XA']

        # Add header.
        zpl.append(f'^FO50,60^A0,150^FB1200,5,25,C^FDBlessings of Hope\&Pack Date^FS')

        # Add date.
        fmtdate = self.format_date(self.date)
        zpl.append(f'^FO50,600^A0,500^FB1200,5,25,C^FD{fmtdate}^FS')

        # Box number. 
        box_id = self.shift + self.num_box
        zpl.append(f'^FO50,1100^A0,750^FB1200,5,25,C^FD{box_id}^FS')

        # Need these so text file will be executed as zpl.
        zpl.append('^XZ')

        return zpl * int(self.num_pages)

if __name__ == '__main__':
#    hoh = HOHLabel(shift='A', num_box=2, date='2021-9-20', num_pages=1, out_file='C:/io/labels')
    sort = SortLabelZPL(product='CABBAGE', date='2021-4-18', num_pages=1, out_file='C:/io/labels')
#    print(hoh.main())
    print(sort.main())
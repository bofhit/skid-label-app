"""
Use PrintIt service to print PDF doc.
"""
import requests
import win32print

from util.logger import LoggerWrapper
from util.utils import load_config

#TODO: Add error handling to printZPL func.

CONFIG_PATH = 'app/config.yaml'

config_data = load_config(CONFIG_PATH)

assert config_data != None, 'Error loading config.'

LABEL_DIR = config_data['LABEL_DIR']
PRINTER_NAME = config_data['PRINTER_NAME']
PRINTIT_URL = config_data['PRINTIT_URL']

assert type(LABEL_DIR) == str, 'Expected a string.'
assert type(PRINTER_NAME) == str, 'Expected a string.'
assert type(PRINTIT_URL) == str, 'Expected a string.'

DOCUMENT_TYPE = config_data['DOCUMENT_TYPE']

assert DOCUMENT_TYPE in ['pdf', 'zpl']

LOGGER_NAME = config_data['LOGGER_NAME']
LOGGING_CONFIG = config_data['LOGGING_CONFIG']
LOG_FILE = config_data['LOG_FILE']

assert type(LOGGER_NAME) == str, 'Expected a string.'
assert type(LOGGING_CONFIG) == str, 'Expected a string.'
assert type(LOG_FILE) == str, 'Expected a string.'

lw = LoggerWrapper(
    LOGGER_NAME,
    LOGGING_CONFIG,
    LOG_FILE
)

def printPDF(url='url', printer_name='printer_name', document_path='path'):
    lw.logger.debug(f'Calling printPDF with params: url={url}, printer_name={printer_name}, document_path={document_path}')

    try:
        # Convert backslashes.
        document_path = document_path.replace('\\', '/')

        payload={'PrinterPath': printer_name}
        files=[
        ('PdfFile',(document_path.rsplit('/')[-1],open(document_path,'rb'),'application/pdf'))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response
    except:
        return 0

def printZPL(printer_name='printer_name', document_path='document_path'):
    lw.logger.debug(f'Calling printZPL with params: printer_name={printer_name}, document_path={document_path}')

    try: 
        with open(document_path, 'rb') as f:
            bytesstr = f.read()
    except:
        lw.logger.exception('Exception reading in bytestream.')

    try:
        handle = win32print.OpenPrinter(printer_name)
        win32print.StartDocPrinter(handle, 1, ('', '', 'RAW'))
        win32print.WritePrinter(handle, bytesstr)
        win32print.EndDocPrinter(handle)
    except:
        lw.logger.exception('Exception sending win32 print job')
    finally:
        win32print.ClosePrinter(handle)
    

if __name__ == '__main__':
    printZPL('GX430t Text Only', 'C:/io/labels/label.zpl')

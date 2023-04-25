"""
Api to print labels.
"""

import os
from pathlib import Path

from flask import Flask, request, render_template

from pdf_label import SortLabelPDF, HOHLabelPDF
from zpl_label import SortLabelZPL, HOHLabelZPL
from print import printPDF, printZPL
from util.logger import LoggerWrapper
from util.utils import load_config

CONFIG_PATH = 'app/config.yaml'

config_data = load_config(CONFIG_PATH)

assert config_data != None, 'Error loading config.'

LABEL_DIR = config_data['LABEL_DIR']
PRINTER_NAME = config_data['PRINTER_NAME']
PRINTIT_URL = config_data['PRINTIT_URL']

assert type(LABEL_DIR) == str, 'Expected a string.'
assert type(WINDOWS_HOST_LABEL_DIR) == str, 'Expected a string.'
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

lw.logger.debug(f'Var LABEL_DIR set to: {LABEL_DIR}')
lw.logger.debug(f'Var PRINTER_NAME set to: {PRINTER_NAME}')
lw.logger.debug(f'Var PRINTIT_URL set to: {PRINTIT_URL}')
lw.logger.debug(f'Var DOCUMENT_TYPE set to: {DOCUMENT_TYPE}')
lw.logger.debug(f'Var LOGGER_NAME set to: {LOGGER_NAME}')
lw.logger.debug(f'Var LOGGING_CONFIG set to: {LOGGING_CONFIG}')
lw.logger.debug(f'Var LOG_FILE set to: {LOG_FILE}')

lw.logger.debug('Initializing app...')

app = Flask(__name__)

# ============================================================================
# Labels for sorting/packing skid.

@app.route('/sort', methods=['GET'])
def render_sort():
    return render_template('sort_label.html')

@app.route('/sort/print', methods=['POST'])
def print_sort():
    if DOCUMENT_TYPE == 'pdf':
        label = SortLabelPDF(product=request.form['product'], 
                        date=request.form['date'],
                        num_pages=request.form['num_pages'], 
                        out_file=LABEL_DIR
                        )
        label_path = label.main()
        # Send to printer.
        printPDF(url=PRINTIT_URL, 
                    printer_name=PRINTER_NAME, 
                    document_path=label_path
                )
        return 'Function completed'

    elif DOCUMENT_TYPE == 'zpl':
        label = SortLabelZPL(product=request.form['product'], 
                        date=request.form['date'],
                        num_pages=request.form['label_count'], 
                        out_file=LABEL_DIR
                        )
        label_path = label.main()
        # Send to printer.
        printZPL(printer_name=PRINTER_NAME, 
                    document_path=label_path
                )
        return 'Function completed'
# ============================================================================

# ============================================================================
# Labels for Hands of Hope skids.

@app.route('/hoh', methods=['GET'])
def render_hoh():
    return render_template('hoh_label.html')

@app.route('/hoh/print', methods=['POST'])
def print_hoh():
    #TODO :Add error handlers.
    if DOCUMENT_TYPE == 'pdf':
        label = HOHLabelPDF(shift=request.form['shift'], 
                        num_box=request.form['box_number'],
                        date=request.form['date'],
                        num_pages=request.form['label_count'], 
                        out_file=LABEL_DIR
                        )
        label_path = label.main()
        # Send to printer.
        printPDF(url=PRINTIT_URL, 
                    printer_name=PRINTER_NAME, 
                    document_path=label_path
                )
        return 'Function completed'
    elif DOCUMENT_TYPE == 'zpl':
        label = HOHLabelZPL(shift=request.form['shift'], 
                        num_box=request.form['box_number'],
                        date=request.form['date'],
                        num_pages=request.form['label_count'], 
                        out_file=LABEL_DIR
                        )
        label_path = label.main()
        # Send to printer.
        printZPL(printer_name=PRINTER_NAME, 
                    document_path=label_path
                )
        return 'Function completed'
# ============================================================================

if __name__ == '__main__':

    LABEL_DIR = os.environ.get('LABEL_DIR')
    WINDOWS_HOST_LABEL_DIR = os.environ.get('WINDOWS_HOST_LABEL_DIR')
    PRINTER_NAME = os.environ.get('PRINTER_NAME')
    PRINTIT_URL = os.environ.get('PRINTIT_URL')

    assert type(LABEL_DIR) == str, 'Expected a string.'
    assert type(WINDOWS_HOST_LABEL_DIR) == str, 'Expected a string.'
    assert type(PRINTER_NAME) == str, 'Expected a string.'
    assert type(PRINTIT_URL) == str, 'Expected a string.'

    app.run(host='0.0.0.0', port=80)

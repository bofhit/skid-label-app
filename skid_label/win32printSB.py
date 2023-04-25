import win32print

def printRAW(bytes_obj, printer_name):
    handle = win32print.OpenPrinter(printer_name)
    win32print.StartDocPrinter(handle, 1, ('', '', 'RAW'))
    win32print.WritePrinter(handle, bytes_obj)
    win32print.EndDocPrinter(handle)
    win32print.ClosePrinter(handle)

def getBytes(file):
    with open(file, 'rb') as f:
        bytestream = f.read()
    return bytestream

if __name__ == '__main__':
    import sys
    args = sys.argv

    file = args[1]
    printer = args[2]

    print(f'file:{file}')
    print(f'printer:{printer}')

    printRAW(getBytes(file), printer)
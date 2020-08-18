import zxing

reader = zxing.BarCodeReader()

def getString(imgPath):
    barcode = reader.decode(imgPath)    
    return barcode.parsed


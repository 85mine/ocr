import logging
import os
from logging import getLogger

import click
import pdf2image
from PIL import Image
from tesserocr import PyTessBaseAPI

logging.basicConfig(level=logging.INFO)


# Validate format
def is_valid_format(path):
    file_ext = os.path.splitext(path)[1]
    return file_ext.lower() in ['.jpg', '.png', '.pdf']


# Convert pdf file to image
def pdf_to_image_convert(path):
    return pdf2image.convert_from_path(path)


# Convert an image to black and white to improve quality
def black_white_convert(mixed):
    if isinstance(mixed, str):
        column = Image.open(mixed)
    else:
        column = mixed

    gray = column.convert('L')
    return gray.point(lambda x: 0 if x < 200 else 255, '1')


# Read image content and write to text file
def ocr_processing(image, output):
    logger.info('Starting OCR processing...')
    with PyTessBaseAPI(lang='eng') as api:
        logger.debug('Save ORC content to ' + output + ' file')
        api.SetImage(image)
        # Save content to text file
        f = open(output, "w")
        f.write(api.GetUTF8Text())
        f.close()
    logger.info('OCR processing is completed !')


@click.command()
@click.option('--input', help='Input file (only support PNG/JPEG/PDF)')
@click.option('--output', help='Output text file')
@click.option('--verbose',
              help='Verbose mode - output detailed logs',
              is_flag=True)
def ocr_reading(input, output, verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)

    if is_valid_format(input):
        logger.debug('Input file is supported format')
        file_ext = os.path.splitext(input)[1]
        # Convert PDF file to image file (Tesseract OCR can't read pdf file format)
        if file_ext.lower() in ['.pdf']:
            logger.debug('Starting convert PDF file to image file...')
            images = pdf_to_image_convert(input)
            for pg, img in enumerate(images):
                # If PDF file have many pages
                if len(images) > 1:
                    output_path = os.path.splitext(output)[0] + '.' + str(
                        pg) + os.path.splitext(output)[1]
                else:
                    output_path = output
                # Convert to black & white image
                bw = black_white_convert(img)
                ocr_processing(bw, output_path)
        else:
            # Convert to black & white image
            logger.debug('Starting convert image file to black & white')
            bw = black_white_convert(input)
            ocr_processing(bw, output)
    else:
        logger.error('File format is not supported.')


if __name__ == '__main__':
    logger = getLogger(__name__)
    try:
        ocr_reading()
    except Exception as e:
        logger.error(e)

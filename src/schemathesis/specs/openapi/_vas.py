import random
from base64 import b64encode
from functools import partial

from faker import Faker
from faker_file.providers.bin_file import BinFileProvider
from faker_file.providers.bmp_file import BmpFileProvider
from faker_file.providers.csv_file import CsvFileProvider
from faker_file.providers.docx_file import DocxFileProvider
from faker_file.providers.eml_file import EmlFileProvider
from faker_file.providers.epub_file import EpubFileProvider
from faker_file.providers.gif_file import GifFileProvider
from faker_file.providers.ico_file import GraphicIcoFileProvider, IcoFileProvider
from faker_file.providers.jpeg_file import GraphicJpegFileProvider, JpegFileProvider
from faker_file.providers.mp3_file import Mp3FileProvider
from faker_file.providers.odp_file import OdpFileProvider
from faker_file.providers.ods_file import OdsFileProvider
from faker_file.providers.odt_file import OdtFileProvider
from faker_file.providers.pdf_file import GraphicPdfFileProvider, PdfFileProvider
from faker_file.providers.png_file import GraphicPngFileProvider, PngFileProvider
from faker_file.providers.pptx_file import PptxFileProvider
from faker_file.providers.rtf_file import RtfFileProvider
from faker_file.providers.svg_file import SvgFileProvider
from faker_file.providers.tar_file import TarFileProvider
from faker_file.providers.tiff_file import TiffFileProvider
from faker_file.providers.txt_file import TxtFileProvider
from faker_file.providers.webp_file import GraphicWebpFileProvider, WebpFileProvider
from faker_file.providers.xlsx_file import XlsxFileProvider
from faker_file.providers.zip_file import ZipFileProvider
from hypothesis import strategies as st

from ...serializers import Binary

FAKER = Faker()

FAKER_FILE_PROVIDERS = {
    "eml_file": partial(EmlFileProvider(FAKER).eml_file, raw=True),
    "odt_file": partial(OdtFileProvider(FAKER).odt_file, raw=True),
    "txt_file": partial(TxtFileProvider(FAKER).txt_file, raw=True),
    "bin_file": partial(BinFileProvider(FAKER).bin_file, raw=True),
    # "bmp_file": partial(BmpFileProvider(FAKER).bmp_file, raw=True),  # MB too large
    "csv_file": partial(CsvFileProvider(FAKER).csv_file, raw=True),
    "gif_file": partial(GifFileProvider(FAKER).gif_file, raw=True),
    "docx_file": partial(DocxFileProvider(FAKER).docx_file, raw=True),
    "epub_file": partial(EpubFileProvider(FAKER).epub_file, raw=True),
    "graphic_ico_file": partial(
        GraphicIcoFileProvider(FAKER).graphic_ico_file, raw=True
    ),
    "graphic_pdf_file": partial(
        GraphicPdfFileProvider(FAKER).graphic_pdf_file, raw=True
    ),
    "graphic_png_file": partial(
        GraphicPngFileProvider(FAKER).graphic_png_file, raw=True
    ),
    "graphic_jpeg_file": partial(
        GraphicJpegFileProvider(FAKER).graphic_jpeg_file, raw=True
    ),
    "graphic_webp_file": partial(
        GraphicWebpFileProvider(FAKER).graphic_webp_file, raw=True
    ),
    "jpeg_file": partial(
        JpegFileProvider(FAKER).jpeg_file, raw=True
    ),  # need wkhtmltopdf
    "pptx_file": partial(PptxFileProvider(FAKER).pptx_file, raw=True),
    # "tiff_file": partial(TiffFileProvider(FAKER).tiff_file, raw=True),  # MB too large
    "webp_file": partial(
        WebpFileProvider(FAKER).webp_file, raw=True
    ),  # need wkhtmltopdf
    "xlsx_file": partial(XlsxFileProvider(FAKER).xlsx_file, raw=True),
    "mp3_file": partial(Mp3FileProvider(FAKER).mp3_file, raw=True),
    "odp_file": partial(OdpFileProvider(FAKER).odp_file, raw=True),
    "ods_file": partial(OdsFileProvider(FAKER).ods_file, raw=True),
    "odt_file": partial(OdtFileProvider(FAKER).odt_file, raw=True),
    "pdf_file": partial(PdfFileProvider(FAKER).pdf_file, raw=True),  # need wkhtmltopdf
    "png_file": partial(PngFileProvider(FAKER).png_file, raw=True),  # need wkhtmltopdf
    "ico_file": partial(IcoFileProvider(FAKER).ico_file, raw=True),  # need wkhtmltopdf
    "rtf_file": partial(RtfFileProvider(FAKER).rtf_file, raw=True),
    "svg_file": partial(SvgFileProvider(FAKER).svg_file, raw=True),  # need wkhtmltopdf
    "tar_file": partial(TarFileProvider(FAKER).tar_file, raw=True),
    "txt_file": partial(TxtFileProvider(FAKER).txt_file, raw=True),
    "zip_file": partial(ZipFileProvider(FAKER).zip_file, raw=True),
}


def get_file_strategy() -> st.SearchStrategy[bytes]:
    def get_random_file_bytes(_: int):
        random_file_method_name = random.choice(list(FAKER_FILE_PROVIDERS.keys()))
        return FAKER_FILE_PROVIDERS[random_file_method_name]()

    return st.builds(get_random_file_bytes, st.integers())


VAS_STRING_FORMATS = {
    "binary": get_file_strategy().map(Binary),
    "byte": get_file_strategy().map(lambda x: b64encode(x).decode()),
}

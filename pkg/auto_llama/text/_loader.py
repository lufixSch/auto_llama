import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import BinaryIO, TextIO
from urllib.parse import urlparse

from auto_llama import exceptions
from auto_llama.data import Article

HAS_DEPENDENCIES = True

# Module specific dependencies
try:
    import arxiv
    import marker.cleaners.bullets as mk_bullets_cleaners
    import marker.cleaners.code as mk_code_cleaners
    import marker.cleaners.fontstyle as mk_font_cleaners
    import marker.cleaners.headers as mk_head_cleaners
    import marker.cleaners.headings as mk_headings_cleaners
    import marker.cleaners.text as mk_text_cleaners
    import marker.equations.equations as mk_equations
    import marker.layout.layout as mk_layout
    import marker.layout.order as mk_order
    import marker.models as mk_models
    import marker.ocr.detection as mk_ocr_detection
    import marker.ocr.lang as mk_ocr_lang
    import marker.ocr.recognition as mk_ocr_recognition
    import marker.pdf.extract_text as mk_pdf_extract_text
    import marker.postprocessors.editor as mk_editor
    import marker.postprocessors.markdown as mk_post
    import marker.tables.table as mk_table
    import marker.utils as mk_utils
    import pdftext.extraction as pdftext_ex
    import pdftext.inference as pdftext_inference
    import pdftext.pdf.chars as pdftext_chars
    import pypdfium2 as pdfium
    import requests
    import wikipedia
    from bs4 import BeautifulSoup
    from marker.settings import settings as mk_settings
    from pdftext.settings import settings as pdftext_settings

    from ._util import merge_symbols
except (ImportError, exceptions.ExtrasDependenciesMissing):
    HAS_DEPENDENCIES = False


@dataclass
class FileLike:
    """File representation with a file name and a file-like object"""

    name: str
    stream: BinaryIO | TextIO


class TextLoader(ABC):
    """Load text documents from different sources"""

    def __init__(self) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.ExtrasDependenciesMissing(self.__class__.__name__, "text")

    @abstractmethod
    def __call__(self, source: str) -> Article:
        """Execute loader"""

    @abstractmethod
    def is_valid(self, source: str) -> bool:
        """Check if the source is valid for this loader"""

    def batch(self, sources: list[str]) -> list[Article]:
        """Execute loader for multiple sources"""

        return [self(s) for s in sources]


class WebTextLoader(TextLoader):
    """Load text documents from the web"""

    def __init__(self, seperator: str = "\n") -> None:
        super().__init__()
        self._seperator = seperator

    def __call__(self, source: str) -> Article:
        page = requests.get(source)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.title.string if soup.title else "HTML Page"
        content = soup.get_text(self._seperator, strip=True)
        content = merge_symbols(content, "\n")

        return Article(text=content, title=title, src=source)

    def is_valid(self, source: str) -> bool:
        url = urlparse(source)
        return url.scheme not in ("file", "") and url.netloc


class WikipediaLoader(WebTextLoader):
    """Load text documents from Wikipedia"""

    def __call__(self, source: str) -> Article:
        article = wikipedia.page(source)

        return Article(text=article.content, title=article.title, src=article.url)

    def summary(self, source: str) -> Article:
        article = wikipedia.page(source)

        return Article(text=wikipedia.summary(source), title=article.title, src=article.url)

    def is_valid(self, source: str) -> bool:
        try:
            wikipedia.page(source)
            return True
        except wikipedia.exceptions.PageError:
            return False


class ArxivLoader(TextLoader):
    """Load abstract from Arxiv article"""

    def __init__(self) -> None:
        super().__init__()
        self._client = arxiv.Client()

    def __call__(self, id: str) -> Article:
        article = arxiv.Search(id_list=[id], max_results=1)
        result = next(self._client.results(article))

        return Article(text=result.summary.replace("\n", " "), title=result.title, src=result.pdf_url)

    def search(
        self, topic: str, limit: int = 10, sort: arxiv.SortCriterion = arxiv.SortCriterion.Relevance
    ) -> list[Article]:
        """Search for a given topic and return a list of articles"""

        search = arxiv.Search(topic, max_results=limit, sort_by=sort)
        results = self._client.results(search)

        return [Article(text=res.summary.replace("\n", " "), title=res.title, src=res.pdf_url) for res in results]


class RedditLoader(WebTextLoader):
    """Load text documents from Reddit posts (Only works with links to a single reddit post)"""

    def __call__(self, source: str) -> Article:
        page = requests.get(source)
        soup = BeautifulSoup(page.content, "html.parser")

        # Get h1 with slot=title
        title_el = soup.find(name="h1", attrs={"slot": "title"})
        title = title_el.get_text(strip=True)

        # Get div with slot=post-media-container
        post_el = title_el.find_next(name="div", attrs={"slot": "text-body"})
        content = post_el.get_text(self._seperator, strip=True)
        content = content.rstrip("\nRead more")

        return Article(text=content, title=title, src=source)

    def is_valid(self, source: str) -> bool:
        url = urlparse(source)
        return url.scheme not in ("file", "") and url.netloc and ("reddit" in url.netloc)


class FileLoader(TextLoader):
    """Load text documents from file like objects or file paths"""

    @abstractmethod
    def __call__(self, source: str | FileLike) -> Article:
        """Execute loader with a file like object or file path"""

    @abstractmethod
    def is_valid(self, source: str | FileLike) -> bool:
        """Check if the source is valid for this loader"""


class PDFLoader(FileLoader):
    """Load text documents from PDFs"""

    def __init__(self) -> None:
        super().__init__()

    def _make_doc(self):
        return pdfium.PdfDocument(self.loader_input)

    # def get_text_blocks(self, doc: pdfium.PdfDocument, model):
    #     def _get_page_range(pdf_path, model, page_range):
    #         pdf_doc = self._make_doc()
    #         text_chars = pdftext_chars.get_pdfium_chars(pdf_doc, page_range)
    #         pages = pdftext_inference.inference(text_chars, model)
    #         return page

    #     toc = mk_pdf_extract_text.get_toc(doc)

    #     page_range = range(0, len(doc))

    #     char_blocks = dictionary_output(
    #         fname, page_range=page_range, keep_chars=True, workers=mk_settings.PDFTEXT_CPU_WORKERS
    #     )
    #     char_blocks = _get_pages(pdf_path, model, page_range, workers=workers)

    #     workers = min(
    #         mk_settings.PDFTEXT_CPU_WORKERS, len(page_range) // pdftext_settings.WORKER_PAGE_THRESHOLD
    #     )  # It's inefficient to have too many workers, since we batch in inference

    #     if workers is None or workers <= 1:
    #         text_chars = pdftext_chars.get_pdfium_chars(doc, page_range)
    #         return pdftext_inference.inference(text_chars, model)

    #     func = partial(_get_page_range, pdf_path, model)
    #     page_range = list(page_range)

    #     pages_per_worker = math.ceil(len(page_range) / workers)
    #     page_range_chunks = [page_range[i * pages_per_worker : (i + 1) * pages_per_worker] for i in range(workers)]

    #     with ProcessPoolExecutor(max_workers=workers) as executor:
    #         pages = list(executor.map(func, page_range_chunks))

    #     ordered_pages = [page for sublist in pages for page in sublist]

    #     for page in char_blocks:
    #         page_width, page_height = page["width"], page["height"]
    #         for block in page["blocks"]:
    #             for k in list(block.keys()):
    #                 if k not in ["lines", "bbox"]:
    #                     del block[k]
    #             block["bbox"] = pdftext_ex.unnormalize_bbox(block["bbox"], page_width, page_height)
    #             for line in block["lines"]:
    #                 for k in list(line.keys()):
    #                     if k not in ["spans", "bbox"]:
    #                         del line[k]
    #                 line["bbox"] = pdftext_ex.unnormalize_bbox(line["bbox"], page_width, page_height)
    #                 for span in line["spans"]:
    #                     pdftext_ex._process_span(span, page_width, page_height, False)

    #     marker_blocks = [
    #         mk_pdf_extract_text.pdftext_format_to_blocks(page, pnum) for pnum, page in enumerate(char_blocks)
    #     ]

    #     return marker_blocks, toc

    def __call__(self, source) -> Article:
        # Set language needed for OCR
        langs = [mk_settings.DEFAULT_LANG]

        langs = mk_ocr_lang.replace_langs_with_codes(langs)
        mk_ocr_lang.validate_langs(langs)

        # Find the filetype
        # filetype = find_filetype(fname)

        # Setup output metadata
        # out_meta = {
        # "languages": langs,
        # "filetype": filetype,
        # }

        # if filetype == "other": # We can't process this file
        # return "", {}, out_meta

        # Get initial text blocks from the pdf
        if isinstance(source, str):
            self.loader_input = source
        else:
            self.loader_input = source.stream
            source = source.name

        doc = self._make_doc()
        title = ".".join(os.path.basename(source).split(".")[:-1])
        pages, toc = mk_pdf_extract_text.get_text_blocks(doc, self.loader_input)
        # out_meta.update({
        # "toc": toc,
        # "pages": len(pages),
        # })

        # Trim pages from doc to align with start page
        # if start_page:
        # for page_idx in range(start_page):
        # doc.del_page(0)

        # Unpack models from list
        texify_model, layout_model, order_model, edit_model, detection_model, ocr_model = mk_models.load_all_models(
            langs
        )

        # Identify text lines on pages
        mk_ocr_detection.surya_detection(doc, pages, detection_model, batch_multiplier=1)
        mk_utils.flush_cuda_memory()

        # OCR pages as needed
        pages, ocr_stats = mk_ocr_recognition.run_ocr(doc, pages, langs, ocr_model, batch_multiplier=1)
        mk_utils.flush_cuda_memory()

        # out_meta["ocr_stats"] = ocr_stats
        if len([b for p in pages for b in p.blocks]) == 0:
            raise ValueError(f"Could not parse any text from PDF: {source}")

        mk_layout.surya_layout(doc, pages, layout_model, batch_multiplier=1)
        mk_utils.flush_cuda_memory()

        # Find headers and footers
        bad_span_ids = mk_head_cleaners.filter_header_footer(pages)
        # out_meta["block_stats"] = {"header_footer": len(bad_span_ids)}

        # Add block types in
        mk_layout.annotate_block_types(pages)

        # Dump debug data if flags are set
        # dump_bbox_debug_data(doc, fname, pages)

        # Find reading order for blocks
        # Sort blocks by reading order
        mk_order.surya_order(doc, pages, order_model, batch_multiplier=1)
        mk_order.sort_blocks_in_reading_order(pages)
        mk_utils.flush_cuda_memory()

        # Fix code blocks
        mk_code_cleaners.identify_code_blocks(pages)
        # out_meta["block_stats"]["code"] = code_block_count
        mk_code_cleaners.indent_blocks(pages)

        # Fix table blocks
        mk_table.format_tables(pages)
        # out_meta["block_stats"]["table"] = table_count

        for page in pages:
            for block in page.blocks:
                block.filter_spans(bad_span_ids)
                block.filter_bad_span_types()

        filtered, eq_stats = mk_equations.replace_equations(doc, pages, texify_model, batch_multiplier=1)
        mk_utils.flush_cuda_memory()
        # out_meta["block_stats"]["equations"] = eq_stats

        # Extract images and figures
        # if settings.EXTRACT_IMAGES:
        # extract_images(doc, pages)

        # Split out headers
        mk_headings_cleaners.split_heading_blocks(pages)
        mk_font_cleaners.find_bold_italic(pages)

        # Copy to avoid changing original data
        merged_lines = mk_post.merge_spans(filtered)
        text_blocks = mk_post.merge_lines(merged_lines)
        text_blocks = mk_head_cleaners.filter_common_titles(text_blocks)
        full_text = mk_post.get_full_text(text_blocks)

        # Handle empty blocks being joined
        full_text = mk_text_cleaners.cleanup_text(full_text)

        # Replace bullet characters with a -
        full_text = mk_bullets_cleaners.replace_bullets(full_text)

        # Postprocess text with editor model
        full_text, edit_stats = mk_editor.edit_full_text(full_text, edit_model, batch_multiplier=1)
        mk_utils.flush_cuda_memory()
        # out_meta["postprocess_stats"] = {"edit": edit_stats}
        # doc_images = images_to_dict(pages)

        # return full_text, doc_images, out_meta

        return Article(full_text, title, source)

    def is_valid(self, source) -> bool:
        if isinstance(source, str):
            return os.path.exists(source) and os.path.isfile(source) and source.lower().endswith(".pdf")

        return isinstance(source, FileLike) and source.name.lower().endswith(".pdf")


class PlainTextLoader(FileLoader):
    """Load text from a plain text file"""

    def __init__(self, file_types: list[str] = ["txt", "md"]):
        super().__init__()
        self._file_types = file_types

    def __call__(self, source) -> Article:
        if isinstance(source, str):
            with open(source, "r") as f:
                content = f.read()
        else:
            content = source.stream.read()
            source = source.name

        title = ".".join(os.path.basename(source).split(".")[:-1])
        return Article(content, title, source)

    def is_valid(self, source) -> bool:
        if isinstance(source, str):
            return os.path.basename(source).split(".")[-1] in self._file_types

        return isinstance(source, FileLike) and source.name.lower().split(".")[-1] in self._file_types

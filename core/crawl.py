from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import Any, Dict, List, Sequence


class WebBaseLoaderWithTextSplitter(WebBaseLoader):
    def __init__(self, web_path: str | Sequence[str] = "", header_template: dict | None = None, verify_ssl: bool = True, proxies: dict | None = None, continue_on_failure: bool = False, autoset_encoding: bool = True, encoding: str | None = None, web_paths: Sequence[str] = ..., requests_per_second: int = 2, default_parser: str = "html.parser", requests_kwargs: Dict[str, Any] | None = None, raise_for_status: bool = False, bs_get_text_kwargs: Dict[str, Any] | None = None, bs_kwargs: Dict[str, Any] | None = None, session: Any = None, *, show_progress: bool = True) -> None:
        super().__init__(web_path, header_template, verify_ssl, proxies, continue_on_failure, autoset_encoding, encoding, web_paths,
                         requests_per_second, default_parser, requests_kwargs, raise_for_status, bs_get_text_kwargs, bs_kwargs, session, show_progress=show_progress)
        self.text_splitter = RecursiveCharacterTextSplitter()

    def load(self, web_path: str | Sequence[str] = "", header_template: dict | None = None, verify_ssl: bool = True, proxies: dict | None = None, continue_on_failure: bool = False, autoset_encoding: bool = True, encoding: str | None = None, web_paths: Sequence[str] = ..., requests_per_second: int = 2, default_parser: str = "html.parser", requests_kwargs: Dict[str, Any] | None = None, raise_for_status: bool = False, bs_get_text_kwargs: Dict[str, Any] | None = None, bs_kwargs: Dict[str, Any] | None = None, session: Any = None, *, show_progress: bool = True) -> Any:
        documents = super().load(web_path, header_template, verify_ssl, proxies, continue_on_failure, autoset_encoding, encoding, web_paths,
                                 requests_per_second, default_parser, requests_kwargs,  raise_for_status, bs_get_text_kwargs, bs_kwargs, session, show_progress=show_progress)
        return self.text_splitter(documents)


def create(paths: List[str]):
    loader = WebBaseLoader(web_paths=paths)
    return loader

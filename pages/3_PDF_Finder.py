"""Streamlit page that discovers and previews PDF files in a directory tree."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import List

import streamlit as st


st.set_page_config(page_title="PDF Finder", layout="wide")


def find_pdfs(base_dir: Path) -> List[Path]:
    """Return a sorted list of PDF file paths under ``base_dir``.

    The search is recursive, case-insensitive, and ignores non-files (e.g.,
    directories or broken symlinks).
    """

    pdfs: List[Path] = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() == ".pdf":
            pdfs.append(path)
    return sorted(pdfs)


def format_size(num_bytes: int) -> str:
    """Pretty-print a file size using binary units."""

    step = 1024
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(num_bytes)
    for unit in units:
        if size < step:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= step
    return f"{size:.1f} PiB"


def main() -> None:
    st.title("PDF Finder")
    st.write(
        "Quickly scan a directory tree for PDF files, see their details, and preview",
        " or download them directly from this page.",
    )

    st.sidebar.header("Search settings")
    default_dir = Path.cwd()
    directory_input = st.sidebar.text_input(
        "Base directory",
        value=str(default_dir),
        help="Enter an absolute or relative path to scan for PDF files.",
    )

    base_dir = Path(directory_input).expanduser().resolve()

    if not base_dir.exists():
        st.error("The provided directory does not exist. Update the path and try again.")
        return
    if not base_dir.is_dir():
        st.error("The provided path points to a file. Please enter a directory path instead.")
        return

    pdf_paths = find_pdfs(base_dir)
    st.subheader("Results")
    st.caption(
        "Listing PDFs recursively under the provided base directory."
        " Paths are shown relative to the base directory for easier reading."
    )

    if not pdf_paths:
        st.info("No PDF files were found. Try another directory or add PDFs to scan.")
        return

    relative_paths = [path.relative_to(base_dir) for path in pdf_paths]
    table_rows = [
        {
            "PDF": str(rel_path),
            "Size": format_size(path.stat().st_size),
            "Modified": dt.datetime.fromtimestamp(path.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        for rel_path, path in zip(relative_paths, pdf_paths)
    ]

    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    st.subheader("Quick preview")
    selected = st.selectbox("Choose a PDF to preview", relative_paths)
    selected_path = base_dir / selected

    with selected_path.open("rb") as pdf_file:
        st.download_button(
            label="Download selected PDF",
            data=pdf_file,
            file_name=selected_path.name,
            mime="application/pdf",
        )

    st.write("Preview below:")
    st.pdf(selected_path)


if __name__ == "__main__":
    main()

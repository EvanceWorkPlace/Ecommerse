from django.core.management.base import BaseCommand
import os
from pathlib import Path

from chatbot.langchain_utils import build_vectorstore_from_texts

DOCS_DIR = Path.cwd().joinpath("docs")  # project_root/docs

class Command(BaseCommand):
    help = "Ingest documents from the docs/ folder into the Chroma vectorstore."

    def handle(self, *args, **options):
        if not DOCS_DIR.exists():
            self.stdout.write(self.style.ERROR(f"Docs directory not found at {DOCS_DIR}"))
            return

        texts = []
        for f in DOCS_DIR.iterdir():
            if f.is_file() and f.suffix.lower() in ('.txt', '.md', '.html'):
                text = f.read_text(encoding='utf-8')
                texts.append(text)
                self.stdout.write(f"Ingesting {f.name}...")

        if not texts:
            self.stdout.write(self.style.WARNING("No documents found to ingest."))
            return

        build_vectorstore_from_texts(texts, persist=True)
        self.stdout.write(self.style.SUCCESS("Ingestion complete — vectorstore persisted."))

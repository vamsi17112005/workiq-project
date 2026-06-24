from app.database import SessionLocal

from app.models.db_models import (
    Source,
    DocumentChunk
)

from app.services.extractors.pdf_extractor import (
    extract_pdf
)

from app.services.extractors.image_extractor import (
    extract_images
)

from app.services.chunkers.pdf_chunker import (
    build_chunks
)

from app.services.embeddings.embedding_services import (
    generate_embedding
)


def ingest_pdf(
    pdf_path,
    image_output_dir
):

    db = SessionLocal()

    try:

        print("Extracting PDF...")

        doc = extract_pdf(
            pdf_path
        )

        print("Extracting Images...")

        images = extract_images(
            pdf_path,
            image_output_dir
        )

        print("Building Chunks...")

        chunks = build_chunks(
            doc,
            images
        )

        source = Source(
            source_type="pdf",
            source_name=pdf_path.split("\\")[-1],
            source_identifier=pdf_path
        )

        db.add(source)

        db.commit()

        db.refresh(source)

        print(
            f"Source ID: {source.id}"
        )

        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(
                chunk.content
            )

            db_chunk = DocumentChunk(
                source_id=source.id,

                chunk_title=chunk.title,

                chunk_text=chunk.content,

                chunk_index=index,

                chunk_metadata=chunk.metadata,

                embedding=embedding
            )

            db.add(db_chunk)

        db.commit()

        print(
            f"Stored {len(chunks)} chunks successfully."
        )

    except Exception as e:

        db.rollback()

        print(
            f"Error: {e}"
        )

    finally:

        db.close()
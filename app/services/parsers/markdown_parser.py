from models.document_element import DocumentElement


def parse_markdown(markdown_text: str):
    elements = []

    lines = markdown_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Image
        if line == "<!-- image -->":

            elements.append(
                DocumentElement(
                    element_type="image",
                    content=""
                )
            )

        # Heading
        elif line.startswith("#"):

            heading = line.lstrip("#").strip()

            elements.append(
                DocumentElement(
                    element_type="heading",
                    content=heading
                )
            )

        # List Item
        elif line.startswith("- "):

            elements.append(
                DocumentElement(
                    element_type="list",
                    content=line[2:]
                )
            )

        # Form Fields (Name: _________)
        elif line.count("\\_") > 10:

            elements.append(
                DocumentElement(
                    element_type="form_field",
                    content=line
                )
            )

        # Email
        elif "mailto:" in line:

            elements.append(
                DocumentElement(
                    element_type="email",
                    content=line
                )
            )

        # Table Row (future PDFs may contain markdown tables)
        elif "|" in line:

            elements.append(
                DocumentElement(
                    element_type="table",
                    content=line
                )
            )

        # Paragraph
        else:

            elements.append(
                DocumentElement(
                    element_type="paragraph",
                    content=line
                )
            )

    return elements
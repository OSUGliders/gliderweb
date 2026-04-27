from django.templatetags.static import static


SEAGLIDER_DOCUMENTS_BASE_PATH = "images/SeaGlider"

OPERATIONS_AND_GUIDES_META = (
    {
        "title": "Parameter Reference Manual",
        "summary": "Core operating parameters and reference material for Seaglider missions.",
        "file": "Parameter_Reference_Manual.pdf",
        "tag": "Reference",
    },
    {
        "title": "Seaglider Pilot's Guide",
        "summary": "Operational guide for piloting, mission planning, and field use.",
        "file": "Seaglider_Pilot's_Guide.pdf",
        "tag": "Operations",
    },
)

TECHNICAL_DOCUMENTATION_META = (
    {
        "title": "Extended PicoDOS Reference Manual",
        "summary": "Extended reference for PicoDOS commands and system behavior.",
        "file": "Extended_PicoDOS_Ref_Man.pdf",
        "tag": "Reference",
    },
    {
        "title": "SG File Formats Manual",
        "summary": "Documentation describing Seaglider file structure and formats.",
        "file": "Seaglider_File_Formats_Manual.pdf",
        "tag": "Technical",
    },
    {
        "title": "Piloting Tools User Guide",
        "summary": "User guide for piloting tools and supporting workflows.",
        "file": "Piloting Tools User Guide.pdf",
        "tag": "Guide",
    },
)


def build_document_links(document_meta):
    documents = []
    for item in document_meta:
        relative_path = f"{SEAGLIDER_DOCUMENTS_BASE_PATH}/{item['file']}"
        documents.append(
            {
                "title": item["title"],
                "summary": item["summary"],
                "file": relative_path,
                "url": static(relative_path),
                "tag": item["tag"],
            }
        )
    return documents


def get_seaglider_documents_context():
    operations_and_guides = build_document_links(OPERATIONS_AND_GUIDES_META)
    technical_documentation = build_document_links(TECHNICAL_DOCUMENTATION_META)
    return {
        "operations_and_guides": operations_and_guides,
        "technical_documentation": technical_documentation,
        "document_total": len(operations_and_guides) + len(technical_documentation),
    }
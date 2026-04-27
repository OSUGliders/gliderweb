from django.templatetags.static import static


SLOCUM_MANUALS_BASE_PATH = "images/Slocum/Slocum_manuals"

TRAINING_MANUALS_META = (
    {
        "title": "Glider Training Presentation",
        "summary": "Introductory slide deck for Slocum platform orientation and training.",
        "file": "glider_training_presentation_2015.pdf",
        "tag": "Training",
    },
    {
        "title": "Slocum Glider Operators Training Guide",
        "summary": "Step-by-step guidance for operator onboarding and mission execution.",
        "file": "Slocum_Glider_Operators_Training_Guide.pdf",
        "tag": "Training",
    },
    {
        "title": "Slocum G1 Glider Manual",
        "summary": "Core G1 vehicle manual covering systems, handling, and operation.",
        "file": "Slocum_G1_Glider_Manual.pdf",
        "tag": "Manual",
    },
    {
        "title": "Slocum G3S Operator Manual",
        "summary": "Operational procedures and reference material for the G3S platform.",
        "file": "G3S Glider Operator Manual 2025-07-18.pdf",
        "tag": "Operations",
    },
    {
        "title": "Slocum G2 Glider Maintenance Manual",
        "summary": "Maintenance procedures and service instructions for G2 systems.",
        "file": "Slocum_G2_Glider_Maintenance_Manual.pdf",
        "tag": "Maintenance",
    },
    {
        "title": "Slocum G3S Maintenance Manual",
        "summary": "Maintenance and servicing guidance specific to the G3S platform.",
        "file": "G3S Glider Maintenance Manual 2025-07-18.pdf",
        "tag": "Maintenance",
    },
    {
        "title": "Slocum G3 Taking Science Bay Apart",
        "summary": "Deconstruction walkthrough for the G3 science bay assembly.",
        "file": "G3_Deconstruction.pptx",
        "tag": "Workshop",
    },
)

TECHNICAL_REFERENCES_META = (
    {
        "title": "SFMC Manual",
        "summary": "Complete user manual for SFMC software version 8.7.0-1.",
        "file": "SFMC User Manual [M313834-NFC, Rev B] Software Ver 8.7.0-1.pdf",
        "tag": "Manual",
    },
    {
        "title": "SFMC HOWTO (Nilza)",
        "summary": "Practical SFMC how-to reference for day-to-day operator tasks.",
        "file": "SFMC_CheatSheet.pdf",
        "tag": "How-To",
    },
    {
        "title": "SFMC Install Manual",
        "summary": "Installation and setup guide for SFMC software version 8.7.0-1.",
        "file": "SFMC Installation Guide [M313589-NFC, Rev B] Software Ver 8.7.0-1.pdf",
        "tag": "Installation",
    },
    {
        "title": "Dock Server User Guide",
        "summary": "User guide for dock server operation, configuration, and routine use.",
        "file": "gmcUserGuide.pdf",
        "tag": "Guide",
    },
    {
        "title": "SFMC 8.7 Release Notes",
        "summary": "Release notes for SFMC 8.7.0 with key changes and known updates.",
        "file": "SFMC 8.7.0 Release Notes.pdf",
        "tag": "Release Notes",
    },
    {
        "title": "G3S Guide",
        "summary": "Processor and software guide for G3S systems.",
        "file": "G3S New Processor Guide Draft B.pdf",
        "tag": "Guide",
    },
)


def build_document_links(document_meta):
    documents = []
    for item in document_meta:
        relative_path = f"{SLOCUM_MANUALS_BASE_PATH}/{item['file']}"
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


def get_slocum_documents_context():
    training_manuals = build_document_links(TRAINING_MANUALS_META)
    technical_references = build_document_links(TECHNICAL_REFERENCES_META)
    return {
        "training_manuals": training_manuals,
        "technical_references": technical_references,
        "document_total": len(training_manuals) + len(technical_references),
    }

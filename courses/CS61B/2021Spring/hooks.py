"""Small MkDocs hooks for course-specific navigation behavior."""


def on_page_context(context, page, config, nav):
    """Keep hidden page outlines out of the integrated left navigation."""
    hidden = page.meta.get("hide", [])
    if isinstance(hidden, str):
        hidden = [hidden]
    if "toc" in hidden:
        page.toc = []
    return context

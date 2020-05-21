import panflute


def prepare(doc):
    doc.isInToc = False
    pass


def action(elem, doc):
    if (not doc.isInToc and
            isinstance(elem, panflute.Header) and
            panflute.stringify(elem) == "Table of Contents"):
        doc.isInToc = True
        return []
    if doc.isInToc and isinstance(elem, panflute.ListItem):
        return []
    if doc.isInToc and isinstance(elem, panflute.Header):
        doc.isInToc = False


def finalize(doc):
    pass


def main(doc=None):
    return panflute.run_filter(
        action,
        prepare=prepare,
        finalize=finalize,
        doc=doc
    )


if __name__ == "__main__":
    main()

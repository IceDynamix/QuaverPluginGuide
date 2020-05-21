import panflute


def prepare(doc):
    pass


def action(elem, doc):
    if isinstance(elem, panflute.Header):
        if elem.level == 1:
            doc.metadata["title"] = panflute.stringify(elem)
            return []
        else:
            elem.level -= 1


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

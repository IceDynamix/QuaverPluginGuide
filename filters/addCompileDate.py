from panflute import run_filter
from datetime import date


def prepare(doc):
    doc.metadata["date"] = date.today().isoformat()


def action(elem, doc):
    pass


def finalize(doc):
    pass


def main(doc=None):
    return run_filter(
        action,
        prepare=prepare,
        finalize=finalize,
        doc=doc
    )


if __name__ == "__main__":
    main()

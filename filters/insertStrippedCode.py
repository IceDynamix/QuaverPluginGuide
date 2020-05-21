import panflute
import re


def prepare(doc):
    doc.commentRegex = re.compile(
        r"<!-- ?insert(?P<type>\w+), ?(?P<path>[\S]+) ?-->"
    )

    # https://regex101.com/r/tIGOhh/1

    reSummary = r"(?:[ ]+/// <summary>[\s/]+(?P<summary>.*?)" + \
        r"\s+/// </summary>(?:\s+///.*$)*\n)?"
    reExcludeNonVisible = r"(?<!\[MoonSharpVisible\(false\)\]\n)"
    reVisibility = r"(?P<visibility>public|private|protected)(?(visibility) |)"
    reStatic = r"(?P<static>static)?(?(static) |)"
    reMethod = r"(?P<method>[\w]+ [\w]+(?:\(.*?\)| =>.*))"
    reEnum = r"(?P<enum>enum \w+)"
    reAttribute = r"(?!class)(?!sealed)(?P<attribute>[\w<>]+ \w+)"
    reCurlyBrackets = r"(?:(?:\n(?P<indent>^ +)| ){(?P<curlyContent>(?(indent)[\s\S]*?^(?P=indent)|.*))})?"

    regex = reSummary + reExcludeNonVisible + r"^\s+" + reVisibility + \
        reStatic + r"(?:" + "|".join([reMethod, reEnum, reAttribute]) + r")" + \
        reCurlyBrackets

    doc.regex = re.compile(regex, re.MULTILINE)


def stripCodeFile(doc, insertType: str, path: str) -> str:
    with open(path) as file:
        fileContent = file.read()
        strippedFile = ["// " + path[2:]]

        for match in doc.regex.finditer(fileContent):

            summary = match.group("summary")
            curlyContent = match.group("curlyContent")
            method = match.group("method")
            attribute = match.group("attribute")

            currentElement = []
            no = False

            if summary:
                currentElement += ["// " + summary]

            if insertType == "ClassMethods" and method:
                currentElement += [method + ";"]

            elif insertType == "ClassAttributes" and attribute:
                if curlyContent:
                    getSet = re.sub(r"\s+", " ", curlyContent).strip()
                    attribute += f' {{ {getSet} }}'
                currentElement += [attribute]

            elif insertType == "Enum" and curlyContent:
                currentElement.extend(
                    [line.strip() for line in curlyContent.strip().split("\n")]
                )

            else:
                no = True

            if not no:
                strippedFile.append("\n".join(currentElement))

        return "\n\n".join(strippedFile)
    pass


def action(elem, doc):
    # is comment
    if (isinstance(elem, panflute.RawBlock)):
        matchResult = doc.commentRegex.match(panflute.stringify(elem))
        if matchResult:
            insertType = matchResult.group("type")
            path = f"./{matchResult.group('path')}"
            content = stripCodeFile(doc, insertType, path)
            return panflute.CodeBlock(content, classes=["cs"])


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

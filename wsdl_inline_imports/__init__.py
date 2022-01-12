__version__ = '0.1.0'

from io import FileIO, BytesIO
from pathlib import Path
from typing import Any, Iterable, Tuple
from lxml import etree
import re
from loguru import logger

def process_file(path: Path) -> str:
    logger.info(f"Processing file {path}")

    parser = etree.XMLPullParser(events=['end'])

    indent: int
    with open(path) as file:
        indent = compute_indent(file)

    with open(path) as file:
        parser.feed(file.read())
        events = parser.read_events()
        expand_imports(path, events)
        result = parser.close()
        etree.indent(result, space=' ' * indent)

        logger.info(f"Done processing {path}")
        return bytes.decode(etree.tostring(result, pretty_print=True, xml_declaration=True, encoding='utf-8'), 'utf-8')

def expand_imports(wsdl_path: Path, events: Iterable[Tuple[str, Any]]):
    for _, elem in events:
        qualified_name = etree.QName(elem.tag)
        if qualified_name.namespace == "http://www.w3.org/2001/XMLSchema" and qualified_name.localname == "schema":
            import_elem = next((el for el in elem if isinstance(el.tag, str) and etree.QName(el.tag).localname == "import"), None)

            if import_elem is not None:
                location = import_elem.get("schemaLocation")
                schema_path = wsdl_path.parent / location
                processed_schema = process_file(schema_path)

                logger.debug(f"processed schema:\n{processed_schema}")

                schema_tree = etree.parse(BytesIO(str.encode(processed_schema, 'utf-8')))
                logger.debug(f"import element: \n{bytes.decode(etree.tostring(elem, pretty_print=True), 'utf-8')}")

                elem.remove(import_elem)
                for child in schema_tree.getroot():
                    elem.append(child)
            else:
                logger.warning(f"Schema with no import element: {elem}")
                logger.warning(f"Schema:\n{bytes.decode(etree.tostring(elem, pretty_print=True), 'utf-8')}")


def compute_indent(file: FileIO) -> int:
    m = re.search(r'^ +', file.read(), flags=re.MULTILINE)

    return len(m.group(0))

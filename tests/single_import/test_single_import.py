from pathlib import Path
from wsdl_inline_imports import process_file

def test_single_import():
    input_path = Path("./tests/single_import/foo.wsdl")

    expected_result: str
    with open('./tests/single_import/foo.wsdl.expected') as expected_file:
        expected_result = expected_file.read()

        assert process_file(input_path) == expected_result

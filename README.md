 # wsdl-inline-imports

 Tool to inline XSD schemas inside WSDL files.
Its main use it's to make WSDL files with external imports usable into Azure API Management ([see here](https://stackoverflow.com/questions/48936766/how-can-i-import-a-wsdl-in-azure-api-management))

## Usage

```shell
$ python wsdl_inline_imports.py -i foo.wsdl -o foo_with_imports.wsdl
```

```
usage: wsdl_inline_imports.py [-h] -i INPUT [-o OUTPUT]

Inline external imports into a WSDL file.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file
  -o OUTPUT, --output OUTPUT
                        output file. If omitted print result to stdout
```
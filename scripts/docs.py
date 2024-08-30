from frictionless import Package, Resource
import random
import typer
from pathlib import Path
import petl as etl
import json

def sample_field(resource, field_name, size=3):
    # return str(etl.look(resource.to_petl().cut(field_name).data()))
    return '<br>'.join(random.sample(list(resource.to_petl().values(field_name)), size))

def format_notas(value):
    if value:
        numbering = range(1, len(value)+1)
        result = [f"{n}.{val}" for n,val in zip(numbering, value)]
        return "<br>".join(result)
    else:
        return ""

def format_constraints(value):
    if value:
        return json.dumps(value, indent = 4).replace("\n", "<br>")
    else:
        return ""

header = ['a', 'b']
data = [[1, 2], [3, 4]]
tbl = [header] + data # good

x = str(etl.wrap(tbl).data())

def to_data_dictionary(path):
    package = Package(path)

    header = ['tabela', 'coluna', 'restrições', 'notas', 'exemplos', 'assunto', 'objeto']

    data = [
        [resource.name,
         field.name,
         format_constraints(field.constraints),
         format_notas(field.custom.get('notas')),
         sample_field(resource, field.name),
         field.custom.get('assunto'),
         field.custom.get('objeto')]
        for resource in package.resources
        for field in resource.schema.fields
    ]

    resource = Resource(data = [header] + data)
    result = resource.to_petl()
    return result

def main(packages: list[str]):
    data_dictionary = [to_data_dictionary(package) for package in packages]
    result = etl.cat(*data_dictionary)
    result.tocsv("data-dictionary.csv")
    result.todataframe().to_html("data-dictionary.html", escape=False)

if __name__ == "__main__":
    typer.run(main)

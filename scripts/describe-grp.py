from frictionless import Package, Resource
import random
import typer
from pathlib import Path
import petl as etl

def sample_field(resource, field_name, size=3):
    return '; '.join(random.sample(list(resource.to_petl().values(field_name)), size))

def format_notas(value):
    if value:
        numbering = range(1, len(value)+1)
        result = [f"{n}) {val}\n" for n,val in zip(numbering, value)]
        return "".join(result)
    else:
        return ""

def to_data_dictionary(path):
    package = Package(path)

    header = ['consulta', 'assunto', 'objeto', 'exemplos', 'notas']

    data = [
        [
             resource.name,
             field.custom.get('assunto'),
             field.name,
             sample_field(resource, field.name),
             format_notas(field.custom.get('notas')),
        ]
        for resource in package.resources
        for field in resource.schema.fields
    ]

    resource = Resource(data = [header] + data)
    result = resource.to_petl()
    return result

def main(packages: list[str]):
    data_dictionary = [to_data_dictionary(package) for package in packages]
    result = etl.cat(*data_dictionary)
    result.toxlsx(f'data-dictionary-grp.xlsx')

if __name__ == "__main__":
    typer.run(main)

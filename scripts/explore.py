from frictionless import Package
from toolkit import line_mode

sigplan_pkg = Package("datapackages/sigplan/datapackage.yaml")
grp_pkg = Package("datapackages/grp/datapackage.yaml")

sigplan_pkg.resource_names
grp_pkg.resource_names

sigplan = sigplan_pkg.get_resource("tb_execorcamentariasiafi").to_petl()
grp = grp_pkg.get_resource("tb_execorcamentariasiafi_a").to_petl()

grp.cut("Valor Crédito Autorizado")

line_mode(sigplan, 1)
line_mode(grp, 1)

sorted(set(sigplan.values("CODIGO_ITEM")))
sorted(set(grp.values("Valor Crédito Autorizado")))
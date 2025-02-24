from code_datasource import CodeDatasource

plugin = CodeDatasource()
nodes = plugin.load()

print("Loaded Nodes:", [vars(node) for node in nodes])
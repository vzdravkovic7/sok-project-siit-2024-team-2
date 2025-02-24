from code_datasource import CodeDatasource

plugin = CodeDatasource()
graph = plugin.load()

print("Loaded Nodes:", [vars(node) for node in graph.nodes])
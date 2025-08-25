from .parser import parse_command

class GraphCLI:
    _instance = None

    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def get_instance(cls, graph=None):
        if cls._instance is None and graph is not None:
            cls._instance = GraphCLI(graph)
        return cls._instance

    def run(self, cmd_str):
        cmd = parse_command(cmd_str)
        if not cmd:
            return f"Unknown command: {cmd_str}"
        cmd.execute(self.graph)

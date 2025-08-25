from .parser import parse_command

class GraphCLI:
    """
    Singleton class representing a command-line interface for interacting with a graph.
    It parses and executes commands on the graph.
    """
    _instance = None

    def __init__(self, graph):
        """
        Initialize the CLI with a graph instance.

        Args:
            graph (Graph): The graph instance to operate on.
        """
        self.graph = graph

    @classmethod
    def get_instance(cls, graph=None):
        """
        Get the singleton instance of the GraphCLI.
        If it does not exist, create a new instance with the provided graph.

        Args:
            graph (Graph, optional): The graph instance to initialize the CLI. Required only if no instance exists.

        Returns:
            GraphCLI: The singleton instance of the CLI.
        """
        if cls._instance is None and graph is not None:
            cls._instance = GraphCLI(graph)
        return cls._instance

    def run(self, cmd_str):
        """
        Parse and execute a command string on the graph.

        Args:
            cmd_str (str): The command string to execute.

        Returns:
            str|None: Returns an error message if the command is unknown; otherwise None.
        """
        cmd = parse_command(cmd_str)
        if not cmd:
            return f"Unknown command: {cmd_str}"
        cmd.execute(self.graph)

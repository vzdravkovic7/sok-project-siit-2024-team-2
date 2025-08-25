from .command import (
    CreateNodeCommand, CreateEdgeCommand,
    EditNodeCommand, DeleteNodeCommand,
    DeleteEdgeCommand, ClearGraphCommand
)


def parse_command(cmd_str: str):
    tokens = cmd_str.strip().split()
    if not tokens:
        return None

    cmd_type = tokens[0].lower()

    if cmd_type == "create":
        if len(tokens) < 2:
            return None

        if tokens[1] == "node":
            node_id = None
            props = {}
            i = 2
            while i < len(tokens):
                token = tokens[i]
                if token.startswith("--id="):
                    node_id = token.split("=", 1)[1]
                elif token == "--property" and i + 1 < len(tokens):
                    prop_pair = tokens[i + 1]
                    if "=" in prop_pair:
                        k, v = prop_pair.split("=", 1)
                        props[k] = v
                    i += 1
                i += 1
            if node_id is None:
                return None
            return CreateNodeCommand(node_id, props)

        if tokens[1] == "edge":
            if len(tokens) < 4:
                return None
            from_id = tokens[2]
            to_id = tokens[3]
            return CreateEdgeCommand(from_id, to_id)

    if cmd_type == "edit":
        if len(tokens) < 2:
            return None

        if tokens[1] == "node":
            node_id = None
            props = {}
            i = 2
            while i < len(tokens):
                token = tokens[i]
                if token.startswith("--id="):
                    node_id = token.split("=", 1)[1]
                elif token == "--property" and i + 1 < len(tokens):
                    prop_pair = tokens[i + 1]
                    if "=" in prop_pair:
                        k, v = prop_pair.split("=", 1)
                        props[k] = v
                    i += 1
                i += 1
            if node_id is None:
                return None
            return EditNodeCommand(node_id, props)

    if cmd_type == "delete":
        if len(tokens) < 2:
            return None

        if tokens[1] == "node":
            node_id = None
            for t in tokens[2:]:
                if t.startswith("--id="):
                    node_id = t.split("=", 1)[1]
                    break
            if node_id is None:
                return None
            return DeleteNodeCommand(node_id)

        if tokens[1] == "edge":
            if len(tokens) < 4:
                return None
            from_id = tokens[2]
            to_id = tokens[3]
            return DeleteEdgeCommand(from_id, to_id)

    if cmd_type == "clear":
        return ClearGraphCommand()

    return None

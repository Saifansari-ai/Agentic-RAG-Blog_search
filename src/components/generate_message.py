class GenMessage:
    def __init__(self):
        pass
    def generate_message(self,graph, inputs):
        generated_message = ""

        for output in graph.stream(inputs):
            for key, value in output.items():
                print(f"{key} + 4")
                print(f"{value} + 5")
                if key == "generate" and isinstance(value, dict):
                    msgs = value.get("messages", [])
                    if msgs:
                        generated_message = msgs[0]
        print(f"{generated_message} + 6")
        return generated_message

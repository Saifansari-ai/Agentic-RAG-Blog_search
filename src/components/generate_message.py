class GenMessage:
    def __init__(self):
        pass
    def generate_message(self,graph, inputs):
        generated_message = ""

        for output in graph.stream(inputs):
            for key, value in output.items():
                if key == "generate" and isinstance(value, dict):
                    generated_message = value.get("messages", [""])[0]
        
        return generated_message

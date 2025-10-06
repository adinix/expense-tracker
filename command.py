class Handler:
    def __init__(self, func, description):
        """Initializes a handler function and its description"""
        self.func = func
        self.desc = description

class Command:
    def __init__(self):
        """Initializes a new instance of Command"""
        self.handlers_map = {}

    def register_handlers(self, command: str, handlers: list[Handler]):
        """Registers a list of handlers for a specific command"""
        self.handlers_map[command] = handlers

    def list_command(self):
        """Returns a list of registered commands"""
        command_list = []
        for command in self.handlers_map:
            command_list.append(command)
        return command_list

    def run(self, command: str):
        """Runs a command"""
        if command in self.handlers_map:
            if len(self.handlers_map[command]) == 1:
                self.handlers_map[command][0].func()
            else:
                handlers = self.handlers_map[command]
                for i in range(len(handlers)):
                    print(f"{i+1}: {handlers[i].desc}")
                choice = 0
                while choice > len(handlers) or choice < 1:
                    choice = int(input("Select a command to run (enter the number):"))
                handler = handlers[choice-1]
                handler.func()

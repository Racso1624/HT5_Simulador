class Event:

    def __init__(self, memory, instructions):
        self.eventmemory = memory
        self.eventinstructions = instructions

    def memory(self):
        return self.eventmemory

    def instructions(self):
        return self.eventinstructionsciclo

    def resta(self):
        self.eventinstructions - 3

    def isDone(self):
        return self.eventinstructions <= 0
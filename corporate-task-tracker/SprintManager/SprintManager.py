from Sprint.Sprint import Sprint

class SprintManager:
    __sprints = []

    def AddSprint(self, sprint: Sprint):
        self.__sprints.append(sprint)

    def GetSprints(self):
        return self.__sprints
        
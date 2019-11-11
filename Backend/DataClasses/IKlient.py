import abc


class IKlient:
    @abc.abstractmethod
    def GetId(self):
        pass

class MatchResultModel:
    FileName : str
    EnumType : str
    EnumValue : str
    LineContent : str

class EnumModel:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class ServiceModel:
    FileName : str
    Service : str
    UI_Action : str
    API_Url : str
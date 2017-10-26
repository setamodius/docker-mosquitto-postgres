class User:


    def __init__(self):
        self._name = ""
        self._privileges = 0
        self._username = "-EMPTY-"
        self._id = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def privileges(self):
        return self._privileges

    @privileges.setter
    def privileges(self, value):
        self._privileges = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

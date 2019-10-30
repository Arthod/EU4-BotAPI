class Value:
    def __init__(self, name, box, value=0):
        self.name = name
        self.box = box
        self.value = value

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value

    def get_box(self):
        return self.box

    def get_name(self):
        return self.name
class Province:
    def __init__(self, id, name, color_rgb, position):
        self.id = id
        self.name = name
        self.color_rgb = color_rgb
        self.pos = position

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos
class ValueLocation:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect

    def get_rect(self):
        return (self.rect.x, self.rect.y, self.rect.w+self.rect.x, self.rect.h+self.rect.y)
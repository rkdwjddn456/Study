class screen:
    def __init__(self, name,pad_width = 1250, pad_height = 800):
        self.pad_width = pad_width
        self.pad_height = pad_height
        self.screen = pygame.display.set_mode((self.pad_width, self.pad_height))
        pygame.display.set_caption(name)

import pygame

class RGB_Square:
    
    def __init__(
            self,
            width: int,
            height: int,
            center: tuple[int, int],
            base_color: tuple[int, int, int],
            background_color: tuple[int, int, int, int] | str = "#FFFFFF42"
        ) -> None:
        self.draw_surface = pygame.Surface((width, height)).convert_alpha()
        self.draw_rect = self.draw_surface.get_rect(center=center)

        self.base_color = base_color

        cursor_width = round(width / 10)
        cursor_height = round(height / 10)
        surf_size = (width - cursor_width, height - cursor_height)

        self.surface = pygame.Surface((256, 256))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, surf_size)

        self.x_offset = round((self.draw_surface.get_width() - self.surface.get_width()) / 2)
        self.y_offset = round((self.draw_surface.get_height() - self.surface.get_height()) / 2)
        self.surface_rect = self.surface.get_rect(topleft=(self.x_offset, self.y_offset))

        self.select = False
        self.color_change = True

        self.cursor_surface = pygame.Surface((cursor_width, cursor_height)).convert_alpha()
        self.cursor_rect = self.cursor_surface.get_rect()
        self.cursor_border_thickness = int(min(max(cursor_height//10, 1), max(cursor_width//10, 1)))
        self.move_cursor(self.surface_rect.right, self.surface_rect.top)

        self.background_color = background_color

    def creat_color(self, x, y):
        x = 255-x
        col = lighten_color(self.base_color, x)
        final_color = darken_color(col, y)
        return final_color
    
    def __color_surface(self):
        for x in range(256):
            for y in range(256):
                color = self.creat_color(x, y)
                self.surface.set_at((x, y), color)
    
    def draw(self, surface):
        self.draw_surface.fill(self.background_color)
        self.draw_surface.blit(self.surface, self.surface_rect)
        self.draw_surface.blit(self.cursor_surface, self.cursor_rect)
        surface.blit(self.draw_surface, self.draw_rect)
    
    def move_cursor(self, x, y):
        self.color_change = True
        x = x - self.surface_rect.x
        y = y - self.surface_rect.y
        self.cursor = (min(max(x, 0), self.surface_rect.width - 1), min(max(y, 0), self.surface_rect.height - 1))
        self.cursor_color = self.surface.get_at(self.cursor)
        self.cursor_rect.center = (1 + self.cursor[0] + self.x_offset, 1 + self.cursor[1] + self.y_offset)

        self.cursor_surface.fill((0, 0, 0, 0))
        rect_coordon = (0, 0, self.cursor_rect.width, self.cursor_rect.height)
        pygame.draw.rect(self.cursor_surface, self.cursor_color, rect_coordon, border_radius=9999)
        pygame.draw.rect(self.cursor_surface, "#FFFFFF", rect_coordon, self.cursor_border_thickness, 9999)
    
    def handle_event(self, event: pygame.event.Event, sub_surface_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - sub_surface_pos[0] - self.draw_rect.x, event.pos[1] - sub_surface_pos[1] - self.draw_rect.y)
            is_colliding = self.surface_rect.collidepoint(pos) or self.cursor_rect.collidepoint(pos)
            if is_colliding:
                self.select = True
                self.move_cursor(*pos)
        if event.type == pygame.MOUSEBUTTONUP:
            self.select = False
        if event.type == pygame.MOUSEMOTION:
            if self.select:
                pos = (event.pos[0] - sub_surface_pos[0] - self.draw_rect.x, event.pos[1] - sub_surface_pos[1] - self.draw_rect.y)
                self.move_cursor(*pos)

    def get_color(self):
        self.color_change = False
        return self.cursor_color
    
    def change_base_color(self, new_color):
        self.base_color = new_color

        surf_size = self.surface_rect.size

        self.surface = pygame.Surface((256, 256))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, surf_size)

        self.surface_rect = self.surface.get_rect(topleft=(self.x_offset, self.y_offset))
        self.color_change = True
        cursor_pos = (self.cursor[0] + self.x_offset, self.cursor[1] + self.y_offset)
        self.move_cursor(*cursor_pos)



def lighten_color(rgb_color, additive_value):
    return_color = []
    return_color.append(round(((255 - rgb_color[0])/255) * additive_value) + rgb_color[0])
    return_color.append(round(((255 - rgb_color[1])/255) * additive_value) + rgb_color[1])
    return_color.append(round(((255 - rgb_color[2])/255) * additive_value) + rgb_color[2])
    return tuple(return_color)

def darken_color(rgb_color, subtractive_value):
    return_color = []
    return_color.append(round((rgb_color[0]/255) * (255-subtractive_value)))
    return_color.append(round((rgb_color[1]/255) * (255-subtractive_value)))
    return_color.append(round((rgb_color[2]/255) * (255-subtractive_value)))
    return tuple(return_color)


if __name__ == "__main__":
    import random
    pygame.init()
    screen_size = (1800, 800)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    rgb_square = RGB_Square(500, 500, tuple(i//2 for i in screen_size), (255, 0, 0))

    while True:
        screen.fill("#424242")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            rgb_square.handle_event(event, (0, 0))

        rgb_square.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if rgb_square.color_change:
            print(rgb_square.get_color())
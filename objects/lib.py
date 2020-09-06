class draw_text(object): # для рендеринга текста
    def __init__(self, position, size, color=(0, 0, 0), font='default'):
        BLACK = (0, 0, 0)
        self.position = position
        self.color = color
        self.font = pygame.font.Font('fonts/' + font + '.ttf', size)
        #self.font.set_bold(True)
    def draw(self, screen, text):
        screen.blit(self.font.render(str(text), 0, self.color), self.position)
    def size(self, text):
        return self.font.size(str(text))

class Button_main_menu_text(object): # текстовая кнопка
    def __init__(self, position_x, position_y, size_text, color_text, text, function=None):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size_text
        self.color = color_text
        self.text = text
        self.function = function

        self.rect = pygame.Rect((self.position_x, self.position_y), (self.size//2.4 * len(self.text), self.size))
        self.selected = False

        self.sound_selected = False

        self.stop = False

    def event_handler(self, event):
        if not self.stop:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        if self.function != None:
                            self.function()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
            else:
                self.selected = False
                self.sound_selected = False

    def draw(self, screen):
        if not self.selected:

            draw_text((self.position_x, self.position_y), self.size, self.color, 'pixel_2').draw(screen, self.text)
        else:
            if not self.sound_selected:
                #beep_selected_sound.play()
                self.sound_selected = True

            draw_text((self.position_x - (self.size//2.4) * 2, self.position_y), self.size, self.color, 'pixel_2').draw(screen, '> ' + self.text + ' <')

class Text_label(object): # продвинутый рендеринг текста
    def __init__(self, position_x, position_y, size_text, color_text, text, text_stroke=False, text_stroke_color=(0, 0, 0), font="pixel_2"):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size_text
        self.color = color_text
        self.text = text
        self.text_stroke = text_stroke
        self.text_stroke_color = text_stroke_color
        self.font = font
    def draw(self, screen):
        if self.text_stroke:
            draw_text((self.position_x, self.position_y), int(self.size * 1.1), self.text_stroke_color, self.font).draw(screen, self.text)

        draw_text((self.position_x, self.position_y), self.size, self.color, self.font).draw(screen, self.text)

class Label(object): # 4х угольник
    def __init__(self, position_x, position_y, size, color, alpha=255):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        self.alpha = alpha
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.image.set_alpha(int(self.alpha))
        self.rect = self.image.get_rect()
        self.rect.x = self.position_x
        self.rect.y = self.position_y

        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

class Label_breathing(object): # 4х угольник с функцией затухания (по окончанию можно указать выполняемую функцию)
    def __init__(self, position_x, position_y, size, color, alpha_first=255, alpha_last=0, alpha_count=5, delay=0.03, function=None):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color

        self.alpha_first = alpha_first
        self.alpha_last = alpha_last

        self.function = function

        self.alpha_count = alpha_count
        self.alpha = self.alpha_first

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.image.set_alpha(int(self.alpha))
        self.rect = self.image.get_rect()
        self.rect.x = self.position_x
        self.rect.y = self.position_y

        self.delay = delay
        self.time = time.perf_counter() + self.delay

    #@nb.njit()
    def update(self):
        if ((self.alpha_first > self.alpha_last and self.alpha_last >= self.alpha) or (self.alpha_first < self.alpha_last and self.alpha_last <= self.alpha)) and self.function != None:
            self.function()

        if self.time <= time.perf_counter() and self.alpha_last != self.alpha:
            if self.alpha_first > self.alpha_last:
                self.alpha -= self.alpha_count
            else:
                self.alpha += self.alpha_count
            self.image.set_alpha(int(self.alpha))
            self.time = time.perf_counter() + self.delay

    def draw(self, screen):
        screen.blit(self.image, self.rect)

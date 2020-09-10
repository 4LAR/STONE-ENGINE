#
#   STONE ENGINE (lib)
#       version: 1.2
#

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

    def event_handler(self, event):
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

class Image_label(object):
    def __init__(self, x, y, image, size):
        self.size = size
        self.image = image
        self.image = pygame.transform.scale(self.image, self.size)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Button(object):
    def __init__(self, position, size, image, function, arg='', nope=False, type=0, image_selected='', text_bool=False, text='', text_color=(0, 0, 0), text_size = 14):
        BLACK = (0, 0, 0)

        self.text_size = text_size

        self.nope = nope
        self.image = image
        self.image_selected = image_selected
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.image.set_colorkey(BLACK)
        if type == 1:
            self.image_selected = pygame.transform.scale(self.image_selected, size)
            self.image_selected.set_colorkey(BLACK)
        self.rect = pygame.Rect(position, size)
        self.index = 0
        self.function = function
        self.arg = arg
        self.type = type

        self.text_bool = text_bool
        self.text = text
        self.text_color = text_color
        screen.blit(self.image, self.rect)
        self.selected = False
        if self.text_bool:
            #draw_text((self.rect.x + self.image.get_rect().size[0]//20, self.rect.y), self.image.get_rect().size[1], self.text_color).draw(screen, self.text)
            draw_text((self.rect.x + self.image.get_rect().size[0]//50, self.rect.y), self.image.get_rect().size[1], self.text_color).draw(screen, self.text)
    def draw(self, screen):
        if self.selected:
            screen.blit(self.image_selected, self.rect)
        else:
            screen.blit(self.image, self.rect)
        if self.text_bool:
            #draw_text((self.rect.x + self.image.get_rect().size[0]//20, self.rect.y), self.image.get_rect().size[1], self.text_color).draw(screen, self.text)
            draw_text((self.rect.x + self.image.get_rect().size[0]//50, self.rect.y), self.text_size, self.text_color, 'pixel_3').draw(screen, self.text)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    beep_sound.play()
                    #beep_2_sound.play()
                    if len(self.arg) > 0:
                        self.function(self.arg)
                    else:
                        self.function()
        if self.type == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                #screen.blit(self.image_selected, self.rect)
                if not self.selected:
                    beep_2_sound.play()
                    self.selected = True
            else:
                #screen.blit(self.image, self.rect)
                self.selected = False
        else:
            #screen.blit(self.image, self.rect)
            pass

class Flag(object):
    def __init__(self, position, size, image_1 , image_2, state = False, type=0, image_1_sel='', image_2_sel=''):
        BLACK = (0, 0, 0)
        self.image_1 = image_1 #off
        self.image_2 = image_2 #on
        if type == 1:
            self.image_1_sel = image_1_sel #off
            self.image_2_sel = image_2_sel #on
            self.image_1_sel = pygame.transform.scale(self.image_1_sel, size)
            self.image_1_sel.set_colorkey(BLACK)
            self.image_2_sel = pygame.transform.scale(self.image_2_sel, size)
            self.image_2_sel.set_colorkey(BLACK)

        self.image_1 = pygame.transform.scale(self.image_1, size)
        self.image_1.set_colorkey(BLACK)
        self.image_2 = pygame.transform.scale(self.image_2, size)
        self.image_2.set_colorkey(BLACK)

        self.type = type


        self.rect = pygame.Rect(position, size)
        self.state = state

        self.selected = False
    def draw(self, screen):
        if self.state:
            if self.selected and self.type == 1:
                screen.blit(self.image_2_sel, self.rect)
            else:
                screen.blit(self.image_2, self.rect)
        else:
            if self.selected and self.type == 1:
                screen.blit(self.image_1_sel, self.rect)
            else:
                screen.blit(self.image_1, self.rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    beep_sound.play()
                    if self.state:
                        self.state = False
                        #screen.blit(self.image_1, self.rect)
                    else:
                        self.state = True
                        #screen.blit(self.image_2, self.rect)
        if self.type == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if not self.selected:
                    beep_2_sound.play()
                    self.selected = True
            else:
                self.selected = False

class Simple_list(object):
    def __init__(self, x, y, size_list, text_array, text_size, color_text, font, background=False, backgraund_alpha=100):
        self.x = x
        self.y = y
        self.size_list = size_list
        self.text_array = text_array
        self.text_size = text_size
        self.color_text = color_text
        self.font = font
        self.backgraund = backgraund
        self.backgraund_alpha = backgraund_alpha
        if self.backgraund:
            self.image = pygame.Surface(self.size_list)
            self.image.set_alpha(self.backgraund_alpha)

        self.scrol = 0

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and self.scrol != 0:
                self.scrol -= 1
            if event.button == 5:
                self.scrol += 1

    def draw(self, screen):
        if self.backgraund:
            screen.blit(self.image, (self.x, self.y, 0, 0))
        for i in range(len(self.text_array)):
            try:
                Text_label(self.x, self.y + (self.text_size//2) * i, self.text_size, self.color_text, self.text_array[i + self.scrol], False, font=self.font).draw(screen)
            except:
                break

# функции
image_type = "RGBA"

def pgtopil(image_pygame):
    pil_string_image = pygame.image.tostring(image_pygame, image_type, False)
    im = Image.frombytes(image_type, image_pygame.get_size(), pil_string_image)
    return im

def piltopg(image_pil):
    mode = image_pil.mode
    size = image_pil.size
    data = image_pil.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    return py_image

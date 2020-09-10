#
#    STONE ENGINE
#       by 100LAR
#

version_engine = '1.3'

import time
import os
import sys
import traceback    # вывод ошибок

# функции
def exit():
    sys.exit(0)

def get_time():
    return time.strftime("%H:%M:%S|%d-%m-%y", time.localtime())

def log(text, time_log_bool=True, print_console=False):
    log_file = open('log.txt', 'a')
    log_file.write((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text) + '\n')
    log_file.close()
    if print_console:
        print((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text) + '\n')
    #console.add_console('[ CRITICAL ] ' + (('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text))

def log_screen(text, time_log_bool=True):
    print((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text))
    console.add_console((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text))

try:
    import configparser     # настройки
    from os import path

    # расположение нужных каталогов
    img_dir     = path.join(path.dirname(__file__), 'img')
    sound_dir   = path.join(path.dirname(__file__), 'sound')
    font_dir    = path.join(path.dirname(__file__), 'fonts')

    class settings():
        def __init__(self):
            # переменные настроек
            self.width = 1280
            self.height = 720
            self.full_screen = False
            self.gamma = 1.0

            self.fps = 30

            self.show_fps = False

            self.console = False

            self.sound_volume = 0.3

            self.sdl2 = False

            self.read_settings() # читаем настроки

        def read_settings(self):
            if not os.path.exists("settings.txt"): # проверка файла с настройками
                config = configparser.ConfigParser()
                config.add_section("Screen")
                config.set("Screen", "width", str(self.width))
                config.set("Screen", "height", str(self.height))
                config.set("Screen", "full-screen", str(self.full_screen))
                config.set("Screen", "gamma", str(self.gamma))
                config.add_section("User_interface")
                config.set("User_interface", "show-fps", str(self.show_fps))
                config.set("User_interface", "console", str(self.console))
                config.add_section("Sound")
                config.set("Sound", "volume", str(self.sound_volume))
                config.add_section("System")
                config.set("System", "sdl2", str(self.sdl2))
                with open("settings.txt", "w") as config_file: # запись файла с настройками
                    config.write(config_file)
                self.read_settings()
            else:
                config = configparser.ConfigParser()
                config.read("settings.txt")
                self.width = int(config.get("Screen", "width"))
                self.height = int(config.get("Screen", "height"))
                self.full_screen = True if (config.get("Screen", "full-screen")).lower() == 'true' else False
                self.gamma = float(config.get("Screen", "gamma"))

                self.show_fps = True if (config.get("User_interface", "show-fps")).lower() == 'true' else False

                self.console = True if (config.get("User_interface", "console")).lower() == 'true' else False

                self.sound_volume = float(config.get("Sound", "volume"))

                self.sdl2 = True if (config.get("System", "sdl2")).lower() == 'true' else False

    class draw_FPS(object):
        def __init__(self, position, size):
            BLACK = (0, 0, 0)
            self.position = position
            self.font = pygame.font.Font('fonts/default.ttf', size)
        def draw(self, screen, fps):
            screen.blit(self.font.render(str(fps), 0, (0, 180, 0)), self.position)

    settings = settings() # инициализация класса с настройками

    # импортирование библиотек для игры
    if settings.sdl2:
        # попытка запуска sdl2
        try:
            import pygame_sdl2 # для портов для android
            pygame_sdl2.import_as_pygame()
        except ImportError:
            log_screen('ERROR IMPORT SDL2')

    import pygame           # прорисовка
    import random           # ну это рандом

    # настройка звука
    sound_volume = settings.sound_volume

    try:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        print('OK IMPORT MIXER')
    except:
        print('ERROR IMPORT MIXER')

    # cоздание игрового окна
    pygame.init()
    if settings.full_screen:
        screen = pygame.display.set_mode((settings.width, settings.height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((settings.width, settings.height), pygame.DOUBLEBUF)

    pygame.display.set_caption('STONE ENGINE (ver: ' + version_engine + ')')
    try:
        gameIcon = pygame.image.load(path.join(img_dir, "icon.png"))
        pygame.display.set_icon(gameIcon)
    except:
        pass
    pygame.display.set_gamma(settings.gamma)

    clock = pygame.time.Clock()

    objects_other = []      # разные объекты не причастные к прорисовке или считыванию нажатий
    objects_display = []    # объекты для отрисовки

    ###

    class Console(object):
        def __init__(self):

            self.text_arr = []

            self.input_ = ' >> '
            self.input = ''

            self.image_terminal_background = pygame.Surface((settings.width, settings.height//2))
            self.image_terminal_background.fill((0, 0, 0))
            self.image_terminal_background.set_alpha(200)
            self.image_terminal_background_rect = self.image_terminal_background.get_rect()
            self.image_terminal_background_rect.x = 0
            self.image_terminal_background_rect.y = 0

            self.size = settings.width//100
            self.font = pygame.font.Font('fonts/default.ttf', self.size)

            self.show = False

            self.char = ' 1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_.'

        def add_console(self, text):
            self.text_arr.append(text)
            if len(self.text_arr) > (settings.height//2) // self.size - 3:
                self.text_arr.pop(0)

        def event_handler(self, event):
            if event.type == pygame.KEYDOWN:
                char = str(chr(event.key))
                #if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                #    char = char.upper()
                if char == '-':
                    char = '_'
                if char in self.char:
                    self.input += char
                if event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:len(self.input)-1]
                if event.key == pygame.K_RETURN:
                    self.add_console(self.input_  + self.input)
                    if self.input == 'clear':
                        self.text_arr.clear()
                    elif self.input == 'exit':
                        exit()
                    elif self.input.split(' ')[0] == 'function':
                        try:
                            exec(self.input.split(' ')[1] + '()')
                            self.show = False
                        except:
                            self.add_console(' ERROR FUNCTION')

                    elif self.input.split(' ')[0] == 'edit':
                        try:
                            exec(self.input.split(' ')[1] + ' = ' + self.input.split(' ')[2])
                            self.add_console(self.input.split(' ')[1] + ' = ' + self.input.split(' ')[2])
                        except:
                            self.add_console(' ERROR EDIT')

                    elif self.input.split(' ')[0] == 'print':
                        try:
                            exec('console.add_console(str(' + self.input.split(' ')[1] + '))')
                        except:
                            self.add_console(' ERROR PRINT')

                    elif self.input == 'fps':
                        if settings.show_fps:
                            settings.show_fps = False
                            self.add_console('FPS OFF')
                        else:
                            settings.show_fps = True
                            self.add_console('FPS ON')

                    self.input = ''

        def draw(self, screen):
            if self.show:
                screen.blit(self.image_terminal_background, self.image_terminal_background_rect)
                for i in range((settings.height//2) // self.size - 2):
                    try:
                        screen.blit(self.font.render(self.text_arr[i] , 0, (180, 180, 180)), (settings.width//80, settings.height//80 +  self.size * i))
                    except:
                        break
                screen.blit(self.font.render(self.input_  + self.input, 0, (180, 180, 180)), (settings.width//80, settings.height//80 +  self.size * i))

    ###

    def del_obj_other(obj_name): # функция для удаления объекта по его названию
        obj_delete_bool = False
        for i in range(len(objects_display)): # проверяем каждый объект
            if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name: # если попадается нужный объект
                objects_other.pop(i)
                obj_delete_bool = True
                log_screen('OTHER OBJECT DELETED: ' + obj_name)
                return True
        if not obj_delete_bool: # на случай отсутсвия нужного объекта
            log_screen('OTHER OBJECT NOT DELETED: ' + obj_name)
            return False
    def add_objects_other(obj): # функция для добавления объектов
        objects_other.append(obj)
        log_screen('OTHER ADD: ' + str(obj))
    def clear_objects_other(): # функция для очищения объектов
        objects_other.clear()
        log_screen('OTHER CLEAR')
    ###
    def clear_display(): # функция для очищения объектов
        objects_display.clear()
        log_screen('DISPLAY CLEAR')

    def del_obj_display(obj_name): # функция для удаления объекта по его названию
        obj_delete_bool = False
        for i in range(len(objects_display)): # проверяем каждый объект
            if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name: # если попадается нужный объект
                objects_display.pop(i)
                obj_delete_bool = True
                log_screen('DISPLAY OBJECT DELETED: ' + obj_name)
                return True
        if not obj_delete_bool: # на случай отсутсвия нужного объекта
            log_screen('DISPLAY OBJECT NOT DELETED: ' + obj_name)
            return False
    def add_display(obj): # функция для добавления объектов
        objects_display.append(obj)
        log_screen('DISPLAY ADD: ' + str(obj))

    console = Console()
    ###
    code = ''
    files = []

    # получаем названия файлов с нужными объктами
    file_objects = (open('objects/objects.list', 'r', encoding="utf-8").read()).split('\n')
    #print(file_objects)
    for i in range(len(file_objects)-1):
        files.append([file_objects[i], 0])
        print('IMPORT: ' + file_objects[i])

    #классы
    for i in range(len(files)):
        file_objects = open('objects/' + files[i][0], 'r', encoding="utf-8")
        code += file_objects.read()
        files[i][1] = len(code.split('\n'))
        file_objects.close()

    exec(code)
    #del_obj_display('Main_logo')

    draw_fps = draw_FPS((0, 0), 30)

    while True: # главный цикл
        clock.tick(settings.fps)

        frameTime = float(clock.get_time()) / 1000.0 # frameTime is the time this frame has taken, in seconds
        t = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if settings.console and event.key == pygame.K_F1:
                    if console.show:
                        console.show = False
                    else:
                        console.show = True

            if not console.show:
                for o in objects_display: # проходим по каждому объекту в цикле
                    try: # проверяем есть ли у объекта такая функция
                        o.event_handler(event)
                    except Exception as e:
                        if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute 'event_handler'":
                            print(e)
            else:
                console.event_handler(event)

        for o in objects_display: # проходим по каждому объекту в цикле
            if not console.show:
                try: # проверяем есть ли у объекта такая функция
                    o.update()
                except Exception as e:
                    if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute 'update'":
                        print(e)
            try: # проверяем есть ли у объекта такая функция
                o.draw(screen)
            except Exception as e:
                if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute 'draw'":
                    print(e)
            if console.show:
                console.draw(screen)

        for o in objects_other:
            try:
                o.update()
            except Exception as e:
                if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute 'update'":
                    print(e)

        if settings.show_fps:
            draw_fps.draw(screen, int(clock.get_fps()))

        pygame.display.update() # обновлем экран
        pygame.display.flip() # После отрисовки всего, переворачиваем экран
except Exception as e:
    pygame.display.quit() # закрытие окна
    # информирование о ошибке
    log('FATAL ERROR: ' + str(e))
    print('FATAL ERROR: ' + str(e))
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        if lineno != 283:
            if lineno - 1 > 0:
                print(' ' + str(lineno - 1) + ' | ' + str(code.split('\n')[lineno - 2]))
            print('>' + str(lineno) + ' | ' + str(code.split('\n')[lineno - 1]))
            if len(code.split('\n')) - 1 >= lineno:
                print(' ' + str(lineno + 1) + ' | ' + str(code.split('\n')[lineno]))
    input('Press enter...')

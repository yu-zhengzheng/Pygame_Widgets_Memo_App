import pygame
import unicodedata
import pygame_widgets.button
import pygame_widgets.textbox
import pygame_widgets.widget
import datetime
import os
import tracemalloc

tracemalloc.start()


class memo_UI:
    list_label = []
    list_time = []
    count = 0

    def memo_init(self):
        pygame.init()

    def save_data(self):
        file = open("new data.txt", "w+", encoding="utf-8")
        for i in range(self.count):
            file.write(self.list_label[i])
            file.write("#$%")
            file.write(self.list_time[i])
            file.write("\n")

        # Close opend file
        file.close()
        if not file.closed:
            print("Warning!!! File not closed!!!")
        print("date saved!")

    def read_data(self):
        file = open("data.txt", "r", encoding="utf-8")
        self.count = 0
        for line in file:
            label, time_str = line.split("\n")[0].split("#$%")
            self.list_label.append(label)
            self.list_time.append(time_str)
            self.count += 1
        self.sort()

    def sort(self):
        time_obj = []
        for i in range(self.count):
            time_obj.append(datetime.datetime.strptime(self.list_time[i], '%Y-%m-%d %H:%M:%S'))
        for i in range(self.count):
            swapped = False
            for j in range(self.count - i - 1):
                if (time_obj[j + 1] - time_obj[j]).days < 0:
                    time_obj[j], time_obj[j + 1] = time_obj[j + 1], time_obj[j]
                    self.list_time[j], self.list_time[j + 1] = self.list_time[j + 1], self.list_time[j]
                    self.list_label[j], self.list_label[j + 1] = self.list_label[j + 1], self.list_label[j]
                    # Set the flag to True
                    swapped = True
            # If no swap occurred, the list is sorted
            if not swapped:
                break

    def display_text(self, display_surface, text, x, y, font_size, color=(255, 255, 255)):
        for char in text:
            name = unicodedata.name(char)
            if name.startswith("CJK UNIFIED IDEOGRAPH"):
                textbox = pygame.font.SysFont('FangSong', size=font_size, bold=False).render(char, True, color)
            else:
                textbox = pygame.font.SysFont('courier new', size=font_size, bold=False).render(char, True, color)
            rect = textbox.get_rect()
            rect.center = (x + rect.width / 2, y + rect.height / 2)
            x += rect.width
            display_surface.blit(textbox, rect)

    def add_weekday(self, ymdhms):
        return datetime.datetime.strftime(datetime.datetime.strptime(ymdhms, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %a %H:%M:%S')

    def timedelta_format(self, td):
        hours, remainder = divmod(td.seconds, 3600)  # get the hours and the remaining seconds
        minutes, seconds = divmod(remainder, 60)
        return "{:d} days, {:02d}:{:02d}:{:02d}.{:03d}".format(td.days, hours, minutes, seconds, int(td.microseconds / 1000))

    def append(self, new_label, new_time):
        self.list_label.append(new_label)
        self.list_time.append(new_time)
        self.count += 1
        self.sort()

    def remove(self, i, list_label, list_time):
        print(list_label[i], list_time[i], "deleted!")
        list_label.pop(i)
        list_time.pop(i)
        self.count -= 1

    def __init__(self):
        # initialize memo
        self.memo_init()
        width = 1600
        height = 1000
        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # def colors
        c_white = (255, 255, 255)
        c_black = (0, 0, 0)
        c_red = (255, 0, 0)
        c_blue = (0, 0, 255)
        c_green = (0, 255, 0)
        c_gray = (191, 191, 191)
        c_dark_gray=(31,31,31)

        window.fill(c_black)

        # Read data
        self.read_data()

        # Creates the button with optional parameters
        save_button = pygame_widgets.button.Button(window, 400, 110, 100, 40, text='Save', fontSize=50, margin=20, inactiveColour=c_gray, hoverColour=c_blue, pressedColour=c_green, radius=5,
                                                   onClick=lambda: self.save_data(), font=pygame.font.SysFont('courier new', size=32))

        label_box = pygame_widgets.textbox.TextBox(window, 20, height-60, 600, 40, fontSize=20, colour=c_dark_gray, borderColour=c_white, textColour=c_white, radius=10, borderThickness=1, placeholderText="",
                                                   font=pygame.font.SysFont('courier new', size=32))
        time_box = pygame_widgets.textbox.TextBox(window, 640, height-60, 600, 40, fontSize=20, colour=c_dark_gray, borderColour=c_white, textColour=c_white, radius=10, borderThickness=1,
                                                  placeholderText='YYYY-MM-DD HH:MM:SS', font=pygame.font.SysFont('courier new', size=32))

        add_button = pygame_widgets.button.Button(window, 1260, height-60, 100, 40, text='Add', fontSize=50, margin=20, inactiveColour=c_gray, hoverColour=c_blue, pressedColour=c_green, radius=5,
                                                  onClick=lambda: self.append(label_box.getText(), time_box.getText()), font=pygame.font.SysFont('courier new', size=32))

        pygame.display.update()

        running = True
        while running:
            time_now = datetime.datetime.now()
            pygame.display.set_caption("Memo " + time_now.strftime('%Y-%m-%d %a %H:%M:%S'))
            window.fill(c_black)
            self.display_text(window, "Memo", 20, 0, 72)
            del_button = [None] * self.count

            self.display_text(window, str(self.count) + " pending", 20, 100, 48)
            for i in range(self.count):
                self.display_text(window, self.list_label[i], 20, 200 + i * 40, 24)
                self.display_text(window, self.add_weekday(self.list_time[i]), (width-180)*1.1/3, 200 + i * 40, 24)
                countdown = datetime.datetime.strptime(self.list_time[i], '%Y-%m-%d %H:%M:%S')
                if (countdown - time_now).days < 0:
                    self.display_text(window, "+" + self.timedelta_format(time_now - countdown), (width-180)*2/3, 200 + i * 40, 24, c_gray)
                else:
                    self.display_text(window, self.timedelta_format(countdown - time_now), (width-180)*2/3, 200 + i * 40, 24)
                del_button[i] = pygame_widgets.button.Button(window, width-140, 198 + i * 40, 120, 30, text='Delete', fontSize=50, margin=20, inactiveColour=c_gray, hoverColour=c_blue,
                                                             pressedColour=c_green, radius=5, onClick=self.remove, onClickParams=(i, self.list_label, self.list_time),
                                                             font=pygame.font.SysFont('courier new', size=24))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    width,height=window.get_size()

            pygame_widgets.update(events)
            pygame.display.update()
            all_widgets = pygame_widgets.widget.WidgetHandler.getWidgets()
            del all_widgets[4:]  # depend on UI elements
            # clock.tick(120)
            # print(tracemalloc.get_traced_memory())

        self.save_data()
        os.remove("backup.txt")
        os.rename("data.txt", "backup.txt")
        os.rename("new data.txt", "data.txt")

        # print(tracemalloc.get_traced_memory())
        tracemalloc.stop()


m1 = memo_UI()

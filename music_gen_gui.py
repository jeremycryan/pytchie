#!/usr/bin/env python

import pygame

from music_generation import *
from sound_generation import *
from constants import *
from helpers import *
import random as rd

import time
import sys





class MusGUI(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 1, 4096)
        pygame.init()
        pygame.font.init()
        self.screen_commit = pygame.display.set_mode(WINDOW_SIZE)
        self.screen = pygame.Surface(FRAME_SIZE)
        pygame.display.set_caption("Pytchie - Random Music Synthesis")
        self.print_font = pygame.font.Font(fp("Myriad.otf"), int(16*SCALE_X))
        self.most_recent_print = ""
        self.print_text = self.most_recent_print
        self.most_recent_print_time = ""

        self.title_font = pygame.font.Font(fp("Myriad.otf"), int(22*SCALE_X))
        texts = ["LEAD", "BASS", "COMP", "PERC", "MIX"]
        self.titles = [self.title_font.render(text, 1, (200, 200, 200)) for text in texts]
        link_font = pygame.font.Font(fp("Myriad.otf"), int(16*SCALE_X))
        self.link = link_font.render("github.com/jeremycryan/pytchie", 1, (120, 120, 120))

        self.main()

    def gui_print(self):
        text = "%s: %s" % (str(self.most_recent_print_time), self.print_text.upper())
        a = self.print_font.render(text, 1, (180, 180, 180))
        self.screen.blit(a, (int(20*SCALE_X), int(FRAME_HEIGHT*0.95)))

    def gui_print_text(self, text):
        self.print_text = text
        self.most_recent_print_time = int(time.time()%1000*100)/100.0

    def draw_titles(self):
        self.screen.blit(self.titles[0], (int(0.08 * FRAME_WIDTH), int((LEAD_Y) * FRAME_HEIGHT)))
        self.screen.blit(self.titles[4], (int(0.08 * FRAME_WIDTH), int(MIX_Y * FRAME_HEIGHT)))
        self.screen.blit(self.titles[1], (int(0.08 * FRAME_WIDTH), int(BASS_Y * FRAME_HEIGHT)))
        self.screen.blit(self.titles[3], (int(0.08 * FRAME_WIDTH), int(SNARE_Y * FRAME_HEIGHT)))
        self.screen.blit(self.titles[2], (int(0.08 * FRAME_WIDTH), int(COMP_Y * FRAME_HEIGHT)))
        self.screen.blit(self.link,
            (int(0.63 * FRAME_WIDTH),
            int(0.85*FRAME_HEIGHT)))

    def main(self):

        then = time.time()
        self.click = False
        lead_text = 0

        generate = Button(pos=(0.83, 0.925), text="GENERATE")
        randomize = Button(pos=(0.66, MIX_Y + MIX_SPACING_Y/2), text="RANDOMIZE")

        tempo = Gauge(pos=(0.2, MIX_Y), label="TEMPO", min_val = 60, max_val = 180, starting_val = 120, size = (0.383, 0.05))
        chord_1 = ModeButton(size = (0.11, 0.05), pos=(0.2 + 0*MIX_SPACING_X, MIX_Y + MIX_SPACING_Y),
            texts = ["I", "ii", "iii", "IV", "V", "vi", "vii", "RAND"], start_mode = 5)
        chord_2 = ModeButton(size = (0.11, 0.05), pos=(0.2 + 1*MIX_SPACING_X, MIX_Y + MIX_SPACING_Y),
            texts = ["I", "ii", "iii", "IV", "V", "vi", "vii", "RAND"], start_mode = 3)
        chord_3 = ModeButton(size = (0.11, 0.05), pos=(0.2 + 2*MIX_SPACING_X, MIX_Y + MIX_SPACING_Y),
            texts = ["I", "ii", "iii", "IV", "V", "vi", "vii", "RAND"], start_mode = 0)
        chord_4 = ModeButton(size = (0.11, 0.05), pos=(0.2 + 3*MIX_SPACING_X, MIX_Y + MIX_SPACING_Y),
            texts = ["I", "ii", "iii", "IV", "V", "vi", "vii", "RAND"], start_mode = 4)

        lead_instrument_button = ModeButton(pos=(0.2, LEAD_Y+LEAD_SPACING), texts = ["RANDOM", "FLUTE", "TRUMPET", "VIOLIN", "SNARE"])
        lead_enable = ToggleButton(pos = (0.2, LEAD_Y))
        lead_intricacy = Gauge(pos=(0.38, LEAD_Y), size=(0.5, 0.05), bar_color = BLUE, label = "INTRICACY", starting_val=0.7)
        lead_temerity = Gauge(pos = (0.38, LEAD_Y+LEAD_SPACING), size=(0.5, 0.05), bar_color = BLUE, label = "TEMERITY", starting_val=0.7)

        bass_enable = ToggleButton(pos = (0.2, BASS_Y))
        bass_instrument_button = ModeButton(pos=(0.2, BASS_Y+LEAD_SPACING), texts = ["RANDOM", "SAWTOOTH", "SQUARE"])
        bass_intricacy = Gauge(pos=(0.38, BASS_Y), size=(0.5, 0.05), bar_color = BLUE, label = "INTRICACY", starting_val=0.3)
        bass_temerity = Gauge(pos = (0.38, BASS_Y+BASS_SPACING), size=(0.5, 0.05), bar_color = BLUE, label = "TEMERITY", starting_val=0.3)

        snare_enable = ToggleButton(pos = (0.2, SNARE_Y))
        snare_intricacy = Gauge(pos=(0.38, SNARE_Y), size=(0.5, 0.05), bar_color = BLUE, label = "INTRICACY", starting_val=0.5)

        comp_enable = ToggleButton(pos = (0.2, COMP_Y))
        comp_instrument_button = ModeButton(pos=(0.38, COMP_Y), texts = ["RANDOM", "FLUTE", "TRUMPET", "VIOLIN"])


        self.buttons = [generate, randomize, lead_enable, lead_instrument_button,
            bass_instrument_button, bass_enable, chord_1, chord_2, chord_3, chord_4,
            snare_enable, comp_enable, comp_instrument_button]
        self.gauges = [lead_intricacy, lead_temerity, tempo, bass_intricacy, bass_temerity,
            snare_intricacy]
        self.clicked = []
        self.bleeps = []

        while True:

            now = time.time()
            dt = now - then
            then = now

            chords = [chord.texts[chord.mode] for chord in [chord_1, chord_2, chord_3, chord_4]]

            to_generate = False
            if generate in self.clicked:
                a = Song(4, tempo.value,
                    lead_intricacy=lead_intricacy.value,
                    lead_temerity=lead_temerity.value,
                    bass_intricacy=bass_intricacy.value,
                    bass_temerity=bass_temerity.value,
                    chords=chords,
                    snare_intricacy=snare_intricacy.value)
                self.gui_print_text("Generating a sample song with your parameters...")
                to_generate = 1

            if randomize in self.clicked:
                self.gui_print_text("Random values assigned to all fields.")
                for item in self.buttons + self.gauges:
                    item.randomize_value()

            self.check_events()
            self.screen.fill((50, 50, 50))
            bot_bar = pygame.Surface((FRAME_WIDTH, int(FRAME_HEIGHT*0.10)))
            self.screen.blit(bot_bar, (0, FRAME_HEIGHT - bot_bar.get_height()))
            bot_bar.fill((0, 0, 0))


            self.gui_print()


            for item in self.buttons + self.gauges + self.bleeps:
                if dt > 0.05:
                    dt = 0.05
                item.update(dt)
                item.draw(self.screen)

                if item in self.bleeps:
                    if item.radius > item.max_radius:
                        self.bleeps.remove(item)

            self.draw_titles()

            if to_generate:
                black = pygame.Surface((FRAME_WIDTH, int(FRAME_HEIGHT*0.9)))
                black.fill((0, 0, 0))
                black.set_alpha(100)
                self.screen.blit(black, (0, 0))
                self.bleeps = []

            screen = pygame.transform.scale(self.screen, WINDOW_SIZE)
            self.screen_commit.blit(screen, (0, 0))

            pygame.display.flip()

            if to_generate:
                lead_instrument = a.label_to_instrument[lead_instrument_button.texts[lead_instrument_button.mode]]
                comp_instrument = a.label_to_instrument[comp_instrument_button.texts[comp_instrument_button.mode]]
                enables = [lead_enable.toggled, snare_enable.toggled, bass_enable.toggled, comp_enable.toggled]
                # t = threading.Thread(name="generate_audio", target=a.generate_preset_0,
                #     kwargs={"lead_instrument": lead_instrument,
                #     "comp_instrument": comp_instrument,
                #     "enables": enables})
                #TODO make this non-blocking, but also not take 40 seconds
                a.generate_preset_0(lead_instrument = lead_instrument, comp_instrument = comp_instrument, enables = enables)
                self.gui_print_text("test.wav generated and ready for playback.")


    def check_events(self):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        click = False
        old_click = self.click
        new_click = pygame.mouse.get_pressed()[0]

        self.clicked = []
        if new_click and not old_click:
            click=True
            self.bleeps.append(Bleep(mouse_pos))
        self.click = new_click

        for button in self.buttons+self.gauges:
            this_button_clicked = button.mouse_over(mouse_pos, click=click, held=new_click)
            if this_button_clicked:
                self.clicked.append(button)


class Bleep(object):

    def __init__(self, pos):

        self.x = int(pos[0]*SCALE_X)
        self.y = int(pos[1]*SCALE_Y)
        self.pos = [self.x, self.y]

        self.radius = 1
        self.max_radius = 20

    def update(self, dt):
        self.radius += dt * 150.0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.pos, int(self.radius*SCALE_X), 2)


class Button(object):

    def __init__(self, text = "BUTTON", size = (0.2, 0.05), pos = (0.1, 0.1)):
        self.width = size[0]
        self.height = size[1]
        self.pos = pos

        self.x = int(self.pos[0] * FRAME_WIDTH)
        self.y = int(self.pos[1] * FRAME_HEIGHT)
        self.w = int(self.width * FRAME_HEIGHT)
        self.h = int(self.height * FRAME_HEIGHT)

        self.text = text
        self.button_font = pygame.font.Font(fp("Myriad.otf"), int(16*SCALE_X))
        self.button_font_render = self.button_font.render(self.text, 1, (0, 0, 0))
        self.brr_w = self.button_font_render.get_width()
        self.brr_h = self.button_font_render.get_height()

        self.hovered = 0
        self.hover_scale = 1.05
        self.cur_scale = 1.0
        self.target_scale = 1.0

        self.h_color = (255, 255, 255)
        self.color = (200, 200, 200)

        self.toggled = 0


    def randomize_value(self):
        pass

    def mouse_over(self, mpos, click=False, held=False):

        clicked = 0
        x, y  = mpos

        if x >= self.x/SCALE_X and x <= self.x/SCALE_X + self.w/SCALE_X:
            if y >= self.y/SCALE_Y and y <= self.y/SCALE_Y + self.h/SCALE_Y:
                if click:
                    self.toggled = 1-self.toggled
                    self.cur_scale = 1.3
                    clicked = 1
                self.hovered = True
                return clicked

        self.hovered = False
        return clicked


    def draw(self, screen):

        if self.hovered:
            color = self.h_color
        else:
            color = self.color


        self.brr_w = self.button_font_render.get_width()
        self.brr_h = self.button_font_render.get_height()


        width = int(self.w * self.cur_scale)
        height = int(self.h * self.cur_scale)
        xdif = int((width - self.w)/2)
        ydif = int((height - self.h)/2)
        self.target_scale = self.hover_scale
        if not self.hovered:
            self.target_scale = 1.0

        button_surf = pygame.Surface((self.w, self.h))
        button_surf.fill(color)

        font_center_pos = (int(self.x + self.w/2), int(self.y + self.h/2))
        font_pos = (int(font_center_pos[0] - self.brr_w/2),
            int(font_center_pos[1] - self.brr_h/2))
        button_surf.blit(self.button_font_render, (self.w/2 - self.brr_w/2, self.h/2 - self.brr_h/2))

        shadow = pygame.Surface((self.w, self.h/2))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(40)
        button_surf.blit(shadow, (0, self.h/2))

        xoff = 0
        yoff = 0
        button_surf = pygame.transform.scale(button_surf, (int(self.w*self.cur_scale), int(self.h*self.cur_scale)))

        screen.blit(button_surf, (self.x - xdif, self.y - ydif))

    def update(self, dt):

        ds = -self.cur_scale + self.target_scale
        self.cur_scale += ds*dt*20

class ToggleButton(Button):

    def __init__(self, text = "DISABLED", size = (0.2, 0.05), pos = (0.1, 0.1), toggle_text = "ENABLED"):
        Button.__init__(self, text=text, size=size, pos=pos)
        self.toggled = True
        self.untoggled_color = (100, 100, 100)
        self.untoggled_color_2 = (120, 120, 120)
        self.toggled_color = GREEN
        self.toggled_color_2 = [c+20 for c in GREEN]
        self.untoggle_text = text
        self.toggle_text = toggle_text
        self.button_font_render_untoggled = self.button_font_render.copy()
        self.button_font_render_toggled = self.button_font.render(self.toggle_text, 1, (0, 0, 0))

    def randomize_value(self):
        self.cur_scale = 1.3
        self.toggled = 0
        if rd.random() < 0.75:
            self.toggled = 1

    def update(self, dt):

        ds = -self.cur_scale + self.target_scale
        self.cur_scale += ds*dt*20

        if not self.toggled:
            self.text = self.untoggle_text
            self.button_font_render = self.button_font_render_untoggled
            self.color = self.untoggled_color
            self.h_color = self.untoggled_color_2
        else:
            self.text = self.toggle_text
            self.button_font_render = self.button_font_render_toggled
            self.color = self.toggled_color
            self.h_color = self.toggled_color_2

class ModeButton(Button):

    def __init__(self, texts = ["MODE 1", "MODE 2", "MODE 3"], size = (0.2, 0.05), pos = (0.1, 0.1), start_mode = 0):
        Button.__init__(self, text=texts[0], size=size, pos=pos)

        self.colors = {}
        self.modes = [i for i in range(len(texts))]
        self.colors = [COLORS[i%len(COLORS)] for i in self.modes]
        self.hover_colors = [(min(c[0]+20, 255), min(c[1]+20, 255), min(c[2]+20, 255)) for c in self.colors]

        self.mode = self.modes[start_mode]
        self.color = self.colors[self.mode]
        self.h_color = self.hover_colors[self.mode]

        self.texts = texts
        self.font_renders = [self.button_font.render(texts[mode], 1, (0, 0, 0)) for mode in self.modes]
        self.button_font_render = self.font_renders[start_mode]
        #self.button_font_render = self.button_font.render(self.text, 1, (0, 0, 0))

    def set_mode(self, mode):
        self.cur_scale = 1.3
        self.mode = mode
        self.color = self.colors[self.mode]
        self.h_color = self.hover_colors[self.mode]
        self.button_font_render = self.font_renders[self.mode]

    def randomize_value(self):
        self.set_mode(rd.choice(self.modes))

    def mouse_over(self, mpos, click=False, held=False):

        clicked = 0
        x, y  = mpos

        if x >= self.x/SCALE_X and x <= self.x/SCALE_X + self.w/SCALE_X:
            if y >= self.y/SCALE_Y and y <= self.y/SCALE_Y + self.h/SCALE_Y:
                if click:
                    self.toggled = 1-self.toggled
                    self.cur_scale = 1.3
                    self.set_mode((self.mode + 1) % len(self.modes))

                self.hovered = True
                return clicked

        self.hovered = False
        return clicked

class Gauge(object):

    def __init__(self, size = (0.4, 0.05), pos = (0.1, 0.1), max_val=1.0, min_val=0, starting_val=0.5, bar_color=RED, label = "GAUGE"):
        self.w = size[0]*FRAME_WIDTH
        self.h = size[1]*FRAME_HEIGHT
        self.x = pos[0]*FRAME_WIDTH
        self.y = pos[1]*FRAME_HEIGHT
        self.background_color = (90, 90, 90)
        self.meter_color = bar_color
        self.meter_highlight = [min(c+25, 255) for c in bar_color]
        self.meter_text_color = (0, 0, 0)#[min(c+50, 255) for c in self.meter_highlight]
        self.value = starting_val
        self.max_val = max_val
        self.min_val = min_val
        self.dragging = 0
        self.scale = 1.0
        self.target_scale = 1.0
        self.h_scale = 1.03
        label_font=  pygame.font.Font(fp("Myriad.otf"), int(16*SCALE_X))
        self.label = label_font.render(label, 1, self.meter_text_color)

    def randomize_value(self):
        self.scale = 1.12
        per = rd.random()
        self.value = per*(self.max_val - self.min_val) + self.min_val

    def draw(self, screen):
        meter_color = self.meter_color
        if self.hovered or self.dragging:
            meter_color = self.meter_highlight

        back = pygame.Surface((int(self.w*self.scale), int(self.h*self.scale)))
        back.fill(self.background_color)
        per_val = 1.0*(self.value - self.min_val)/(self.max_val - self.min_val)
        meter = pygame.Surface((int(self.w * self.scale * per_val), int(self.h * self.scale)))
        meter.fill(meter_color)

        w = int(self.w*self.scale)
        h = int(self.h*self.scale)
        xdif = int(w - self.w)/2
        ydif = int(h - self.h)/2
        shadow = pygame.Surface((w, h))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(40)

        back.blit(meter, (0, 0))
        back.blit(self.label, (int(10*SCALE_X), h/2 - self.label.get_height()/2))
        back = pygame.transform.scale(back, (w, h))
        back.blit(shadow, (0, h/2))

        screen.blit(back, (self.x - xdif, self.y - ydif))

    def update(self, dt):

        if self.hovered or self.dragging:
            self.target_scale = self.h_scale
        else:
            self.target_scale = 1.0

        ds = -self.scale + self.target_scale
        self.scale += ds*dt*20

    def mouse_over(self, mpos, click=False, held=False):

        x, y  = mpos

        if self.dragging and not held:
            self.dragging = False
            self.scale = 1.08

        if self.dragging:
            bar_min = self.x/SCALE_X
            bar_max = self.x/SCALE_X + self.w/SCALE_X
            percent = 1.0*(x - bar_min)/(bar_max - bar_min)
            percent = max(min(percent, 1.0), 0.0)
            self.value = (self.max_val - self.min_val) * percent + self.min_val

        if x >= self.x/SCALE_X and x <= self.x/SCALE_X + self.w/SCALE_X:
            if y >= self.y/SCALE_Y and y <= self.y/SCALE_Y + self.h/SCALE_Y:
                self.hovered = True
                if click:
                    self.dragging = True
                elif not held:
                    self.dragging = False
                return

        self.hovered = False





if __name__ == '__main__':
    a = MusGUI()
    pass

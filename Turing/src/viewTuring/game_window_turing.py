import tkinter as tk
from tkinter import Label
from PIL import ImageTk, Image
import pygame


DUELIST1 = 0
DUELIST2 = 1
DUELIST1_ATAQUE = 2
DUELIST2_ATAQUE = 3
DUELIST1_DEFESA = 4
DUELIST2_DEFESA = 5
DUELIST1_CURA = 6
DUELIST2_CURA = 7
DUELIST1_MORTO = 8
DUELIST2_MORTO = 9

productions = {'A': 'Ataque',
               'D': 'Defesa',
               'C': 'Cura'
               }


class GameWindow:
    def __init__(self, root, duelist1, duelist2):
        self.duelist1_state_label = None
        self.duelist2_life_label = None
        self.duelist2_state_label = None
        self.play_button = None
        self.duelist1_life_label = None
        self.duelist1_actions_label = None
        self.duelist2_actions_label = None
        self.turn_label = None
        self.choice_entry = None
        self.result_label = None
        self.current_player_label = None
        self.root = root
        self.duelist1 = duelist1
        self.duelist2 = duelist2
        self.turn = 1
        self.current_player = self.duelist1 if self.turn % 2 != 0 else self.duelist2  # Definir jogador atual
        self.duelist1_img_nrm = ImageTk.PhotoImage(Image.open("imgs/scorpion.png"))
        self.duelist2_img_nrm = ImageTk.PhotoImage(Image.open("imgs/subzero.png"))
        self.duelist1_img_atk = ImageTk.PhotoImage(Image.open("imgs/scorpionatk.png"))
        self.duelist2_img_atk = ImageTk.PhotoImage(Image.open("imgs/subzeroatk.png"))
        self.duelist1_img_def = ImageTk.PhotoImage(Image.open("imgs/scorpiondef.png"))
        self.duelist2_img_def = ImageTk.PhotoImage(Image.open("imgs/subzerodef.png"))
        self.duelist1_img_cura = ImageTk.PhotoImage(Image.open("imgs/scorpionheal.png"))
        self.duelist2_img_cura = ImageTk.PhotoImage(Image.open("imgs/subzeroheal.png"))
        self.duelist1_img_morto = ImageTk.PhotoImage(Image.open("imgs/scorpiondead.png"))
        self.duelist2_img_morto = ImageTk.PhotoImage(Image.open("imgs/subzerodead.png"))
        self.create_widgets()
        self.update_stats()
        self.duelist1_frame = None
        self.duelist2_frame = None

        pygame.mixer.init()
        pygame.mixer.music.load("mk.mp3")
        pygame.mixer.music.play(-1)  # -1 para reproduzir em loop infinito

        self.root.protocol("WM_DELETE_WINDOW", self.stop_audio)

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.root.destroy()

    def show_machines(self):
        def create_tape_label(window, tape):
            tk.Label(
                window,
                text="Fita:",
                font=("Arial", 12, "bold")
            ).pack()

            tape_str = ""
            for character in tape:
                if character == '<':
                    tape_str += f"{character} | "
                elif character == ' ':
                    tape_str += f"{character} | ..."
                else:
                    tape_str += f"{character} | "

            tk.Label(
                window,
                text=f"[ {tape_str} ]",
                font=("Arial", 10),
                wraplength=300  # Define um limite de largura para a label da fita
            ).pack()

        transitions_window = tk.Toplevel()
        transitions_window.title(f"{self.duelist1.name}")
        transitions_window.geometry("500x800")

        create_tape_label(transitions_window, self.duelist1.tape)

        for current_state, transitions in self.duelist1.transitions.items():
            tk.Label(transitions_window,
                     text=f"Estado: {current_state}",
                     font=("Arial", 12, "bold")).pack()

            for read, next_state in transitions.items():
                tk.Label(
                    transitions_window,
                    text=f"{read} → {next_state}",
                    font=("Arial", 10)
                ).pack()

        transitions_window2 = tk.Toplevel()
        transitions_window2.title(f"{self.duelist2.name}")
        transitions_window2.geometry("500x800")

        create_tape_label(transitions_window2, self.duelist2.tape)

        for current_state, transitions in self.duelist2.transitions.items():
            tk.Label(transitions_window2,
                     text=f"Estado: {current_state}",
                     font=("Arial", 12, "bold")).pack()

            for read, next_state in transitions.items():
                tk.Label(
                    transitions_window2,
                    text=f"{read} → {next_state}",
                    font=("Arial", 10)
                ).pack()

    def create_widgets(self):

        # Carregar a imagem de fundo
        self.background_img = ImageTk.PhotoImage(Image.open("imgs/background.png"))
        self.background_label = Label(self.root, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="MORTURING KOMBAT", font=("GodOfWar", 20, "bold"), fg="red").pack(pady=10)

        self.current_player_label = tk.Label(self.root, text=f"Turno de {self.current_player.name}",
                                             font=("GodOfWar", 14, "bold"), fg="red")
        self.current_player_label.pack(pady=5)

        self.reading_label = tk.Label(self.root, text=f"Qual leitura você deseja fazer? ",
                                      font=("Arial", 12, "bold"))
        self.reading_label.pack(pady=5)

        self.duelist1_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(self.duelist1_frame, text="DUELISTA 1", font=("GodOfWar", 12)).pack()
        self.duelist1_img = tk.Label(self.duelist1_frame, image=self.duelist1_img_nrm)
        self.duelist1_img.pack()
        tk.Label(self.duelist1_frame, text=f"Nome: {self.duelist1.name}", font=("Arial", 12)).pack()
        self.duelist1_life_label = tk.Label(
            self.duelist1_frame,
            text=f"Vida atual: {self.duelist1.life_points}/{self.duelist1.max_life_points}",
            font=("Arial", 12)
        )
        self.duelist1_life_label.pack()
        self.duelist1_state_label = tk.Label(self.duelist1_frame, text=f"Estado atual: {self.duelist1.state}",
                                             font=("Arial", 12))
        self.duelist1_state_label.pack()

        self.duelist1_frame.pack(side=tk.LEFT, padx=20)

        self.duelist2_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(self.duelist2_frame, text="DUELISTA 2", font=("GodOfWar", 12)).pack()
        self.duelist2_img = tk.Label(self.duelist2_frame, image=self.duelist2_img_nrm)
        self.duelist2_img.pack()
        tk.Label(self.duelist2_frame, text=f"Nome: {self.duelist2.name}", font=("Arial", 12)).pack()

        self.duelist2_life_label = tk.Label(
            self.duelist2_frame,
            text=f"Vida atual: {self.duelist2.life_points}/{self.duelist2.max_life_points}",
            font=("Arial", 12)
        )
        self.duelist2_life_label.pack()
        self.duelist2_state_label = tk.Label(self.duelist2_frame, text=f"Estado atual: {self.duelist2.state}",
                                             font=("Arial", 12))
        self.duelist2_state_label.pack()
        self.duelist2_frame.pack(side=tk.RIGHT, padx=20)

        self.turn_label = tk.Label(self.root, text=f"Turno: {self.turn}")
        self.turn_label.pack(pady=20)

        tk.Label(self.root, text="Digite uma leitura:", font=("Arial", 12, "bold")).pack()

        self.choice_entry = tk.Entry(self.root, font=("Arial", 12))
        self.choice_entry.pack()

        self.play_button = tk.Button(
            self.root,
            text="Ler",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.check_choice
        )
        self.play_button.pack(pady=10)

        self.root.bind("<Return>", lambda event: self.check_choice())


        # o self result label não pode mostart=r nada na tela inicialmente
        self.result_label = tk.Label(self.root,  font=("Arial",12, "bold"))

        duelist_actions_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist_actions_frame, text=f"Escritas na fita: ", font=("GodOfWar", 12, "bold")).pack()
        self.duelist1_actions_label = tk.Label(duelist_actions_frame,
                                               text=f"", font=("Arial", 12))

        self.duelist1_actions_label.pack()
        self.duelist2_actions_label = tk.Label(duelist_actions_frame, text=f"", font=("Arial", 12))
        self.duelist2_actions_label.pack()
        # no meio
        duelist_actions_frame.pack(side=tk.BOTTOM, padx=20)

        tk.Button(
            self.root,
            text="Ver máquinas e fitas",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            command=self.show_machines
        ).pack(pady=10)

    def update_stats(self):

        self.current_player_label.config(text=f"Turno de {self.current_player.name}", fg="purple",
                                         font=("GodOfWar", 14, "bold"))

        self.duelist1_life_label.config(
            text=f"Vida atual: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_state_label.config(text=f"Estado atual: {self.duelist1.state}")

        self.duelist2_life_label.config(
            text=f"Vida atual: {self.duelist2.life_points}/{self.duelist2.max_life_points}"
        )
        self.duelist2_state_label.config(text=f"Estado atual: {self.duelist2.state}")

        self.turn_label.config(text=f"Turno: {self.turn}")
        nome1 = ""
        valor1 = ""
        nome2 = ""
        valor2 = ""
        for a in self.duelist1.actions.values():
            nome1 = productions[a[1]]
            valor1 = str(a[0])
        for a in self.duelist2.actions.values():
            nome2 = productions[a[1]]
            valor2 = str(a[0])
        if self.current_player == self.duelist2:
            self.duelist1_actions_label.config(
                text=f"Escreveu e efetuou: {nome1 + ' ' + valor1}"
                     f" no duelista {self.duelist1.name}")
            self.duelist2_actions_label.config(
                text=f"Escreveu e efetuou: {nome2 + ' ' + valor2}"
                     f" no duelista {self.duelist2.name}")
        else:
            self.duelist2_actions_label.config(
                text=f"Escreveu e efetuou: {', '.join(nome2 + ' ' + str(a[0]) for a in self.duelist1.actions.values())}"
                     f" no duelista {self.duelist1.name}")
            self.duelist1_actions_label.config(
                text=f"Escreveu e efetuou: {', '.join(nome1 + ' ' + str(a[0]) for a in self.duelist2.actions.values())}"
                     f" no duelista {self.duelist2.name}")
        try:
            if nome1 == "Cura":
                self.duelist1_img.config(image=self.duelist1_img_cura)
            elif nome1 == "Ataque":
                self.duelist1_img.config(image=self.duelist1_img_atk)
            elif nome1 == "Defesa":
                self.duelist1_img.config(image=self.duelist1_img_def)
            else:
                self.duelist1_img.config(image=self.duelist1_img_nrm)

            if nome2 == "Cura":
                self.duelist2_img.config(image=self.duelist2_img_cura)
            elif nome2 == "Ataque":
                self.duelist2_img.config(image=self.duelist2_img_atk)
            elif nome2 == "Defesa":
                self.duelist2_img.config(image=self.duelist2_img_def)
            else:
                self.duelist2_img.config(image=self.duelist2_img_nrm)

        except:
            pass

    def check_choice(self):
        try:
            choice = int(self.choice_entry.get())
            if choice in [0, 1, 2]:
                self.result_label.config(text="")
                self.play_turn()
            else:
                self.result_label.config(text="Digite um número válido!", fg="red")
        except ValueError:
            self.result_label.config(text="Digite um número válido!", fg="red")

    def play_turn(self):
        choice = self.choice_entry.get()

        if self.current_player == self.duelist1:
            opponent = self.duelist2
        else:
            opponent = self.duelist1

        self.current_player.play_turn(opponent, choice)
        self.update_stats()

        if self.duelist1.life_points <= 0 and self.duelist2.life_points <= 0:
            self.result_label.config(text=f"Empate!", fg="blue")
            self.duelist1_img.config(image=self.duelist1_img_morto)
            self.duelist2_img.config(image=self.duelist2_img_morto)
            self.play_button.config(state=tk.DISABLED)
            pygame.mixer.music.stop()
            self.root.bind('<Return>', lambda e: None)
        elif self.duelist2.life_points <= 0:
            self.result_label.config(text=f"{self.duelist1.name} WINS! FATALITY!", fg="blue")
            self.result_label.pack()
            self.duelist2_img.config(image=self.duelist2_img_morto)
            self.play_button.config(state=tk.DISABLED)
            pygame.mixer.music.stop()
            self.root.bind('<Return>', lambda e: None)
            sound1 = pygame.mixer.Sound('scorpionwins.mp3')
            sound2 = pygame.mixer.Sound('fatality.mp3')
            sound1.play()
            pygame.time.wait(int(sound1.get_length() * 1000))
            sound2.play()

        elif self.duelist1.life_points <= 0:
            self.result_label.config(text=f"{self.duelist2.name} WINS! FATALITY", fg="blue")
            self.result_label.pack()
            self.duelist1_img.config(image=self.duelist1_img_morto)
            self.play_button.config(state=tk.DISABLED)
            pygame.mixer.music.stop()
            self.root.bind('<Return>', lambda e: None)
            sound1 = pygame.mixer.Sound('subzerowins.mp3')
            sound2 = pygame.mixer.Sound('fatality.mp3')
            sound1.play()
            pygame.time.wait(int(sound1.get_length() * 1000))
            sound2.play()



        self.turn += 1
        self.current_player = self.duelist1 if self.turn % 2 != 0 else self.duelist2  # Atualizar jogador atual
        self.choice_entry.delete(0, tk.END)

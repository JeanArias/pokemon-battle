import importlib
import inspect
import re
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from pokemon import Pokemon

BASE_DIR = Path(__file__).resolve().parent
SPRITES_DIR = BASE_DIR / "assets" / "sprites"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

BG = "#0b1020"
PANEL = "#151c2f"
PANEL_2 = "#202a44"
TEXT = "#f5f7ff"
MUTED = "#aab4cc"
ACCENT = "#f5c542"
GREEN = "#45d483"
RED = "#ef5b6b"
BLUE = "#4da3ff"
PURPLE = "#9b7bff"
ORANGE = "#ff9f43"


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def slugify(nombre):
    nombre = nombre.lower().strip()
    return re.sub(r"[^a-z0-9-]", "", nombre.replace(" ", "-"))


def sprite_url(pokemon):
    if getattr(pokemon, "imagen", None):
        return pokemon.imagen

    return (
        "https://img.pokemondb.net/sprites/red-blue/normal/"
        f"{slugify(pokemon.nombre)}.png"
    )


def get_sprite(pokemon, size=(140, 140)):
    """
    Downloads the sprite only once and stores it locally.
    The game uses the local copy after the first download.
    """

    filename = SPRITES_DIR / f"{slugify(pokemon.nombre)}.png"

    try:
        if not filename.exists():
            urllib.request.urlretrieve(
                sprite_url(pokemon),
                filename
            )

        if not PIL_AVAILABLE:
            return None

        image = Image.open(filename).convert("RGBA")
        image.thumbnail(size, Image.Resampling.NEAREST)

        return ImageTk.PhotoImage(image)

    except Exception:
        return None


def descubrir_pokemons():
    """
    Automatically finds classes that inherit from Pokemon
    inside the pokemons folder.
    """

    encontrados = []
    package_dir = BASE_DIR / "pokemons"

    for archivo in sorted(package_dir.glob("*.py")):

        if archivo.name.startswith("_"):
            continue

        try:
            modulo = importlib.import_module(
                f"pokemons.{archivo.stem}"
            )

        except Exception as error:
            print(
                f"No se pudo cargar {archivo.name}: {error}"
            )
            continue

        for _, clase in inspect.getmembers(
            modulo,
            inspect.isclass
        ):

            if (
                issubclass(clase, Pokemon)
                and clase is not Pokemon
                and clase.__module__ == modulo.__name__
            ):
                encontrados.append(clase)

    return encontrados


# ---------------------------------------------------------
# SELECTION CARD
# ---------------------------------------------------------

class PokemonSelectionCard(tk.Frame):

    def __init__(
        self,
        master,
        pokemon,
        app
    ):

        super().__init__(
            master,
            bg=PANEL,
            highlightthickness=2,
            highlightbackground=PANEL_2,
            width=205,
            height=245
        )

        self.pokemon = pokemon
        self.app = app

        self.pack_propagate(False)

        tk.Label(
            self,
            text=pokemon.nombre.upper(),
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(8, 0))

        tk.Label(
            self,
            text=pokemon.tipo,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack()

        photo = get_sprite(
            pokemon,
            (110, 110)
        )

        if photo:

            image_label = tk.Label(
                self,
                image=photo,
                bg=PANEL
            )

            image_label.image = photo
            image_label.pack(pady=(2, 0))

        else:

            tk.Label(
                self,
                text="SPRITE",
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 14, "bold")
            ).pack(pady=35)

        tk.Label(
            self,
            text=(
                f"HP {pokemon.vida()}   "
                f"ATK {pokemon.ataque}   "
                f"DEF {pokemon.defensa}   "
                f"SPD {pokemon.velocidad}"
            ),
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack()

        buttons = tk.Frame(
            self,
            bg=PANEL
        )

        buttons.pack(
            fill="x",
            padx=8,
            pady=8
        )

        self.j1_button = tk.Button(
            buttons,
            text="J1",
            command=lambda: app.select_pokemon(
                1,
                pokemon.nombre
            ),
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.j1_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 3)
        )

        self.j2_button = tk.Button(
            buttons,
            text="J2",
            command=lambda: app.select_pokemon(
                2,
                pokemon.nombre
            ),
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.j2_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(3, 0)
        )

    def update_selection(
        self,
        choice1,
        choice2
    ):

        self.j1_button.configure(
            bg=(
                ACCENT
                if choice1 == self.pokemon.nombre
                else PANEL_2
            ),
            fg=(
                "#151515"
                if choice1 == self.pokemon.nombre
                else TEXT
            ),
            activebackground=ACCENT
        )

        self.j2_button.configure(
            bg=(
                BLUE
                if choice2 == self.pokemon.nombre
                else PANEL_2
            ),
            fg=TEXT,
            activebackground=BLUE
        )


# ---------------------------------------------------------
# BATTLE FRAME
# ---------------------------------------------------------

class BattleFrame(tk.Frame):

    def __init__(
        self,
        master,
        pokemon1,
        pokemon2,
        on_new_battle,
        on_selection
    ):

        super().__init__(
            master,
            bg=BG
        )

        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

        self.on_new_battle = on_new_battle
        self.on_selection = on_selection

        self.round_number = 1
        self.turn_number = 0
        self.finished = False

        self.sleeping = {
            pokemon1: False,
            pokemon2: False
        }

        self.first, self.second = self._orden_turno()

        self.cards = {}
        self.images = {}

        # Maximum HP is used only by the visual bar.
        self.pokemon1._gui_max_hp = pokemon1.vida()
        self.pokemon2._gui_max_hp = pokemon2.vida()

        self._build()

        self._log(
            "La batalla comienza. "
            f"{self.first.nombre} tiene mayor velocidad y empieza."
        )

        self._refresh()

    def _orden_turno(self):

        if (
            self.pokemon1.velocidad
            >= self.pokemon2.velocidad
        ):

            return (
                self.pokemon1,
                self.pokemon2
            )

        return (
            self.pokemon2,
            self.pokemon1
        )

    # -----------------------------------------------------
    # BUILD BATTLE SCREEN
    # -----------------------------------------------------

    def _build(self):

        header = tk.Frame(
            self,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=24,
            pady=(12, 6)
        )

        tk.Label(
            header,
            text="POKEMON BATTLE ARENA",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 22, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="BATTLE MODE",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="right",
            pady=8
        )

        # Arena
        self.arena = tk.Frame(
            self,
            bg=PANEL
        )

        self.arena.pack(
            fill="x",
            padx=24,
            pady=(0, 8)
        )

        self.arena.grid_columnconfigure(
            0,
            weight=1
        )

        self.arena.grid_columnconfigure(
            1,
            weight=0
        )

        self.arena.grid_columnconfigure(
            2,
            weight=1
        )

        self.card1 = self._fighter_card(
            self.arena,
            self.pokemon1,
            0
        )

        self.card1["frame"].grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(15, 90),
            pady=15
        )

        self.card2 = self._fighter_card(
            self.arena,
            self.pokemon2,
            2
        )

        self.card2["frame"].grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(90, 15),
            pady=15
        )

        center = tk.Frame(
            self.arena,
            bg=PANEL
        )

        center.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            center,
            text="VS",
            bg=PANEL,
            fg=ACCENT,
            font=("Segoe UI", 25, "bold")
        ).pack()

        self.round_label = tk.Label(
            center,
            text="ROUND 1",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        )

        self.round_label.pack()

        self.turn_label = tk.Label(
            center,
            text=f"Turno: {self.first.nombre}",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        )

        self.turn_label.pack(
            pady=(4, 0)
        )

        # Compact log
        log_frame = tk.Frame(
            self,
            bg=PANEL,
            height=155
        )

        log_frame.pack(
            fill="x",
            padx=24,
            pady=(0, 8)
        )

        log_frame.pack_propagate(False)

        tk.Label(
            log_frame,
            text="BATTLE LOG",
            bg=PANEL,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(7, 2)
        )

        self.log = tk.Text(
            log_frame,
            bg="#0f1526",
            fg=TEXT,
            relief="flat",
            wrap="word",
            font=("Consolas", 9),
            padx=10,
            pady=5,
            state="disabled"
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8)
        )

        # Controls
        controls = tk.Frame(
            self,
            bg=BG
        )

        controls.pack(
            fill="x",
            padx=24,
            pady=(0, 12)
        )

        self.next_button = tk.Button(
            controls,
            text="▶  SIGUIENTE TURNO",
            command=self.next_turn,
            bg=ACCENT,
            fg="#151515",
            activebackground="#ffd95a",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=22,
            pady=9
        )

        self.next_button.pack(
            side="left"
        )

        tk.Button(
            controls,
            text="↩  SELECCIONAR POKÉMON",
            command=self.on_selection,
            bg=PANEL_2,
            fg=TEXT,
            activebackground="#2c3857",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=9
        ).pack(
            side="right",
            padx=(6, 0)
        )

        tk.Button(
            controls,
            text="↻  NUEVA BATALLA",
            command=self.on_new_battle,
            bg=PANEL_2,
            fg=TEXT,
            activebackground="#2c3857",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=9
        ).pack(
            side="right"
        )

    def _fighter_card(
        self,
        master,
        pokemon,
        column
    ):

        frame = tk.Frame(
            master,
            bg=PANEL,
            highlightthickness=2,
            highlightbackground=PANEL_2,
            width=350,
            height=270
        )

        frame.pack_propagate(False)

        top = tk.Frame(
            frame,
            bg=PANEL
        )

        top.pack(
            fill="x",
            padx=12,
            pady=(9, 0)
        )

        tk.Label(
            top,
            text=pokemon.nombre.upper(),
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        tk.Label(
            top,
            text=pokemon.tipo,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

        hp_background = tk.Frame(
            frame,
            bg="#30384f",
            height=16
        )

        hp_background.pack(
            fill="x",
            padx=12,
            pady=(8, 3)
        )

        hp_background.pack_propagate(False)

        hp_bar = tk.Frame(
            hp_background,
            bg=GREEN
        )

        hp_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=1
        )

        hp_label = tk.Label(
            frame,
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 8, "bold")
        )

        hp_label.pack(
            anchor="w",
            padx=12
        )

        image = get_sprite(
            pokemon,
            (120, 120)
        )

        if image:

            image_label = tk.Label(
                frame,
                image=image,
                bg=PANEL
            )

            image_label.image = image

            image_label.pack(
                pady=(0, 0)
            )

            self.images[pokemon] = image

        stats = tk.Label(
            frame,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        )

        stats.pack(
            pady=(0, 5)
        )

        card = {
            "frame": frame,
            "normal_bg": PANEL,
            "bar": hp_bar,
            "hp_label": hp_label,
            "stats": stats
        }

        self.cards[pokemon] = card

        return card

    # -----------------------------------------------------
    # REFRESH
    # -----------------------------------------------------

    def _refresh_card(
        self,
        pokemon,
        card
    ):

        current = pokemon.vida()

        maximum = getattr(
            pokemon,
            "_gui_max_hp",
            current
        )

        ratio = (
            max(
                0,
                min(
                    1,
                    current / maximum
                )
            )
            if maximum
            else 0
        )

        card["bar"].place_configure(
            relwidth=ratio
        )

        if ratio > 0.5:
            color = GREEN

        elif ratio > 0.2:
            color = ACCENT

        else:
            color = RED

        card["bar"].configure(
            bg=color
        )

        card["hp_label"].configure(
            text=f"HP  {current} / {maximum}"
        )

        card["stats"].configure(
            text=(
                f"ATK {pokemon.ataque}   "
                f"DEF {pokemon.defensa}   "
                f"SPD {pokemon.velocidad}"
            )
        )

    def _refresh(self):

        self._refresh_card(
            self.pokemon1,
            self.card1
        )

        self._refresh_card(
            self.pokemon2,
            self.card2
        )

        self.round_label.configure(
            text=f"ROUND {self.round_number}"
        )

        if not self.finished:

            current = (
                self.first
                if self.turn_number % 2 == 0
                else self.second
            )

            self.turn_label.configure(
                text=f"Turno: {current.nombre}"
            )

    # -----------------------------------------------------
    # EFFECTS
    # -----------------------------------------------------

    def flash_pokemon(
        self,
        pokemon,
        color,
        repetitions=3,
        duration=120
    ):

        card = self.cards.get(pokemon)

        if not card:
            return

        frame = card["frame"]

        def flash(step):

            if step >= repetitions * 2:

                frame.configure(
                    bg=card["normal_bg"]
                )

                return

            frame.configure(
                bg=(
                    color
                    if step % 2 == 0
                    else card["normal_bg"]
                )
            )

            self.after(
                duration,
                lambda: flash(step + 1)
            )

        flash(0)

    # -----------------------------------------------------
    # LOG
    # -----------------------------------------------------

    def _log(self, message):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            "end",
            message + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.configure(
            state="disabled"
        )

    # -----------------------------------------------------
    # TURN
    # -----------------------------------------------------

    def next_turn(self):

        if self.finished:
            return

        attacker = (
            self.first
            if self.turn_number % 2 == 0
            else self.second
        )

        defender = (
            self.second
            if self.turn_number % 2 == 0
            else self.first
        )

        self._log(
            f"\nROUND {self.round_number} — "
            f"Turno de {attacker.nombre}"
        )

        # Sleeping effect
        if self.sleeping[attacker]:

            self.sleeping[attacker] = False

            self._log(
                f"😴 {attacker.nombre} estaba dormido "
                "y pierde el turno."
            )

            self.flash_pokemon(
                attacker,
                PURPLE,
                repetitions=2
            )

            self._finish_turn()

            return

        # -------------------------------------------------
        # Compatible with the existing events.py
        # -------------------------------------------------

        try:

            from eventos import aplicar_evento_detallado

            event = aplicar_evento_detallado(
                attacker,
                defender
            )

            event_type = event["tipo"]
            target = event.get(
                "objetivo",
                attacker
            )

            event_text = event.get(
                "texto",
                ""
            )

        except ImportError:

            # Fallback for projects that still have only
            # aplicar_evento(atacante, defensor).
            from eventos import aplicar_evento

            event_result = aplicar_evento(
                attacker,
                defender
            )

            if event_result == "critico":
                event_type = "critico"

            elif event_result == "dormido":
                event_type = "dormido"

            elif event_result == "fallado":
                event_type = "fallado"

            else:
                event_type = "baya"

            target = (
                defender
                if event_type == "critico"
                else attacker
            )

            event_text = ""

        # -------------------------------------------------
        # EVENT: BERRY
        # -------------------------------------------------

        if event_type == "baya":

            self._log(
                event_text
                or f"🍓 {target.nombre} encontró una baya."
            )

            self.flash_pokemon(
                target,
                GREEN
            )

        # -------------------------------------------------
        # EVENT: CRITICAL
        # -------------------------------------------------

        elif event_type == "critico":

            self._log(
                event_text
                or "💥 ¡ATAQUE CRÍTICO!"
            )

            self.flash_pokemon(
                attacker,
                RED
            )

            damage = attacker.atacar()
            damage *= 2

            before = defender.vida()

            defender.recibir_daño(
                damage
            )

            dealt = (
                before
                - defender.vida()
            )

            self._log(
                f"⚔ {attacker.nombre} causa "
                f"{dealt} de daño crítico."
            )

            self.flash_pokemon(
                defender,
                RED,
                repetitions=2
            )

        # -------------------------------------------------
        # EVENT: SLEEP
        # -------------------------------------------------

        elif event_type == "dormido":

            self.sleeping[target] = True

            self._log(
                event_text
                or f"😴 {target.nombre} se quedó dormido."
            )

            self.flash_pokemon(
                target,
                PURPLE
            )

            self._log(
                f"{target.nombre} perderá su próximo turno."
            )

        # -------------------------------------------------
        # EVENT: MISS
        # -------------------------------------------------

        elif event_type == "fallado":

            self._log(
                event_text
                or f"❌ {attacker.nombre} falló el ataque."
            )

            self.flash_pokemon(
                attacker,
                ORANGE
            )

        # -------------------------------------------------
        # NORMAL ATTACK
        # -------------------------------------------------

        else:

            damage = attacker.atacar()

            before = defender.vida()

            defender.recibir_daño(
                damage
            )

            dealt = (
                before
                - defender.vida()
            )

            self._log(
                f"⚔ {attacker.nombre} ataca a "
                f"{defender.nombre} y causa "
                f"{dealt} de daño."
            )

            self.flash_pokemon(
                defender,
                RED,
                repetitions=2
            )

        self._refresh()

        if not defender.esta_vivo():

            self._finish_battle(
                attacker,
                defender
            )

            return

        self._finish_turn()

    def _finish_turn(self):

        self.turn_number += 1

        if self.turn_number % 2 == 0:
            self.round_number += 1

        self._refresh()

    # -----------------------------------------------------
    # END
    # -----------------------------------------------------

    def _finish_battle(
        self,
        winner,
        loser
    ):

        self.finished = True

        self.next_button.configure(
            state="disabled"
        )

        self._refresh()

        self._log(
            "\n🏆 "
            f"{winner.nombre} es el ganador."
        )

        self._log(
            f"💀 {loser.nombre} queda fuera de combate."
        )

        self.after(
            350,
            lambda: self._show_winner(
                winner
            )
        )

    def _show_winner(
        self,
        winner
    ):

        for widget in self.winfo_children():
            widget.destroy()

        WinnerFrame(
            self,
            winner,
            self.on_new_battle,
            self.on_selection
        ).pack(
            fill="both",
            expand=True
        )


# ---------------------------------------------------------
# WINNER FRAME
# ---------------------------------------------------------

class WinnerFrame(tk.Frame):

    def __init__(
        self,
        master,
        winner,
        on_new_battle,
        on_selection
    ):

        super().__init__(
            master,
            bg=BG
        )

        tk.Label(
            self,
            text="VICTORIA",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 30, "bold")
        ).pack(
            pady=(70, 10)
        )

        tk.Label(
            self,
            text="🏆",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI Emoji", 50)
        ).pack()

        photo = get_sprite(
            winner,
            (180, 180)
        )

        if photo:

            image_label = tk.Label(
                self,
                image=photo,
                bg=BG
            )

            image_label.image = photo
            image_label.pack(
                pady=5
            )

        tk.Label(
            self,
            text=winner.nombre,
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack(
            pady=5
        )

        tk.Label(
            self,
            text="¡Ha ganado la batalla!",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).pack()

        buttons = tk.Frame(
            self,
            bg=BG
        )

        buttons.pack(
            pady=30
        )

        tk.Button(
            buttons,
            text="↻  NUEVA BATALLA",
            command=on_new_battle,
            bg=ACCENT,
            fg="#151515",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=22,
            pady=10
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="👾  CAMBIAR POKÉMON",
            command=on_selection,
            bg=PANEL_2,
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10
        ).pack(
            side="left",
            padx=5
        )


# ---------------------------------------------------------
# MAIN APPLICATION - ONE WINDOW ONLY
# ---------------------------------------------------------

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "Pokemon Battle Arena"
        )

        self.geometry(
            "1120x760"
        )

        self.minsize(
            980,
            680
        )

        self.configure(
            bg=BG
        )

        self.classes = descubrir_pokemons()

        self.choice1 = tk.StringVar()
        self.choice2 = tk.StringVar()

        if self.classes:
            self.choice1.set(
                self.classes[0]().nombre
            )

        if len(self.classes) > 1:
            self.choice2.set(
                self.classes[1]().nombre
            )

        # ONE permanent content container.
        self.content = tk.Frame(
            self,
            bg=BG
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        self.show_selection()

    # -----------------------------------------------------
    # SCREEN MANAGEMENT
    # -----------------------------------------------------

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_selection(self):

        self.clear_content()

        self.classes = descubrir_pokemons()

        if not self.classes:

            tk.Label(
                self.content,
                text="No se encontraron Pokémon.",
                bg=BG,
                fg=RED,
                font=("Segoe UI", 16, "bold")
            ).pack(
                expand=True
            )

            return

        SelectionFrame(
            self.content,
            self
        ).pack(
            fill="both",
            expand=True
        )

    def show_battle(
        self,
        pokemon1,
        pokemon2
    ):

        self.clear_content()

        BattleFrame(
            self.content,
            pokemon1,
            pokemon2,
            self.new_battle,
            self.show_selection
        ).pack(
            fill="both",
            expand=True
        )

    def new_battle(self):

        self.start_battle()

    # -----------------------------------------------------
    # SELECTION
    # -----------------------------------------------------

    def select_pokemon(
        self,
        player,
        name
    ):

        if player == 1:

            if name == self.choice2.get():

                messagebox.showwarning(
                    "Pokémon repetido",
                    "Cada jugador debe escoger "
                    "un Pokémon diferente."
                )

                return

            self.choice1.set(name)

        else:

            if name == self.choice1.get():

                messagebox.showwarning(
                    "Pokémon repetido",
                    "Cada jugador debe escoger "
                    "un Pokémon diferente."
                )

                return

            self.choice2.set(name)

        self.show_selection()

    def start_battle(self):

        if (
            not self.choice1.get()
            or not self.choice2.get()
        ):

            messagebox.showwarning(
                "Selección incompleta",
                "Debes seleccionar dos Pokémon."
            )

            return

        if (
            self.choice1.get()
            == self.choice2.get()
        ):

            messagebox.showwarning(
                "Selección inválida",
                "Debes seleccionar dos Pokémon diferentes."
            )

            return

        classes_by_name = {
            cls().nombre: cls
            for cls in self.classes
        }

        p1 = classes_by_name[
            self.choice1.get()
        ]()

        p2 = classes_by_name[
            self.choice2.get()
        ]()

        self.show_battle(
            p1,
            p2
        )


# ---------------------------------------------------------
# SELECTION FRAME
# ---------------------------------------------------------

class SelectionFrame(tk.Frame):

    def __init__(
        self,
        master,
        app
    ):

        super().__init__(
            master,
            bg=BG
        )

        self.app = app
        self.cards = []

        self._build()

    def _build(self):

        header = tk.Frame(
            self,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(18, 4)
        )

        tk.Label(
            header,
            text="POKEMON BATTLE ARENA",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 25, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text=(
                f"{len(self.app.classes)} "
                "POKEMON DISPONIBLES"
            ),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="right",
            pady=10
        )

        tk.Label(
            self,
            text=(
                "Selecciona un Pokémon para "
                "cada jugador"
            ),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 7)
        )

        # Selection panel
        panel = tk.Frame(
            self,
            bg=PANEL
        )

        panel.pack(
            fill="x",
            padx=25,
            pady=5
        )

        top = tk.Frame(
            panel,
            bg=PANEL
        )

        top.pack(
            fill="x",
            padx=12,
            pady=(8, 2)
        )

        tk.Label(
            top,
            text="SELECCIÓN DE POKÉMON",
            bg=PANEL,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        tk.Label(
            top,
            text="← desplázate para ver más →",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(side="right")

        canvas_container = tk.Frame(
            panel,
            bg=PANEL
        )

        canvas_container.pack(
            fill="x",
            padx=8,
            pady=(2, 8)
        )

        self.canvas = tk.Canvas(
            canvas_container,
            bg=PANEL,
            highlightthickness=0,
            height=275
        )

        scrollbar = tk.Scrollbar(
            canvas_container,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.canvas.configure(
            xscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            fill="x",
            expand=True
        )

        scrollbar.pack(
            fill="x"
        )

        cards_frame = tk.Frame(
            self.canvas,
            bg=PANEL
        )

        self.canvas.create_window(
            (0, 0),
            window=cards_frame,
            anchor="nw"
        )

        cards_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        for pokemon_class in self.app.classes:

            pokemon = pokemon_class()

            card = PokemonSelectionCard(
                cards_frame,
                pokemon,
                self.app
            )

            card.pack(
                side="left",
                padx=6,
                pady=4
            )

            self.cards.append(card)

        self.canvas.bind(
            "<Shift-MouseWheel>",
            self.horizontal_scroll
        )

        # Selected players
        selected = tk.Frame(
            self,
            bg=BG
        )

        selected.pack(
            fill="x",
            padx=25,
            pady=(8, 5)
        )

        tk.Label(
            selected,
            text=(
                f"JUGADOR 1: "
                f"{self.app.choice1.get() or '--'}"
            ),
            bg=PANEL,
            fg=ACCENT,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=8
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        tk.Label(
            selected,
            text=(
                f"JUGADOR 2: "
                f"{self.app.choice2.get() or '--'}"
            ),
            bg=PANEL,
            fg=BLUE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=8
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        tk.Label(
            self,
            text=(
                f"{self.app.choice1.get() or '--'}"
                "   ⚔   VS   ⚔   "
                f"{self.app.choice2.get() or '--'}"
            ),
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(
            pady=(3, 8)
        )

        tk.Button(
            self,
            text="⚔  INICIAR BATALLA",
            command=self.app.start_battle,
            bg=ACCENT,
            fg="#151515",
            activebackground="#ffd95a",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=35,
            pady=11
        ).pack(
            pady=4
        )

        self.update_cards()

    def horizontal_scroll(self, event):

        direction = (
            -1
            if event.delta > 0
            else 1
        )

        self.canvas.xview_scroll(
            direction,
            "units"
        )

    def update_cards(self):

        for card in self.cards:

            card.update_selection(
                self.app.choice1.get(),
                self.app.choice2.get()
            )


# ---------------------------------------------------------
# START
# ---------------------------------------------------------

def iniciar():

    app = App()
    app.mainloop()


if __name__ == "__main__":
    iniciar()
import random
import tkinter as tk


CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
BOARD_WIDTH = CELL_SIZE * GRID_WIDTH
BOARD_HEIGHT = CELL_SIZE * GRID_HEIGHT
START_SPEED = 125

BACKGROUND = "#9bbc0f"
DARK = "#0f380f"
MID = "#306230"
LIGHT = "#8bac0f"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake 97")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK)
        self.root.bind("<KeyPress>", self.handle_key)

        header = tk.Frame(root, bg=DARK, padx=18, pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SNAKE 97",
            font=("Courier New", 22, "bold"),
            fg=BACKGROUND,
            bg=DARK,
        ).pack(side="left")

        self.score_label = tk.Label(
            header,
            text="PUNTOS: 0",
            font=("Courier New", 12, "bold"),
            fg=BACKGROUND,
            bg=DARK,
        )
        self.score_label.pack(side="right", pady=5)

        self.canvas = tk.Canvas(
            root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=BACKGROUND,
            highlightthickness=5,
            highlightbackground=MID,
        )
        self.canvas.pack(padx=18, pady=(0, 12))

        controls = tk.Frame(root, bg=DARK, padx=18, pady=0)
        controls.pack(fill="x", pady=(0, 16))
        tk.Label(
            controls,
            text="FLECHAS: MOVER   ESPACIO: PAUSA   R: REINICIAR",
            font=("Courier New", 9, "bold"),
            fg=BACKGROUND,
            bg=DARK,
        ).pack()

        self.reset()

    def reset(self):
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.speed = START_SPEED
        self.paused = False
        self.game_over = False
        self.food = self.create_food()
        self.update_score()
        self.draw()
        self.root.after(self.speed, self.tick)

    def create_food(self):
        available = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        return random.choice(available) if available else None

    def handle_key(self, event):
        key = event.keysym.lower()
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        if key in directions:
            proposed = directions[key]
            if proposed != (-self.direction[0], -self.direction[1]):
                self.next_direction = proposed
        elif key == "space" and not self.game_over:
            self.paused = not self.paused
            self.draw()
        elif key == "r":
            self.reset()

    def tick(self):
        if not self.game_over and not self.paused:
            self.move()
        self.root.after(self.speed, self.tick)

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        direction_x, direction_y = self.direction
        new_head = (head_x + direction_x, head_y + direction_y)

        hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
        hit_self = new_head in self.snake[:-1]
        if hit_wall or hit_self:
            self.game_over = True
            self.draw()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.speed = max(55, START_SPEED - (self.score // 50) * 5)
            self.food = self.create_food()
            self.update_score()
        else:
            self.snake.pop()
        self.draw()

    def update_score(self):
        self.score_label.config(text=f"PUNTOS: {self.score}")

    def draw_cell(self, position, color):
        x, y = position
        margin = 2
        self.canvas.create_rectangle(
            x * CELL_SIZE + margin,
            y * CELL_SIZE + margin,
            (x + 1) * CELL_SIZE - margin,
            (y + 1) * CELL_SIZE - margin,
            fill=color,
            outline=color,
        )

    def draw(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.draw_cell((x, y), DARK)
        if self.snake:
            self.draw_cell(self.snake[0], MID)
        if self.food:
            self.draw_cell(self.food, DARK)

        if self.paused:
            self.draw_message("PAUSA", "Pulsa ESPACIO para continuar")
        elif self.game_over:
            self.draw_message("GAME OVER", "Pulsa R para volver a jugar")

    def draw_message(self, title, subtitle):
        self.canvas.create_rectangle(
            90,
            BOARD_HEIGHT // 2 - 54,
            BOARD_WIDTH - 90,
            BOARD_HEIGHT // 2 + 54,
            fill=BACKGROUND,
            outline=DARK,
            width=3,
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            BOARD_HEIGHT // 2 - 20,
            text=title,
            fill=DARK,
            font=("Courier New", 20, "bold"),
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            BOARD_HEIGHT // 2 + 20,
            text=subtitle,
            fill=DARK,
            font=("Courier New", 9, "bold"),
        )


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
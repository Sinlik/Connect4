import tkinter as tk

# Initialize the main window
root = tk.Tk()

# Create a Canvas widget
canvas = tk.Canvas(root, width=1000, height=1000)
canvas.pack()

# Create a Label to display the winner
winner_label = tk.Label(root, text="", font=("Helvetica", 16))
winner_label.pack()
winner_label.place(x=150, y=20)

# Initialize a variable to track the current player
current_player = "red"

def createBoard(width, height):
    board = [[None for _ in range(width)] for _ in range(height)]
    return board

def draw_circle(canvas, x, y, radius, color):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="black")

def displayerBoard(board, canvas, width, height, radius, color):
    """
    Display the board using the graphics
    """
    spacing = radius * 3
    offsetX = 50
    offsetY = 50
    margin = 10
    board_width = width * spacing + margin * 2
    board_height = height * spacing + margin * 2

    # Draw the board
    canvas.create_rectangle(offsetX - 30, 75, offsetX + board_width, 100 + board_height, fill="blue")

    for i in range(height):
        y = i * spacing + radius
        for j in range(width):
            x = j * spacing + radius
            board[i][j] = draw_circle(canvas, x + offsetX, y + 100, radius, color)

    # Mouse click binding
    canvas.bind("<Button-1>", lambda event: dropPiece(board, canvas, offsetX, offsetY, event.y, event.x - offsetX, radius))

def dropPiece(board, canvas, offsetX, offsetY, y, x, radius):
    global current_player
    spacing = radius * 3
    col = None

    # Determine which column was clicked
    for j in range(len(board[0])):
        if x > j * spacing and x < (j + 1) * spacing:
            col = j
            break

    if col is None:
        return  # Click was outside of the board

    # Find the lowest empty spot in the column
    for i in range(len(board) - 1, -1, -1):
        if canvas.itemcget(board[i][col], "fill") == "white":
            # Place the piece
            canvas.itemconfig(board[i][col], fill=current_player)
            # Check for a win after placing the piece
            if check_win(board, canvas, current_player, i, col, radius):
                winner_label.config(text=f"{current_player.capitalize()} wins!")
                canvas.unbind("<Button-1>")  # Stop further input
                return
            # Switch player after placing a piece
            current_player = "yellow" if current_player == "red" else "red"
            break

def check_win(board, canvas, player, row, col, radius):
    # Vertical check
    if check_direction(board, canvas, player, row, col, 1, 0, radius):
        return True
    # Horizontal check
    if check_direction(board, canvas, player, row, col, 0, 1, radius):
        return True
    # Diagonal check (bottom-left to top-right)
    if check_direction(board, canvas, player, row, col, 1, 1, radius):
        return True
    # Diagonal check (bottom-right to top-left)
    if check_direction(board, canvas, player, row, col, 1, -1, radius):
        return True
    return False

def check_direction(board, canvas, player, row, col, row_dir, col_dir, radius):
    count = 0
    # Check in the positive direction (e.g., right for horizontal)
    for i in range(4):
        r = row + i * row_dir
        c = col + i * col_dir
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            if canvas.itemcget(board[r][c], "fill") == player:
                count += 1
            else:
                break
        else:
            break

    # Check in the negative direction (e.g., left for horizontal)
    for i in range(1, 4):
        r = row - i * row_dir
        c = col - i * col_dir
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            if canvas.itemcget(board[r][c], "fill") == player:
                count += 1
            else:
                break
        else:
            break

    return count >= 4


def connectFour(width, height, radius):
    board = createBoard(width, height)
    displayerBoard(board, canvas, width, height, radius, "white")
    root.mainloop()

connectFour(7, 6, 20)
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_9_BY_15
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18

#---------------CONSTANTS FOR GRID SIZE--------------#
GRID_WIDTH = 10
GRID_HEIGHT = 20         
CELL_SIZE = 30  # Size of each cell/block in pixels
current_tetromino = None  # to keep track of the current Tetromino that is falling down the grid
score = 0
lines_cleared = 0
#----------------2D ARRAY GRID--------------#
GRID = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

#---------------FOR LINE DRAWING-------------#

def Zone_Of_Interest(x0, y0, x1, y1):   # Initial zone of the endpoints
    dy = y1 - y0
    dx = x1 - x0
    if abs(dx) > abs(dy):
        if dx > 0:
            return 0 if dy > 0 else 7
        else:
            return 3 if dy > 0 else 4
    else:
        if dy > 0:
            return 1 if dx > 0 else 2
        else:
            return 6 if dx > 0 else 5


def To_Zone_Zero(zone, x, y):    # Converting to Zone 0
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def Zone_Zero_To(zone, x, y):   # Converting to the desired zone from zone 0
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def Midpoint_Line(zone, x0, y0, x1, y1):    # Line drawing
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    d_init = 2 * dy - dx
    East = 2 * dy
    North_East = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        a, b = Zone_Zero_To(zone, x, y)
        Draw_Pixel(a, b)

        if d_init <= 0:
            x += 1
            d_init += East
        else:
            x += 1
            y += 1
            d_init += North_East


#-----------------DRAW FUNCTIONS--------------#

def Draw_Pixel(x, y):
    glVertex2f(x, y)


def Draw_Pixelz(x, y):

    glBegin(GL_POINTS)
    # Draw points inside the cell to fill it
    for i in range(int(x), int(x + CELL_SIZE)):
        for j in range(int(y), int(y + CELL_SIZE)):
            glVertex2f(i, j)
    glEnd()


def Draw_Horizontal_Lines(x0, y0, x1, y1):
    Zone = Zone_Of_Interest(x0, y0, x1, y1)
    x0_zero, y0_zero = To_Zone_Zero(Zone, x0, y0)
    x1_zero, y1_zero = To_Zone_Zero(Zone, x1, y1)
    Midpoint_Line(Zone, x0_zero, y0_zero, x1_zero, y1_zero)


def Draw_Vertical_Lines(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))

    for i in range(steps + 1):
        x = x0 + (dx * i) // steps
        y = y0 + (dy * i) // steps
        Draw_Pixel(x, y)


def Draw_Grid():
    glColor3f(0.5, 0.5, 0.5)  # Set color for grid lines
    glBegin(GL_POINTS)
    # Draw horizontal lines
    for i in range(GRID_HEIGHT + 1):
        Draw_Horizontal_Lines(0, i * CELL_SIZE, GRID_WIDTH * CELL_SIZE, i * CELL_SIZE)

    # Draw vertical lines
    for j in range(GRID_WIDTH + 1):
        Draw_Vertical_Lines(j * CELL_SIZE, 0, j * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
    glEnd()


#-----------------TETROMMINO SHAPES----------------#
I_SHAPE = [
    [1, 1, 1, 1]
]

O_SHAPE = [
    [1, 1],
    [1, 1]
]

T_SHAPE = [
    [0, 1, 0],
    [1, 1, 1]
]

L_SHAPE = [
    [1, 0],
    [1, 0],
    [1, 1]
]

J_SHAPE = [
    [0, 1],
    [0, 1],
    [1, 1]
]

S_SHAPE = [
    [0, 1, 1],
    [1, 1, 0]
]

Z_SHAPE = [
    [1, 1, 0],
    [0, 1, 1]
]

#-------------------TETROMINOS SPAWING-----------------#

def spawn_tetromino():
    tetromino_shapes = [I_SHAPE, O_SHAPE, T_SHAPE, L_SHAPE, J_SHAPE, S_SHAPE, Z_SHAPE]
    return random.choice(tetromino_shapes)


#----------------USER INPUT HANDLING--------------#

def keyboard(key, x, y):
    global paused, game_over, current_tetromino
    
    if key == b' ':
        paused = not paused  # Toggle pause state
    
    # If the game is not paused and not game over, handle other key inputs
    elif not game_over and not paused:
        if key == b'a':
            current_tetromino.move_left()
        elif key == b'd':
            current_tetromino.move_right()
        elif key == b's':
            current_tetromino.move_down()
        elif key == b'q':
            current_tetromino.rotate_counterclockwise()
        elif key == b'e':
            current_tetromino.rotate_clockwise()
        elif key == b'r':
            restart_game()

    # Redraw the scene if pause state changed or other inputs occurred
    glutPostRedisplay()


def restart_game():
    global GRID, current_tetromino, score, lines_cleared, game_over, paused
    
    # Reset the grid to an empty state
    GRID = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Reset the game state
    score = 0
    lines_cleared = 0
    game_over = False
    paused = False
    
    # Spawn a new tetromino
    tetromino_shape = spawn_tetromino()
    current_tetromino = Tetromino(tetromino_shape)
    
    # Refresh the display
    glutPostRedisplay()


#-------------------TETROMINO CLASS-----------------#

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0
        self.can_move_down = True  # Flag to track if Tetromino can move down
    
    def render(self):
        glColor3f(0.0, 1.0, 0.0)  # Set color for Tetromino shapes
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    Draw_Pixelz((self.x + j) * CELL_SIZE, (GRID_HEIGHT - 1 - (self.y + i)) * CELL_SIZE)

    def move_left(self):
        if self.x > 0 and all(not GRID[self.y + i][self.x + j - 1] for i, row in enumerate(self.shape) for j, cell in enumerate(row) if cell):
            self.x -= 1

    def move_right(self):
        if self.x + len(self.shape[0]) < GRID_WIDTH and all(not GRID[self.y + i][self.x + j + 1] for i, row in enumerate(self.shape) for j, cell in enumerate(row) if cell):
            self.x += 1

    def move_down(self):
        global score  # Access the global score variable
    
        if self.y + len(self.shape) < GRID_HEIGHT and not self.check_collision():
            self.y += 1
        # Increment score each time the Tetromino moves down
            score += 1  # Increase score by 1 each time a block falls
            return True
        else:
        # Land the Tetromino and update the grid
            self.update_grid()
            return False
    
        return True

    def rotate_clockwise(self):
        # Rotate the shape
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        # Check if the new shape can fit in the current position
        if self.can_place(new_shape, self.x, self.y):
            self.shape = new_shape

    def rotate_counterclockwise(self):
        # Rotate the shape
        new_shape = [list(row[::-1]) for row in zip(*self.shape)]
        # Check if the new shape can fit in the current position
        if self.can_place(new_shape, self.x, self.y):
            self.shape = new_shape

    def can_place(self, shape, x, y):
        # Check if the shape can be placed at the given coordinates without going out of bounds or overlapping
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or GRID[y + i][x + j]:
                        return False
        return True

    def update_grid(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    GRID[self.y + i][self.x + j] = 1


#------------------------------------------------#

    def check_game_over(self):
    # Check if the Tetromino collides with existing tetrominoes in the grid
    # near the top of the grid (rows 0 to 2)
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                # Calculate the grid coordinates for the Tetromino block
                    grid_x = self.x + j
                    grid_y = self.y + i
                
                # Check for collision at the top of the grid
                    if grid_y < 2 and GRID[grid_y][grid_x]:
                        return True
                
                # Check if the Tetromino is placed above the grid's top row
                    if grid_y < 0:
                        return True
    
        return False


#----------------COLLISION DETECTION AND ROW CHECK---------------#
    def check_collision(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    # Check for collision with the grid boundaries
                    if self.y + i >= GRID_HEIGHT - 1 or self.x + j < 0 or self.x + j >= GRID_WIDTH:
                        return True
                    # Check for collision with other Tetrominoes
                    if GRID[self.y + i + 1][self.x + j]:
                        return True
        return False

def render_grid():
    glColor3f(1.0, 1.0, 1.0)
    #glBegin(GL_POINTS)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            #print(x,y)
            if GRID[y][x] == 1:
                Draw_Pixelz(x * CELL_SIZE, (GRID_HEIGHT - y -1) * CELL_SIZE)

#------------------------------------------------#
def check_completed_rows():
    global score, lines_cleared
    completed_rows = []
    
    # Check each row from bottom to top for completed rows
    for i in range(GRID_HEIGHT - 1, -1, -1):
        # Check if the row is completed (all cells filled)
        if all(GRID[i]):
            completed_rows.append(i)
    
    # If there are any completed rows
    if completed_rows:
        # Increment score and lines cleared
        lines_cleared += len(completed_rows)
        # score += len(completed_rows) # Adjust score as desired
        
        # Remove completed rows and shift rows above downwards
        for row in completed_rows:
            del GRID[row]
            GRID.insert(0, [0 for _ in range(GRID_WIDTH)])  # Add empty row at the top of the grid
    
    # Refresh display to reflect changes
    glutPostRedisplay()

#-----------------DISPLAY FUNCTION--------------#

def display_text(text, x, y):
    glColor3f(1.0, 1.0, 1.0)  # White text
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    if game_over:
        # Display the game over screen
        display_game_over_screen()
    elif paused:
        # Display a pause message when the game is paused
        display_text("Game Paused", GRID_WIDTH * CELL_SIZE // 2 - 50, GRID_HEIGHT * CELL_SIZE // 2)
    else:
        # Render the current Tetromino and the grid if the game is not over
        if current_tetromino is not None:
            current_tetromino.render()
        render_grid()
        Draw_Grid()
        
        # Display the live score counter and lines cleared counter
        display_text(f"Score: {score}", GRID_WIDTH * CELL_SIZE + 10, GRID_HEIGHT * CELL_SIZE - 20)
        display_text(f"Lines: {lines_cleared}", GRID_WIDTH * CELL_SIZE + 10, GRID_HEIGHT * CELL_SIZE - 40)
        
        # Display restart and pause options
        glColor3f(0.0, 1.0, 0.0)  # Green for restart option
        display_text("Press 'R' to Restart", GRID_WIDTH * CELL_SIZE + 10, GRID_HEIGHT * CELL_SIZE - 70)
        
        glColor3f(0.0, 0.0, 1.0)  # Blue for pause option
        display_text("Press ' ' (Space) to Pause", GRID_WIDTH * CELL_SIZE + 10, GRID_HEIGHT * CELL_SIZE - 90)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 600, 0, 600)
    glMatrixMode(GL_MODELVIEW)

game_over = False  # Global flag to track if the game is over
paused = False  # Global flag to track if the game is paused

def display_game_over_screen():
    glColor3f(1.0, 0.0, 0.0)  # Red text color
    glRasterPos2f(GRID_WIDTH * CELL_SIZE // 2 - 50, GRID_HEIGHT * CELL_SIZE // 2)  # Centered in the window
    
    # Display "Game Over" message
    message = "Game Over"
    for char in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Display the final score and lines cleared
    final_score_text = f"Final Score: {score}"
    glRasterPos2f(GRID_WIDTH * CELL_SIZE // 2 - 80, GRID_HEIGHT * CELL_SIZE // 2 - 30)
    for char in final_score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    final_lines_text = f"Lines Cleared: {lines_cleared}"
    glRasterPos2f(GRID_WIDTH * CELL_SIZE // 2 - 80, GRID_HEIGHT * CELL_SIZE // 2 - 60)
    for char in final_lines_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def timer_callback(value):
    global current_tetromino, game_over  # Added game_over to globals

    # If the game is paused, skip the game loop
    if paused:
        glutTimerFunc(1000, timer_callback, 0)
        return  # Skip further game loop operations and exit the function

    # Check if the current tetromino is None
    if current_tetromino is not None:
        # If the tetromino cannot move down, handle game over or other logic
        if not current_tetromino.move_down():
            # Check for game over
            if current_tetromino.check_game_over():
                # Set the game_over flag to True and print a message
                game_over = True
                print("Game Over")
                display_game_over_message()  # Display the game over screen
                return  # Stop the game loop

            # Handle landing the tetromino and spawning a new one
            current_tetromino.update_grid()
            check_completed_rows()
            tetromino_shape = spawn_tetromino()
            current_tetromino = Tetromino(tetromino_shape)
            
            # Check again for game over with the new tetromino
            if current_tetromino.check_game_over():
                # Set the game_over flag to True and print a message
                game_over = True
                print("Game Over")
                display_game_over_message()  # Display the game over screen
                return  # Stop the game loop

    # Continue the game loop
    glutPostRedisplay()
    glutTimerFunc(1000, timer_callback, 0)




def display_game_over_message():
    glColor3f(1.0, 0.0, 0.0)  # Set text color to red
    glRasterPos2f(150, 300)  # Position the text in the center of the screen
    
    # Display the "Game Over" message using GLUT bitmap fontss
    message = "Game Over"
    for char in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Display an optional restart message
    restart_message = "Press 'R' to Restart"
    glRasterPos2f(120, 270)  # Position the restart message below the game over message
    for char in restart_message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Tetris Game")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    
    global current_tetromino
    # Spawn the initial Tetromino
    tetromino_shape = spawn_tetromino()
    current_tetromino = Tetromino(tetromino_shape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(1000, timer_callback, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
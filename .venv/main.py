import turtle
import time

# Game setup
wn = turtle.Screen()
wn.title("Breakout Game")
wn.bgcolor("black")
wn.setup(width=800, height=700)  # Increased height
wn.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -300)  # Adjusted position for new screen height

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 3
ball.dy = -3
ball_radius = 10  # Circle radius in pixels

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]

for y in range(250, 150, -30):  # Adjusted brick positions
    for x in range(-350, 350, 70):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[(y // 30) % 5])
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(x, y)
        bricks.append(brick)

# Score
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 310)  # Adjusted position
score_display.write("Score: 0", align="center", font=("Courier", 24, "normal"))


# Paddle movement (same as before)
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        x += 20
    paddle.setx(x)


def paddle_left():
    x = paddle.xcor()
    if x > -350:
        x -= 20
    paddle.setx(x)


# Keyboard binding
wn.listen()
wn.onkeypress(paddle_right, "Right")
wn.onkeypress(paddle_left, "Left")

# Game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border collisions
    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1

    if ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1

    if ball.ycor() > 340:  # Adjusted for new screen height
        ball.sety(340)
        ball.dy *= -1

    # Bottom border (game over)
    if ball.ycor() < -340:  # Adjusted for new screen height
        ball.goto(0, 0)
        ball.dy *= -1
        score_display.clear()
        score_display.write("Game Over! Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
        time.sleep(2)
        break

    # Improved paddle collision
    paddle_top = paddle.ycor() + 10  # Top of paddle
    ball_bottom = ball.ycor() - ball_radius

    if (ball.dy < 0 and  # Only check when moving downward
            paddle_top - 5 <= ball_bottom <= paddle_top + 5 and  # Collision range
            (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50)):
        # Calculate hit position relative to paddle center
        hit_pos = (ball.xcor() - paddle.xcor()) / 50
        ball.dx = hit_pos * 5  # Adjust horizontal speed based on hit position
        ball.dy *= -1

        # Prevent ball from getting stuck in paddle
        ball.sety(paddle_top + ball_radius + 1)

    # Brick collisions
    for brick in bricks:
        if brick.distance(ball) < 30:
            bricks.remove(brick)
            brick.hideturtle()
            score += 10
            score_display.clear()
            score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
            ball.dy *= -1
            break

    # Check for win
    if len(bricks) == 0:
        score_display.clear()
        score_display.write("You Win! Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
        time.sleep(2)
        break

    # Speed control
    time.sleep(0.01)

wn.mainloop()
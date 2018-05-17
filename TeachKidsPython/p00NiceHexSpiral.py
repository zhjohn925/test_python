
import turtle

# https://docs.python.org/3.3/library/turtle.html?highlight=turtle

colors = ['red', 'purple', 'blue', 'green', 'yellow', 'orange']
# we can multiple turtles
t1 = turtle.Turtle()  # alias to Pen()
t2 = turtle.Turtle()
# we can has only one screen, set screen color to black 
turtle.bgcolor('black')
for x in range(30):  #360
    # pen methods
    t1.pencolor(colors[x%6])
    t1.width(x/100+1)
    t1.forward(x)
    t1.left(59)
t2.pencolor('pink')    
t2.left(45)
t2.forward(100)

while True:
    t1.hideturtle()
    t2.hideturtle()


import turtle

# https://docs.python.org/3.3/library/turtle.html?highlight=turtle

t = turtle.Pen() # alias to turtle.Turtle()
# set screen background color to black
turtle.bgcolor('black')

colors = ['red','yellow','blue','orange','green','purple']
# you can choose between 2 and 6 sides for different shapes
# sides = 6
sides = eval(input('Enter number of sides (2-6): '))
for x in range(60):
    t.pencolor(colors[x % sides])
    t.forward(x*3/sides + x)
    t.left(360/sides+1)   # try plus 1 to tilt 
    t.width(x*sides/200)

while True:
    t.hideturtle()

import pyglet, json, time, subprocess, string
from pyglet import gl
#data_orig = json.load(open("test", "r"))
#data = data_orig
data_orig = []
message = string.ascii_letters
#message = ["lmao"]
message = ["g/u/rl", "please"] * 20
def from_char(c):
    data_orig = []
    for line in subprocess.check_output(["toilet", "-f", "letter", c]).decode("utf-8").split("\n"):
        for i in range(2):
            data_orig.append([[0 if x == " " or x == '"' else 1 for x in line]])
    data_orig = data_orig[::-1]
    return data_orig
data = []
#side_length = 40
side_length = 15
window = pyglet.window.Window()
def line(x1, y1, x2, y2):
    gl.glBegin(gl.GL_LINES)
    gl.glColor3f(1.0,1.0,1.0)
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x2, y2)
    gl.glEnd()
def graph(x, y, val):
    x = int(x)
    y = int(y)
    if val == 1:
        origin = [x, y]
        # middle left, middle right, top middle, top left, top right, top top
        #    tt
        # tl    tr
        # ml tm mr
        #    or
        ml = [x - side_length, y + int(side_length/2)]
        mr = [x + side_length, y + int(side_length/2)]
        tm = [x, y + int(side_length/2)]
        tl = [ml[0], ml[1] + int(side_length/2)]
        tr = [mr[0], mr[1] + int(side_length/2)]
        tt = [x, y + int(1.5 * side_length)]

        gl.glBegin(gl.GL_POLYGON);
        gl.glColor3f(0, 0, 0);
        for point in [origin, ml, tl, tt, tr, mr, origin]:
            gl.glVertex2f(*point)
        gl.glEnd();

        line(*origin, *ml);
        line(*origin, *mr);
        line(*mr, *tr);
        line(*ml, *tl);
        line(*origin, *tm);
        line(*tl, *tm);
        line(*tr, *tm);
        line(*tl, *tt);
        line(*tr, *tt);
    else:
        pass

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    for z in range(len(data)):
        level = []
        for x in range(len(data[z])):
            for y in range(len(data[z][x])):
                level.append([x, y, z]);
        #     2,2
        #   1,2 2,1
        # 0,2 1,1 2,0
        #   0,1 1,0
        #     0,0
        #
        #      1 
        #    2   3 
        #  4   5   6 
        #    7   8 
        #      9 
        level.sort(key = lambda x: x[0])
        level.sort(key = lambda x: x[1])
        level.sort(key = lambda x: -sum(x))
        for point in level:
            x, y, z = point
            c_x = int(window.width/5)
            c_y = int(window.height/99) + int(z*side_length/2)

            c_x -= side_length * x
            c_y += x*int(side_length/2)

            c_x += side_length * y
            c_y += y*int(side_length/2)

            graph(c_x, c_y, data[z][x][y])
i = 0
wait = 0
def change(unused):
    global i, message, data_orig, data, wait
    if i <= len(data_orig):
        data = data_orig[0:i]
        #print(len(data))
        i += 1
        on_draw()
    else:
        wait+= 1
        if wait > 10:
            wait = 0
            i = 0
            try:
                data_orig = from_char(message[0])
            except:
                return
            message = message[1:]
pyglet.clock.schedule_interval(change, 1.0/10)
pyglet.app.run()

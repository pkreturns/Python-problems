import cairo
import math

WIDTH, HEIGHT = 800, 400
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)

context.rectangle(0, 0, WIDTH, HEIGHT)
context.set_source_rgb(0.53, 0.81, 0.98)
context.fill()

context.set_source_rgb(0.6, 0.6, 0.6)
context.move_to(100, 200)
context.curve_to(200, 100, 600, 100, 700, 200)
context.curve_to(600, 300, 200, 300, 100, 200)
context.fill_preserve()
context.set_source_rgb(0, 0, 0)
context.stroke()

context.set_source_rgb(0.5, 0.5, 0.5)
context.move_to(700, 200)
context.line_to(750, 150)
context.line_to(750, 250)
context.close_path()
context.fill_preserve()
context.stroke()

context.set_source_rgb(0.5, 0.5, 0.5)
context.move_to(730, 200)
context.line_to(780, 170)
context.line_to(780, 230)
context.close_path()
context.fill_preserve()
context.stroke()

context.move_to(350, 140)
context.line_to(400, 90)
context.line_to(450, 140)
context.close_path()
context.fill_preserve()
context.stroke()

context.move_to(350, 250)
context.line_to(400, 300)
context.line_to(450, 250)
context.close_path()
context.fill_preserve()
context.stroke()

context.set_source_rgb(0, 0, 0)
context.arc(180, 180, 15, 0, 2 * math.pi)
context.fill()

context.set_source_rgb(1, 1, 1)
context.arc(180, 180, 5, 0, 2 * math.pi)
context.fill()

context.set_source_rgb(0, 0, 0)
for i in range(5):
    context.move_to(240 + i * 10, 210 + i * 5)
    context.line_to(260 + i * 10, 210 + i * 5)
    context.stroke()

context.set_source_rgb(0, 0, 0)
context.arc(170, 200, 30, math.pi / 8, 7 * math.pi / 8)
context.stroke()

surface.write_to_png("shark.png")
print("saved as shark.png.")
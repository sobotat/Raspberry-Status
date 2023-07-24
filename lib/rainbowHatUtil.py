import rainbowhat as rh

class RainbowHatUtil:

    def show_graph(v, r, g, b):
        v *= rh.rainbow.NUM_PIXELS
        for x in range(rh.rainbow.NUM_PIXELS):
            if v < 0:
                r, g, b = 0, 0, 0
            else:
                r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
            rh.rainbow.set_pixel(x, r, g, b)
            v -= 1
        rh.rainbow.show()

    def display_message(message):
        rh.display.clear()
        rh.display.print_float(message)
        rh.display.show()

    def show_rgb(r, g, b):
        rh.lights.rgb(r, g, b)

    def clear():
        RainbowHatUtil.show_graph(0, 0, 0, 0)
        rh.display.clear()
        rh.display.show()
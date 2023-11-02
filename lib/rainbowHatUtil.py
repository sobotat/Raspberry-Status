try:
    import rainbowhat as rh
except ImportError:
    print("This script requires the rainbowhat module\nInstall with: sudo pip install rainbowhat")

class RainbowHatUtil:

    def show_graph(v, r, g, b):
        try:
            v *= rh.rainbow.NUM_PIXELS
            for x in range(rh.rainbow.NUM_PIXELS):
                if v < 0:
                    r, g, b = 0, 0, 0
                else:
                    r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
                rh.rainbow.set_pixel(x, r, g, b)
                v -= 1
            rh.rainbow.show()
        except:
            pass

    def display_message(message):
        try:
            rh.display.clear()
            rh.display.print_float(message)
            rh.display.show()
        except:
            pass

    def show_rgb(r, g, b):
        try:
            rh.lights.rgb(r, g, b)
        except:
            pass

    def clear():
        try:
            RainbowHatUtil.show_graph(0, 0, 0, 0)
            rh.display.clear()
            rh.display.show()
        except:
            pass

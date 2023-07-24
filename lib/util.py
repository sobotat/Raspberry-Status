
class Util:
    def lerp(a, b, alpha):
        return a * (1.0 - alpha) + (b * alpha)
    
    def getPercent(min, max, value):
        return (((value - min) * 100) / (max - min)) / 100
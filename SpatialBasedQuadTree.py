class spatialQaudTree2D:

    itemsAndAssociatedQuads = {}

    def __init__(self, originX, originY, length, width, storedItems, quadrantCapacity):
        self.originX = originX
        self.orginY = originY
        self.length = length
        self.width = width
        self.storedItems = storedItems

        self.quadrantCapacity = quadrantCapacity
        self.quadrant1 = None
        self.quadrant2 = None
        self.quadrant3 = None
        self.quadrant4 = None

    def add(self, item):

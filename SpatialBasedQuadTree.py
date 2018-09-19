class spatialQaudTree2D:

    itemsAndAssociatedQuads = {}

    def __init__(self, originX, originY, length, width, storedItems, quadrantCapacity):
        self.originX = originX
        self.originY = originY
        self.length = length
        self.width = width
        self.storedItems = storedItems

        self.quadrantCapacity = quadrantCapacity
        self.quadrant1 = None
        self.quadrant2 = None
        self.quadrant3 = None
        self.quadrant4 = None

    def add(self, item):
        pass

    def chooseQuadToAddTo(self, originX, originY):
        pass

    def isWithinCapacity(self):
        return len(self.storedItems) + 1 < self.quadrantCapacity

    def increaseQuadDepth(self):
        pass

    def removeItem(self, item):
        pass

    def getAllItemsWithinWidthLength(self, originX, originY, width, length):
        pass

    def getItemsFromQuadsIntersectingXY(self, originX, originY):
        pass

    def updateQuadToUpdatedItem(self, item):
        pass
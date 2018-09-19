class SpatialQaudTree2D:

    itemsAndAssociatedQuads = {}

    def __init__(self, originX, originY, length, width, storedItems, quadrantCapacity):
        self.originX = originX
        self.originY = originY
        self.length = length
        self.width = width
        self.storedItems = storedItems

        self.quadrantCapacity = quadrantCapacity
        self.quadrant0 = None
        self.quadrant1 = None
        self.quadrant2 = None
        self.quadrant3 = None

    def add(self, item):
        pass

    def chooseQuadToAddTo(self, originX, originY):

        if originX < self.originX or originX > self.originX + self.width:
            raise ValueError("originX not within quad")
        if originY < self.originY or originY > self.originY + self.length:
            raise ValueError("OriginY not within quad")

        chooseFromLeftQuads = originX > self.originX + self.width / 2
        chooseFromTopQuads = originY < self.originY + self.length / 2

        if chooseFromLeftQuads and chooseFromTopQuads:
            if self.quadrant0 == None:
                self.quadrant0 = SpatialQaudTree2D()
        elif not chooseFromLeftQuads and chooseFromTopQuads:
            quadToChoose = 1
        elif chooseFromLeftQuads and not chooseFromTopQuads:
            quadToChoose = 2
        elif not chooseFromLeftQuads and not chooseFromTopQuads:
            quadToChoose = 3


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
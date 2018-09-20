class SpatialQuadTree2D:

    itemsAndAssociatedQuads = {}

    def __init__(self, originX, originY, length, width, storedItems, quadrantCapacity):
        self.originX = originX
        self.originY = originY
        self.length = length
        self.width = width
        self.items = storedItems

        self.quadrantCapacity = quadrantCapacity
        self.quadrant0 = None
        self.quadrant1 = None
        self.quadrant2 = None
        self.quadrant3 = None

    def add(self, item):

        '''

        if what's being added isn't already contained within self
        add it to the itemsDict
        if within capacity add it to self list
        else add it to the appropriate quad
         and then iterate over my list
        '''

        pass

    def isWithinAddRange(self):

    def findItemsThatBelongInQuad(self, items, originX, originY, width, length):
        itemsBelonging = []

        for i in items:
            if i.originX >= originX and i.originX <= originX + width:
                if i.originY >= originY and i.originY <= originY + length:
                    itemsBelonging.append(i)

        return itemsBelonging

    def chooseQuadToAddTo(self, originX, originY):

        if originX < self.originX or originX > self.originX + self.width:
            raise ValueError("originX not within quad")
        if originY < self.originY or originY > self.originY + self.length:
            raise ValueError("OriginY not within quad")

        chooseFromLeftQuads = originX > self.originX + self.width / 2
        chooseFromTopQuads = originY < self.originY + self.length / 2
        quadToReturn = None
        x = self.originX
        y = self.originY
        l = self.length / 2
        w = self.width / 2
        items = []
        capacity = self.quadrantCapacity

        if chooseFromLeftQuads and chooseFromTopQuads:
            if self.quadrant0 is None:
                self.quadrant0 = SpatialQuadTree2D(x, y, l, w, items, capacity)
            quadToReturn = self.quadrant0
        elif not chooseFromLeftQuads and chooseFromTopQuads:
            if self.quadrant1 is None:
                x += w
                y += l
                self.quadrant1 = SpatialQuadTree2D(x, y, l, w, items, capacity)
            quadToReturn = self.quadrant1
        elif chooseFromLeftQuads and not chooseFromTopQuads:
            if self.quadrant2 is None:
                y -= l
                self.quadrant2 = SpatialQuadTree2D(x, y, l, w, items, capacity)
            quadToReturn = self.quadrant2
        elif not chooseFromLeftQuads and not chooseFromTopQuads:
            if self.quadrant3 is None:
                x += w
                y -= l
                self.quadrant3 = SpatialQuadTree2D(x, y, l, w, items, capacity)
            quadToReturn = self.quadrant3

        return quadToReturn

    def isWithinCapacity(self):
        return len(self.items) + 1 < self.quadrantCapacity

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
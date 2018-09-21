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
        self

    def add(self, item):

        '''

        if the item being added doesnt contain item:
            if not within capacity:
                expandCapacity
            else:
                if has child quad:
                    add to appropriate child quad based on location
                else:
                    add to itemsAssociated with this quad
        '''

        pass

    def isWithinAddRange(self, itemX, itemY, originX, originY, width, length):
        return itemX >= originX and itemX <= originX + width and itemY >= originY and itemY <= originY + length

    def findItemsThatBelongInQuad(self, items, originX, originY, width, length):
        itemsBelonging = []

        for i in items:
            if self.isWithinAddRange(i.originX, i.originY, originX, originY, width, length):
                itemsBelonging.append(i)

        return itemsBelonging

    def chooseQuadToAddTo(self, originX, originY):

        if originX < self.originX or originX > self.originX + self.width:
            raise ValueError("originX not within quad")
        if originY < self.originY or originY > self.originY + self.length:
            raise ValueError("OriginY not within quad")



    def isWithinCapacity(self, items, cap):
        return len(items) + 1 < cap

    def expandCapacity(self):
        pass

    def removeItem(self, item):
        pass

    def getAllItemsWithinWidthLength(self, originX, originY, width, length):
        pass

    def getItemsFromQuadsIntersectingXY(self, originX, originY):
        pass

    def containsItem(self, item):
        pass

    def initChildQuads(self):
        pass

    def updateQuadToUpdatedItem(self, item):
        pass
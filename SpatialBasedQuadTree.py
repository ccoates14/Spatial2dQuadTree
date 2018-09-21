class SpatialQuadTree2D:

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

        self.itemsAndAssociatedQuads = {}

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
        doesContainItem = False
        if self.areChildrenBorn():
            for c in self.getChildrenQuadAsList():
                if c.containsItem(item):
                    doesContainItem = True
        else:
            doesContainItem = item in self.itemsAndAssociatedQuads
        return doesContainItem

    def initChildQuads(self, clearParentItemsWhenDone=False):
        x = self.originX
        y = self.originY
        l = self.length
        w = self.width
        itemsThatBelongInChild = self.findItemsThatBelongInQuad()


    def updateQuadToUpdatedItem(self, item):
        pass

    def areChildrenBorn(self):
        childrenAreBorn = False
        for c in self.getChildrenQuadAsList():
            if c is not None:
                childrenAreBorn = True
                break
        return childrenAreBorn

    def getChildrenQuadAsList(self):
        return [self.quadrant0, self.quadrant1, self.quadrant2, self.quadrant3]
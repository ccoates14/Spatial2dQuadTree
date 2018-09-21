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

        self.itemsAndAssociatedQuads = storedItems

    def getItemXY(self, item):
        return item.x, item.y

    def hasNone(self, *i):
        for x in i:
            if x is None:
                return True
        return False

    def xyToItemWhenNone(self,item ,x,y):
        if self.hasNone(x, y):
            return self.getItemXY(item)
        return x, y

    def add(self, item, itemX=None, itemY=None):
        added = False
        itemX, itemY = self.xyToItemWhenNone(item, itemX, itemY)

        if not self.containsItem(item):
            if self.areChildrenBorn():
                q = self.chooseQuadByXY(originY=itemY, originX=itemX)
                q.add(item, itemX, itemY)
            else:
                if not self.isWithinCapacity(self.itemsAndAssociatedQuads, self.quadrantCapacity):
                    self.expandCapacity()
                    added = self.add(item, itemX, itemY)
                else:
                    self.itemsAndAssociatedQuads.update(item)
                    added = True

        return added

    def isWithinQuadRange(self, itemX, itemY, originX=None, originY=None, width=None,
                          length=None):
        if self.hasNone(itemX, itemY):
            raise ValueError("x and y must not be none")

        if originX is None:
            originX = self.originX
        if originY is None:
            originY = self.originY
        if width is None:
            width = self.width
        if length is None:
            length = self.length
        return itemX >= originX and itemX <= originX + width and itemY >= originY and itemY <= originY + length

    def findItemsThatBelongInQuad(self, items, originX, originY, width, length):
        itemsBelonging = {}

        for i in items.keys():
            if self.isWithinQuadRange(i.x, i.y, originX, originY, width, length):
                itemsBelonging.update(i, items[i])

        return itemsBelonging

    def chooseQuadByXY(self, originX, originY):
        q = self.quadrant0
        if originX < self.originX or originX > self.originX + self.width:
            raise ValueError("originX not within quad")
        if originY < self.originY or originY > self.originY + self.length:
            raise ValueError("OriginY not within quad")

        if self.isWithinQuadRange(originX, originY, self.quadrant1.originX, self.quadrant1.originY,
                                 self.quadrant1.width / 2, self.quadrant1.length / 2):
            q = self.quadrant1
        elif self.isWithinQuadRange(originX, originY, self.quadrant2.originX, self.quadrant2.originY,
                                 self.quadrant2.width / 2, self.quadrant2.length / 2):
            q = self.quadrant2
        elif self.isWithinQuadRange(originX, originY, self.quadrant3.originX, self.quadrant3.originY,
                                 self.quadrant3.width / 2, self.quadrant3.length / 2):
            q = self.quadrant3

        return q

    def isWithinCapacity(self, items, cap):
        return len(items) + 1 < cap

    def expandCapacity(self):
        self.initChildQuads(clearParentItemsWhenDone=True)

    def removeItem(self, item, itemX, itemY):
        didRemove = False
        itemRemoved = None

        if self.containsItem(item, itemX, itemY):
            if self.areChildrenBorn():
                q = self.chooseQuadByXY(itemX, itemY)
                didRemove, itemRemoved = q.removeItem(item, itemX, itemY)
            else:
                itemRemoved = self.itemsAndAssociatedQuads.pop(item, default=False)

                if itemRemoved == False:
                    itemRemoved = None

        return didRemove, itemRemoved

    def getAllItemsWithinWidthLength(self, originX, originY, width, length):
        corners = (originX, originY), (originX + width, originY), (originX, originY + length), \
                  (originX + width, originY + length)
        items = {}

        if self.areChildrenBorn():
            for point in corners:
                q = self.chooseQuadByXY(point[0], point[1])
                i = q.getAllItemsWithinWidthLength(point[0], point[1], q.width, q.length)

                if len(i) > 0:
                    items = {**items, **i}

        else:
            for point in corners:
                for i in self.itemsAndAssociatedQuads:
                    if self.isWithinQuadRange(i.x, i.y, point[0], point[1], width, length):
                        items.update(i, self.itemsAndAssociatedQuads[i])

        return items

    def containsItem(self, item, itemX=None, itemY=None):
        doesContainItem = False
        if self.areChildrenBorn():
            if itemX is not None and itemY is not None:
                q = self.chooseQuadByXY(itemX, itemY)
                doesContainItem = q.containsItem(item, itemX, itemY)
            else:
                for c in self.getChildrenQuadAsList():
                    if c.containsItem(item):
                        doesContainItem = True
        else:
            doesContainItem = item in self.itemsAndAssociatedQuads
        return doesContainItem

    def initChildQuads(self, clearParentItemsWhenDone=False):
        x = self.originX
        y = self.originY
        l = self.length / 2
        w = self.width / 2
        c = self.quadrantCapacity
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)

        self.quadrant0 = SpatialQuadTree2D(originX=x, originY=x, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)
        ####################################################
        #adjust args for q1 right top
        x += self.width / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.quadrant1 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)

        #####################################################################
        #this is bottom left
        x = self.originX
        y += self.length / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.quadrant2 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)
        #####################################################################
        # this is bottom right
        x = self.originX + self.width / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.quadrant3 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)

        ###################################################################
        if clearParentItemsWhenDone:
            self.itemsAndAssociatedQuads = {}


    def updateQuadToUpdatedItem(self, item, itemX, itemY):
        self.removeItem(item, itemX, itemY)
        return self.add(item, itemX, itemY)

    def areChildrenBorn(self):
        childrenAreBorn = False
        for c in self.getChildrenQuadAsList():
            if c is not None:
                childrenAreBorn = True
                break
        return childrenAreBorn

    def getChildrenQuadAsList(self):
        return [self.quadrant0, self.quadrant1, self.quadrant2, self.quadrant3]

    def runUnitTests(self, sysArgs):
        pass

    if __name__ == "__main__":
        import sys
        runUnitTests(sys.argv)
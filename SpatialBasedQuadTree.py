
class SpatialQuadTree2D:

    def __init__(self, originX, originY, length, width, storedItems, quadrantCapacity):
        self.originX = originX
        self.originY = originY
        self.length = length
        self.width = width
        self.itemsAndAssociatedQuads = {}
        self.quadrantCapacity = quadrantCapacity
        self.quadrant0 = None
        self.quadrant1 = None
        self.quadrant2 = None
        self.quadrant3 = None

        if storedItems is not None:
            for i in storedItems:
                self.add(i, i.x, i.y)

    def getItemXY(self, item):
        return item.x, item.y

    def hasNone(self, *i):
        for x in i:
            if x is None:
                return True
        return False

    def xyToItemWhenNone(self, item, x, y):
        if self.hasNone(x, y):
            return self.getItemXY(item)
        return x, y

    def add(self, item, itemX=None, itemY=None):
        added = False
        itemX, itemY = self.xyToItemWhenNone(item, itemX, itemY)

        if self.isWithinQuadRange(itemX, itemY, self.originX, self.originY, self.width, self.length) \
                and not self.containsItem(item):
            if self.areChildrenBorn():
                q = self.chooseQuadByXY(originY=itemY, originX=itemX)
                added = q.add(item, itemX, itemY)
            else:
                if not self.isWithinCapacity(self.itemsAndAssociatedQuads, self.quadrantCapacity):
                    self.expandCapacity()
                    added = self.add(item, itemX, itemY)
                else:
                    self.itemsAndAssociatedQuads[item] = self
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
                itemsBelonging[i] = items[i]

        return itemsBelonging

    def chooseQuadByXY(self, originX, originY):
        q = None

        #TODO
        #I MUST MAKE IT SO THAT WHEN IT HITS THE EDGE OF THE QUAD BUT IS STILL TECHNICALLY WITHIN THE QUAD IT DOESNT
        # ALWAYS DEFUALT TO THAT QUAD IT SHOULD MAKE IT BALANCED OR PUT IT INTO BOTH

        if self.isWithinQuadRange(originX, originY, self.quadrant0.originX, self.quadrant0.originY,
                                  self.quadrant0.width , self.quadrant0.length ):
            q = self.quadrant0
        elif self.isWithinQuadRange(originX, originY, self.quadrant1.originX, self.quadrant1.originY,
                                 self.quadrant1.width , self.quadrant1.length ):
            q = self.quadrant1
        elif self.isWithinQuadRange(originX, originY, self.quadrant2.originX, self.quadrant2.originY,
                                 self.quadrant2.width , self.quadrant2.length ):
            q = self.quadrant2
        elif self.isWithinQuadRange(originX, originY, self.quadrant3.originX, self.quadrant3.originY,
                                 self.quadrant3.width , self.quadrant3.length ):
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
                found = item in self.itemsAndAssociatedQuads

                if found:
                    didRemove = True
                    itemRemoved = item
                    del self.itemsAndAssociatedQuads[item]

            if didRemove is self.containsItem(item):
                raise AssertionError('didRemove and containsItem matched! With didRemove:' + str(didRemove)
                                     + " contains:" + str(self.containsItem(item)) + " item:{x:" + str(item.x) +
                                     " ,y:" + str(item.y) + "} Quad:{x:" + str(self.originX) + ", y:" + str(self.originY)
                                     + " , width:" + str(self.width) + " ,length:" + str(self.length) + "}")

        return didRemove, itemRemoved

    def getAllItemsWithinWidthLength(self, originX, originY, width, length):
        items = {}
        searchCorners = (originX, originY), (originX + width, originY), (originX + width, originY + length), \
                        (originX, originY + length)

        if self.areChildrenBorn():
            for child in self.getChildrenQuadAsList():
                childWithinWidthLength = False
                childCorners = (child.originX, child.originY), (child.originX + child.width, child.originY),
                (child.originX + child.width, child.originY + child.length), \
                (child.originX, child.originY + child.length)

                corners = searchCorners

                if width > child.width and length > child.length:
                    corners = childCorners

                for c in corners:

                    if self.isWithinQuadRange(c[0], c[1], originX, originY, width, length):
                        childWithinWidthLength = True
                        break

                if childWithinWidthLength:
                    i = child.getAllItemsWithinWidthLength(originX, originY, width, length)

                    if len(i) > 0:
                        items = {**items, **i}

        else:
            for i in self.itemsAndAssociatedQuads:
                if self.isWithinQuadRange(i.x, i.y, originX, originY, width, length):
                    items[i] = self

        return items

    def containsItem(self, item, itemX=None, itemY=None):

        if itemX is None or itemY is None:
            return self.containsItem(item, item.x, item.y)

        if self.areChildrenBorn():
            q = self.chooseQuadByXY(itemX, itemY)
            doesContainItem = q.containsItem(item, itemX, itemY)
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
        self.removeItemsFromItemsDict(itemsThatBelongInChild.keys())
        self.quadrant0 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)
        ####################################################
        #adjust args for q1 right top
        x += self.width / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.removeItemsFromItemsDict(itemsThatBelongInChild.keys())
        self.quadrant1 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)

        #####################################################################
        #this is bottom right
        x = self.originX + self.width / 2
        y = self.originY + self.length / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.removeItemsFromItemsDict(itemsThatBelongInChild.keys())
        self.quadrant2 = SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, quadrantCapacity=c,
                                           storedItems=itemsThatBelongInChild)
        #####################################################################
        # this is bottom left

        x = self.originX
        y = self.originY + self.length / 2
        itemsThatBelongInChild = self.findItemsThatBelongInQuad(originX=x, originY=y, length=l, width=w,
                                                                items=self.itemsAndAssociatedQuads)
        self.removeItemsFromItemsDict(itemsThatBelongInChild.keys())
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

    def removeItemsFromItemsDict(self, items):
        for i in items:
            if i in self.itemsAndAssociatedQuads:
                del self.itemsAndAssociatedQuads[i]
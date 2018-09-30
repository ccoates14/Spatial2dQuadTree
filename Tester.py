import unittest, SpatialBasedQuadTree
from SpatialBasedQuadTree import SpatialQuadTree2D
from QuadTestItem import TestItem
from random import randint

runPerformanceTests = False

class Tester(unittest.TestCase):

    def test_GetItemXY(self):
        q = getBaseSpatialTree()
        intendedX = 10
        intendedY = 10
        t = TestItem(intendedX, intendedY)
        actualX, actualY = q.getItemXY(t)
        self.assertTrue(intendedX == actualX and intendedY == actualY)

    def test_HasNone(self):
        q = getBaseSpatialTree()
        self.assertTrue(q.hasNone(14, 'ee', getBaseSpatialTree(), None))

    def test_XYToItemWhenNone(self):
        q = getBaseSpatialTree()
        t = TestItem(10,10)
        x,y = q.xyToItemWhenNone(t, 10, None)
        self.assertTrue(x == 10 and y == 10)

    def testAdd(self, amountToAdd=None):
        if amountToAdd is None:
            amountToAdd = 1000
        q = getQuadTreeWithItems()
        itemsAdded = []
        for i in range(amountToAdd):
            t = TestItem(randint(0,q.width), randint(0,q.length))
            itemsAdded.append(t)
            self.assertTrue(q.add(t))

        self.assertFalse(q.add(TestItem(10000,10000)))

        return q, itemsAdded

    def testBigAdd(self):
        global runPerformanceTests

        if not runPerformanceTests:
            return

        n = 1000 * 100
        x,y = 0,0
        len,width = n,n
        capacity = 30
        s = {}
        q = getBaseSpatialTree(x=x, y=y, l=len, w=width, c=capacity, s=s)
        for i in range(n):
            print("Now doing " + str(i))
            self.assertTrue(q.add(TestItem(randint(0, n), randint(0, n))))

        self.assertFalse(q.add(TestItem(n * 2, n * 2)))

    def testIsWithinQuadRange(self):
        q = getBaseSpatialTree()
        # 500,500, q.originX, q.originY, q.width, q.length
        self.assertTrue(q.isWithinQuadRange(500,500, q.originX, q.originY, q.width, q.length))

        self.assertTrue(q.isWithinQuadRange(0, 0, q.originX, q.originY, q.width, q.length))

        self.assertTrue(q.isWithinQuadRange(1000, 1000, q.originX, q.originY, q.width, q.length))

        self.assertTrue(q.isWithinQuadRange(500, 500))

        self.assertTrue(q.isWithinQuadRange(0, 0))

        self.assertTrue(q.isWithinQuadRange(1000, 1000))

    def testFindItemsThatBelongInQuad(self):
        q,itemsAdded = self.testAdd(1000)
        itemsToBeChecked = {i: q for i in itemsAdded}

        for i in range(100):
            itemsToBeChecked[TestItem(randint(1000,10000), randint(1000,10000))] : q

        itemsToBelongInQuad = q.findItemsThatBelongInQuad(itemsToBeChecked, q.originX, q.originY, q.width, q.length)

        for i in itemsToBeChecked:

            self.assertTrue(i in itemsToBelongInQuad)


    def testChooseQuadByXY(self):
        q0,q1,q2,q3 = getChildrenOfBaseSpatialTree()

        q = getBaseSpatialTree()

        q.quadrant0 = q0
        q.quadrant1 = q1
        q.quadrant2 = q2
        q.quadrant3 = q3

        x = 150
        y = 150
        self.assertTrue(q.chooseQuadByXY(x,y) is q0)

        x = 0
        y = 0
        self.assertTrue(q.chooseQuadByXY(x,y) is q0)

        x = 250
        y=250
        self.assertTrue(q.chooseQuadByXY(x,y) is q0)

        x = 600
        y=400
        self.assertTrue(q.chooseQuadByXY(x,y) is q1)

        x = 1000
        self.assertTrue(q.chooseQuadByXY(x,y) is q1)

        x = 750
        y = 799
        self.assertTrue(q.chooseQuadByXY(x,y) is q2)

        x = 1000
        y = 1000
        self.assertTrue(q.chooseQuadByXY(x,y) is q2)

        x=450
        y=600
        self.assertTrue(q.chooseQuadByXY(x,y) is q3)

        x=400
        self.assertTrue(q.chooseQuadByXY(x, y) is q3)

    def testIsWithinCapacity(self):
        q = getQuadTreeWithItems()
        self.assertTrue(q.isWithinCapacity([TestItem(10,10)], q.quadrantCapacity))

    def testExpandCapacity(self):
        q = getBaseSpatialTree()

        q.expandCapacity()
        self.assertTrue(q.quadrant0 is not None)
        self.assertTrue(q.quadrant1 is not None)
        self.assertTrue(q.quadrant2 is not None)
        self.assertTrue(q.quadrant3 is not None)

    def testRemoveItem(self, amountToRemove=None):
        if amountToRemove is None:
            amountToRemove = 100

        q, itemsAdded = self.testAdd(amountToRemove * 10)
        itemsRemoved = []

        for i in itemsAdded:
            if randint(0,1):
                itemsRemoved.append(i)
                didRemove, itemRemoved = q.removeItem(i, i.x, i.y)
                self.assertTrue(didRemove)
                self.assertTrue(itemRemoved is i)

        for i in itemsRemoved:
            self.assertFalse(q.containsItem(i, i.x, i.y))
            self.assertFalse(q.containsItem(i))
            didRemove, itemRemoved = q.removeItem(i, i.x, i.y)
            self.assertFalse(didRemove)
            self.assertTrue(itemRemoved is None)
            self.assertFalse(self.quadContainsItem(q, i))

    '''
    Forcibly looks at the quad and all its children quads to see if
    item is in it
    '''
    def quadContainsItem(self, q, item):
        if q.quadrant0 is not None:
            if self.quadContainsItem(q.quadrant0, item):
                return True
        if q.quadrant1 is not None:
            if self.quadContainsItem(q.quadrant1, item):
                return True
        if q.quadrant2 is not None:
            if self.quadContainsItem(q.quadrant2, item):
                return True
        if q.quadrant3 is not None:
            if self.quadContainsItem(q.quadrant3, item):
                return True

        if q.itemsAndAssociatedQuads is None:
            return False

        if item in q.itemsAndAssociatedQuads:
            print("item xy: " + str(item.x) + " " + str(item.y) + " in Q: width: " + str(q.width) + " len: " +
                  str(q.length) +
                  " x: " + str(q.originX) + " y: " + str(q.originY))

        return item in q.itemsAndAssociatedQuads

    def testGetAllItemsWithinWidthLength(self):
        q = getBaseSpatialTree()
        areaX = 450
        areaY = 600
        areaWidth = 100
        areaLength = 100

        itemsNotToBeIncluded = []
        itemsToBeIncluded = []

        def getNonAreaX():
            if randint(0,1):
                return randint(0, 449)# X before area to look at
            return randint(551, q.width)

        def getNonAreaY():
            if randint(0,1):
                return randint(0, 599)# Y before area Y
            return randint(700, q.length)

        def getAreaX():
            return randint(areaX, areaX + areaWidth)

        def getAreaY():
            return randint(areaY, areaY + areaLength)

        for i in range(1000):
            itemsNotToBeIncluded.append(TestItem(getNonAreaX(), getNonAreaY()))

        for i in range(1000):
            itemsToBeIncluded.append(TestItem(getAreaX(), getAreaY()))

        for i in itemsToBeIncluded:
            q.add(i)

        for i in itemsNotToBeIncluded:
            q.add(i)

        itemsWithinWidthLength = q.getAllItemsWithinWidthLength(areaX, areaY, areaWidth, areaLength)

        for i in itemsToBeIncluded:
            if i not in itemsWithinWidthLength:
                print("X:"+str(i.x)+" y:"+str(i.y))
            self.assertTrue(i in itemsWithinWidthLength)

        for i in itemsNotToBeIncluded:
            self.assertFalse(i in itemsWithinWidthLength)

    def testContainsItem(self):
        q, itemsAdded = self.testAdd()
        itemsNotAdded = [TestItem(randint(0, q.width), randint(0,q.length)) for i in range(100)]

        for i in itemsAdded:
            self.assertTrue(q.containsItem(i))

        for i in itemsNotAdded:
            self.assertFalse(q.containsItem(i))

    def testInitChildQuads(self):
        q = getBaseSpatialTree()
        q.itemsAndAssociatedQuads = {TestItem(10,10) : q,
                                     TestItem(100,100) : q}
        q.initChildQuads(clearParentItemsWhenDone=True)

        self.assertTrue(len(q.itemsAndAssociatedQuads) == 0)

        #TEST q0
        q0 = q.quadrant0
        self.assertTrue(q0 is not None)
        self.assertTrue(q0.originX == q.originX)
        self.assertTrue(q0.originY == q.originY)
        self.assertTrue(q0.width == q.width / 2)
        self.assertTrue(q0.length == q.length / 2)

        #
        q1 = q.quadrant1
        self.assertTrue(q1 is not None)
        self.assertTrue(q1.originX == q.originX + q.width / 2)
        self.assertTrue(q1.originY == q.originY)
        self.assertTrue(q1.width == q.width / 2)
        self.assertTrue(q1.length == q.length / 2)

        #
        q2 = q.quadrant2
        self.assertTrue(q2 is not None)
        self.assertTrue(q2.originX == q.originX + q.width / 2)
        self.assertTrue(q2.originY == q.originY + q.length / 2)
        self.assertTrue(q2.width == q.width / 2)
        self.assertTrue(q2.length == q.length / 2)

        #
        q3 = q.quadrant3
        self.assertTrue(q3 is not None)
        self.assertTrue(q3.originX == q.originX)
        self.assertTrue(q3.originY == q.originY + q.length / 2)
        self.assertTrue(q3.width == q.width / 2)
        self.assertTrue(q3.length == q.length / 2)

    def testUpdateQuadToUpdatedItem(self):
        pass

    def testAreChildrenBorn(self):
        q = getBaseSpatialTree()
        q.quadrant0 = getBaseSpatialTree()

        self.assertTrue(q.areChildrenBorn())

        q.quadrant0 = q.quadrant1 = q.quadrant2 = q.quadrant3 = getBaseSpatialTree()

        self.assertTrue(q.areChildrenBorn())

    def testGetChildrenQuadAsList(self):
        q = getQuadTreeWithItems()

        for i in range(1000):
            q.add(TestItem(randint(0, i), randint(0, i)))

        q0,q1,q2,q3 = q.getChildrenQuadAsList()

        self.assertTrue(q0 is not None)
        self.assertTrue(q1 is not None)
        self.assertTrue(q2 is not None)
        self.assertTrue(q3 is not None)

        self.assertTrue(type(q0) is SpatialQuadTree2D)
        self.assertTrue(type(q1) is SpatialQuadTree2D)
        self.assertTrue(type(q2) is SpatialQuadTree2D)
        self.assertTrue(type(q3) is SpatialQuadTree2D)




print("Starting tests")

def getBaseSpatialTree(x=None,y=None,w=None,l=None,s=None,c=None):
    if y is None:
        y = 0
    if x is None:
        x=0
    if l is None:
        l = 1000
    if w is None:
        w = 1000
    if s is None:
        s = {}
    if c is None:
        c = 25

    quad = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                  quadrantCapacity=c)
    return quad


def getChildrenOfBaseSpatialTree():
    baseTree = getBaseSpatialTree()

    x = baseTree.originX
    y = baseTree.originY
    l = baseTree.length / 2
    w = baseTree.width / 2
    s = {}
    c = baseTree.quadrantCapacity
    q0 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                  quadrantCapacity=c)

    l = baseTree.length / 2
    w = baseTree.width / 2
    x = baseTree.originX + w
    y = baseTree.originY
    s = {}
    c = baseTree.quadrantCapacity
    q1 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                quadrantCapacity=c)

    l = baseTree.length / 2
    w = baseTree.width / 2
    x = baseTree.originX + w
    y = baseTree.originY + l
    s = {}
    c = baseTree.quadrantCapacity
    q2 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                quadrantCapacity=c)

    l = baseTree.length / 2
    w = baseTree.width / 2
    x = baseTree.originX
    y = baseTree.originY + l
    s = {}
    c = baseTree.quadrantCapacity
    q3 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                quadrantCapacity=c)

    return q0,q1,q2,q3


def getQuadTreeWithItems():
    x=0
    y = 0
    l = 1000
    w = 1000
    s = [TestItem(10,10)]
    c = 25
    quad = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                  quadrantCapacity=c)

    return quad

if __name__ == "__main__":
    unittest.main()
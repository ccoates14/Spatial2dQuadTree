import unittest, SpatialBasedQuadTree
from QuadTestItem import TestItem
from random import randint
class Tester(unittest.TestCase):

    def test_GetItemXY(self):
        q = getBaseSpatialTree()
        intendedX = 10
        intendedY = 10
        t = TestItem(intendedX, intendedY)
        actualX, actualY = q.getItemXY(t)
        self.assertTrue(intendedX is actualX and intendedY is actualY)

    def test_HasNone(self):
        q = getBaseSpatialTree()
        self.assertTrue(q.hasNone(14, 'ee', getBaseSpatialTree(), None))

    def test_XYToItemWhenNone(self):
        q = getBaseSpatialTree()
        t = TestItem(10,10)
        x,y = q.xyToItemWhenNone(t, 10, None)
        self.assertTrue(x is 10 and y is 10)

    def testAdd(self):
        q = getQuadTreeWithItems()

        for i in range(1000):
            q.add(TestItem(randint(0,i), randint(0,i)))

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
        pass

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

        x = 500
        self.assertTrue(q.chooseQuadByXY(x,y) is q1)

        x = 750
        y = 500
        self.assertTrue(q.chooseQuadByXY(x,y) is q2)

        x = 1000
        y = 1000
        self.assertTrue(q.chooseQuadByXY(x,y) is q2)

        x=500
        y=600
        self.assertTrue(q.chooseQuadByXY(x,y) is q3)

    def testIsWithinCapacity(self):
        q = getQuadTreeWithItems()
        self.assertTrue(q.isWithinCapacity([TestItem(10,10)], q.quadrantCapacity))

    def testExpandCapacity(self):
        pass

    def testRemoveItem(self):
        pass

    def testGetAllItemsWithinWidthLength(self):
        pass

    def testContainsItem(self):
        pass

    def testInitChildQuads(self):
        pass

    def testUpdateQuadToUpdatedItem(self):
        pass

    def testAreChildrenBorn(self):
        pass

    def testGetChildrenQuadAsList(self):
        pass


print("Starting tests")

def getBaseSpatialTree():
    y = 0
    x=0
    l = 1000
    w = 1000
    s = {}
    c = 25
    quad = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                  quadrantCapacity=c)
    return quad


def getChildrenOfBaseSpatialTree():
    y = 0
    x=0
    l = 500
    w = 500
    s = {}
    c = 25
    q0 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                  quadrantCapacity=c)

    y = 0
    x=250
    l = 500
    w = 500
    s = {}
    c = 25
    q1 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                quadrantCapacity=c)

    y = 250
    x=0
    l = 500
    w = 500
    s = {}
    c = 25
    q2 = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s,
                                                quadrantCapacity=c)

    x=250
    y = 250
    l = 500
    w = 500
    s = {}
    c = 25
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
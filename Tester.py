import unittest, SpatialBasedQuadTree


class Tester(unittest.TestCase):

    def test_GetItemXY(self):
        print("The quad: " + str(quad))
        pass

    def test_HasNone(self):
        pass

    def test_XYToItemWhenNone(self):
        pass

    def testAdd(self):
        pass

    def testIsWithinQuadRange(self):
        pass

    def testFindItemsThatBelongInQuad(self):
        pass

    def testChooseQuadByXY(self):
        pass

    def testIsWithinCapacity(self):
        pass

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
x = 0
y = 0
l = 1000
w = 1000
s = {}
c = 25
quad = SpatialBasedQuadTree.SpatialQuadTree2D(originX=x, originY=y, length=l, width=w, storedItems=s, quadrantCapacity=c)

if __name__ == "__main__":
    unittest.main()
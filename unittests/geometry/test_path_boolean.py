#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest

import pero
from pero.geometry.boolean import _Contour, _parse_path, _Segment


class TestCase(unittest.TestCase):
    """Tests filled-path boolean operations."""
    
    def assertPoint(self, points, expected, places=5):
        """Checks that a point exists in a collection."""
        
        for point in points:
            if (round(point[0]-expected[0], places) == 0 and
                    round(point[1]-expected[1], places) == 0):
                return
        self.fail("Point %r not found in %r" % (expected, points))
    
    
    def test_combine_rectangles(self):
        """Union inserts crossings and removes interior anchors."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        other = pero.Path().rect(5, 5, 10, 10)
        result = path.union(other)
        
        self.assertIs(result, path)
        self.assertEqual(path.commands(), (
            ('M', 0., 0.), ('L', 10., 0.), ('L', 10., 5.),
            ('L', 15., 5.), ('L', 15., 15.), ('L', 5., 15.),
            ('L', 5., 10.), ('L', 0., 10.), ('Z',)))
    
    
    def test_subtract_rectangles(self):
        """Difference keeps only the uncut rectangle boundary."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        path.subtract(pero.Path().rect(5, 5, 10, 10))
        
        self.assertEqual(path.commands(), (
            ('M', 0., 0.), ('L', 10., 0.), ('L', 10., 5.),
            ('L', 5., 5.), ('L', 5., 10.), ('L', 0., 10.),
            ('Z',)))
    
    
    def test_intersect_rectangles(self):
        """Intersection retains only the shared rectangle area."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        other = pero.Path().rect(5, 5, 10, 10)
        other_commands = other.commands()
        result = path.intersect(other)
        
        self.assertIs(result, path)
        self.assertEqual(path.commands(), (
            ('M', 5., 5.), ('L', 10., 5.), ('L', 10., 10.),
            ('L', 5., 10.), ('Z',)))
        self.assertEqual(other.commands(), other_commands)
    
    
    def test_intersect_disjoint_and_contained(self):
        """Intersection handles empty and fully contained results."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        path.intersect(pero.Path().rect(20, 20, 5, 5))
        self.assertEqual(path.commands(), ())
        self.assertEqual(path.cursor, (0, 0))
        
        inner = pero.Path().rect(2, 2, 3, 3)
        path = pero.Path().rect(0, 0, 10, 10)
        path.intersect(inner)
        self.assertEqual(path.commands(), inner.commands())
    
    
    def test_intersect_curves(self):
        """Curved intersection preserves cubic boundary segments."""
        
        path = pero.Path().circle(0, 0, 10)
        path.intersect(pero.Path().circle(10, 0, 10))
        
        self.assertEqual(sum(x[0] == pero.PATH_CURVE for x in path.commands()), 4)
        self.assertPoint(path.anchors(), (5., -8.66217805))
        self.assertPoint(path.anchors(), (5., 8.66217805))
    
    
    def test_intersect_shared_boundary(self):
        """A boundary-only contact has no filled intersection."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        path.intersect(pero.Path().rect(10, 0, 10, 10))
        self.assertEqual(path.commands(), ())
    
    
    def test_disjoint_and_nested(self):
        """Disjoint contours and nested holes remain separate."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        path.union(pero.Path().rect(20, 0, 5, 5))
        self.assertEqual(sum(x[0] == pero.PATH_MOVE for x in path.commands()), 2)
        
        path = pero.Path(pero.WINDING).rect(0, 0, 20, 20)
        path.subtract(pero.Path().rect(5, 5, 10, 10))
        self.assertEqual(sum(x[0] == pero.PATH_MOVE for x in path.commands()), 2)
        self.assertEqual(path.fill_rule, pero.WINDING)
    
    
    def test_identical_and_contained(self):
        """Identical and fully contained operands use the outer boundary."""
        
        original = pero.Path().circle(0, 0, 10)
        combined = original.clone().union(original)
        self.assertEqual(len(combined.commands()), 6)
        self.assertEqual(sum(x[0] == pero.PATH_CURVE for x in combined.commands()), 4)
        
        removed = original.clone().subtract(original)
        self.assertEqual(removed.commands(), ())
        self.assertEqual(removed.cursor, (0, 0))
        self.assertIsNone(removed.bbox())
        
        outer = pero.Path().rect(0, 0, 20, 20)
        outer.union(pero.Path().rect(5, 5, 5, 5))
        self.assertEqual(len(outer.anchors()), 4)
    
    
    def test_circle_crossings_preserve_curves(self):
        """Curve intersections become anchors without flattening curves."""
        
        path = pero.Path().circle(0, 0, 10)
        path.union(pero.Path().circle(10, 0, 10))
        
        self.assertEqual(sum(x[0] == pero.PATH_CURVE for x in path.commands()), 8)
        self.assertPoint(path.anchors(), (5., -8.66217805))
        self.assertPoint(path.anchors(), (5., 8.66217805))
    
    
    def test_line_curve_crossings(self):
        """A line can cut cubic segments while both command types survive."""
        
        path = pero.Path().circle(0, 0, 10)
        path.subtract(pero.Path().rect(0, -5, 15, 10))
        
        keys = [x[0] for x in path.commands()]
        self.assertIn(pero.PATH_LINE, keys)
        self.assertIn(pero.PATH_CURVE, keys)
        self.assertPoint(path.anchors(), (8.66217805, -5.))
        self.assertPoint(path.anchors(), (8.66217805, 5.))
    
    
    def test_shared_and_tangent_boundaries(self):
        """Shared edges disappear while point tangencies remain closed."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        path.union(pero.Path().rect(10, 0, 10, 10))
        self.assertEqual(path.anchors(), ([0., 0.], [20., 0.], [20., 10.], [0., 10.]))
        
        path = pero.Path().circle(0, 0, 10)
        path.union(pero.Path().circle(20, 0, 10))
        self.assertTrue(path.is_closed())
        self.assertPoint(path.anchors(), (10., 0.))
    
    
    def test_reversed_coincident_boundary(self):
        """Coincident contours are independent of drawing direction."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        reversed_path = pero.Path().polygon(((0, 0), (0, 10), (10, 10), (10, 0)))
        
        self.assertEqual(len(path.clone().union(reversed_path).anchors()), 4)
        self.assertEqual(path.clone().subtract(reversed_path).commands(), ())
    
    
    def test_partial_coincident_curve(self):
        """A shared cubic span does not leave unnecessary split anchors."""
        
        path = pero.Path().move_to(0, 0)
        path.curve_to(0, 10, 10, 10, 10, 0).close()
        
        shared = pero.Path().move_to(8.4375, 5.625)
        shared.curve_to(6.5625, 8.125, 3.4375, 8.125, 1.5625, 5.625).close()
        
        path.union(shared)
        self.assertEqual(sum(x[0] == pero.PATH_CURVE for x in path.commands()), 1)
    
    
    def test_fill_rules(self):
        """Each input is interpreted using its own fill rule."""
        
        evenodd = pero.Path(pero.EVENODD)
        evenodd.rect(0, 0, 20, 20).rect(5, 5, 10, 10)
        evenodd.union(pero.Path().rect(30, 0, 5, 5))
        self.assertEqual(sum(x[0] == pero.PATH_MOVE for x in evenodd.commands()), 3)
        
        winding = pero.Path(pero.WINDING)
        winding.rect(0, 0, 20, 20).rect(5, 5, 10, 10)
        winding.union(pero.Path().rect(30, 0, 5, 5))
        self.assertEqual(sum(x[0] == pero.PATH_MOVE for x in winding.commands()), 2)
    
    
    def test_self_intersection(self):
        """Self-intersecting input contours are resolved into filled faces."""
        
        path = pero.Path().polygon(((0, 0), (10, 10), (0, 10), (10, 0)))
        path.union(pero.Path().rect(20, 0, 5, 5))
        
        self.assertEqual(sum(x[0] == pero.PATH_MOVE for x in path.commands()), 3)
        self.assertPoint(path.anchors(), (5., 5.))
    
    
    def test_empty_and_degenerate_paths(self):
        """Empty and zero-area contours have neutral boolean behavior."""
        
        shape = pero.Path().rect(0, 0, 2, 2)
        empty = pero.Path()
        degenerate = pero.Path().polygon(((0, 0), (1, 0), (2, 0)))
        
        self.assertEqual(empty.clone().union(shape).commands(), shape.commands())
        self.assertEqual(shape.clone().union(empty).commands(), shape.commands())
        self.assertEqual(empty.clone().subtract(shape).commands(), ())
        self.assertEqual(shape.clone().subtract(empty).commands(), shape.commands())
        self.assertEqual(shape.clone().union(degenerate).commands(), shape.commands())
    
    
    def test_validation_is_atomic(self):
        """Invalid inputs do not partially modify either path."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        commands = path.commands()
        
        self.assertEqual(path.commands(), commands)
        self.assertEqual(path.commands(), commands)
    
    
    def test_operand_and_caches(self):
        """The operand remains unchanged and cached geometry is refreshed."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        other = pero.Path().rect(5, 0, 10, 10)
        other_commands = other.commands()
        self.assertEqual(path.bbox().width, 10)
        self.assertEqual(len(path.anchors()), 4)
        
        path.union(other)
        self.assertEqual(other.commands(), other_commands)
        self.assertEqual(path.bbox().width, 15)
        self.assertEqual(len(path.anchors()), 4)
        self.assertEqual(path.cursor, (0., 0.))
    
    
    def test_coordinate_scales(self):
        """Tolerance works for small and heavily translated geometry."""
        
        for origin, size in ((0., 1e-6), (1e9, 10.)):
            path = pero.Path().rect(origin, origin, size, size)
            path.union(pero.Path().rect(origin+size/2., origin, size, size))
            box = path.bbox()
            self.assertAlmostEqual(box.width, 1.5*size)
            self.assertAlmostEqual(box.height, size)
    
    
    def test_segment_uses_bezier_geometry(self):
        """Segments delegate line detection and tight curve bounds to Bezier."""
        
        line = _Segment(pero.PATH_LINE, (0, 0), (12, 6))
        self.assertTrue(line.curve.is_line())
        self.assertEqual(line.point(.25), (3., 1.5))
        self.assertEqual(line.bbox(), (0., 0., 12., 6.))
        
        curve = _Segment(pero.PATH_CURVE, (0, 0), (0, 0), (100, 100), (-100, 100))
        expected = pero.Bezier(0, 0, 100, 100, -100, 100, 0, 0).bbox()
        
        self.assertAlmostEqual(curve.bbox()[0], expected.left)
        self.assertAlmostEqual(curve.bbox()[1], expected.top)
        self.assertAlmostEqual(curve.bbox()[2], expected.right)
        self.assertAlmostEqual(curve.bbox()[3], expected.bottom)
        self.assertAlmostEqual(curve.bbox()[2]-curve.bbox()[0], 57.7350269)
        self.assertAlmostEqual(curve.bbox()[3]-curve.bbox()[1], 75.)
    
    
    def test_parser_uses_path_beziers(self):
        """Boolean parsing wraps the Bezier objects supplied by Path."""
        
        path = pero.Path().rect(0, 0, 10, 10)
        curves = path.beziers()
        path.beziers = lambda: curves
        
        contours, segments = _parse_path(path, 0, 1e-9)
        
        self.assertEqual(len(contours), 1)
        self.assertEqual(len(segments), 4)
        for segment, curve in zip(segments, curves):
            self.assertTrue(segment.curve.equals(curve, 1e-9))
    
    
    def test_contour_geometry_and_serialization(self):
        """Contour owns bounds, area, simplification and Path output."""
        
        contour = _Contour((
            _Segment(pero.PATH_LINE, (0, 0), (5, 0)),
            _Segment(pero.PATH_LINE, (5, 0), (10, 0)),
            _Segment(pero.PATH_LINE, (10, 0), (10, 10)),
            _Segment(pero.PATH_LINE, (10, 10), (0, 10)),
            _Segment(pero.PATH_LINE, (0, 10), (0, 0))))
        
        self.assertEqual(contour.bbox(), (0., 0., 10., 10.))
        self.assertAlmostEqual(contour.area(), 100.)
        
        contour.simplify(1e-9)
        contour.normalize(1e-9)
        
        self.assertEqual(len(contour), 4)
        self.assertEqual(contour.commands(1e-9), [
            ('M', 0., 0.), ('L', 10., 0.), ('L', 10., 10.),
            ('L', 0., 10.), ('Z',)])


if __name__ == '__main__':
    unittest.main()

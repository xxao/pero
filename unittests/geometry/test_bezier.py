#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
from unittest import mock

import pero


class TestCase(unittest.TestCase):
    """Tests cubic Bezier geometry."""
    
    def test_monotonic_line(self):
        """A collinear monotonic cubic has straight-segment geometry."""
        
        curve = pero.Bezier(0, 0, 0, 0, 10, 0, 10, 0)
        
        self.assertTrue(curve.is_line())
        self.assertTrue(curve.is_simple())
        self.assertEqual(curve.bbox().rect, (0., 0., 10., 0.))
        self.assertEqual(curve.extremes(), ((), ()))
        self.assertFalse(curve.inflections())
        self.assertEqual(curve.reduced(), (curve,))
    
    
    def test_line_parameterization(self):
        """Straight cubics retain their original non-linear parameterization."""
        
        curve = pero.Bezier(0, 0, 0, 0, 10, 0, 10, 0)
        
        self.assertTrue(curve.is_line())
        self.assertFalse(curve.is_linear())
        self.assertEqual(curve.point(.25), (1.5625, 0.))
        self.assertEqual(curve.derivative(.25), (11.25, 0.))
        
        line = pero.Bezier.from_line(0, 0, 10, 0)
        self.assertTrue(line.is_line())
        self.assertTrue(line.is_linear())
    
    
    def test_backtracking_curve(self):
        """Collinear controls outside the chord are not a straight segment."""
        
        curve = pero.Bezier(0, 0, 20, 0, 20, 0, 10, 0)
        
        self.assertFalse(curve.is_line())
        self.assertGreater(curve.bbox().right, 10.)
    
    
    def test_nearly_straight_curve(self):
        """Visible curvature is not absorbed by line-classification tolerance."""
        
        curve = pero.Bezier(0, 0, 3, .01, 7, .01, 10, 0)
        self.assertFalse(curve.is_line())
    
    
    def test_extremes(self):
        """Extremes contain unique roots of the first derivative only."""
        
        curve = pero.Bezier(0, 0, 0, 1, 1, 1, 1, 0)
        self.assertEqual(curve.extremes(), ((0., 1.), (.5,)))
        
        duplicate = pero.Bezier(0, 0, 0, 1, 0, 1, 1, 0)
        self.assertEqual(duplicate.extremes(), ((0.,), (.5,)))
    
    
    def test_extremes_cache_is_immutable(self):
        """Callers cannot corrupt cached extremes or subsequent bounds."""
        
        curve = pero.Bezier(0, 0, 1./3, 10, 2./3, 10, 1, 0)
        
        self.assertEqual(curve.extremes(), ((), (.5,)))
        self.assertEqual(curve.bbox().rect, (0., 0., 1., 7.5))
    
    
    def test_inflections_are_scale_invariant(self):
        """Equivalent curves retain their inflections at every scale."""
        
        for scale in (1e-6, 1e-3, 1e-2, 1., 1e6):
            
            curve = pero.Bezier(0, 0, 0, scale, scale, -scale, scale, 0)
            
            self.assertEqual(len(curve.inflections()), 1)
            self.assertAlmostEqual(curve.inflections()[0], .5)
    
    
    def test_normalized_vectors_are_scale_invariant(self):
        """Tangent and normal normalization avoid overflow and underflow."""
        
        for scale in (1e-200, 1., 1e200):
            
            curve = pero.Bezier.from_line(0, 0, scale, 5.*scale)
            tangent = curve.tangent(.5)
            normal = curve.normal(.5)
            
            self.assertAlmostEqual(tangent[0], 1./26.**.5)
            self.assertAlmostEqual(tangent[1], 5./26.**.5)
            self.assertAlmostEqual(normal[0], -5./26.**.5)
            self.assertAlmostEqual(normal[1], 1./26.**.5)
    
    
    def test_degenerate_line(self):
        """A zero-length chord is linear only if every point coincides."""
        
        point = pero.Bezier(1, 1, 1, 1, 1, 1, 1, 1)
        loop = pero.Bezier(0, 0, 1, 0, -1, 0, 0, 0)
        
        self.assertTrue(point.is_line())
        self.assertFalse(loop.is_line())
    
    
    def test_reduce_preserves_full_parameter_range(self):
        """Reduction covers the entire curve without gaps or truncation."""
        
        curve = pero.Bezier(0, -10, 5.5228475, -10, 10, -5.5228475, 10, 0)
        segments = curve.reduced()
        
        self.assertEqual(segments[0]._t1, 0.)
        self.assertEqual(segments[-1]._t2, 1.)
        
        for first, second in zip(segments[:-1], segments[1:]):
            self.assertAlmostEqual(first._t2, second._t1)
    
    
    def test_reduce_resets_sliced_parameter_range(self):
        """Reduced slices use parameters local to the sliced curve."""
        
        curve = pero.Bezier(0, 0, 0, 10, 10, 10, 10, 0)
        sliced = curve.slice(.1, .2)
        segments = sliced.reduced()
        
        self.assertTrue(sliced.is_simple())
        self.assertEqual(segments[0]._t1, 0.)
        self.assertEqual(segments[-1]._t2, 1.)
        self.assertEqual(segments[0].points, sliced.points)
        
        loop = pero.Bezier(0, 0, 10, 10, -10, 10, 2, 0)
        sliced = loop.slice(.1, .9)
        segments = sliced.reduced()
        
        self.assertFalse(sliced.is_simple())
        self.assertEqual(segments[0]._t1, 0.)
        self.assertEqual(segments[-1]._t2, 1.)
    
    
    def test_reduce_merges_nearby_extremes(self):
        """Near-identical extrema do not create microscopic segments."""
        
        def controls(root, other):
            a = root*other
            b = a-(root+other)/2.
            c = 1.-root-other+a
            return 0., a/3., (a+b)/3., (a+b+c)/3.
        
        x = controls(.5, 2.)
        y = controls(.5+5e-10, -2.)
        curve = pero.Bezier(
            x[0], y[0], x[1], y[1],
            x[2], y[2], x[3], y[3])
        segments = curve.reduced()
        boundaries = [x._t1 for x in segments] + [segments[-1]._t2]
        nearby = [x for x in boundaries if abs(x-.5) <= 1e-9]
        
        self.assertEqual(len(nearby), 1)
        self.assertTrue(all(x.is_simple() for x in segments))
    
    
    def test_curve_intersections(self):
        """Reduced curves retain curve/curve and self intersections."""
        
        first = pero.Bezier(0, -10, 5.5228475, -10, 10, -5.5228475, 10, 0)
        second = pero.Bezier(0, 0, 0, -5.5228475, 4.4771525, -10, 10, -10)
        intersections = first.intersects(second, 1e-5)
        
        self.assertTrue(intersections)
        self.assertAlmostEqual(intersections[0][0], .3298001, places=5)
        self.assertAlmostEqual(intersections[0][1], .6701999, places=5)
        
        loop = pero.Bezier(0, 0, 10, 10, -10, 10, 2, 0)
        intersections = loop.intersects(None, 1e-5)
        
        self.assertTrue(intersections)
        self.assertAlmostEqual(intersections[0][0], .0333717, places=5)
        self.assertAlmostEqual(intersections[0][1], .9666283, places=5)
    
    
    def test_intersects_dispatches_straight_curves(self):
        """Public intersections handle lines and their true parameterization."""
        
        horizontal = pero.Bezier.from_line(0, 0, 10, 0)
        vertical = pero.Bezier.from_line(5, -5, 5, 5)
        intersections = horizontal.intersects(vertical)
        
        self.assertEqual(intersections, ((.5, .5),))
        
        nonlinear = pero.Bezier(0, 0, 0, 0, 10, 0, 10, 0)
        vertical = pero.Bezier.from_line(1.5625, -1, 1.5625, 1)
        intersections = nonlinear.intersects(vertical, 1e-9)
        
        self.assertAlmostEqual(intersections[0][0], .25)
        self.assertAlmostEqual(intersections[0][1], .5)
    
    
    def test_intersects_coincident_spans(self):
        """Public intersections return endpoints of coincident curve spans."""
        
        curve = pero.Bezier(0, 0, 0, 10, 10, 10, 10, 0)
        shared = curve.slice(.25, .75)
        
        intersections = curve.intersects(shared, 1e-9)
        self.assertAlmostEqual(intersections[0][0], .25)
        self.assertEqual(intersections[0][1], 0.)
        self.assertAlmostEqual(intersections[1][0], .75)
        self.assertEqual(intersections[1][1], 1.)
        
        intersections = curve.intersects(shared.reversed(), 1e-9)
        self.assertAlmostEqual(intersections[0][0], .25)
        self.assertEqual(intersections[0][1], 1.)
        self.assertAlmostEqual(intersections[1][0], .75)
        self.assertEqual(intersections[1][1], 0.)
    
    
    def test_degenerate_cut_line(self):
        """A point does not define an infinite cutting line."""
        
        curve = pero.Bezier.from_line(0, 0, 2, 2)
        
        self.assertEqual(curve.cuts(1, 1, 1, 1), ())
        self.assertEqual(curve.cuts(0, 1, 2, 1), (.5,))
    
    
    def test_cut_roots_are_numerically_stable(self):
        """Curve-line roots survive extreme scales and remain distinct."""
        
        curve = pero.Bezier(
            0, 1e308,
            1, 1e308,
            2, -1e308,
            3, -1e308)
        roots = curve.ycuts(0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], .5)
        
        r1, r2 = .5, .50000002
        a = 1.
        b = -(r1+r2)
        c = r1*r2
        values = (
            c,
            c+b/3.,
            c+2.*b/3.+a/3.,
            c+b+a)
        curve = pero.Bezier(
            0, values[0],
            1./3., values[1],
            2./3., values[2],
            1, values[3])
        roots = curve.ycuts(0)
        
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], r1, delta=3e-9)
        self.assertAlmostEqual(roots[1], r2, delta=3e-9)
    
    
    def test_cut_roots_represent_coincident_curve(self):
        """Coincident curve-line roots are represented by both endpoints."""
        
        curve = pero.Bezier(0, 0, 20, 0, -10, 0, 10, 0)
        
        self.assertEqual(curve.cuts(-1, 0, 1, 0), (0., 1.))


if __name__ == '__main__':
    unittest.main()

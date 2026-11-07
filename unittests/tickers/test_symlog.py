#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for symmetric logarithmic ticker."""
    
    
    def test_major_ticks(self):
        """Tests whether major ticks are generated correctly."""
        
        ticker = pero.SymlogTicker()
        
        ticker(start=-100, end=100)
        self.assertEqual(ticker.major_ticks(), (-100, -10, -1, 0, 1, 10, 100))
        
        ticker(start=100, end=-100)
        self.assertEqual(ticker.major_ticks(), (100, 10, 1, 0, -1, -10, -100))
        
        ticker(start=1, end=100)
        self.assertEqual(ticker.major_ticks(), (1, 10, 100))
        
        ticker(start=-100, end=-1)
        self.assertEqual(ticker.major_ticks(), (-100, -10, -1))
        
        ticker(start=-1, end=100)
        self.assertEqual(ticker.major_ticks(), (-1, 0, 1, 10, 100))
    
    
    def test_minor_ticks(self):
        """Tests whether linear and logarithmic minor ticks are generated."""
        
        ticker = pero.SymlogTicker(start=-10, end=10)
        
        ticks = tuple(round(x, 10) for x in ticker.minor_ticks())
        model = (
            -10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
            -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        
        self.assertEqual(ticks, model)
        
        ticker(start=10, end=-10)
        ticks = tuple(round(x, 10) for x in ticker.minor_ticks())
        
        self.assertEqual(ticks, model[::-1])
    
    
    def test_linear_region(self):
        """Tests whether linear ranges use the same ticks as linear ticker."""
        
        ticker = pero.SymlogTicker(start=-0.5, end=0.5)
        model = pero.LinTicker(start=-0.5, end=0.5)
        
        self.assertEqual(ticker.major_ticks(), model.major_ticks())
        self.assertEqual(ticker.minor_ticks(), model.minor_ticks())
        self.assertEqual(ticker.labels(), model.labels())
        self.assertEqual(ticker.beautify(-0.5, 0.5), model.beautify(-0.5, 0.5))
        
        ticker(start=0.5, end=-0.5)
        
        self.assertEqual(ticker.major_ticks(), model.major_ticks()[::-1])
        self.assertEqual(ticker.minor_ticks(), model.minor_ticks()[::-1])
    
    
    def test_narrow_region(self):
        """Tests whether narrow logarithmic ranges retain useful ticks."""
        
        ticker = pero.SymlogTicker(start=1.1, end=1.2)
        
        ticks = tuple(round(x, 10) for x in ticker.major_ticks())
        self.assertEqual(ticks, (1.1, 1.12, 1.14, 1.16, 1.18, 1.2))
        
        ticker(start=-1.2, end=-1.1)
        
        ticks = tuple(round(x, 10) for x in ticker.major_ticks())
        self.assertEqual(ticks, (-1.2, -1.18, -1.16, -1.14, -1.12, -1.1))
    
    
    def test_log_only_range_has_no_linear_ticks(self):
        """Tests that ranges beyond the threshold skip the linear tick region."""
        
        ticker = pero.SymlogTicker(start=1.1, end=1.2, threshold=1)
        
        self.assertEqual(
            tuple(round(tick, 10) for tick in ticker.major_ticks()),
            (1.1, 1.12, 1.14, 1.16, 1.18, 1.2))
        self.assertTrue(all(tick > 1 for tick in ticker.minor_ticks()))
        
        ticker(start=1.2, end=1.1)
        
        self.assertEqual(
            tuple(round(tick, 10) for tick in ticker.major_ticks()),
            (1.2, 1.18, 1.16, 1.14, 1.12, 1.1))
        self.assertTrue(all(tick > 1 for tick in ticker.minor_ticks()))
    
    
    def test_threshold(self):
        """Tests that thresholds respect the allocated linear tick budget."""
        
        ticker = pero.SymlogTicker(start=-200, end=200, threshold=2)
        
        self.assertEqual(ticker.major_ticks(), (-100, -10, 0, 10, 100))
        self.assertEqual(ticker.labels(), ('-100', '-10', '0', '10', '100'))
        
        ticker(threshold=1, start=-100, end=100)
        
        self.assertEqual(ticker.major_ticks(), (-100, -10, -1, 0, 1, 10, 100))
        
        ticker(threshold=0.1, start=-10, end=10)
        
        self.assertEqual(ticker.major_ticks(), (-10, -1, -0.1, 0, 0.1, 1, 10))
        self.assertEqual(ticker.labels(), ('-10', '-1', '-0.1', '0', '0.1', '1', '10'))

        ticker(threshold=2, start=-1e25, end=1e25)
        ticks = ticker.major_ticks()
        self.assertIn(0, ticks)
        self.assertNotIn(-2, ticks)
        self.assertNotIn(2, ticks)
    
    
    def test_threshold_regions(self):
        """Tests whether log and linear tickers are restricted to their regions."""
        
        ticker = pero.SymlogTicker(start=-500, end=500, threshold=0.1)
        
        self.assertEqual(
            ticker.major_ticks(),
            (-100, -10, -1, -0.1, 0, 0.1, 1, 10, 100))
        
        logarithmic = pero.LogTicker(start=0.1, end=500)
        model = sorted(set(
            [-tick for tick in logarithmic.minor_ticks()]
            + list(logarithmic.minor_ticks())))
        
        self.assertEqual(ticker.minor_ticks(), tuple(model))
    
    
    def test_linear_minor_ticks_are_limited_to_nearby_log_ranges(self):
        """Tests that central minor ticks are hidden for very wide log ranges."""
        
        ticker = pero.SymlogTicker(start=-10, end=10, threshold=1)
        
        self.assertIn(0.2, ticker.minor_ticks())
        self.assertIn(-0.2, ticker.minor_ticks())
        
        ticker(start=-1e25, end=1e25)
        
        self.assertEqual(
            [tick for tick in ticker.minor_ticks() if abs(tick) < 1],
            [])
        self.assertIn(0, ticker.major_ticks())
        self.assertIn(1, ticker.major_ticks())
        self.assertIn(-1, ticker.major_ticks())
    
    
    def test_small_threshold_major_ticks(self):
        """Tests whether major tick density stays global with a small threshold."""
        
        ticker = pero.SymlogTicker(start=-500, end=500, threshold=0.01)
        
        self.assertEqual(
            ticker.major_ticks(),
            (-100, -1, -0.01, 0, 0.01, 1, 100))
    
    
    def test_major_count_is_allocated_by_symlog_span(self):
        """Tests that linear and log portions share the major tick budget."""
        
        ticker = pero.SymlogTicker(start=-10, end=10, threshold=9)
        
        self.assertEqual(
            ticker.major_ticks(),
            (-10, -9, -6, -3, 0, 3, 6, 9, 10))
        self.assertEqual(ticker._lin_ticker.major_count, 6)
        self.assertEqual(ticker._log_ticker.major_count, 1)
        
        minor_ticks = ticker.minor_ticks()
        self.assertEqual(
            [round(tick, 10) for tick in minor_ticks if 9 < tick < 10],
            [])
        self.assertEqual(
            [round(tick, 10) for tick in minor_ticks if -10 < tick < -9],
            [])
    
    
    def test_short_log_wing_does_not_get_a_full_tick_budget(self):
        """Tests that a narrow log section receives ticks proportional to span."""
        
        ticker = pero.SymlogTicker(start=0, end=0.011, threshold=0.01)
        
        self.assertEqual(
            ticker.major_ticks(),
            (0, 0.002, 0.004, 0.006, 0.008, 0.01, 0.011))
        self.assertEqual(ticker._lin_ticker.major_count, 6)
        self.assertEqual(ticker._log_ticker.major_count, 1)
        self.assertEqual(ticker._log_ticker.minor_count, 2)
        self.assertEqual(
            [round(tick, 10) for tick in ticker.minor_ticks() if 0.01 < tick < 0.011],
            [0.0105])
    
    
    def test_asymmetric_ranges_use_symmetric_log_ticks(self):
        """Tests whether both log wings use steps from the longer side."""
        
        ticker = pero.SymlogTicker(start=-0.02, end=0.035, threshold=0.01)
        
        positive = [tick for tick in ticker.major_ticks() if tick > 0.01]
        negative = sorted(-tick for tick in ticker.major_ticks() if tick < -0.01)
        
        self.assertEqual(positive, [0.02, 0.03])
        self.assertEqual(negative, [0.02])
        
        positive = [tick for tick in ticker.minor_ticks() if tick > 0.01]
        negative = sorted(-tick for tick in ticker.minor_ticks() if tick < -0.01)
        
        numpy.testing.assert_almost_equal(
            positive[:5], [0.012, 0.014, 0.016, 0.018, 0.02])
        numpy.testing.assert_almost_equal(negative, positive[:5])
        
        ticker(start=-0.035, end=0.02)
        
        positive = [tick for tick in ticker.major_ticks() if tick > 0.01]
        negative = sorted(-tick for tick in ticker.major_ticks() if tick < -0.01)
        
        self.assertEqual(positive, [0.02])
        self.assertEqual(negative, [0.02, 0.03])
    
    
    def test_logarithmic_positions(self):
        """Tests whether geometric ticks have equal spacing outside threshold."""
        
        interpol = pero.SymlogInterpol(threshold=0.1)
        
        ticks = numpy.array([0.1, 1, 10])
        positions = interpol.normalize(ticks, 0.1, 10)
        numpy.testing.assert_almost_equal(list(positions), [0, 0.5, 1], 10)
        
        ticks = numpy.array([-10, -1, -0.1])
        positions = interpol.normalize(ticks, -10, -0.1)
        numpy.testing.assert_almost_equal(list(positions), [0, 0.5, 1], 10)
        
        ticker = pero.LogTicker(start=0.1, end=1, major_count=2)
        self.assertEqual(ticker.major_ticks(), (0.1, 1.0))
    
    
    def test_base(self):
        """Tests whether alternative logarithm bases are supported."""
        
        ticker = pero.SymlogTicker(start=-4, end=4, base=2)
        
        self.assertEqual(ticker.major_ticks(), (-4, -2, -1, -0.5, 0, 0.5, 1, 2, 4))
        
        ticker(base=2.5, start=-6.25, end=6.25)
        
        self.assertEqual(ticker.major_ticks(), (-6.25, -2.5, -1, 0, 1, 2.5, 6.25))
    
    
    def test_constant(self):
        """Tests whether constant ranges generate one major tick."""
        
        ticker = pero.SymlogTicker(start=0, end=0)
        
        self.assertEqual(ticker.major_ticks(), (0,))
        self.assertEqual(ticker.minor_ticks(), ())
        self.assertEqual(ticker.labels(), ('0',))
        self.assertEqual(ticker.beautify(0, 0), (0, 0))
        
        ticker(start=-10, end=-10)
        
        self.assertEqual(ticker.major_ticks(), (-10,))
        self.assertEqual(ticker.minor_ticks(), ())
        self.assertEqual(ticker.beautify(-10, -10), (-10, -10))
    
    
    def test_beautify(self):
        """Tests whether beautified ranges cover both signed logarithmic wings."""
        
        ticker = pero.SymlogTicker()
        
        self.assertEqual(ticker.beautify(-90, 90), (-100, 100))
        self.assertEqual(ticker.beautify(90, -90), (100, -100))
        self.assertEqual(ticker.beautify(1.1, 90), (1, 100))
        self.assertEqual(ticker.beautify(-90, -1.1), (-100, -1))
        self.assertEqual(ticker.beautify(-0.2, 90), (-1, 100))
        self.assertEqual(ticker.beautify(-90, 0.2), (-100, 1))
        
        ticker.threshold = 2
        
        self.assertEqual(ticker.beautify(-19, 190), (-100, 1000))
    
    
    def test_condensed(self):
        """Tests whether large ranges respect the requested tick density."""
        
        ticker = pero.SymlogTicker(start=-1e10, end=1e10)
        ticks = ticker.major_ticks()
        
        self.assertLessEqual(len(ticks), 2 * ticker.major_count)
        self.assertEqual(ticks, tuple(-x for x in ticks[::-1]))
        
        ticker.major_count = 20
        
        self.assertGreater(len(ticker.major_ticks()), len(ticks))
    
    
    def test_hidden_ticks(self):
        """Tests whether hiding boundary ticks also hides corresponding labels."""
        
        ticker = pero.SymlogTicker(start=-100, end=100, hide_first=True, hide_last=True)
        
        self.assertEqual(ticker.major_ticks(), (-10, -1, 0, 1, 10))
        self.assertEqual(ticker.labels(), ('-10', '-1', '0', '1', '10'))
    
    
    def test_property_changes(self):
        """Tests whether property changes update the internal tickers."""

        ticker = pero.SymlogTicker(start=-100, end=100)
        linear = ticker._lin_ticker
        logarithmic = ticker._log_ticker

        ticker(base=2, major_count=12, minor_count=2)

        self.assertEqual(logarithmic.base, 2)
        self.assertEqual(linear.major_count, 12)
        self.assertEqual(logarithmic.major_count, 12)
        self.assertEqual(linear.minor_count, 2)
        self.assertEqual(logarithmic.minor_count, 2)

        model = pero.SymlogTicker(start=-100, end=100, base=2, major_count=12, minor_count=2)

        self.assertEqual(ticker.major_ticks(), model.major_ticks())
        self.assertEqual(ticker.minor_ticks(), model.minor_ticks())
        self.assertEqual(ticker.labels(), model.labels())
        self.assertIs(ticker._lin_ticker, linear)
        self.assertIs(ticker._log_ticker, logarithmic)


    def test_region_changes(self):
        """Tests whether reused tickers reset settings between regions."""

        ticker = pero.SymlogTicker(start=-100, end=100)
        ticker.major_ticks()
        ticker.beautify(-90, 90)
        ticker(start=-0.5, end=0.5)

        model = pero.SymlogTicker(start=-0.5, end=0.5)

        self.assertEqual(ticker.major_ticks(), model.major_ticks())
        self.assertEqual(ticker.minor_ticks(), model.minor_ticks())
        self.assertEqual(ticker.beautify(-0.5, 0.5), model.beautify(-0.5, 0.5))

        ticker(threshold=2, start=-200, end=200)
        model(threshold=2, start=-200, end=200)

        self.assertEqual(ticker.major_ticks(), model.major_ticks())
        self.assertEqual(ticker.minor_ticks(), model.minor_ticks())
        self.assertEqual(ticker.beautify(-190, 190), model.beautify(-190, 190))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)

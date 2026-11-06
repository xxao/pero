#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


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
        model = (-10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
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
    
    
    def test_threshold(self):
        """Tests whether custom thresholds anchor logarithmic ticks."""
        
        ticker = pero.SymlogTicker(start=-200, end=200, threshold=2)
        
        self.assertEqual(ticker.major_ticks(), (-200, -20, -2, 0, 2, 20, 200))
        self.assertEqual(ticker.labels(), ('-200', '-20', '-2', '0', '2', '20', '200'))
        
        ticker(threshold=1, start=-100, end=100)
        
        self.assertEqual(ticker.major_ticks(), (-100, -10, -1, 0, 1, 10, 100))
        
        ticker(threshold=0.1, start=-10, end=10)
        
        self.assertEqual(ticker.major_ticks(), (-10, -1, -0.1, 0, 0.1, 1, 10))
        self.assertEqual(ticker.labels(), ('-10', '-1', '-0.1', '0', '0.1', '1', '10'))
    
    
    def test_base(self):
        """Tests whether alternative logarithm bases are supported."""
        
        ticker = pero.SymlogTicker(start=-4, end=4, base=2)
        
        self.assertEqual(ticker.major_ticks(), (-4, -2, -1, 0, 1, 2, 4))
        
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
        
        self.assertEqual(ticker.beautify(-19, 190), (-20, 200))
    
    
    def test_condensed(self):
        """Tests whether large ranges respect the requested tick density."""
        
        ticker = pero.SymlogTicker(start=-1e10, end=1e10)
        ticks = ticker.major_ticks()
        
        self.assertLessEqual(len(ticks), ticker.major_count + 2)
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

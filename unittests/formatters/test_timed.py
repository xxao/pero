#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for time formatter."""
    
    
    def test_standalone(self):
        """Tests whether formatter works as standalone tool."""
        
        # init formatter
        formatter = pero.TimeFormatter()
        
        # test hours
        self.assertEqual(formatter.format(3600), "1.00")
        self.assertEqual(formatter.format(3600+1800), "1.50")
        
        # test minutes
        self.assertEqual(formatter.format(60), "1.00")
        self.assertEqual(formatter.format(3600-1), "59.98")
        
        # test seconds
        self.assertEqual(formatter.format(1), "1.00")
        self.assertEqual(formatter.format(17.555), "17.55")
        self.assertEqual(formatter.format(59), "59.00")
        
        # test milliseconds
        self.assertEqual(formatter.format(.001), "1.00")
        self.assertEqual(formatter.format(.1), "100.00")
    
    
    def test_units(self):
        """Tests whether units are added correctly."""
        
        formatter = pero.TimeFormatter(add_units=True)
        
        self.assertEqual(formatter.format(3600+1800-1), "1.50 h")
        self.assertEqual(formatter.format(70.5), "1.18 m")
        self.assertEqual(formatter.format(17.567), "17.57 s")
        self.assertEqual(formatter.format(.1), "100.00 ms")
    
    
    def test_precision(self):
        """Tests whether precision is used correctly."""
        
        # check hours
        formatter = pero.TimeFormatter(precision=3600)
        
        self.assertEqual(formatter.format(3600+1800-1), "1.50")
        self.assertEqual(formatter.format(70.5), "1.18")
        self.assertEqual(formatter.format(17.567), "17.57")
        self.assertEqual(formatter.format(.1), "100.00")
        
        # check minutes
        formatter = pero.TimeFormatter(precision=60)
        
        self.assertEqual(formatter.format(3600+1800-1), "1:30")
        self.assertEqual(formatter.format(70.5), "1.18")
        self.assertEqual(formatter.format(17.567), "17.57")
        self.assertEqual(formatter.format(.1), "100.00")
        
        # check seconds
        formatter = pero.TimeFormatter(precision=1)
        
        self.assertEqual(formatter.format(3600+1800-1), "1:29:59")
        self.assertEqual(formatter.format(70.5), "01:10")
        self.assertEqual(formatter.format(17.567), "17.57")
        self.assertEqual(formatter.format(.1), "100.00")
        
        # check milliseconds
        formatter = pero.TimeFormatter(precision=0.1)
        
        self.assertEqual(formatter.format(3600+1800-1), "1:29:59:000")
        self.assertEqual(formatter.format(70.5), "01:10:500")
        self.assertEqual(formatter.format(17.567), "17:567")
        self.assertEqual(formatter.format(.1), "100.00")
    
    
    def test_domain(self):
        """Tests whether domain is used correctly."""
        
        # test hours
        formatter = pero.TimeFormatter(domain=3600)
        
        self.assertEqual(formatter.format(3600+1800-1), "1.50")
        self.assertEqual(formatter.format(70.5), "0.02")
        self.assertEqual(formatter.format(17.567), "0.00")
        self.assertEqual(formatter.format(.1), "0.00")
        
        # test minutes
        formatter = pero.TimeFormatter(domain=60)
        
        self.assertEqual(formatter.format(3600+1800-1), "89.98")
        self.assertEqual(formatter.format(70.5), "1.18")
        self.assertEqual(formatter.format(17.567), "0.29")
        self.assertEqual(formatter.format(.1), "0.00")
        
        # test seconds
        formatter = pero.TimeFormatter(domain=1)
        
        self.assertEqual(formatter.format(3600+1800-1), "5399.00")
        self.assertEqual(formatter.format(70.5), "70.50")
        self.assertEqual(formatter.format(17.567), "17.57")
        self.assertEqual(formatter.format(.1), "0.10")
    
    
    def test_auto_range(self):
        """Tests whether domain together with precision are used correctly."""
        
        formatter = pero.TimeFormatter(domain=3600, precision=1)
        
        self.assertEqual(formatter.format(3600+1800-1), "1:29:59")
        self.assertEqual(formatter.format(70.5), "0:01:10")
        self.assertEqual(formatter.format(17.567), "0:00:18")
        self.assertEqual(formatter.format(.1), "0:00:00")
    
    
    def test_separator(self):
        """Tests whether separator is used correctly."""
        
        formatter = pero.TimeFormatter(separator=" ", add_units=True, domain=3600, precision=1)
        
        self.assertEqual(formatter.format(3600+1800-1), "1 h 29 m 59 s")
        self.assertEqual(formatter.format(70.5), "0 h 01 m 10 s")
        self.assertEqual(formatter.format(17.567), "0 h 00 m 18 s")
        self.assertEqual(formatter.format(.1), "0 h 00 m 00 s")
    
    
    def test_template(self):
        """Tests whether custom template is used correctly."""
        
        formatter = pero.TimeFormatter(
            template = "time: {h}:{m}:{s}.{ms}",
            domain = 3600,
            precision = 1,
            add_units = True)
        
        self.assertEqual(formatter.format(3600+1800-1), "time: 1:29:59.000")
        self.assertEqual(formatter.format(70.5), "time: 0:01:10.500")
        self.assertEqual(formatter.format(17.567), "time: 0:00:17.567")
        self.assertEqual(formatter.format(.1), "time: 0:00:00.100")
    
    
    def test_parts_templates(self):
        """Tests whether custom parts templates are used correctly."""
        
        # with specified unit
        formatter = pero.TimeFormatter(
            template="{h} {m} {s} {ms} {us} {ns}",
            h_template = "h:{h:.0f}",
            m_template = "m:{m:.0f}",
            s_template = "s:{s:.0f}",
            ms_template = "ms:{ms:.0f}",
            us_template = "us:{us:.0f}",
            ns_template = "ns:{ns:.0f}")
        
        self.assertEqual(formatter.format(3600+1800-1), "h:1 m:29 s:59 ms:0 us:0 ns:0")
        self.assertEqual(formatter.format(70.5), "h:0 m:1 s:10 ms:500 us:0 ns:0")
        self.assertEqual(formatter.format(17.567), "h:0 m:0 s:17 ms:567 us:0 ns:0")
        self.assertEqual(formatter.format(.1), "h:0 m:0 s:0 ms:100 us:0 ns:0")
        
        # without specified unit
        formatter = pero.TimeFormatter(
            template="{h} {m} {s} {ms} {us} {ns}",
            h_template = "h:{:.0f}",
            m_template = "m:{:.0f}",
            s_template = "s:{:.0f}",
            ms_template = "ms:{:.0f}",
            us_template = "us:{:.0f}",
            ns_template = "ns:{:.0f}")
        
        self.assertEqual(formatter.format(3600+1800-1), "h:1 m:29 s:59 ms:0 us:0 ns:0")
        self.assertEqual(formatter.format(70.5), "h:0 m:1 s:10 ms:500 us:0 ns:0")
        self.assertEqual(formatter.format(17.567), "h:0 m:0 s:17 ms:567 us:0 ns:0")
        self.assertEqual(formatter.format(.1), "h:0 m:0 s:0 ms:100 us:0 ns:0")
    
    
    def test_rounding(self):
        """Tests whether rounding works correctly."""
        
        # round down
        formatter = pero.TimeFormatter(rounding=pero.ROUNDING.FLOOR, add_units=True)
        
        self.assertEqual(formatter.format(3600+1800-1), "1.49 h")
        self.assertEqual(formatter.format(70.5), "1.17 m")
        self.assertEqual(formatter.format(17.567), "17.56 s")
        
        # round up
        formatter = pero.TimeFormatter(rounding=pero.ROUNDING.CEIL, add_units=True)
        
        self.assertEqual(formatter.format(3600+1800-1), "1.50 h")
        self.assertEqual(formatter.format(70.5), "1.18 m")
        self.assertEqual(formatter.format(17.567), "17.57 s")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)

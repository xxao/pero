#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# run all available tests
if __name__ == "__main__":
    
    import os.path
    import unittest
    
    suite = unittest.TestLoader().discover(os.path.dirname(__file__), pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)


"""
tests/run_all_tests.py
Test Runner for All Components
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """Run all test suites"""
    
    print("🧪 DENSO888 Test Suite")
    print("=" * 50)
    print("Created by: Thammaphon Chittasuwanna (SDM)")
    print("เฮียตอมจัดหั้ย!!! - Testing Edition 🚀")
    print("=" * 50)
    print()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    
    # Test directories
    test_dirs = [
        'tests',
        'tests/test_gui'
    ]
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add tests from all directories
    for test_dir in test_dirs:
        test_path = project_root / test_dir
        if test_path.exists():
            print(f"📁 Loading tests from: {test_dir}")
            discovered_tests = loader.discover(
                str(test_path),
                pattern='test_*.py',
                top_level_dir=str(project_root)
            )
            suite.addTests(discovered_tests)
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    print("\n🚀 Running tests...")
    print("-" * 50)
    
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {total_tests - failures - errors}")
    print(f"❌ Failed: {failures}")
    print(f"🔥 Errors: {errors}")
    print(f"⏭️ Skipped: {skipped}")
    
    if failures == 0 and errors == 0:
        print("\n🎉 All tests passed! เฮียตอมเก่งมาก!!! 🚀")
        return True
    else:
        print("\n⚠️ Some tests failed. Check output above for details.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1) 
    
        """environment"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        
        self.config = {
            'db_type': 'sqlite',
            'sqlite_file': self.temp_db.name
        }
        
        self.db_manager = DatabaseManager(self.config)
    
    def tearDown(self):
        """Cleanup test environment"""
        if self.db_manager:
            self.db_manager.close()
        
        # Remove temporary database
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_sqlite_connection(self):
        """Test SQLite database connection"""
        success, message = self.db_manager.connect()
        self.assertTrue(success, f"Connection failed: {message}")
        self.assertIsNotNone(self.db_manager.connection)
    
    def test_create_table_from_data(self):
        """Test table creation from data"""
        # Connect first
        self.db_manager.connect()
        
        # Sample data
        test_data = [
            {'id': 1, 'name': 'Test User 1', 'email': 'test1@example.com'},
            {'id': 2, 'name': 'Test User 2', 'email': 'test2@example.com'}
        ]
        
        # Create table
        success, message = self.db_manager.create_table_from_data('test_users', test_data)
        self.assertTrue(success, f"Table creation failed: {message}")
        
        # Verify table exists
        tables = self.db_manager.get_tables()
        self.assertIn('test_users', tables)
    
    def test_insert_data(self):
        """Test data insertion"""
        # Connect and create table
        self.db_manager.connect()
        
        test_data = [
            {'id': 1, 'name': 'John Doe', 'age': 30},
            {'id': 2, 'name': 'Jane Smith', 'age': 25}
        ]
        
        # Create table
        self.db_manager.create_table_from_data('test_insert', test_data)
        
        # Insert data
        success, message = self.db_manager.insert_data('test_insert', test_data)
        self.assertTrue(success, f"Data insertion failed: {message}")
        
        # Verify data was inserted
        success, result = self.db_manager.execute_query("SELECT COUNT(*) FROM test_insert")
        self.assertTrue(success)
        self.assertEqual(result['rows'][0][0], 2)
    
    def test_get_tables(self):
        """Test getting table list"""
        self.db_manager.connect()
        
        # Create test table
        test_data = [{'col1': 'value1'}]
        self.db_manager.create_table_from_data('test_table_list', test_data)
        
        # Get tables
        tables = self.db_manager.get_tables()
        self.assertIsInstance(tables, list)
        self.assertIn('test_table_list', tables)
    
    def test_get_table_info(self):
        """Test getting table information"""
        self.db_manager.connect()
        
        # Create test table
        test_data = [
            {'id': 1, 'name': 'Test', 'active': True},
            {'id': 2, 'name': 'Test2', 'active': False}
        ]
        self.db_manager.create_table_from_data('test_info', test_data)
        self.db_manager.insert_data('test_info', test_data)
        
        # Get table info
        info = self.db_manager.get_table_info('test_info')
        
        self.assertIn('table_name', info)
        self.assertIn('row_count', info)
        self.assertIn('columns', info)
        self.assertEqual(info['table_name'], 'test_info')
        self.assertEqual(info['row_count'], 2)
    
    def test_execute_query(self):
        """Test query execution"""
        self.db_manager.connect()
        
        # Test SELECT query
        success, result = self.db_manager.execute_query("SELECT 1 as test_value")
        self.assertTrue(success)
        self.assertIn('columns', result)
        self.assertIn('rows', result)
        self.assertEqual(result['rows'][0][0], 1)
    
    def test_database_stats(self):
        """Test database statistics"""
        self.db_manager.connect()
        
        # Create test data
        test_data = [{'id': i, 'value': f'test_{i}'} for i in range(10)]
        self.db_manager.create_table_from_data('test_stats', test_data)
        self.db_manager.insert_data('test_stats', test_data)
        
        # Get stats
        stats = self.db_manager.get_database_stats()
        
        self.assertIn('database_type', stats)
        self.assertIn('connected', stats)
        self.assertIn('total_tables', stats)
        self.assertEqual(stats['database_type'], 'sqlite')
        self.assertTrue(stats['connected'])

class TestDatabaseConfig(unittest.TestCase):
    """Test database configuration model"""
    
    def test_sqlite_config(self):
        """Test SQLite configuration"""
        config = DatabaseConfig(db_type='sqlite', sqlite_file='test.db')
        
        self.assertEqual(config.db_type, 'sqlite')
        self.assertEqual(config.sqlite_file, 'test.db')
        
        # Test connection URL
        url = config.get_connection_url()
        self.assertEqual(url, 'sqlite:///test.db')
    
    def test_sqlserver_config_windows_auth(self):
        """Test SQL Server configuration with Windows auth"""
        config = DatabaseConfig(
            db_type='sqlserver',
            server='localhost',
            database='testdb',
            use_windows_auth=True
        )
        
        url = config.get_connection_url()
        self.assertIn('mssql+pyodbc', url)
        self.assertIn('trusted_connection=yes', url)
    
    def test_sqlserver_config_sql_auth(self):
        """Test SQL Server configuration with SQL auth"""
        config = DatabaseConfig(
            db_type='sqlserver',
            server='localhost',
            database='testdb',
            username='testuser',
            password='testpass',
            use_windows_auth=False
        )
        
        url = config.get_connection_url()
        self.assertIn('mssql+pyodbc', url)
        self.assertIn('testuser', url)
    
    def test_update_from_dict(self):
        """Test updating config from dictionary"""
        config = DatabaseConfig()
        
        update_data = {
            'db_type': 'sqlserver',
            'server': 'newserver',
            'database': 'newdb'
        }
        
        config.update_from_dict(update_data)
        
        self.assertEqual(config.db_type, 'sqlserver')
        self.assertEqual(config.server, 'newserver')
        self.assertEqual(config.database, 'newdb')

if __name__ == '__main__':
    unittest.main()
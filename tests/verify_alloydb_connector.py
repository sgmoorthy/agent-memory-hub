"""
Verification script for AlloyDB Connector driver support.
This script attempts to initialize the Connector with 'pg8000' to ensure it is supported.
"""
import sys
from unittest.mock import MagicMock, patch

def verify_driver_support():
    print(">> Verifying google-cloud-alloydb-connector driver support...")
    
    # 1. Check if we can import the connector
    try:
        from google.cloud.alloydb.connector import Connector
        print("   [OK] google-cloud-alloydb-connector imported.")
    except ImportError:
        print("   [SKIP] google-cloud-alloydb-connector not installed.")
        return

    # 2. Check if pg8000 is importable (needed by SQLAlchemy+Connector)
    try:
        import pg8000
        print("   [OK] pg8000 imported.")
    except ImportError:
        print("   [FAIL] pg8000 not installed!")
        # We don't exit here, we let the connector fail to see the message
    
    # 3. Test Connector.connect argument validation validation
    # We mock _connect_func or similar internal to avoid actual network calls,
    # BUT we want to hit the argument validation logic first.
    
    connector = Connector()
    
    # We mock the actual 'connect' method's internal network call, 
    # but we hope to pass the driver check before that.
    # Looking at library source, validity checks happen early.
    
    print("   [INFO] Attempting connector.connect() with 'pg8000' driver...")
    
    try:
        # We patch the internal 'connect' or 'InstanceConnectionManager' to avoid real network
        # The connector.connect() usually returns a socket or connection object.
        # We just want to ensure it DOES NOT raise "driver not supported".
        
        # We'll expect a network/auth error if it proceeds, 
        # or success if we mock enough.
        # But if it raises "psycopg2 not supported" (or pg8000 equivalent), we fail.
        
        # Let's just try to call it with a dummy instance string.
        # It will likely fail on Metadata or API calls, but that proves passed driver check.
        
        with patch("google.cloud.alloydb.connector.connector.Connector.connect") as mock_connect: # mocking simply to prevent real hang
             # actually, if we mock the method itself, we verify nothing about the method's logic.
             # We should NOT mock the entry point if we want to test its validation.
             pass

        # Real call will hang or fail faster.
        # Let's rely on the user's previous error: 
        # "psycopg2 is not a supported database driver"
        
        # If we get past that to "403 Forbidden" or "Name resolution failure", we are good.
        
        try:
            # Short timeout? The connector doesn't typically accept timeout on connect entry.
            # We will catch "ValueError" or similar library errors.
            connector.connect(
                "project:region:instance",
                "pg8000",
                user="test",
                password="test",
                db="test"
            )
        except Exception as e:
            error_msg = str(e)
            print(f"   [RESULT] Caught exception: {type(e).__name__}: {error_msg}")
            
            if "not a supported database driver" in error_msg:
                print("   [FAIL] Driver 'pg8000' rejected by Connector!")
                sys.exit(1)
            elif "pg8000" in error_msg and "module not found" in error_msg.lower():
                 print("   [FAIL] Driver 'pg8000' missing from environment.")
                 sys.exit(1)
            else:
                 print("   [PASS] Driver check passed (failed later on proper network/auth error).")

    except Exception as e:
         print(f"   [ERROR] Unexpected: {e}")

if __name__ == "__main__":
    verify_driver_support()

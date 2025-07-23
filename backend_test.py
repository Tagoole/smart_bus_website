import requests
import sys
from datetime import datetime

class SmartBusAPITester:
    def __init__(self, base_url="https://d3d056c3-54f2-4a2b-8f47-f910d5474269.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, expected_keys=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, timeout=10)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                
                # Check response content if it's JSON
                try:
                    json_response = response.json()
                    print(f"   Response: {json_response}")
                    
                    # Validate expected keys if provided
                    if expected_keys:
                        missing_keys = []
                        for key in expected_keys:
                            if key not in json_response:
                                missing_keys.append(key)
                        
                        if missing_keys:
                            print(f"⚠️  Warning: Missing expected keys: {missing_keys}")
                        else:
                            print(f"✅ All expected keys present: {expected_keys}")
                    
                    return True, json_response
                except Exception as e:
                    print(f"   Response (non-JSON): {response.text[:200]}...")
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except requests.exceptions.ConnectionError:
            print(f"❌ Failed - Connection error")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_endpoint(self):
        """Test health check endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200,
            expected_keys=["status", "message"]
        )

    def test_stats_endpoint(self):
        """Test platform stats endpoint"""
        return self.run_test(
            "Platform Stats",
            "GET", 
            "api/stats",
            200,
            expected_keys=["daily_users", "on_time_performance", "routes_covered"]
        )

    def test_features_endpoint(self):
        """Test features endpoint"""
        success, response = self.run_test(
            "Features",
            "GET",
            "api/features", 
            200,
            expected_keys=["features"]
        )
        
        if success and isinstance(response, dict) and "features" in response:
            features = response["features"]
            print(f"   Found {len(features)} features")
            for feature in features:
                if "id" in feature and "name" in feature:
                    print(f"   - {feature['name']} ({feature['id']})")
        
        return success, response

    def test_download_info_endpoint(self):
        """Test download info endpoint"""
        success, response = self.run_test(
            "Download Info",
            "GET",
            "api/download-info",
            200,
            expected_keys=["android", "ios"]
        )
        
        if success and isinstance(response, dict):
            if "android" in response:
                android = response["android"]
                print(f"   Android: Available={android.get('available', 'N/A')}, Version={android.get('version', 'N/A')}")
            if "ios" in response:
                ios = response["ios"]
                print(f"   iOS: Available={ios.get('available', 'N/A')}, Version={ios.get('version', 'N/A')}")
        
        return success, response

    def test_mock_endpoints(self):
        """Test mock endpoints for future functionality"""
        print(f"\n📱 Testing Mock Endpoints...")
        
        # Test nearby buses
        self.run_test(
            "Nearby Buses (Mock)",
            "GET",
            "api/buses/nearby",
            200,
            expected_keys=["buses"]
        )
        
        # Test routes
        self.run_test(
            "Routes (Mock)",
            "GET", 
            "api/routes",
            200,
            expected_keys=["routes"]
        )

def main():
    print("🚌 SmartBus API Testing Suite")
    print("=" * 50)
    
    # Setup
    tester = SmartBusAPITester()
    
    # Test core landing page endpoints
    print(f"\n📋 Testing Core Landing Page Endpoints...")
    tester.test_health_endpoint()
    tester.test_stats_endpoint() 
    tester.test_features_endpoint()
    tester.test_download_info_endpoint()
    
    # Test mock endpoints
    tester.test_mock_endpoints()
    
    # Print final results
    print(f"\n" + "=" * 50)
    print(f"📊 Final Results:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print(f"🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
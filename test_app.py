"""
Test Script for TalentScout Hiring Assistant
Tests all major functionality
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔍 Testing Environment Setup...")
    print("-" * 50)
    
    load_dotenv()
    api_key = os.getenv("GROK_API_KEY")
    
    if not api_key:
        print("❌ GROK_API_KEY not found in .env file")
        return False
    
    if api_key == "your_api_key_here":
        print("❌ GROK_API_KEY is still the default value")
        print("   Please replace it with your actual API key")
        return False
    
    print("✅ Environment variables loaded successfully")
    print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
    return True


def test_imports():
    """Test if all required packages are installed"""
    print("\n🔍 Testing Package Imports...")
    print("-" * 50)
    
    required_packages = {
        'gradio': 'gradio',
        'openai': 'openai',
        'dotenv': 'python-dotenv',
        'json': 'json (built-in)',
        're': 're (built-in)',
        'datetime': 'datetime (built-in)'
    }
    
    all_imported = True
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            all_imported = False
    
    return all_imported


def test_api_connection():
    """Test connection to Grok API"""
    print("\n🔍 Testing API Connection...")
    print("-" * 50)
    
    try:
        from openai import OpenAI
        load_dotenv()
        
        client = OpenAI(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        
        # Make a simple test call
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "user", "content": "Say 'test successful' if you can read this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API connection successful")
        print(f"   Response: {result[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False


def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing File Structure...")
    print("-" * 50)
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env',
        '.gitignore',
        'README.md'
    ]
    
    optional_files = [
        'view_candidates.py',
        'test_app.py'
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (required)")
            all_exist = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} (optional)")
        else:
            print(f"⚠️  {file} (optional - not found)")
    
    return all_exist


def test_data_directory():
    """Test data storage directory"""
    print("\n🔍 Testing Data Storage...")
    print("-" * 50)
    
    # Create directory if it doesn't exist
    if not os.path.exists("candidate_data"):
        os.makedirs("candidate_data")
        print("✅ Created 'candidate_data' directory")
    else:
        print("✅ 'candidate_data' directory exists")
        
        # Check for existing data
        files = [f for f in os.listdir("candidate_data") if f.endswith('.json')]
        if files:
            print(f"   Found {len(files)} candidate file(s)")
        else:
            print("   No candidate files yet (this is normal)")
    
    return True


def test_validation_functions():
    """Test email and phone validation"""
    print("\n🔍 Testing Validation Functions...")
    print("-" * 50)
    
    try:
        import re
        
        # Test email validation
        def validate_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        # Test phone validation
        def validate_phone(phone):
            clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
            return len(clean_phone) >= 10 and clean_phone.isdigit()
        
        # Test cases
        test_emails = [
            ("john@example.com", True),
            ("invalid.email", False),
            ("test@test.co.uk", True)
        ]
        
        test_phones = [
            ("1234567890", True),
            ("(123) 456-7890", True),
            ("123", False)
        ]
        
        all_passed = True
        
        print("Email validation tests:")
        for email, expected in test_emails:
            result = validate_email(email)
            status = "✅" if result == expected else "❌"
            print(f"   {status} {email}: {result}")
            if result != expected:
                all_passed = False
        
        print("\nPhone validation tests:")
        for phone, expected in test_phones:
            result = validate_phone(phone)
            status = "✅" if result == expected else "❌"
            print(f"   {status} {phone}: {result}")
            if result != expected:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Validation test failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("🧪 TALENTSCOUT HIRING ASSISTANT - TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Package Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Data Storage", test_data_directory),
        ("Validation Functions", test_validation_functions),
        ("API Connection", test_api_connection)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your app is ready to run.")
        print("\n▶️  Run the app with: python app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("   Refer to the README.md for setup instructions.")
    
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()

    
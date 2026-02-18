"""
Test script to verify all backend dependencies are installed correctly
"""
import sys

def test_imports():
    """Test all critical imports"""
    print("=" * 60)
    print("🧪 Testing Backend Dependencies")
    print("=" * 60)
    
    tests = [
        # Web Framework & API
        ("FastAPI", "fastapi", "FastAPI"),
        ("Uvicorn", "uvicorn", "run"),
        ("Pydantic", "pydantic", "BaseModel"),
        ("Pydantic Settings", "pydantic_settings", "BaseSettings"),
        
        # Authentication & Security
        ("Python-JOSE", "jose", "jwt"),
        ("Passlib", "passlib.context", "CryptContext"),
        ("Email Validator", "email_validator", "validate_email"),
        
        # Database & ORM
        ("SQLAlchemy", "sqlalchemy", "create_engine"),
        ("Alembic", "alembic", "config"),
        
        # ML Libraries
        ("Scikit-learn", "sklearn", "ensemble"),
        ("NumPy", "numpy", "array"),
        ("Pandas", "pandas", "DataFrame"),
        ("SciPy", "scipy", "stats"),
        ("Prophet", "prophet", "Prophet"),
        ("Statsmodels", "statsmodels", "api"),
        ("TensorFlow", "tensorflow", "keras"),
        ("Joblib", "joblib", "dump"),
        ("Matplotlib", "matplotlib", "pyplot"),
        ("Seaborn", "seaborn", "set_theme"),
        
        # Monitoring & Services
        ("Prometheus Client", "prometheus_client", "Counter"),
        ("Requests", "requests", "get"),
        ("AioHTTP", "aiohttp", "ClientSession"),
        
        # Utilities
        ("Python-dotenv", "dotenv", "load_dotenv"),
    ]
    
    passed = 0
    failed = 0
    failed_packages = []
    
    for name, module, attr in tests:
        try:
            mod = __import__(module, fromlist=[attr])
            if hasattr(mod, attr):
                print(f"✅ {name:<25} - OK")
                passed += 1
            else:
                print(f"⚠️  {name:<25} - Imported but missing {attr}")
                failed += 1
                failed_packages.append(name)
        except ImportError as e:
            print(f"❌ {name:<25} - FAILED: {str(e)}")
            failed += 1
            failed_packages.append(name)
        except Exception as e:
            print(f"⚠️  {name:<25} - ERROR: {str(e)}")
            failed += 1
            failed_packages.append(name)
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n❌ Some dependencies failed to import!")
        print("\n📦 Failed packages:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        print("\n💡 To fix, run:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed correctly!")
        print("\n🚀 You can now start the backend:")
        print("   python start_backend.py")
        return True


def test_ml_models():
    """Test ML model imports"""
    print("\n" + "=" * 60)
    print("🤖 Testing ML Models")
    print("=" * 60)
    
    ml_models = [
        ("Anomaly Detector", "app.ml_models.anomaly_detector", "AnomalyDetector"),
        ("CPU Predictor", "app.ml_models.cpu_predictor", "CPUPredictor"),
        ("Memory Predictor", "app.ml_models.memory_predictor", "MemoryPredictor"),
        ("Health Scorer", "app.ml_models.health_scorer", "HealthScorer"),
        ("Failure Predictor", "app.ml_models.failure_predictor", "FailurePredictor"),
        ("Root Cause Analyzer", "app.ml_models.root_cause_analyzer", "RootCauseAnalyzer"),
        ("Capacity Planner", "app.ml_models.capacity_planner", "CapacityPlanner"),
    ]
    
    passed = 0
    failed = 0
    
    for name, module, class_name in ml_models:
        try:
            mod = __import__(module, fromlist=[class_name])
            cls = getattr(mod, class_name)
            instance = cls()
            print(f"✅ {name:<25} - OK")
            passed += 1
        except Exception as e:
            print(f"❌ {name:<25} - FAILED: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 ML Models: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


def main():
    """Run all tests"""
    deps_ok = test_imports()
    
    if deps_ok:
        ml_ok = test_ml_models()
        
        if ml_ok:
            print("\n🎉 All tests passed! Backend is ready to run!")
            sys.exit(0)
        else:
            print("\n⚠️  ML models have issues but core dependencies are OK")
            sys.exit(1)
    else:
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)


if __name__ == "__main__":
    main()

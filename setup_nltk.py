import nltk
import sys

def setup_nltk_data():
    """Download all required NLTK data"""
    print("🔧 Setting up NLTK data for Pinocchio Voice App...")
    
    # List of required NLTK resources
    resources = [
        'punkt_tab',     # New tokenizer (NLTK 3.8+)
        'punkt',         # Old tokenizer (fallback)
        'wordnet',       # WordNet corpus for synonyms
        'omw-1.4',       # Open Multilingual Wordnet
        'averaged_perceptron_tagger',  # POS tagger (useful for future phases)
    ]
    
    success_count = 0
    total_count = len(resources)
    
    for resource in resources:
        try:
            print(f"📦 Downloading {resource}...")
            nltk.download(resource, quiet=False)
            print(f"✅ Successfully downloaded {resource}")
            success_count += 1
        except Exception as e:
            print(f"⚠️  Warning: Could not download {resource}: {e}")
    
    print(f"\n🎉 Setup complete! {success_count}/{total_count} resources downloaded successfully.")
    
    if success_count >= 3:  # At least punkt, wordnet, and one other
        print("✅ You should be able to run the Pinocchio Voice App now!")
    else:
        print("❌ Some downloads failed. The app might have limited functionality.")
    
    # Test the setup
    print("\n🧪 Testing NLTK setup...")
    try:
        # Test tokenization
        from nltk.tokenize import sent_tokenize, word_tokenize
        test_text = "Hello world. This is a test."
        sentences = sent_tokenize(test_text)
        words = word_tokenize(test_text)
        print(f"✅ Tokenization test passed: {len(sentences)} sentences, {len(words)} words")
        
        # Test WordNet
        from nltk.corpus import wordnet
        synonyms = wordnet.synsets('happy')
        print(f"✅ WordNet test passed: Found {len(synonyms)} synsets for 'happy'")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("You may need to install additional packages or run as administrator")

def check_other_dependencies():
    """Check if other required packages are installed"""
    print("\n🔍 Checking other dependencies...")
    
    required_packages = {
        'speech_recognition': 'speechrecognition',
        'pyttsx3': 'pyttsx3',
        'langdetect': 'langdetect',
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
    
    # Check for PyAudio (tricky one)
    try:
        import pyaudio
        print("✅ pyaudio is installed")
    except ImportError:
        print("❌ pyaudio is NOT installed")
        print("For PyAudio installation help:")
        print("  Windows: pip install pyaudio")
        print("  macOS: brew install portaudio && pip install pyaudio")
        print("  Linux: sudo apt-get install python3-pyaudio")
        missing_packages.append("pyaudio")
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    print("🎭 Pinocchio Voice App - Setup Script")
    print("=" * 50)
    
    # Setup NLTK data
    setup_nltk_data()
    
    # Check other dependencies
    all_deps_ok = check_other_dependencies()
    
    print("\n" + "=" * 50)
    if all_deps_ok:
        print("🎉 All dependencies are ready! You can now run the main app.")
    else:
        print("⚠️  Some dependencies are missing. Please install them before running the main app.")
    
    print("\nTo run the Pinocchio Voice App:")
    print("python pinocchio_voice_app.py")
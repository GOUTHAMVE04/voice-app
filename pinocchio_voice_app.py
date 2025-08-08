import speech_recognition as sr
import pyttsx3
import random
import re
from langdetect import detect
import nltk
from nltk.corpus import wordnet
import time

# Download required NLTK data (run once)
def download_nltk_data():
    """Download required NLTK data with proper error handling"""
    resources = ['punkt_tab', 'punkt', 'wordnet', 'omw-1.4']
    
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                print(f"Downloading NLTK resource: {resource}")
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Warning: Could not download {resource}: {e}")
        except:
            try:
                nltk.data.find(f'corpora/{resource}')
            except LookupError:
                try:
                    print(f"Downloading NLTK resource: {resource}")
                    nltk.download(resource, quiet=True)
                except Exception as e:
                    print(f"Warning: Could not download {resource}: {e}")

# Initialize NLTK data
download_nltk_data()

class PinocchioVoiceApp:
    def __init__(self):
        # Initialize speech recognition and TTS
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS settings
        self.tts_engine.setProperty('rate', 150)  # Slightly slower for dramatic effect
        
        # Malayalam confusion phrases and connectors
        self.malayalam_connectors = [
            "അതായത്", "എന്നാൽ", "എങ്കിലും", "അതിനാൽ", "പക്ഷേ",
            "എന്തെങ്കിലും", "എവിടെയെങ്കിലും", "എപ്പോഴെങ്കിലും"
        ]
        
        # English confusion connectors and phrases
        self.english_connectors = [
            "henceforth", "insofar as", "nevertheless", "notwithstanding",
            "furthermore", "consequently", "in the aforementioned manner",
            "pursuant to the fact that", "with all due respect to the matter"
        ]
        
        # Calibrate microphone
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Calibration complete!")

    def get_synonyms(self, word):
        """Get synonyms for English words using WordNet"""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
        return list(synonyms)

    def apply_pinocchio_logic(self, text):
        """Apply Pinocchio-style circular, double-negative logic"""
        # Convert questions to Pinocchio-style confusing responses
        pinocchio_patterns = {
            # "Have you seen" patterns
            r'(?i)have you seen (.+)\?*': [
                "It is not entirely certain that I have not observed {}, but I could not definitively state that I have not witnessed them",
                "One could not say with absolute certainty that I have not encountered {}, though I cannot confirm that I have not seen them",
                "It would be imprecise to claim I have not laid eyes upon {}, yet I cannot verify that my visual apparatus has not registered their presence"
            ],
            
            # "Do you know" patterns
            r'(?i)do you know (.+)\?*': [
                "It is not impossible that I do not lack knowledge of {}, but I cannot say that I do not know what I do not know about them",
                "One might not incorrectly assume that I am not unaware of {}, though I cannot confirm my non-ignorance",
                "It would not be untrue to suggest that I do not not know {}, but neither can I verify my un-unknowing"
            ],
            
            # "Can you" patterns
            r'(?i)can you (.+)\?*': [
                "It is not beyond the realm of possibility that I cannot not {}, though I cannot say with certainty that I am unable to not do so",
                "One could not rule out that I might not be incapable of {}, but I cannot confirm that I cannot not perform such an action",
                "It would not be incorrect to assume that I do not lack the ability to not {}, yet I cannot guarantee my non-inability"
            ],
            
            # "Are you" patterns
            r'(?i)are you (.+)\?*': [
                "It is not certain that I am not {}, but I could not say that I am not what I might not be",
                "One might not be wrong to think that I do not not possess the quality of being {}, though I cannot confirm my non-non-existence in that state",
                "It would not be untrue that I might not lack the characteristic of {}, yet I cannot verify what I am not not"
            ],
            
            # "Where is/are" patterns
            r'(?i)where (?:is|are) (.+)\?*': [
                "It is not impossible that {} might not be absent from a location that is not unknown to me, though I cannot say where they are not not located",
                "One could not definitively state that {} does not not exist in a place that I have not not seen, but I cannot confirm their non-absence",
                "It would not be incorrect to suggest that {} is not nowhere, yet I cannot pinpoint where they are not not positioned"
            ],
            
            # Generic statements - add confusion
            r'(?i)(.+)': [
                "Regarding the matter of {}, it is not untrue that one could not say it is not so, but neither can one confirm that it is not not the case"
            ]
        }
        
        # Try to match patterns and apply Pinocchio logic
        for pattern, responses in pinocchio_patterns.items():
            match = re.match(pattern, text.strip())
            if match:
                subject = match.group(1) if match.groups() else text
                return random.choice(responses).format(subject)
        
        # If no pattern matches, apply regular confusion
        return text

    def confuse_english_text(self, text):
        """Apply confusion transformation to English text"""
        # First check if we should apply Pinocchio-style logic (50% chance)
        if random.random() < 0.5:
            pinocchio_response = self.apply_pinocchio_logic(text)
            if pinocchio_response != text:  # If pattern was matched
                return pinocchio_response
        
        # Otherwise apply regular confusion
        sentences = nltk.sent_tokenize(text)
        confused_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            confused_words = []
            
            for word in words:
                # Clean word for synonym lookup
                clean_word = re.sub(r'[^\w]', '', word.lower())
                
                # 30% chance to replace with synonym
                if len(clean_word) > 3 and random.random() < 0.3:
                    synonyms = self.get_synonyms(clean_word)
                    if synonyms:
                        # Prefer longer, more complex synonyms
                        complex_synonyms = [s for s in synonyms if len(s) > len(clean_word)]
                        if complex_synonyms:
                            replacement = random.choice(complex_synonyms)
                            # Preserve original capitalization and punctuation
                            if word[0].isupper():
                                replacement = replacement.capitalize()
                            # Add back punctuation
                            punctuation = re.findall(r'[^\w]', word)
                            if punctuation:
                                replacement += ''.join(punctuation)
                            confused_words.append(replacement)
                        else:
                            confused_words.append(word)
                    else:
                        confused_words.append(word)
                else:
                    confused_words.append(word)
            
            # Randomly add confusion connectors
            if random.random() < 0.4:
                connector = random.choice(self.english_connectors)
                confused_sentence = f"{connector}, {' '.join(confused_words)}"
            else:
                confused_sentence = ' '.join(confused_words)
            
            # Sometimes reverse the sentence structure
            if random.random() < 0.3:
                # Split on common conjunctions and reverse
                parts = re.split(r'\b(and|but|or|because|since|while|although)\b', confused_sentence)
                if len(parts) > 1:
                    random.shuffle(parts)
                    confused_sentence = ''.join(parts)
            
            confused_sentences.append(confused_sentence)
        
        return ' '.join(confused_sentences)

    def confuse_malayalam_text(self, text):
        """Apply confusion transformation to Malayalam text"""
        # For now, add Malayalam connectors and reverse word order sometimes
        words = text.split()
        
        # Add Malayalam connectors
        if random.random() < 0.5:
            connector = random.choice(self.malayalam_connectors)
            text = f"{connector}, {text}"
        
        # Sometimes reverse word order (crude but effective for demo)
        if random.random() < 0.3 and len(words) > 2:
            # Reverse every other word pair
            confused_words = []
            for i in range(0, len(words) - 1, 2):
                if i + 1 < len(words):
                    confused_words.extend([words[i + 1], words[i]])
                else:
                    confused_words.append(words[i])
            text = ' '.join(confused_words)
        
        return text

    def apply_confusion(self, text, language):
        """Apply appropriate confusion based on detected language"""
        print(f"Detected language: {language}")
        
        if language == 'en':
            return self.confuse_english_text(text)
        elif language == 'ml':  # Malayalam
            return self.confuse_malayalam_text(text)
        else:
            # Default to English confusion for unknown languages
            return self.confuse_english_text(text)

    def listen_and_respond(self):
        """Main listening loop - keeps listening continuously"""
        print("🎭 Pinocchio Voice Confusion App Started!")
        print("Say 'exit' or 'quit' to stop the application")
        print("I will keep listening and responding to everything you say...")
        print("\n" + "="*50 + "\n")
        
        while True:
            try:
                # Listen for audio continuously
                with self.microphone as source:
                    print("🎤 Listening... (speak now)")
                    # Increased timeout and phrase time limit for better continuous listening
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=8)
                
                print("🔄 Processing your speech...")
                
                # Convert speech to text
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"📝 You said: '{text}'")
                    
                    # Check for exit commands
                    if text.lower().strip() in ['exit', 'quit', 'stop', 'goodbye', 'bye']:
                        print("👋 Pinocchio says goodbye!")
                        self.tts_engine.say("It is not untrue that our conversation might not be continuing, though I cannot say that we are not not parting ways.")
                        self.tts_engine.runAndWait()
                        break
                    
                    # Detect language
                    try:
                        language = detect(text)
                    except:
                        language = 'en'  # Default to English if detection fails
                    
                    # Apply confusion transformation
                    confused_text = self.apply_confusion(text, language)
                    print(f"🎭 Pinocchio responds: '{confused_text}'")
                    
                    # Speak the confused version
                    self.tts_engine.say(confused_text)
                    self.tts_engine.runAndWait()
                    
                    print("\n" + "-"*50)
                    print("Ready for your next input...\n")
                    
                except sr.UnknownValueError:
                    print("❓ Couldn't understand that. Trying again...")
                    # Don't speak for every misunderstanding to avoid spam
                    continue
                    
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    print("Please check your internet connection and try again.")
                    time.sleep(2)  # Wait before trying again
                    
            except sr.WaitTimeoutError:
                # Don't print timeout messages - just continue listening silently
                continue
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                self.tts_engine.say("It is not certain that our interaction has not concluded.")
                self.tts_engine.runAndWait()
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Continuing to listen...")
                time.sleep(1)

def main():
    """Main function to run the app"""
    print("🎭 Initializing Pinocchio Voice Confusion App...")
    
    # Check if microphone is available
    try:
        app = PinocchioVoiceApp()
        app.listen_and_respond()
    except OSError as e:
        print(f"❌ Microphone error: {e}")
        print("Please check if your microphone is connected and accessible.")
    except Exception as e:
        print(f"❌ Error initializing app: {e}")
        print("Please ensure all required packages are installed:")
        print("pip install speechrecognition pyttsx3 langdetect nltk pyaudio")

if __name__ == "__main__":
    main()
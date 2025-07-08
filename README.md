# 🧠 Propaganda Detector

A machine learning system to detect propaganda in news articles using a hybrid backend (Python) and demo frontend (Java GUI). Built for a university course on applied AI.

---

## ⚙️ How It Works

The system uses the OpenAI GPT-3.5-turbo model as a semantic encoder to process input articles and extract sentence-level features. These are then passed to a neural network built with TensorFlow/Keras to classify whether the article contains propaganda techniques.

---

## 🧪 Technologies Used

- **Python 3.10** (backend)
- **TensorFlow + Keras** (neural network)
- **OpenAI API** (semantic encoding)
- **spaCy + VADER** (NLP and sentiment features)
- **Java (JDK 20) + JavaFX** (GUI demo)
- **Sklearn, NumPy, Pathlib, dotenv**

---

## 🖥️ Running the Classifier (Backend)

Make sure you have Python 3.10 and all dependencies installed.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Run the classifier from the terminal:**
   ```bash
   python3 -m ANN.classify
   ```

---

## 🧪 File Structure

```
.
├── code/
│   ├── ANN/                       # Neural network code and model weights
│   ├── DATA/                      # Numpy arrays with test/train labels
│   ├── DATASETS/                  # Processed input feature vectors
│   ├── evaluators/                # Propaganda technique evaluators
│   ├── gui/                       # Java files for GUI (JavaFX)
│   ├── src/, target/, build/      # Java build structure
│   └── Main.py                    # Central script (if needed for integration)
├── demo/
│   ├── propaganda_example.png     # Screenshot of propaganda result
│   └── neutral_example.png        # Screenshot of neutral result
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── Propaganda_Detector_Report.pdf # University report
```

---

## 🧪 Optional (Java GUI Demo)

To run the GUI demo (JavaFX-based):
1. Make sure Java JDK 20 is installed.
2. Compile and run the Java code in `code/gui` or via the `Main.java` file.

You can test with demo texts to visualize classification results interactively.
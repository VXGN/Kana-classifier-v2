tensorflow
opencv-python
numpy
pandas
matplotlib
seaborn
scikit-learn
tqdm

# **Doka 🦉 Katakana Classifier**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![License](https://img.shields.io/github/license/yourusername/yourrepo?color=blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

<p align="center">
	<img src="https://em-content.zobj.net/source/microsoft-teams/363/owl_1f989.png" width="80" alt="Owl"/>
</p>

**DoitsuKa** (ドイツカ) is a fun, interactive web app for recognizing and learning to distinguish tricky Katakana characters (シ, ツ, ン, ソ, ノ, メ) using your webcam and a deep learning model. Inspired by Duolingo's playful style!

---

## 🚀 Features

- 📷 **Webcam-based Katakana recognition**
- 🦉 **Intuitive, Duolingo-inspired UI** (dark mode, glassmorphism, green highlights)
- 🔬 **See what the model sees**: view both your captured and preprocessed (64x64 grayscale) images
- ⚡ **Instant feedback** with confidence scores
- 🖼️ **Dataset & model included** for easy retraining

---

## 🛠️ Requirements

```
tensorflow
opencv-python
numpy
flask
```

---

## 📦 Project Structure

```
├── app.py                # Flask backend
├── model/
│   └── kana_classifier.h5
├── static/
│   ├── style.css         # All styles
│   └── script.js         # All JS
├── templates/
│   └── index.html        # Main UI
├── Datasets/             # Training/test images
│   ├── shi/ tsu/ n/ so/ no/ me/
│   └── ...
└── Training/             # Training scripts/notebooks
```

---

## 🖥️ Usage

1. **Install dependencies**
	 ```bash
	 pip install -r requirements.txt
	 ```
2. **Run the app**
	 ```bash
	 python app.py
	 ```
3. **Open in browser**: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✨ Demo

<p align="center">
	<img src="https://user-images.githubusercontent.com/yourusername/demo.gif" width="400" alt="DoitsuKa Demo"/>
</p>

---

## 📚 Acknowledgements

- Inspired by [Duolingo](https://www.duolingo.com/)
- Katakana dataset: [etldb](http://etlcdb.db.aist.go.jp/the-etl-character-database/)
- Model: TensorFlow/Keras CNN

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
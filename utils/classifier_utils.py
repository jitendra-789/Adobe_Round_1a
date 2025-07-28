import joblib #type: ignore
import numpy as np # type: ignore

class HeadingClassifier:
    def __init__(self, model_path="models/heading_classifier.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, lines):
        features = []
        for line in lines:
            features.append([
                line["font_size"],
                line["page"],
                line["x0"],
                line["y0"],
                line["x1"],
                line["y1"],
                len(line["text"]),
                int(line["text"][0].isupper()),
                int(line["text"].endswith(":"))
            ])
        return self.model.predict(np.array(features))
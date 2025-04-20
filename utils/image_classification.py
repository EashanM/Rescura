from transformers import pipeline
from PIL import Image

# You can use a more specialized model if available
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify_condition(image_path: str):
    image = Image.open(image_path)
    results = classifier(image)
    # Get top prediction
    top = results[0]
    label = top['label']
    score = top['score']
    return label, score, results

if __name__ == "__main__":
    image_path = "data/trial_inputs/Image/image-56a2f5615f9b58b7d0cfdf44.jpg"  # Replace with your image path
    label, score, results = classify_condition(image_path)
    print(f"Label: {label}, Score: {score}")
    print("All results:", results)
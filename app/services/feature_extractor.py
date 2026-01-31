"""
Feature Extractor - Extracts features from images and text
Uses DINOv2, SIFT, BGE Reranker
"""
import torch
import cv2
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from rapidfuzz import fuzz
from typing import Tuple, Optional

class FeatureExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔧 Initializing Feature Extractor on {self.device}...")
        
        # DINOv2 for image embeddings
        self.img_processor = AutoImageProcessor.from_pretrained('facebook/dinov2-base')
        self.img_model = AutoModel.from_pretrained('facebook/dinov2-base').to(self.device).eval()
        
        # BGE Reranker for text similarity
        rerank_name = 'BAAI/bge-reranker-v2-m3'
        self.tokenizer = AutoTokenizer.from_pretrained(rerank_name)
        self.reranker = AutoModelForSequenceClassification.from_pretrained(rerank_name).to(self.device).eval()
        
        # SIFT for traditional CV features
        self.sift = cv2.SIFT_create()
        
        print("✅ Feature extractor ready!")
    
    def extract_dino_features(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Extract DINOv2 embeddings and compute cosine similarity
        
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        try:
            # Preprocess images
            inputs = self.img_processor(images=[img1, img2], return_tensors="pt").to(self.device)
            
            # Extract features
            with torch.no_grad():
                outputs = self.img_model(**inputs).last_hidden_state.mean(dim=1)
                feat1, feat2 = outputs[0], outputs[1]
                
                # Cosine similarity
                similarity = torch.nn.functional.cosine_similarity(feat1.unsqueeze(0), feat2.unsqueeze(0))
                
            return float(similarity.cpu().numpy()[0])
        
        except Exception as e:
            print(f"⚠️ DINOv2 extraction error: {e}")
            return 0.5  # Default neutral score
    
    def extract_sift_features(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Extract SIFT keypoints and compute matching score
        
        Returns:
            SIFT match score (0.0 to 1.0)
        """
        try:
            # Convert to grayscale
            cv_img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2GRAY)
            cv_img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
            
            # Detect keypoints
            kp1, des1 = self.sift.detectAndCompute(cv_img1, None)
            kp2, des2 = self.sift.detectAndCompute(cv_img2, None)
            
            if des1 is None or des2 is None:
                return 0.0
            
            # Match keypoints using KNN
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            
            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            
            # Compute score
            if len(kp1) > 0:
                score = min((len(good_matches) / len(kp1)) * 10, 1.0)
            else:
                score = 0.0
            
            return float(score)
        
        except Exception as e:
            print(f"⚠️ SIFT extraction error: {e}")
            return 0.0
    
    def extract_text_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic text similarity using BGE Reranker
        
        Returns:
            Text similarity score (0.0 to 1.0)
        """
        try:
            # Tokenize
            inputs = self.tokenizer(
                [(text1, text2)],
                padding=True,
                truncation=True,
                return_tensors='pt'
            ).to(self.device)
            
            # Get similarity score
            with torch.no_grad():
                logits = self.reranker(**inputs).logits.view(-1)
                score = torch.sigmoid(logits)
            
            return float(score.cpu().numpy()[0])
        
        except Exception as e:
            print(f"⚠️ Text similarity error: {e}")
            return 0.5
    
    def extract_item_name_similarity(self, item_name: str, description: str) -> float:
        """
        Compute fuzzy match between item name and description
        
        Returns:
            Fuzzy match score (0.0 to 1.0)
        """
        try:
            score = fuzz.token_set_ratio(item_name.lower(), description.lower()) / 100.0
            return float(score)
        except:
            return 0.5
    
    def extract_color_match(self, desc1: str, desc2: str) -> float:
        """
        Check if same color keywords appear in both descriptions
        
        Returns:
            1.0 if color match, 0.5 otherwise
        """
        colors = ['red', 'blue', 'black', 'white', 'green', 'yellow', 
                  'pink', 'purple', 'brown', 'orange', 'gray', 'grey',
                  'লাল', 'নীল', 'কালো', 'সাদা', 'সবুজ', 'হলুদ']  # Bangla colors too
        
        desc1_lower = desc1.lower()
        desc2_lower = desc2.lower()
        
        for color in colors:
            if color in desc1_lower and color in desc2_lower:
                return 1.0
        
        return 0.5
    
    def extract_all_features(
        self,
        img1: Image.Image,
        img2: Image.Image,
        text1: str,
        text2: str,
        item_name: str
    ) -> np.ndarray:
        """
        Extract all features for a pair of items
        
        Returns:
            Feature vector: [dino_sim, sift_sim, text_sim, item_sim, color_match]
        """
        dino_sim = self.extract_dino_features(img1, img2)
        sift_sim = self.extract_sift_features(img1, img2)
        text_sim = self.extract_text_similarity(text1, text2)
        item_sim = self.extract_item_name_similarity(item_name, text2)
        color_match = self.extract_color_match(text1, text2)
        
        features = np.array([dino_sim, sift_sim, text_sim, item_sim, color_match])
        
        return features

# Singleton instance
feature_extractor = FeatureExtractor()
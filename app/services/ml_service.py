"""
ML Service - Loads trained XGBoost model and performs inference
"""


from anyio import Path
import torch


class MLService:
    def __init__(self, model_dir: str = "ml_models"):
        self.model_dir = Path(model_dir)
        self.model = None
        self.threshold = 0.5
        self.metadata = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self._load_model()
    
    def _load_model(self):
        """Load trained XGBoost model and metadata"""
        try:
            # Load XGBoost model
            model_path = self.model_dir / "xgboost_model.pkl"
            self.model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
            
            # Load threshold
            threshold_path = self.model_dir / "best_threshold.txt"
            if threshold_path.exists():
                self.threshold = float(threshold_path.read_text().strip())
                print(f"✅ Threshold loaded: {self.threshold:.4f}")
            
            # Load metadata
            metadata_path = self.model_dir / "model_metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    self.metadata = json.load(f)
                print(f"✅ Model metadata loaded")
                print(f"   Training date: {self.metadata.get('training_date')}")
                print(f"   Test accuracy: {self.metadata.get('test_accuracy', 0)*100:.2f}%")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def predict(self, features: np.ndarray) -> Tuple[int, float]:
        """
        Predict if two items match
        
        Args:
            features: [dino_sim, sift_sim, text_sim, item_sim, color_match]
        
        Returns:
            (prediction, confidence)
            prediction: 0 (no match) or 1 (match)
            confidence: probability score (0.0 to 1.0)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Ensure features is 2D array
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        # Get probability predictions
        proba = self.model.predict_proba(features)[0, 1]
        
        # Apply threshold
        prediction = 1 if proba >= self.threshold else 0
        
        return prediction, float(proba)
    
    def batch_predict(self, features_list: List[np.ndarray]) -> List[Tuple[int, float]]:
        """
        Predict for multiple feature sets
        
        Args:
            features_list: List of feature arrays
        
        Returns:
            List of (prediction, confidence) tuples
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Stack features
        X = np.vstack(features_list)
        
        # Get probabilities
        probas = self.model.predict_proba(X)[:, 1]
        
        # Apply threshold
        predictions = (probas >= self.threshold).astype(int)
        
        return list(zip(predictions.tolist(), probas.tolist()))
    
    def get_model_info(self) -> Dict:
        """Get model metadata"""
        return {
            "model_loaded": self.model is not None,
            "threshold": self.threshold,
            "device": self.device,
            "metadata": self.metadata
        }

# Singleton instance
ml_service = MLService()
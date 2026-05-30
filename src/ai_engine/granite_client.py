"""
Dual AI Client — SubMindsAI custom deployment + Llama 4 Maverick (parallel)
Deep image analysis with emoji emotion mapping
"""
import os
import re
import time
import logging
import threading
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json

try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    IBM_WML_AVAILABLE = True
except ImportError:
    IBM_WML_AVAILABLE = False
    logging.warning("ibm-watsonx-ai not available — run: pip install ibm-watsonx-ai")

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Emotion → Emoji mapping ───────────────────────────────────────────────────
EMOTION_EMOJI = {
    "joyful":            "😄",
    "happy":             "😊",
    "content":           "🙂",
    "excited":           "🤩",
    "confident":         "😎",
    "focused":           "🧐",
    "intensely_focused": "🔥",
    "contemplative":     "🤔",
    "neutral":           "😐",
    "calm":              "😌",
    "tired":             "😴",
    "distant":           "😶",
    "anxious":           "😰",
    "stressed":          "😤",
    "fearful":           "😨",
    "angry":             "😠",
    "sad":               "😢",
    "surprised":         "😲",
    "disgusted":         "🤢",
    "no_face":           "🚫",
    "unknown":           "❓",
    "error":             "⚠️",
}

# Deployment ID for the custom SubMindsAI prompt-template deployment
SUBMINDS_DEPLOYMENT_ID = "019e77db-031e-722c-aa9d-2ed020542403"
LLAMA_MODEL_ID         = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"


def get_emotion_emoji(emotion: str) -> str:
    """Return emoji for a given emotion string."""
    key = emotion.lower().replace(" ", "_")
    return EMOTION_EMOJI.get(key, EMOTION_EMOJI.get(key.split("_")[0], "🧠"))


def extract_image_features(image_path: str) -> Dict[str, Any]:
    """
    Run deep OpenCV feature extraction on an image.
    Returns a rich feature dict used as input to both AI models.
    """
    features = {
        "file": Path(image_path).name,
        "face_count": 0,
        "eye_count": 0,
        "smile_detected": False,
        "mean_brightness": 0.0,
        "brightness_std": 0.0,
        "width": 0,
        "height": 0,
        "face_size_ratio": 0.0,
        "dominant_region": "unknown",
        "edge_density": 0.0,
    }
    try:
        import cv2
        import numpy as np

        frame = cv2.imread(str(image_path))
        if frame is None:
            return features

        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        features["width"] = w
        features["height"] = h
        features["mean_brightness"] = float(np.mean(gray))
        features["brightness_std"] = float(np.std(gray))

        # Edge density (Canny) — indicates tension/activity in the frame
        edges = cv2.Canny(gray, 50, 150)
        features["edge_density"] = float(np.sum(edges > 0) / (h * w))

        # Face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        features["face_count"] = len(faces)

        if len(faces) > 0:
            # Use the largest face
            x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
            features["face_size_ratio"] = round((fw * fh) / (w * h), 4)

            face_roi = gray[y:y+fh, x:x+fw]

            eye_cascade   = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
            smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

            eyes   = eye_cascade.detectMultiScale(face_roi, 1.1, 5)
            smiles = smile_cascade.detectMultiScale(face_roi, 1.8, 20, minSize=(25, 25))

            features["eye_count"]      = len(eyes)
            features["smile_detected"] = len(smiles) > 0

            # Dominant image region (upper/lower/left/right brightness split)
            top_half    = float(np.mean(gray[:h//2, :]))
            bottom_half = float(np.mean(gray[h//2:, :]))
            features["dominant_region"] = "upper" if top_half > bottom_half else "lower"

    except Exception as e:
        logger.warning(f"OpenCV feature extraction failed: {e}")

    return features


def features_to_description(f: Dict[str, Any]) -> str:
    """Convert feature dict to a rich natural-language description for the LLM."""
    smile  = "yes" if f["smile_detected"] else "no"
    bright = "bright" if f["mean_brightness"] > 160 else ("dark" if f["mean_brightness"] < 80 else "moderate")
    tension = "high" if f["edge_density"] > 0.15 else ("moderate" if f["edge_density"] > 0.07 else "low")
    return (
        f"Image: {f['file']} ({f['width']}x{f['height']}px). "
        f"Lighting: {bright} (mean={f['mean_brightness']:.1f}, std={f['brightness_std']:.1f}). "
        f"Faces detected: {f['face_count']}. Eyes visible: {f['eye_count']}. "
        f"Smile: {smile}. Face-to-frame ratio: {f['face_size_ratio']:.3f}. "
        f"Visual tension/activity level: {tension} (edge density={f['edge_density']:.3f}). "
        f"Dominant image region: {f['dominant_region']}."
    )


class GraniteAIClient:
    """
    Dual AI client:
      • SubMindsAI  — your custom WatsonX deployment (prompt-template tuned)
      • Llama 4 Maverick — raw foundation model for deep independent analysis
    Both run in parallel threads; results are merged and returned together.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        space_id: Optional[str] = None,
        url: str = "https://us-south.ml.cloud.ibm.com",
    ):
        self.url        = url
        self.api_key    = api_key or os.getenv("IBM_CLOUD_API_KEY")
        self.project_id = project_id or os.getenv("IBM_PROJECT_ID")
        self.space_id   = space_id or os.getenv("IBM_SPACE_ID")

        # Sanitise placeholder values
        for attr in ("project_id", "space_id"):
            v = getattr(self, attr)
            if isinstance(v, str):
                v = v.strip()
                if not v or (v.startswith("${") and v.endswith("}")):
                    setattr(self, attr, None)

        # Load YAML config
        if config_path and Path(config_path).exists():
            self.config = self._load_config(config_path)
        else:
            self.config = self._default_config()

        self.url = self.config.get("url", self.url)

        # Two separate model handles
        self.subminds_model: Optional[Any] = None   # custom deployment
        self.llama_model:    Optional[Any] = None   # direct foundation model

        if IBM_WML_AVAILABLE and self.api_key and (self.project_id or self.space_id):
            self._init_models()
        else:
            logger.warning("WatsonX credentials missing — running in mock mode.")

        # Stats
        self.request_count = 0
        self.error_count   = 0
        self.total_tokens  = 0

    # ── Config helpers ────────────────────────────────────────────────────────

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            if not YAML_AVAILABLE:
                return self._default_config()
            with open(path, "r") as f:
                cfg = yaml.safe_load(f)
            if "ibm_granite" in cfg:
                cfg = cfg["ibm_granite"]
            return self._resolve_env(cfg)
        except Exception as e:
            logger.error(f"Config load error: {e}")
            return self._default_config()

    def _resolve_env(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._resolve_env(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._resolve_env(v) for v in obj]
        if isinstance(obj, str):
            resolved = re.sub(r"\$\{([^}]+)\}", lambda m: os.getenv(m.group(1), ""), obj)
            return resolved or None
        return obj

    def _default_config(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "model": {"id": LLAMA_MODEL_ID},
            "parameters": {"max_tokens": 2000, "temperature": 0.7, "top_p": 0.9},
            "rate_limits": {"retry_attempts": 3, "retry_delay": 2},
        }

    # ── Model initialisation ──────────────────────────────────────────────────

    def _init_models(self):
        creds = Credentials(url=self.url, api_key=self.api_key)
        params = {
            "max_new_tokens": self.config["parameters"].get("max_tokens", 2000),
            "temperature":    self.config["parameters"].get("temperature", 0.7),
            "top_p":          self.config["parameters"].get("top_p", 0.9),
        }
        scope = {"space_id": self.space_id} if self.space_id else {"project_id": self.project_id}

        # 1. SubMindsAI custom deployment
        try:
            self.subminds_model = ModelInference(
                deployment_id=SUBMINDS_DEPLOYMENT_ID,
                credentials=creds,
                params=params,
                **scope,
            )
            logger.info("SubMindsAI custom deployment initialised ✓")
        except Exception as e:
            logger.error(f"SubMindsAI deployment init failed: {e}")

        # 2. Llama 4 Maverick direct
        try:
            self.llama_model = ModelInference(
                model_id=LLAMA_MODEL_ID,
                credentials=creds,
                params=params,
                **scope,
            )
            logger.info("Llama 4 Maverick model initialised ✓")
        except Exception as e:
            logger.error(f"Llama 4 Maverick init failed: {e}")

    def is_available(self) -> bool:
        return self.subminds_model is not None or self.llama_model is not None

    # ── Parallel generation ───────────────────────────────────────────────────

    def _call_model(self, model, prompt: str, label: str) -> Tuple[str, str]:
        """Call a single model and return (label, response_text)."""
        retries    = self.config["rate_limits"].get("retry_attempts", 3)
        retry_delay = self.config["rate_limits"].get("retry_delay", 2)
        for attempt in range(retries):
            try:
                resp = model.generate_text(prompt=prompt)
                return label, resp
            except Exception as e:
                logger.warning(f"[{label}] attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
        return label, ""

    def _parallel_generate(self, prompt: str) -> Dict[str, str]:
        """
        Fire both models simultaneously in threads.
        Returns {"subminds": "...", "llama": "..."}.
        """
        results: Dict[str, str] = {}

        def run(model, label):
            if model:
                _, text = self._call_model(model, prompt, label)
                results[label] = text
            else:
                results[label] = ""

        t1 = threading.Thread(target=run, args=(self.subminds_model, "subminds"), daemon=True)
        t2 = threading.Thread(target=run, args=(self.llama_model,    "llama"),    daemon=True)
        t1.start(); t2.start()
        t1.join();  t2.join()
        return results

    # ── Deep image analysis ───────────────────────────────────────────────────

    def analyze_image(
        self,
        image_path: str,
        analysis_type: str = "facial_expression",
        additional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deep image analysis using both models in parallel.
        OpenCV extracts rich features; both LLMs interpret them independently.
        """
        try:
            features    = extract_image_features(image_path)
            description = features_to_description(features)

            ctx = f"\nAdditional context: {additional_context}" if additional_context else ""

            prompt = f"""You are an expert sports psychologist and neuroscientist specialising in F1 driver performance.

DEEP IMAGE ANALYSIS DATA:
{description}{ctx}

Perform a thorough psychological analysis covering:
1. PRIMARY EMOTION — identify the single dominant emotion with intensity (0.0–1.0)
2. SECONDARY EMOTIONS — up to 3 additional emotions present with intensities
3. MICRO-EXPRESSION SIGNALS — subtle facial cues and what they reveal subconsciously
4. STRESS & AROUSAL LEVEL — rate 1–10 and explain physiological indicators
5. COGNITIVE STATE — focus, decision-readiness, mental fatigue assessment
6. SUBCONSCIOUS DRIVERS — hidden motivations or anxieties visible in the expression
7. PERFORMANCE IMPACT — how this emotional state affects racing performance RIGHT NOW
8. ACTIONABLE RECOMMENDATIONS — 3 specific mental coaching interventions

Respond ONLY with valid JSON using these exact keys:
{{
  "primary_emotion": {{"name": "...", "intensity": 0.0}},
  "secondary_emotions": [{{"name": "...", "intensity": 0.0}}],
  "micro_expressions": ["..."],
  "stress_level": 0,
  "arousal_level": 0,
  "cognitive_state": "...",
  "subconscious_drivers": ["..."],
  "performance_impact": "...",
  "recommendations": ["...", "...", "..."]
}}"""

            if self.subminds_model or self.llama_model:
                raw = self._parallel_generate(prompt)
            else:
                raw = {"subminds": self._mock_image_response(), "llama": self._mock_image_response()}

            subminds_parsed = self._parse_json(raw.get("subminds", ""))
            llama_parsed    = self._parse_json(raw.get("llama", ""))

            # Merge: llama is primary, subminds fills gaps
            merged = {**subminds_parsed, **{k: v for k, v in llama_parsed.items() if v}}

            # Attach emoji to primary emotion
            primary_name = merged.get("primary_emotion", {})
            if isinstance(primary_name, dict):
                ename = primary_name.get("name", "unknown")
            else:
                ename = str(primary_name)
            merged["emotion_emoji"] = get_emotion_emoji(ename)

            self.request_count += 1
            return {
                "timestamp":        time.time(),
                "image_path":       str(image_path),
                "image_features":   features,
                "subminds_raw":     raw.get("subminds", ""),
                "llama_raw":        raw.get("llama", ""),
                "subminds_result":  subminds_parsed,
                "llama_result":     llama_parsed,
                "merged":           merged,
            }

        except Exception as e:
            logger.error(f"analyze_image error: {e}")
            self.error_count += 1
            return self._error_response(str(e))

    # ── Subconscious pattern analysis ────────────────────────────────────────

    def analyze_subconscious_patterns(
        self,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any],
        art_analysis: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run dual-model subconscious pattern analysis and return merged insights."""
        try:
            prompt = self._build_pattern_prompt(facial_data, telemetry, art_analysis, context)

            if self.subminds_model or self.llama_model:
                raw = self._parallel_generate(prompt)
            else:
                raw = {
                    "subminds": self._mock_pattern_response(facial_data, telemetry),
                    "llama":    self._mock_pattern_response(facial_data, telemetry),
                }

            subminds_parsed = self._parse_json(raw.get("subminds", ""))
            llama_parsed    = self._parse_json(raw.get("llama", ""))
            merged          = {**subminds_parsed, **{k: v for k, v in llama_parsed.items() if v}}

            # Emoji for dominant emotion
            emotion = facial_data.get("dominant_emotion", "neutral")
            emoji   = get_emotion_emoji(emotion)

            self.request_count += 1
            return {
                "timestamp":        time.time(),
                "emotion_emoji":    emoji,
                "dominant_emotion": emotion,
                "emotional_state":  merged.get("emotional_state", f"{emoji} {emotion.replace('_', ' ').title()}"),
                "stress_analysis":  merged.get("stress_analysis", ""),
                "decision_patterns": merged.get("decision_patterns", []),
                "recommendations":  merged.get("recommendations", []),
                "predictions":      merged.get("predictions", []),
                "subminds_insight": subminds_parsed,
                "llama_insight":    llama_parsed,
                "raw_subminds":     raw.get("subminds", ""),
                "raw_llama":        raw.get("llama", ""),
            }

        except Exception as e:
            logger.error(f"analyze_subconscious_patterns error: {e}")
            self.error_count += 1
            return self._error_response(str(e))

    def _build_pattern_prompt(self, facial_data, telemetry, art_analysis, context) -> str:
        emotion = facial_data.get("dominant_emotion", "unknown")
        emoji   = get_emotion_emoji(emotion)
        prompt  = f"""You are an expert F1 sports psychologist. Analyse the driver's subconscious state.

FACIAL DATA:
- Dominant emotion: {emoji} {emotion}
- Confidence: {facial_data.get('confidence', 0):.2f}
- Valence: {facial_data.get('valence', 0):.2f}  (−1=negative, +1=positive)
- Arousal: {facial_data.get('arousal', 0):.2f}  (0=calm, 1=excited)
- Stress level: {facial_data.get('stress_level', 0)}/10

TELEMETRY:
- Speed: {telemetry.get('speed', 0):.1f} km/h
- Steering: {telemetry.get('steering', 0):.3f}
- Track position: {telemetry.get('track_position', 0):.3f}
"""
        if art_analysis:
            prompt += f"\nART ANALYSIS: {art_analysis}\n"
        if context:
            prompt += f"\nCONTEXT: {context}\n"

        prompt += """
Respond ONLY with valid JSON:
{
  "emotional_state": "one-sentence summary with emoji",
  "stress_analysis": "detailed stress assessment",
  "decision_patterns": ["pattern1", "pattern2", "pattern3"],
  "recommendations": ["rec1", "rec2", "rec3"],
  "predictions": ["prediction1", "prediction2"]
}"""
        return prompt

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Extract and parse the first JSON object found in text."""
        if not text:
            return {}
        try:
            start = text.index("{")
            end   = text.rindex("}") + 1
            return json.loads(text[start:end])
        except Exception:
            return {}

    def _mock_pattern_response(self, facial_data: Dict, telemetry: Dict) -> str:
        emotion = facial_data.get("dominant_emotion", "neutral")
        emoji   = get_emotion_emoji(emotion)
        speed   = telemetry.get("speed", 0)
        return json.dumps({
            "emotional_state":   f"{emoji} Driver is {emotion.replace('_', ' ')} — monitoring closely",
            "stress_analysis":   "Moderate stress. Breathing pattern suggests manageable tension.",
            "decision_patterns": [f"Consistent inputs at {speed:.0f} km/h", "Reactive steering", "Controlled braking"],
            "recommendations":   ["Box breathing — 4s in, 4s hold, 4s out", "Narrow focus to next corner only", "Relax grip pressure"],
            "predictions":       ["Stable performance for next 2 laps", "Watch for stress spike under pressure"],
        })

    def _mock_image_response(self) -> str:
        return json.dumps({
            "primary_emotion":      {"name": "focused", "intensity": 0.75},
            "secondary_emotions":   [{"name": "calm", "intensity": 0.4}, {"name": "confident", "intensity": 0.3}],
            "micro_expressions":    ["slight brow furrow", "steady gaze", "relaxed jaw"],
            "stress_level":         5,
            "arousal_level":        6,
            "cognitive_state":      "Alert and task-focused",
            "subconscious_drivers": ["Achievement motivation", "Competitive drive"],
            "performance_impact":   "Current state supports optimal lap time execution",
            "recommendations":      ["Maintain current breathing rhythm", "Visualise apex entry", "Trust muscle memory"],
        })

    def _error_response(self, msg: str) -> Dict[str, Any]:
        return {
            "timestamp":        time.time(),
            "error":            True,
            "error_message":    msg,
            "emotion_emoji":    "⚠️",
            "emotional_state":  "⚠️ Analysis error",
            "stress_analysis":  "Analysis failed — check logs",
            "decision_patterns": [],
            "recommendations":  ["Retry analysis"],
            "predictions":      [],
        }

    # ── Stats ─────────────────────────────────────────────────────────────────

    def get_statistics(self) -> Dict[str, Any]:
        success_rate = (
            (self.request_count - self.error_count) / self.request_count
            if self.request_count > 0 else 0.0
        )
        return {
            "total_requests":       self.request_count,
            "successful_requests":  self.request_count - self.error_count,
            "failed_requests":      self.error_count,
            "success_rate":         success_rate,
            "subminds_available":   self.subminds_model is not None,
            "llama_available":      self.llama_model is not None,
            "ibm_wml_available":    IBM_WML_AVAILABLE,
        }

    def reset_statistics(self):
        self.request_count = 0
        self.error_count   = 0
        self.total_tokens  = 0

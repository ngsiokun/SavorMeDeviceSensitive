"""
Evidence-Based Mood Nutrition Engine
Scores recipes based on scientific nutrient-mood mappings
"""
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class NutrientTarget:
    """Single nutrient target for a mood"""
    name: str
    unit: str
    min_per_meal: Optional[float] = None
    max_per_meal: Optional[float] = None
    weight: float = 1.0
    note: Optional[str] = None


@dataclass
class MoodDefinition:
    """Complete mood definition with targets and explainers"""
    id: str
    aliases: List[str]
    nutrient_targets: List[NutrientTarget]
    patterns: List[str]
    explainers: List[str]
    contraindications: List[str]
    evidence: Optional[str] = None
    evidence_level: Optional[str] = None


@dataclass
class ScoredRecipe:
    """Recipe with nutrition score and explanations"""
    recipe_id: str
    score: float
    reasons: List[str]
    nutrient_contributions: Dict[str, float]


class MoodNutritionEngine:
    """
    Evidence-based engine that scores recipes based on mood-nutrient science
    
    Based on:
    - Mediterranean diet RCTs (SMILES trial)
    - Omega-3 meta-analyses
    - Iron-fatigue correlations
    - Magnesium-stress studies
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize with mood mapping configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "data" / "mood_mapping.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.version = self.config.get("version", "1.0.0")
        self.moods: Dict[str, MoodDefinition] = {}
        self.nutrient_aliases = self.config.get("nutrient_aliases", {})
        self.patterns = self.config.get("patterns", {})
        self.disclaimers = self.config.get("disclaimers", {})
        
        # Parse mood definitions
        for mood_data in self.config.get("moods", []):
            targets = [
                NutrientTarget(
                    name=t["name"],
                    unit=t["unit"],
                    min_per_meal=t.get("min_per_meal"),
                    max_per_meal=t.get("max_per_meal"),
                    weight=t.get("weight", 1.0),
                    note=t.get("note")
                )
                for t in mood_data["targets"]["nutrients"]
            ]
            
            mood_def = MoodDefinition(
                id=mood_data["id"],
                aliases=mood_data.get("aliases", []),
                nutrient_targets=targets,
                patterns=mood_data["targets"].get("patterns", []),
                explainers=mood_data.get("explainers", []),
                contraindications=mood_data.get("contraindications", []),
                evidence=mood_data.get("evidence"),
                evidence_level=mood_data.get("evidence_level")
            )
            
            self.moods[mood_data["id"]] = mood_def
    
    def aggregate_targets(self, mood_ids: List[str]) -> List[NutrientTarget]:
        """
        Merge nutrient targets from multiple moods
        
        Strategy:
        - Take max of minimums (most restrictive lower bound)
        - Take min of maximums (most restrictive upper bound)
        - Average weights
        """
        mood_defs = [self.moods[mid] for mid in mood_ids if mid in self.moods]
        
        nutrient_bucket: Dict[str, NutrientTarget] = {}
        
        for mood_def in mood_defs:
            for target in mood_def.nutrient_targets:
                if target.name in nutrient_bucket:
                    existing = nutrient_bucket[target.name]
                    
                    # Combine mins (take max)
                    min_val = max(
                        existing.min_per_meal or 0,
                        target.min_per_meal or 0
                    ) or None
                    
                    # Combine maxs (take min)
                    max_val = None
                    if existing.max_per_meal and target.max_per_meal:
                        max_val = min(existing.max_per_meal, target.max_per_meal)
                    elif existing.max_per_meal:
                        max_val = existing.max_per_meal
                    elif target.max_per_meal:
                        max_val = target.max_per_meal
                    
                    # Average weights, cap at 1.0
                    avg_weight = min(1.0, (existing.weight + target.weight) / 2.0)
                    
                    nutrient_bucket[target.name] = NutrientTarget(
                        name=target.name,
                        unit=target.unit,
                        min_per_meal=min_val,
                        max_per_meal=max_val,
                        weight=avg_weight,
                        note=target.note or existing.note
                    )
                else:
                    nutrient_bucket[target.name] = target
        
        return list(nutrient_bucket.values())
    
    def canonicalize_nutrients(self, raw_nutrients: Dict[str, float]) -> Dict[str, float]:
        """
        Convert raw nutrient names to canonical names using alias mapping
        
        Example:
            {"Iron, Fe": 7.5, "dietary_fiber": 9} 
            → {"iron": 7.5, "fiber": 9}
        """
        canonical: Dict[str, float] = {}
        
        for canonical_name, aliases in self.nutrient_aliases.items():
            value = 0.0
            
            # Check all aliases for this nutrient
            for alias in aliases + [canonical_name]:
                if alias in raw_nutrients:
                    value += raw_nutrients[alias]
            
            if value > 0:
                canonical[canonical_name] = value
        
        return canonical
    
    def score_recipe(
        self,
        recipe_nutrients: Dict[str, float],
        mood_ids: List[str]
    ) -> Tuple[float, List[str], Dict[str, float]]:
        """
        Score a recipe based on how well it matches mood nutrient targets
        
        Args:
            recipe_nutrients: Canonical nutrient values per serving
            mood_ids: List of mood IDs (e.g., ["stress", "fatigue"])
        
        Returns:
            (score, reasons, contributions)
            - score: 0-1+ overall match score
            - reasons: Human-readable explanations
            - contributions: Per-nutrient scores
        """
        targets = self.aggregate_targets(mood_ids)
        
        if not targets:
            return (0.0, ["No mood targets found"], {})
        
        total_weight = sum(t.weight for t in targets)
        weighted_sum = 0.0
        reasons = []
        contributions = {}
        
        for target in targets:
            value = recipe_nutrients.get(target.name, 0.0)
            contrib = 0.0
            
            # Calculate contribution based on target type
            if target.min_per_meal is not None and target.max_per_meal is not None:
                # Range target: reward being in range, slight bonus for being centered
                if target.min_per_meal <= value <= target.max_per_meal:
                    mid = (target.min_per_meal + target.max_per_meal) / 2.0
                    closeness = 1.0 - min(1.0, abs(value - mid) / max(mid, 1.0))
                    contrib = 0.75 + 0.5 * closeness  # 0.75 to 1.25
                elif value > target.max_per_meal:
                    # Overshoot gets some credit but penalty
                    contrib = 0.6
                else:
                    # Under minimum
                    contrib = min(1.25, value / max(target.min_per_meal, 1e-6))
            
            elif target.min_per_meal is not None:
                # Minimum only: scale up to 1.25 for exceeding
                contrib = min(1.25, value / max(target.min_per_meal, 1e-6))
            
            elif target.max_per_meal is not None:
                # Maximum only: penalize exceeding
                if value <= target.max_per_meal:
                    contrib = 1.0
                else:
                    contrib = max(0.3, target.max_per_meal / max(value, 1e-6))
            
            else:
                # No bounds: just check presence
                contrib = 1.0 if value > 0 else 0.0
            
            weighted_sum += contrib * target.weight
            contributions[target.name] = contrib
            
            # Build human-readable reason
            pretty_name = target.name.replace("_", " ").title()
            target_str = ""
            
            if target.min_per_meal and target.max_per_meal:
                target_str = f"{target.min_per_meal:.0f}-{target.max_per_meal:.0f} {target.unit}"
            elif target.min_per_meal:
                target_str = f"≥{target.min_per_meal:.0f} {target.unit}"
            elif target.max_per_meal:
                target_str = f"≤{target.max_per_meal:.0f} {target.unit}"
            
            reason = f"{pretty_name}: {value:.1f} {target.unit}"
            if target_str:
                reason += f" (target: {target_str})"
            if target.note:
                reason += f" — {target.note}"
            
            reasons.append(reason)
        
        # Normalize score
        final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return (final_score, reasons, contributions)
    
    def get_mood_explainers(self, mood_ids: List[str]) -> List[str]:
        """Get evidence-based explainers for selected moods"""
        explainers = []
        for mood_id in mood_ids:
            if mood_id in self.moods:
                mood = self.moods[mood_id]
                explainers.extend(mood.explainers)
                if mood.evidence:
                    explainers.append(f"Evidence: {mood.evidence}")
        return explainers
    
    def get_contraindications(self, mood_ids: List[str]) -> List[str]:
        """Get medical contraindications for selected moods"""
        contraindications = set()
        for mood_id in mood_ids:
            if mood_id in self.moods:
                contraindications.update(self.moods[mood_id].contraindications)
        return list(contraindications)
    
    def get_disclaimer(self, contraindication_type: Optional[str] = None) -> str:
        """Get appropriate medical disclaimer"""
        if contraindication_type and contraindication_type in self.disclaimers:
            return self.disclaimers[contraindication_type]
        return self.disclaimers.get("general", "")


# Singleton instance
_engine_instance: Optional[MoodNutritionEngine] = None

def get_mood_nutrition_engine() -> MoodNutritionEngine:
    """Get or create singleton instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = MoodNutritionEngine()
    return _engine_instance


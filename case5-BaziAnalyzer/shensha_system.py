import json
from typing import Any, Dict, List

class ShenShaRule:
    """
    ShenShaRule encapsulates a single ShenSha (spiritual star) rule.
    
    The JSON structure for a rule should look like:
    [
      {
        "name": "Tianyi Guiren",
        "description": "Based on the rule from Sanming Tonghui: when the day stem is one of [Jia, Wu, Geng] and any pillar's branch is either Chou or Wei, then the rule triggers.",
        "conditions": {
          "day_gan": ["甲", "戊", "庚"],
          "allowed_zhi": ["丑", "未"]
        }
      },
      {
        "name": "Sample ShenSha",
        "description": "A sample rule triggered when the day stem is Yi and any pillar's branch is Zi or Shen.",
        "conditions": {
          "day_gan": ["乙"],
          "allowed_zhi": ["子", "申"]
        }
      }
    ]
    """
    def __init__(self, name: str, description: str, conditions: Dict[str, Any]):
        self.name = name
        self.description = description
        self.conditions = conditions

    def check(self, pillars: Dict[str, Dict[str, str]]) -> bool:
        """
        Check whether this rule is triggered given the four pillars.
        Uses the day stem and checks if any pillar's branch is within allowed_zhi.
        """
        day_gan = pillars.get("day", {}).get("gan", "")
        allowed_zhi = self.conditions.get("allowed_zhi", [])
        if day_gan in self.conditions.get("day_gan", []):
            for pillar in pillars.values():
                if pillar.get("zhi", "") in allowed_zhi:
                    return True
        return False

class ShenShaRuleLoader:
    """
    ShenShaRuleLoader loads rules from already-loaded JSON data (a list of dictionaries).
    """
    def __init__(self, rules_data: List[Dict[str, Any]]):
        self.rules_data = rules_data

    def load_rules(self) -> List[ShenShaRule]:
        rules = []
        for rule_data in self.rules_data:
            rule = ShenShaRule(
                name=rule_data.get("name", ""),
                description=rule_data.get("description", ""),
                conditions=rule_data.get("conditions", {})
            )
            rules.append(rule)
        return rules

class ShenSha:
    """
    The ShenSha system:
      - Contains an internal implementation for Tianyi Guiren.
      - Uses an external JSON data list (loaded into Python) to load additional ShenSha rules.
    """
    def __init__(self, rules_data: List[Dict[str, Any]] = None):
        self.custom_rules: List[ShenShaRule] = []
        if rules_data:
            loader = ShenShaRuleLoader(rules_data)
            self.custom_rules = loader.load_rules()

    def check_tianyi(self, pillars: Dict[str, Dict[str, str]]) -> bool:
        """
        Internal rule for Tianyi Guiren based on a simplified interpretation from Sanming Tonghui.
        For example:
          - Jia, Wu, Geng → corresponding branches Chou, Wei.
          - Yi, Ji   → corresponding branches Zi, Shen.
          - Bing, Ding   → corresponding branches Hai, You.
          - Ren, Gui   → corresponding branches Mao, Si.
          - Xin       → corresponding branches Wu, Chen.
        (The mapping below is an example and can be adjusted to match the exact text.)
        """
        day_gan = pillars.get('day', {}).get('gan', '')
        zhi_list = [v.get('zhi', '') for v in pillars.values()]
        rules = {
            '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
            '乙': ['子', '申'], '己': ['子', '申'],
            '丙': ['亥', '酉'], '丁': ['亥', '酉'],
            '壬': ['卯', '巳'], '癸': ['卯', '巳'],
            '辛': ['午', '寅']
        }
        allowed = rules.get(day_gan, [])
        return any(z in allowed for z in zhi_list)

    def check_custom_shensha(self, pillars: Dict[str, Dict[str, str]]) -> List[str]:
        """
        Checks all loaded external ShenSha rules and returns a list of rule names that trigger.
        """
        triggered = []
        for rule in self.custom_rules:
            if rule.check(pillars):
                triggered.append(rule.name)
        return triggered

    def evaluate(self, pillars: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """
        Evaluates both the internal and external ShenSha rules.
        Returns a dictionary with the results.
        """
        result = {}
        result["天乙贵人"] = self.check_tianyi(pillars)
        result["自定义神煞"] = self.check_custom_shensha(pillars)
        return result

# -------------------------------
# Example usage:
# -------------------------------
if __name__ == '__main__':
    # Example pillars (each pillar has a 'gan' and a 'zhi')
    example_pillars = {
        "year": {"gan": "甲", "zhi": "子"},
        "month": {"gan": "乙", "zhi": "丑"},
        "day": {"gan": "甲", "zhi": "寅"},
        "hour": {"gan": "丙", "zhi": "卯"}
    }

    # Sample JSON data (loaded externally, here defined as a Python list)
    sample_rules_data = [
      {
        "name": "天乙贵人",
        "description": "Based on Sanming Tonghui: when the day stem is one of [甲, 戊, 庚] and any pillar's branch is 丑 or 未.",
        "conditions": {
          "day_gan": ["甲", "戊", "庚"],
          "allowed_zhi": ["丑", "未"]
        }
      },
      {
        "name": "示例神煞",
        "description": "Triggered when the day stem is 乙 and any pillar's branch is 子 or 申.",
        "conditions": {
          "day_gan": ["乙"],
          "allowed_zhi": ["子", "申"]
        }
      },
      {
        "name": "福星高照",
        "description": "Triggered when the day stem is 丙 or 丁 and any pillar's branch is 亥 or 酉, indicating good fortune.",
        "conditions": {
          "day_gan": ["丙", "丁"],
          "allowed_zhi": ["亥", "酉"]
        }
      }
    ]

    # Create the ShenSha system by passing the loaded JSON data directly.
    shensha_system = ShenSha(rules_data=sample_rules_data)

    # Evaluate internal Tianyi Guiren rule.
    tianyi_flag = shensha_system.check_tianyi(example_pillars)
    print("天乙贵人判定:", tianyi_flag)

    # Evaluate external custom ShenSha rules.
    custom_results = shensha_system.check_custom_shensha(example_pillars)
    print("外部规则触发的神煞:", custom_results)

    # Get comprehensive evaluation.
    evaluation = shensha_system.evaluate(example_pillars)
    print("综合神煞判定结果:", evaluation)
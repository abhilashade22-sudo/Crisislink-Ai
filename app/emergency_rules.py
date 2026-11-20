
"""
CrisisLink AI — High-Priority Emergency Rules

These rules run before the normal classifier and Gemini response.
They provide immediate, rule-based safety guidance for emergencies.

Important:
- This module does not call or notify emergency services.
- For emergencies in India, call 112 directly.
- This is not a medically validated triage system.
"""

import re


# -------------------------------------------------------------------
# 1. Emergency responses
# -------------------------------------------------------------------

FIRE_RESPONSE = (
    "FIRE AND SMOKE EMERGENCY:\n"
    "1. If you can reach a safe exit without entering fire or dense smoke, "
    "leave immediately and move away from the building.\n"
    "2. If smoke is present, stay low while moving. Do not use lifts.\n"
    "3. If your escape route is blocked by fire or smoke, do not enter it. "
    "Close the door between you and the fire if possible, block smoke "
    "gaps with available material if safe, and move to a location where "
    "you can signal rescuers.\n"
    "4. Call 112 in India as soon as you can safely do so. Tell the "
    "operator the exact building, floor, room, and whether anyone is trapped.\n"
    "5. Do not return inside for belongings. Follow emergency responders' "
    "instructions.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

BREATHING_RESPONSE = (
    "POSSIBLE BREATHING EMERGENCY:\n"
    "1. Call 112 in India immediately if someone is struggling to breathe "
    "or cannot breathe normally.\n"
    "2. Help the person rest in a position that makes breathing easier. "
    "Do not force them to lie down.\n"
    "3. If choking is suspected, follow the emergency operator's "
    "instructions and seek immediate help.\n"
    "4. If the person becomes unresponsive and is not breathing normally, "
    "tell the emergency operator immediately and follow their CPR instructions.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

UNCONSCIOUS_RESPONSE = (
    "UNCONSCIOUS PERSON:\n"
    "1. Call 112 in India immediately.\n"
    "2. Check whether the person responds and whether they are breathing "
    "normally, if you can do so safely.\n"
    "3. If they are not breathing normally, follow the emergency operator's "
    "CPR instructions.\n"
    "4. If they are unconscious but breathing normally, follow the operator's "
    "instructions. Do not give them food, drink, or medication by mouth.\n"
    "5. Do not move them unless there is immediate danger, such as fire.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

BLEEDING_RESPONSE = (
    "SEVERE BLEEDING:\n"
    "1. Call 112 in India immediately.\n"
    "2. Apply firm, continuous direct pressure to the wound using clean "
    "cloth or gauze if available.\n"
    "3. If blood soaks through, add more material without removing the "
    "original dressing.\n"
    "4. For life-threatening bleeding from an arm or leg, use a commercial "
    "tourniquet only if available and you know how, or follow the emergency "
    "operator's instructions.\n"
    "5. Keep the injured person as still and warm as possible while waiting "
    "for professional help.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

STROKE_RESPONSE = (
    "POSSIBLE STROKE:\n"
    "1. Call 112 in India immediately. Sudden facial drooping, arm weakness, "
    "or difficulty speaking can indicate a stroke.\n"
    "2. Note the time symptoms began or when the person was last well.\n"
    "3. Do not give food, drink, or medication unless instructed by a "
    "medical professional.\n"
    "4. Follow the emergency operator's instructions.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

ALLERGY_RESPONSE = (
    "POSSIBLE SEVERE ALLERGIC REACTION:\n"
    "1. Call 112 in India immediately if there is difficulty breathing, "
    "swelling of the tongue or throat, faintness, or rapid worsening.\n"
    "2. If the person has their own prescribed epinephrine auto-injector, "
    "help them use it according to their prescribed instructions.\n"
    "3. Follow the emergency operator's instructions. Do not let the "
    "person stand or walk if they feel faint.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

FLOOD_RESPONSE = (
    "IMMEDIATE FLOOD DANGER:\n"
    "1. Move to higher ground if you can do so safely.\n"
    "2. Never walk, swim, or drive through floodwater. Avoid electrical "
    "equipment and fallen power lines.\n"
    "3. If trapped, call 112 in India and provide your precise location "
    "and the safest way for rescuers to reach you.\n"
    "4. Follow official evacuation instructions.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

TRAPPED_RESPONSE = (
    "TRAPPED PERSON:\n"
    "1. If there is immediate danger, call 112 in India and explain "
    "where you are trapped.\n"
    "2. If there is fire or smoke, do not enter a smoke-filled escape route. "
    "Follow the fire-specific instructions and tell responders your location.\n"
    "3. If there is no immediate hazard, avoid risky climbing or forcing "
    "your way through unstable structures.\n"
    "4. Call or signal someone nearby if it is safe to do so.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

ACCIDENT_RESPONSE = (
    "POSSIBLE SERIOUS ACCIDENT:\n"
    "1. Call 112 in India if anyone is seriously injured or in immediate danger.\n"
    "2. Keep yourself away from traffic, fire, electricity, and other hazards.\n"
    "3. Do not move a seriously injured person unless remaining there "
    "poses immediate danger.\n"
    "4. Follow the emergency operator's instructions.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)

GENERAL_DANGER_RESPONSE = (
    "IMMEDIATE DANGER:\n"
    "1. Move away from the danger if you can do so safely.\n"
    "2. Call 112 in India as soon as it is safe, and describe what is "
    "happening and where you are.\n"
    "3. Avoid confronting a dangerous person or approaching hazardous objects.\n"
    "4. Follow instructions from emergency responders.\n\n"
    "CrisisLink AI has NOT contacted emergency services."
)


# -------------------------------------------------------------------
# 2. High-priority patterns
# Order matters: specific, life-threatening situations come first.
# -------------------------------------------------------------------

RULES = [
    {
        "rule": "fire_smoke",
        "category": "Fire",
        "patterns": [
            r"\bfire\s+(?:is\s+)?(?:entering|spreading|coming)\s+(?:into|in|through)\s+(?:my\s+)?room\b",
            r"\bfire\s+(?:is\s+)?(?:inside|in)\s+(?:my\s+)?room\b",
            r"\broom\s+is\s+(?:covered|filled|full)\s+with\s+smoke\b",
            r"\b(?:my\s+)?room\s+(?:is\s+)?(?:filling|flooding)\s+with\s+smoke\b",
            r"\bsmoke\s+is\s+(?:filling|entering|coming\s+into)\s+(?:my\s+)?room\b",
            r"\bsmoke\s+(?:is\s+)?(?:coming|entering)\s+(?:into\s+)?(?:my\s+)?room\b",
            r"\b(?:thick|heavy|dense)\s+smoke\b",
            r"\b(?:smoke|flames?)\s+(?:is|are)\s+(?:blocking|blocking\s+off)\s+(?:my\s+)?exit\b",
            r"\b(?:building|house|room|kitchen)\s+is\s+on\s+fire\b",
            r"\bthere\s+is\s+(?:a\s+)?fire\b",
            r"\b(?:fire|smoke)\s+(?:near|inside|in)\s+(?:the\s+)?(?:building|house|room)\b",
            r"\btrapped\s+(?:inside|in)\s+(?:a\s+)?(?:burning|smoke[- ]filled)\s+(?:room|building|house)\b",
            r"\bcan't\s+breathe\s+because\s+of\s+smoke\b",
            r"\bcannot\s+breathe\s+because\s+of\s+smoke\b",
        ],
        "response": FIRE_RESPONSE,
        "indicators": ["fire", "smoke", "possible immediate danger"],
    },
    {
        "rule": "breathing_emergency",
        "category": "Medical Emergency",
        "patterns": [
            r"\b(?:can't|cannot|can not)\s+breathe\b",
            r"\b(?:difficulty|trouble|problem|struggling)\s+(?:with\s+)?breathing\b",
            r"\b(?:difficulty|trouble)\s+breathing\b",
            r"\bnot\s+(?:able|being able)\s+to\s+breathe\b",
            r"\b(?:lips|face|skin)\s+(?:are\s+)?(?:turning\s+)?blue\b",
            r"\bchoking\s+(?:and\s+)?(?:can't|cannot)\s+breathe\b",
            r"\b(?:throat|tongue)\s+(?:is\s+)?swelling\b",
        ],
        "response": BREATHING_RESPONSE,
        "indicators": ["possible breathing emergency"],
    },
    {
        "rule": "unconsciousness",
        "category": "Medical Emergency",
        "patterns": [
            r"\b(?:is|has become|became|found)\s+unconscious\b",
            r"\b(?:person|man|woman|child|baby|father|mother|friend)\s+(?:is\s+)?unresponsive\b",
            r"\bnot\s+(?:waking up|responding)\b",
            r"\bwon't\s+wake\s+up\b",
            r"\bpassed out\s+and\s+(?:won't|cannot)\s+wake\b",
        ],
        "response": UNCONSCIOUS_RESPONSE,
        "indicators": ["unconscious or unresponsive person"],
    },
    {
        "rule": "severe_bleeding",
        "category": "Medical Emergency",
        "patterns": [
            r"\b(?:bleeding|bleeds)\s+(?:heavily|severely|a lot|badly)\b",
            r"\bsevere\s+bleeding\b",
            r"\b(?:blood|bleeding)\s+(?:is\s+)?(?:spurting|gushing)\b",
            r"\bwon't\s+stop\s+bleeding\b",
            r"\bdeep\s+(?:cut|wound)\s+(?:and\s+)?(?:heavy\s+)?bleeding\b",
        ],
        "response": BLEEDING_RESPONSE,
        "indicators": ["possible severe bleeding"],
    },
    {
        "rule": "possible_stroke",
        "category": "Medical Emergency",
        "patterns": [
            r"\b(?:face|facial)\s+(?:is\s+)?drooping\b",
            r"\bsudden\s+(?:arm|leg)\s+weakness\b",
            r"\bsuddenly\s+(?:can't|cannot)\s+speak\b",
            r"\bsudden\s+slurred\s+speech\b",
            r"\bpossible\s+stroke\b",
            r"\bsigns?\s+of\s+a\s+stroke\b",
        ],
        "response": STROKE_RESPONSE,
        "indicators": ["possible stroke symptoms"],
    },
    {
        "rule": "severe_allergic_reaction",
        "category": "Medical Emergency",
        "patterns": [
            r"\b(?:anaphylaxis|anaphylactic)\b",
            r"\b(?:allergic reaction)\b.{0,60}\b(?:can't breathe|cannot breathe|throat swelling|faint)\b",
            r"\b(?:throat|tongue)\s+(?:is\s+)?swelling\s+after\b",
            r"\b(?:allergy|allergic)\b.{0,40}\b(?:breathing difficulty|difficulty breathing)\b",
        ],
        "response": ALLERGY_RESPONSE,
        "indicators": ["possible severe allergic reaction"],
    },
    {
        "rule": "immediate_flood_danger",
        "category": "Flood",
        "patterns": [
            r"\b(?:trapped|stuck)\s+(?:by|in|inside)\s+(?:the\s+)?(?:flood|floodwater|rising water)\b",
            r"\bwater\s+(?:is\s+)?(?:rising|entering)\s+(?:my|the)\s+(?:room|house|home|building)\b",
            r"\bfloodwater\s+(?:is\s+)?(?:entering|rising inside)\b",
            r"\b(?:swept away|being swept away)\b",
            r"\b(?:stranded|trapped)\s+(?:on|inside)\s+(?:a\s+)?(?:roof|vehicle|building)\b.{0,40}\b(?:flood|water)\b",
        ],
        "response": FLOOD_RESPONSE,
        "indicators": ["possible immediate flood danger"],
    },
    {
        "rule": "trapped_person",
        "category": "Trapped Person",
        "patterns": [
            r"\b(?:i am|i'm|we are|we're|i feel)\s+(?:trapped|stuck)\s+(?:inside|in)\b",
            r"\b(?:trapped|stuck)\s+inside\s+(?:a|the|my)\s+(?:room|house|building|lift|elevator)\b",
            r"\b(?:door|exit)\s+(?:is\s+)?(?:jammed|blocked|won't open|will not open)\b",
            r"\bcan't\s+(?:get out|escape|leave)\b",
            r"\bcannot\s+(?:get out|escape|leave)\b",
            r"\bunable\s+to\s+(?:get out|escape|leave)\b",
        ],
        "response": TRAPPED_RESPONSE,
        "indicators": ["person may be trapped"],
    },
    {
        "rule": "serious_accident",
        "category": "Accident",
        "patterns": [
            r"\b(?:serious|major|bad)\s+(?:car|road|vehicle)\s+accident\b",
            r"\b(?:car|bike|motorcycle|vehicle)\s+(?:crash|collision)\b",
            r"\bperson\s+(?:was\s+)?(?:hit|struck)\s+by\s+(?:a\s+)?(?:car|vehicle|truck|bus)\b",
            r"\b(?:someone|person)\s+is\s+seriously\s+injured\b",
        ],
        "response": ACCIDENT_RESPONSE,
        "indicators": ["possible serious accident"],
    },
    {
        "rule": "immediate_danger",
        "category": "Public Safety Threat",
        "patterns": [
            r"\b(?:someone|person)\s+(?:is\s+)?(?:attacking|threatening)\s+(?:me|us|people)\b",
            r"\b(?:gun|weapon)\s+(?:threat|attack|being used)\b",
            r"\b(?:explosion|bomb threat)\b",
            r"\b(?:building|structure)\s+(?:is\s+)?collapsing\b",
            r"\bpower line\s+(?:is\s+)?down\b",
        ],
        "response": GENERAL_DANGER_RESPONSE,
        "indicators": ["possible immediate public safety danger"],
    },
]


# -------------------------------------------------------------------
# 3. Context-aware yes/no handling
# -------------------------------------------------------------------

def _normalise(value):
    """Lowercase text and normalize whitespace."""
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _is_short_affirmative(text):
    """Recognize short replies to a previous emergency question."""
    return _normalise(text) in {
        "yes",
        "yes please",
        "yeah",
        "yep",
        "y",
        "i do",
        "i am",
        "i'm",
        "correct",
        "that's right",
        "that is right",
        "true",
    }


def _is_short_negative(text):
    """Recognize short negative replies."""
    return _normalise(text) in {
        "no",
        "nope",
        "not really",
        "i don't",
        "i do not",
        "i am not",
        "no, i'm not",
        "no, i am not",
    }


def _has_negation_before(text, match_start):
    """
    Avoid treating a clearly negated symptom as a positive emergency
    signal, for example: 'I am not having trouble breathing'.

    This is a simple safeguard, not a complete language understanding
    system. When uncertain, real emergency symptoms require human help.
    """
    prefix = text[max(0, match_start - 45):match_start]

    return bool(
        re.search(
            r"\b(?:not|never|no|without|denies|don't|do not|"
            r"doesn't|does not|isn't|is not|aren't|are not|"
            r"wasn't|was not|isn't having|is not having)\b"
            r"(?:\W+\w+){0,4}\W*$",
            prefix,
        )
    )


def _find_rule(text):
    """Return the first matching high-priority rule."""
    for rule in RULES:
        for pattern in rule["patterns"]:
            match = re.search(pattern, text, flags=re.IGNORECASE)

            if not match:
                continue

            # Do not trigger a symptom rule on an obvious nearby negation.
            if _has_negation_before(text, match.start()):
                continue

            return rule

    return None


def detect_emergency(
    message,
    previous_message="",
    previous_question="",
):
    """
    Detect an emergency before normal classification or Gemini.

    Returns:
        dict: emergency result when a rule matches.
        None: no configured high-priority rule matched.

    The result fields are compatible with the Flask integration:
        category, rule, urgent, requires_human_review,
        urgency_indicators, assistant_response
    """
    text = _normalise(message)

    if not text:
        return None

    # Handle a short "yes" answer only when the preceding question
    # explicitly concerns a high-risk emergency symptom.
    if _is_short_affirmative(text):
        question = _normalise(previous_question)

        contextual_rules = [
            (
                r"\b(?:trouble|difficulty)\s+breathing\b|"
                r"\b(?:can't|cannot)\s+breathe\b",
                "breathing_emergency",
            ),
            (
                r"\bunconscious\b|\bunresponsive\b",
                "unconsciousness",
            ),
            (
                r"\bsevere\s+bleeding\b|\bbleeding\s+heavily\b",
                "severe_bleeding",
            ),
            (
                r"\bfire\b|\bsmoke\b",
                "fire_smoke",
            ),
        ]

        for question_pattern, target_rule in contextual_rules:
            if re.search(question_pattern, question):
                for rule in RULES:
                    if rule["rule"] == target_rule:
                        return _make_result(rule)

    # Do not turn an explicit "no" into an emergency just because the
    # previous question mentioned a dangerous symptom.
    if _is_short_negative(text):
        return None

    matched_rule = _find_rule(text)

    if matched_rule:
        return _make_result(matched_rule)

    return None


def _make_result(rule):
    """Return a stable response object for the Flask API."""
    return {
        "category": rule["category"],
        "rule": rule["rule"],
        "urgent": True,
        "requires_human_review": True,
        "urgency_indicators": list(rule["indicators"]),
        "assistant_response": rule["response"],
    }

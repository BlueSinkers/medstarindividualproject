This is for the naive analysis of simply finding Reddit posts that ascribe to the keywords we assigned from the JSON file structure given by Zannatul Ferdous with some minor changes by me, Abhiram Kidambi:

```
ibd_keywords = {
    'crohn': ['crohn', 'crohns', "crohn's"],
    'colitis': ['colitis', 'ulcerative colitis', 'uc'],
    'ibd_general': ['ibd', 'inflammatory bowel', 'inflammatory bowel disease']
}

anxiety_keywords = {
    'anxiety_direct': ['anxiety', 'anxious', 'panic', 'panic attack'],
    'worry': ['worry', 'worried', 'worrying', 'concern', 'concerned'],
    'fear': ['fear', 'afraid', 'scared', 'terrified', 'frightened'],
    'stress': ['stress', 'stressed', 'overwhelming', 'overwhelmed'],
    'mental_health': ['mental health', 'depression', 'depressed']
}

alzheimer_keywords = {
    'alzheimer_direct': ['alzheimer', 'alzheimers', "alzheimer's", 'alzheimer disease'],
    'dementia': ['dementia', 'cognitive decline', 'memory loss'],
    'memory': ['memory problems', 'memory issues', 'forgetful', 'forgetting'],
    'cognitive': ['cognitive', 'brain fog', 'concentration', 'confusion', 'confused'],
    'family_history': ['family history', 'hereditary', 'genetic risk', 'runs in family']
}

subreddits_ordered = [
    "mentalhealth", "Anxiety", "depression", "health", "ChronicIllness", "IBD", "CrohnsDisease",
    "AnxietySupport", "Alzheimers", "caregivers", "ChronicPain", "AskDocs", "medicine", "OCD",
    "PTSD", "IBS", "MentalHealthSupport", "Stress", "Aging", "Dementia", "brainfog", "GutHealth",
    "HealthAnxiety", "SleepDisorders", "Nootropics", "Bipolar", "Psychology", "PatientSupport",
    "UlcerativeColitis", "Neurodegeneration"
]

queries_to_search = [
    "ibd", "crohn", "ulcerative colitis", "anxiety", "panic attack",
    "stress", "depression", "alzheimer", "dementia", "memory loss"
]
```
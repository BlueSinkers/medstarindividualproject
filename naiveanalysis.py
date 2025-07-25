import praw
import csv

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
    "mentalhealth",
    "Anxiety",
    "depression",
    "health",
    "ChronicIllness",
    "IBD",
    "CrohnsDisease",
    "AnxietySupport",
    "Alzheimers",
    "caregivers",
    "ChronicPain",
    "AskDocs",
    "medicine",
    "OCD",
    "PTSD",
    "IBS",
    "MentalHealthSupport",
    "Stress",
    "Aging",
    "Dementia",
    "brainfog",
    "GutHealth",
    "HealthAnxiety",
    "SleepDisorders",
    "Nootropics",
    "Bipolar",
    "Psychology",
    "PatientSupport",
    "UlcerativeColitis",
    "Neurodegeneration"
]

queries_to_search = [
    "ibd",
    "crohn",
    "ulcerative colitis",
    "anxiety",
    "panic attack",
    "stress",
    "depression",
    "alzheimer",
    "dementia",
    "memory loss"
]

def check_cooccurrence(post_text, ibd_dict, anxiety_dict, alzheimer_dict):
    text = post_text.lower()
    has_ibd = any(keyword in text for group in ibd_dict.values() for keyword in group)
    has_anxiety = any(keyword in text for group in anxiety_dict.values() for keyword in group)
    has_alz = any(keyword in text for group in alzheimer_dict.values() for keyword in group)
    return {
        "has_ibd": int(has_ibd),
        "has_anxiety": int(has_anxiety),
        "has_alzheimer": int(has_alz),
        "ibd_and_anxiety": int(has_ibd and has_anxiety),
        "ibd_and_alzheimer": int(has_ibd and has_alz),
        "anxiety_and_alzheimer": int(has_anxiety and has_alz),
        "ibd_and_anxiety_and_alzheimer": int(has_ibd and has_anxiety and has_alz)
    }

def fetch_posts(reddit_instance, query, subreddit_name, limit=100):
    posts = []
    subreddit = reddit_instance.subreddit(subreddit_name)
    try:
        for submission in subreddit.search(query, limit=limit):
            combined_text = (submission.title or "") + " " + (submission.selftext or "")
            posts.append({
                "id": submission.id,
                "subreddit": subreddit_name,
                "title": submission.title,
                "selftext": submission.selftext,
                "url": submission.url,
                "created_utc": submission.created_utc,
                "combined_text": combined_text
            })
    except Exception:
        pass
    return posts

def main():
    reddit = praw.Reddit(
        client_id="sCeLd37WV10y24pIX06TJw",
        client_secret="Dal5UA-kutoG5GdBFhkEzctFaDMX-A",
        user_agent="ibd_anxiety_alzheimer by u/Advanced-Sector-6535",
        redirect_uri="http://localhost:8080"
    )
    
    all_posts = []
    for subreddit in subreddits_ordered:
        for query in queries_to_search:
            fetched = fetch_posts(reddit, query, subreddit, limit=50)  # limit per query per subreddit
            all_posts.extend(fetched)

    seen_ids = set()
    filtered_posts = []
    for post in all_posts:
        if post['id'] not in seen_ids:
            seen_ids.add(post['id'])
            cooccur_flags = check_cooccurrence(post['combined_text'], ibd_keywords, anxiety_keywords, alzheimer_keywords)
            post_record = {
                "id": post['id'],
                "subreddit": post['subreddit'],
                "title": post['title'],
                "selftext": post['selftext'],
                "url": post['url'],
                "created_utc": post['created_utc'],
                **cooccur_flags
            }
            filtered_posts.append(post_record)

    counts = {
        "total_posts": len(filtered_posts),
        "has_ibd": sum(p["has_ibd"] for p in filtered_posts),
        "has_anxiety": sum(p["has_anxiety"] for p in filtered_posts),
        "has_alzheimer": sum(p["has_alzheimer"] for p in filtered_posts),
        "ibd_and_anxiety": sum(p["ibd_and_anxiety"] for p in filtered_posts),
        "ibd_and_alzheimer": sum(p["ibd_and_alzheimer"] for p in filtered_posts),
        "anxiety_and_alzheimer": sum(p["anxiety_and_alzheimer"] for p in filtered_posts),
        "ibd_and_anxiety_and_alzheimer": sum(p["ibd_and_anxiety_and_alzheimer"] for p in filtered_posts)
    }

    print("Summary Statistics:")
    for k, v in counts.items():
        print(f"{k}: {v}")

    csv_columns = ["id", "subreddit", "title", "selftext", "url", "created_utc",
                   "has_ibd", "has_anxiety", "has_alzheimer",
                   "ibd_and_anxiety", "ibd_and_alzheimer", "anxiety_and_alzheimer", "ibd_and_anxiety_and_alzheimer"]

    with open("reddit_posts_cooccurrence.csv", "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in filtered_posts:
            writer.writerow(data)

if __name__ == "__main__":
    main()

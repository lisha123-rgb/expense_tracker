def auto_detect_category(description: str) -> str:
    text = description.lower()

    rules = {
        "Food": ["pizza","burger","restaurant","cafe","swiggy","zomato","kfc","dominos","biryani"],
        "Travel": ["uber","ola","petrol","bus","metro","train","flight","auto"],
        "Shopping": ["amazon","flipkart","mall","clothes","shopping","ajio","myntra"],
        "Bills": ["wifi","electricity","rent","subscription","recharge","bill","water"],
        "Entertainment": ["movie","netflix","spotify","game","concert"]
    }

    for category, keywords in rules.items():
        if any(word in text for word in keywords):
            return category

    return "Others"
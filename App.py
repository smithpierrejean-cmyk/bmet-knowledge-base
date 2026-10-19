def search_index(query, index):
    query_lower = query.lower().strip()
    words = [w for w in query_lower.split() if w not in ["error", "errors", "issue", "fault", "problem"]]
    
    if not words:
        words = query_lower.split()

    scored_results = []

    for item in index:
        text_content = (item["section"] + " " + item["text"]).lower()
        score = 0
        
        # Exact full phrase match gets the highest priority score
        if query_lower in text_content:
            score += 10
            
        # Match primary keywords (like 'spo2', 'battery', 'ecg', 'nbp')
        for word in words:
            if word in text_content:
                score += 3
                
        if score > 0:
            scored_results.append((score, item))
            
    # Sort by highest score first
    scored_results.sort(key=lambda x: x[0], reverse=True)
    
    # Return top matching items only
    return [item for score, item in scored_results]

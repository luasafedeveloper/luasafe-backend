def is_browser(request) -> bool:
    ua = request.headers.get("User-Agent", "").lower()
    accept = request.headers.get("Accept", "").lower()
    
    # 일반적인 브라우저 패턴
    browser_keywords = ["mozilla", "chrome", "safari", "firefox", "edge", "opera"]
    if any(k in ua for k in browser_keywords):
        return True
    if "text/html" in accept:
        return True
    return False

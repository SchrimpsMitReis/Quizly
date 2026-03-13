url = "https://youtu.be/-a6aqGDIAcg?si=Zl6D-nAo5M84o0bG"
def transform_yt_url(url):
    base_url = "https://www.youtube.com/watch?v="
    
    if "https://youtu.be/" in url:
        video_id = url[17:28]
        return base_url + video_id
    
    return url
print(transform_yt_url(url))
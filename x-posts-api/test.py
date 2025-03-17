from XPostsScraper import XPostsScraper
from DarkEvaluator import DarkEvaluator

scraper = XPostsScraper()
dark = DarkEvaluator()



def get_dark_posts(user_id):
    pages = 1
    posts = scraper.getPosts(user_id, pages)
    return posts

print(get_dark_posts("taiseiue"))
exit()

scraper.performLogin()

userId = input("誰の黒歴史を探しますか?")
posts = scraper.getPosts(userId, 5)

if len(posts) == 0:
    print("投稿が取得できませんでした")
    exit()

print("AIがジャッジ中...")

darks = []
for content in scraper.getPosts(userId):
    print(f"[LOG] {content}をジャッジしています...")
    if(dark.Evaluate(content)):
        darks += [content]

print(f'{len(darks)}個の黒歴史を発見しました')
for content in darks:
    print(f"黒歴史: {content}")

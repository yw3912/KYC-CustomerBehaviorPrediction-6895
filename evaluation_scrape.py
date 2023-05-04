from requests_html import HTMLSession
import json
import build_customer_profiling as b
from datetime import datetime



class Evaluation_Review:
    def __init__(self, url):
        self.session = HTMLSession()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        # careful that the sortBy and page number orders are switched compared to my real url
        self.url = url

    def access_url(self):
        r = self.session.get(self.url)
        r.html.render(sleep=1)
        if not r.html.find('div[data-hook = review]'):
            return False
        else:
            return r.html.find('div[data-hook = review]')

    def parse(self, review):
        data = {}

        title = review.find('a[data-hook = review-title]', first=True).text
        rating = review.find('i[data-hook = review-star-rating] span', first=True).text
        customer_id = review.find("div[data-hook = genome-widget] span", first=True).text
        body = review.find('span[data-hook = review-body] span', first=True)
        if body is None:
            body = None
        else:
            body = body.text.replace('\n', '').strip()
        people_count = review.find('span[data-hook = helpful-vote-statement]', first=True)
        if people_count is None:
            people_count = 0
        else:
            count_text = people_count.text
            index = count_text.index(" ")
            first_word = count_text[:index]
            if first_word == "One":
                people_count = 1
            else:
                people_count = int(first_word)

        whether_image = 0
        img_src = review.find('img[data-hook = review-image-tile]', first=True)
        if img_src is not None:
            whether_image = 1

        date = review.find('span[data-hook = review-date]', first=True).text
        index_of_On = date.index("on")
        date = date[index_of_On+3:]



        # profile_link = review.find("div[data-hook = genome-widget] a.a-profile.href", first=True).text
        # profile_link = review.find("a.a-profile", first=True).attrs['href']



        # data = {"title": title, "rating": rating, "customer_id": customer_id, "body": body,
        #         "customer_profile_link": profile_link}
        data = {"title": title, "rating": rating, "customer_id": customer_id, "body": body,
                "people_count": people_count, "image_usage": whether_image, "written_date": date}
        return data


    def save(self, results):
        with open("json/" + self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f, ensure_ascii=False)
        # with open('collective-reviews.json', 'w') as f:
        #     json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
    link = "https://www.amazon.com/gp/customer-reviews/R26FCI31NEEYFQ/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B07YGY3RMQ"
    amz = Evaluation_Review(link)
    review = amz.access_url()
    data = []
    if review is not False:
       data.append(amz.parse(review[0]))
    else:
        print("Error Occurred")

    print(data)
    b.get_body_length(data)
    b.get_keywords_number(b.get_keywords(data))
    b.get_word_diversity(data)
    b.get_word_complexity(data)
    b.get_whether_image(data)
    b.get_whether_emoji(data)
    date_1 = datetime.strptime(data[0]["written_date"], '%B %d, %Y')
    date_2 = datetime.strptime("December 1, 2019", '%B %d, %Y')
    timing = date_1 - date_2
    b.get_count_helpful(data)

    print(f"review writing length: {b.review_length_list[0]}")
    print(f"keyword count: {b.count_keyword_list[0]}")
    print(f"word diversity range(0-100): {b.word_diversity_measure_list[0]}")
    print(f"word complexity range(0-20): {b.word_complexity_measure_list[0]}")
    print(f"whether contains an image: {b.whether_image_list[0]}")
    print(f"whether contains an emoji: {b.whether_emoji_list[0]}")
    print(f"Days between review date and the first available data of this product: {timing}")
    print(f"Number of people who upvote this review: {b.count_helpful_list[0]}")

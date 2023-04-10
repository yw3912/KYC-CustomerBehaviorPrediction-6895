from requests_html import HTMLSession
import json
import time


class Reviews:
    def __init__(self, asin):
        # asin is the amazon standard identification number
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        # careful that the sortBy and page number orders are switched compared to my real url
        self.url = f'https://www.amazon.com/product-reviews/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=helpful&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        r.html.render(sleep=1)
        if not r.html.find('div[data-hook = review]'):
            return False
        else:
            return r.html.find('div[data-hook = review]')

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook = review-title]', first=True).text
            rating = review.find('i[data-hook = review-star-rating] span', first=True).text
            customer_id = review.find("div[data-hook = genome-widget] span", first=True).text
            body = review.find('span[data-hook = review-body] span', first=True)
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

            img_src = review.find('img', {'data-hook': 'review-image-tile'})['src']


            # profile_link = review.find("div[data-hook = genome-widget] a.a-profile.href", first=True).text
            # profile_link = review.find("a.a-profile", first=True).attrs['href']

            if body is None:
                continue
            body = body.text.replace('\n', '').strip()

            # data = {"title": title, "rating": rating, "customer_id": customer_id, "body": body,
            #         "customer_profile_link": profile_link}
            data = {"title": title, "rating": rating, "customer_id": customer_id, "body": body,
                    "people_count": people_count}
            total.append(data)
        return total


    def save(self, results):
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
    asin_list = ['B094PS5RZQ', "B01ASGKN8O", "B07NQJ4XM6", "B095YJW56C", "B07N2F3JXP", "B09223P6Q3", "B0859PX8H9",
                 "B00778B90S", "B007HJOQ0W", "B086Z79HXS"]
    results = []
    for asin in asin_list:
        amz = Reviews('B094PS5RZQ')
        # reviews = amz.pagination(1)
        # print(amz.parse(reviews))

        # # This 100 is caused by there is not enough space
        # reviews = amz.pagination(100)
        # print(reviews)

        for x in range(1, 10):
            print("getting page ", x)
            time.sleep(0.3)
            reviews = amz.pagination(x)
            if reviews is not False:
                results.append(amz.parse(reviews))
            else:
                print("no more pages")
                break
        if asin == "B086Z79HXS":
            amz.save(results)
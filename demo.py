from baidu_index.utils import test_cookies
from baidu_index import config
from baidu_index import BaiduIndex, ExtendedBaiduIndex

cookies = """put cookie here"""

if __name__ == "__main__":
    # Test whether the cookies are configured correctly
    # True means the configuration is successful, False means the configuration is unsuccessful
    print(test_cookies(cookies))

    keywords = [['英雄联盟'], ['冠军杯', '英雄联盟'], ['抑郁', '自杀', '明星']]

   # Get the city code, pass the code into the area to get the index of different cities, if not pass it for the whole country
   # Media index cannot be obtained by region
    print(config.PROVINCE_CODE)
    print(config.CITY_CODE)

    # Get Baidu search index (area=901 is Shandong province)
    # index: {'keyword': ['抑郁', '自杀', '明星'], 'type': 'wise', 'date': '2018-06-10', 'index': '1835'}
    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        area=901
    )
    for index in baidu_index.get_index():
        print(index)
    
    # Get Baidu Media Index
    # index: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'index': '0'}
    news_index = ExtendedBaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        kind='news'
    )
    for index in news_index.get_index():
        print(index)

    # Get Baidu consulting index
    # index: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'index': '1102911'}
    feed_index = ExtendedBaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        kind='feed'
    )
    for index in feed_index.get_index():
        print(index)

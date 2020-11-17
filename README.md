### Requirements
python3.5+
  
requests==2.19.1  

### Use
Single-account crawling: Please open the homepage of Baidu, after logging in, find the GET request of www.baidu.com, copy the cookie in the request headers of this request, and paste this cookie into the cookies object in demo.py in  
Write the following code in demo.py:

```
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

```
  
### Result
```
百度搜索指数: {'keyword': ['抑郁', '自杀', '明星'], 'type': 'wise', 'date': '2018-06-10', 'index': '1835'}
百度媒体指数: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'index': '0'}
百度咨询指数: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'index': '1102911'}
```


### Tip
-Unlimited number of incoming keywords
-The earliest data date of the search index is 2011-01-01
-The start time exceeds the earliest data date and the data will be inaccurate
-When you initialize the class, pass in area to query the Baidu index of the specified area, the default is the whole country
-Some codes are not particularly rigorous, please do your own DIY if necessary
-Media index does not support sub-regional query
-When querying keywords not included in the Baidu Index, an error will also appear, this will be fixed later

### update 
2018/02/10 Update the method format_data
2018/12/29 Update the function of querying Baidu index in designated area
2018/11/07 update
2019/05/31 update
2020/02/14 Add the function of consulting index and media index
2020/04/16 Refactor the project structure
2020/05/08 Baidu Index Modified Transfer Parameters
2020/07/13 Add compound word query



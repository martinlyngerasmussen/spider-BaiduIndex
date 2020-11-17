from urllib.parse import urlencode
import queue
import datetime
import json

import requests

from . import utils


class BaiduIndex:
    """
        Baidu Search Index
        :keywords; list
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """
    _all_kind = ['all', 'pc', 'wise']

    def __init__(
        self,
        *,
        keywords: list,
        start_date: str,
        end_date: str,
        cookies: str,
        area=0
    ):
        self.keywords = keywords
        self.area = area
        self.start_date = start_date
        self.end_date = end_date
        self.cookies = cookies
        self._params_queue = utils.get_params_queue(start_date, end_date, keywords)

    def get_index(self):
        """
        Get Baidu Index
        The format of the returned data is:
        {
            'keyword': '武林外传',
            'type': 'wise',
            'date': '2019-04-30',
            'index': '202'
        }
        """
        while 1:
            try:
                params_data = self._params_queue.get(timeout=1)
                encrypt_datas, uniqid = self._get_encrypt_datas(
                    start_date=params_data['start_date'],
                    end_date=params_data['end_date'],
                    keywords=params_data['keywords']
                )
                key = utils.get_key(uniqid, self.cookies)
                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = utils.decrypt_func(
                                key, encrypt_data[kind]['data'])
                    for formated_data in self._format_data(encrypt_data):
                        yield formated_data
            except requests.Timeout:
                self._params_queue.put(params_data)
            except queue.Empty:
                break
            utils.sleep_func()

    def _get_encrypt_datas(self, start_date, end_date, keywords):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        :keyword; list, ['1', '2', '3']
        """
        word_list = [
            [{'name': keyword, 'wordType': 1} for keyword in keyword_list]
            for keyword_list in keywords
        ]
        request_args = {
            'word': json.dumps(word_list),
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'area': self.area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = utils.http_get(url, self.cookies)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def _format_data(self, data):
        """
            Format piled data
        """
        keyword = str(data['word'])
        start_date = datetime.datetime.strptime(data['all']['startDate'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(data['all']['endDate'], '%Y-%m-%d')
        date_list = []
        while start_date <= end_date:
            date_list.append(start_date)
            start_date += datetime.timedelta(days=1)

        for kind in self._all_kind:
            index_datas = data[kind]['data']
            for i, cur_date in enumerate(date_list):
                try:
                    index_data = index_datas[i]
                except IndexError:
                    index_data = ''
                formated_data = {
                    'keyword': [keyword_info['name'] for keyword_info in json.loads(keyword.replace('\'', '"'))],
                    'type': kind,
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                yield formated_data

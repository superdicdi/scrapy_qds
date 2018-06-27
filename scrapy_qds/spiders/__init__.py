# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# import re
#
# a = 'geetest_1529490351110({"status": "success", "data": {"api_server": "api.geetest.com", "logo": true, "theme_version": "1.3.6", "image_servers": ["geenew.geetest.com"], "num": 0, "feedback": "http://www.geetest.com/contact#report", "pic": "/gee_static/0e142429b384a30790c349073d64977ec28a8c8a45d79ec1662b442bfa7ed12311b94fc692ecf5372a2ce23c88ceca00", "sign": "", "static_servers": ["static.geetest.com/", "dn-staticdown.qbox.me/"], "c": [12, 58, 98, 36, 43, 95, 62, 15, 12], "spec": "1*1", "theme": "silver", "s": "74736564", "pic_type": "word"}})'
# b = re.search(".*\"pic\": \"(.*?)\".*", a)
# if b:
#     print(b.group(1))
# else:
#     print("wu")
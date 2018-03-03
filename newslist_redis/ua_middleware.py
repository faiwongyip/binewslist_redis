import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.conf import settings

class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        # self.user_agent = user_agent
        self.user_agent = settings['USER_AGENT']
        
    # @classmethod
    # def from_crawer(cls, crawler):
        # return cls(user_agent=crawler.settings.get('USER_AGENT'))
        
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        request.headers.setdefault('User-Agent', ua)
        # print('\n','----------' + ua + '----------','\n')
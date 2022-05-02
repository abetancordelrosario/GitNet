from datetime import datetime, timedelta
from enum import Enum
from typing import Tuple
import aiohttp
import asyncio
import json
import re


class api_data(Enum):
    STARRED = "starred"
    FOLLOWERS = "followers" 
    STARGAZERS = "stargazers"

class dataExtraction:
    '''
    Fetch information from the GitHub API and save it into lists concurrently 
    using asynchronous programming.

    The construtor requires two strings, first is the full repository name
    (author/repository) and the second one is the user's GitHub token.
    '''

    __MAX_REPOS_STARGAZER: int = 20
    __MAX_NUMBER_ITEMS: int = 100
    __NO_PAGES: int = 0
    __API_URL: str = "https://api.github.com/"
    __UNLOCK: bool = True

    
    __RATE_LIMIT_STATUS_CODE: int = 403
    __NOT_FOUND_STATUS_CODE: int = 404
    __OK_STATUS_CODE: int = 200

    __stargazers: list = []
    __main_repository: json

    def __init__(self, full_name_repository: str, token: str) -> None:
        self.full_name_repository = full_name_repository
        self.headers = {"Authorization": 'token %s' % token,
                        "Retry-After": '5'}

    def fetch_data(self) -> Tuple[list,list]:
        stargazers_followers_list, stargazer_starred_repos_list = asyncio.run(self.fetch_repo_and_stargazers())
        return stargazers_followers_list, stargazer_starred_repos_list


    async def fetch_repo_and_stargazers(self) -> Tuple[list, list]:
        session_timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(headers=self.headers, timeout=session_timeout) as session:
            await self.fetch_main_repo(session)
            self.__stargazers = await self.request_api(None, self.__MAX_NUMBER_ITEMS, api_data.STARGAZERS.value, True, session)
            
            starred_tasks = []
            follower_tasks = []
            for stargazer in self.__stargazers:
                follow_task =  asyncio.ensure_future(self.request_api(stargazer, 
                                                                      self.__MAX_NUMBER_ITEMS, 
                                                                      api_data.FOLLOWERS.value, 
                                                                      False, 
                                                                      session))
                follower_tasks.append(follow_task)
                starred_task = asyncio.ensure_future(self.request_api(stargazer, 
                                                                      self.__MAX_REPOS_STARGAZER, 
                                                                      api_data.STARRED.value, 
                                                                      False, 
                                                                      session))
                starred_tasks.append(starred_task)
            starred_results = await asyncio.gather(*starred_tasks)
            follower_results = await asyncio.gather(*follower_tasks)

            return starred_results, follower_results


    async def request_api(self, stargazer: json, num_items: int, info: str, is_repo_url: bool, session) -> list:
        if is_repo_url:
            url: str = self.__API_URL+"repos/%s/%s?per_page=%d" % (self.full_name_repository, info, num_items)
        else:
            url: str = self.__API_URL+"users/%s/%s?per_page=%d" % (stargazer['login'], info, num_items)

        if self.__UNLOCK:
            async with session.get(url , headers=session.headers) as api_response:
                response_json: list = await api_response.json()
                if api_response.status == self.__OK_STATUS_CODE:
                    response_json = await self.check_pagination(session, info, api_response, response_json, url)
                elif api_response.status == self.__RATE_LIMIT_STATUS_CODE and self.__UNLOCK:
                    self.__UNLOCK = False
                    await self.sleep_execution(api_response)
                    response_json = await self.request_api(stargazer, num_items, info, is_repo_url, session)
                else:
                    await asyncio.sleep(60)
                    response_json = await self.request_api(stargazer, num_items, info, is_repo_url, session)
                return response_json
        else:
            await asyncio.sleep(60)
            response_json = await self.request_api(stargazer, num_items, info, is_repo_url, session)
            return response_json
            

    async def check_pagination(self, session, info, api_response, response_json, url):
        if info != api_data.STARRED.value:
            num_pages: int = await self.get_number_pages(api_response)
            pages_tasks = []
            for page in range(2, num_pages+1):
                page_task = asyncio.ensure_future(self.consume_pages(session, api_response, url, page))
                pages_tasks.append(page_task)
            pages_list = await asyncio.gather(*pages_tasks)
            consumed_pages = [item for page in pages_list for item in page]
            response_json.extend(consumed_pages)

        return response_json

    async def consume_pages(self, session, api_response, url, page) -> list:
        url: str = url+"&page=%d" % page

        if self.__UNLOCK:
            async with session.get(url, headers= session.headers) as api_response:
                response_json = await api_response.json()
                if api_response.status == self.__RATE_LIMIT_STATUS_CODE and self.__UNLOCK:
                    self.__UNLOCK = False
                    await self.sleep_execution(api_response)
                    response_json = await self.consume_pages(session, api_response, url, page)
                else:
                    await asyncio.sleep(60)
                    response_json = await self.consume_pages(session, api_response, url, page)
                return response_json
        else:
            await asyncio.sleep(60)
            response_json = await self.consume_pages(session, response_json, api_response, url, page)
            return response_json
            
                        
    async def fetch_main_repo(self, session) -> None:
        main_repo_url: str = self.__API_URL+"repos/%s" % self.full_name_repository
        async with session.get(main_repo_url, headers= session.headers) as main_repo_response:
            if main_repo_response.status == self.__OK_STATUS_CODE:
                self.__main_repository = await main_repo_response.json()
            elif main_repo_response.status == self.__RATE_LIMIT_STATUS_CODE:
                await self.sleep_execution(main_repo_response) 
                self.fetch_main_repo(self, session)               


    async def get_number_pages(self, api_response: aiohttp.ClientResponse) -> int:
        response = api_response.headers.get('Link')
        if response:
            links: list = str(response).split(",")
            num_pages = re.findall('\d+', links[1])
            return int(num_pages[2])
        else:
            return self.__NO_PAGES

    async def sleep_execution(self, api_response: aiohttp.ClientResponse) -> None:
        try: 
            utc_reset_time = datetime.fromtimestamp(int(api_response.headers['X-RateLimit-Reset']))
            sleep_time: float = (utc_reset_time - datetime.utcnow() + timedelta(0, 5)).total_seconds()
            print(sleep_time)
            print("Rate limit exceeded")
            await asyncio.sleep(sleep_time) 
        except:
            print("Secondary rate limit exceeded")
            retry_after = api_response.headers['Retry-After']
            s_t = int(retry_after)
            if retry_after == '60':
                await asyncio.sleep(60)

        self.__UNLOCK = True

    def get_stargazers(self) -> list:
        return self.__stargazers

    def get_main_repo(self) -> list:
        return self.__main_repository

import aiohttp
import asyncio             
import json

class extractData:

    __MAX_REPOS_STARGAZER: int = 20
    __MAX_NUMBER_ITEMS: int = 100
    __API_URL = "https://api.github.com/"

    def __init__(self, full_name_repository: str, token: str) -> None:
        self.full_name_repository = full_name_repository
        self.token = token

        

    def foo(self):
        asyncio.run(self.foo2())
        


    async def foo2(self):
        headers = {"Authorization": 'token %s' % self.token}
        async with aiohttp.ClientSession(headers=headers) as session:
            main_repo_url: str = self.__API_URL+"repos/%s" % self.full_name_repository
            main_repository = await session.get(main_repo_url, headers= session.headers)
            stargazers: list = await self.foo3(None, self.__MAX_NUMBER_ITEMS, "stargazers", True, session)
            starred_tasks = []
            follower_tasks = []
            
            for stargazer in stargazers:
                follow_relationship_task =  asyncio.ensure_future(self.foo3(stargazer, self.__MAX_NUMBER_ITEMS, "followers", False, session))
                follower_tasks.append(follow_relationship_task)
                starred_repos_task = asyncio.ensure_future(self.foo3(stargazer, self.__MAX_REPOS_STARGAZER, "starred", False, session))
                starred_tasks.append(starred_repos_task)
            listt = await asyncio.gather(*starred_tasks)
            listt1 = await asyncio.gather(*follower_tasks)


    async def foo3(self, stargazer: json, num_items: int, info: str, is_repo_url: bool, session) -> list:
        if is_repo_url:
            url: str = self.__API_URL+"repos/%s/%s?per_page=%d" % (self.full_name_repository, info, num_items)
        else:
            url: str = self.__API_URL+"users/%s/%s?per_page=%d" % (stargazer['login'], info, num_items)

        async with session.get(url , headers=session.headers) as api_response:
            response_json: list = await api_response.json()
            if info != "starred":
                while 'next' in api_response.links.keys():
                    async with session.get(api_response.links['next']['url'], headers= session.headers) as api_response:
                        response_json.extend(await api_response.json())
                        
            return response_json


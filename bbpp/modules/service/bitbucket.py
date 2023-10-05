import asyncio
import platform

import bbpp
import httpx
from notifypy import Notify
from .config import Config
from typing import List


class BitBucket:
    def __init__(self, config: Config):
        self.config = config
        self.ENDPOINT = 'https://api.bitbucket.org/2.0'
        self.repositories = list[str]
        self.state = list[tuple[str, str]]
        self.notifier_service = Notify()

    def get_repos(self):
        print('Getting repos')
        output = asyncio.run(self._get_first_repo())
        self.repositories = list(self.parse_repos(output))
        pages = int(output.get('size') / output.get('pagelen'))
        output = asyncio.run(self._get_all_pages(pages))
        for page in output:
            self.repositories += list(self.parse_repos(page))

    async def _get(self, client, url):
        r = await client.get(url, auth=self.config.auth)
        return r.json()

    async def _get_first_repo(self):
        url = f'{self.ENDPOINT}/repositories/{self.config.workspace}'
        async with httpx.AsyncClient() as client:
            r = await self._get(client, url)
            return r

    async def _get_all_pages(self, pages: int):
        async with httpx.AsyncClient() as client:
            tasks = []
            for page in range(1, pages + 1):
                url = f'{self.ENDPOINT}/repositories/{self.config.workspace}?page={page + 1}'
                tasks.append(asyncio.ensure_future(self._get(client, url)))

            repos = await asyncio.gather(*tasks)
            return repos

    def _get_pipelines(self, repo: str):
        r = httpx.get(f"{self.ENDPOINT}/repositories/{self.config.workspace}/{repo}/pipelines?sort=-created_on",
                      auth=self.config.auth)
        return r.json()

    def check(self, repo: str):
        pipelines = self._get_pipelines(repo)
        self.print_pipeline(pipelines)
        path = f'{bbpp.__path__[0]}/assets/audio/{self.config.sound}'
        if self.update_state(pipelines):
            self.notifier_service.title = f"BitBucket {repo} pipeline"
            self.notifier_service.message = "Pipeline state changed"
            self.notifier_service.application_name = "BBPP"
            if platform.system() == 'Darwin':
                self.notifier_service.audio = path
            self.notifier_service.send()

    from typing import Dict
    def update_state(self, pipelines: dict[str, list]) -> bool:
        state = []
        pipelines = pipelines.get('values')
        for pipeline in pipelines:
            state.append(self.parse_state(pipeline))

        if self.state != state and self.state != []:
            return True

        self.state = state
        return False

    @staticmethod
    def parse_repos(output: dict[str, list]):
        for repo in output.get('values'):
            yield repo.get('name')

    @staticmethod
    def print_pipeline(pipelines: dict):
        for pipeline in pipelines.get('values'):
            print(
                f"Pipeline: {pipeline.get('state').get('name')} {pipeline.get('created_on')} {pipeline.get('duration_in_seconds')}s")

    @staticmethod
    def parse_state(pipeline: dict):
        return pipeline.get('uuid'), pipeline.get('state').get('name')
        pass

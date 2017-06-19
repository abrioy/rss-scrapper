# -*- coding: utf-8 -*-
import logging

from rss_scrapper.tasks.read import ReadTask

logger = logging.getLogger(__name__)


class WriteTask(ReadTask):
    name = "write"

    def do_execute(self, data):
        with open(self.file_name, 'w', encoding=self.encoding) as file:
            file.write(data)

        yield data

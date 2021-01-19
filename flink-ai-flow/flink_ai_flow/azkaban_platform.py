#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import threading
import logging
import traceback
from typing import Text, List

from ai_flow.plugins.platform import AbstractPlatform, AbstractJobStatusListener, AbstractJobHandler


class AzkabanPlatform(AbstractPlatform):
    @staticmethod
    def job_status_listener() -> type(AbstractJobStatusListener):
        return AzkabanJobStatusListener

    @staticmethod
    def platform() -> Text:
        return 'azkaban'


class AzkabanJobStatusListener(AbstractJobStatusListener):
    def __init__(self):
        super().__init__(platform='azkaban')
        self.job_handles: List[AbstractJobHandler] = []
        self.status_map = {}
        self.running = True
        self.lock = threading.Lock()

    # TODO
    # implement it!!
    def listen(self):
        raise NotImplementedError("please implement listen")

    def run(self) -> None:
        try:
            self.listen()
        except Exception as e:
            logging.info(e)
            traceback.print_exc()

    # TODO
    # implement it!!
    def start_listen(self):
        raise NotImplementedError("please implement start_listen")

    # TODO
    # implement it!!
    def stop_listen(self):
        raise NotImplementedError("please implement stop_listen")

    def register_job_listening(self, job_handler: AbstractJobHandler):
        # since the api server will push the pod status changing event to watcher, there is no need to register
        # kubernetes job listening explicitly.
        pass

    def stop_job_listening(self, job_id: Text):
        pass

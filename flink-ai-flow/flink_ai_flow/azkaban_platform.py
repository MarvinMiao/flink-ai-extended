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
from typing import Text, Dict

from ai_flow.plugins.platform import AbstractPlatform, AbstractJobStatusListener
from flink_ai_flow.vvp.vvp_restful_api import VVPRestful
from flink_ai_flow.vvp_platform import VVPJobHandler, VVPJobStatusListener


AzkabanJobHandler = VVPJobHandler
AzkabanJobStatusListener = VVPJobStatusListener


class AzkabanPlatform(AbstractPlatform):
    @staticmethod
    def job_status_listener() -> type(AbstractJobStatusListener):
        return AzkabanJobStatusListener

    @staticmethod
    def platform() -> Text:
        return 'azkaban'

    @staticmethod
    def generate_job_handler(json_conf: Dict):
        base_url = json_conf.pop("base_url")
        namespace = json_conf.pop("namespace")
        token = json_conf.pop("token", None)

        return VVPRestful(base_url=base_url, namespace=namespace, token=token)

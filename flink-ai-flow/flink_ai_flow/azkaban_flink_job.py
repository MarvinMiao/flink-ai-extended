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
import uuid
import time
import json
from abc import ABC
from typing import Dict, Text, List, Optional

from ai_flow.plugins.job_plugin import AISubGraph, AbstractJobPlugin, ProjectDesc, JobContext, \
    AbstractJobConfig, AbstractJob, AbstractEngine
from ai_flow.common.json_utils import Jsonable
from ai_flow.workflow.job_config import PeriodicConfig
from ai_flow.plugins.platform import AbstractPlatform
from flink_ai_flow.flink_engine import FlinkEngine
from notification_service.base_notification import BaseEvent, EventWatcher
from flink_ai_flow.azkaban_platform import AzkabanPlatform, AzkabanJobHandler

from ai_flow.meta.job_meta import ExecutionMode
from ai_flow.common.yaml_utils import dump_yaml_str
from ai_flow.api.notification import send_event, start_listen_event, stop_listen_event


"""
VVP flink job plugin for azkaban engine
"""


class AzkabanJobConfig(AbstractJobConfig):
    class AzkabanJobNode(object):
        def __init__(self, name: Text, type: Text = "vvp_flink", config: Dict = {}, depends_on: List[Text] = []) -> None:
            """
            Azkaban config translator. Parsing input vvp config and azkaban pipeline depends_on to azkaban's yaml config format.

            :param name: Job name.
            :param type: Job type, default value is vvp_flink.
            :param config: Job config. It's value is the dict parsed from VVPJobConfig.
            :param depends_on: Azkaban job dependents, default value is empty list.
            """
            super().__init__()
            self.name = name
            self.type = type
            self.config = config
            self.depends_on = depends_on

        def to_dict(self) -> Dict:
            return {
                "name": self.name,
                "type": self.type,
                "config": self.config,
                "dependsOn": self.depends_on
            }

    def __init__(self, nodes: List[Dict] = [], job_name: Text = None,
                 periodic_config: PeriodicConfig = None, exec_mode: Optional[ExecutionMode] = ExecutionMode.STREAM,
                 properties: Dict[Text, Jsonable] = None):
        super().__init__(platform="azkaban", engine="flink", job_name=job_name, periodic_config=periodic_config, exec_mode=exec_mode, properties=properties)
        self.nodes = {
            "nodes": list(map(lambda node: AzkabanJobConfig.AzkabanJobNode(**node).to_dict(), nodes))
        }

    def to_yaml_str(self):
        return dump_yaml_str(self.nodes)


class AzkabanFlinkJob(AbstractJob):
    def __init__(self,
                 job_context: JobContext = JobContext(),
                 job_config: AbstractJobConfig = AzkabanJobConfig(),
                 project_desc: ProjectDesc = ProjectDesc()):
        super().__init__(job_context, job_config)
        self.project_desc = project_desc
        self.vvp_deployment_id: Text = None
        self.vvp_job_id: Text = None
        self.config_file = None
        self.exec_cmd = None


class AzkabanFlinkJobPlugin(AbstractJobPlugin, ABC):

    NS_JOB_KEY = "azkaban_jobs"
    NS_WAITING_PERIOD = 0.01  # period for checking event
    NS_EXPIRED_TIME = 300  # expiration time for notification response

    class AzkabanJobWatcher(EventWatcher):
        def __init__(self, event_list) -> None:
            super().__init__()
            self.event_list = event_list

        def process(self, events: List[BaseEvent]):
            self.event_list.extend(events)

    def __init__(self) -> None:
        super().__init__()

    def generate(self, sub_graph: AISubGraph, project_desc: ProjectDesc) -> AbstractJob:
        assert 1 == len(sub_graph.nodes)
        if sub_graph.config.exec_mode == ExecutionMode.BATCH:
            context = JobContext(ExecutionMode.BATCH)
        else:
            context = JobContext(ExecutionMode.STREAM)
        assert isinstance(sub_graph.config, AzkabanJobConfig)
        return AzkabanFlinkJob(job_context=context, job_config=sub_graph.config, project_desc=project_desc)

    # compact AzkabanFlinkJob with user defined resources
    def generate_job_resource(self, job: AbstractJob) -> None:
        pass

    @staticmethod
    def job_type() -> type(AbstractJob):
        return AzkabanFlinkJob

    @staticmethod
    def job_config_type() -> type(AbstractJobConfig):
        return AzkabanJobConfig

    @staticmethod
    def platform() -> type(AbstractPlatform):
        return AzkabanPlatform

    @staticmethod
    def engine() -> type(AbstractEngine):
        return FlinkEngine

    def submit_job(self, job: AzkabanFlinkJob) -> AzkabanJobHandler:
        job_yaml_conf = job.job_config.to_yaml_str()
        job_id = job.uuid if job.uuid is not None else str(uuid.uuid4())
        ns_resp_key = "{}-{}".format(job.project_desc.project_name, job_id)
        event_list = []
        try:
            # setup current job's envet listener
            start_listen_event(key=ns_resp_key, watcher=AzkabanFlinkJobPlugin.AzkabanJobWatcher(event_list))

            # send job event to notification service
            send_event(key=self.NS_JOB_KEY, value=job_yaml_conf)

            # waiting for response
            start_time = time.time()
            while len(event_list) == 0 and (time.time() - start_time) < self.NS_EXPIRED_TIME:
                time.sleep(self.NS_WAITING_PERIOD)

            if len(event_list) != 1:
                raise Exception("invalid number of notification responses: {}, should be exactly one".format(len(event_list)))

            event_resp = json.loads(event_list[0].value)
            vvp_restful = AzkabanPlatform.generate_job_handler(event_resp)
            return AzkabanJobHandler(vvp_restful=vvp_restful, **event_resp)
        finally:
            stop_listen_event(ns_resp_key)

    def stop_job(self, job: AzkabanFlinkJob):
        self.cleanup_job(job)

    # code used in airflow pipeline
    # should not be implemented for azkaban generator
    def generate_code(self, op_index, job):
        return super().generate_code(op_index, job)

    # TODO
    # implement cleanup_job
    def cleanup_job(self, job: AzkabanFlinkJob):
        return super().cleanup_job(job)

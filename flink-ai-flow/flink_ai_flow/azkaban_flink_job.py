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
from abc import ABC
from typing import Dict

from ai_flow.plugins.job_plugin import AISubGraph, AbstractJobPlugin, ProjectDesc, JobContext, \
    AbstractJobConfig, AbstractJob, AbstractEngine
from flink_ai_flow.azkaban_platform import AzkabanPlatform, AzkabanJobHandler
from flink_ai_flow.flink_job_common import FlinkJobConfig
from ai_flow.meta.job_meta import ExecutionMode
from ai_flow.plugins.engine import NSEngine


class AzkabanFlinkJobConfig(FlinkJobConfig):
    @staticmethod
    def from_dict(data: Dict, config) -> object:
        return FlinkJobConfig.from_dict(data, config)

    def __init__(self):
        super().__init__(platform=AzkabanPlatform.platform())


class AzkabanFlinkJob(AbstractJob):
    def __init__(self,
                 job_context: JobContext = JobContext(),
                 job_config: AbstractJobConfig = AzkabanFlinkJobConfig()):
        super().__init__(job_context, job_config)


class AzkabanJobPlugin(AbstractJobPlugin, ABC):
    def __init__(self) -> None:
        super().__init__()

    def generate(self, sub_graph: AISubGraph, project_desc: ProjectDesc) -> AbstractJob:
        assert 1 == len(sub_graph.nodes)
        if sub_graph.config.exec_mode == ExecutionMode.BATCH:
            context = JobContext(ExecutionMode.BATCH)
        else:
            context = JobContext(ExecutionMode.STREAM)
        return AzkabanFlinkJob(job_context=context, job_config=sub_graph.config)

    def generate_job_resource(self, job: AbstractJob) -> None:
        pass

    def job_type(self) -> type(AbstractJob):
        return AzkabanFlinkJob

    def job_config_type(self) -> type(AbstractJobConfig):
        return AzkabanFlinkJobConfig

    def platform(self) -> type(AbstractPlatform):
        return AzkabanPlatform

    def engine(self) -> type(AbstractEngine):
        return NSEngine

    def generate_job_name(self, job):
        return job.job_name.lower().replace('.', '-').replace('_', '-')

    # TODO
    # return AzkabanJobHandler
    def submit_job(self, job: AzkabanFlinkJob) -> AzkabanJobHandler:
        return super().submit_job(job)

    def stop_job(self, job: AzkabanFlinkJob):
        self.cleanup_job(job)

    # TODO
    # implement cleanup_job
    def cleanup_job(self, job: AzkabanFlinkJob):
        return super().cleanup_job(job)

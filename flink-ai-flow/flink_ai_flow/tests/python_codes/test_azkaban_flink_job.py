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
import unittest
import uuid
import json
from typing import List, Dict, Text
from ai_flow.common.json_utils import Jsonable

import ai_flow
import flink_ai_flow
from ai_flow.api.notification import send_event
from ai_flow.test import test_util
from ai_flow.common.yaml_utils import dump_yaml_str
from ai_flow.meta.job_meta import ExecutionMode
from flink_ai_flow.azkaban_platform import AzkabanPlatform
from flink_ai_flow.azkaban_flink_job import AzkabanFlinkJob, AzkabanJobConfig, AzkabanFlinkJobPlugin
from ai_flow.plugins.job_plugin import ProjectDesc, JobContext
from ai_flow.application_master.master import AIFlowMaster


class TestAzkabanFlinkJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # config = MasterConfig()
        # config.set_db_uri(db_type=DBType.SQLITE, uri="sqlite:///sql.db")
        cls.master = AIFlowMaster(config_file=test_util.get_master_config_file())
        cls.master.start(is_block=False)
        cls.project_desc = ProjectDesc()
        cls.project_desc.project_config.set_master_ip("localhost")
        cls.project_desc.project_config.set_master_port("50051")
        cls.project_desc.project_config.set_project_name("test_project")

    @classmethod
    def tearDownClass(cls):
        cls.master.stop()

    def get_exec_args(self) -> Dict[Text, Jsonable]:
        return {
            "platform": AzkabanPlatform.platform(),
            "engine": AzkabanFlinkJobPlugin.engine().engine(),
            "base_url": "http://test.vvp.platfom.com",
            "namespace": "ververica",
            "token": "test_user_token",
            "deployment_name": "test_azkaban_job",
            "jar_file": "flink-python.jar",
            "entrypoint": "org.apache.flink.client.python.PythonDriver",
            "entrypoint_args": "-args1=1\n-args2=2",
            "additional_dependenceis": ["dep1", "dep2"],
            "parallelisim": 1,
            "flink_image": "test_flinkjob_image"
        }

    def generate_test_nodes(self) -> List[Dict]:
        node_a = {
            "name": "node_a",
            "type": "vvp_flink",
            "config": {
                "jar_file": "flink-python.jar",
                "entrypoint": "org.apache.flink.client.python.PythonDriver",
                "entrypoint_args": "-args1=1\n-args2=2",
                "additional_dependenceis": ["dep1", "dep2"],
                "parallelisim": 1,
                "flink_image": "test_flinkjob_image"
            }
        }

        return [node_a]

    def test_azkaban_job_config(self):
        test_nodes = self.generate_test_nodes()
        azkaban_job_conf = AzkabanJobConfig(test_nodes).to_yaml_str()
        test_nodes[0]["dependsOn"] = []
        test_job_yaml_str = dump_yaml_str({"nodes": test_nodes})
        self.assertEqual(azkaban_job_conf, test_job_yaml_str)

    def test_submit_job(self):
        test_job_plugin = AzkabanFlinkJobPlugin()
        job_context = JobContext(ExecutionMode.STREAM)
        test_nodes = self.generate_test_nodes()
        azkaban_job_conf = AzkabanJobConfig(test_nodes)
        test_azkaban_job = AzkabanFlinkJob(job_context, azkaban_job_conf, self.project_desc)
        test_azkaban_job.uuid = str(uuid.uuid4())
        ns_resp_key = "{}-{}".format(test_azkaban_job.project_desc.project_name, test_azkaban_job.uuid)
        event_resp = json.dumps({
            "base_url": "http://localhost/test_vvp_restful",
            "namespace": "ververica",
            "token": "12345",
            "vvp_job_id": "12345",
            "vvp_deployment_id": "12345",
            "job_instance_id": "12345",
            "job_uuid": 1,
            "workflow_id": 1
        })
        send_event(ns_resp_key, event_resp)  # mock response from ns server
        test_job_plugin.submit_job(test_azkaban_job)

    def test_build_graph(self):
        azkaban_job_node = [{
            "name": "test_azkaban_job",
            "type": "vvp_flink",
            "config": self.get_exec_args(),
            "depends_on": []
        }]
        azkaban_config = AzkabanJobConfig(nodes=azkaban_job_node, job_name="test_azkaban_job", exec_mode="vvp_flink")
        with ai_flow.config(azkaban_config):
            flink_ai_flow.azkaban_job(exec_args=self.get_exec_args(
            ), name="test_azkaban_train", job_type=ExecutionMode.STREAM)
            workflow_id = ai_flow.run(dag_id="test_azkaban_train", scheduler_type=ai_flow.SchedulerType.AIFLOW)
            res = ai_flow.wait_workflow_execution_finished(workflow_id)
            print(f"test_build_graph result: {res}")


if __name__ == '__main__':
    unittest.main()

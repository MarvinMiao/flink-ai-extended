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
from typing import Text, List
from ai_flow.common.registry import BaseRegistry
from ai_flow.common import json_utils
from ai_flow.graph.edge import MetConfig, MetCondition, EventLife, MetValueCondition, TaskAction
from ai_flow.workflow.workflow import Workflow


def match_stop_before_config(met_config: MetConfig) -> bool:
    if met_config.event_value == "FINISHED" \
            and met_config.action == TaskAction.START \
            and met_config.condition == MetCondition.NECESSARY \
            and met_config.life == EventLife.ONCE \
            and met_config.value_condition == MetValueCondition.EQUAL:
        return True
    else:
        return False


def job_name_to_task_id(job_name):
    first_index = job_name.find('_')
    last_index = job_name.rfind('_')
    return job_name[first_index+1: last_index]


class AirflowCodeGenerator(ABC):

    def generate_operator_code(self) -> Text:
        """
        run once.
        :return:
        """
        return ""

    def generate_code(self, op_index, job):
        raise Exception("do not have AirflowCodeGenerator generate_code implement!")


class AirflowCodeManager(BaseRegistry):

    def register_generator(self, platform, engine, generator: AirflowCodeGenerator):
        self.register((platform, engine), generator)

    def get_generator(self, platform, engine) -> AirflowCodeGenerator:
        return self.get_object((platform, engine))


_default_airflow_code_generator_manager = AirflowCodeManager()


def register_airflow_code_generator(platform, engine, generator: AirflowCodeGenerator):
    _default_airflow_code_generator_manager.register_generator(platform, engine, generator)


def get_airflow_code_manager() -> AirflowCodeManager:
    return _default_airflow_code_generator_manager


class DAGTemplate(object):
    AIRFLOW_IMPORT = """from airflow.models.dag import DAG
from airflow.utils import timezone
from airflow.ti_deps.met_handlers.aiflow_met_handler import AIFlowMetHandler
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from ai_flow.deployer.utils.kubernetes_util import load_kubernetes_config
import ai_flow as af
load_kubernetes_config()\n"""

    SET_CONFIG = """af.set_project_config_file('{0}')\naf.set_master_config()\n"""

    DAG_DEFINE = """dag = DAG(dag_id='{0}', start_date=timezone.utcnow(), schedule_interval='{1}')\n"""

    UPSTREAM_OP = """{0}.set_upstream({1})\n"""

    EVENT_DEPS = """{0}.add_event_dependency('{1}', '{2}')\n"""

    MET_HANDLER = """configs_{0}='{1}'\n
{0}.set_event_met_handler(AIFlowMetHandler(configs_{0}))\n"""


class DAGGenerator(object):
    def __init__(self):
        self.op_count = -1

    def generate_op_code(self, job):
        self.op_count += 1
        generator: AirflowCodeGenerator = get_airflow_code_manager().get_generator(job.platform, job.exec_engine)
        code_text = generator.generate_code(op_index=self.op_count, job=job)
        return job.instance_id, "op_{0}".format(self.op_count), code_text

    def generate_upstream(self, op_1, op_2):
        return DAGTemplate.UPSTREAM_OP.format(op_1, op_2)

    def generate_event_deps(self, op, met_config):
        return DAGTemplate.EVENT_DEPS.format(op, met_config.event_key, met_config.event_type)

    def generate_handler(self, op, configs: List[MetConfig]):
        return DAGTemplate.MET_HANDLER.format(op, json_utils.dumps(configs))

    def generator(self, workflow: Workflow, dag_id=None) -> Text:
        self.op_count = -1
        if dag_id is None:
            dag_id = workflow.project_desc.project_name
        code_text = DAGTemplate.AIRFLOW_IMPORT

        op_set = set()
        for name, job in workflow.jobs.items():
            generator: AirflowCodeGenerator = get_airflow_code_manager().get_generator(job.platform, job.exec_engine)
            if generator not in op_set:
                code_text += generator.generate_operator_code()
                op_set.add(generator)

        code_text += DAGTemplate.SET_CONFIG.format(workflow.project_desc.project_path + '/project.yaml')
        code_text += DAGTemplate.DAG_DEFINE.format(dag_id, workflow.project_desc.project_config.get_schedule_interval())

        task_map = {}
        for name, job in workflow.jobs.items():
            task_id, op_name, code = self.generate_op_code(job)
            task_map[task_id] = op_name
            code_text += code

        for instance_id, edges in workflow.edges.items():
            op_name = task_map[instance_id]
            configs = []
            for edge in edges:
                met_config: MetConfig = edge.met_config
                if match_stop_before_config(met_config):
                    dep_task_id = edge.target_node_id
                    code = self.generate_upstream(op_name, task_map[dep_task_id])
                    code_text += code
                else:
                    code = self.generate_event_deps(op_name, met_config)
                    code_text += code
                    configs.append(met_config)
            if len(configs) > 0:
                code = self.generate_handler(op_name, configs)
                code_text += code

        return code_text

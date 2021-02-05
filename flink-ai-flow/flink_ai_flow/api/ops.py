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
from typing import Text, List
from ai_flow.common.properties import Properties

from ai_flow.executor.executor import BaseExecutor

from ai_flow.api.ops import user_define_operation
from ai_flow.common.args import ExecuteArgs
from ai_flow.graph.channel import NoneChannel
from ai_flow.meta.job_meta import ExecutionMode
from flink_ai_flow.vvp_flink_job import VVPJobConfig


def vvp_job(exec_args: ExecuteArgs = None, name: Text = None) -> NoneChannel:
    return user_define_operation(executor=BaseExecutor('vvp'),
                                 output_num=0,
                                 input_data_list=None,
                                 exec_args=exec_args,
                                 name=name)


def azkaban_job(exec_args: Properties = None,
                name: Text = None, job_type: ExecutionMode = ExecutionMode.STREAM, az_job_type: Text = "vvp_flink", az_depends_on: List[Text] = []) -> NoneChannel:
    parsed_vvp_config = VVPJobConfig.from_dict(exec_args, VVPJobConfig())
    if job_type == ExecutionMode.STREAM:
        exec_args = ExecuteArgs(stream_properties=parsed_vvp_config)
    elif job_type == ExecutionMode.BATCH:
        exec_args = ExecuteArgs(batch_properties=parsed_vvp_config)
    else:
        raise Exception(f"Invalid job type: {job_type.value}, only support {ExecutionMode.get_all_values}")
    return user_define_operation(executor=BaseExecutor('azkaban'),
                                 output_num=0,
                                 input_data_list=None,
                                 exec_args=exec_args,
                                 name=name)

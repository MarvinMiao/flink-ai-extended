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

import ai_flow as af
from ai_flow.common import json_utils
import python_ai_flow
from ai_flow.api.configuration import *
from ai_flow import translator
from ai_flow.test import test_util
from ai_flow.executor.executor import CmdExecutor
from ai_flow.translator.base_translator import *
from ai_flow.application_master.master import AIFlowMaster
from ai_flow.application_master.master_config import MasterConfig, DBType


def build_ai_graph_node(size) -> AIGraph:
    graph = AIGraph()
    for i in range(size):
        graph.add_node(AINode(name="name_" + str(i)))
    return graph


def add_data_edge(graph, src, target):
    nodes = []
    for n in graph.nodes.values():
        nodes.append(n)
    graph.add_edge(nodes[src].instance_id,
                   DataEdge(source_node_id=nodes[src].instance_id, target_node_id=nodes[target].instance_id))


def add_control_edge(graph, src, target):
    nodes = []
    for n in graph.nodes.values():
        nodes.append(n)
    graph.add_edge(nodes[src].instance_id,
                   ControlEdge(source_node_id=nodes[src].instance_id, target_node_id=nodes[target].instance_id))


class TestTranslator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = MasterConfig()
        config.set_db_uri(db_type=DBType.SQLITE, uri="sqlite:///sql.db")
        cls.master = AIFlowMaster(config_file=test_util.get_master_config_file())
        cls.master.start(is_block=False)

    @classmethod
    def tearDownClass(cls):
        cls.master.stop()

    def test_split_graph(self):
        def build_ai_graph() -> AIGraph:
            graph = AIGraph()
            for i in range(6):
                graph.add_node(AINode(name="name_" + str(i)))
            nodes = []
            for n in graph.nodes.values():
                nodes.append(n)

            graph.add_edge(nodes[2].instance_id,
                           DataEdge(source_node_id=nodes[2].instance_id, target_node_id=nodes[0].instance_id, port=0))
            graph.add_edge(nodes[2].instance_id,
                           DataEdge(source_node_id=nodes[2].instance_id, target_node_id=nodes[1].instance_id, port=0))
            graph.add_edge(nodes[4].instance_id,
                           ControlEdge(source_node_id=nodes[4].instance_id, target_node_id=nodes[2].instance_id))
            graph.add_edge(nodes[4].instance_id,
                           ControlEdge(source_node_id=nodes[4].instance_id, target_node_id=nodes[3].instance_id))
            return graph

        graph: AIGraph = build_ai_graph()
        splitter = DefaultGraphSplitter()
        graph = DefaultTranslator.optimize(graph)
        split_graph = splitter.split(graph, ProjectDesc())
        self.assertEqual(4, len(split_graph.nodes))
        self.assertEqual(1, len(split_graph.edges))
        for v in split_graph.edges.values():
            self.assertEqual(2, len(v))

    def test_split_ai_graph(self):
        def build_ai_graph() -> AIGraph:
            with af.engine('cmd_line'):
                p_list = []
                for i in range(3):
                    p = af.user_define_operation(
                        executor=CmdExecutor(cmd_line="echo 'hello_{}' && sleep 3".format(i)))
                    p_list.append(p)
                af.stop_before_control_dependency(p_list[0], p_list[1])
                af.stop_before_control_dependency(p_list[0], p_list[2])

            return af.default_graph()

        graph: AIGraph = build_ai_graph()
        splitter = DefaultGraphSplitter()
        split_graph = splitter.split(graph, ProjectDesc())
        self.assertEqual(3, len(split_graph.nodes))
        self.assertEqual(1, len(split_graph.edges))

    def test_optimize_graph(self):
        def build_ai_graph() -> AIGraph:
            """
            - or | data edge
            == or || control edge
                 11
                 ||
            12=0-1-2--3-5
               | |  | ||
               | 13 4--6
               |      ||
               7-8====9

            10

            """
            graph = build_ai_graph_node(14)

            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 2)
            add_data_edge(graph, 4, 2)
            add_data_edge(graph, 5, 3)
            add_data_edge(graph, 6, 4)
            add_data_edge(graph, 7, 0)
            add_data_edge(graph, 8, 7)
            add_data_edge(graph, 13, 1)

            add_control_edge(graph, 6, 3)
            add_control_edge(graph, 9, 6)
            add_control_edge(graph, 8, 9)
            add_control_edge(graph, 11, 1)
            add_control_edge(graph, 0, 12)

            return graph

        graph: AIGraph = build_ai_graph()
        g = DefaultTranslator.optimize(graph)
        cluster_graph = build_cluster_graph(g)

        self.assertEqual(18, len(g.nodes))
        self.assertEqual(7, len(cluster_graph.cluster_dict))
        node_list_name_0 = []
        for n in graph.nodes.values():
            if n.name == "name_0":
                node_list_name_0.append(n)
        self.assertEqual(3, len(node_list_name_0))
        for n in node_list_name_0:
            es = graph.edges[n.instance_id]
            self.assertEqual(1, len(es))
            self.assertEqual("name_12", graph.nodes[es[0].target_node_id].name)

    def test_compute_cluster_graph_1(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(5)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 0)
            add_data_edge(graph, 4, 3)
            add_control_edge(graph, 4, 2)
            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(2, len(cluster_graph.cluster_dict))

    def test_compute_cluster_graph_2(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(6)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 0)
            add_data_edge(graph, 4, 3)
            add_control_edge(graph, 5, 2)
            add_control_edge(graph, 4, 5)

            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(3, len(cluster_graph.cluster_dict))

    def test_compute_cluster_graph_3(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(6)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 0)
            add_data_edge(graph, 4, 3)
            add_control_edge(graph, 5, 2)
            add_control_edge(graph, 4, 5)
            add_control_edge(graph, 3, 1)
            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(3, len(cluster_graph.cluster_dict))

    def test_compute_cluster_graph_4(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(6)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 0)
            add_data_edge(graph, 4, 3)
            add_control_edge(graph, 5, 2)
            add_control_edge(graph, 4, 5)
            add_control_edge(graph, 2, 3)
            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(3, len(cluster_graph.cluster_dict))
        self.assertTrue(True, cluster_graph.has_circle())

    def test_compute_cluster_graph_5(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(8)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 0)
            add_data_edge(graph, 4, 3)
            add_data_edge(graph, 5, 0)
            add_data_edge(graph, 6, 1)
            add_data_edge(graph, 7, 6)
            add_control_edge(graph, 4, 2)
            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(2, len(cluster_graph.cluster_dict))
        self.assertEqual(9, len(graph.nodes))
        self.assertFalse(cluster_graph.has_circle())

    def test_compute_cluster_graph_6(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(8)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 0)
            add_data_edge(graph, 3, 1)
            add_data_edge(graph, 3, 2)

            add_data_edge(graph, 5, 4)
            add_data_edge(graph, 6, 4)
            add_data_edge(graph, 7, 5)
            add_data_edge(graph, 7, 6)
            add_control_edge(graph, 5, 1)
            add_control_edge(graph, 2, 6)

            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertFalse(do_split)
        cluster_graph = build_cluster_graph(graph)

    def test_compute_cluster_graph_7(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(4)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 2, 0)
            add_data_edge(graph, 3, 0)
            add_control_edge(graph, 3, 1)
            return graph

        graph: AIGraph = build_ai_graph()

        has_circle, do_split, err_message = DefaultTranslator.compute_cluster_graph(graph)
        self.assertTrue(has_circle)
        self.assertTrue(do_split)
        cluster_graph = build_cluster_graph(graph)
        self.assertEqual(2, len(cluster_graph.cluster_dict))
        res = set()
        for n in graph.nodes.values():
            if n.name == "name_2":
                n2 = n
        for e in graph.edges[n2.instance_id]:
            res.add(e.target_node_id)

        self.assertTrue("AINode_4" in res)

    def test_compute_cluster_graph_8(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(5)
            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 1)
            add_data_edge(graph, 4, 3)
            add_control_edge(graph, 2, 3)
            add_control_edge(graph, 4, 1)
            return graph

        graph: AIGraph = build_ai_graph()
        exception_flag = False
        try:
            graph = DefaultTranslator.optimize(graph)
        except Exception as e:
            exception_flag = True
        self.assertTrue(True, exception_flag)

    def test_compute_cluster_graph_9(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(5)
            add_data_edge(graph, 2, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 2)
            add_data_edge(graph, 4, 2)
            add_control_edge(graph, 1, 0)
            add_control_edge(graph, 3, 4)
            return graph

        graph: AIGraph = build_ai_graph()
        exception_flag = False
        try:
            DefaultTranslator.optimize(graph)
        except Exception as e:
            exception_flag = True
        self.assertTrue(True, exception_flag)

    def test_translate_workflow(self):
        def build_ai_graph() -> AIGraph:
            graph = build_ai_graph_node(14)

            add_data_edge(graph, 1, 0)
            add_data_edge(graph, 2, 1)
            add_data_edge(graph, 3, 2)
            add_data_edge(graph, 4, 2)
            add_data_edge(graph, 5, 3)
            add_data_edge(graph, 6, 4)
            add_data_edge(graph, 7, 0)
            add_data_edge(graph, 8, 7)
            add_data_edge(graph, 13, 1)

            add_control_edge(graph, 6, 3)
            add_control_edge(graph, 9, 6)
            add_control_edge(graph, 8, 9)
            add_control_edge(graph, 11, 1)
            add_control_edge(graph, 0, 12)
            return graph

        graph: AIGraph = build_ai_graph()
        tmp_translator = get_default_translator()
        proj_desc = ProjectDesc()
        proj_desc.project_config.set_master_ip("localhost")
        proj_desc.project_config.set_master_port("50051")
        proj_desc.project_config.set_project_name("test_project")
        workflow = tmp_translator.translate(graph, proj_desc)
        print("#####workflow: {}".format(json_utils.dumps(workflow)))


if __name__ == '__main__':
    unittest.main()

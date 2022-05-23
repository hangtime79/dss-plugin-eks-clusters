def get_node_pool_args(node_pool):
    args = []
    if 'machineType' in node_pool:
        args = args + ['--node-type', ', '.join(str(x) for x in node_pool['machineType'])]
    if 'diskType' in node_pool:
        args = args + ['--node-volume-type', node_pool['diskType']]
    if 'diskSizeGb' in node_pool and node_pool['diskSizeGb'] > 0:
        args = args + ['--node-volume-size', str(node_pool['diskSizeGb'])]

    args = args + ['--nodes', str(node_pool.get('numNodes', 3))]
    if node_pool.get('numNodesAutoscaling', False):
        args = args + ['--asg-access']
        args = args + ['--nodes-min', str(node_pool.get('minNumNodes', 2))]
        args = args + ['--nodes-max', str(node_pool.get('maxNumNodes', 5))]

    tags = node_pool.get('tags', {})
    if len(tags) > 0:
        tag_list = [key + '=' + value for key, value in tags.items()]
        args = args + ['--tags', ','.join(tag_list)]
        
    nodeLabels = node_pool.get('nodeLabels', {})
    if len(nodeLabels) > 0:
        nodeLabels_list = [key + '=' + value for key, value in nodeLabels.items()]
        args = args + ['--node-labels', ','.join(nodeLabels_list)]

    if node_pool.get('useSpotInstances', False):
        args = args + ['--managed', '--spot']

    return args
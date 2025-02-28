def do(payload, config, plugin_config, inputs):
    from dku_aws.boto3_command import get_instances_and_spot, split_fsg 
    
    instanceFamily = plugin_config.get("instanceFamily")
    instanceVCPUsMin = plugin_config.get("instanceVCPUsMin")
    instanceVCPUsMax = plugin_config.get("instanceVCPUsMax")
    memoryMin = plugin_config.get("memoryMin")
    memoryMax = plugin_config.get("memoryMax")


    instances_df = get_instances_and_spot()
    instances_df = instances_df[['Instance_Type','vCPUs','Memory','GPU_Ind','Processor_Speed','Current_Spot_Price','Instance_Recommended', 'Instance_Family']]
    instances_df = instances_df.sort_values(by=['Instance_Recommended', 'GPU_Ind', 'vCPUs', 'Memory', 'Processor_Speed', 'Current_Spot_Price'], ascending=[False, True, True, False, False, True])

    instances_df = instances_df[(instances_df.vCPUs >= instanceVCPUsMin) & 
                                (instances_df.vCPUs <= instanceVCPUsMax) &
                                (instances_df.Memory >= memoryMin) &
                                (instances_df.Memory <= memoryMax) & 
                                (instances_df.Instance_Family.isin(instanceFamily))
                               ]

    instances_df['Inst_Description'] = (
        instances_df['Instance_Type'] + '/' + 
        'vCPUs:' + instances_df['vCPUs'].astype(str) + '/' + 
        'Mem:' + instances_df['Memory'].astype(str) + '/' + 
        'Ghz:' + instances_df['Processor_Speed'].astype(str) + '/' + 
        'Spot: $' + instances_df['Current_Spot_Price'].astype(str) + '/' + 
        'GPU:' + instances_df['GPU_Ind'].astype(str) )

    df = instances_df[['Instance_Type','Inst_Description']]

    df.columns.values[0] = "value"
    df.columns.values[1] = "label"
    
    choices = list()
    
    choices.append(( { "value" : "t4g.nano", "label" : "t4g.nano - For Keeping a Cluster Alive Only"}))

    for i, row in df.iterrows():
        val = f"{row['value']}"
        label = f"{row['label']}"
        choices.append(( { "value" : val, "label" : label}))

    return {"choices": choices}
def do(payload, config, plugin_config, inputs):
    from dku_aws.boto3_command import get_instances_and_spot, build_choices_list_from_pandas

    instances_df = get_instances_and_spot()
    instances_df = instances_df[['Instance_Type','vCPUs','Memory','GPU_Ind','Processor_Speed','Current_Spot_Price','Instance_Recommended']]
    instances_df = instances_df.sort_values(by=['Instance_Recommended', 'GPU_Ind', 'vCPUs', 'Memory', 'Processor_Speed', 'Current_Spot_Price'], ascending=[False, True, True, False, False, True])

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
    
    for i, row in df.iterrows():
        val = f"{row['value']}"
        label = f"{row['label']}"
        choices.append(( { "value" : val, "label" : desc}))

    return {"choices": choices}
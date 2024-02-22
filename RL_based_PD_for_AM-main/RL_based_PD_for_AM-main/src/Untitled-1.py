dicts={1:1,2:2}
parts=[1,2]
obs={}
for part in parts:
    temp={}
    for key in dicts.keys():
        temp[key]=dicts[key]
    obs[part]=temp
print(obs)
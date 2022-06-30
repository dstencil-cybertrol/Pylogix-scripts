#!/usr/bin/env python3

import datetime
import json
rom pylogix import PLC

IP = input('Enter AB PLC IP Address xxx.xxx.xxx.xxx \n')
microstatus = input('is PLC a Micro800 series? (y or n) def(n) \n')
if microstatus == 'y':
    microstatus = True
else:
    microstatus = False
dateformat = datetime.datetime.now()
date_formatted = dateformat.strftime('%m%d%y')
files = f"{IP}_{date_formatted}".json
with PLC() as comm:
        comm.IPAddress = IP
        tags = comm.GetTagList()
        output_tags = {IP: []}

        comm.Micro800 = microstatus
        comm.GetTagList()

        for t in tags.Value:
            t_read = comm.Read(t.TagName)
            t_value = t_read.Value
            #if type(t_value) == bytes:
                #tag_value = f'{tag_value}'

            tag_dict = {
                "Value":     t_value, 
                "Data Type": t.DataType,
                "Status":    t.Status
            }
            output_tags[IP].append({t_read.TagName: tag_dict})
            
            print(f'Writing: {t_read.TagName}: {tag_dict}')

json.dump(output_tags, open(files, "w"), indent=4)
print(f'Tag Data written to {files}')
#Git test
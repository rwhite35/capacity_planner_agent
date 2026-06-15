### Capacity Planning Report

Computer 1 (planner.txt — first file)

|   Filesystem   |  Size  |  Used  | Available | Capacity |
| :------------: | :----: | :----: | :-------: | :------: |
| /dev/disk1s5s1 | 500 GB | 12 GB  |   55 GB   |   19%    |
|     devfs      | 228 KB | 228 KB |    0 B    |   100%   |

<br>

Computer 2 (planner.txt — second file)

|   Filesystem   |  Size  |  Used  | Available | Capacity |
| :------------: | :----: | :----: | :-------: | :------: |
| /dev/disk1s6s1 | 500 GB |  8 GB  |   59 GB   |   16%    |
|     devfs      | 228 KB | 228 KB |    0 B    |   100%   |

<br>

## Agents Key Takeaways Report

<br>
Both machines have 500 GB primary disks. Computer 1 is using slightly more space (12 GB / 19%) compared to Computer 2 (8 GB / 16%), leaving Computer 2 with a bit more available space (59 GB vs. 55 GB). Both are well within healthy usage ranges on their primary volumes.
Note: It looks like both files were uploaded with the same name (planner.txt). You may have intended to upload two different files — if so, feel free to re-upload and I can redo the summary.
<br>
<br>

## Setup Solution

The following are steps to setup a similar agent for local development.

# Add a Cronjob

Once the project is setup, generate reports using crontab to create a job that runs the `disk free` command on each of the VirtualMachines with the report saved to the projects `capacity/planner.txt` file location.

> crontab -e
> VMS=["path/to/vmproj1","path/to/vmproj2"]
> PATH=/bin:/path/to/CapacityPlanner
> 0 8 \* \* _ summarize_planner.py $VMS && claude "Read /var/reports/vmdisk_.txt and summarize capacity" >> ~/disk_summary.log

This cronjob will run at 8am EST everyday until removed. The report disk*summary.log is the output from the claude agent reading in all the `vndisk*[0-9].txt` files which then summarizes the capacity details and suggestions.

# About Tokens

Depending on the account type and level of token use, this call is .01 cent per request.

[Token]

```
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: sk-ant-api03-0r4X5...-OoMb5gAA" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{"model": "claude-sonnet-4-6", "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, world"}]}'
```

## Building the Agent

Build a full agent with [Claude Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference). This solution is using the `file-reading` tool and lets it decide how to report.

[python]

```
tools = [{
    "name": "read_file",
    "description": "Read a text file from disk",
    "input_schema": {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"]
    }
}]
```

import re
from datetime import datetime

# 从给定路径读取log文件内容
log_file_path = "/home/scy24/asc-rna/.snakemake/log/"  # 请替换成你的日志文件路径
log_file_path += "2025-01-18T144705.247394.snakemake.log"
# 打开文件并读取内容
with open(log_file_path, "r") as file:
    log_data = file.readlines()

timestamp_pattern = re.compile( r'\[(.*?)\]')
job_name_pattern = re.compile( r'localrule\s+(\S+):')
jobid_pattern = re.compile (r'\s+jobid:\s*(\d+)')
finished_job_pattern = re.compile (r'Finished\s+job\s+(\d+)')

job_start_times = {}
jobs = []


for i in range(len(log_data)):
    line = log_data[i]
    time_match = timestamp_pattern.match(line)
    if time_match:
        start_time_str = time_match.group(1)
        start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Y")

        job_name_match = job_name_pattern.match(log_data[i+1])
        if job_name_match is None:
            continue;
        job_name = job_name_match.group(1)

        jobid_match = jobid_pattern.match(log_data[i+4])
        if jobid_match is None:
            continue;
        job_id = jobid_match.group(1)

        job_start_times[job_id] = {"start_time": start_time, "job_name": job_name}
        # print("start_time: ", start_time, "job_name: ", job_name, "job_id: ", job_id)

for i in range(len(log_data)):
    line = log_data[i]
    time_match = timestamp_pattern.match(line)

    if time_match:
        end_time_str = time_match.group(1)
        end_time = datetime.strptime(end_time_str, "%a %b %d %H:%M:%S %Y")

        finished_job_match = finished_job_pattern.match(log_data[i+1])

        if finished_job_match is None:
            continue;

        job_id = finished_job_match.group(1)

        if job_id in job_start_times:
            start_time = job_start_times[job_id]["start_time"]
            job_name = job_start_times[job_id]["job_name"]
            
            # 计算耗时
            duration = end_time - start_time
            jobs.append({
                "Job Name": job_name,
                "Job ID": job_id,
                "Duration": duration
            })

# for job in jobs:
#     print(f"Job Name: {job['Job Name']},\t Job ID: {job['Job ID']},\t Duration: {job['Duration']}")

# 动态计算最大长度
max_job_name_length = max(len(job['Job Name']) for job in jobs)
max_job_id_length = max(len(str(job['Job ID'])) for job in jobs)
max_duration_length = max(len(str(job['Duration'])) for job in jobs)

# 输出时长格式化为小时:分钟:秒
for job in jobs:
    duration = job['Duration']
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    print(f"Job Name: {job['Job Name']:<{max_job_name_length}},\t Job ID: {job['Job ID']:<{max_job_id_length}},\t Duration: {formatted_duration:<{max_duration_length}}")

# # 存储每个job的开始时间


# # 存储结果
# jobs = []

# # 提取开始时间
# for match in re.finditer(job_start_pattern, log_data):
#     print(match)
#     start_time_str = match.group(1)
#     job_name = match.group(2)
#     job_id = match.group(3)
    
#     # 转换时间字符串为datetime对象
#     start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Y")
    
#     # 记录每个job的开始时间
#     job_start_times[job_id] = {"start_time": start_time, "job_name": job_name}

# # 提取结束时间并计算耗时
# for match in re.finditer(job_end_pattern, log_data):
#     end_time_str = match.group(1)
#     job_id = match.group(2)
    
#     # 转换时间字符串为datetime对象
#     end_time = datetime.strptime(end_time_str, "%a %b %d %H:%M:%S %Y")
    
    # 如果找到了对应job的开始时间
    # if job_id in job_start_times:
    #     start_time = job_start_times[job_id]["start_time"]
    #     job_name = job_start_times[job_id]["job_name"]
        
    #     # 计算耗时
    #     duration = end_time - start_time
    #     jobs.append({
    #         "Job Name": job_name,
    #         "Job ID": job_id,
    #         "Duration": duration
    #     })

# # 输出结果
# for job in jobs:
#     print(f"Job Name: {job['Job Name']}, Job ID: {job['Job ID']}, Duration: {job['Duration']}")
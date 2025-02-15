import re
from datetime import datetime

def cal_stage_1_time(dic):
    filter_time = dic["filter_bam"]
    multi_time = max (dic["unfiltered_multi"] , dic["unfiltered_uniq"], filter_time + dic["filtered_multi"], filter_time + dic["filtered_uniq"])
    other_time = dic["cut_fastq"] + dic["align_to_ncrna"] + dic["bam_to_fastq"] + \
    dic["align_to_genome"] + dic["sort_bam"] + dic["umi_dedup"] +\
    dic["join_pileup"]

    return multi_time + other_time


def parse_log_for_job_duration(log_file_path):
    # 打开文件并读取内容
    with open(log_file_path, "r") as file:
        log_data = file.readlines()

    timestamp_pattern = re.compile(r'\[(.*?)\]')
    job_name_pattern = re.compile(r'localrule\s+(\S+):')
    jobid_pattern = re.compile(r'\s+jobid:\s*(\d+)')
    finished_job_pattern = re.compile(r'Finished\s+job\s+(\d+)')

    job_start_times = {}
    jobs = {}

    # 提取作业开始时间和相关信息
    for i in range(len(log_data)):
        line = log_data[i]
        time_match = timestamp_pattern.match(line)
        if time_match:
            start_time_str = time_match.group(1)
            start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Y")

            job_name_match = job_name_pattern.match(log_data[i+1])
            if job_name_match is None:
                continue
            job_name = job_name_match.group(1)

            jobid_match = jobid_pattern.match(log_data[i+4])
            if jobid_match is None:
                continue
            job_id = jobid_match.group(1)

            job_start_times[job_id] = {"start_time": start_time, "job_name": job_name}

    # 提取作业结束时间并计算耗时
    for i in range(len(log_data)):
        line = log_data[i]
        time_match = timestamp_pattern.match(line)

        if time_match:
            end_time_str = time_match.group(1)
            end_time = datetime.strptime(end_time_str, "%a %b %d %H:%M:%S %Y")

            finished_job_match = finished_job_pattern.match(log_data[i+1])

            if finished_job_match is None:
                continue

            job_id = finished_job_match.group(1)

            if job_id in job_start_times:
                start_time = job_start_times[job_id]["start_time"]
                job_name = job_start_times[job_id]["job_name"]

                # 计算耗时
                duration = end_time - start_time
                jobs[job_name] = int(duration.total_seconds())

    return jobs

# 示例使用
log_file_path = "/home/scy24/asc-rna/.snakemake/log/2025-01-19T061536.814192.snakemake.log"

# "2025-01-19T061536.814192.snakemake.log" # original stage-2
log_name_list = ["case1-origin.log","case2-origin.log","case3-origin.log","case1-opt.log","case2-opt.log","case3-opt.log"]

job_name_list = ["cut_fastq", "align_to_ncrna", "bam_to_fastq", "align_to_genome", \
                 "sort_bam", "umi_dedup", "join_pileup","unfiltered_uniq", "unfiltered_multi", \
                    "filter_bam",  "filtered_uniq", "filtered_multi", "join_pileup","stage_1_time"]

all_time_dic = {}


for log_name in log_name_list:

    log_file_path = "/home/scy24/asc-rna/log-doc/" + log_name
    job_durations = parse_log_for_job_duration(log_file_path)

    stage_1_time = cal_stage_1_time(job_durations)

    job_durations["stage_1_time"] = stage_1_time

    all_time_dic[log_name] = job_durations



for job_name in job_name_list:
    print(job_name, end = " & ")
    for i in range(len(log_name_list)):
        log_name = log_name_list[i]
        if i == len(log_name_list) - 1:
            print(all_time_dic[log_name][job_name], end = " \\\\")
        else:
            print(all_time_dic[log_name][job_name], end = " & ")

    print()
# job_durations = parse_log_for_job_duration(log_file_path)

# # 输出结果
# for job_name, duration in job_durations.items():
#     print(f"Job Name: {job_name}, Duration: {duration} seconds")
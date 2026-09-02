import csv
import re
import os
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from test_new_fd_parser import parse_fd_csv_new

res = parse_fd_csv_new('ops_fd.csv')
print("Parsed result keys:", res.keys())
print("Summary:", json.dumps(res["summary"], ensure_ascii=False, indent=2))
print("Channels:", json.dumps(res["channels"], ensure_ascii=False, indent=2))
print(f"Top 10 count: {len(res['top10'])}")
print("Sample top 10:", json.dumps(res["top10"][:3], ensure_ascii=False, indent=2))
print(f"AM rankings count: {len(res['am_rankings'])}")
print("Sample AM ranking:", json.dumps(res["am_rankings"][:3], ensure_ascii=False, indent=2))
print(f"All POs count: {len(res['all_pos'])}")
print("Sample All POs:", json.dumps(res["all_pos"][:3], ensure_ascii=False, indent=2))
print("Unique AMs:", res["unique_ams"])

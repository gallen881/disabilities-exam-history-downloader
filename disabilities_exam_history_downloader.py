# v1.0

import requests
import json
import os

class UrlFinder:
    def __init__(self, schoolSysName: list, classGroupName: list, subjects: list, year: list) -> None:
        self.schoolSysName = schoolSysName
        self.classGroupName = classGroupName
        self.subjects = subjects
        self.start_year = year[0]
        self.end_year = year[1]
        self.download_list = []

    def run(self):
        for year in range(self.start_year, self.end_year + 1):
            r = requests.get(f'https://cis.ncu.edu.tw/EnableSys/home/changeTabNo?year={year}')
            data = json.loads(r.text)
            for row in data['questionList']:
                if row['schoolSysName'] in self.schoolSysName and row['classGroupName'] in self.classGroupName and row['fileName'] in self.subjects:
                    self.download_list.append({
                        'id': row['id'],
                        'name': row['attachments'],
                        'year': year
                        })
        return self.download_list

class Downloader:
    def __init__(self, download_list: list, qa_download: tuple, download_path: str) -> None:
        self.download_list = download_list
        self.q_download = qa_download[0]
        self.a_download = qa_download[1]
        self.download_path = download_path
        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)

    def run(self):
        for row in self.download_list:
            if self.q_download:
                file_name = f'{self.download_path}({row["year"]}){row["name"][0]}'
                with open(file_name, 'wb') as f:
                    f.write(requests.get(f'https://cis.ncu.edu.tw/EnableSys/home/readExamInfoFile?examInfoId={row["id"]}&row=0').content)
                print(f'Downloaded {file_name.replace(self.download_path, "")}')
            if self.a_download:
                file_name = f'{self.download_path}({row["year"]}){row["name"][1]}'
                with open(file_name, 'wb') as f:
                    f.write(requests.get(f'https://cis.ncu.edu.tw/EnableSys/home/readExamInfoFile?examInfoId={row["id"]}&row=1').content)
                print(f'Downloaded {file_name.replace(self.download_path, "")}')
            
subjects = ['國文', '英文', '數學A', '數學B', '數學甲', '數學乙', '歷史', '地理']
finder = UrlFinder(['大學組'], ['共同'], subjects, [102, 112])
download_list = finder.run()
downloader = Downloader(download_list, (True, True), 'D:/disabilities_exam_history/')
downloader.run()
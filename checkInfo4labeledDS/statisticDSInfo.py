import ply
import os
from glob import glob

class StatisticDataSetInfo:
    
    file_paths = list()
    class_names = {0: 'ground',
                   1: 'road',
                   2: 'slope',
                   3: 'wall',
                   4: 'building',
                   5: 'vehicle',
                   6: 'mapelement',
                   7: 'vegetation',
                   8: 'noise'}
    
    def __init__(self, file_path, class_name = None) -> None:
        if class_name is not None:
            self.rewrite_class_names(class_name=class_name)
        else:
            print('Use default class_names dict:', self.class_names)
            
        if file_path is None:
            print('file_paths is none, check anr retry.')
            raise(ValueError)
        else: self.file_paths = file_path
    
    def rewrite_class_names(self, class_name):
        self.class_names = dict()
        for id, name in enumerate(class_name):
            self.class_names[id] = name
        print('class_names dict is rewrited to:', self.class_names)
            
    def statisticLabeledDSNumberPerClass(self, format='.ply'):
        # 生成字典存储统计点数量，初始都为零
        statisticInfo = dict()
        for key in self.class_names:
            statisticInfo[self.class_names[key]] = 0
        # 目前仅支持.ply格式的
        if format != '.ply':
            print('目前不支持[', format, ']格式。')
            return statisticInfo
        for path in self.file_paths:
            all_files = ''
            if os.path.exists(path=path) and os.path.isdir(path):
                all_files = glob(os.path.join(path, '*'+format))
            else:
                print(path, '当前路径不存在或该路径不是目录。')
                raise(ValueError)

            
            for file_name in all_files:
                _file = os.path.split(file_name)[1].split('.')[0]
                try:
                    _file = _file.split('_')[0]
                except:
                    print(file_name, ', skipped')
                    continue
                if statisticInfo.__contains__(_file):
                    file = ply.read_ply(filename=file_name)
                    statisticInfo[_file] += file.shape[0]
                else:
                    print(file_name, ', skipped')
                    continue
            
        return statisticInfo
                
            
if __name__ == '__main__':
    paths = [r'D:/data\decode/NanLuTianDrone_label/NanLuTian_8_10',
             r'D:/data\decode/NanLuTianDrone_label/NanLuTian_4_7',
             r'D:/data\decode/NanLuTianDrone_label/NanLuTian_0-3',
             r'D:/data/decode/NanLuTianDrone_label/NanLuTian_11_16']
    
    operator_statistic = StatisticDataSetInfo(file_path=paths)
    statistic = operator_statistic.statisticLabeledDSNumberPerClass(format='.txt')
    print(statistic)
    
    
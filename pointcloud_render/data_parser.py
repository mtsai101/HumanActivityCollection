import json
import csv
import os

def visiualize_json(name):
    f = open('./dataset/0514/fork_eat_1620974183398.json')
    data = json.load(f)
    if os.path.isfile(f'visual_csv/{name}_accelerator.csv'):
        os.remove(f'visual_csv/{name}_accelerator.csv'); 
        os.remove(f'visual_csv/{name}_gryoscope.csv'); 
        os.remove(f'visual_csv/{name}_orientation.csv'); 
    for d in data['result']:
        with open(f'visual_csv/{name}_accelerator.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([float(d['accelerator'][0]), float(d['accelerator'][1]), float(d['accelerator'][2])])

        with open(f'visual_csv/{name}_gryoscope.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([float(d['gryoscope'][0]), float(d['gryoscope'][1]), float(d['gryoscope'][2])])

        with open(f'visual_csv/{name}_orientation.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([float(d['orientation'][0]), float(d['orientation'][1]), float(d['orientation'][2]), float(d['orientation'][3])])

if __name__== "__main__":
    visiualize_json("fork")

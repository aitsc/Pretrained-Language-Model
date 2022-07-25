import sys, os
sys.path.append(os.getcwd())

import torch
from torchviz import make_dot
from transformer.modeling import TinyBertForSequenceClassification


def main():

    # 构建模型结构
    model = TinyBertForSequenceClassification.from_pretrained('data/TinyBERT_General_6L_768D', num_labels=2)
    model.to(torch.cuda.current_device())
    # 构建模型需要的模拟参数
    minputs = [
        {'name': 'input_ids', 'size': [32, 128]},
        {'name': 'segment_ids', 'size': [32, 128]},
        {'name': 'input_mask', 'size': [32, 128]},
    ]
    for i in minputs:
        i['v'] = torch.full(i['size'], 1, dtype=torch.int64).to(torch.cuda.current_device())
    data = tuple(i['v'] for i in minputs)
    # 输出模型图, TD_inter
    result = model(*data)
    result_d = {}
    for i, name in enumerate(['student_logits', 'student_atts', 'student_reps']):
        result_d[name] = result[i]
    for k, v in result_d.items():
        model_img_path = f'tsc/TD_inter_{k}'
        g = make_dot(tuple(v) if type(v)==list else v, params=dict(model.named_parameters()), show_attrs=True, show_saved=True)
        g.render(filename=model_img_path, cleanup=True, format='pdf')


if __name__ == '__main__':
    main()
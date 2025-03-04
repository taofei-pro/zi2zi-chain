#!/bin/bash
# 长时间训练后的推理脚本

# 激活conda环境
conda activate zi2zi_chain

# 对不同检查点进行推理
for checkpoint in 1000 2000 5000 10000 15000 20000
do
  echo "使用检查点 $checkpoint 进行推理..."
  python infer.py \
    --experiment_dir=/home/zihun/workspace/zi2zi-chain/experiment_long \
    --gpu_ids=cuda:0 \
    --batch_size=32 \
    --resume=$checkpoint \
    --from_txt \
    --src_font=/home/zihun/workspace/zi2zi-chain/fonts/T1.ttf \
    --src_txt="你好世界中国人工智能" \
    --infer_dir=infer_long_$checkpoint \
    --type_file=/home/zihun/workspace/zi2zi-chain/type/宋黑类字符集.txt
done

echo "推理完成！"

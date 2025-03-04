#!/bin/bash
# 长时间训练脚本 - 预计10小时

# 激活conda环境
conda activate zi2zi_chain

# 开始训练
python train.py \
  --experiment_dir=/home/zihun/workspace/zi2zi-chain/experiment_long \
  --gpu_ids=cuda:0 \
  --batch_size=16 \
  --epoch=100 \
  --L1_penalty=180 \
  --Lconst_penalty=20 \
  --Lcategory_penalty=1.5 \
  --sample_steps=200 \
  --checkpoint_steps=200 \
  --schedule=15 \
  --lr=0.0008

echo "长时间训练完成！"

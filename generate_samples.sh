#!/bin/bash
# 使用新的目录结构生成样本

# 激活conda环境
conda activate zi2zi_chain

# 创建样本目录
mkdir -p /home/zihun/workspace/zi2zi-chain/samples_new

# 生成样本
echo "生成样本..."
python font2img.py --mode=font2font \
  --src_font=/home/zihun/workspace/zi2zi-chain/fonts/source/T1.ttf \
  --dst_font=/home/zihun/workspace/zi2zi-chain/fonts/target/M5.ttf \
  --sample_count=1000 \
  --sample_dir=/home/zihun/workspace/zi2zi-chain/samples_new \
  --label=0 \
  --filter \
  --canvas_size=256 \
  --char_size=220 \
  --x_offset=15 \
  --y_offset=15

# 打包样本
echo "打包样本..."
python package.py \
  --dir=/home/zihun/workspace/zi2zi-chain/samples_new \
  --save_dir=/home/zihun/workspace/zi2zi-chain/experiment_new/data \
  --split_ratio=0.1

echo "样本生成和打包完成！"

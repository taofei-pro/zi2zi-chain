#!/bin/bash
# 数据增强脚本 - 在训练过程中增加更多样本

# 激活conda环境
conda activate zi2zi_chain

# 创建新的样本目录
mkdir -p /home/zihun/workspace/zi2zi-chain/samples_augmented

# 生成不同参数的样本
echo "生成样本集1..."
python font2img.py --mode=font2font \
  --src_font=/home/zihun/workspace/zi2zi-chain/fonts/T1.ttf \
  --dst_font=/home/zihun/workspace/zi2zi-chain/fonts/M5.ttf \
  --sample_count=1000 \
  --sample_dir=/home/zihun/workspace/zi2zi-chain/samples_augmented \
  --label=0 \
  --filter \
  --canvas_size=256 \
  --char_size=210 \
  --x_offset=15 \
  --y_offset=15

# 创建新的样本目录
mkdir -p /home/zihun/workspace/zi2zi-chain/samples_augmented2

# 生成不同参数的样本
echo "生成样本集2..."
python font2img.py --mode=font2font \
  --src_font=/home/zihun/workspace/zi2zi-chain/fonts/T1.ttf \
  --dst_font=/home/zihun/workspace/zi2zi-chain/fonts/M5.ttf \
  --sample_count=1000 \
  --sample_dir=/home/zihun/workspace/zi2zi-chain/samples_augmented2 \
  --label=0 \
  --filter \
  --canvas_size=256 \
  --char_size=230 \
  --x_offset=5 \
  --y_offset=5

# 合并样本
mkdir -p /home/zihun/workspace/zi2zi-chain/samples_augmented_combined
cp /home/zihun/workspace/zi2zi-chain/samples_augmented/*.jpg /home/zihun/workspace/zi2zi-chain/samples_augmented_combined/
cp /home/zihun/workspace/zi2zi-chain/samples_augmented2/*.jpg /home/zihun/workspace/zi2zi-chain/samples_augmented_combined/

# 打包样本
echo "打包增强样本..."
python package.py \
  --dir=/home/zihun/workspace/zi2zi-chain/samples_augmented_combined \
  --save_dir=/home/zihun/workspace/zi2zi-chain/experiment_long/data_augmented \
  --split_ratio=0.1

echo "数据增强完成！"

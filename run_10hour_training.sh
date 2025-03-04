#!/bin/bash
# 10小时训练主脚本

echo "开始10小时训练流程..."

# 记录开始时间
start_time=$(date +%s)

# 第1步：开始长时间训练
echo "第1步：开始长时间训练..."
./train_long.sh &
training_pid=$!

# 第2步：等待1小时后进行数据增强
echo "等待1小时后进行数据增强..."
sleep 3600  # 等待1小时
./data_augmentation.sh

# 第3步：等待训练完成
echo "等待训练完成..."
wait $training_pid

# 第4步：进行推理
echo "第4步：进行推理..."
./infer_long.sh

# 记录结束时间并计算总时间
end_time=$(date +%s)
total_time=$((end_time - start_time))
hours=$((total_time / 3600))
minutes=$(((total_time % 3600) / 60))
seconds=$((total_time % 60))

echo "10小时训练流程完成！"
echo "总训练时间: ${hours}小时 ${minutes}分钟 ${seconds}秒"

# 创建训练结果摘要
echo "创建训练结果摘要..."
echo "训练结果摘要" > /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "总训练时间: ${hours}小时 ${minutes}分钟 ${seconds}秒" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "训练参数:" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 轮次: 100" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 批次大小: 16" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- L1损失权重: 180" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 常量损失权重: 20" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 类别损失权重: 1.5" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 学习率: 0.0008" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "- 学习率衰减周期: 15轮" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt
echo "推理结果保存在: experiment_long/infer_long_*/" >> /home/zihun/workspace/zi2zi-chain/training_summary.txt

echo "训练结果摘要已保存到 training_summary.txt"

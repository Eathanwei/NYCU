import openai

# 设置 OpenAI API 密钥
openai.api_key = ""

# 准备用于训练的数据集
training_data = [
    "Your training data example 1",
    "Your training data example 2",
    # Add more training data examples as needed
]

# 设置训练参数
training_params = {
    "model": "gpt-3.5-turbo",  # 选择要使用的 GPT-3 模型
    "n_epochs": 3,  # 训练轮数
    # Add more training parameters as needed
}

# 调用 OpenAI API 开始训练
response = openai.Train.create(training_data=training_data, **training_params)

# 输出训练结果
print(response)

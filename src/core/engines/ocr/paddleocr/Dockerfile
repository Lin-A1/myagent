# PaddleOCR Docker 镜像
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.0.0-gpu-cuda11.8-cudnn8.9-trt8.6

# 设置工作目录
WORKDIR /paddle

# 设置环境变量
ENV PYTHONPATH=/paddle
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN rm -rf /usr/lib/python3/dist-packages/PyYAML* && \
    rm -rf /usr/local/lib/python3.10/dist-packages/PyYAML* && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --ignore-installed PyYAML \
    paddleocr \
    fastapi \
    "uvicorn[standard]" \
    pillow \
    requests \
    python-multipart

# 复制项目文件到容器
COPY . /paddle/

# 创建模型目录和日志目录
RUN mkdir -p /paddle/model /paddle/logs

# 下载 PaddleOCR 模型（如果不存在）
# RUN python -c "import paddleocr; import os; ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='ch'); print('Models downloaded successfully!')"

# 暴露端口
EXPOSE 8001

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# 启动命令
CMD ["python", "server.py"]
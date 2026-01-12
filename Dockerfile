# HabitBloom APK 打包 Docker 镜像
FROM ubuntu:22.04

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 安装基础工具
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 配置 Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# 安装 Buildozer
RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app/

# 默认命令
CMD ["buildozer", "android", "debug"]

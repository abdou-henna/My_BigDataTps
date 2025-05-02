FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HADOOP_VERSION=3.3.6
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    ssh \
    rsync \
    curl \
    nano \
    sudo \
    openssh-server \
    net-tools \
    iputils-ping \
    vim \
    lsof && \
    apt-get clean

RUN mkdir /var/run/sshd

RUN useradd -ms /bin/bash hduser && \
    echo "hduser:hduser" | chpasswd && \
    adduser hduser sudo

RUN curl -O https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    chown -R hduser:hduser $HADOOP_HOME && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

RUN ssh-keygen -A
USER hduser
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

COPY config/* $HADOOP_HOME/etc/hadoop/

USER root
EXPOSE 9870 9864 8088 8042 22

CMD service ssh start && tail -f /dev/null

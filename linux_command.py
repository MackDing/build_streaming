# -*- coding: utf-8 -*-
# @Author: Pegin
# @Time: 2021/7/16 15:47
# @File: linux_command.py
# @Software: PyCharm

import paramiko

from datetime import datetime


class LinuxCommand:

    def __init__(self, hostname=None, port=None, username=None, password=None):
        self.linux_client = paramiko.SSHClient()
        self._connect_server(hostname=hostname, port=port,
                             username=username, password=password)

    def _connect_server(self, hostname=None, port=None, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.pwd = password
        self.linux_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 取消安全认证
        try:
            self.linux_client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.pwd
            )
        except Exception as err:
            # logging.error(err)
            print(err)

    def exec_command(self, cmd: str, out_error=False):
        try:
            stdin, stdout, stderr = self.linux_client.exec_command(cmd,
                                                                   timeout=1000)
            result = str(stdout.read(), encoding='utf-8')
            list_result = result.strip().split('\n')
            status = stderr.channel.recv_exit_status()
            result_err = bytes.decode(stderr.read())
            # stdin = bytes.decode(stdin.read())
            # if not result and out_error:
            #     list_result = result_err

            print(f'command:"{cmd}"')
            print(f'command results:{str(list_result)}')
            if status:
                # logging.error(bytes.decode(stderr.read()))
                print(result_err)
            if status and out_error:
                return result_err

            return list_result

        except Exception as err:
            print(err)

    def exec_no_return_command(self, cmd: str, out_error=False):
        try:
            transport = self.linux_client.get_transport()
            channel = transport.open_session()

            channel.exec_command(cmd)

        except Exception as err:
            print(err)

    ##########
    # 获取服务器性能数据
    ##########
    def get_linux_cpu_temperature(self):
        """
        :return: 去除符号后的CPU温度数据
        """
        cpu_command = "sensors |grep Core|awk '{print $3}'"
        initial_data = self.exec_command(cpu_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        for data in initial_data:
            data = data.strip()[:-2]
            revised_data.append(data)
        return revised_data

    def get_linux_gpu_temperature(self):
        """
        获取服务器的GPU温度
        :return: GPU温度数据
        """
        gpu_command = "nvidia-smi |grep Default|awk '{print $3}'"
        initial_data = self.exec_command(gpu_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        for data in initial_data:
            data = data.strip()[:-1]
            revised_data.append(data)
        return revised_data

    def get_linux_gpu_total_memory_usage(self):
        """
        获取服务器的GPU显存的总使用量
        :return: GPU显存的总使用量
        """
        gpu_command = "nvidia-smi |grep Default|awk '{print $9}'"
        initial_data = self.exec_command(gpu_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        temp_data = []
        for data in initial_data:
            # 如果含有MiB，插入temp
            if 'MiB' in data:
                data = data.strip()[:-3]
                temp_data.append(data)

        # 如果temp只有一个元素，加入revised
        if len(temp_data) == 1:
            revised_data.append(temp_data[0])
        # 如果有多个元素，计算占用最大值(使用量)
        elif len(temp_data) > 1:
            max_data = max(temp_data)
            # 如果多个元素使用量相同，写入多个数据
            for i in range(temp_data.count(max_data)):
                revised_data.append(max_data)
        # 如果没有有效数据，返回原始数据
        else:
            revised_data.append('未找到有效数据，命令返回为：')
            for data in initial_data:
                data = data.strip()
                revised_data.append(data)
        return revised_data

    def get_linux_total_gpu_memory(self):
        """
        获取服务器的GPU显存的总量
        :return: GPU显存的总量
        """
        gpu_command = "nvidia-smi |grep Default|awk '{print $11}'"
        initial_data = self.exec_command(gpu_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        temp_data = []
        for data in initial_data:
            # 如果含有MiB，插入temp
            if 'MiB' in data:
                data = data.strip()[:-3]
                temp_data.append(data)

        # 如果temp只有一个元素，加入revised
        if len(temp_data) == 1:
            revised_data.append(temp_data[0])
        # 如果有多个元素，计算占用最大值(使用量)
        elif len(temp_data) > 1:
            max_data = max(temp_data)
            # 如果多个元素使用量相同，写入多个数据
            for i in range(temp_data.count(max_data)):
                revised_data.append(max_data)
        # 如果没有有效数据，返回原始数据
        else:
            revised_data.append('未找到有效数据，命令返回为：')
            for data in initial_data:
                data = data.strip()
                revised_data.append(data)
        return revised_data

    def get_linux_gpu_memory_usage(self):
        """
        获取服务器的显存使用数据
        :return: 显存使用数据
        """
        gpu_memory_command = 'nvidia-smi |grep ias'
        initial_data = self.exec_command(gpu_memory_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        for data in initial_data:
            for p_data in data.strip().split():
                if 'MiB' in p_data:
                    revised_data.append(p_data[:-3])
        return revised_data

    def get_linux_mem(self):
        """
        获取服务器内存使用数据
        :return: 内存使用数据
        """
        mem_command = 'free -m |grep Mem'
        initial_data = self.exec_command(mem_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        data = initial_data[0].strip().split()
        total_mem = data[1]
        usage_mem = data[2]
        mem_usage_rate = int(usage_mem) / int(total_mem)
        revised_data += [usage_mem, total_mem, mem_usage_rate]
        return revised_data

    def get_linux_cpu(self):
        """
        获取服务器CPU使用数据
        :return: CPU使用数据
        """
        cpu_command = "top -b -n1 | sed -n '3p'|awk '{print $2}'"
        initial_data = self.exec_command(cpu_command)
        revised_data = [str(datetime.now())[11:19]]
        if len(initial_data) is 0 or initial_data is None or initial_data[0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data
        data = initial_data[0].strip()
        revised_data.append(data)
        return revised_data


class FtpCommand:

    # 初始化连接创建Transport通道
    def __init__(self, hostname=None, port=None, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.pwd = password
        self.__transport = paramiko.Transport((self.hostname, self.port))
        self.__transport.banner_timeout = 60
        self.__transport.connect(username=self.username, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode='0777'):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)


if __name__ == '__main__':
    l_client = LinuxCommand()
    # r = l_client.get_linux_gpu_temperature()
    # csv_file = open("abc.csv", "w", newline="", encoding="utf-8")
    # csv_write = csv.writer(csv_file, dialect="excel")
    # csv_write.writerow(r)
    # l_client.get_linux_mem()
    # print(l_client.get_linux_gpu_total_memory_usage())
    l_client.transfer_files(r'D:\WorkSpace\Project\Developers\ModelTest\IAS\ias_v4.74_cv4.1.tar.gz')

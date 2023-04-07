# -*- coding: utf-8 -*-
# @Author: Pegin
# @Time: 2021/7/16 15:56
# @File: docker_command.py
# @Software: PyCharm
import os
import time

from linux_command import LinuxCommand


class DockerCommand(LinuxCommand):

    def __init__(self, hostname=None, port=None, username=None, password=None):
        super().__init__(hostname, port, username, password)

        self.sdk_image = None
        self.sdk_container_id = None

    def pull_image(self, image):
        pull_image_command = 'docker pull '
        pull_ias_image_command = pull_image_command + image
        pull_result = self.exec_command(pull_ias_image_command)
        pull_sdk_image_command = pull_image_command + self.sdk_image
        pull_result.append(self.exec_command(pull_sdk_image_command))
        return pull_result

    # def run_sdk_container(self, sdk_image, path):
    #     container_run_command = \
    #         'docker run -itd --runtime=nvidia --privileged ' \
    #         f'-v /home/caf/dataset/{path}:/usr/local/ev_sdk/bin/dataset ' \
    #         f'-v /home/caf/result/{path}:/usr/local/ev_sdk/bin/result ' \
    #         f'-v /home/caf/script:/usr/local/ev_sdk/bin/script  ' \
    #         '-v /etc/localtime:/etc/localtime:ro -p ${p1}:10000 -p ${p2}:80 -e LANG=C.UTF-8 ' \
    #         f'-e NVIDIA_VISIBLE_DEVICES=all -e CUDA_VISIBLE_DEVICES=0 '
    #     container_run_command += sdk_image
    #     container_run_command += ' /bin/bash'
    #     print(container_run_command)
    #
    #     docker_run_result = self.exec_command(container_run_command)
    #     try:
    #         self.sdk_container_id = docker_run_result[0][:12]
    #         print(f'容器{self.sdk_container_id}启动成功')
    #         return self.sdk_container_id
    #     except Exception as err:
    #         print(err)

    def run_sdk_container(self, sdk_image, path):
        container_run_command = \
            'docker run -itd --runtime=nvidia --privileged  -e NVIDIA_VISIBLE_DEVICES=all -e CUDA_VISIBLE_DEVICES=0 '
        container_run_command += sdk_image
        container_run_command += ' /bin/bash'
        print(container_run_command)

        docker_run_result = self.exec_command(container_run_command)
        try:
            self.sdk_container_id = docker_run_result[0][:12]
            print(f'{self.sdk_container_id} 容器启动成功')
            return self.sdk_container_id
        except Exception as err:
            print(err)

    def get_container_port_mapping_80(self, container_id):
        get_port_command = 'docker port '
        get_port_command += container_id
        get_port_command += ' |grep 80/tcp'
        result = self.exec_command(get_port_command)
        port_80 = 80
        try:
            for port in result:
                if '80/tcp' in port:
                    port_80 = int(port[18:])
                    print(
                        f'container:{container_id} 80 port mapping to {port_80}')
                    return port_80
        except Exception as err:
            print(err)

    def get_sdk_container_port_mapping_80(self):
        # try:
        #     sc_id = self._get_running_containers_by_image(self.sdk_image)
        #     if len(sc_id) > 1:
        #         raise SDKPortError(sc_id)
        #     else:
        #         self.sdk_container_id = sc_id[0]
        #         Log.get_logger().warning(f'{PubConfig.SERVER_IP} started SDK Container, ID: {self.sdk_container_id}')
        #
        # except Exception as err:
        #     Log.get_logger().error(f'{PubConfig.SERVER_IP}{err}')
        result = self.get_container_port_mapping_80(self.sdk_container_id)
        return result

    def get_running_sdk_container(self):
        result = self._get_running_containers_by_image(self.sdk_image)
        return result

    def _get_running_containers_by_image(self, image):
        get_containers_command = 'docker ps -qf ancestor='
        get_containers_command += image
        result = self.exec_command(get_containers_command)
        return result

    def _get_all_containers_by_image(self, image):
        get_all_containers_command = 'docker ps -aqf ancestor='
        get_all_containers_command += image
        result = self.exec_command(get_all_containers_command)
        return result

    def _kill_container_by_id(self, container_id):
        if container_id:
            kill_command = 'docker kill '
            kill_command += container_id
            result = self.exec_command(kill_command)
            if result[0] in container_id or container_id in result[0]:
                print(f'{container_id} kill success')
            else:
                print(f'{container_id} kill fail')

    def _kill_skd_container(self):
        containers_id = self._get_running_containers_by_image(self.sdk_image)
        for c_id in containers_id:
            self._kill_container_by_id(c_id)

    def _remove_container_by_id(self, container_id):
        if container_id:
            remove_command = 'docker rm '
            remove_command += container_id
            result = self.exec_command(remove_command)
            if result[0] in container_id or container_id in result[0]:
                print(f'{container_id} rm success')
            else:
                print(f'{container_id} rm fail')

    def _remove_sdk_container(self):
        containers_id = self._get_all_containers_by_image(self.sdk_image)
        for c_id in containers_id:
            self._remove_container_by_id(c_id)

    def clean_sdk_containers(self):
        self._kill_skd_container()
        self._remove_sdk_container()

    ##########
    # 在宿主机上运行docker脚本
    ##########
    def _docker_exec_base(self, workdir, container_id, command,
                          need_result=True):
        if need_result:
            docker_exec_base_command = f'docker exec -i --privileged -w {workdir} {container_id} {command}'
        else:
            docker_exec_base_command = f'docker exec -d --privileged -w {workdir} {container_id} {command}'
        print(docker_exec_base_command)
        result = self.exec_command(docker_exec_base_command)
        return result

    def docker_exec_base(self, container_id, command,
                         workdir='/usr/local', out_error=True,
                         need_result=True):
        if need_result:
            docker_exec_base_command = f'docker exec -i --privileged -w {workdir} {container_id} bash -c "{command}"'
        else:
            docker_exec_base_command = f'docker exec -d --privileged -w {workdir} {container_id} bash -c "{command}"'
        result = self.exec_command(docker_exec_base_command, out_error)
        time.sleep(5)
        return result

    ##########
    # 性能数据
    ##########
    def get_container_cpu_usage(self, containers_id: list):
        cpu_usage_command = 'docker stats --no-stream --format "table{{.Container}}\t{{.CPUPerc}}"'
        initial_data = self.exec_command(cpu_usage_command)
        revised_data = []
        if len(initial_data) == 0 or initial_data is None or initial_data[
            0] is None:
            revised_data.append('未找到有效数据，命令无返回')
            return revised_data

        for c_id in containers_id:
            for data in initial_data:
                p_data = data.strip().split()
                if c_id == p_data[0]:
                    revised_data += [p_data[1]]
                    break
        return revised_data


if __name__ == '__main__':
    dc = DockerCommand()
    # dc.clean_ias_containers()
    # dc.clean_sdk_containers()
    # dc._get_opencv_version('4124dd1ff7c2774d574b434f73388f6acf5a7b9a25540d91686b5a23ea8d2f68')
    # dc._chmod_install('4124dd1ff7c2774d574b434f73388f6acf5a7b9a25540d91686b5a23ea8d2f68')
    # dc._install_ias('4124dd1ff7c2774d574b434f73388f6acf5a7b9a25540d91686b5a23ea8d2f68')
    # version = dc.get_sdk_version(container_id='34558046407f')
    # print(version)
    dc.run_sdk_container("cvmart-zhuhai-tcr.tencentcloudcr.com/sdk/grounddustidentification_14177:v1.0.5")

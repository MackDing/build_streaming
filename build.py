# -*- coding: utf-8 -*-
# @Author: 丁燃
# @File: push_package.py
# @Software: PyCharm


import os
import time

from docker_command import DockerCommand
from linux_command import FtpCommand


class RunDataset:
    dc = DockerCommand(hostname='192.168.1.107', port=20022,
                       username='root', password='y36py5jz')
    ftp = FtpCommand(hostname='192.168.1.107', port=20022,
                     username='root', password='y36py5jz')

    def __init__(self, image_id=None, dataset_path=None, new_package_name=None):
        self.image_id = image_id
        self.dataset_path = dataset_path
        self.new_package_name = new_package_name
        self.container_id = None
        self.result_timestamp = f"{time.strftime('%Y_%m_%d_%H_%M_%S')}"

    def start_container(self):
        self.container_id = self.dc.run_sdk_container(
            sdk_image=self.image_id, path=self.result_timestamp)

    def run_script(self):
        # self.ftp.upload(
        #     local_path=r'./clean.sh',
        #     remote_path=f'/usr/local/clean.sh'
        # )
        self.dc.exec_command(
            f'docker cp /home/mack/new_package_tools/clean.sh {self.container_id}:/usr/local/ev_sdk/bin')

        # self.ftp.upload(
        #     local_path=r'./install',
        #     remote_path=f'/usr/local/install'
        # )
        self.dc.exec_command(
            f'docker cp /home/mack/new_package_tools/install {self.container_id}:/usr/local/ev_sdk/bin')

        self.ftp.upload(
            local_path=self.dataset_path,
            remote_path=f'/home/mack/new_package_tools/{os.path.basename(self.dataset_path)}'
        )
        self.dc.exec_command(
            f'docker cp /home/mack/new_package_tools/{os.path.basename(self.dataset_path)} {self.container_id}:/usr/local/ev_sdk/bin')

        self.dc.docker_exec_base(container_id=self.container_id,
                                 command=f'. ./usr/local/ev_sdk/bin/install {os.path.basename(self.dataset_path)}',
                                 need_result=False)

        self.dc.docker_exec_base(container_id=self.container_id,
                                 command='. ./usr/local/ev_sdk/bin/clean.sh',
                                 need_result=False)

        self.dc.exec_command(f'docker commit {self.container_id} {self.new_package_name}')

        self.dc.exec_command(f'docker push {self.new_package_name}')
        print(f"{self.new_package_name} push Successful")

        self.dc.exec_command(f'docker rm -f {self.container_id}')


if __name__ == '__main__':
    run = RunDataset(
        image_id='cvmart-zhuhai-tcr.tencentcloudcr.com/pack-sdk/dev_chaojingjian_shiyuan_gpu_sdk4.0_modc_lic1b:v1.3.5',
        dataset_path=r'K:\package\vas\vas_v6.5.0_cv4.5.1_cuda11.1.tar.gz',
        new_package_name='cvmart-zhuhai-tcr.tencentcloudcr.com/public_images/dev_chaojingjian_shiyuan_gpu_sdk4.0_vas_v6.5.0_cv4.5.1:v13.5'

    )

    run.start_container()
    run.run_script()

# homelab


## Install PyInfra

```bash

pip install pyinfra

pyinfra ssh-server-name exec -- echo "hello world"


pyinfra server-name deploy.py

```

## Install Docker

```bash

# Maintained by Debian
apt-get install docker.io docker-compose -y

OR

curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $(whoami)
exit

OR

# Maintained by Docker
apt-get install docker-ce docker-ce-cli containerd.io -y

```


---

### Development Notes

```bash


sudo apt-get install docker-ce docker-ce-cli containerd.io


sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"

sudo apt-get install kubelet kubeadm kubectl

sudo swapoff -a


sudo kubeadm init --control-plane-endpoint=$IPADDR --pod-network-cidr=$POD_CIDR --node-name $NODENAME --apiserver-cert-extra-sans=$IPADDR --ignore-preflight-errors Swap

kubeadm token create --print-join-command

docker run -d --restart=unless-stopped \
 -p 80:80 -p 443:443 \
 --privileged \
 rancher/rancher:latest



curl -sfL https://get.k3s.io | sh -
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644





https://phoenixnap.com/kb/how-to-install-kubernetes-on-a-bare-metal-server

https://dockerlabs.collabnix.com/kubernetes/beginners/install/ubuntu/18.04/install-k8s.html

```
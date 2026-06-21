---


title: 'fix ''certificate apiserver-kubelet-client not signed by CA certificate ca:
  crypto/rsa: verification error'' error during minikube start'
date: '2021-08-25T00:00:00+00:00'
lastmod: '2021-08-25T00:00:00+00:00'
slug: fix-certificate-apiserver-kubelet-client-not-signed-by-ca-certificate-ca-crypto-rsa-verification-error-error-during-minikube-start
categories:
- devops
tags:
- "kube"
- "kubectl"
- "minikube"
- "certificate"
- "apiserver"
draft: false
---
I tried some solutions from [here](https://github.com/kubernetes/minikube/issues/4835) but it did not work. I deleted `~/.kube` directory and it just made matters worse.

My solution is

```generic
$ minikube delete
$ minikube start
```

The `~/.kube` directory was restored after doing this. I guess minikube takes care of initial .kube directory contents if there isn’t any. The `~/.kube/config` file was created with minikube’s cluster info populated.

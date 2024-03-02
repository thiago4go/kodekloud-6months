# CKAD

Making most of the labs in KodeKloud

## CKAD Curriculum

*   ### Application Design and Build

    20%

<!---->

* [ ] Define, build and modify containers images
* [ ] Choose and use the right workload resource (Deployment, DeamonSet, Cronjb, etc.)
* [ ] Understand multi-container Pod design patterns (e.g. sidecar, init and others)
* [ ] Utilize persistent and ephemeral volumes

<!---->

*   ### Application Deployment

    20%

<!---->

* [ ] Use kubernetes primitives to implement common deployment strategies( e.g. blue/gree or canary)
* [ ] Undestand Deploymenets and how to perform rolling updates
* [ ] Use the Helm package manager to deploy existing packages
* [ ] Kustomize

<!---->

*   ### Application Observability and Maintenance&#x20;

    15%

<!---->

* [ ] Understand API deprecations
* [ ] Implement probes and health checks
* [ ] Use built-in CLI tools to monitor Kubernetes applications
* [ ] Utilize containers logs
* [ ] Debugging in Kubernetes



*   ### Application Enviroment, Configuration and Security

    25%

<!---->

* [ ] Discover and use resources that extend Kubernetes (CRD, Operatiors)
* [ ] Understand authentication, auhorization and admission control
* [ ] Understand requests, limits, quotas
* [ ] Understand ConfigMaps
* [ ] Define resource requirements
* [ ] Create & consume Secrets
* [ ] Understand ServiceAccounts
* [ ] Understand Appliocation Security (SecurityContexts, Capabilities, etc.)



*   ### Services and Networking

    20%

<!---->

* [ ] Demonstrate basic understanding of NetworkPolicies
* [ ] Provide and troubleshoot access to applications via services
* [ ] Use Ingress rules to expose applications



The CKAD Certification focuses on the skills required to be a successuful Kubernetes Application Developer in industry today, The exame assumes working knowledge of container runtimes and microservice architecture.

The sucessful candidate will be confortable:

Working with (OCI-compliant) container images

Applying Cloud Native application concepts and architectures

Working with and validating Kubernetes resource definitions



The exam is based on Kubernetes V1.29



### **Resources allowed during exam**

Please review the Resources Allowed information published here: [CKA & CKAD Resources Allowed](https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed#certified-kubernetes-administrator-cka-and-certified-kubernetes-application-developer-ckad)\


### **Exam Technical Instructions**

1. Root privileges can be obtained by running 'sudo −i'.
2. You must NOT reboot the base node (hostname **node-1)**. Rebooting the base node will NOT restart your exam environment.
3. Do not stop or tamper with the certerminal process as this will END YOUR EXAM SESSION.
4. Do not block incoming ports 8080/tcp, 4505/tcp and 4506/tcp. This includes firewall rules that are found within the distribution's default firewall configuration files as well as interactive firewall commands.
5.  Use Ctrl+Alt+W instead of Ctrl+W.

    5.1 Ctrl+W is a keyboard shortcut that will close the current tab in Google Chrome.
6.  The Terminal (Terminal Emulator Application) is a Linux Terminal; to copy & paste within the Linux Terminal you need to use LINUX shortcuts:

    Copy  = Ctrl+SHIFT+C (inside the terminal)\
    Paste = Ctrl+SHIFT+V (inside the terminal)\
    OR Use the Right Click Context Menu and select Copy or Paste
7. For security reasons, the INSERT  key is prohibited within the Remote Desktop. \
   Candidates can Type i to switch into insert mode so that you can start editing the file. \
   Once you're done, press the escape key Esc to get out of insert mode and back to command mode.
8. Installation of services and applications included in this exam may require modification of system security policies to successfully complete.

### **CKA & CKAD Environment**

* Each task on this exam must be completed on a designated cluster/configuration context.
* An infobox at the start of each task provides you with the cluster name/context information.&#x20;
* Nodes making up each cluster can be reached via ssh, using a command such as the following: ssh \<nodename>
  * NOTE: You must return to the base node (hostname node-1) after completing each task.
  * Nested-ssh is not supported.
* You can assume elevated privileges on any node by issuing the following command: sudo -i
* You can also use sudo to execute commands with elevated privileges at any time
* You can use kubectl and the appropriate context to work on any cluster from the base node. When connected to a cluster member via ssh, you will only be able to work on that particular cluster via kubectl.
* For your convenience, all environments, in other words, the base system and the cluster nodes, have the following additional command-line tools pre-installed and pre-configured:
  * `kubectl` with `k`alias and Bash autocompletion
  * `jq` for YAML/JSON processing
  * `tmux` for terminal multiplexing
  * `curl` and `wget` for testing web services
  * `man` and man pages for further documentation
* Further instructions for connecting to cluster nodes will be provided in the appropriate tasks
* Where no explicit namespace is specified, the default namespace should be acted upon.
* If you need to destroy/recreate a resource to perform a certain task, it is your responsibility to back up the resource definition appropriately prior to destroying the resource.

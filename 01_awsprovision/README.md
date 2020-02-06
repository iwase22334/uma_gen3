# uma_aws
```
./dumpsql.sh
(cd terraform; terraform init;) # update trraform module
ansible-playbook create.yml
ansible-playbook -i inventory/ec2.py provision.yml
ansible-playbook harvst.yml
ansible-playbook destroy.yml
```

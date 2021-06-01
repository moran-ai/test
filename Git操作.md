



# Git操作

#### 1.先在本地创建一个文件夹，用来做为本地仓库

```shell
20622@DESKTOP-4PHULHH MINGW64 /
$ cd D:\githubfile

20622@DESKTOP-4PHULHH MINGW64 /d/githubfile
$ cd demo
```

#### 2.进行初始化

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo
$ git init
Initialized empty Git repository in D:/githubfile/demo/.git/
```

#### 3.需要提前在文件夹中创建一个md文件，然后在这个文件中写入一些内容

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ touch README.md
```

#### 4.初始化这个mk文件

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$  git add README.md
```

#### 5.提交这个md文件到远程仓库  

提交时出现了这个错误，原因是gitbase是区分大小写的，所以需要忽视大小写

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git commit -m README.md
On branch master
nothing to commit, working tree clean
```

忽视大小写

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git config core.ignorecase false
```

进行提交，但出现了一个问题

因为 mi-flex.html 有更新未跟踪，使用git commit -am可以省略使用git add命令将已跟踪文件放到暂存区的功能
即可提交成功

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git commit -m README.md
On branch master
Changes not staged for commit:
        modified:   README.md

no changes added to commit
```

使用git commit -am进行提交，即可提交成功

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git commit -am README.md
[master 458227c] README.md
 1 file changed, 1 insertion(+)
```

#### 6.提交到github

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git remote add origin https://github.com/moran-ai/test.git
```

git remote add origin https://github.com/moran-ai/test.git 这个链接每个仓库都不一样

#### 7.提交

在提交时出现了错误

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (master)
$ git push -u origin main
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/moran-ai/test.git'
```

md文件中写入内容

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test
$ echo "#test" >> README.md
```

初始化

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test
$ git init
Initialized empty Git repository in D:/githubfile/git_test/.git/
```

添加md文件

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test (master)
$ git add README.md
warning: LF will be replaced by CRLF in README.md.
The file will have its original line endings in your working directory
```

提交

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test (master)
$ git commit -m "first commit"
[master (root-commit) b4fa78b] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

连接到远程仓库

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test (master)
$ git remote add origin git@github.com:tianqixin/runoob-git-test.git
```

提交，但出现了问题

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test (master)
$ git push -u origin master
The authenticity of host 'github.com (13.229.188.59)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com,13.229.188.59' (RSA) to the list of known hosts.
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

解决：配置公钥

```shell
20622@DESKTOP-4PHULHH MINGW64 /D/githubfile/git_test (master)
$ cd ~/.ssh

20622@DESKTOP-4PHULHH MINGW64 ~/.ssh
$ ls
known_hosts

20622@DESKTOP-4PHULHH MINGW64 ~/.ssh
$ git config --global --list
user.name=moran-ai
user.email=58198222+moran-ai@users.noreply.github.com
filter.lfs.process=git-lfs filter-process
filter.lfs.required=true
filter.lfs.clean=git-lfs clean -- %f
filter.lfs.smudge=git-lfs smudge -- %f
http.sslverify=false
```

配置公钥的格式  多敲几次回车  会在C盘生成id_rsa.pub和id_rsa 两个文件

```
$ ssh-keygen -t rsa -C "自己的邮箱"
```

然后将id_rsa.pub的内容复制到github的公钥中去

进行测试，成功的结果如下

```shell
20622@DESKTOP-4PHULHH MINGW64 ~/.ssh
$ ssh -T git@github.com
Hi moran-ai! You've successfully authenticated, but GitHub does not provide shell access.
```

https://www.cnblogs.com/zhangguorenmi/p/13034989.html





# 错误解决

错误1：

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/git_test (main)
$ git push -u origin main
Logon failed, use ctrl+c to cancel basic credential prompt.
To https://github.com/moran-ai/test.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://moran-ai@github.com/moran-ai/test.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

解决： git pull --rebase origin master

https://blog.csdn.net/k_young1997/article/details/90489734



错误2：

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/git_test (master)
$ git push -u origin master
Logon failed, use ctrl+c to cancel basic credential prompt.
remote: Permission to moran-ai/test.git denied to moran-ai.
fatal: unable to access 'https://github.com/moran-ai/test.git/': The requested URL returned error: 403
```

解决：

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/git_test (master)
$ vim .Git/config
```

https://blog.51cto.com/chaohuang/1895880

### 错误3

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (main)
$ git push -u origin main
Logon failed, use ctrl+c to cancel basic credential prompt.
Everything up-to-date
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

解决：
 ① 输入git log 查看日志，会看到这样的一个序列号  commit后面是序列号

```shell
$ git log 
commit 8eeb457a55c0248d504bd1a3343174128592ecc1 (HEAD -> main, origin/main)
Author: moran-ai <58198222+moran-ai@users.noreply.github.com>
Date:   Tue Jun 1 10:33:17 2021 +0800

    first commit
```

②  输入命令：git reset --hard + 序列号

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (main)
$ git reset --hard 8eeb457a55c0248d504bd1a3343174128592ecc1
HEAD is now at 8eeb457 first commit
```

③ 输入命令： git add .

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (main)
$ git add .
```

④ 输入命令： git commit -m "five commit"  "" 中得内容是修改过后的信息

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (main)
$ git commit -m "five commit"
[main 80f77e4] five commit
 3 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 IMG_20201201_002733.jpg
 create mode 100644 IMG_20201201_002742.jpg
 create mode 100644 IMG_20201201_002904.jpg
```

⑤ 提交 输入命令：git push -f origin main   

```shell
20622@DESKTOP-4PHULHH MINGW64 /d/githubfile/demo (main)
$  git push -f origin main
Logon failed, use ctrl+c to cancel basic credential prompt.
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 8 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.30 MiB | 1003.00 KiB/s, done.
Total 5 (delta 0), reused 0 (delta 0)
To https://github.com/moran-ai/curriculum.git
   8eeb457..80f77e4  main -> main
```

https://www.cnblogs.com/kkvt/p/11692025.html



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





# 提交

创建一个新的仓库  需要创建一个README.md的文件

```
echo "# test" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/moran-ai/test.git
git push -u origin main
```

从现有的仓库进行推送

```
git remote add origin https://github.com/moran-ai/test.git
git branch -M main
git push -u origin main
```


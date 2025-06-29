# beyondtextmode
Images and Words - beyond text mode

This is a continuation after we've seen the structure of programs (executables/libraries) and the tools used to debug them. 
This section will keep the focus on the different ways that the flow of the code is handled. 

For this we'll give some examples on how real life applications are handled, how the flow is controlled.

We all know the "classic" applications that are the very start of programming. They are quite simple:

1. they start
2. receive some imput
3. process the input
4. display output
5. exit with some error code

An example is the `ls` program that lists the contents of the specified directory (or current one by default):

```
Manager:/usr # ls
bin  etc  include  lib  lib64  libexec  local  sbin  share  src  tmp  x86_64-suse-linux
Manager:/usr # echo $? # this is the exit code - 0 means success
0
Manager:/usr #
```

If the command has some options it can do something different. For example adding `-l` to the command yields this output:
```
Manager:/usr # ls -l
total 164
drwxr-xr-x   2 root root 40960 Apr 15 11:27 bin
drwxr-xr-x   2 root root  4096 May 25  2018 etc
drwxr-xr-x   3 root root  4096 Apr 15 11:16 include
drwxr-xr-x  73 root root  4096 Jun  2 13:08 lib
drwxr-xr-x  73 root root 69632 Jun  2 13:03 lib64
drwxr-xr-x   3 root root  4096 Feb 23  2024 libexec
drwxr-xr-x  11 root root  4096 Apr 15 11:27 local
drwxr-xr-x   2 root root 20480 Apr 15 11:16 sbin
drwxr-xr-x 137 root root  4096 Apr 15 11:16 share
drwxr-xr-x   3 root root  4096 Feb 23  2024 src
lrwxrwxrwx   1 root root     8 Apr 15 11:27 tmp -> /var/tmp
drwxr-xr-x   5 root root  4096 Feb 23  2024 x86_64-suse-linux
Manager:/usr #
```
In case of failure, we see that we get a failure code

```
Manager:/usr # ls non-existent-file-or-dir
ls: cannot access 'non-existent-file-or-dir': No such file or directory
Manager:/usr # echo $?
2
Manager:/usr #
```

This content was conceived while listening to these bands:

* Dream Theater https://www.youtube.com/watch?v=a9j-v9EbBBM
* Orbit Culture https://www.youtube.com/watch?v=cSmth9OTGvY
* Underworld https://www.youtube.com/watch?v=hRo4U_VHsYo
* Reverse The Moment (RO) https://www.youtube.com/watch?v=ffOxHPCiUMc


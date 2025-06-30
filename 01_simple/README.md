The simple flow of a program can be expressed in the following simple code example:

This program wants to be a replacement of `cat -n` command, that is printing the line numbers.

As you can see it just reads from stdin until there's noting more to read.

NOTE: Most of linux executables do simple tasks like this but together they can make very complex tasks, so don't disregard the utility of such programs.

```
iulians@tumbleweed:~> cat poor_cat_mn.c
#include<stdio.h>

#define MAXBUFLEN 1024

int main(void)
{
        char buffer[MAXBUFLEN+1];
        int counter = 0;
        while(fgets(buffer,MAXBUFLEN,stdin)) {
                buffer[MAXBUFLEN]='\0';
                fprintf(stdout,"%d %s",++counter,buffer);
        }
        return 0;
}
iulians@tumbleweed:~>
```

Compiling and running the code by reading from stdin (end with CTRL+D pressed in bash shell on an empty line)

```
iulians@tumbleweed:~> gcc -Wall poor_cat_mn.c -o catn
iulians@tumbleweed:~> ./catn
1
1 1
2
2 2
third line
3 third line
iulians@tumbleweed:~>
```

A clearer example is printing the code from the source file:

```
iulians@tumbleweed:~> cat poor_cat_mn.c | ./catn
1 #include<stdio.h>
2
3 #define MAXBUFLEN 1024
4
5 int main(void)
6 {
7       char buffer[MAXBUFLEN+1];
8       int counter = 0;
9       buffer[MAXBUFLEN]='\0';
10      while(fgets(buffer,MAXBUFLEN,stdin)) {
11              fprintf(stdout,"%d %s",++counter,buffer);
12      }
13      return 0;
14 }
iulians@tumbleweed:~>
```

It is similar to what cat -n provides
```
iulians@tumbleweed:~> cat -n < poor_cat_mn.c
     1  #include<stdio.h>
     2
     3  #define MAXBUFLEN 1024
     4
     5  int main(void)
     6  {
     7          char buffer[MAXBUFLEN+1];
     8          int counter = 0;
     9          buffer[MAXBUFLEN]='\0';
    10          while(fgets(buffer,MAXBUFLEN,stdin)) {
    11                  fprintf(stdout,"%d %s",++counter,buffer);
    12          }
    13          return 0;
    14  }
iulians@tumbleweed:~>
```

# The flow

The program is very simple. It has a loop that reads until there's nothing more to read, very simple doesn't interact with "unexpected" messages or something similar, just plain simple code flow.

It is very easy to understand because it will not make many interactions with the external environment, it will only read from a file (standard input is considered a file in Linux just like most of the things).

Next we'll study a more difficult program that will make an animation based on the keys that the user presses.

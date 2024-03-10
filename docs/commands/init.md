# init 

```shell
chef init <DIRECTORY> 
```

Sets up a new recipe library in the given directory. 

```shell
~/foo$ chef init .
robin@lgn:~/foo$ ll
total 28
drwxrwxr-x  5 robin robin  4096 Mar 10 15:20 ./
drwxr-xr-x 42 robin robin 12288 Mar 10 15:20 ../
drwxrwxr-x  2 robin robin  4096 Mar 10 15:20 .chef/
drwxrwxr-x  2 robin robin  4096 Mar 10 15:20 md/
drwxrwxr-x  2 robin robin  4096 Mar 10 15:20 yaml/
```
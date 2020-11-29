#Virtual Assistant

##To Run##

- clone this repo
- ```pip install requirements.txt```
- update the ```.env``` file with your information (the program will work as it is, you just wont be able to email or use wolfram)
Format of the ```.env``` script:

```

#.env
wolframappid = '*'
Your_Username = "*"
Codingemail = "*"
Normalemail = "*"
Your_Password = "*"

```


I will be trying to make this modular,  where there is one device (a raspberry pi probably) running a host script and that will send information to other pis, so they can do other things.

This will mean that all you have to do is edit a couple of lines and you are ready to go.

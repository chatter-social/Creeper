# Creeper
![Lines of code](https://img.shields.io/tokei/lines/github/chatter-social/Creeper?color=1) [![Chatterware](https://img.shields.io/badge/license%20addition-Chatterware-%2385ff95?labelColor=black)](https://github.com/chatter-social/chatterware)

Creeper is a dynamic, interpreted language.

## Demo

In this quick demo, I will explain how to write a basic program in Creeper that will display ten numbers of the Fibonacci sequence. I recommend using our Visual Studio Code extension while writing your program. You can get it [here](https://marketplace.visualstudio.com/items?itemName=Chatter.creeper-language).

```swift
// Creeper program to display the first few numbers of the Fibonacci sequence

// Declare our variables
var a = 0
var b = 1
var c = 0
// Main 'do' loop that performs the algorithm 10 times
do "c; var c = a + b; var a = b; var b = c" 10 times
```

First, we declare our variables. This involves setting 'a' to 0, 'b' to 1, and 'c' to 0. Next, we actually implement the algorithm. For each loop, we print the value of 'c'. Next, we initialize it to equal 'a' + 'b', the two previous numbers. Finally, it initializes the 'a' and 'b' variables with the previous numbers and repeats it ten times. You can run your program using 
```
python creeper.py {filename}.cre
```
Expected output:
```
Creeper Interpreter
0
1
2
3
5
8
13
21
34
55
```
## DISCLAIMER
Creeper is currently very young, and therefore lacks important features. Feature updates will occur very regularly.

##  Chatterware

<!-- Project --> is Chatterware! 🗣<br>
This means that you are free to use this project, as long as you give it a :star: and spread the word!
If you use this project, it is encouraged that you make a contribution, especially if you haven't ever contributed to open source!
Never contributed to open source? Read this guide: https://opensource.guide/how-to-contribute/ <br>
Your contributions make us _**chatter**_ appreciation! ❤️

Homework 05
===========

# Activity 1: hulk.py

## Question 1

I generated all of the candidate password combinations by implementing the permutations function. This function used recursion to yield all of the 
possible permutations of a given length with a given alphabet. I had base cases for if the length was zero or the length was one, but the only one 
that would normally be used is base case for the length being one. To find all the permutations I used a nested for loop, with the outside going through
each character in the alphabet and the inside going through each permutation of one shorter than the current case. By implementing this as a generator, 
we saved lots of memory as compared to using a list to store all of the permutations.

I used list comprehension to filter all of the candidate passwords to contain only the valid ones. I went through each permuataion, added the prefix 
to the front, encoded it using the sha1sum function, and checked if that was in the given set of hashes. If it was, I added it to my list of passwords 
and eventually returned the list.

I handled processing on multiple cores by mostly using the code that was given in the homework. All I had to do was make a list of prefixes, which 
consisted of the given prefix plus one letter from the given alphabet. I after doing this, I made a subfunction for smash that then was called using 
multiprocessing for however many cores were specified.

As I wrote each function, I would test it using the doctest. This way I could be sure that each function was working correctly before moving on to the 
next function. Once I wrote each function, I wrote main and started using the test script for hulk to see if it was working. Once the doctest and test 
script both indicated that the program was working, I started going through the hashes file that we were given to break the passwords. I did this for 
passwords up to 6 characters long and submitted my results to the deadpool, which indicated that I was right.


## Question 2

| Processes     | Time
---------------------------- 
| 1             | 3m 2.206s 
----------------------------              
| 2             | 1m 30.740s
----------------------------
| 4             | 0m 44.494s
----------------------------
| 6             | 0m 29.586s
----------------------------
| 8             | 0m 24.486s

The more processes utilized, the quicker the program is in cracking the passwords.


## Question 3

A longer password would be more difficult to brute force than a more complex alphabet. Since passwords can be thought of as permuatations of a certain 
length of letters from a given alphabet, permutations increase much more rapidly when you start choosing more from the alphabet than when you add to 
the alphabet, though both increase the number of possible permutations. When there are more permutations possible, it becomes more difficult for the 
program to brute-force the passwords.

 

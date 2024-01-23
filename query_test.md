This [article](https://flak.tedunangst.com/post/memory-leak-proof-every-C-program) is kind of cool as it basically defines
what memory leak is. Memory leak is condition when you ask memory from heap and store it in a pointer but you lost that
pointer somewhere else and you can't fucking free the memory.

Here, author just creates a wrapper around malloc so that whenever we allocate memory, it creates two pointer reference, one
given to us like normal pointer do and another saved in a array. Now later on, you can just free that whole array to free
the memory.

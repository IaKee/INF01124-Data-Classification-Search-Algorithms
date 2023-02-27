This folder contains the implementation of hashing algorithms developed in a laboratory. The implemented hash function calculates the key of the given string based on the values of each character as they are read. It calculates the sum of the elements, where each position corresponds to a power of 27. For example, for the string "Casa", the algorithm calculates:

Value of character C * 27^3
Value of character A * 27^2
Value of character S * 27^1
Value of character A * 27^0

For comparison purposes, the algorithm considers the given string to be formed only by uppercase characters. In case of a collision during the insertion of a new element in the table, the element will be inserted in a linked list, in the corresponding hash (the element is always inserted at the end of the list), as proposed in the assignment.
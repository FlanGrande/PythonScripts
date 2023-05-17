# Program that shifts text by a given number of characters from input.txt to output.txt
# Every line contains a single word and a number of characters to shift

# Import the sys module
import sys

# Open the input.txt file for reading
inputFile = open("input.txt", "r")

# Open the output.txt file for writing
outputFile = open("output.txt", "w")

# Loop through the input file
for line in inputFile:
    # Split the line into a list
    lineList = line.split()

    # If the line is empty, skip it
    if len(lineList) == 0:
        continue

    # Get the word and number of characters to shift
    word = lineList[0]
    shift = int(lineList[1])

    # Loop through the word
    shiftedWord = ""
    for letter in word:
        # If the letter is not a letter, skip it
        if not letter.isalpha():
            shiftedWord += letter
            continue

        # Shift the letter by the number of characters to shift
        shiftedLetter = chr(ord(letter) + shift)

        # if the shifted letter is out of the bounds of the alphabet, wrap it around
        if shiftedLetter > "z":
            shiftedLetter = chr(ord(shiftedLetter) - 26)
        elif shiftedLetter < "a":
            shiftedLetter = chr(ord(shiftedLetter) + 26)
        
        # Add the shifted letter to the shifted word
        shiftedWord += shiftedLetter

    # Write the shifted word to the output file
    outputFile.write(shiftedWord + "\n")

# Close the input file
inputFile.close()

# Close the output file
outputFile.close()
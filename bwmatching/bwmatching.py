# python3
import sys


def PreprocessBWT(bwt):

  """
  Preprocess the Burrows-Wheeler Transform bwt of some text
  and compute as a result:
    * starts - for each character C in bwt, starts[C] is the first position 
        of this character in the sorted array of 
        all characters of the text.
    * occ_counts_before - for each character C in bwt and each position P in bwt,
        occ_counts_before[C][P] is the number of occurrences of character C in bwt
        from position 0 to position P inclusive.
  """

  # iterate through each char in string and map char to its index (list of indices where each char appears in the string)
  occurence_dict = dict()

  for i in range(len(bwt)):

    char = bwt[i]

    if not occurence_dict.get(char, None):

      occurence_dict.update({ char : [] })
    
    occurence_dict[char].append(i)

  occ_counts_before = { char : [] for char in list(occurence_dict.keys())}

  for char in occurence_dict.keys():

    i = 0
    j = 0

    occurences = occurence_dict[char]

    for occurence in occurences:

      # append the running counter (j) of occurences for that char it to the list until we reach the next occurence index
      # this works as the lists of indices in occurence_dict is in sorted order since we iterated from start to end of the string
      while i < occurence:

        occ_counts_before[char].append(j)

        i += 1

      # increment the running counter of occurences 
      j += 1
    
    # append j for the remaining indices up till the end of the string
    while i <= len(bwt):

      occ_counts_before[char].append(j)
      i += 1

  # get the set of chars in the string sorted lexigraphically
  chars = sorted(list(occ_counts_before.keys()))

  starts = {char : 0 for char in chars}

  i = 0
  for j in range(1, len(chars)):

    # the index of the first occurence of a char would be the number of occurences of the previous char added to the index of the first occurence of the previous char (which is represented by the pointer i)
    # e.g. string = 'AAABBBBCC'
    # starts[A] = 0, num_occurences[A] = 3. Thus, starts[B] = 3 + 0 = 3
    next_char = chars[j]
    char = chars[j-1]

    starts[next_char] += (i + occ_counts_before[char][len(bwt)])
    i = starts[next_char] 


  return starts, occ_counts_before


def CountOccurrences(pattern, bwt, starts, occ_counts_before):
  """
  Compute the number of occurrences of string pattern in the text
  given only Burrows-Wheeler Transform bwt of the text and additional
  information we get from the preprocessing stage - starts and occ_counts_before.
  """
  top = 0
  bottom = len(bwt)-1

  j = 1
 
  while top <= bottom:
    
    if j <= len(pattern):
      # the pattern has not been fully searched
      
      char = pattern[-j]

      if char not in starts:
        # the char is not a char in the string 
        return 0  

      
      # get the number of occurences of the char in the last column of our BWT matrix (i.e the input string) between the index/row range of top and bottom (inclusive)
      if top == 0:

        num_counts = occ_counts_before[char][bottom]

      else:

        num_counts = occ_counts_before[char][bottom] - occ_counts_before[char][top-1]

      if num_counts > 0:

        # the char occurs in the specified range
        # update top and bottom to the corresponding rows in the first col of the BWT matrix (i.e. sorted string)
        top = starts[char] + occ_counts_before[char][bottom] - num_counts
        bottom = starts[char] + occ_counts_before[char][bottom] - 1
       
      else:

        # char does not occur between top and bottom rows -> pattern not found
        return 0
    
    else:
      
      # pattern has been fully searched -> get the number of occurences of pattern
      return bottom - top + 1

    j += 1
     

if __name__ == '__main__':
  
  bwt = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()

  # Preprocess the BWT once to get starts and occ_counts_before.
  # For each pattern, we will then use these precomputed values and
  # spend only O(|pattern|) to find all occurrences of the pattern
  # in the text instead of O(|pattern| + |text|).  

  starts, occ_counts_before = PreprocessBWT(bwt)

  occurrence_counts = []

  for pattern in patterns:
    occurrence_counts.append(CountOccurrences(pattern, bwt, starts, occ_counts_before))

  print(' '.join(map(str, occurrence_counts)))


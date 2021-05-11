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

  occ_counts_before = dict()

  for i in range(len(bwt)):

    char = bwt[i]

    if not occ_counts_before.get(char, None):

      occ_counts_before.update({ char : [0 for j in range(len(bwt)+1)] })

    for index in range(len(bwt), 0, -1):

      if i <= index:

        occ_counts_before[char][index] += 1

      else:

        break
    
  chars = sorted(list(occ_counts_before.keys()))

  starts = {char : 0 for char in chars}

  i = 0
  for j in range(1, len(chars)):

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
      
      char = pattern[-j]

      if char not in starts:
        return 0

      # pattern = pattern[:-1]

      # print(char)
      # print(top, bottom)
      if top == 0:
        num_counts = occ_counts_before[char][bottom]

      else:

        num_counts = occ_counts_before[char][bottom] - occ_counts_before[char][top-1]

      if num_counts > 0:
        # bottom = starts[char] + num_counts  - 1
        # top = starts[char]
        # print('{} occurs {} times'.format(char, num_counts))
        top = starts[char] + occ_counts_before[char][bottom] - num_counts
        bottom = starts[char] + occ_counts_before[char][bottom] - 1
       
      else:

        return 0
    
    else:
      # print('done', top, bottom)
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

  # print(starts)
  # for char, index in occ_counts_before.items():
  #   print(char, occ_counts_before[char], '\n')

  occurrence_counts = []

  for pattern in patterns:
    occurrence_counts.append(CountOccurrences(pattern, bwt, starts, occ_counts_before))

  print(' '.join(map(str, occurrence_counts)))


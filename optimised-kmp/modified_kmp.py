### PLEASE NOTE: ALL THE COMMENTS AND DOCSTRING IN THIS FILE IS FORMATTED WITH LINE-WRAPPING AT 140 CHARACTERS.
### SOME DOCSTRING WILL NOT BE ALIGNED CORRECTLY IF LINE-WRAP IS BELOW THIS VALUE.

import sys

def get_z_array(str):
    """
    For 1-character pattern, use naive search (not implemented).
    """
    n = len(str)
    z = [0]*n
    # Comparision of str[1:] with prefix
    # Because the prefix is practically the substring str[1:]] 1 character prior, we only need to check each character with its previous.
    if n > 2:   # O(m+n)
        for i in range(1,n):
            if str[i] == str[i-1]:
                z[1] += 1
            else:
                break
    else:   # Handles 2-long patterns
        if str[1] == str[0]:
            z[1] += 1

    # Finished initiating Z[0] (or Z[1] in the lecture slides)
    # Begin using Z-boxes
    r = 0
    l = 0

    if z[1] > 0:
        r = z[1]
        l = 1

    for k in range(2,n):
        # Case 1:
        if k > r:
            for i in range(k,n):
                if str[i] == str[i-k]:
                    z[k] += 1
                else:
                    break
            r = i - 1
            l = k
        # Case 2:
        else:
            # Case 2a:
            if r - k + 1 > z[k - l]:
                z[k] = z[k-l]
            # Case 2b: z[k] must also be > r - k + 1. Compare characters from str[r+1] with str[r+1-(k+1)]
            else:
                # Use count to iterate r instead of having to use q. (q is the mismatch point in lecture slides)
                mismatched = False
                i = r + 1
                while (i < n) and not mismatched:
                    if str[i] == str[i-k]:
                        r += 1
                        i += 1
                    else:
                        break

                l = k
                z[k] = r - k + 1
    return z

def KMP(txt,pat):
    """
    Modified KMP to incoporate storing mismatched characters.
    """
    m = len(pat)
    n = len(txt)

    # Stores the sp[i] values according to the mismatched characters
    sp = [[0]*26 for _ in range(m)]   # 26 is alphabet size
    # The regular sp[i] values (for shifting when found an occurence)
    sp1 = [0]*m
    occur = []

    z = get_z_array(pat)

    # Get the sp[i] values and set them using the character at the position as key
    for j in range(m-1,0,-1):
        i = j + z[j] - 1
        x = pat[z[j] + 1]
        sp[i][ord(x)-97] = z[j]
        sp1[i] = z[j]

    i = 0
    j = 0
    while i < n:
        # Iterates until a mismatch or full match
        if pat[j] == txt[i]:
            i += 1
            j += 1

        # A full match, shift like the regular KMP
        if j == m:
            occur.append(i-j)
            j = sp1[j-1]

        # A mismatch, checks if the character is in the alphabet, if not just iterate i
        # If yes, use the new sp[i] table to shift using the information about mismatched characters
        if i < n and pat[j] != txt[i]:
            if j != 0:
                j = sp[j-1][ord(txt[i])-97]
                i += 1
            else:
                i += 1

    return occur

if __name__ == '__main__':
    txt_filename = sys.argv[1]
    pat_filename = sys.argv[2]

    txt_file = open(txt_filename,'r')
    txt = txt_file.read()
    txt_file.close()

    pat_file = open(pat_filename,'r')
    pat = pat_file.read()
    pat_file.close()

    found = KMP(txt,pat)
    #print(found)
    output = open('output_kmp.txt','w')
    for o in found:
        output.write(str(o+1)+'\n')

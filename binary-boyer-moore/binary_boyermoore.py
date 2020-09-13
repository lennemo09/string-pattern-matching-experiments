# Name: Ha Tri Nhan Luong
# ID: 29644364
# FIT3155 - Assignment 1 Q2.

### PLEASE NOTE: ALL THE COMMENTS AND DOCSTRING IN THIS FILE IS FORMATTED WITH LINE-WRAPPING AT 140 CHARACTERS.
### SOME DOCSTRING WILL NOT BE ALIGNED CORRECTLY IF LINE-WRAP IS BELOW THIS VALUE.

import sys

comp = 0
def get_z_array(str):
    """
    For 1-character pattern, use naive search (not implemented).
    """
    n = len(str)
    z = [0]*n
    global comp
    # Comparision of str[1:] with prefix
    # Because the prefix is practically the substring str[1:]] 1 character prior, we only need to check each character with its previous.
    if n > 2:   # O(m+n)
        for i in range(1,n):
            comp += 1
            if str[i] == str[i-1]:
                z[1] += 1
            else:
                break
    else:   # Handles 2-long patterns
        comp += 1
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
                comp += 1
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
                    comp += 1
                    if str[i] == str[i-k]:
                        r += 1
                        i += 1
                    else:
                        break

                l = k
                z[k] = r - k + 1
    return z


def bad_char_binary(str):
    """
    Extended bad character rule for binary alphabet.
    """
    m = len(str)
    # 2D array of size 2*m -> O(m)
    r = [[-1,-1] for _ in range(m)]
    for i in range(1,m):
        char = int(str[i-1]) # Because string is binary we can safely assume it is a valid int

        # Make sure string is binary
        assert char == 1 or char == 0

        # 1 - 0 = 1
        # 1 - 1 = 0
        # Use this fact to update the other character using only the current character
        r[i][char] = i - 1
        r[i][1-char] = r[i-1][1-char]

    return r

"""
OBSOLETE
DOES NOT WORK: IT MISSES MATCHES THAT ARE INBETWEEN DIVISIBLE CHUNKS
def bad_bits_binary(str,num_bits):

    #Essentially uses extended bad character heusristics on a string ~4 (by default of 4 bits) times shorter.
    #We will use this when k is divisible by 4 and there's a mismatch, thus guarantees a shift of at least 4 characters.

    m = len(str)
    assert num_bits < m

    max_dec = 2**num_bits - 1   # Max decimal value representable by a binary chunk
    rem = m % num_bits          # Remainder of string that couldn't fit into a chunk, haven't dealt with it yet?

    dec_array = []

    i = 0
    # Converts binary string to an array of decimals
    while i < m - rem:
        curr = str[i:i+num_bits]
        dec = int(curr,2)
        dec_array.append(dec)
        i += num_bits

    dec_m = len(dec_array)
    print(dec_array)
    r = [[-1]*(max_dec+1) for _ in range(dec_m)]
    for i in range(1,dec_m):
        char = dec_array[i-1]

        r[i][char] = i - 1

        for j in range(max_dec+1):
            if j == char:
                pass
            else:
                r[i][j] = r[i-1][j]

    return r
"""

def matched_prefix(str):
    m = len(str)
    mp = [0]*(m+1)
    z = get_z_array(str)

    for i in range(m-1,-1,-1):
        if z[i] + i == m:
            mp[i] = z[i]
        else:
            if i == 0: # Denotes the entire string as its own suffix and prefix (as the first index of Z-values doesn't have any meaning (0 by default))
                mp[i] = m
            else:
                mp[i] = mp[i+1]
    return mp

def good_suffix(str):
    m = len(str)
    str = str[::-1] # Reverse the string
    z_suffix = get_z_array(str)
    z_suffix.reverse()

    gs =  [0 for _ in range(m+1)]

    # Get gs[j] values
    for p in range(m-1):
        j = m - z_suffix[p]
        gs[j] = p

    mp = matched_prefix(str)
    #print(z_suffix)
    #print(gs)
    #print(mp)
    return z_suffix, gs, mp

#good_suffix('acababacaba')


def should_search(txt,pat):
    """
    One way to know if the pattern can even exist at all in the text is to check if the number of 1's and 0's in the pattern is
    (correspondingly) more than the number of 1's and 0's in the text.
    Another way to phrase it is: In order for it to be possible for the pattern to be in the text, the number of 1's in txt has to be >= number of 1's in pat AND number of 0's in txt has to be >= number of 0's in pat .
    e.g. if a pattern has more 1's than there are 1's in the text, it definitely cannot exist in the pattern.
    This takes O(m + n) time in preprocessing.
    """
    should_search = True

    txt_1s = 0
    txt_0s = 0
    pat_1s = 0
    pat_0s = 0

    for c in txt:
        if c == '1':
            txt_1s += 1
        if c == '0':
            txt_0s += 1

    for c in pat:
        if c == '1':
            pat_1s += 1
        if c == '0':
            pat_0s += 1

    # According to the above rule, pattern cannot exist in text.
    if txt_0s < pat_0s or txt_1s < pat_1s:
        should_search = False

    return should_search


def bad_chunks(str,CHUNK_SIZE=3):
    m = len(str)

    # Get number of chunks
    if m % CHUNK_SIZE == 0:
        chunk_count = m // CHUNK_SIZE
    else:
        chunk_count = (m // CHUNK_SIZE) + 1

    assert CHUNK_SIZE < m

    max_dec = 2**CHUNK_SIZE - 1   # Max decimal value representable by a binary chunk
    rem = m % CHUNK_SIZE          # Remainder of string that couldn't fit into a chunk

    # Stores decimal values of chunks for each offset, if chunk is smaller than 3-bits, value is -1
    # O(3*m) = O(m)
    dec_array = [[-1]*chunk_count for _ in range(CHUNK_SIZE)]
    #print(dec_array)
    # O(3*m) = O(m)
    for off in range(CHUNK_SIZE):
        curr_chunk_num = 0
        bucket_start = 0
        bucket_end = 0 + off + 1

        while bucket_end <= m:
            #print(bucket_end,bucket_start)
            if bucket_end - bucket_start < CHUNK_SIZE:
                pass
            else:
                current_chunk = str[bucket_start:bucket_end]
                #print(current_chunk,curr_chunk_num)
                current_chunk_dec = int(current_chunk,2)
                dec_array[off][curr_chunk_num] = current_chunk_dec
            bucket_start = bucket_end
            bucket_end += CHUNK_SIZE
            curr_chunk_num += 1


    dec_m = len(dec_array[0])
    #print(dec_array)
    # Creates 3-D array R(x) * {decimal values} * offset
    # To get chunk_num of a chunk: chunk_num = R[offset][i][decimal value]
    # O(3*m*alphabet) = O(m)
    r_chunks = [[[-1]*(max_dec+1) for _ in range(chunk_count)] for _ in range(CHUNK_SIZE)]
    for o in range(CHUNK_SIZE):
        for i in range(1,dec_m):

            char = dec_array[o][i-1]
            #print(i,char)
            if char == -1:
                continue

            r_chunks[o][i][char] = i - 1
            for j in range(max_dec+1):
                if j == char:
                    pass
                else:
                    r_chunks[o][i][j] = r_chunks[o][i-1][j]
    #print(r_chunks[2])
    return(r_chunks)



def get_rightmost_chunk(str,k,r_chunks,CHUNK_SIZE=3):
    assert len(str) <= CHUNK_SIZE
    if k % CHUNK_SIZE == 0:
        k = k//CHUNK_SIZE
    else:
        k = k//CHUNK_SIZE + 1
    char_dec = int(str,2)
    chunk_num = -1
    off = -1
    for i in range(len(r_chunks)):
        #print(i,k,char_dec)
        #print(r_chunks[i])
        if r_chunks[i][k][char_dec] > chunk_num:
            chunk_num = r_chunks[i][k][char_dec]
            off = i
    if chunk_num == -1:
        return -1,-1
    return off,chunk_num

def get_new_chunk_k(off,chunk_num,CHUNK_SIZE=3):
    return off + chunk_num*CHUNK_SIZE


def bm_binary(txt,pat,CHUNK_SIZE=3):
    """
    For 1-character pattern, use naive search (not implemented).

    VERY IMPORTANT TO-DO: Find a way to split pat into chunks for bad "chunk" rule that does not miss matches that are inbetween 2 (or multiple) chunks. UPDATE: FINISHED IMPLEMENTATION.
    VERY IMPORTANT NOTE: Only implement chunks when the mismatch is the first character! (This is the only case where bad_char could match goodsuffix in shift count)

    Potential pseudocode:

    set an int CHUNK_SIZE
    if mismatched on first character of scan (k == m-1 and gs_shift == bad_char_shift):
        txt_chunk = txt[i+k-CHUNK_SIZE+1 : i+k+1]   # Chunk in text that ended in the mismatched character

        # Now we should find the rightmost occurence of this chunk in pat.
        # (only take the rightmost from the 3 segmentations, if there are multiple)
        # We can potentially avoid missing in-between chunks matches by creating CHUNK-SIZE number of tables, each is offset by 1 index
        # e.g. pat = 0010111000100 and the chunk we want to find is: 101.
        # We can have 3 different chunk segmentations:
        # off := offset from k
        #                                   k
        # off = 0: [0] [010] [111] [000] [100]
        # off = 1: [00] [101] [110] [001] [00]   <- We found RIGHMOST [101]
        # off = 2: [001] [011] [100] [010] [0]
        # chunk_no:   0   1     2     3     4
        # But this causes us to practically do 3 times the work of bad_character_rule, which is O(3m) -> O(m) but for large m this is not a # great way to do it?
        # Note: The number of chunks are the same for every length of pat for every offset.

    Assume we have found the chunk, which is identified by chunk_no (starting from 0 at k, increasing backwards).
    How do we use the chunk to shift?
    -> shift so that the old txt[i+k] is new aligned with new_k = off + chunk_no*CHUNK_SIZE
    """
    m = len(pat)
    n = len(txt)

    global comp
    shift_count = 0

    occur = []

    should = should_search(txt,pat)

    if should:

        #r = bad_char_binary(pat)   # Old bad character rule is not needed for binary
        r_chunks = bad_chunks(pat)
        #print(r)
        z_suffix, gs, mp = good_suffix(pat)

        galil_shifted = False
        galil_start = 0
        galil_stop = 0
        i = 0
        while i < (n-m) + 1:
            #print("i:",i)
            shift = 0

            #print('txt:',txt)
            #print('pat:' + i*' ',pat)
            k = m-1
            while k >= 0: # Scan right to left
                if galil_shifted:
                    if k == galil_stop:
                        k = galil_start - 1
                        galil_shifted = False

                if k < 0:   # Galil shifted pass the start of pat, break
                    break

                comp += 1
                char_pat = int(pat[k])
                char_txt = int(txt[i+k])

                if char_pat != char_txt:  # Mismatch

                    """
                    OLD BAD CHAR RULE IS NO LONGER NEEDED FOR BINARY (CAUSE: NEVER USED)
                    if r[k][char_txt] > -1:
                        bad_char_shift = k - r[k][char_txt]
                    else:
                        bad_char_shift = k
                    """
                    bad_char_shift = 0
                    if k == m - 1:
                        #print("chunk check")
                        off, chunk_num = get_rightmost_chunk(txt[i+k-CHUNK_SIZE+1 : i+k+1],k,r_chunks)
                        if chunk_num == -1: # Chunk is not in pat.
                            bad_char_shift = k - 1 # Or k
                        else:
                            new_k = get_new_chunk_k(off,chunk_num)
                            #print(txt[i+k-CHUNK_SIZE+1 : i+k+1],pat[new_k-CHUNK_SIZE+1:new_k+1])
                            bad_char_shift = k - new_k
                            #print(bad_char_shift)

                    #print('Found mismatch at: i = {}, k = {}, bad_char = {}'.format(i,k,bad_char_shift))

                    # Case 1a
                    if gs[k+1] > 0:
                        """
                        Because we are working with binary, say when a character x in pattern mismatches a character y in text, when we shift by using goodsuffix rule, we are finding the matched suffix with a preceding character z, because z != x,
                        z has to be == y -> This is essentially the same as using bad character rule and aligning z and y.
                        Thus we also prefer to use goodsuffix over bad_char to utilize Galil's skips.
                        """
                        gs_shift = m - 1 - gs[k+1]
                        if gs_shift >= bad_char_shift: # If this is the same as bad_char, use gs to utilize Galil's skips
                            #print('m = {}, k = {}, gs[k+1] = {}'.format(m,k,gs[k+1]))
                            #print('shifted gs =',gs_shift)
                            galil_shifted = True
                            galil_stop = gs[k+1]
                            galil_start = gs[k+1] - m + k + 1
                        else:
                            galil_shifted = False
                            #print('shifted bad char =',bad_char_shift)
                        shift = max(1,bad_char_shift,gs_shift)
                        break
                    # Case 1b
                    if gs[k+1] == 0:
                        mp_shift = m - mp[k+1]
                        if mp_shift >= bad_char_shift:
                            galil_shifted = True
                            galil_stop = mp[k+1] - 1
                            galil_start = 0
                            #print('shifted mp =',mp_shift)
                        else:
                            galil_shifted = False
                            #print('shifted bad char =',bad_char_shift)
                        shift = max(1,bad_char_shift,mp_shift)
                        break

                k -= 1

            # No mismatches -> A match
            if shift == 0:
                occur.append(i)
                shift = max(1,m-mp[1])
                #print('Found a match at: {}, shifted {}'.format(i,shift))


            #print('Shifted:',shift)
            shift_count += 1
            i += shift

    #if should:
        #print('r:',r)
        #print('zsuffix:',z_suffix)
        #print('gs:',gs)
        #print('mp:',mp)
    #print('Comps:',comp)
    #print('Shifts:',shift_count)
    #print(len(occur))
    return occur

#print(bm_binary('0011010101111001001101100','010'))

def test_asm():
    """
    Should be 942 matches.
    """
    txt_file = open("txt1.txt",'r')
    pat_file = open("pat1.txt",'r')
    txt = txt_file.read()
    pat = pat_file.read()
    bm_binary(txt,pat)

#test_asm()
#bm_binary('000001000','101110')
#bm_binary('001000100','00101')
#bm_binary('00110101000000001111111101011011010001111001011000000011110000010101011110100001011001100000100','1101000111100101100000')

if __name__ == '__main__':
    txt_filename = sys.argv[1]
    pat_filename = sys.argv[2]

    txt_file = open(txt_filename,'r')
    txt = txt_file.read()
    txt_file.close()

    pat_file = open(pat_filename,'r')
    pat = pat_file.read()
    pat_file.close()

    found = bm_binary(txt,pat)
    print("Number of comparisons:",comp)
    #print(found)
    output = open('output_binary_boyermoore.txt','w')
    for o in found:
        output.write(str(o+1)+'\n')
        #print(txt[o:o+len(pat)],pat)

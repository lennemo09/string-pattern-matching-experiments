# Name: Ha Tri Nhan Luong
# ID: 29644364
# FIT3155 - Assignment 1 Q1.

### PLEASE NOTE: ALL THE COMMENTS AND DOCSTRING IN THIS FILE IS FORMATTED WITH LINE-WRAPPING AT 140 CHARACTERS.
### SOME DOCSTRING WILL NOT BE ALIGNED CORRECTLY IF LINE-WRAP IS BELOW THIS VALUE.

import sys

def upper(char):
    """
    Using character's ASCII value to check if it is in uppercase character (from the SIGMA alphabet).
    O(1) time.
    """
    if char >= 'A' and char <= 'Z':
        return True
    else:
        return False


def lower(char):
    """
    Using character's ASCII value to check if it is in lower character (from the PI alphabet).
    O(1) time.
    """
    if char >= 'a' and char <= 'z':
        return True
    else:
        return False


def same_case(char1,char2):
    """
    Checks if both characters are all lowercase or uppercase.
    O(1) time (only 1-character long comparison).
    Return: 0 if not same case, 1 if both uppercase, 2 if both lowercase.
    """
    if upper(char1) and upper(char2):
        return 1
    if lower(char1) and lower(char2):
        return 2
    else:
        return 0


def get_z_array_pstring(pstr):
    """
    For 1-character pattern, use naive search (not implemented).
    """
    N = len(pstr) # N = m+n. Should be O(1) since Python stores array length at beginning of stack(?) <- From FIT1008, not guaranteed
    assert N > 1
    z = [0]*N   # O(m+n) space
    z[0] = N
    # Comparision of pstr[1:] with prefix
    # Because the prefix is practically the substring str[1:] 1 character prior, we only need to check each character with its previous.
    if N > 2:   # O(m+n)
        for i in range(1,N):
            if pstr[i] == pstr[i-1]:
                z[1] += 1
            else:
                break
    else:   # Handles 2-long patterns
        if pstr[i] == pstr[i-1]:
            z[1] += 1


    # Finished initiating Z[0] (or Z[1] in the lecture slides)
    # Begin using Z-boxes
    r = 0
    l = 0

    if z[1] > 0:
        r = z[1]
        l = 1
    else:
        r = 0
        l = 0

    ### P-STRING COMPARISON HEURISTICS:
    ### If: pat[i] is lower and str[k] is upper and vice versa: break
    ### If: pat[i] is lower and str[k] is lower: if no mapping for pat[i]: mapping table pat[i] = str[k], else check if mapping holds, if not: break.
    ### If: pat[i] is upper and str[k] is upper: compare pat[i] and str[k], if mismatch, break.

    for k in range(2,N):    # O(m+n) time
        # Mapping for parameters (resets every shift). This may take O(1) or O(26) ~> O(1) time depending on how Python manages array allocation.
        # IMPORTANT DISCLAIMER: Because for this question we have a fixed alphabet for both SIGMA and PI and it is relative small (26), therefore our ALPHABET SIZE is CONSTANT -> This is O(1) space. For problem with larger alphabet size (such as the entire UTF-8 character set) we may need another implementation.
        mapping = [None]*26    # 26 characters in alphabet, indexing/hashing by using [ASCII of character - 97]
                            # (because we are only checking lowercase characters so ASCII code minus 97 brings 'a' to 0)

        # Case 1: k > r: Explicit comparisons until mismatch is found
        if k > r:
            for i in range(k,N):
                char_txt = pstr[i]  # A bit misleading name because char only 'txt' when k > m (though that is trivial for our case)
                char_pat = pstr[i-k]    # Should always be in pat because it always mismatches at '$'

                # Different case -> mismatch
                case = same_case(char_txt, char_pat)

                if case == 0:
                    break
                # Both uppercase -> Both token, compare
                elif case == 1:
                    if char_txt == char_pat:
                        z[k] += 1
                    else:
                        break
                # Both lowercase -> Both parameters, check if mapping is one-to-one
                elif case == 2:
                    # Check if parameter has been mapped:
                    idx = ord(char_txt) - 97
                    # This character has not been mapped.
                    # Map it and continue (consider this is a matched character for now)
                    if mapping[idx] is None:
                        mapping[idx] = char_pat
                        z[k] += 1
                    # This character has been mapped, checks if mapping is one-to-one
                    else:
                        # Mapping is one-to-one, consider this character is a match
                        if mapping[idx] == char_pat:
                            z[k] += 1
                        # Mismatching parameter/mapping not one-to-one -> A mismatch
                        else:
                            break
            r = k + z[k] - 1
            l = k

        # Case 2: k <= r
        else:
            # Case 2a:
            if r - k + 1 > z[k - l]:
                z[k] = z[k-l]
            # Case 2b: z[k] must also be >= r - k + 1. Compare characters from str[r+1] with str[r-k+2]
            else:
                # Use count to iterate r instead of having to use q. (q is the mismatch point in lecture slides)
                count = 0

                for i in range(r+1,N):
                    char_txt = pstr[i]
                    char_pat = pstr[i-k]

                    # Different case -> mismatch
                    case = same_case(char_txt, char_pat)
                    if case == 0:
                        break
                    # Both uppercase -> Both token, compare
                    elif case == 1:
                        if char_txt == char_pat:
                            count += 1
                        else:
                            break
                    # Both lowercase -> Both parameters, check if mapping is one-to-one
                    elif case == 2:
                        # Check if parameter has been mapped:
                        idx = ord(char_txt) - 97
                        # This character has not been mapped.
                        # Map it and continue (consider this is a matched character for now)
                        if mapping[idx] is None:
                            mapping[idx] = char_pat
                            count += 1
                        # This character has been mapped, checks if mapping is one-to-one
                        else:
                            # Mapping is one-to-one, consider this character is a match
                            if mapping[idx] == char_pat:
                                count += 1
                            # Mismatching parameter/mapping not one-to-one -> A mismatch
                            else:
                                break

                l = k
                r = r + count
                z[k] = r - k + 1
    return z

def z_search_pstring(txt,pat):
    """
    Exact p-string pattern matching using modified Gusfield's Z-algorithm (pattern has to be at least 2 characters in length).
    For 1-character pattern, use naive search (not implemented).
    """
    pstr = pat + '$' + txt
    occur = []
    z = get_z_array_pstring(pstr)
    #print(z)

    for i in range(len(pat)+1,len(pstr)):
        if z[i] == len(pat):
            occur.append(i - len(pat) - 1)

    # Convert to 1-indexing
    for i in range(len(occur)):
        occur[i] += 1

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

    found = z_search_pstring(txt,pat)
    #print(found)
    output = open('output_parameter_matching.txt','w')
    for o in found:
        output.write(str(o)+'\n')
    #print(found)

#print(z_search_pstring("","aBc"))

def get_z_array(str):
    """
    For 1-character pattern, use naive search (not implemented).
    """
    n = len(str)
    assert n > 1
    z = [0]*n

    # Comparision of str[1:] with prefix
    # Because the prefix is practically the substring str[1:]] 1 character prior, we only need to check each character with its previous.
    for i in range(1,n):
        if str[i] == str[i-1]:
            z[1] += 1
        else:
            break

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
            r = k + z[k] - 1
            l = k
        # Case 2:
        else:
            # Case 2a:
            if z[k-l] < (r - k + 1):
                z[k] = z[k-l]
            # Case 2b: z[k] must also be >= r - k + 1. Compare characters from str[r+1] with str[r-k+2]
            else:
                # Use count to iterate r instead of having to use q. (q is the mismatch point in lecture slides)
                count = 0
                for i in range(r+1,n):
                    if str[i] == str[i-k]:
                        count += 1
                    else:
                        break

                l = k
                r = r + count
                z[k] = r - k + 1
    return z

def z_search(txt,pat):
    """
    Using Z-algorithm to search for pattern (pattern has to be at least 2 characters in length).
    For 1-character pattern, use naive search (not implemented).
    """
    str = pat + '$' + txt
    print(str)
    occur = []
    z = get_z_array(str)
    print(z)

    for i in range(len(pat)+1,len(str)):
        if z[i] == len(pat):
            occur.append(i - len(pat) - 1)
    print(occur)


print(z_search("hello this is a string helloworld hahahello","hello")) # should be 0, 23, 38
print(z_search("aaaaaaa","a"))
print(z_search("babac","ba"))
print(z_search("AaBcBaABCaBaAxBy","aBc"))

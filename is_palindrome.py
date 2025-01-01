#better approach to palindrom complexity O(1)

def is_palindrome(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    s = ''.join(filter(str.isalnum, s)).lower()
    
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
        
    return True
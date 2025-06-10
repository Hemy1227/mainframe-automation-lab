def run_length_encode(s):
    if not s:
        return ""
    
    result = []
    count = 1
    prev_char = s[0]
    
    for char in s[1:]:
        if char == prev_char:
            count += 1
        else:
            result.append(prev_char + str(count))
            prev_char = char
            count = 1
    result.append(prev_char + str(count))  # Add the last group
    
    return ''.join(result)

# Example usage
input_str = "aaabbcddd"
output = run_length_encode(input_str)
print(output)  # Output: a3b2c1d3

import re
from fractions import Fraction




def get_numeric_string_tokens(string, no_minus=False):
    ''' Get the numeric string tokens in a string.
    
    This function uses regular expression to match numeric string tokens in a string.
    The "-?[0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?" pattern matches strings like "25", "-25", "125,000,000", "0.25"
    The "\.[0-9]+" pattern matches numbers like ".25", ".12"
    
    Args:
        string: A string from which we want to find the numeric strings.
        no_minus: A bool that decides whether to detect the minus sign before numbers.
        
    Returns:
        tokens: A list of string containing the targeted numeric string tokens 
    
    Example Usage:
        >>> string1 = "U.S. goods and services trade with China totaled an estimated $710.4 billion in 2017. "
        >>> get_numeric_string_tokens(string1)
        ['710.4', '2017']

        >>> string2 = "David spent .25 billion dollars buying a building and 600,000,000.5 dollars getting himself a new car."
        >>> get_numeric_string_tokens(string2)
        ['.25', '600,000,000.5']

        >>> string3 = "Find the product of 4 and -5?"
        >>> get_numeric_string_tokens(string3)
        ['4', '-5']

        >>> string4 = "The flight number is Airbus A330-300"
        >>> get_numeric_string_tokens(string4, no_minus=True)
        ['330', '300']
        
    References:
        Numbers with Thousand Separators: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch06s11.html

    '''
    if not no_minus:
        tokens = re.findall(r'-?[0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?|\.[0-9]+', string)  
    else:
        tokens = re.findall(r'[0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?|\.[0-9]+', string)  
    return tokens




def to_num(numeric_string):
    '''Convert numeric string to number
    
    Convert a numeric string to a number according to its type, i.e. int, float, fraction.
    
    Args:
        numeric_string: A string which we want to convert. But for reason of flexibility, a int or float input is allowed to pass and will be returned directly.
    
    Returns:
        A int, float or Fraction which is converted from the input string.
    
    Raises: 
        ValueError: If the input isn't a string, int or float, it will raise a ValueError("Invalid  input type!"). 
                            If the input is a string with invalid character, it will raise a ValueError("Invalid numerical string!")
        
    Example Usage:
        >>> s0 = "255"
        >>> to_num(s0)
        255
    
        >>> s1 = "-255,000.0"
        >>> to_num(s1)
        -255000.0
        
        >>> s2 = "87/25"
        >>> to_num(s2)
        Fraction(87, 25)
        
        >>> s3 = "a1b2"
        >>> to_num(s3)
        Traceback (most recent call last):
            ...
        ValueError: Invalid numerical string!
    '''
     
    if isinstance(numeric_string, str):
        # Preprocess - remove the thousands seperators, e.g. "255,000" --> "255000"
        numeric_string = numeric_string.replace(",","")
        
        # Convert strings to nums
        try:
            if "/" in numeric_string:  # Convert to Fractions with automatic reduction
                return Fraction(numeric_string)
            elif "." in numeric_string: # Convert to float
                return float(numeric_string)
            else: # Convert to int
                return  int(numeric_string)
        except ValueError:
                raise ValueError("Invalid numerical string!")

    # If the type isn't a str but an int or float, we still do it a favor and return it directly
    elif isinstance(numeric_string, int) or isinstance(numeric_string, float): 
        return numeric_string
    
    # The situation of an invalid input type
    else: 
        raise ValueError("Invalid input type!")


        
        
        
def get_nums(string):
    ''' Get the numbers from a string.
    
    This function uses regular expression to match numerical string tokens in a string, and convert them to numbers according to their types.
    
    Args:
        string: A string from which we want to find numbers.
        
    Returns:
        nums: A list of ints or floats  or a mixture of them containing the numbers we extract from the input string. 

    Example Usage:
        >>> string1 = "U.S. goods and services trade with China totaled an estimated $710.4 billion in 2017. "
        >>> get_nums(string1)
        [710.4, 2017]

        >>> string2 = "David spent .25 billion dollars buying a building and 600,000,000.5 dollars getting himself a new car."
        >>> get_nums(string2)
        [0.25, 600000000.5]
  
    '''
    
    tokens = get_numeric_string_tokens(string)
    nums = [to_num(t) for t in tokens]
    return nums
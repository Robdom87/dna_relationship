# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        tran_dict = {}  
        # add all consonsants to tran_dict with their respective same letter in upper case and lowercase
        def add_2_dict_con(con_str):
            con_arr = []
            con_arr[:] = con_str
            for con in con_arr:
                tran_dict[con]=con
        add_2_dict_con(CONSONANTS_LOWER)
        add_2_dict_con(CONSONANTS_UPPER)
        # function to add vowels to tran_dict according to vow_perm
        def add_2_dict_vow(vow_str, vow_perm):
            # make base vowel string into arr
            vow_arr = []
            vow_arr[:] = vow_str
            # make permutated vowel string into an arr
            vow_p_arr = []
            vow_p_arr[:]= vow_perm
            # for each vowel in base arr
            for i,vow in enumerate(vow_arr):
                # pull current vowel from permutated vowel array
                perm_vow = vow_p_arr[i]
                # if base vowel array is in upper case, also make perm_vow array into upper case
                if vow.isupper():
                    perm_vow = perm_vow.upper()
                # add key pair for base vowel arr and perm vowel arr
                tran_dict[vow]= perm_vow
        add_2_dict_vow(VOWELS_LOWER, vowels_permutation)
        add_2_dict_vow(VOWELS_UPPER, vowels_permutation)
        
        return tran_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        messageArr = []
        messageArr[:] = self.get_message_text()
        for i, char in enumerate(messageArr):
            if char.isalpha():
                messageArr[i] = transpose_dict[messageArr[i]]
        return "".join(messageArr)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        permut_arr = get_permutations(VOWELS_LOWER)
        # variable to hold max amount of valid words
        max_words = 0
        max_message = ""
        # for each permutation possibility
        for permut in permut_arr:
             #apply use permute to build new tranpose dict
            curr_tran_dict = self.build_transpose_dict(permut)
            curr_message = self.apply_transpose(curr_tran_dict)
            # varaible to hold current amount of valid words
            curr_words = 0
            # break decipered message str into an array of 
            curr_words_arr = curr_message.split(" ")
            # for each word in dec message arr, check if is word
            for word in curr_words_arr:
                #   if so add to variable
                if is_word(self.valid_words, word):
                    curr_words += 1
            #check if total amount of current valid words is more than max
            if curr_words > max_words:
                #   if so subsstitu max amount with new max and save new message
                max_words = curr_words
                max_message = curr_message 
        # return message for message with largest amount of valid words
        return max_message

    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())


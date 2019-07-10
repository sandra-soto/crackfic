import nltk
from random import randint
from collections import defaultdict
from math import floor


#to see documentation of part-of-speech tags, run commented code below
##nltk.download('tagsets')
##nltk.help.upenn_tagset('RB') #RB is a pos tag
## alternatively, visit https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/

example_psg = """Keith opened his eyes slowly, blinking a couple times as he tried to adjust to the bright light above his head. He wasn’t fully awake until he heard a groan a few feet away.
Keith pushed himself up from the ground, shaking his head a couple times for good measure and looked around.
The other paladins, and Allura and Coran, were sprawled out across the ground around him.
Lance had landed on top of Hunk, his head half resting on the other boy’s shoulder. Pidge had fallen onto her side, and she almost looked like she was just sleeping.
Coran and Allura had fallen next to each other, and one of Coran’s hands was in Allura’s hair. Shiro had his head resting on Allura’s leg.
Keith had to stare out over the group for a solid 10 seconds just wondering if this was real life. Unfortunately, it was.
He sighed and staggered to his feet. After all, this wasn’t the weirdest thing that ever happened to him.
He walked over to Lance and Hunk first, lightly tapping Hunk’s cheek. “Hunk? Can you please get up?”
Hunk wrinkled his nose and snored louder in response. Keith rolled his eyes and focused on waking Lance."""


# names and descriptions of part-of-speech tags used
POS = {"CD": "cardinal digit (ex: three, 33)", "JJ": "adjective (ex: big, tall)", "JJR": "comparative adjective (ex: bigger, smaller, taller)",
"JJS": "superlative adjective (ex: greatest, reddest, dumbest)", "NN": "noun (ex: desk, nose, dirt)", "NNS": """plural noun (ex: bottles, \
eyeballs, birds)""", "RB": "adverb (ex: stealthily, slowly, quickly)", "RBR": "comparative adverb (ex: harder, better, faster, stronger)",
"RBS": "superlative adverb (ex: quickest, fastest, best)", "VB": "verb, base form (ex: take, sing, scream)", "VBD": "verb, past tense\
(ex: poured, killed, broke)", "VBG": "verb, gerund/present participle (ex: sinning, chanting, racing)", "VBN": "verb, past participle\
(ex: broken, taken, spoken)", "VBP": "verb, singular present tense (ex: take, burn)", "VBZ": "verb, 3rd person sing. present (ex: takes\
 shouts, throws)"}

# part-of-speech tags to be excluded
excluded_pos = [':', '.','.' ',', 'TO', 'IN', 'CC', 'DT', 'EX', 'LS', 'MD', 'PRP', 'PRP$', 'RP', 'WDT', 'WP', 'WP$', 'WRB', 'NNP', 'NNPS']

# describes how many words will be changed for a given text length
num_of_changes = {100:6, 200: 7, 300: 9, 400: 11, 500: 13, 600: 14, 700: 16, 800: 18, 900:19, 1000:20}

# tokens we don't want -- tradeoff for using nltk tokenizer
unwanted_tokens = ['"', "'", ",", "'t", "t", "?", '“', '”', '’', 's']


def num_of_repls(text_len:int)-> int:
  #utility function for cut_pos() below
    """determines the number of words to be replaced on the text"""
    mod_remainder, div_quotient = text_len%100, text_len//100
    if mod_remainder >= 50: # if larger than 50, round up to next hundred
      div_quotient += 1
    return num_of_changes[div_quotient * 100]

def nltk_pos_tag(tokens:list)-> '{(part_of_speech, word):[indices of occurences]}':
  #used in process() below
  """given a tokenized text, returns a data structure of words, their part of speech tags, and a list of occurences"""
  pos_dict = defaultdict(list)
  for num, (word, pos) in enumerate(nltk.pos_tag(tokens)):
      pos_dict[(pos,word)].append(num)
  return pos_dict
          
def process(text)-> '{(part_of_speech, word):[indices of occurences]}, [tokens_list]':
  #important!, must be run -- not a utility function
  """returns a pos-tagged data structure of tokens and a list of the text's tokens"""
  tokens = nltk.tokenize.casual_tokenize(text)
  return nltk_pos_tag(tokens), tokens

def cut_pos(pos_dict, text_len:int) -> "[((part_of_speech, word), [occurences])], int":
  #important!, must be run -- not a utility function
  """removes unnecessary keys from pos_dict and returns only the most frequent tokens in a list data structure"""
  num_changes = num_of_repls(200) # hardcoded story length, should be changed later
  for i in set(pos_dict.keys()):
    if (i[0] in excluded_pos or i[1] in unwanted_tokens) == True:
      del pos_dict[(i)]
  return sorted(pos_dict.items(), key=lambda x:len(x[1]), reverse = True)[:num_changes], num_changes

def repl_all(occ_list, tokens, new_word)-> None:
  # utility function for repl_tokens() below
  """replaces all occurences of a word in the tokens list"""
  for occurence in occ_list:
    tokens[occurence] = new_word
    
def repl_tokens(pos_list, tokens) -> str:
  #important!, must be run -- not a utility function
  """prompts the user to replace words and returns the new text"""
  for (pos, word), occ_list in pos_list:
    new_word = input(f"gimme a {pos} - a {POS[pos]} -> ")
    repl_all(occ_list, tokens, new_word)
  return tokens


def madlib_out(text:str):
    pos_dict,tokens = process(text)
    pos_list, num_changes = cut_pos(pos_dict, 200)
    message = []
    for (pos, word), occ_list in pos_list:
        message.append(f"Enter a {POS[pos]}")
    return message, num_changes, pos_list, tokens

def madlib_done(new_list, num_changes, pos_list, tokens):
    for i in range(0, num_changes):
        (pos, word), occ_list = pos_list[i]
        new_word = new_list[i]
        repl_all(occ_list, tokens, new_word)
    return " ".join(tokens)


if __name__ == '__main__':
  pos_dict,tokens = process(example_psg)
  pos_list, num_changes = cut_pos(pos_dict, 200)
##  tokens = repl_tokens(pos_list, tokens)
  print(" ".join(tokens))

'''
for local madlibs

def repl_tokens(pos_list, tokens) -> str:
  #important!, must be run -- not a utility function
  """prompts the user to replace words and returns the new text"""
  for (pos, word), occ_list in pos_list:
    new_word = input(f"gimme a {pos} - a {POS[pos]} -> ")
    repl_all(occ_list, tokens, new_word)
  return " ".join(tokens)
'''

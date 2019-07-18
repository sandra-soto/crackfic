import nltk
from random import randint
from collections import defaultdict
from math import floor
## needs nltk.download("punkt") and nltk.download("averaged_perceptron_tagger")


#to see documentation of part-of-speech tags, run commented code below
##nltk.download('tagsets')
##nltk.help.upenn_tagset('RB') #RB is a pos tag
## alternatively, visit https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/



# part-of-speech tags used and their names in plain english
POS = {'CD': 'cardinal digit ', 'JJ': 'adjective ', 'JJR': 'comparative adjective ', 'JJS': 'superlative adjective ',
       'NN': 'noun ', 'NNS': 'plural noun ', 'RB': 'adverb ', 'RBR': 'comparative adverb ', 'RBS': 'superlative adverb ',
       'VB': 'verb, base form ', 'VBD': 'verb, past tense','VBG': 'verb, gerund/present participle ',
       'VBN': 'verb, past participle', 'VBP': 'verb, singular present tense ', 'VBZ': 'verb, 3rd person sing. present '}

# part-of-speech tags wiht examples
pos_ex = {'cardinal digit ': '(ex: three, 33)', 'adjective ': '(ex: big, tall)', 'comparative adjective ': '(ex: bigger, smaller, taller)',
 'superlative adjective ': '(ex: greatest, reddest, dumbest)', 'noun ': '(ex: desk, nose, dirt)',
 'plural noun ': '(ex: bottles, eyeballs, birds)', 'adverb ': '(ex: stealthily, slowly, quickly)',
 'comparative adverb ': '(ex: harder, better, faster, stronger)', 'superlative adverb ': '(ex: quickest, fastest, best)',
 'verb, base form ': '(ex: take, sing, scream)', 'verb, past tense': '(ex: poured, killed, broke)',
 'verb, gerund/present participle ': '(ex: sinning, chanting, racing)', 'verb, past participle': '(ex: broken, taken, spoken)',
 'verb, singular present tense ': '(ex: take, burn)', 'verb, 3rd person sing. present ': '(ex: takes shouts, throws)'}

# part-of-speech tags to be excluded
excluded_pos = [':', '.','.' ',', 'TO', 'IN', 'CC', 'DT', 'EX', 'LS', 'MD', 'PRP', 'PRP$', 'RP', 'WDT', 'WP', 'WP$', 'WRB', 'NNP', 'NNPS']

# describes how many words will be changed for a given text length
num_of_changes = {100:6, 200: 7, 300: 9, 400: 11, 500: 13, 600: 14, 700: 16, 800: 18, 900:19, 1000:20}

# tokens we don't want -- tradeoff for using nltk tokenizer
unwanted_tokens = ['"', "'", ",", "'t", "t", "?", '“', '”', '’', 's', 'was', 'said', 'is', 'says', 'were']


def num_of_repls(text_len:int)-> int:
  #utility function for cut_pos() below
    """determines the number of words to be replaced on the text"""
    mod_remainder, div_quotient = text_len%100, text_len//100
    if mod_remainder >= 50: # if larger than 50, round up to next hundred
      div_quotient += 1
    return abs(num_of_changes[div_quotient * 100])

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
  num_changes = num_of_repls(text_len)
  for i in set(pos_dict.keys()):
    if (i[0] in excluded_pos or i[1] in unwanted_tokens or (i[0] == 'VBD' and i[1] == 'had')) == True:
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
    """returns the words needed to be replaced and their POS"""
    pos_dict,tokens = process(text)
    pos_list, num_changes = cut_pos(pos_dict, len(tokens)-50)
    message = []
    for (pos, word), occ_list in pos_list:
        message.append(f"{POS[pos]}")
    return message, num_changes, pos_list, tokens

def madlib_done(new_list, num_changes, pos_list, tokens):
    """returns newly created madlib"""
    for i in range(0, num_changes):
        (pos, word), occ_list = pos_list[i]
        new_word = new_list[i]
        repl_all(occ_list, tokens, new_word)
        
    def formatter(tokens, remove):
        new_tokens = []
        for index, token in enumerate(tokens):
            # dealing with quotes“ open,,,, ” close
            if index == len(tokens)-1:
                new_tokens.append(token)
            elif token == "”":
                new_tokens.append(token + " ")
            elif token == "," and tokens[index+1] == "”":
                new_tokens.append(token)
            elif token == ",":
                new_tokens.append(token + " ")
            elif token not in remove and tokens[index+1] in remove:
                new_tokens.append(token)
            elif token in ["(", "“"]:
                new_tokens.append(token)
            else:
                new_tokens.append(token + " ")     
                
        return "".join(new_tokens)
    
    return formatter(tokens, [".", "?", ",", '"', "'",',', "!", "-", "⁠—", ")"])

##
##if __name__ == '__main__':
##  pos_dict,tokens = process(example_psg)
##  pos_list, num_changes = cut_pos(pos_dict, 200)
####  tokens = repl_tokens(pos_list, tokens)
##  print(" ".join(tokens))

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

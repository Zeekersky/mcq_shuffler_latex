import re
import random
import itertools
import os
import sys
import string

# Read Latex code from a file
def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

#_______________________________________________________________________________________

input_latex_path = 'source'
input_latex_name = 'quiz2.tex'
output_latex_path = 'modified'

#_______________________________________________________________________________________

num_mcq = int(sys.argv[1])
num_permutations = int(sys.argv[2])

latex_code = read(os.path.join(input_latex_path, input_latex_name))

pattern = re.compile(r'\\begin\{enumerate\}', re.IGNORECASE)
matches = [match.start() for match in pattern.finditer(latex_code)]
pattern_end = re.compile(r'\\end\{enumerate\}', re.IGNORECASE)
matches_end = [match_end.start() for match_end in pattern_end.finditer(latex_code)]
questions = []

if len(matches) >= 2:
    split_index = matches[1]
    split_index_end = matches_end[1]
    part1 = latex_code[:split_index]
    part2 = latex_code[split_index:split_index_end]
    part3 = latex_code[split_index_end:]

    pattern_items = re.compile(r'\\item(.*?)(?=\\end\{enumerate\*\})', re.DOTALL)
    items = re.findall(pattern_items, part2)
    remaining_part = part2.split(r'\end{enumerate*}')[-1]

    # num_mcq = int(input('Enter the number of MCQs to generate: '))

    for item in items[:-1]:
        questions.append('\\item' + item + r'\end{enumerate*}')
    questions.append('\\item' + items[-1] + r'\end{enumerate*}')

    questions_need_shuffle = []
    questions_not_need_shuffle = []

    for i in range(num_mcq):
        questions_need_shuffle.append(questions[i])
    for i in range(num_mcq, len(questions)):
        questions_not_need_shuffle.append(questions[i])

    all_permutations = list(itertools.permutations(questions_need_shuffle))
    selected_permutations = random.sample(all_permutations, num_permutations)
    set_number = 0

    for i, mcq_questions in enumerate(selected_permutations):

        set_number += 1

        questions_choice_shuffle = []
        for question in mcq_questions:
            pattern1 = re.compile(r'\\begin{enumerate\*}', re.IGNORECASE)
            matches1 = [match.start() for match in pattern1.finditer(question)]
            split_index1 = matches1[0]
            question_part1 = question[:split_index1]
            question_part2 = question[split_index1:]
            
            pattern_choices = re.compile(r'\\item(.*?)(?=\\item)', re.DOTALL)
            choices = re.findall(pattern_choices, question_part2)

            last_part = question_part2.split(r'\item')[-1]
            last_choice = last_part.split(r'\end{enumerate*}')[0]
            choices.append(last_choice)
            choices_with_item = []
            for choice in choices:
                choice = r'\item ' + choice
                choices_with_item.append(choice)
        
            random.shuffle(choices_with_item)
            question = question_part1 + '\n' + r'\begin{enumerate*}' + '\n'.join(choices_with_item) + '\n' + r'\end{enumerate*}' + '\n'
            questions_choice_shuffle.append(question)

        shuffled_questions = '\n\n'.join(questions_choice_shuffle)
        reassembled_latex = part1 + '\n' + r'\begin{enumerate}' + shuffled_questions + '\n' + '\n'.join(questions_not_need_shuffle) + '\n' + remaining_part + part3

        pattern_set = re.compile(r'footnote{(.*?)}', re.DOTALL)
        set_found = re.findall(pattern_set, reassembled_latex)
        random_characters = [random.choice(string.ascii_letters) for _ in range(len(set_found[0])-1)]
        if set_found:
            reassembled_latex = re.sub(pattern_set, r'footnote{' + str(set_number) + ''.join(random_characters) + '}' , reassembled_latex, count=1)

        output_file = f'shuffled_quiz_{i + 1}.tex'
        with open(os.path.join(output_latex_path, output_file), 'w', encoding='utf-8') as output_file:
            output_file.write(reassembled_latex)
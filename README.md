LaTeX MCQ Shuffler

Overview:
-----------
The LaTeX MCQ Shuffler is a Python script designed to shuffle choices in multiple-choice questions within a LaTeX document. It takes a LaTeX file containing questions and choices, shuffles the choices, and generates multiple sets of shuffled quizzes.

Usage:
-----------
1. Clone the Repository:

   git clone [https://github.com/your-username/latex-quiz-shuffler.git](https://github.com/Zeekersky/mcq_shuffler_latex.git)
   cd mcq_shuffler_latex

2. Install Dependencies:

   The script uses Python. Make sure you have Python installed on your machine.

3. Run the Script:

   python randomized_mcq.py 5 2

   where 5 is the number of MCQ question and 2 is the number of different set you want to make.

4. Output:

   The shuffled quizzes will be generated in the 'modified' directory.

Project Structure:
-------------------
- source: Contains the original LaTeX files with questions.
- modified: Stores the output shuffled quizzes.

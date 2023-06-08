:: Random mutation and crossovers
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random random              0.4 20 20

:: Single mutations with random crossovers
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random add_packs           0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random inverse_packages    0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random cut_out_packs       0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random inverse_permutation 0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random shift_block         0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 random shuffle_block       0.4 20 20

:: Single crossovers with random mutations
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 choice_from_one_order_from_other random 0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 extract_and_random_pick          random 0.4 20 20
py tester.py test_input_7.txt 3000 1000 60 7.95 0.7 0.05 halve_and_swap                   random 0.4 20 20
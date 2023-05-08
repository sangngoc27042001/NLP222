from utils import *
import glob
import os




queries = open('Input/querie_test.txt', 'r',  encoding="utf8").read()
queries = queries.split('\n')
queries = [normalize_sentence(s) for s in queries]

db = open('Input/database.txt', 'r',  encoding="utf8").read()
db = [a.strip().replace('(','').replace(')','').split(' ') for a in db.split('\n')]

i = 1


files = glob.glob('Output/*')
for f in files:
    os.remove(f)

for query in queries:
    idx_POS_regex_list = get_idx_POS_regex_list(query)
    relations = parse_dependency(idx_POS_regex_list)
    gramatical_relations = get_grammatical_relations(relations)
    logical_form_res = get_logical_form(gramatical_relations, relations)      
    procedural_sematic_res = get_procedural_sematic(logical_form_res)
    answers_dict = retrieve_database(procedural_sematic_res, db) 
    res = f"""Query: {query}
    
**Dependency Parsing:
{draw_relation(relations)}

**Gramatical Relations:
{draw_grammatical_relations(gramatical_relations)}

**Logical Form:
{draw_logical_form(logical_form_res)}

**Procedural Sematic:
{draw_procedural_sematic(procedural_sematic_res)}

**Answer:
{draw_answer(answers_dict)}"""
    file = open("Output"+"/output_query_{:4d}".format(i)+'.txt', 'w', encoding="utf8")
    file.write(res)
    # print(draw_relation(relations))
    # print(draw_grammatical_relations(gramatical_relations))
    # print(draw_logical_form(logical_form_res))
    # print(draw_procedural_sematic(procedural_sematic_res))
    # print(draw_answer(answers_dict))
    i+=1

print(f'Successful, {i-1} output files have been saved in Output/')
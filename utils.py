from unidecode import unidecode
import re
import re
from flightDict import flightDict

def normalize_sentence(s):
    s = s.replace('TP.', 'thành phố ').replace('Tp.', 'thành phố ').strip().lower()
    return s

def get_idx_POS_regex_list(s):
    idx_POS_regex_list = []
    normalized_s = unidecode(s)
    for x in flightDict:
        idx_POS_regex_list += [(e.start(), e.end(), x['POS'], e.group(), s[e.start():e.end()]) for e in re.finditer(x['regex'], normalized_s)]
    idx_POS_regex_list.sort()
    delete_list=[]
    for i in idx_POS_regex_list:
        for j in idx_POS_regex_list:
            if (i is not j) and (i[1] > j[0]) and (i[0] < j[1]):
                if i[1] - i[0] < j[1] - j[0]:
                    # idx_POS_regex_list.pop(idx_POS_regex_list.index(i))
                    delete_list.append(i)
                else:
                    # idx_POS_regex_list.pop(idx_POS_regex_list.index(j))
                    delete_list.append(j)
    for e in delete_list:
        try:
            idx_POS_regex_list.pop(idx_POS_regex_list.index(e))
        except:
            pass
    return idx_POS_regex_list

def parse_dependency(idx_POS_regex_list):
    stack = ['ROOT']
    input_buffer = idx_POS_regex_list.copy()
    relations = []
    def leftArc(r):
        relations.append((r, input_buffer[0], stack[-1]))
        stack.pop(-1)
    def rightArc(r):
        relations.append((r, stack[-1], input_buffer[0]))
        stack.append(input_buffer.pop(0))
    def shift():
        stack.append(input_buffer.pop(0))
    def reduce():
        stack.pop(-1)

    for item in [x for x in input_buffer if x[2] in ['YES-WH', 'NO-WH']]:
        input_buffer.pop(input_buffer.index(item))

    while len(input_buffer) != 0:
        if stack[-1] == 'ROOT':
            if input_buffer[0][2] in [['FLIGHT_END-V', 'TO-P'], 'FLIGHT-V', 'FLIGHT_END-V', 'FLIGHT_BEGIN-V', 'LAST-P']:
                if 'root' not in [x[0] for x in relations]:
                    rightArc('root')
                    continue
        if stack[-1][2] in ['FLIGHT-N', 'FLIGHT-NAME']:
            if input_buffer[0][2] == 'QDET':
                rightArc('qdet')
                continue
            if input_buffer[0][2] in [['FLIGHT_END-V', 'TO-P'], 'FLIGHT-V', 'FLIGHT_END-V', 'FLIGHT_BEGIN-V']:
                if stack[1][2] == 'TIME-N':
                    rightArc('acl')
                    continue
                leftArc('nsubj')
                continue
            if stack[-1][3] == 'ma hieu' and input_buffer[0][3] == 'may bay':
                leftArc('nmod')
                continue
            if input_buffer[0][2] == 'FLIGHT-NAME':
                leftArc('nmod')
                continue
            if input_buffer[0][2] == 'BRAND-NAME':
                rightArc('aposs')
                continue
            if stack[1][2] == 'TIME-N':
                reduce()
                continue


        if stack[-1][2] == 'QDET':
            if stack[-1][3] == 'hay cho biet':
                if input_buffer[0][2] in ['FLIGHT-N']:
                    leftArc('qdet')
                    continue
            if input_buffer[0][2] in ['HOUR-N']:
                leftArc('qdet')
                continue
            reduce()
            continue
        if stack[-1][2] in [['FLIGHT_END-V', 'TO-P']]:
            if input_buffer[0][2] in ['CITY-NAME', 'CITY-N']:
                if 'root' in [x[0] for x in relations]:
                    if [x for x in relations if x[0] == 'root'][0][2][3] != 'den':
                        if input_buffer[0][2] == 'CITY-N' and input_buffer[1][2] == 'CITY-NAME':
                            shift()
                            continue
                        leftArc('case')
                        continue
                    if input_buffer[0][2] == 'CITY-N' and input_buffer[1][2] == 'CITY-NAME':
                        shift()
                        continue
                    rightArc('obl')
                    continue
                elif stack[1][2] == 'TIME-N':
                    leftArc('case')
                    continue
            if input_buffer[0][2] in ['FLIGHT_TIME-N']:
                rightArc('obl')
                continue
            if input_buffer[0][2] in ['PUNC']:
                rightArc('punc')
                continue
        if stack[-1][2] in ['FLIGHT-V', 'FLIGHT_END-V', 'FLIGHT_BEGIN-V']:
            if input_buffer[0][2] in ['CITY-NAME', 'HOUR-N']:
                rightArc('obl')
                continue
            if input_buffer[0][2] == 'CITY-N' and input_buffer[1][2] != 'CITY-NAME':
                rightArc('obl')
                continue
            if input_buffer[0][2] in ['PUNC']:
                rightArc('punc')
                continue
            if input_buffer[0][2] in ['LAST-P']:
                if stack[1][2] == 'TIME-N':
                    reduce()
                    continue
                rightArc('advmod')
                continue
        if stack[-1][2] in ['CITY-N']:
            if input_buffer[0][2] in ['CITY-NAME']:
                leftArc('nmod')
                continue
            if input_buffer[0][2] in ['QDET']:
                rightArc('qdet')
                continue

        if stack[-1][2] in ['CITY-NAME']:
            reduce()
            continue
        if stack[-1][2] in ['AT-P']:
            if input_buffer[0][2] in ['FLIGHT_TIME-N', 'HOUR-N']:
                leftArc('case')
                continue
        
        if stack[-1][2] in ['FROM-P', 'TO-P', 'IN-P']:
            if input_buffer[0][2] in ['CITY-NAME']:
                leftArc('case')
                continue
        if stack[-1][2] in ['FLIGHT_TIME_DURATION-N']:
            if input_buffer[0][2] in ['HOUR-N']:
                leftArc('nummod')
                continue
        if stack[-1][2] in ['LAST-P']:
            if input_buffer[0][2] in ['HOUR-N']:
                rightArc('dobj')
                continue
            if input_buffer[0][2] in ['PUNC']:
                if [x for x in relations if x[0] == 'root'][0][2][3] == 'mat':
                    rightArc('punc')
                    continue

        if stack[-1][2] in ['PLURAL-DET']:
            if input_buffer[0][2] in ['FLIGHT-N', 'CITY-N']:
                leftArc('det')
                continue
        if stack[-1][2] in ['TIME-N']:
            if input_buffer[0][2] in ['FLIGHT-NAME']:
                rightArc('nmod')
                continue
            if input_buffer[0][2] in ['LAST-P']:
                leftArc('nsubj')
                continue
        
        if stack[-1][2] in ['BRAND-N']:
            if input_buffer[0][2] == 'BRAND-NAME':
                leftArc('nmod')
                continue
        
        if stack[-1][2] in ['POSS-P']:
            if input_buffer[0][2] == 'BRAND-NAME':
                leftArc('case')
                continue
        if stack[-1][2] in ['BRAND-NAME']:
            reduce()
            continue

        if input_buffer[0][2] == 'PUNC':
            if stack[-1][2] not in [['FLIGHT_END-V', 'TO-P'], 'FLIGHT-V']:
                reduce()
                continue
        shift()
    return relations

def draw_relation(relations):
    res = ''
    for r in relations:
        res += f'{r[0]}: {r[1] if (r[1]=="ROOT") else r[1][4]} -> {r[2][4]}\n'
    return res

def get_grammatical_relations(relations):
    gramatical_relations = []

    def add_gramatical_relations(var, gramma, word):
        gramatical_relations.append((var, gramma, word))

    root = [x for x in relations if x[0] == 'root'][0]
    add_gramatical_relations('s1', 'PRED', root[2])
    nsubj = [x for x in relations if x[0] == 'nsubj'][0]
    add_gramatical_relations('s1', 'LSUBJ', nsubj[2])
    dobj = [x for x in relations if x[0] == 'dobj']
    if len(dobj) != 0:
        add_gramatical_relations('s1', 'LOBJ', dobj[0][2])

    obls = [x for x in relations if x[0] == 'obl']
    for obl in obls:
        if obl[1][2] in [['FLIGHT_END-V', 'TO-P'], 'FLIGHT_END-V']:
            if obl[2][2] in ['CITY-NAME']:
                add_gramatical_relations('s1', 'TO', obl[2])
            elif obl[2][2] in ['FLIGHT_TIME-N']:
                add_gramatical_relations('s1', 'AT-TIME', obl[2])
            
    
    cases = [x for x in relations if x[0] == 'case']
    for case in cases:
        if case[1][2] in ['CITY-NAME', 'CITY-N']:
            if case[2][2] in ['FROM-P']:
                add_gramatical_relations('s1', 'FROM', case[1])
            if case[2][2] in [['FLIGHT_END-V', 'TO-P']]:
                add_gramatical_relations('s1', 'TO', case[1])
        if case[1][2] in ['HOUR-N']:
            if case[2][2] in ['AT-P']:
                add_gramatical_relations('s1', 'AT-TIME', case[1])
    
    advmods = [x for x in relations if x[0] == 'advmod']
    for advmod in advmods:
        if advmod[2][3] == 'mat':
            unit = [x for x in relations if x[0] == 'dobj' and x[1][3] == 'mat'][0][2][3]
            num = [x for x in relations if x[0] == 'nummod' and x[1][3] == unit][0][2][3]
            unit = 'HR' if unit=='gio' else unit
            add_gramatical_relations('s1', 'TAKE', f'{num}:00{unit}')
    

    acls =   [x for x in relations if x[0] == 'acl']      
    for acl in acls:
        add_gramatical_relations('s2', 'LSUBJ', acl[1])
        add_gramatical_relations('s2', 'PRED', acl[2])
        stack_add = []
        stack_delete = []
        for ele in gramatical_relations:
            if ele[1] not in ['PRED', 'LSUBJ', 'LOBJ']:
                stack_add.append(('s2', ele[1], ele[2]))
                stack_delete.append(ele)
        [gramatical_relations.pop(gramatical_relations.index(ele)) for ele in stack_delete]
        gramatical_relations += stack_add
    
    return gramatical_relations

def draw_grammatical_relations(gramatical_relations):
    res = ""
    for i in gramatical_relations:
        res += f'({i[0]} {i[1]} "{i[2][4]}")\n'
    return res

def get_logical_form(gramatical_relations, relations):
    source = []
    dest = []
    run_time = []
    arrive = []
    depart = []
        
    lsubj = [x for x in gramatical_relations if x[1] == 'LSUBJ'][0]
    try: 
        lsubj = [x for x in gramatical_relations if x[1] == 'LSUBJ'][1]
    except:
        pass
    if lsubj[2][2] == 'FLIGHT-NAME':
        flight = ['FLIGHT', lsubj[2][3]]
    else:
        flight = ['FLIGHT', 'f1']
    
    pred = [x for x in gramatical_relations if x[1] == 'PRED'][0]
    if pred[2][2] == 'LAST-P':
        run_time = ['RUN-TIME', 'r1', 't3']
    


    if 'AT-TIME' in [x[1] for x in gramatical_relations]:
        name_time = [x[2][4] for x in gramatical_relations if x[1] == 'AT-TIME'][0]
        pred = [x for x in gramatical_relations if x[1] == 'PRED'][0]
        if pred[2][2] in [['FLIGHT_END-V', 'TO-P']]:
            arrive = ['ARRIVE', 'a1', f'(NAME t2 "{name_time}")']
        elif pred[2][2] == 'FLIGHT_BEGIN-V':
            depart = ['DEPART', 'd1', f'(NAME t1 "{name_time}")']
    
    if 'TO' in [x[1] for x in gramatical_relations]:
        name_to = [x[2][4] for x in gramatical_relations if x[1] == 'TO'][0]
        dest = ['DEST', flight[1], f'(NAME c2 "{name_to}")']
    
    if 'FROM' in [x[1] for x in gramatical_relations]:
        name_source = [x[2][4] for x in gramatical_relations if x[1] == 'FROM'][0]
        source = ['SOURCE', flight[1], f'(NAME c1 "{name_source}")']
    
    if 'TAKE' in [x[1] for x in gramatical_relations]:
        name_hour = [x[2] for x in gramatical_relations if x[1] == 'TAKE'][0]
        run_time = ['RUN-TIME', 'r1', f'(NAME t3 "{name_hour}")']

    #what element the question ask?
    vars_question = []
    try:
        qdets = [x for x in relations if x[0] == 'qdet']
        for qdet in qdets:
            if qdet[1][2] == 'FLIGHT-N':
                vars_question.append(flight[1])
            elif qdet[1][2] == 'HOUR-N':
                l = [depart, arrive, run_time]
                vars_question.append(f't{1+l.index([x for x in l if x!= []][0])}')
            elif qdet[1][2] == 'CITY-N':
                eles = [x for x in gramatical_relations if x[1] == 'FROM']+[x for x in gramatical_relations if x[1] == 'TO']
                for ele in eles:
                    if ele[2][2] != 'CITY-NAME' and ele[1] == 'TO':
                        vars_question.append('c2')
                    elif ele[2][2] != 'CITY-NAME' and ele[1] == 'FROM':
                        vars_question.append('c1')
    except:
        vars_question.append(flight[1])

    if len(qdets) == 0: # yes no question
        flight[1] = 'f1'
        if source != []:
            source[1] = 'f1'
        if dest != []:
            dest[1] = 'f1'
        vars_question.append(flight[1])
    
    return [vars_question, flight, source, dest, arrive, depart, run_time]

def draw_logical_form(args):
    def list2string(l):
        if len(l)==0:
            return ''
        s = ''
        for e in l:
            s += e + ' '
        s = s.strip()
        return f'({s})'
    
    def list2string_vars_question(l):
        s = ''
        for e in l:
            s += e + ', '
        return s[:-2]
    vars_question, flight, source, dest, arrive, depart, run_time = args
    return f'WH {list2string_vars_question(vars_question)}: (&{list2string(flight)}{list2string(source)}{list2string(dest)}){list2string(arrive)}{list2string(depart)}{list2string(run_time)}\n'
        
def get_procedural_sematic(logical_form_args):
    vars_question, flight, source, dest, arrive, depart, run_time = logical_form_args

    Flight = []
    Atime = []
    Dtime = []
    Runtime = []

    pattern = re.compile('(vn|vj)\d')
    Flight = ['FLIGHT', flight[1].upper() if pattern.match(flight[1]) else '?f1']

    #handle Dtime
    city1 = '?c1'
    time1 = '?t1'
    if len(source) != 0:
        name_city = source[2].split('"')[1]
        cities_vietnam = ['hồ chí minh', 'huế', 'hà nội', 'đà nẵng', 'hải phòng', 'khánh hòa']
        city_codes = ['HCMC', 'HUE', 'HN', 'ĐN', 'HP', 'KH']
        if name_city in cities_vietnam:
            city1 = city_codes[cities_vietnam.index(name_city)]
    if len(depart) != 0:
        name_hour = depart[2].split('"')[1].upper()
        pattern = re.compile("\d+:\d+HR")
        if pattern.match(name_hour):
            time1 = name_hour
    Dtime = ['DTIME', Flight[1], city1, time1]    
    
    #handle Atime
    city2 = '?c2'
    time2 = '?t2'
    if len(dest) != 0:
        name_city = dest[2].split('"')[1]
        cities_vietnam = ['hồ chí minh', 'huế', 'hà nội', 'đà nẵng', 'hải phòng', 'khánh hòa']
        city_codes = ['HCMC', 'HUE', 'HN', 'ĐN', 'HP', 'KH']
        if name_city in cities_vietnam:
            city2 = city_codes[cities_vietnam.index(name_city)]
    if len(arrive) != 0:
        name_hour = arrive[2].split('"')[1].upper()
        pattern = re.compile("\d+:\d+HR")
        if pattern.match(name_hour):
            time2 = name_hour
    Atime = ['ATIME', Flight[1], city2, time2]

    time3 = '?t3'
    if len(run_time) != 0:
        name_hour = run_time[2] if run_time[2]=='t3' else run_time[2].split('"')[1].upper()
        pattern = re.compile("\d+:\d+HR")
        if pattern.match(name_hour):
            time3 = name_hour
    Runtime = ['RUN-TIME', Flight[1], city1, city2, time3]

    vars_question = [f'?{x}' for x in vars_question]

    
    return [vars_question, Flight, Atime, Dtime, Runtime]

def draw_procedural_sematic(procedural_sematic_res):
    def list2string(l, f=0):
        if all(x[0]=='?' for x in l[1:]) and f == 0:
            return ''
        if f == 2:
            if not all(x[0]!='?' for x in l[2:-1]):
                return ''
        s = ''
        for e in l:
            s += e + ' '
        s = s.strip()
        return f'({s})'
    
    def list2string_vars_question(l):
        s = ''
        for e in l:
            s += e + ', '
        return s[:-2]
    vars_question, Flight, Atime, Dtime, Runtime = procedural_sematic_res
    res = f'(PRINT-ALL {list2string_vars_question(vars_question)} {list2string(Flight, 1)} {list2string(Dtime)} {list2string(Atime)} {list2string(Runtime,2)})\n'
    res = f"{re.sub(' +', ' ',res).strip()}\n"
    return res

def retrieve_database(procedural_sematic_res, db):
    vars_question, Flight, Atime, Dtime, Runtime = procedural_sematic_res

    def no_consts(cond, is_runtime = 0):
        a = len ([x for x in cond if x[0]=='?'])
        return 4 - a if is_runtime else 3 - a
    
    def match(cond_db, cond_query):
        if len(cond_db) != len(cond_query):
            return False
        for idx in range(len(cond_db)):
            if cond_query[idx][0] !='?':
                if cond_query[idx] != cond_db[idx]:
                    return False
        return True
    
    num_of_const = [no_consts(Dtime), no_consts(Atime), no_consts(Runtime, 1)]

    idx_handle = num_of_const.index(max(num_of_const))
    matches=[]

    if idx_handle == 0: #handle DTime
        matches = [x for x in db if match(x, Dtime)]
    if idx_handle == 1: #handle ATime
        matches = [x for x in db if match(x, Atime)]
    if idx_handle == 2: #handle RumTime
        matches = [x for x in db if match(x, Runtime)]

    #handle vars_question
    answers_dict = {}
    for var in vars_question:
        answer = set()
        if var == '?f1':
            for a in [x[1] for x in matches]:
                answer.add(a)
        if var == '?t1':
            for a in [x[3] for x in matches if x[0]=='DTIME']:
                answer.add(a)
        if var == '?t2':
            for a in [x[3] for x in matches if x[0]=='ATIME']:
                answer.add(a)
        if var == '?t3':
            for a in [x[4] for x in matches if x[0]=='RUN-TIME']:
                answer.add(a)
        answers_dict.update({var:list(answer)})
    
    return answers_dict

def draw_answer(answers_dict):
    def list2string_vars_question(l):
        s = ''
        for e in l:
            s += e + ', '
        return s[:-2]
    res = ''
    for key in answers_dict.keys():
        keys1 = ['?f1', '?t1', '?t2', '?t3', '?c1', '?c2']
        keys2 = ['Flights', 'Depart Time', 'Arrive Time', 'Run Time', 'Source', 'Destination']
        res += f'{keys2[keys1.index(key)]}: {list2string_vars_question(answers_dict[key])}\n'
    return res



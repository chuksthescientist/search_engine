from qualifiers import qualifiers_database
import re
import json

dmeshFile = '../data/d2021.bin'
qmeshFile = '../data/q2021.bin'
cmeshFile = '../data/c2021.bin'
cdmeshFile = '../data/c2021_disease.bin'

# descriptors
with open(dmeshFile, mode='rb') as file:
    dmesh = file.readlines()

# qualifiers
with open(qmeshFile, mode='rb') as file:
    qmesh = file.readlines()

# Supplementary Records
with open(cmeshFile, mode='rb') as file:
    cmesh = file.readlines()

# Supplementary Records - Diseases
with open(cdmeshFile, mode='rb') as file:
    cdmesh = file.readlines()


def get_qualifiers(record):
    temp = {}
    for line in record.split(b'\n'):
        entry = re.search(b' SH = (.+)$', line)
        if entry:
            term = entry.group(1)
            temp['identifier'] = term.decode('utf-8')

        entry = re.search(b' QX = (.+)$', line)
        if entry:
            term = entry.group(1)
            if 'synonyms' in temp:
                temp['synonyms'].append(term.decode('utf-8').split('|')[0])
            else:
                temp['synonyms'] = [term.decode('utf-8').split('|')[0]]

        ui = re.search(b' UI = (.+)$', line)
        if ui:
            term = ui.group(1)
            temp['mesh_id'] = term.decode('utf-8')

    if 'identifier' not in temp:
        temp['identifier'] = ""
    if 'synonyms' not in temp:
        temp['synonyms'] = []
    if 'mesh_id' not in temp:
        temp['mesh_id'] = []

    return temp


def get_scr(record):
    temp = {}
    for line in record.split(b'\n'):
        entry = re.search(b' NM = (.+)$', line)
        if entry:
            term = entry.group(1)
            temp['identifier'] = term.decode('utf-8')

        entry = re.search(b' SY = (.+)$', line)
        if entry:
            term = entry.group(1)
            if 'synonyms' in temp:
                temp['synonyms'].append(term.decode('utf-8').split('|')[0])
            else:
                temp['synonyms'] = [term.decode('utf-8').split('|')[0]]

        pa = re.search(b' PA = (.+)$', line)
        if pa:
            term = pa.group(1)
            if 'pharmalogical_actions' in temp:
                temp['pharmalogical_actions'].append(term.decode('utf-8'))
            else:
                temp['pharmalogical_actions'] = [term.decode('utf-8')]

        ui = re.search(b' UI = (.+)$', line)
        if ui:
            term = ui.group(1)
            temp['mesh_id'] = term.decode('utf-8')

    if 'identifier' not in temp:
        temp['identifier'] = ""
    if 'synonyms' not in temp:
        temp['synonyms'] = []
    if 'pharmalogical_actions' not in temp:
        temp['pharmalogical_actions'] = []
    if 'mesh_id' not in temp:
        temp['mesh_id'] = []

    return temp


def get_descriptors(record):
    temp = {}
    for line in record.split(b'\n'):
        qualifiers = re.search(b' AQ = (.+)$', line)
        if qualifiers:
            term = qualifiers.group(1)
            temp['subheads'] = []
            temp['subheads_synonyms'] = []
            for t in term.decode('utf-8').split():
                temp['subheads'].append(qualifiers_database[t])
                temp['subheads_synonyms'].extend(qualifiers_synoymns[t]['synonyms'])

        entry = re.search(b' ENTRY = (.+)$', line)
        if entry:
            term = entry.group(1)
            if 'synonyms' in temp:
                temp['synonyms'].append(term.decode('utf-8').split('|')[0])
            else:
                temp['synonyms'] = [term.decode('utf-8').split('|')[0]]

        tree_no = re.search(b' MN = (.+)$', line)
        if tree_no:
            term = tree_no.group(1)
            temp['tree_no'] = term.decode('utf-8')

        ui = re.search(b' UI = (.+)$', line)
        if ui:
            term = ui.group(1)
            temp['mesh_id'] = term.decode('utf-8')

        pa = re.search(b' PA = (.+)$', line)
        if pa:
            term = pa.group(1)
            if 'pharmalogical_actions' in temp:
                temp['pharmalogical_actions'].append(term.decode('utf-8'))
            else:
                temp['pharmalogical_actions'] = [term.decode('utf-8')]

        fx = re.search(b' FX = (.+)$', line)
        if fx:
            term = fx.group(1)
            if 'cross_reference' in temp:
                temp['cross_reference'].append(term.decode('utf-8'))
            else:
                temp['cross_reference'] = [term.decode('utf-8')]

        ec = re.search(b' EC = (.+)$', line)
        if ec:
            term = ec.group(1)
            if 'synonym_combination' in temp:
                temp['synonym_combination'].append(term.decode('utf-8'))
            else:
                temp['synonym_combination'] = [term.decode('utf-8')]

    if 'subheads' not in temp:
        temp['subheads'] = []
    if 'synonyms' not in temp:
        temp['synonyms'] = []
    if 'tree_no' not in temp:
        temp['tree_no'] = []
    if 'mesh_id' not in temp:
        temp['mesh_id'] = []
    if 'pharmalogical_actions' not in temp:
        temp['pharmalogical_actions'] = []
    if 'cross_reference' not in temp:
        temp['cross_reference'] = []
    if 'synonym_combination' not in temp:
        temp['synonym_combination'] = []

    return temp


if __name__ == "__main__":
    qualifiers_records = b" ".join(qmesh).split(b'*NEWRECORD')[1:]
    qualifiers_synoymns = {}
    for record in qualifiers_records:
        for line in record.split(b'\n'):
            qtype = re.search(b'QA = (.+)$', line)
            if qtype:
                term = qtype.group(1)
                qualifiers_synoymns[term.decode('utf-8')] = get_qualifiers(record)
                break

    scr_records = b" ".join(cmesh).split(b'*NEWRECORD')[1:]
    scr_records.extend(b" ".join(cdmesh).split(b'*NEWRECORD')[1:])
    scr_synoymns = {}
    for record in scr_records:
        for line in record.split(b'\n'):
            ctype = re.search(b' HM = (.+)$', line)
            if ctype:
                term = ctype.group(1)
                recrd = get_scr(record)
                for trm in term.decode('utf-8').split('/'):
                    scr_synoymns[trm.split('-')[-1].strip()] = recrd
                break

    records = b" ".join(dmesh).split(b'*NEWRECORD')[1:]
    mesh_database = {}
    for record in records:
        for line in record.split(b'\n'):
            dtype = re.search(b'MH = (.+)$', line)
            if dtype:
                term = dtype.group(1)
                mesh_database[term.decode('utf-8')] = get_descriptors(record)
                if term.decode('utf-8') in scr_synoymns:
                    if scr_synoymns[term.decode('utf-8')]['synonyms']:
                        mesh_database[term.decode('utf-8')]['synonyms'].extend(
                            scr_synoymns[term.decode('utf-8')]['synonyms'])
                    if scr_synoymns[term.decode('utf-8')]['identifier']:
                        mesh_database[term.decode('utf-8')]['synonyms'].append(
                            scr_synoymns[term.decode('utf-8')]['identifier'])
                    if scr_synoymns[term.decode('utf-8')]['pharmalogical_actions']:
                        mesh_database[term.decode('utf-8')]['pharmalogical_actions'].extend(
                            scr_synoymns[term.decode('utf-8')]['pharmalogical_actions'])
                break

    with open('../data/mesh_database.json', 'w') as f:
        json.dump(mesh_database, f)

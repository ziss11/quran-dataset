import codecs
import json
import re


def load_json(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        data = json.load(f)

    return data


def build_verses():
    quran_id_path = 'old/quran_id.json'
    quran_en_path = 'old/quran_en.json'

    data_id = load_json(quran_id_path)
    data_en = load_json(quran_en_path)

    new_verses = list()

    for idn, en in zip(data_id, data_en):
        idn_verses = idn['verses']
        en_verses = en['verses']

        new_data_list = list()
        for idn_verse, en_verse in zip(idn_verses, en_verses):
            new_data = {'text': idn_verse['text'],
                        'translation': {
                            'idn': idn_verse['translation'],
                            'en': en_verse['translation']}}
            new_data_list.append(new_data)

        verse_model = {'id': idn['id'], 'data': new_data_list}
        new_verses.append(verse_model)

    return {'verses': new_verses}


def build_surah():
    quran1_path = 'old/quran.json'
    quran2_path = 'old/quran_id.json'
    juz_path = 'old/juz.json'

    surah1_json = load_json(quran1_path)
    surah2_json = load_json(quran2_path)
    juz_json = load_json(juz_path)

    unused_columns = ['recitation', 'place',
                      'number_of_surah', 'number_of_ayah']
    new_surah = list()

    for juz in juz_json:
        start = int(juz['start']['index'])
        end = int(juz['end']['index'])

        for surah1, surah2 in zip(surah1_json, surah2_json):
            en_revelation = ''
            id_revelation = ''

            if surah1['place'] == 'Mecca':
                en_revelation = 'Mecca'
                id_revelation = 'Mekkah'
            elif surah1['place'] == 'Medina':
                en_revelation = 'Medina'
                id_revelation = 'Madinah'

            surah1['name'] = surah2['transliteration']

            new = {'id': surah1['number_of_surah'],
                   'total_verse': surah1['number_of_ayah'],
                   'revelation': {'en': en_revelation, 'id': id_revelation}}

            new.update(surah1)
            new_surah.append(new)

    for surah in new_surah:
        for column in unused_columns:
            surah.pop(column)

    return {'surah': new_surah}


def build_juz():
    juz_path = 'old/juz.json'
    surah_path = 'data/new_surah.json'

    juz_json = load_json(juz_path)
    surah_json = load_json(surah_path)

    new_juz = list()

    for juz in juz_json:
        start = int(juz['start']['index'])
        end = int(juz['end']['index'])

        selected_surah = [surah_json['surah'][i] for i in range(start-1, end)]

        start_verse = re.findall(r'[0-9]+', juz['start']['verse'])[0]
        end_verse = re.findall(r'[0-9]+', juz['end']['verse'])[0]

        juz_model = {'id': int(juz['index']),
                     'start_surah': selected_surah[0]['name'],
                     'start_verse': start_verse,
                     'end_surah': selected_surah[len(selected_surah)-1]['name'],
                     'end_verse': end_verse,
                     'surah': selected_surah}

        new_juz.append(juz_model)

    return {'juz': new_juz}


if __name__ == '__main__':
    juz = build_juz()
    # surah = build_surah()
    # verses = build_verses()

    with codecs.open('data/new_juz.json', 'w', 'utf-8') as f:
        f.write(json.dumps(juz, ensure_ascii=False))

    # with codecs.open('data/new_surah.json', 'w', 'utf-8') as f:
    #     f.write(json.dumps(surah, ensure_ascii=False))

    # with codecs.open('data/new_verse.json', 'w', 'utf-8') as f:
    #     f.write(json.dumps(verses, ensure_ascii=False))
